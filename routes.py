# routes.py — Flask routes (webhook, dashboard, expenses, SSE, parse)
# UPDATED: bank-balance delete/reset, auto-insight after save, Muscat-tz daily total fix
import os, json, threading, time, datetime, re, queue
from urllib.parse import unquote
from flask import Blueprint, request, jsonify, send_from_directory, Response, stream_with_context, session, redirect
import requests

from config import BOT_TOKEN, ALLOWED_CHAT_IDS, ADMIN_CHAT_ID, SQLITE_PATH, db_conn, PASSWORD
from firebase import firebase_db, broadcast_event, _sse_clients, _preview_clients, _sse_lock
from ai_engine import hybrid_parse, extract_gps_from_text, PROVIDERS, generate_daily_insight
from db_helpers import _muscat_today, _muscat_month
from regex_templates import generate_regex_for_text, save_regex_template
# BUG FIX: import db_helpers module (not individual functions) so the
# monkey-patched save_expense from app.py is resolved at call-time,
# not frozen at import-time.
import db_helpers as _db_helpers
from db_helpers import (get_expenses_firebase, get_expenses_sqlite_fast,
                        get_bank_balances_sqlite,
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

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json or {}
    if data.get("password") == PASSWORD:
        session["authed"] = True
        session.permanent = True
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "كلمة المرور غير صحيحة"}), 401

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})

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
                    msg = q.get(timeout=20)
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
        from db_helpers import get_bank_balances_sqlite
        from config import db_conn as _db_conn
        banks_raw = get_bank_balances_sqlite()
        banks = [
            {
                "bank_name":  b.get("bank_name") or b.get("account_id") or "بنك",
                "account_id": b.get("account_id", ""),
                "balance":    float(b.get("balance") or 0),
                "currency":   b.get("currency", "OMR"),
            }
            for b in (banks_raw or [])
        ]

        # Last transaction from SQLite (fast, no Firebase call)
        last_tx = None
        try:
            conn = _db_conn()
            row = conn.execute(
                "SELECT * FROM expenses ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
            conn.close()
            if row:
                e = dict(row)
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
        "db_sqlite": True,
        "db_firebase": firebase_db is not None,
        "ai_providers": providers_status,
        "hybrid_parsing": True,
    })

# ── Emergency DB reset (password-protected) ──
@app.route("/api/admin/reset-db", methods=["POST"])
def admin_reset_db():
    import os as _os
    from config import SQLITE_PATH, init_db, PASSWORD as _PW
    if request.json.get("password") != _PW:
        return jsonify({"ok": False, "error": "unauthorized"}), 403
    deleted = []
    for suffix in ["", "-wal", "-shm"]:
        path = SQLITE_PATH + suffix
        try:
            _os.remove(path)
            deleted.append(path)
        except Exception:
            pass
    init_db()
    print(f"[Admin] ✅ DB reset — deleted: {deleted}", flush=True)
    # Trigger Firebase restore
    try:
        from app import restore_from_firebase
        restore_from_firebase()
    except Exception as _re:
        print(f"[Admin] restore error (non-fatal): {_re}", flush=True)
    return jsonify({"ok": True, "deleted": deleted})

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

    data = request.json
    if not data:
        print("[WEBHOOK] ⚠️  Empty body received")
        return jsonify({"ok": True})

    print(f"DEBUG: Webhook received — keys: {list(data.keys())}")

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

        print(f"[SHORTCUT] {len(sms_text)} chars  chat_id={chat_id}", flush=True)

        # Save raw message immediately
        save_raw_message(chat_id or "shortcut", sms_text, source="ios_shortcut")

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

        def _bg_full(sms_text, ios_lat_f, ios_lon_f, chat_id, bot_token, primary_id):
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
                                       map_url=map_url, raw_text=sms_text, chat_id=chat_id)
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
            args=(sms_text, ios_lat_f, ios_lon_f, chat_id, BOT_TOKEN, PRIMARY_NOTIFY_ID),
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
def _trigger_insight_refresh(doc: dict):
    """
    After a new expense is saved, asynchronously regenerate today's daily
    insight so the Smart Daily Analytics section stays current.
    Broadcasts an SSE 'daily_insight' event when done.
    """
    def _run():
        try:
            today = _muscat_today()
            # Only refresh for today's transactions
            tx_date = str(doc.get("date", ""))[:10]
            if tx_date and tx_date != today:
                return
            exps = get_expenses_firebase(date_filter=today)
            if not exps:
                return
            # Force-delete cached insight so generate_daily_insight creates fresh one
            if firebase_db:
                try:
                    firebase_db.collection("daily_insights").document(today).delete()
                except Exception:
                    pass
            try:
                conn = db_conn()
                conn.execute("DELETE FROM daily_insights WHERE date=?", (today,))
                conn.commit()
                conn.close()
            except Exception:
                pass
            insight = generate_daily_insight(exps)
            broadcast_event("daily_insight", {"date": today, "insight": insight})
            print(f"[Insight] ✅ Auto-refreshed for {today} after new expense")
        except Exception as e:
            print(f"[Insight] ⚠️  Auto-refresh error: {e}")
    threading.Thread(target=_run, daemon=True).start()


@app.route("/api/stream")
def sse_stream():
    if not session.get("authed"):
        return Response("data: {\"error\":\"unauthorized\"}\n\n", mimetype='text/event-stream', status=401)
    q = queue.Queue(maxsize=50)
    with _sse_lock:
        if len(_sse_clients) >= 20:
            try:
                _sse_clients[0].put_nowait("event: close\ndata: {}\n\n")
            except Exception:
                pass
            _sse_clients.pop(0)
        _sse_clients.append(q)
    def generate():
        try:
            yield "data: {\"type\":\"connected\"}\n\n"
            deadline = time.time() + 270  # 4.5 min max per SSE connection
            while time.time() < deadline:
                try:
                    msg = q.get(timeout=20)
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
                if q in _sse_clients:
                    _sse_clients.remove(q)
    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# ── Expenses API ──
@app.route("/api/expenses")
def api_expenses():
    month = request.args.get("month", _muscat_month())
    date  = request.args.get("date", "")
    limit = int(request.args.get("limit", 500))
    if date:
        return jsonify(get_expenses_sqlite_fast(date_filter=date, limit=limit))
    return jsonify(get_expenses_sqlite_fast(month_filter=month, limit=limit))

@app.route("/api/expenses/map")
def api_expenses_map():
    month = request.args.get("month", _muscat_month())
    conn = db_conn()
    rows = conn.execute("""
        SELECT id, name, amount, currency, category, date, bank_name,
               source, parse_method, available_balance, map_url,
               latitude, longitude
        FROM expenses
        WHERE date LIKE ?
          AND latitude IS NOT NULL
          AND longitude IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 500
    """, (month + "%",)).fetchall()
    conn.close()
    pins = []
    for r in rows:
        d = dict(r)
        try:
            d["latitude"]  = float(d["latitude"])
            d["longitude"] = float(d["longitude"])
            pins.append(d)
        except (TypeError, ValueError):
            pass
    return jsonify(pins)

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
                       latitude=lat, longitude=lon, map_url=map_url)
    # FIX #3: also refresh insight for manually added expenses
    _trigger_insight_refresh(doc)
    # FIX #4: tell frontend a fresh fetch is needed
    resp = jsonify(doc)
    resp.headers["X-Data-Updated"] = "true"
    return resp

@app.route("/api/expense/<eid>", methods=["DELETE"])
def api_delete(eid):
    # Grab the expense date_only before deleting so we can recompute the daily total
    expense_date = None
    conn = db_conn()
    row = conn.execute("SELECT date FROM expenses WHERE id=?", (eid,)).fetchone()
    if row:
        expense_date = str(row["date"] or "")[:10]
    conn.execute("DELETE FROM expenses WHERE id=?", (eid,))
    conn.commit()
    conn.close()

    if firebase_db:
        try:
            firebase_db.collection("expenses").document(eid).delete()
        except Exception:
            pass
        try:
            firebase_db.collection("transactions").document(eid).delete()
        except Exception:
            pass

    # Broadcast deletion to all SSE clients
    broadcast_event("expense_deleted", {"id": eid})

    # Recompute and broadcast the daily total so every connected client updates immediately
    today_str = _muscat_today()
    if not expense_date:
        expense_date = today_str
    new_daily = get_daily_total_firebase(expense_date)
    broadcast_event("daily_total", {"date": expense_date, "total": new_daily})

    # Tell every client to fully re-fetch dashboard + analytics
    broadcast_event("refresh_dashboard", {"reason": "expense_deleted", "id": eid})

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
    if "name" in update:
        conn = db_conn()
        old_row = conn.execute("SELECT name FROM expenses WHERE id=?", (eid,)).fetchone()
        conn.close()
        if old_row and old_row["name"] and old_row["name"] != update["name"]:
            old_name = old_row["name"].strip()
            name_changed = True

    # ── 2. SQLite: update this expense + bulk-rename same merchant ─────────
    import datetime as _dt
    _now = _dt.datetime.utcnow().isoformat()

    set_clause = ", ".join(f"{k}=?" for k in update)
    values     = list(update.values()) + [eid]
    conn = db_conn()
    conn.execute(f"UPDATE expenses SET {set_clause} WHERE id=?", values)
    if name_changed:
        preferred    = update["name"].strip()
        original_key = old_name.lower()
        conn.execute(
            "INSERT OR REPLACE INTO merchant_categories (merchant_key, category, updated_at) VALUES (?,?,?)",
            ("~name~" + original_key, preferred, _now)
        )
        conn.execute(
            "UPDATE expenses SET name=? WHERE LOWER(name)=? AND id!=?",
            (preferred, original_key, eid)
        )
    conn.commit()
    conn.close()

    # ── 3. Broadcast SSE immediately (before Firebase) ────────────────────
    broadcast_event("expense_edited", {"id": eid, "updates": update})
    if name_changed:
        broadcast_event("names_bulk_updated", {"old": old_name, "new": preferred})

    # ── 4. Firebase writes in background — never block the response ────────
    def _firebase_sync(eid, update, name_changed, old_name):
        if not firebase_db:
            return
        # Update this expense
        try:
            firebase_db.collection("expenses").document(eid).update(update)
        except Exception as e:
            print(f"[Firebase] edit sync (expenses): {e}")
        try:
            txn_update = {k: update[k] for k in update
                          if k in ("amount","currency","category","date","type","bank_name","name")}
            if txn_update:
                firebase_db.collection("transactions").document(eid).update(txn_update)
        except Exception as e:
            print(f"[Firebase] edit sync (transactions): {e}")

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
        # Bulk rename matching docs
        for coll in ("expenses", "transactions"):
            try:
                for d in firebase_db.collection(coll).where("name", "==", old_name).stream():
                    try:
                        d.reference.update({"name": preferred})
                    except Exception:
                        pass
            except Exception as e:
                print(f"[Firebase] bulk name update ({coll}): {e}")

    threading.Thread(target=_firebase_sync, args=(eid, update, name_changed, old_name), daemon=True).start()

    return jsonify({"ok": True, "id": eid})

# ── Bank Balances ──
@app.route("/api/bank-balances")
def api_bank_balances():
    return jsonify(get_bank_balances_sqlite())


# ─────────────────────────────────────────────────────────────────────────────
# FIX #2 — Bank balance delete / reset endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/bank-balances/<path:account_id>", methods=["DELETE"])
def api_delete_bank_balance(account_id):
    """
    Permanently remove a bank account balance record from both SQLite and
    Firestore, then broadcast a real-time SSE event so the dashboard
    Net Worth total updates immediately without a page reload.

    BUG FIX 1 — URL encoding mismatch:
      The browser's fetch() + encodeURIComponent() turns "Bank Muscat_1234"
      into "Bank%20Muscat_1234".  Flask's <path:> converter does NOT decode
      percent-encoding, so the raw DB lookup silently missed every time.
      unquote() decodes the ID before any DB/Firestore call.

    BUG FIX 2 — Firestore errors swallowed / wrong "ok: true":
      Old code always returned {"ok": true} even when Firestore failed.
      Now: check snap.exists before deleting, capture firebase_error in
      the response body, and return HTTP 404 when SQLite found 0 rows.

    BUG FIX 3 — SSE broadcast fired unconditionally:
      Phantom balance_deleted events could confuse the frontend into
      removing a card that was never actually deleted.
      Now: only broadcast when at least SQLite or Firestore confirmed success.
    """
    # BUG FIX 1: always decode percent-encoding before any DB lookup
    account_id = unquote(account_id)
    print(f"[Balance] DELETE requested for account_id={account_id!r}")

    # ── SQLite ────────────────────────────────────────────────────────
    conn = db_conn()
    result = conn.execute(
        "DELETE FROM bank_balances WHERE account_id=?", (account_id,)
    )
    sqlite_deleted = result.rowcount   # BUG FIX 3: track actual rows removed
    conn.commit()
    conn.close()
    print(f"[Balance] SQLite rows deleted: {sqlite_deleted}")

    # Broadcast immediately after SQLite delete — don't wait for Firebase
    if sqlite_deleted > 0:
        broadcast_event("balance_deleted", {"account_id": account_id})
        print(f"[Balance] SSE balance_deleted broadcast for {account_id!r}")

    # Firebase delete in background — never block the response
    def _fb_delete_balance(account_id):
        if not firebase_db:
            return
        try:
            ref  = firebase_db.collection("bank_balances").document(account_id)
            snap = ref.get()
            if snap.exists:
                ref.delete()
                print(f"[Balance] Firestore deleted: {account_id!r}")
            else:
                print(f"[Balance] Firestore doc not found: {account_id!r}")
        except Exception as e:
            print(f"[Balance] Firestore delete error: {e}")

    threading.Thread(target=_fb_delete_balance, args=(account_id,), daemon=True).start()

    status_code = 200 if sqlite_deleted > 0 else 404
    return jsonify({"ok": sqlite_deleted > 0, "account_id": account_id}), status_code


@app.route("/api/bank-balances/<path:account_id>/reset", methods=["POST"])
def api_reset_bank_balance(account_id):
    """
    Set a bank account balance to zero (keeps the record, just zeroes it).

    BUG FIX 1 — URL encoding mismatch (same as DELETE endpoint):
      unquote() decodes percent-encoded account_id before any DB call.

    BUG FIX 4 — conn.close() ordering:
      Old code fetched the row for the broadcast payload AFTER conn.close()
      was ambiguous in position.  Now the SELECT is explicit BEFORE close().
    """
    # BUG FIX 1: decode percent-encoding
    account_id = unquote(account_id)
    print(f"[Balance] RESET requested for account_id={account_id!r}")

    now = datetime.datetime.now().isoformat()

    # ── SQLite — update then fetch BEFORE closing ──────────────────────
    conn = db_conn()
    conn.execute(
        "UPDATE bank_balances SET balance=0, updated_at=? WHERE account_id=?",
        (now, account_id),
    )
    conn.commit()
    # BUG FIX 4: fetch BEFORE conn.close() so the row is still readable
    row = conn.execute(
        "SELECT * FROM bank_balances WHERE account_id=?", (account_id,)
    ).fetchone()
    conn.close()   # close AFTER the SELECT

    if not row:
        print(f"[Balance] ⚠️  account_id={account_id!r} not found in SQLite after reset")
        return jsonify({"ok": False, "error": "account not found"}), 404

    # ── Firestore ─────────────────────────────────────────────────────
    firebase_error = None
    if firebase_db:
        try:
            firebase_db.collection("bank_balances").document(account_id).update({
                "balance":    0.0,
                "updated_at": now,
            })
            print(f"[Balance] ✅ Firestore balance reset for {account_id!r}")
        except Exception as e:
            firebase_error = str(e)
            print(f"[Balance] ❌ Firestore reset error for {account_id!r}: {firebase_error}")

    # Build broadcast payload from the freshly-fetched row
    payload               = dict(row)
    payload["balance"]    = 0.0
    payload["account_id"] = account_id   # guarantee present
    broadcast_event("balance_update", payload)
    print(f"[Balance] 📡 SSE balance_update broadcast for {account_id!r} (balance=0)")

    response = {"ok": True, "account_id": account_id, "balance": 0.0}
    if firebase_error:
        response["firebase_warning"] = firebase_error
    return jsonify(response)


# ── Messages (raw SMS log) ──
@app.route("/api/messages")
def api_messages():
    limit = int(request.args.get("limit", 100))
    return jsonify(get_raw_messages(limit))

@app.route("/api/messages/<int:mid>", methods=["DELETE"])
def api_delete_message(mid):
    conn = db_conn()
    conn.execute("DELETE FROM messages WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    # Also delete from Firebase
    if firebase_db:
        try:
            docs = firebase_db.collection("messages").where("id", "==", mid).stream()
            for doc in docs:
                doc.reference.delete()
        except Exception:
            pass
    return jsonify({"ok": True})


@app.route("/api/inbox")
def api_inbox():
    """Return recent expenses from telegram/ios_shortcut, newest first, up to 40."""
    limit = int(request.args.get("limit", 40))
    since = request.args.get("since", "")  # ISO datetime — only return rows after this
    conn = db_conn()
    query = """
        SELECT id, type, name, amount, currency, category, date, bank_name,
               source, parse_method, created_at, latitude, longitude
        FROM expenses
        WHERE source IN ('telegram','ios_shortcut')
    """
    params: list = []
    if since:
        query += " AND created_at > ?"
        params.append(since)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    result = [dict(r) for r in rows]
    return jsonify(result)


@app.route("/api/messages/clear-all", methods=["DELETE", "POST"])
def api_clear_all_messages():
    """Permanently delete ALL raw messages from SQLite and Firebase."""
    # SQLite
    conn = db_conn()
    result = conn.execute("DELETE FROM messages")
    deleted_sqlite = result.rowcount
    conn.commit()
    conn.close()

    # Firebase — batch delete all docs in messages collection
    deleted_firebase = 0
    firebase_error = None
    if firebase_db:
        try:
            batch = firebase_db.batch()
            count = 0
            for doc in firebase_db.collection("messages").stream():
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

    print(f"[Messages] Cleared: SQLite={deleted_sqlite}, Firebase={deleted_firebase}")
    resp = {"ok": True, "deleted_sqlite": deleted_sqlite, "deleted_firebase": deleted_firebase}
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

        # Fetch expenses: SQLite first (fast), Firebase fallback only if SQLite empty
        all_expenses = []
        start_date = dates_30[0]
        end_date   = dates_30[-1]

        # ── 1. Try SQLite ──────────────────────────────────────────────────
        try:
            _ac = db_conn()
            _total = _ac.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
            if _total > 0:
                _arows = _ac.execute(
                    "SELECT * FROM expenses "
                    "WHERE created_at >= ? AND created_at <= ? "
                    "ORDER BY created_at DESC LIMIT 2000",
                    (start_date, end_date + "T99")
                ).fetchall()
                all_expenses = [dict(r) for r in _arows]
                print(f"[Analytics] SQLite: {len(all_expenses)} docs")
            _ac.close()
        except Exception as _sqle:
            print(f"[Analytics] SQLite error: {_sqle}")

        # ── 2. Firebase fallback — only when SQLite is completely empty ────
        if not all_expenses and firebase_db:
            try:
                docs = (firebase_db.collection("expenses")
                        .where("date_only", ">=", start_date)
                        .where("date_only", "<=", end_date)
                        .order_by("date_only", direction="DESCENDING")
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
                if e.get("type", "debit") == "debit":
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
        debit_expenses = [e for e in all_expenses if e.get("type", "debit") == "debit"]

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
    حذف جميع البيانات (مصروفات، رسائل خام، أرصدة)
    مع الاحتفاظ بـ: التعلم الذاتي، regex templates، merchant categories
    """
    try:
        from config import db_conn
        from firebase import firebase_db, broadcast_event
        
        deleted_counts = {
            "expenses_deleted": 0,
            "messages_deleted": 0,
            "balances_deleted": 0,
            "insights_deleted": 0
        }
        
        # حذف من SQLite
        conn = db_conn()
        
        # حذف المصروفات
        result = conn.execute("DELETE FROM expenses")
        deleted_counts["expenses_deleted"] = result.rowcount
        
        # حذف الرسائل الخام
        result = conn.execute("DELETE FROM messages")
        deleted_counts["messages_deleted"] = result.rowcount
        
        # حذف الأرصدة
        result = conn.execute("DELETE FROM bank_balances")
        deleted_counts["balances_deleted"] = result.rowcount
        
        # حذف الـ insights
        result = conn.execute("DELETE FROM daily_insights")
        deleted_counts["insights_deleted"] = result.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"[Delete All] SQLite deleted: {deleted_counts}")
        
        # حذف من Firebase
        if firebase_db:
            try:
                def _batch_delete_collection(coll_name):
                    batch = firebase_db.batch()
                    docs = firebase_db.collection(coll_name).stream()
                    count = 0
                    for doc in docs:
                        batch.delete(doc.reference)
                        count += 1
                        if count % 500 == 0:
                            batch.commit()
                            batch = firebase_db.batch()
                    if count % 500 != 0 or count == 0:
                        batch.commit()
                    print(f"[Delete All] Firebase {coll_name} deleted: {count}")
                    return count

                _batch_delete_collection("expenses")
                _batch_delete_collection("transactions")
                _batch_delete_collection("bank_balances")
                _batch_delete_collection("messages")
                _batch_delete_collection("daily_insights")

            except Exception as fb_err:
                print(f"[Delete All] Firebase error: {fb_err}")
        
        # بث SSE لتحديث الواجهة
        broadcast_event("data_deleted", {
            "message": "All data deleted",
            "counts": deleted_counts
        })
        
        return jsonify({
            "ok": True,
            "message": "تم حذف جميع البيانات بنجاح",
            **deleted_counts
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

        # Use SQLite-fast reader — no Firebase network call
        today_exps = get_expenses_sqlite_fast(date_filter=today_str)
        month_exps = get_expenses_sqlite_fast(month_filter=month_str)

        # ── Daily totals — compute directly from already-fetched rows (no extra query)
        from decimal import Decimal as _Dtd, InvalidOperation as _IOtd
        _td_acc = _Dtd("0")
        for e in today_exps:
            if e.get("type", "debit") == "debit":
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
                if e.get("type", "debit") == type_val:
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
            if e.get("type", "debit") == "debit":
                c = e.get("category", "other")
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

        # ── Daily insight — SQLite only (no AI call here, no Firebase) ──────
        insight = None
        try:
            _ic = db_conn()
            _irow = _ic.execute(
                "SELECT insight FROM daily_insights WHERE date=?", (today_str,)
            ).fetchone()
            _ic.close()
            if _irow:
                insight = _irow["insight"]
        except Exception:
            pass

        # ── Parse method stats ────────────────────────────────────────────────
        method_counts = {"regex": 0, "ai": 0, "fallback": 0, "template": 0}
        for e in month_exps:
            m = e.get("parse_method", "ai") or "ai"
            if m in method_counts:
                method_counts[m] += 1

        # ── Bank balances (for Net Worth) ─────────────────────────────────────
        bank_balances = get_bank_balances_sqlite()

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
    exps  = get_expenses_sqlite_fast(date_filter=today)
    force = request.args.get("force", "0") == "1"
    if force:
        if firebase_db:
            try:
                firebase_db.collection("daily_insights").document(today).delete()
            except Exception as e:
                print(f"[Firebase] insight delete error: {e}")
        conn = db_conn()
        conn.execute("DELETE FROM daily_insights WHERE date=?", (today,))
        conn.commit()
        conn.close()
    insight = generate_daily_insight(exps)
    broadcast_event("daily_insight", {"date": today, "insight": insight})
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
                        })
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
                           map_url=map_url, raw_text=text)
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
    """Return all self-learned regex templates."""
    try:
        conn = db_conn()
        rows = conn.execute(
            "SELECT id, bank_name, description, hit_count, created_at, last_used_at FROM regex_templates ORDER BY hit_count DESC"
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/regex-templates/<int:tid>", methods=["DELETE"])
def api_delete_regex_template(tid):
    """Delete a stored regex template by id."""
    conn = db_conn()
    conn.execute("DELETE FROM regex_templates WHERE id=?", (tid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ==================== MERCHANT CATEGORY OVERRIDES ====================

@app.route("/api/merchant-categories", methods=["GET"])
def api_get_merchant_categories():
    """List all user-defined merchant→category overrides."""
    try:
        conn = db_conn()
        rows = conn.execute(
            "SELECT merchant_key, category, updated_at FROM merchant_categories ORDER BY merchant_key"
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/merchant-categories", methods=["POST"])
def api_set_merchant_category():
    data = request.json or {}
    merchant_name = (data.get("merchant") or "").strip()
    category      = (data.get("category") or "").strip().lower()
    valid_cats = {"food","shopping","transport","bills","health","entertainment",
                  "education","groceries","fuel","rent","subscriptions","transfer","savings","other"}
    if not merchant_name:
        return jsonify({"error": "merchant required"}), 400
    if category not in valid_cats:
        return jsonify({"error": f"invalid category — must be one of: {', '.join(sorted(valid_cats))}"}), 400

    merchant_key = merchant_name.lower()
    now = datetime.datetime.now().isoformat()

    conn = db_conn()
    conn.execute(
        "INSERT OR REPLACE INTO merchant_categories (merchant_key, category, updated_at) VALUES (?,?,?)",
        (merchant_key, category, now)
    )
    result = conn.execute(
        "UPDATE expenses SET category=? WHERE LOWER(name)=? AND type='debit'",
        (category, merchant_key)
    )
    updated_count = result.rowcount
    conn.commit()
    conn.close()

    if firebase_db:
        try:
            firebase_db.collection("merchant_categories").document(merchant_key).set({
                "merchant_key": merchant_key, "category": category, "updated_at": now
            })
            docs = (firebase_db.collection("expenses")
                    .where("type", "==", "debit")
                    .stream())
            batch = firebase_db.batch()
            count_fb = 0
            for doc in docs:
                d = doc.to_dict()
                if (d.get("name") or "").lower() == merchant_key:
                    batch.update(doc.reference, {"category": category})
                    count_fb += 1
                if count_fb > 0 and count_fb % 500 == 0:
                    batch.commit()
                    batch = firebase_db.batch()
            if count_fb % 500 != 0 or count_fb == 0:
                batch.commit()
        except Exception as e:
            print(f"[Firebase] merchant_categories sync error: {e}")

    broadcast_event("category_override", {
        "merchant": merchant_name,
        "merchant_key": merchant_key,
        "category": category,
        "updated_count": updated_count,
    })

    return jsonify({
        "ok": True,
        "merchant_key": merchant_key,
        "category": category,
        "expenses_updated": updated_count,
    })

@app.route("/api/merchant-categories/<path:merchant_key>", methods=["DELETE"])
def api_delete_merchant_category(merchant_key):
    """Remove a merchant category override (reverts to auto-detection)."""
    conn = db_conn()
    conn.execute("DELETE FROM merchant_categories WHERE merchant_key=?", (merchant_key.lower(),))
    conn.commit()
    conn.close()
    if firebase_db:
        try:
            firebase_db.collection("merchant_categories").document(merchant_key.lower()).delete()
        except Exception:
            pass
    return jsonify({"ok": True})
