# db_helpers.py — save_expense(), get_expenses_*(), get_bank_balances_*(), daily totals
# UPDATED: Muscat-tz daily-total SSE fix, chat_id + timestamp persistence, insight_needed broadcast
import uuid as _uuid
import datetime, json

from config import BOT_TOKEN, ADMIN_CHAT_ID, SQLITE_PATH, db_conn
from firebase import firebase_db, broadcast_event
from ai_engine import (_detect_bank, _extract_sender_field, _resolve_bank_from_sender,
                       _categorize, _get_merchant_category_override,
                       _get_merchant_preferred_name,
                       generate_daily_insight, _ai_call, DAILY_INSIGHT_PROMPT)
import requests


def save_expense(parsed, source="manual", latitude=None, longitude=None,
                 map_url=None, raw_text="", chat_id=None):
    tx_type = parsed.get("type", "debit")
    eid = str(_uuid.uuid4())
    now = datetime.datetime.now().isoformat()

    # ── Sender-aware bank resolution ──────────────────────────────────────
    raw_sender_field = parsed.get("sender_raw") or _extract_sender_field(raw_text)
    resolved_bank = _resolve_bank_from_sender(raw_sender_field) if raw_sender_field else ""
    bank_name = resolved_bank or parsed.get("bank_name", "") or _detect_bank(raw_text)

    # amount: Decimal cast to avoid silent rounding of small values (e.g. 0.400)
    from decimal import Decimal
    _raw_amount = parsed.get("amount", 0)
    try:
        _safe_amount = float(Decimal(str(_raw_amount)))
    except Exception:
        _safe_amount = float(_raw_amount)

    # ── Compute date_only in Asia/Muscat timezone (UTC+4) ─────────────────
    # FIX #4: timestamp is now stored in every record so the UI can always
    # sort / filter correctly regardless of which tz the server runs in.
    try:
        _utc_now = datetime.datetime.utcnow()
        _muscat_offset = datetime.timedelta(hours=4)
        _muscat_now = _utc_now + _muscat_offset
        date_only_muscat = _muscat_now.strftime("%Y-%m-%d")
    except Exception:
        date_only_muscat = parsed.get("date", datetime.date.today().isoformat())

    _raw_name = (
        parsed.get("recipient") or parsed.get("merchant", parsed.get("name", "غير معروف"))
        if tx_type == "transfer_out"
        else parsed.get("merchant", parsed.get("name", "غير معروف"))
    )
    # Apply user's preferred display name if set (survives deployments via SQLite restore)
    _display_name = _get_merchant_preferred_name(_raw_name) or _raw_name

    doc = {
        "id":        eid,
        "type":      tx_type,
        "name":      _display_name,
        "sender":    raw_sender_field or parsed.get("sender", ""),
        "recipient": parsed.get("recipient", ""),
        "txn_id":    parsed.get("txn_id", ""),
        "amount":    _safe_amount,
        # FIX #4: always store both a full ISO timestamp and a Muscat-tz date
        "timestamp":   now,           # ISO 8601 full datetime for audit trail
        "date_only":   date_only_muscat,   # YYYY-MM-DD Muscat tz — used by all filters
        "currency":  parsed.get("currency", "OMR"),
        "category": (
            "transfer"
            if tx_type in ("transfer_out", "credit")
            else (
                _get_merchant_category_override(
                    parsed.get("merchant") or parsed.get("name") or ""
                ) or parsed.get("category") or _categorize(
                    parsed.get("merchant") or parsed.get("name") or ""
                )
            )
        ),
        "date":      parsed.get("date", date_only_muscat),
        "notes":     (
            f"بطاقة ****{parsed['card_last4']}"
            if parsed.get("card_last4")
            else parsed.get("notes", "")
        ),
        "source":            source,
        "bank_name":         bank_name,
        "available_balance": parsed.get("available_balance"),
        "card_last4":        parsed.get("card_last4"),
        "latitude":          latitude,
        "longitude":         longitude,
        "map_url":           map_url,
        "parse_method":      parsed.get("parse_method", "ai"),
        # FIX #4: persist chat_id so the UI can filter by user / verify ownership
        "chat_id":           str(chat_id) if chat_id is not None else "",
        "created_at": (
            parsed.get("date", date_only_muscat) + "T" + parsed["msg_time"]
            if parsed.get("msg_time") and parsed.get("date")
            else now
        ),
    }

    # ── SQLite insert ──────────────────────────────────────────────────────
    conn = db_conn()
    conn.execute("""INSERT INTO expenses
        (id,type,name,sender,recipient,txn_id,amount,currency,category,date,notes,source,bank_name,
         available_balance,card_last4,latitude,longitude,map_url,parse_method,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (doc["id"],doc["type"],doc["name"],doc["sender"],doc.get("recipient",""),doc.get("txn_id",""),
         doc["amount"],doc["currency"],doc["category"],doc["date"],doc["notes"],doc["source"],doc["bank_name"],
         doc["available_balance"],doc["card_last4"],doc["latitude"],doc["longitude"],
         doc["map_url"],doc["parse_method"],doc["created_at"]))

    # Save/update balance if we have at least card_last4 OR bank_name
    balance_updated = False
    if doc["available_balance"] is not None and (doc["bank_name"] or doc["card_last4"]):
        card_key   = doc["card_last4"] or "default"
        bank_key   = doc["bank_name"]  or "Unknown Bank"
        account_id = f"{bank_key}_{card_key}"
        conn.execute("""INSERT OR REPLACE INTO bank_balances
            (account_id,bank_name,card_last4,balance,currency,updated_at)
            VALUES (?,?,?,?,?,?)""",
            (account_id, bank_key, doc["card_last4"], doc["available_balance"], doc["currency"], now))
        balance_updated = True
    conn.commit()
    conn.close()

    # ── Firebase mirror (non-blocking) ────────────────────────────────────
    # Run all Firebase writes in a daemon thread so save_expense returns
    # immediately after SQLite — prevents the caller from hanging on network.
    if firebase_db:
        def _to_float(v):
            if v is None:
                return None
            try:
                from decimal import Decimal
                return float(Decimal(str(v)))
            except Exception:
                try:
                    return float(v)
                except Exception:
                    return None

        def _fb_mirror():
            try:
                fb_doc = {k: v for k, v in doc.items() if k != "id"}
                fb_doc["createdAt"]         = now
                fb_doc["date_only"]         = date_only_muscat
                fb_doc["amount"]            = _to_float(doc["amount"]) or 0.0
                fb_doc["available_balance"] = _to_float(doc.get("available_balance"))
                fb_doc["latitude"]          = _to_float(doc.get("latitude"))
                fb_doc["longitude"]         = _to_float(doc.get("longitude"))
                firebase_db.collection("expenses").document(eid).set(fb_doc)

                _lat = _to_float(doc.get("latitude"))
                _lng = _to_float(doc.get("longitude"))
                txn_doc = {
                    "amount":            _to_float(doc["amount"]) or 0.0,
                    "available_balance": _to_float(doc.get("available_balance")),
                    "lat":               _lat,
                    "lng":               _lng,
                    "vendor":            doc.get("name", "غير معروف"),
                    "bank":              doc.get("bank_name", ""),
                    "timestamp":         now,
                    "date":              doc.get("date", date_only_muscat),
                    "date_only":         date_only_muscat,
                    "type":              doc.get("type", "debit"),
                    "category":          doc.get("category", "other"),
                    "currency":          doc.get("currency", "OMR"),
                    "card_last4":        doc.get("card_last4"),
                    "source":            doc.get("source", "manual"),
                    "parse_method":      doc.get("parse_method", "ai"),
                    "chat_id":           doc.get("chat_id", ""),
                }
                firebase_db.collection("transactions").document(eid).set(txn_doc)

                if balance_updated:
                    card_key   = doc["card_last4"] or "default"
                    bank_key   = doc["bank_name"]  or "Unknown Bank"
                    account_id = f"{bank_key}_{card_key}"
                    firebase_db.collection("bank_balances").document(account_id).set({
                        "bank_name":  bank_key,
                        "card_last4": doc["card_last4"],
                        "account_id": account_id,
                        "balance":    _to_float(doc["available_balance"]) or 0.0,
                        "currency":   doc["currency"],
                        "updated_at": now,
                    })

                print(f"[Firebase] ✅ Saved expense {eid} (date_only={date_only_muscat})")
            except Exception as e:
                print(f"[Firebase] ❌ mirror error for expense {eid}: {e}")

        import threading as _threading
        _threading.Thread(target=_fb_mirror, daemon=True).start()

    doc["_firebase_ok"]    = True
    doc["_firebase_error"] = None
    method = doc.get("parse_method", "?")
    print(f"[{source}][{method}] ✅ [{tx_type}] {doc['name']} — "
          f"{doc['amount']} {doc['currency']} | Bank: {bank_name}")

    # ── Real-time SSE broadcasts in a daemon thread (avoids _sse_lock deadlock) ──
    def _do_broadcasts():
        try:
            broadcast_event("new_expense", doc)
            if doc["date_only"] == date_only_muscat and tx_type == "debit":
                try:
                    _dc = db_conn()
                    _dc.execute("PRAGMA busy_timeout = 3000")
                    _row = _dc.execute(
                        "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE date_only=? AND type='debit'",
                        (date_only_muscat,)
                    ).fetchone()
                    _dc.close()
                    daily_total = float(_row[0]) if _row else 0.0
                except Exception:
                    daily_total = 0.0
                broadcast_event("daily_total", {"date": date_only_muscat, "total": daily_total})
            if balance_updated:
                broadcast_event("balance_update", {
                    "bank_name":  doc["bank_name"],
                    "card_last4": doc["card_last4"],
                    "balance":    doc["available_balance"],
                    "currency":   doc["currency"],
                    "account_id": f"{doc['bank_name']}_{doc['card_last4'] or 'default'}",
                    "amount":     doc["amount"],
                    "merchant":   doc["name"],
                    "tx_type":    tx_type,
                })
            broadcast_event("insight_needed", {
                "date":     date_only_muscat,
                "category": doc.get("category", "other"),
                "amount":   doc["amount"],
                "name":     doc["name"],
            })
        except Exception as _be:
            print(f"[broadcast] error: {_be}")

    import threading as _t2
    _t2.Thread(target=_do_broadcasts, daemon=True).start()

    return doc


def _muscat_today() -> str:
    """Return today's date as YYYY-MM-DD in Asia/Muscat timezone (UTC+4)."""
    try:
        import pytz
        tz = pytz.timezone("Asia/Muscat")
        return datetime.datetime.now(tz).strftime("%Y-%m-%d")
    except ImportError:
        return (datetime.datetime.utcnow() + datetime.timedelta(hours=4)).strftime("%Y-%m-%d")

def _muscat_month() -> str:
    """Return current month as YYYY-MM in Asia/Muscat timezone."""
    return _muscat_today()[:7]

def _normalize_expense(d):
    """Guarantee amount is always float and id field exists.
    Uses Decimal to preserve small values like 0.200 or 0.050."""
    from decimal import Decimal, InvalidOperation
    raw = d.get("amount")
    if raw is None:
        d["amount"] = 0.0
    else:
        try:
            d["amount"] = float(Decimal(str(raw)))
        except (InvalidOperation, ValueError, TypeError):
            d["amount"] = 0.0
    for coord in ("latitude", "longitude", "lat", "lng"):
        v = d.get(coord)
        if v is not None:
            try:
                d[coord] = float(v)
            except (TypeError, ValueError):
                d[coord] = None
    return d


def get_expenses_firebase(date_filter=None, month_filter=None, limit=500):
    """
    Read expenses DIRECTLY from Firestore only.
    Filters on 'date_only' (YYYY-MM-DD, Asia/Muscat tz).
    """
    if not firebase_db:
        print("[DB] ⚠️  Firebase not connected — cannot read expenses for dashboard.")
        return []

    try:
        ref = firebase_db.collection("expenses")

        if date_filter:
            docs = (ref
                    .where("date_only", "==", date_filter)
                    .order_by("date_only", direction="DESCENDING")
                    .limit(limit)
                    .stream())
            result = []
            for doc in docs:
                d = doc.to_dict()
                d["id"] = doc.id
                result.append(_normalize_expense(d))
            if not result:
                print(f"[DB] date_only field empty for {date_filter} — falling back to 'date' field")
                docs2 = (ref
                         .where("date", ">=", date_filter)
                         .where("date", "<=", date_filter + "T99")
                         .order_by("date", direction="DESCENDING")
                         .limit(limit)
                         .stream())
                for doc in docs2:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    if str(d.get("date", "")).startswith(date_filter):
                        result.append(_normalize_expense(d))
            return result

        elif month_filter:
            month_start = month_filter + "-01"
            month_end   = month_filter + "-32"
            docs = (ref
                    .where("date_only", ">=", month_start)
                    .where("date_only", "<=", month_end)
                    .order_by("date_only", direction="DESCENDING")
                    .limit(limit)
                    .stream())
            result = []
            for doc in docs:
                d = doc.to_dict()
                d["id"] = doc.id
                if str(d.get("date_only", "")).startswith(month_filter):
                    result.append(_normalize_expense(d))
            if not result:
                print(f"[DB] date_only empty for month {month_filter} — falling back to 'date' field")
                docs2 = (ref
                         .where("date", ">=", month_filter + "-01")
                         .where("date", "<=", month_filter + "-32")
                         .order_by("date", direction="DESCENDING")
                         .limit(limit)
                         .stream())
                for doc in docs2:
                    d = doc.to_dict()
                    d["id"] = doc.id
                    if str(d.get("date", "")).startswith(month_filter):
                        result.append(_normalize_expense(d))
            return result

        else:
            docs = (ref
                    .order_by("createdAt", direction="DESCENDING")
                    .limit(limit)
                    .stream())
            return [_normalize_expense({**doc.to_dict(), "id": doc.id}) for doc in docs]

    except Exception as e:
        print(f"[Firebase] ❌ get_expenses_firebase error: {e}")
        return []


def get_expenses_sqlite_fast(date_filter=None, month_filter=None, limit=500):
    """Read expenses directly from local SQLite — fast, no network call.
    Falls back to Firebase ONLY when SQLite is genuinely empty (first boot).
    Any lock/busy/error when data might exist → return [] immediately, never block on Firebase."""
    import sqlite3 as _sqlite3
    from config import db_conn as _db_conn
    sqlite_has_data = None  # None = unknown (COUNT not yet executed)
    conn = None
    try:
        conn = _db_conn()
        conn.execute("PRAGMA busy_timeout = 8000")
        total = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        sqlite_has_data = total > 0
        if total == 0:
            conn.close()
            raise _SQLiteEmpty()

        if date_filter:
            rows = conn.execute(
                """SELECT * FROM expenses
                   WHERE (date LIKE ? OR created_at LIKE ?)
                   ORDER BY created_at DESC LIMIT ?""",
                (date_filter + "%", date_filter + "%", limit)
            ).fetchall()
        elif month_filter:
            rows = conn.execute(
                """SELECT * FROM expenses
                   WHERE (date LIKE ? OR created_at LIKE ?)
                   ORDER BY created_at DESC LIMIT ?""",
                (month_filter + "%", month_filter + "%", limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM expenses ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        conn.close()
        return [_normalize_expense(dict(r)) for r in rows]
    except _SQLiteEmpty:
        if conn:
            try: conn.close()
            except Exception: pass
    except _sqlite3.OperationalError as e:
        if conn:
            try: conn.close()
            except Exception: pass
        print(f"[DB] SQLite busy/locked — returning [] (no Firebase fallback): {e}")
        return []
    except Exception as e:
        if conn:
            try: conn.close()
            except Exception: pass
        print(f"[DB] SQLite fast read error: {e}")
        if sqlite_has_data is None or sqlite_has_data:
            return []
    # Only reach here if SQLite was empty (first boot after wipe)
    return get_expenses_firebase(date_filter=date_filter, month_filter=month_filter, limit=limit)


class _SQLiteEmpty(Exception):
    pass


# Keep alias so internal callers continue to work
def get_expenses_sqlite(date_filter=None, month_filter=None, limit=500):
    """Alias → always delegates to the Firebase-only reader."""
    return get_expenses_firebase(date_filter=date_filter, month_filter=month_filter, limit=limit)


def get_daily_total_firebase(date_str: str) -> float:
    """
    Sum debit expenses for date_str (YYYY-MM-DD, Muscat tz) from Firestore.
    Uses Decimal accumulation to capture all transaction values including very small amounts.
    """
    if not firebase_db:
        print("[DB] ⚠️  Firebase not connected — daily total unavailable.")
        return 0.0
    try:
        from decimal import Decimal
        total = Decimal("0")
        seen_ids: set = set()
        for coll in ("expenses", "transactions"):
            try:
                docs = (firebase_db.collection(coll)
                        .where("date_only", "==", date_str)
                        .stream())
                for doc in docs:
                    if doc.id in seen_ids:
                        continue
                    d = doc.to_dict()
                    if d.get("type", "debit") != "debit":
                        continue
                    try:
                        amt = d.get("amount")
                        if amt is not None:
                            total += Decimal(str(amt))
                            seen_ids.add(doc.id)
                    except Exception:
                        pass
            except Exception as coll_err:
                print(f"[Firebase] daily total ({coll}) date_only query error: {coll_err}")
        if seen_ids:
            return float(total)
        print(f"[DB] No date_only docs for {date_str} — trying legacy 'date' field")
        for coll in ("expenses", "transactions"):
            try:
                docs = (firebase_db.collection(coll)
                        .where("date", ">=", date_str)
                        .where("date", "<=", date_str + "T99")
                        .stream())
                for doc in docs:
                    if doc.id in seen_ids:
                        continue
                    d = doc.to_dict()
                    if not str(d.get("date", "")).startswith(date_str):
                        continue
                    if d.get("type", "debit") != "debit":
                        continue
                    try:
                        amt = d.get("amount")
                        if amt is not None:
                            total += Decimal(str(amt))
                            seen_ids.add(doc.id)
                    except Exception:
                        pass
            except Exception as coll_err:
                print(f"[Firebase] daily total ({coll}) legacy query error: {coll_err}")
        return float(total)
    except Exception as e:
        print(f"[Firebase] ❌ get_daily_total_firebase error: {e}")
        return 0.0


def get_daily_total_sqlite(date_str: str) -> float:
    return get_daily_total_firebase(date_str)


def get_bank_balances_sqlite():
    """Read bank balances — SQLite first (fast), Firebase fallback if SQLite empty."""
    try:
        conn = db_conn()
        rows = conn.execute(
            "SELECT account_id, bank_name, card_last4, balance, currency, updated_at "
            "FROM bank_balances ORDER BY bank_name"
        ).fetchall()
        conn.close()
        if rows:
            result = []
            for r in rows:
                d = dict(r)
                try:
                    d["balance"] = float(d.get("balance") or 0)
                except (TypeError, ValueError):
                    d["balance"] = 0.0
                result.append(d)
            return result
    except Exception as e:
        print(f"[DB] bank_balances SQLite error: {e}")
    # Fallback to Firebase if SQLite empty
    if not firebase_db:
        return []
    try:
        docs = firebase_db.collection("bank_balances").order_by("bank_name").stream()
        result = []
        for doc in docs:
            d = {**doc.to_dict(), "account_id": doc.id}
            try:
                d["balance"] = float(d.get("balance") or 0)
            except (TypeError, ValueError):
                d["balance"] = 0.0
            result.append(d)
        return result
    except Exception as e:
        print(f"[Firebase] ❌ get_bank_balances error: {e}")
        return []

def save_raw_message(chat_id, text, source="telegram"):
    now = datetime.datetime.now().isoformat()
    conn = db_conn()
    conn.execute("INSERT INTO messages (chat_id, raw_text, source, created_at) VALUES (?,?,?,?)",
                 (str(chat_id), text, source, now))
    conn.commit()
    conn.close()
    if firebase_db:
        try:
            firebase_db.collection("messages").add({
                "chat_id": str(chat_id), "raw_text": text,
                "source": source, "created_at": now
            })
        except Exception as e:
            print(f"[Firebase] save_raw_message error: {e}")

def get_raw_messages(limit=100):
    """SQLite first (fast), Firebase fallback if SQLite empty."""
    try:
        conn = db_conn()
        rows = conn.execute(
            "SELECT * FROM messages ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        if rows:
            return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] get_raw_messages SQLite error: {e}")
    if firebase_db:
        try:
            docs = (firebase_db.collection("messages")
                    .order_by("created_at", direction="DESCENDING")
                    .limit(limit)
                    .stream())
            return [{**doc.to_dict(), "id": doc.id} for doc in docs]
        except Exception as e:
            print(f"[Firebase] get_raw_messages error: {e}")
    return []
