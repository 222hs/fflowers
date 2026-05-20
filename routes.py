# routes.py — Flask routes (webhook, dashboard, expenses, SSE, parse)
# UPDATED: bank-balance delete/reset, auto-insight after save, Muscat-tz daily total fix
import os, json, threading, time, datetime, re, queue
import secrets as _secrets
from urllib.parse import unquote
from flask import Blueprint, request, jsonify, send_from_directory, Response, stream_with_context, session, redirect
import requests
from google.cloud.firestore_v1 import FieldFilter as _FF

from config import BOT_TOKEN, ALLOWED_CHAT_IDS, ADMIN_CHAT_ID, PASSWORD, ADMIN_UID
from firebase import firebase_db, broadcast_event, _sse_clients, _preview_clients, _sse_lock
from ai_engine import hybrid_parse, extract_gps_from_text, PROVIDERS, generate_daily_insight
from db_helpers import _muscat_today, _muscat_month
from regex_templates import generate_regex_for_text, save_regex_template
# BUG FIX: import db_helpers module (not individual functions) so the
# monkey-patched save_expense from app.py is resolved at call-time,
# not frozen at import-time.
import db_helpers as _db_helpers
from db_helpers import (get_expenses_firebase, get_expenses_sqlite_fast,
                        get_bank_balances_sqlite, _bb_cache_invalidate,
                        get_daily_total_firebase, save_raw_message, get_raw_messages)

def save_expense(*args, **kwargs):
    """Thin shim — always delegates to the (possibly monkey-patched) module-level function."""
    return _db_helpers.save_expense(*args, **kwargs)

bp = Blueprint('main', __name__)
app = bp   # alias so existing @app.route() decorators keep working

# ── Auth routes ──────────────────────────────────────────────────────────

@app.route("/login")
def login_page():
    if session.get("authed"):
        return redirect("/")
    return send_from_directory(".", "login.html")

@app.route("/auth/popup")
def auth_popup():
    """Same-origin OAuth popup — bypasses COOP isolation between Google and our domain."""
    return send_from_directory(".", "auth_popup.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json or {}
    if data.get("password") == PASSWORD:
        session["authed"] = True
        session.permanent = True
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "كلمة المرور غير صحيحة"}), 401

@app.route("/api/logout", methods=["POST", "GET"])
def api_logout():
    from flask import current_app
    session.clear()
    session.modified = True
    resp = redirect("/login")
    # احذف الكوكي بنفس الإعدادات التي أُنشئ بها بالضبط
    cookie_name = current_app.config.get("SESSION_COOKIE_NAME", "session")
    resp.set_cookie(
        cookie_name, "",
        max_age=0, expires=0,
        path=current_app.config.get("SESSION_COOKIE_PATH", "/"),
        domain=current_app.config.get("SESSION_COOKIE_DOMAIN"),
        secure=current_app.config.get("SESSION_COOKIE_SECURE", False),
        httponly=current_app.config.get("SESSION_COOKIE_HTTPONLY", True),
        samesite=current_app.config.get("SESSION_COOKIE_SAMESITE", "Lax"),
    )
    return resp

@app.route("/api/auth/google", methods=["POST"])
def api_auth_google():
    """Verify Firebase ID token from Google Sign-In and create session."""
    data = request.json or {}
    id_token = data.get("idToken", "").strip()
    if not id_token:
        return jsonify({"ok": False, "error": "missing token"}), 400
    try:
        import firebase_admin.auth as _fb_auth
        decoded = _fb_auth.verify_id_token(id_token)
        real_uid = decoded["uid"]
        email    = decoded.get("email", "")
        name     = decoded.get("name", "")

        # ── إذا كان هذا حساب الأدمن، نستخدم ADMIN_UID ثابتاً ──────────
        # هذا يضمن أن الأدمن يقرأ دائماً من SQLite + Firebase admin path
        uid = ADMIN_UID if real_uid == ADMIN_UID else real_uid

        session["authed"]   = True
        session["uid"]      = uid
        session["email"]    = email
        session["name"]     = name
        session["is_admin"] = (uid == ADMIN_UID)
        session.permanent   = True

        # ── Background: profile upsert + auto-create first webhook token ────
        if firebase_db:
            def _bg_login_tasks(_uid, _email, _name):
                try:
                    now = datetime.datetime.now().isoformat()
                    # 1. Upsert profile
                    ref = firebase_db.collection("users").document(_uid)
                    doc = ref.get()
                    if not doc.exists:
                        ref.set({"uid": _uid, "email": _email, "name": _name, "created_at": now, "last_login": now})
                        print(f"[Auth] 🆕 Created profile: {_email}", flush=True)
                    else:
                        ref.update({"last_login": now, "email": _email, "name": _name})
                    # 2. Auto-create first webhook token if user has none
                    import secrets as _sec
                    from google.cloud.firestore_v1 import FieldFilter as _FFl
                    existing = list(firebase_db.collection("webhook_tokens")
                                    .where(filter=_FFl("uid", "==", _uid))
                                    .limit(1).stream())
                    if not existing:
                        tok = _sec.token_urlsafe(32)
                        firebase_db.collection("webhook_tokens").document(tok).set({
                            "uid": _uid, "label": "الجهاز الرئيسي", "created_at": now
                        })
                        print(f"[Auth] 🔑 Auto-created token for {_email}", flush=True)
                except Exception as _fe:
                    print(f"[Auth] ⚠️ bg_login_tasks: {_fe}", flush=True)
            threading.Thread(target=_bg_login_tasks, args=(uid, email, name), daemon=True).start()

        is_admin = (uid == ADMIN_UID)
        print(f"[Auth] ✅ Google sign-in: {email} (uid={uid}, admin={is_admin})", flush=True)
        return jsonify({"ok": True, "uid": uid, "name": name, "is_admin": is_admin})
    except Exception as e:
        print(f"[Auth] ❌ Token verify failed: {e}", flush=True)
        return jsonify({"ok": False, "error": str(e)}), 401

def _resolve_uid_from_token(token_str):
    """Look up uid from a webhook token in Firebase. Returns None if invalid."""
    if not token_str or not firebase_db:
        return None
    try:
        doc = firebase_db.collection("webhook_tokens").document(token_str).get()
        if doc.exists:
            return doc.to_dict().get("uid")
        return None
    except Exception:
        return None

def _get_token_uid():
    uid = session.get("uid")
    if uid:
        return uid
    if session.get("authed"):
        return ADMIN_UID
    return None

@app.route("/api/tokens", methods=["GET"])
def api_tokens_list():
    uid = _get_token_uid()
    if not uid:
        return jsonify({"ok": False, "error": "login required"}), 401
    if not firebase_db:
        return jsonify({"ok": True, "tokens": []})
    try:
        from google.cloud.firestore_v1 import FieldFilter as _FFt
        docs = (firebase_db.collection("webhook_tokens")
                .where(filter=_FFt("uid", "==", uid))
                .stream())
        tokens = [{"token": doc.id, **doc.to_dict()} for doc in docs]
        tokens.sort(key=lambda x: x.get("created_at",""), reverse=True)
        return jsonify({"ok": True, "tokens": tokens})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/tokens", methods=["POST"])
def api_tokens_create():
    uid = _get_token_uid()
    if not uid:
        return jsonify({"ok": False, "error": "login required"}), 401
    if not firebase_db:
        return jsonify({"ok": False, "error": "Firebase not connected"}), 500
    data = request.json or {}
    label = data.get("label", "").strip() or "جهازي"
    token = _secrets.token_urlsafe(32)
    now = datetime.datetime.now().isoformat()
    try:
        firebase_db.collection("webhook_tokens").document(token).set({
            "uid": uid, "label": label, "created_at": now
        })
        return jsonify({"ok": True, "token": token, "label": label})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/tokens/<token>", methods=["DELETE"])
def api_tokens_delete(token):
    uid = _get_token_uid()
    if not uid:
        return jsonify({"ok": False, "error": "login required"}), 401
    if not firebase_db:
        return jsonify({"ok": False, "error": "Firebase not connected"}), 500
    try:
        doc = firebase_db.collection("webhook_tokens").document(token).get()
        if doc.exists and doc.to_dict().get("uid") == uid:
            firebase_db.collection("webhook_tokens").document(token).delete()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/preview-stream")
def api_preview_stream():
    """Public SSE — emits only data_changed pings, no financial data."""
    import queue as _queue
    q = _queue.Queue(maxsize=20)
    with _sse_lock:
        _preview_clients.append(q)

    def generate():
        try:
            yield 'data: {"type":"connected"}\n\n'
            deadline = time.time() + 270
            while time.time() < deadline:
                try:
                    msg = q.get(timeout=5)
                    yield msg
                except _queue.Empty:
                    yield ": ping\n\n"
            yield "event: reconnect\ndata: {}\n\n"
        except GeneratorExit:
            pass
        finally:
            with _sse_lock:
                if q in _preview_clients:
                    _preview_clients.remove(q)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Access-Control-Allow-Origin': '*',
        }
    )

@app.route("/api/login-preview")
def api_login_preview():
    """Public endpoint — returns bank balances and last transaction for the login page preview."""
    try:
        from db_helpers import get_bank_balances_sqlite, get_expenses_sqlite_fast
        banks_raw = get_bank_balances_sqlite(uid=ADMIN_UID)
        banks = [
            {
                "bank_name":  b.get("bank_name") or b.get("account_id") or "بنك",
                "account_id": b.get("account_id", ""),
                "balance":    float(b.get("balance") or 0),
                "currency":   b.get("currency", "OMR"),
            }
            for b in (banks_raw or [])
        ]
        # Last transaction from Firebase
        last_tx = None
        try:
            exps = get_expenses_sqlite_fast(limit=1, uid=ADMIN_UID)
            if exps:
                e = exps[0]
                last_tx = {
                    "name":      e.get("name") or e.get("bank_name") or "معاملة",
                    "amount":    float(e.get("amount") or 0),
                    "currency":  e.get("currency", "OMR"),
                    "category":  e.get("category", "other"),
                    "bank_name": e.get("bank_name", ""),
                    "date":      (e.get("date") or "")[:10],
                }
        except Exception:
            pass
        return jsonify({"banks": banks, "last_tx": last_tx})
    except Exception as ex:
        return jsonify({"banks": [], "last_tx": None, "error": str(ex)})

# ── Main app ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/static/banks/<path:filename>")
def bank_static(filename):
    return send_from_directory("static/banks", filename)

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


@app.route("/health")
def health():
    providers_status = {}
    for p in PROVIDERS:
        total = len(p["keys"])
        active = sum(1 for v in p["key_states"].values() if not v["depleted"])
        if total > 0:
            providers_status[p["name"]] = {"total": total, "active": active}
    return jsonify({
        "status": "ok",
        "bot": bool(BOT_TOKEN),
        "db_firebase": firebase_db is not None,
        "db_sqlite": False,
        "ai_providers": providers_status,
        "hybrid_parsing": True,
    })

# ── Emergency DB reset (no-op in Firebase-only mode) ──
@app.route("/api/admin/reset-db", methods=["POST"])
def admin_reset_db():
    if request.json.get("password") != PASSWORD:
        return jsonify({"ok": False, "error": "unauthorized"}), 403
    return jsonify({"ok": True, "message": "Firebase-only mode — no local DB to reset"})

# ── Unified Webhook (Telegram + iOS Shortcut) ──
@app.route("/webhook", methods=["POST"])
@app.route("/api/webhook", methods=["POST"])
def webhook():
    """
    Single entry-point for both:
      • Telegram bot updates (message / callback_query from long-polling or webhook)
      • iOS Shortcut payloads  {"sms_text": "...", "latitude": ..., "longitude": ..., "chat_id": ...}
    """
    from decimal import Decimal as _D

    PRIMARY_NOTIFY_ID = 7319712950   # always receives a confirmation

    # force=True so we parse JSON even if Content-Type is missing/wrong (iOS Shortcut issue)
    data = request.get_json(force=True, silent=True)
    if not data:
        # Try form data fallback (some shortcuts send form-encoded)
        raw = request.data
        if raw:
            try:
                import json as _json
                data = _json.loads(raw)
            except Exception:
                pass
    if not data:
        print("[WEBHOOK] ⚠️  Empty or unparseable body received")
        print(f"[WEBHOOK] Content-Type: {request.content_type}, Body: {request.data[:200]}")
        return jsonify({"ok": True})

    print(f"[WEBHOOK] Received — Content-Type: {request.content_type} — keys: {list(data.keys())}", flush=True)

    # ── A) iOS Shortcut payload ────────────────────────────────────────
    _raw_text = (data.get("sms_text") or data.get("text") or "").strip()

    if _raw_text and "message" not in data:
        sms_text = _raw_text
        ios_lat  = data.get("latitude")
        ios_lon  = data.get("longitude")

        chat_id = data.get("chat_id") or ADMIN_CHAT_ID or None
        if chat_id:
            try:
                chat_id = int(str(chat_id).strip())
            except (ValueError, TypeError):
                chat_id = None

        _token = data.get("token", "").strip()
        _shortcut_uid = _resolve_uid_from_token(_token) or ADMIN_UID

        print(f"[SHORTCUT] {len(sms_text)} chars  chat_id={chat_id}  uid={_shortcut_uid}", flush=True)

        # Save raw message immediately
        save_raw_message(chat_id or "shortcut", sms_text, source="ios_shortcut", uid=_shortcut_uid)

        def _safe_coord(v):
            if v is None:
                return None
            try:
                return float(_D(str(v)))
            except Exception:
                return float(v)

        ios_lat_f = _safe_coord(ios_lat)
        ios_lon_f = _safe_coord(ios_lon)

        def _send_tg_error(bot_token, targets, msg):
            """Send an error notification to Telegram targets."""
            if not bot_token:
                return
            for _t in targets:
                try:
                    requests.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={"chat_id": _t, "text": msg, "parse_mode": "HTML"},
                        timeout=10,
                    )
                except Exception:
                    pass

        def _bg_full(sms_text, ios_lat_f, ios_lon_f, chat_id, bot_token, primary_id, shortcut_uid=None):
            """Parse + save + Telegram — all in background so webhook returns instantly."""
            _tg_targets = {primary_id, *([] if not chat_id else [chat_id])}
            try:
                print(f"[SHORTCUT] 🔄 BG: parsing...", flush=True)
                parsed, extracted_lat, extracted_lon, map_url = hybrid_parse(sms_text)

                # Validate: need amount > 0 AND a non-empty vendor name
                _vendor_check = (parsed or {}).get("merchant") or (parsed or {}).get("name") or ""
                _amount_check = float((parsed or {}).get("amount", 0) or 0)
                if not parsed or _amount_check <= 0 or not _vendor_check.strip():
                    print(f"[SHORTCUT] ❌ Parse failed — amount={_amount_check} vendor={_vendor_check!r}", flush=True)
                    preview = sms_text[:200].replace("<","&lt;").replace(">","&gt;")
                    _send_tg_error(bot_token, _tg_targets,
                        f"⚠️ <b>Shortcut: لم أستطع تحليل هذه الرسالة</b>\n\n<code>{preview}</code>")
                    return

                try:
                    parsed["amount"] = float(_D(str(parsed["amount"])))
                except Exception:
                    pass

                final_lat = ios_lat_f if ios_lat_f is not None else extracted_lat
                final_lon = ios_lon_f if ios_lon_f is not None else extracted_lon

                vendor_name = parsed.get("merchant") or parsed.get("name") or "غير معروف"
                print(f"[SHORTCUT] 💾 Saving: {vendor_name!r} {parsed.get('amount')}", flush=True)
                try:
                    doc = save_expense(parsed, "ios_shortcut",
                                       latitude=final_lat, longitude=final_lon,
                                       map_url=map_url, raw_text=sms_text, chat_id=chat_id,
                                       uid=shortcut_uid or ADMIN_UID)
                except Exception as _save_err:
                    import traceback as _tb
                    print(f"[SHORTCUT] ❌ save_expense failed: {_save_err}", flush=True)
                    print(_tb.format_exc(), flush=True)
                    _send_tg_error(bot_token, _tg_targets,
                        f"❌ <b>Shortcut: خطأ أثناء حفظ المعاملة</b>\n\n"
                        f"المتجر: <b>{vendor_name}</b>\n"
                        f"المبلغ: <b>{parsed.get('amount')} OMR</b>\n\n"
                        f"<code>{str(_save_err)[:200]}</code>")
                    return

                print(f"[SHORTCUT] ✅ Saved: {doc.get('name')} {float(doc.get('amount',0)):.3f}", flush=True)

                _trigger_insight_refresh(doc)

                if not bot_token:
                    return

                vendor   = doc.get("name", "غير معروف")
                amount   = float(doc.get("amount", 0.0))
                currency = doc.get("currency", "OMR")
                parse_method = parsed.get("parse_method", "ai")
                ai_provider  = parsed.get("ai_provider", "")
                PROVIDER_ICONS = {"Grok":"⚡ Grok","DeepSeek":"🌊 DeepSeek","Gemini":"♊ Gemini","ChatGPT":"🟢 ChatGPT","OpenRouter":"🔀 OpenRouter"}
                METHOD_ICONS  = {"regex":"📐 Regex","template":"📚 Template","learning":"🧠 Learning","fallback":"🔁 Fallback","ai":"🤖 AI"}
                method_tag = (PROVIDER_ICONS.get(ai_provider, f"🤖 {ai_provider}")
                              if parse_method == "ai" and ai_provider
                              else METHOD_ICONS.get(parse_method, "🤖 AI"))

                try:
                    from app import _build_confirmation
                    msg_text, keyboard = _build_confirmation(doc, method_tag)
                except Exception as _bc_err:
                    print(f"[SHORTCUT] ⚠️ _build_confirmation: {_bc_err}", flush=True)
                    em  = CAT_EMOJI.get(doc.get("category","other"), "📦")
                    bal = (f"\n💳 الرصيد: {doc['available_balance']:.3f} {currency}"
                           if doc.get("available_balance") is not None else "")
                    gps = (f"\n📍 {final_lat:.6f}, {final_lon:.6f}"
                           if final_lat is not None and final_lon is not None else "")
                    msg_text = (f"✅ <b>مصروف مسجّل</b>\n\n"
                                f"💰 المبلغ: <b>{amount:.3f} {currency}</b>\n"
                                f"🏪 المتجر: <b>{vendor}</b>\n"
                                f"{em} الفئة: <b>{doc.get('category','other')}</b>\n"
                                f"🏦 {doc.get('bank_name','—')}{bal}{gps}\n"
                                f"📅 {doc.get('date','')}\n\n"
                                f"<i>حُلِّلت بـ: <b>{method_tag}</b></i>")
                    keyboard = None

                for _target in {primary_id, *([] if not chat_id else [chat_id])}:
                    try:
                        payload = {"chat_id": _target, "text": msg_text, "parse_mode": "HTML"}
                        if keyboard:
                            import json as _json
                            payload["reply_markup"] = _json.dumps(keyboard)
                        r = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                                          json=payload, timeout=12)
                        if r.json().get("ok"):
                            print(f"[SHORTCUT] ✅ Telegram → {_target}", flush=True)
                        else:
                            print(f"[SHORTCUT] ❌ Telegram error: {r.json()}", flush=True)
                    except Exception as te:
                        print(f"[SHORTCUT] ❌ Telegram failed → {_target}: {te}", flush=True)

            except Exception as _err:
                import traceback
                print(f"[SHORTCUT] 💥 BG crashed: {_err}", flush=True)
                print(traceback.format_exc(), flush=True)

        threading.Thread(
            target=_bg_full,
            args=(sms_text, ios_lat_f, ios_lon_f, chat_id, BOT_TOKEN, PRIMARY_NOTIFY_ID, _shortcut_uid),
            daemon=True,
        ).start()

        # Return immediately — parse/save/Telegram happen in background
        return jsonify({"ok": True, "queued": True})

    # ── B) Telegram bot update ─────────────────────────────────────────
    if "callback_query" in data:
        try:
            from app import handle_callback_query
            threading.Thread(
                target=handle_callback_query,
                args=(data["callback_query"],),
                daemon=True,
            ).start()
        except Exception as e:
            print(f"[WEBHOOK] callback_query dispatch error: {e}")
        return jsonify({"ok": True})

    msg      = data.get("message", {})
    chat_id  = msg.get("chat", {}).get("id")
    text     = msg.get("text", "")
    loc      = msg.get("location", {})
    lat      = loc.get("latitude")  if loc else None
    lon      = loc.get("longitude") if loc else None

    if chat_id and text:
        print(f"DEBUG: Telegram message from chat_id={chat_id}: {text[:80]!r}")
        if ALLOWED_CHAT_IDS and str(chat_id) not in ALLOWED_CHAT_IDS:
            tg_send(chat_id, "⛔ غير مصرح لك باستخدام هذا البوت")
            return jsonify({"ok": True})
        from telegram_handler import handle_telegram
        threading.Thread(
            target=handle_telegram,
            args=(chat_id, text, lat, lon),
            daemon=True,
        ).start()

    return jsonify({"ok": True})


CAT_EMOJI = {
    "food": "🍕", "shopping": "🛍️", "transport": "🚗", "bills": "📄",
    "health": "💊", "entertainment": "🎮", "education": "📚",
    "groceries": "🛒", "fuel": "⛽", "rent": "🏠",
    "subscriptions": "🔄", "transfer": "💸", "savings": "💰", "other": "📦",
}


def tg_send(chat_id, text, reply_markup=None):
    """Local tg_send for routes.py — avoids importing from telegram_handler."""
    if not BOT_TOKEN:
        return
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        import json as _json
        payload["reply_markup"] = _json.dumps(reply_markup)
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json=payload, timeout=10,
        )
    except Exception as e:
        print(f"[TG] send error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# FIX #3 — Auto daily-insight refresh after every new expense
# Runs in a background thread so it never blocks the response.
# ─────────────────────────────────────────────────────────────────────────────
def _trigger_insight_refresh(doc: dict, uid: str = None):
    """
    After a new expense is saved, asynchronously regenerate today's daily
    insight so the Smart Daily Analytics section stays current.
    Broadcasts an SSE 'daily_insight' event when done.
    """
    _ins_uid = uid or ADMIN_UID
    def _run():
        try:
            today = _muscat_today()
            tx_date = str(doc.get("date", ""))[:10]
            if tx_date and tx_date != today:
                return
            exps = get_expenses_firebase(date_filter=today, uid=_ins_uid)
            if not exps:
                return
            if firebase_db:
                try:
                    firebase_db.collection("daily_insights").document(today).delete()
                except Exception:
                    pass
            insight = generate_daily_insight(exps)
            broadcast_event("daily_insight", {"date": today, "insight": insight}, uid=_ins_uid)
            print(f"[Insight] ✅ Auto-refreshed for {today} (uid={_ins_uid})")
        except Exception as e:
            print(f"[Insight] ⚠️  Auto-refresh error: {e}")
    threading.Thread(target=_run, daemon=True).start()


@app.route("/api/stream")
def sse_stream():
    if not session.get("authed"):
        return Response("data: {\"error\":\"unauthorized\"}\n\n", mimetype='text/event-stream', status=401)
    _stream_uid = session.get("uid") or ADMIN_UID
    q = queue.Queue(maxsize=50)
    entry = {"uid": _stream_uid, "q": q}
    with _sse_lock:
        if len(_sse_clients) >= 20:
            try:
                _sse_clients[0]["q"].put_nowait("event: close\ndata: {}\n\n")
            except Exception:
                pass
            _sse_clients.pop(0)
        _sse_clients.append(entry)
    def generate():
        try:
            yield "data: {\"type\":\"connected\"}\n\n"
            deadline = time.time() + 270  # 4.5 min max per SSE connection
            while time.time() < deadline:
                try:
                    msg = q.get(timeout=5)
                    yield msg
                except queue.Empty:
                    yield ": ping\n\n"
            yield "event: reconnect\ndata: {}\n\n"
        except GeneratorExit:
            pass
        except Exception as e:
            print(f"[SSE] stream error: {e}")
        finally:
            with _sse_lock:
                if entry in _sse_clients:
                    _sse_clients.remove(entry)
    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# ── Days with expenses (for calendar dots) ──
@app.route("/api/expenses/active-days")
def api_active_days():
    """Return list of YYYY-MM-DD dates that have at least one expense, for a given month."""
    month = request.args.get("month", _muscat_month())  # e.g. "2026-05"
    _uid = session.get("uid") or ADMIN_UID
    days = set()
    try:
        exps = get_expenses_sqlite_fast(month_filter=month, limit=1000, uid=_uid)
        for e in exps:
            d = e.get("date_only") or str(e.get("date", ""))[:10]
            if d and d.startswith(month):
                days.add(d)
    except Exception as e:
        print(f"[active-days] error: {e}")
    return jsonify(sorted(days))

# ── Expenses API ──
@app.route("/api/expenses")
def api_expenses():
    month = request.args.get("month", _muscat_month())
    date  = request.args.get("date", "")
    limit = int(request.args.get("limit", 500))
    _uid = session.get("uid") or ADMIN_UID
    if date:
        return jsonify(get_expenses_sqlite_fast(date_filter=date, limit=limit, uid=_uid))
    return jsonify(get_expenses_sqlite_fast(month_filter=month, limit=limit, uid=_uid))

@app.route("/api/expenses/map")
def api_expenses_map():
    month = request.args.get("month", _muscat_month())
    _uid  = session.get("uid") or ADMIN_UID
    from firebase import user_col
    if not firebase_db:
        return jsonify([])
    try:
        month_start = month + "-01"
        month_end   = month + "-32"
        docs = (user_col(_uid, "expenses")
                .where(filter=_FF("date_only", ">=", month_start))
                .where(filter=_FF("date_only", "<=", month_end))
                .limit(500).stream())
        pins = []
        for doc in docs:
            d = doc.to_dict(); d["id"] = doc.id
            lat = d.get("latitude"); lon = d.get("longitude")
            if lat is None or lon is None:
                continue
            try:
                d["latitude"] = float(lat); d["longitude"] = float(lon)
                pins.append(d)
            except (TypeError, ValueError):
                pass
        return jsonify(pins)
    except Exception as e:
        print(f"[map] Firebase error: {e}")
        return jsonify([])

@app.route("/api/expense", methods=["POST"])
def api_add():
    data = request.json
    if not data.get("name") or not data.get("amount"):
        return jsonify({"error": "missing fields"}), 400
    lat = data.get("latitude")
    lon = data.get("longitude")
    map_url = data.get("map_url")
    try:
        lat = float(lat) if lat is not None else None
        lon = float(lon) if lon is not None else None
    except (TypeError, ValueError):
        lat = lon = None
    doc = save_expense(data, data.get("source", "manual"),
                       latitude=lat, longitude=lon, map_url=map_url,
                       uid=session.get("uid") or ADMIN_UID)
    # FIX #3: also refresh insight for manually added expenses
    _trigger_insight_refresh(doc)
    # FIX #4: tell frontend a fresh fetch is needed
    resp = jsonify(doc)
    resp.headers["X-Data-Updated"] = "true"
    return resp

@app.route("/api/expense/<eid>", methods=["DELETE"])
def api_delete(eid):
    _del_uid = session.get("uid") or ADMIN_UID
    # Grab the expense date before deleting so we can recompute the daily total
    expense_date = None
    if firebase_db:
        try:
            from firebase import user_col
            snap = user_col(_del_uid, "expenses").document(eid).get()
            if snap.exists:
                expense_date = str(snap.to_dict().get("date", "") or "")[:10]
            user_col(_del_uid, "expenses").document(eid).delete()
        except Exception:
            pass

    from db_helpers import exp_cache_invalidate
    exp_cache_invalidate(session.get("uid") or ADMIN_UID)

    _del_ev_uid = session.get("uid") or ADMIN_UID
    broadcast_event("expense_deleted", {"id": eid}, uid=_del_ev_uid)

    today_str = _muscat_today()
    if not expense_date:
        expense_date = today_str
    new_daily = get_daily_total_firebase(expense_date, uid=_del_ev_uid)
    broadcast_event("daily_total", {"date": expense_date, "total": new_daily}, uid=_del_ev_uid)
    broadcast_event("refresh_dashboard", {"reason": "expense_deleted", "id": eid}, uid=_del_ev_uid)

    return jsonify({"ok": True})

@app.route("/api/expense/<eid>", methods=["PUT"])
def api_edit(eid):
    data = request.json or {}
    allowed = ["name","amount","currency","category","date","notes","bank_name","available_balance","sender","type","parse_method"]
    update = {k: data[k] for k in allowed if k in data}
    if not update:
        return jsonify({"error": "no valid fields"}), 400

    # Coerce amount to float via Decimal to preserve precision
    if "amount" in update:
        from decimal import Decimal, InvalidOperation
        try:
            update["amount"] = float(Decimal(str(update["amount"])))
        except (InvalidOperation, Exception):
            update["amount"] = float(update["amount"])

    # ── 1. Read old name before any changes ───────────────────────────────
    old_name = None
    name_changed = False
    import datetime as _dt
    _now = _dt.datetime.utcnow().isoformat()
    _edit_pre_uid = session.get("uid") or ADMIN_UID
    if "name" in update and firebase_db:
        try:
            from firebase import user_col as _uc_pre
            snap = _uc_pre(_edit_pre_uid, "expenses").document(eid).get()
            if snap.exists:
                old_row_name = (snap.to_dict().get("name") or "").strip()
                if old_row_name and old_row_name != update["name"]:
                    old_name = old_row_name
                    name_changed = True
        except Exception:
            pass

    # ── 2. Broadcast SSE immediately ──────────────────────────────────────
    _edit_uid = _edit_pre_uid
    preferred = update["name"].strip() if name_changed else None
    broadcast_event("expense_edited", {"id": eid, "updates": update}, uid=_edit_uid)
    if name_changed:
        broadcast_event("names_bulk_updated", {"old": old_name, "new": preferred}, uid=_edit_uid)

    # ── 3. Firebase writes in background — never block the response ────────
    def _firebase_sync(eid, update, name_changed, old_name):
        if not firebase_db:
            return
        # Update this expense (user-scoped path)
        try:
            from firebase import user_col as _uc
            _sync_uid = session.get("uid") or ADMIN_UID
            _uc(_sync_uid, "expenses").document(eid).update(update)
        except Exception as e:
            print(f"[Firebase] edit sync (expenses): {e}")

        if not name_changed:
            return
        preferred    = update["name"].strip()
        original_key = old_name.lower()
        # Save override
        try:
            firebase_db.collection("merchant_name_overrides").document(original_key).set({
                "original_name": old_name,
                "preferred_name": preferred,
                "updated_at": _now
            })
        except Exception as e:
            print(f"[Firebase] merchant_name_override save: {e}")
        # Bulk rename matching docs (user-scoped)
        try:
            from firebase import user_col as _uc
            _rename_uid = session.get("uid") or ADMIN_UID
            for d in _uc(_rename_uid, "expenses").where(filter=_FF("name", "==", old_name)).stream():
                try:
                    d.reference.update({"name": preferred})
                except Exception:
                    pass
        except Exception as e:
            print(f"[Firebase] bulk name update (expenses): {e}")

    threading.Thread(target=_firebase_sync, args=(eid, update, name_changed, old_name), daemon=True).start()

    return jsonify({"ok": True, "id": eid})

# ── Bank Balances ──
@app.route("/api/bank-balances")
def api_bank_balances():
    _uid = session.get("uid") or ADMIN_UID
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TE
    with ThreadPoolExecutor(max_workers=1) as _ex:
        try:
            result = _ex.submit(get_bank_balances_sqlite, _uid).result(timeout=8)
            return jsonify(result or [])
        except _TE:
            print(f"[BankBalances] ⚠️ timeout for uid={_uid}")
            return jsonify([])
        except Exception as e:
            print(f"[BankBalances] ❌ error: {e}")
            return jsonify([])


# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 — Bank balance delete / reset endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/bank-balances/<path:account_id>", methods=["DELETE"])
def api_delete_bank_balance(account_id):
    """Permanently remove a bank account balance record from Firestore."""
    account_id = unquote(account_id)
    print(f"[Balance] DELETE requested for account_id={account_id!r}")
    _del_uid = session.get("uid") or ADMIN_UID
    fb_deleted = False
    if firebase_db:
        try:
            from firebase import user_col
            ref  = user_col(_del_uid, "bank_balances").document(account_id)
            snap = ref.get()
            if snap.exists:
                ref.delete()
                fb_deleted = True
                print(f"[Balance] Firestore deleted: {account_id!r}")
            else:
                print(f"[Balance] Firestore doc not found: {account_id!r}")
        except Exception as e:
            print(f"[Balance] Firestore delete error: {e}")
    _bb_cache_invalidate(_del_uid)
    if fb_deleted:
        broadcast_event("balance_deleted", {"account_id": account_id}, uid=_del_uid)
        print(f"[Balance] SSE balance_deleted broadcast for {account_id!r}")
    status_code = 200 if fb_deleted else 404
    return jsonify({"ok": fb_deleted, "account_id": account_id}), status_code


@app.route("/api/bank-balances/<path:account_id>/reset", methods=["POST"])
def api_reset_bank_balance(account_id):
    """Set a bank account balance to zero (Firebase-only)."""
    account_id = unquote(account_id)
    print(f"[Balance] RESET requested for account_id={account_id!r}")
    now = datetime.datetime.now().isoformat()
    _reset_uid = session.get("uid") or ADMIN_UID
    firebase_error = None
    if not firebase_db:
        return jsonify({"ok": False, "error": "Firebase not connected"}), 500
    try:
        from firebase import user_col
        ref  = user_col(_reset_uid, "bank_balances").document(account_id)
        snap = ref.get()
        if not snap.exists:
            return jsonify({"ok": False, "error": "account not found"}), 404
        ref.update({"balance": 0.0, "updated_at": now})
        print(f"[Balance] ✅ Firestore balance reset for {account_id!r}")
    except Exception as e:
        firebase_error = str(e)
        print(f"[Balance] ❌ Firestore reset error for {account_id!r}: {firebase_error}")
        return jsonify({"ok": False, "error": firebase_error}), 500
    _bb_cache_invalidate(_reset_uid)
    payload = {"account_id": account_id, "balance": 0.0, "updated_at": now}
    broadcast_event("balance_update", payload, uid=_reset_uid)
    print(f"[Balance] 📡 SSE balance_update broadcast for {account_id!r} (balance=0)")
    return jsonify({"ok": True, "account_id": account_id, "balance": 0.0})


@app.route("/api/bank-balances/<path:account_id>", methods=["PUT"])
def api_update_bank_balance(account_id):
    """Update bank name and/or balance for an existing account (Firebase-only)."""
    account_id = unquote(account_id)
    data = request.json or {}
    new_name    = data.get("bank_name", "").strip()
    new_balance = data.get("balance")
    now = datetime.datetime.now().isoformat()
    _upd_uid = session.get("uid") or ADMIN_UID

    fb_data = {"updated_at": now}
    if new_name:
        fb_data["bank_name"] = new_name
    if new_balance is not None:
        try:
            fb_data["balance"] = float(new_balance)
        except (ValueError, TypeError):
            return jsonify({"ok": False, "error": "invalid balance"}), 400
    if len(fb_data) <= 1:
        return jsonify({"ok": False, "error": "nothing to update"}), 400

    if not firebase_db:
        return jsonify({"ok": False, "error": "Firebase not connected"}), 500
    try:
        from firebase import user_col
        ref  = user_col(_upd_uid, "bank_balances").document(account_id)
        snap = ref.get()
        if not snap.exists:
            return jsonify({"ok": False, "error": "not found"}), 404
        ref.update(fb_data)
    except Exception as e:
        print(f"[Balance] Firebase update error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

    _bb_cache_invalidate(_upd_uid)
    payload = {"account_id": account_id, **fb_data}
    broadcast_event("balance_updated", payload, uid=_upd_uid)
    return jsonify({"ok": True, "account": payload})


# ── Messages (raw SMS log) ──
@app.route("/api/messages")
def api_messages():
    limit = int(request.args.get("limit", 100))
    _uid  = session.get("uid") or ADMIN_UID
    return jsonify(get_raw_messages(limit, uid=_uid))

@app.route("/api/messages/<string:mid>", methods=["DELETE"])
def api_delete_message(mid):
    """Delete a raw message from Firebase."""
    if firebase_db:
        try:
            from firebase import user_col
            _msg_uid = session.get("uid") or ADMIN_UID
            # Try direct doc delete by id (Firebase auto-id)
            ref = user_col(_msg_uid, "messages").document(str(mid))
            snap = ref.get()
            if snap.exists:
                ref.delete()
            else:
                # Fall back: stream and match by legacy numeric id field
                for doc in user_col(_msg_uid, "messages").limit(200).stream():
                    if str(doc.to_dict().get("id", "")) == str(mid):
                        doc.reference.delete()
                        break
        except Exception as e:
            print(f"[Messages] delete error: {e}")
    return jsonify({"ok": True})


@app.route("/api/inbox")
def api_inbox():
    """Return recent expenses from telegram/ios_shortcut, newest first, up to 40."""
    limit = int(request.args.get("limit", 40))
    since = request.args.get("since", "")
    _uid  = session.get("uid") or ADMIN_UID
    if not firebase_db:
        return jsonify([])
    try:
        from firebase import user_col
        q = user_col(_uid, "expenses").where(filter=_FF("source", "in", ["telegram", "ios_shortcut"]))
        if since:
            q = q.where(filter=_FF("created_at", ">", since))
        docs = q.order_by("created_at", direction="DESCENDING").limit(limit).stream()
        result = []
        for doc in docs:
            d = doc.to_dict(); d["id"] = doc.id
            result.append(d)
        return jsonify(result)
    except Exception as e:
        print(f"[Inbox] Firebase error: {e}")
        return jsonify([])


@app.route("/api/messages/clear-all", methods=["DELETE", "POST"])
def api_clear_all_messages():
    """Permanently delete ALL raw messages from Firebase."""
    deleted_firebase = 0
    firebase_error = None
    if firebase_db:
        try:
            from firebase import user_col
            _clr_uid = session.get("uid") or ADMIN_UID
            batch = firebase_db.batch()
            count = 0
            for doc in user_col(_clr_uid, "messages").limit(500).stream():
                batch.delete(doc.reference)
                count += 1
                if count % 500 == 0:
                    batch.commit()
                    batch = firebase_db.batch()
            if count % 500 != 0 or count == 0:
                batch.commit()
            deleted_firebase = count
        except Exception as e:
            firebase_error = str(e)
            print(f"[Messages] Firebase clear error: {e}")

    print(f"[Messages] Cleared: Firebase={deleted_firebase}")
    resp = {"ok": True, "deleted_firebase": deleted_firebase}
    if firebase_error:
        resp["firebase_error"] = firebase_error
    return jsonify(resp)

# ── Dashboard ──


# ══════════════════════════════════════════════════════════════
# 14-DAY ANALYTICS & AI INSIGHTS - ULTRA SAFE VERSION
# ══════════════════════════════════════════════════════════════
@app.route("/api/analytics/14-day")
@app.route("/api/analytics/30-day")
def api_analytics_14day():
    """
    30-day spending analytics with AI insights.
    Route kept as /api/analytics/14-day for backward compatibility.
    Ultra-safe version with comprehensive error handling.
    """
    import datetime

    PERIOD_DAYS = 30

    # Default response structure
    default_response = {
        "chart_14_days": {
            "labels": [],
            "values": []
        },
        "analytics": {
            "total_spend_period": "0.000",
            "average_daily": "0.000",
            "days_with_spending": 0,
            "top_spending_category": "other",
            "spending_status": "Stable",
            "category_breakdown": {}
        },
        "ai_tips_arabic": []
    }

    try:
        # Generate 30-day date range using Muscat timezone (UTC+4)
        _muscat_now = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        today = _muscat_now.date()
        dates_30 = []
        for i in range(PERIOD_DAYS - 1, -1, -1):
            date_obj = today - datetime.timedelta(days=i)
            dates_30.append(date_obj.isoformat())

        # Fetch expenses from Firebase
        all_expenses = []
        start_date = dates_30[0]
        end_date   = dates_30[-1]

        if firebase_db:
            try:
                from firebase import user_col
                _an_uid = session.get("uid") or ADMIN_UID
                docs = (user_col(_an_uid, "expenses")
                        .where(filter=_FF("date_only", ">=", start_date))
                        .where(filter=_FF("date_only", "<=", end_date))
                        .limit(2000)
                        .stream())
                for doc in docs:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    all_expenses.append(d)
                print(f"[Analytics] Firebase: {len(all_expenses)} docs")
            except Exception as fb_err:
                print(f"[Analytics] Firebase error: {fb_err}")

        # If no expenses found, return empty data with helpful tips
        if not all_expenses:
            print("[Analytics] No expenses found for 30-day period")
            return jsonify({
                "chart_14_days": {
                    "labels": [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b %d")
                               for d in dates_30],
                    "values": [0.0] * PERIOD_DAYS
                },
                "analytics": {
                    "total_spend_period": "0.000",
                    "average_daily": "0.000",
                    "days_with_spending": 0,
                    "top_spending_category": "other",
                    "spending_status": "Stable",
                    "category_breakdown": {}
                },
                "ai_tips_arabic": [
                    "ابدأ بتسجيل مصروفاتك اليومية عبر التيليجرام 📱",
                    "أرسل رسائل البنك للبوت وسيحللها تلقائياً 🤖",
                    "تتبع إنفاقك لمدة شهر لترى نمطك المالي 💡"
                ]
            })

        # Calculate daily totals — use date_only if available, fall back to date[:10]
        from decimal import Decimal as _D30, InvalidOperation as _IO30
        daily_totals = {}
        for e in all_expenses:
            day = e.get("date_only") or str(e.get("date", ""))[:10]
            if day and day in set(dates_30):
                if e.get("type", "debit") in ("debit", "transfer_out"):
                    try:
                        raw_amt = e.get("amount")
                        if raw_amt is None:
                            continue
                        amt = _D30(str(raw_amt))
                        daily_totals[day] = float(
                            _D30(str(daily_totals.get(day, 0))) + amt
                        )
                    except (_IO30, Exception):
                        daily_totals[day] = daily_totals.get(day, 0.0) + float(e.get("amount") or 0)

        # Format chart data
        chart_labels = []
        for d in dates_30:
            try:
                chart_labels.append(datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%b %d"))
            except Exception:
                chart_labels.append(d[-5:])

        chart_values = [daily_totals.get(d, 0.0) for d in dates_30]

        # Calculate analytics
        debit_expenses = [e for e in all_expenses if e.get("type", "debit") in ("debit", "transfer_out")]

        from decimal import Decimal as _Dtot, InvalidOperation as _IOtot
        _total_dec = _Dtot("0")
        for e in debit_expenses:
            try:
                raw = e.get("amount")
                if raw is not None:
                    _total_dec += _Dtot(str(raw))
            except (_IOtot, Exception):
                try:
                    _total_dec += _Dtot(str(float(e.get("amount") or 0)))
                except Exception:
                    continue
        total_spend = float(_total_dec)

        days_with_spending = sum(1 for v in chart_values if v > 0)
        avg_daily = total_spend / PERIOD_DAYS if total_spend > 0 else 0.0
        
        # Category breakdown
        from decimal import Decimal as _Dcat
        category_totals = {}
        for e in debit_expenses:
            cat = e.get("category", "other")
            try:
                raw = e.get("amount")
                if raw is None:
                    continue
                amount = float(_Dcat(str(raw)))
                category_totals[cat] = round(
                    float(_Dcat(str(category_totals.get(cat, 0))) + _Dcat(str(raw))), 3
                )
            except Exception:
                try:
                    amount = float(e.get("amount", 0))
                    category_totals[cat] = category_totals.get(cat, 0.0) + amount
                except Exception:
                    continue
        
        top_category = "other"
        if category_totals:
            top_category = max(category_totals.items(), key=lambda x: x[1])[0]
        
        # Spending trend (first half vs second half of 30-day period)
        week1_total = sum(chart_values[:15])
        week2_total = sum(chart_values[15:])
        
        spending_status = "Stable"
        if week1_total > 0:
            change_pct = ((week2_total - week1_total) / week1_total) * 100
            if change_pct > 15:
                spending_status = "Increasing"
            elif change_pct < -15:
                spending_status = "Decreasing"
        
        # Generate tips
        ai_tips = _generate_safe_tips(
            total_spend, avg_daily, top_category, 
            category_totals, spending_status, 
            week1_total, week2_total
        )
        
        return jsonify({
            "chart_14_days": {
                "labels": chart_labels,
                "values": [round(v, 3) for v in chart_values]
            },
            "analytics": {
                "total_spend_period": f"{total_spend:.3f}",
                "average_daily": f"{avg_daily:.3f}",
                "days_with_spending": days_with_spending,
                "top_spending_category": top_category,
                "spending_status": spending_status,
                "category_breakdown": {
                    k: f"{v:.3f}" 
                    for k, v in sorted(category_totals.items(), 
                                     key=lambda x: x[1], reverse=True)
                }
            },
            "ai_tips_arabic": ai_tips
        })
        
    except Exception as e:
        # Log the error
        print(f"[Analytics] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        
        # Return safe fallback response
        return jsonify({
            "chart_14_days": {
                "labels": ["Day " + str(i) for i in range(1, 31)],
                "values": [0.0] * 30
            },
            "analytics": {
                "total_spend_period": "0.000",
                "average_daily": "0.000",
                "days_with_spending": 0,
                "top_spending_category": "other",
                "spending_status": "Stable",
                "category_breakdown": {}
            },
            "ai_tips_arabic": [
                "حدث خطأ في جلب البيانات — تحقق من اتصال Firebase 🔥",
                "تأكد من إضافة FIREBASE_KEY_JSON في المتغيرات البيئية ⚙️",
                "راجع السجلات (logs) لمعرفة تفاصيل الخطأ 📋"
            ]
        })


def _generate_safe_tips(total_spend, avg_daily, top_category, 
                        category_totals, spending_status, 
                        week1_total, week2_total):
    """Generate 3 financial tips - safe version with fallbacks."""
    
    CAT_AR = {
        "food": "الطعام", "shopping": "التسوق", 
        "transport": "المواصلات", "bills": "الفواتير",
        "health": "الصحة", "entertainment": "الترفيه",
        "education": "التعليم", "groceries": "البقالة",
        "fuel": "الوقود", "rent": "الإيجار",
        "subscriptions": "الاشتراكات", "transfer": "التحويل",
        "savings": "الادخار", "other": "أخرى"
    }
    
    tips = []
    top_cat_ar = CAT_AR.get(top_category, "الأخرى")
    top_cat_amount = category_totals.get(top_category, 0)
    
    # Tip 1: Spending trend
    if spending_status == "Increasing" and week1_total > 0:
        change = abs(((week2_total - week1_total) / week1_total) * 100)
        tips.append(f"لاحظت زيادة {change:.0f}% في الإنفاق — راقب {top_cat_ar} 🎯")
    elif spending_status == "Decreasing":
        tips.append(f"ممتاز! إنفاقك انخفض هذا الأسبوع — استمر بنفس النهج 🌟")
    else:
        if avg_daily > 0:
            tips.append(f"إنفاقك مستقر عند {avg_daily:.1f} ر.ع يومياً — تحكم جيد 💪")
        else:
            tips.append(f"ابدأ بتتبع مصروفاتك اليومية لرؤية أنماطك المالية 📊")
    
    # Tip 2: Category insights
    if total_spend > 0 and top_cat_amount > 0:
        cat_pct = (top_cat_amount / total_spend) * 100
        if cat_pct > 40:
            tips.append(f"{top_cat_ar} تشكل {cat_pct:.0f}% من إنفاقك — فرصة للتوفير 💡")
        elif cat_pct > 20:
            tips.append(f"{top_cat_ar} هي أكبر فئة بـ {cat_pct:.0f}% — راقبها بعناية 👀")
        else:
            tips.append(f"توزيع متوازن للمصروفات — {top_cat_ar} ضمن الحدود ✅")
    else:
        tips.append(f"نوّع فئات مصروفاتك لفهم أفضل لإنفاقك 🏷️")
    
    # Tip 3: Savings potential
    if total_spend > 50:
        saving = total_spend * 0.15
        tips.append(f"لو وفرت 15%، ستدخر {saving:.3f} ر.ع كل أسبوعين 💰")
    elif total_spend > 0:
        tips.append(f"إنفاقك {total_spend:.1f} ر.ع — حافظ على هذا المستوى المنخفض 👍")
    else:
        tips.append(f"سجّل معاملاتك من التيليجرام لبدء رحلة التوفير 🚀")
    
    # Ensure we always have 3 tips
    while len(tips) < 3:
        tips.append("استمر في تتبع مصروفاتك يومياً لتحقيق أهدافك المالية 🎯")
    
    return tips[:3]





# ══════════════════════════════════════════════════════════════
# DELETE ALL DATA ENDPOINT
# ══════════════════════════════════════════════════════════════
@app.route("/api/delete-all-data", methods=["POST"])
def api_delete_all_data():
    """
    حذف جميع البيانات (مصروفات، رسائل خام، أرصدة) من Firebase
    مع الاحتفاظ بـ: التعلم الذاتي، regex templates، merchant categories
    """
    try:
        deleted_counts = {
            "expenses_deleted": 0,
            "messages_deleted": 0,
            "balances_deleted": 0,
            "insights_deleted": 0,
        }

        _dd_uid = session.get("uid") or ADMIN_UID

        if firebase_db:
            try:
                from firebase import user_col

                def _batch_delete(col_ref):
                    batch = firebase_db.batch()
                    count = 0
                    for doc in col_ref.limit(500).stream():
                        batch.delete(doc.reference)
                        count += 1
                        if count % 500 == 0:
                            batch.commit()
                            batch = firebase_db.batch()
                    if count % 500 != 0 or count == 0:
                        batch.commit()
                    return count

                deleted_counts["expenses_deleted"]  = _batch_delete(user_col(_dd_uid, "expenses"))
                deleted_counts["messages_deleted"]   = _batch_delete(user_col(_dd_uid, "messages"))
                deleted_counts["balances_deleted"]   = _batch_delete(user_col(_dd_uid, "bank_balances"))
                deleted_counts["insights_deleted"]   = _batch_delete(
                    firebase_db.collection("daily_insights")
                )
                print(f"[Delete All] Firebase deleted: {deleted_counts}")
            except Exception as fb_err:
                print(f"[Delete All] Firebase error: {fb_err}")
                return jsonify({"error": str(fb_err)}), 500

        from db_helpers import exp_cache_invalidate, _bb_cache_invalidate
        exp_cache_invalidate(_dd_uid)
        _bb_cache_invalidate(_dd_uid)

        broadcast_event("data_deleted", {
            "message": "All data deleted",
            "counts": deleted_counts,
        }, uid=_dd_uid)

        return jsonify({
            "ok": True,
            "message": "تم حذف جميع البيانات بنجاح",
            **deleted_counts,
        })

    except Exception as e:
        print(f"[Delete All] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/dashboard")
def api_dashboard():
    try:
        today_str = _muscat_today()
        month_str = _muscat_month()
        _uid = session.get("uid") or ADMIN_UID

        # ── Run the 3 Firebase queries IN PARALLEL (cuts load time by ~60%) ──
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as _ex:
            _ft = _ex.submit(get_expenses_sqlite_fast, today_str, None, 500, _uid)
            _fm = _ex.submit(get_expenses_sqlite_fast, None, month_str, 500, _uid)
            _fb = _ex.submit(get_bank_balances_sqlite, _uid)
            today_exps   = _ft.result(timeout=12) or []
            month_exps   = _fm.result(timeout=12) or []
            bank_balances_pre = _fb.result(timeout=12) or []

        # ── Daily totals — compute directly from already-fetched rows (no extra query)
        from decimal import Decimal as _Dtd, InvalidOperation as _IOtd
        _td_acc = _Dtd("0")
        for e in today_exps:
            if e.get("type", "debit") in ("debit", "transfer_out"):
                try:
                    raw = e.get("amount")
                    if raw is not None:
                        _td_acc += _Dtd(str(raw))
                except (_IOtd, Exception):
                    pass
        today_debit  = float(_td_acc)
        today_credit = sum(float(e.get("amount") or 0) for e in today_exps
                           if e.get("type") == "credit")

        # ── Monthly totals ────────────────────────────────────────────────────
        from decimal import Decimal as _Dm, InvalidOperation as _IOm
        def _dec_sum(items, type_val):
            acc = _Dm("0")
            for e in items:
                t = e.get("type", "debit")
                # include transfer_out alongside debit in the spending total
                match = (t == type_val) or (type_val == "debit" and t == "transfer_out")
                if match:
                    try:
                        raw = e.get("amount")
                        if raw is not None:
                            acc += _Dm(str(raw))
                    except (_IOm, Exception):
                        pass
            return float(acc)

        month_debit  = _dec_sum(month_exps, "debit")
        month_credit = _dec_sum(month_exps, "credit")

        # ── Outgoing transfers ────────────────────────────────────────────────
        transfer_exps = [e for e in month_exps
                         if e.get("type") == "transfer_out"
                         or (e.get("type") == "debit" and e.get("category") == "transfer")]
        _mt_acc = _Dm("0")
        for e in transfer_exps:
            try:
                raw = e.get("amount")
                if raw is not None:
                    _mt_acc += _Dm(str(raw))
            except (_IOm, Exception):
                pass
        month_transfer = float(_mt_acc)
        transfer_count = len(transfer_exps)

        # ── Category breakdown ────────────────────────────────────────────────
        from decimal import Decimal as _Dcat2
        cats: dict = {}
        for e in month_exps:
            if e.get("type", "debit") in ("debit", "transfer_out"):
                c = e.get("category", "other") if e.get("type") != "transfer_out" else "transfer"
                try:
                    raw = e.get("amount")
                    if raw is not None:
                        cats[c] = float(
                            _Dcat2(str(cats.get(c, 0))) + _Dcat2(str(raw))
                        )
                except Exception:
                    cats[c] = cats.get(c, 0.0) + float(e.get("amount") or 0)

        # ── Daily spending chart ──────────────────────────────────────────────
        from decimal import Decimal as _Dday
        daily: dict = {}
        for e in month_exps:
            d = e.get("date_only") or str(e.get("date", ""))[:10]
            if d:
                try:
                    raw = e.get("amount")
                    if raw is not None:
                        daily[d] = float(
                            _Dday(str(daily.get(d, 0))) + _Dday(str(raw))
                        )
                except Exception:
                    daily[d] = daily.get(d, 0.0) + float(e.get("amount") or 0)

        # ── Daily insight — Firebase only ────────────────────────────────────
        insight = None
        if firebase_db:
            try:
                snap = firebase_db.collection("daily_insights").document(today_str).get()
                if snap.exists:
                    insight = snap.to_dict().get("insight")
            except Exception:
                pass

        # ── Parse method stats ────────────────────────────────────────────────
        method_counts = {"regex": 0, "ai": 0, "fallback": 0, "template": 0}
        for e in month_exps:
            m = e.get("parse_method", "ai") or "ai"
            if m in method_counts:
                method_counts[m] += 1

        # ── Bank balances already fetched in parallel above ───────────────────
        bank_balances = bank_balances_pre

        return jsonify({
            "today": {
                "total":        round(today_debit, 3),
                "total_credit": round(today_credit, 3),
                "count":        len(today_exps),
                "date":         today_str,
            },
            "month": {
                "total":          round(month_debit, 3),
                "total_credit":   round(month_credit, 3),
                "count":          len(month_exps),
                "total_transfer": round(month_transfer, 3),
                "transfer_count": transfer_count,
                # FIX #1: return ALL month items, not capped at 50
                "items":          month_exps,
            },
            "categories":       [{"category": k, "total": round(v, 3)}
                                  for k, v in sorted(cats.items(),
                                                     key=lambda x: x[1], reverse=True)],
            "daily":            [{"date": k, "total": round(v, 3)}
                                  for k, v in sorted(daily.items())],
            "bank_balances":    bank_balances,
            "daily_insight":    insight,
            "parse_method_stats": method_counts,
            "db_source":        "sqlite",
            "db_connected":     firebase_db is not None,
        })
    except Exception as e:
        import traceback
        print(f"[DASHBOARD] ❌ Unhandled error: {e}")
        print(traceback.format_exc())
        return jsonify({
            "error": str(e),
            "today":  {"total": 0, "count": 0},
            "month":  {"total": 0, "count": 0, "items": []},
            "categories": [], "daily": [], "bank_balances": [],
            "db_connected": False,
        }), 500

@app.route("/api/insight")
def api_insight():
    today = _muscat_today()
    exps  = get_expenses_sqlite_fast(date_filter=today, uid=session.get("uid") or ADMIN_UID)
    force = request.args.get("force", "0") == "1"
    if force:
        if firebase_db:
            try:
                firebase_db.collection("daily_insights").document(today).delete()
            except Exception as e:
                print(f"[Firebase] insight delete error: {e}")
    insight = generate_daily_insight(exps)
    broadcast_event("daily_insight", {"date": today, "insight": insight}, uid=session.get("uid") or ADMIN_UID)
    return jsonify({"date": today, "insight": insight})

@app.route("/api/parse", methods=["POST"])
def api_parse():
    """
    Smart Manual Analysis with Self-Learning:
    1. Hybrid parse (template → regex → AI → fallback).
    2. If the message was NOT matched by any existing pattern, generate a reusable regex.
    3. Broadcast daily_total + new_expense SSE events.
    4. Optionally save the expense when save=true is passed.
    """
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "empty text"}), 400

    lat  = data.get("latitude")
    lon  = data.get("longitude")
    try:
        lat = float(lat) if lat is not None else None
        lon = float(lon) if lon is not None else None
    except (TypeError, ValueError):
        lat = lon = None

    parsed, extracted_lat, extracted_lon, map_url = hybrid_parse(text)
    final_lat = lat if lat is not None else extracted_lat
    final_lon = lon if lon is not None else extracted_lon

    if not parsed or float(parsed.get("amount", 0) or 0) <= 0:
        # Use Decimal to double-check — float(0.200) > 0 is true, but guard against None
        from decimal import Decimal as _Dparse, InvalidOperation as _IOparse
        try:
            _amt_check = _Dparse(str(parsed.get("amount", 0) if parsed else 0))
        except (_IOparse, Exception):
            _amt_check = _Dparse("0")
        if not parsed or _amt_check <= 0:
            return jsonify({"error": "Not a transaction"}), 400

    parse_method = parsed.get("parse_method", "ai")
    new_template_saved = False
    if parse_method in ("ai", "fallback"):
        def _learn_in_background():
            try:
                gen = generate_regex_for_text(text)
                if gen and gen.get("pattern"):
                    bank = parsed.get("bank_name", "")
                    saved = save_regex_template(
                        pattern=gen["pattern"],
                        bank_name=bank,
                        description=gen.get("description", ""),
                    )
                    if saved:
                        broadcast_event("template_learned", {
                            "description": gen.get("description", ""),
                            "bank_name": bank,
                        }, uid=session.get("uid") or ADMIN_UID)
            except Exception as e:
                print(f"[RegexGen] background error: {e}")
        threading.Thread(target=_learn_in_background, daemon=True).start()
        new_template_saved = True

    parsed["extracted_latitude"]  = final_lat
    parsed["extracted_longitude"] = final_lon
    parsed["extracted_map_url"]   = map_url
    parsed["learning_triggered"]  = new_template_saved

    # ── Optional auto-save ──────────────────────────────────────────────
    if data.get("save"):
        doc = save_expense(parsed, "manual",
                           latitude=final_lat, longitude=final_lon,
                           map_url=map_url, raw_text=text,
                           uid=session.get("uid") or ADMIN_UID)
        parsed["saved_id"] = doc["id"]
        # FIX #3: refresh insight for manually parsed+saved transactions
        _trigger_insight_refresh(doc)

    return jsonify(parsed)

# ── Test endpoint for GPS extraction only ──
@app.route("/api/extract-gps", methods=["POST"])
def api_extract_gps():
    text = request.json.get("text", "")
    lat, lon, url = extract_gps_from_text(text)
    return jsonify({"latitude": lat, "longitude": lon, "map_url": url})


@app.route("/api/regex-templates")
def api_regex_templates():
    """Return all self-learned regex templates from in-memory cache."""
    try:
        from ai_engine import _regex_templates_cache, _mc_lock
        with _mc_lock:
            result = list(_regex_templates_cache)
        result.sort(key=lambda x: x.get("hit_count", 0), reverse=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/regex-templates/<string:tid>", methods=["DELETE"])
def api_delete_regex_template(tid):
    """Delete a stored regex template by doc id."""
    try:
        from ai_engine import _regex_templates_cache, _mc_lock
        with _mc_lock:
            before = len(_regex_templates_cache)
            _regex_templates_cache[:] = [
                t for t in _regex_templates_cache
                if str(t.get("id", "")) != str(tid)
            ]
        if firebase_db:
            try:
                firebase_db.collection("shared").document("regex_templates").collection("items").document(str(tid)).delete()
                firebase_db.collection("regex_templates").document(str(tid)).delete()
            except Exception as e:
                print(f"[RegexTemplate] delete Firebase error: {e}")
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})


# ==================== MERCHANT CATEGORY OVERRIDES ====================
# NOTE: Full implementation lives in merchant_routes.py (bp_merchant blueprint).
# These stubs are kept so any direct /api/merchant-categories calls still work
# if bp_merchant is registered with a url_prefix. If both blueprints register
# the same routes without prefix, the first one wins — remove whichever conflicts.
