"""
app.py — Entry point for مصروفاتي  (v2 — Full Edit + Smart Learning)
Creates the Flask app, registers all Blueprints, runs startup.

NEW in v2
─────────
• Inline "✏️ Edit" button on every Telegram confirmation message.
• Multi-step edit flow via callback_query:
    Category  │  Place Type  │  Vendor Name  │  Amount  │  Fix GPS
• Smart category learning:
    Saving a manual correction writes to category_rules (Firestore + SQLite)
    and back-fills all past expenses for that vendor.
• Dynamic location pinning:
    /pin_<expense_id>  command + location attachment pins the True Location
    for a vendor and back-fills all existing geo-tagged expenses.
• POST /api/callback  receives Telegram callback_query updates from the
    Telegram getUpdates loop (bot_polling.py already calls handle_telegram;
    we extend it to also dispatch callback_queries).
• POST /api/pin-location  REST endpoint for the dashboard map to send a
    corrected lat/lon for a vendor.
• GET  /api/category-rules  to inspect all learned rules.

Module map (unchanged from v1 except new routes/logic in this file)
  config.py           → ENV vars, SQLite schema, db_conn()
  firebase.py         → Firebase init, SSE queue, broadcast_event()
  ai_engine.py        → AI providers, GPS extraction, hybrid_parse()
  regex_templates.py  → Self-learning regex system
  db_helpers.py       → save_expense(), get_expenses_*(), get_bank_balances_*()
  telegram_handler.py → handle_telegram(), tg_send()
  routes.py           → Main Flask routes (bp Blueprint)
  merchant_routes.py  → Merchant category overrides (bp_merchant Blueprint)
"""

import datetime
import json
import os
import threading
import time

import requests
from flask import Flask, request, jsonify, session, redirect

# ── Flask app ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "masarifati-secret-2024-hussain")

# ── Auth middleware ─────────────────────────────────────────────────────
# Public paths that don't require a login session
_PUBLIC_PREFIXES = (
    "/login",
    "/api/login",
    "/api/logout",
    "/api/preview-stream",   # public SSE — login page real-time
    "/api/login-preview",    # public data — login page preview
    "/webhook",              # Telegram webhook (no /api/ prefix)
    "/api/webhook",          # Telegram webhook (api prefix)
    "/api/telegram",         # Telegram long-poll fallback
    "/api/callback",         # Telegram callback_query
    "/api/sms",              # iOS Shortcut legacy
    "/api/stream",           # SSE dashboard stream (session checked inside)
    "/health",               # health check
    "/api/admin/reset-db",   # emergency DB repair (password-protected)
)

@app.before_request
def require_login():
    path = request.path
    # Allow public endpoints
    if any(path == p or path.startswith(p + "/") or path.startswith(p + "?")
           for p in _PUBLIC_PREFIXES):
        return
    # Allow if already authenticated
    if session.get("authed"):
        return
    # API calls → 401 JSON (so JS can handle it)
    if path.startswith("/api/"):
        return jsonify({"error": "unauthorized", "redirect": "/login"}), 401
    # Browser requests → redirect to login
    return redirect("/login")

# ── Register existing Blueprints ───────────────────────────────────────
from routes import bp
from merchant_routes import bp_merchant
from ai_training import bp_learning   # AI Training — ملف مستقل بداتابيس خاص
from categories_routes import bp_categories, bp_theme, bp_weather  # NEW: Enhanced categories + dynamic theme

app.register_blueprint(bp)
app.register_blueprint(bp_merchant)
app.register_blueprint(bp_learning)
app.register_blueprint(bp_categories)  # NEW
app.register_blueprint(bp_theme)       # NEW
app.register_blueprint(bp_weather)     # NEW

# ── Lazy imports (avoid circular at module load) ───────────────────────
from config import BOT_TOKEN, db_conn
from firebase import firebase_db, broadcast_event

# ═══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

VALID_CATEGORIES = [
    # الفئات الأساسية
    "food", "shopping", "transport", "bills", "health",
    "entertainment", "education", "groceries", "fuel", "rent",
    "subscriptions", "transfer", "savings", "other",
    
    # الفئات الجديدة - مطاعم ومقاهي
    "restaurants", "cafes", "hot_drinks", "cold_drinks", "fastfood", "desserts", "bakery",
    
    # بقالة
    "supermarkets", "monthly_ration", "vegetables", "meat", "dairy", "snacks",
    
    # موضة
    "clothing", "shoes", "bags", "accessories", "jewelry", "watches",
    
    # جمال
    "perfumes", "cosmetics", "skincare", "haircare",
    
    # صحة
    "pharmacy", "hospital", "dental", "fitness",
    
    # مواصلات
    "taxi", "parking", "maintenance",
    
    # فواتير
    "utilities", "telecom", "insurance",
    
    # ترفيه
    "cinema", "gaming", "books", "hobbies",
    
    # تعليم
    "school", "university", "courses", "tutoring",
    
    # إلكترونيات
    "phones", "computers", "accessories_tech", "appliances",
    
    # منزل
    "furniture", "decor", "cleaning",
    
    # سفر
    "flights", "hotels", "tourism", "visa",
    
    # أخرى
    "charity",
]

VALID_PLACE_TYPES = [
    # الأنواع الأساسية
    "cafe", "restaurant", "pharmacy", "supermarket", "petrol_station",
    "hospital", "school", "mall", "online", "bank", "gym",
    "salon", "hotel", "transport", "other",
    
    # الأنواع الجديدة - مطاعم ومقاهي
    "coffee_shop", "fast_food", "bakery", "juice_bar", "ice_cream", "food_court",
    
    # تسوق
    "hypermarket", "grocery", "boutique", "clothing_store", "shoe_store",
    "jewelry", "electronics", "bookstore", "toy_store", "gift_shop", "market",
    
    # صحة وجمال
    "clinic", "dental", "optical", "barber", "spa", "beauty_center",
    
    # خدمات
    "car_wash", "garage", "atm", "post_office", "laundry", "tailor", "printing",
    
    # ترفيه
    "cinema", "theater", "museum", "park", "beach", "resort", 
    "tourist_spot", "amusement_park",
    
    # تعليم
    "university", "library", "training_center", "office",
    
    # مواصلات
    "taxi", "airport", "bus_station", "parking",
    
    # أونلاين
    "app_store", "subscription",
    
    # أخرى
    "government", "mosque", "charity",
]

CAT_EMOJI = {
    # الأساسية
    "food": "🍕", "shopping": "🛍️", "transport": "🚗", "bills": "📄",
    "health": "💊", "entertainment": "🎮", "education": "📚",
    "groceries": "🛒", "fuel": "⛽", "rent": "🏠",
    "subscriptions": "🔄", "transfer": "💸", "savings": "💰", "other": "📦",
    
    # مطاعم ومقاهي
    "restaurants": "🍽️", "cafes": "☕", "hot_drinks": "🫖", "cold_drinks": "🥤",
    "fastfood": "🍔", "desserts": "🍰", "bakery": "🥐",
    
    # بقالة
    "supermarkets": "🏪", "monthly_ration": "📦", "vegetables": "🥗", 
    "meat": "🥩", "dairy": "🥛", "snacks": "🍿",
    
    # موضة
    "clothing": "👕", "shoes": "👟", "bags": "👜", "accessories": "⌚",
    "jewelry": "💍", "watches": "⌚",
    
    # جمال
    "perfumes": "🌸", "cosmetics": "💅", "skincare": "🧴", "haircare": "💇",
    
    # صحة
    "pharmacy": "💊", "hospital": "🏥", "dental": "🦷", "fitness": "💪",
    
    # مواصلات
    "taxi": "🚖", "parking": "🅿️", "maintenance": "🔧",
    
    # فواتير
    "utilities": "💡", "telecom": "📱", "insurance": "🛡️",
    
    # ترفيه
    "cinema": "🎬", "gaming": "🎮", "books": "📚", "hobbies": "🎨",
    
    # تعليم
    "school": "🏫", "university": "🎓", "courses": "💻", "tutoring": "👨‍🏫",
    
    # إلكترونيات
    "phones": "📱", "computers": "💻", "accessories_tech": "🎧", "appliances": "🏠",
    
    # منزل
    "furniture": "🛋️", "decor": "🎨", "cleaning": "🧹",
    
    # سفر
    "flights": "✈️", "hotels": "🏨", "tourism": "🗺️", "visa": "🛂",
    
    # أخرى
    "charity": "🤲",
}

PLACE_EMOJI = {
    # الأساسية
    "cafe": "☕", "restaurant": "🍽️", "pharmacy": "💊",
    "supermarket": "🛒", "petrol_station": "⛽", "hospital": "🏥",
    "school": "🏫", "mall": "🏬", "online": "🌐", "bank": "🏦",
    "gym": "💪", "salon": "✂️", "hotel": "🏨", "transport": "🚌", "other": "📍",
    
    # الجديدة
    "coffee_shop": "☕", "fast_food": "🍔", "bakery": "🥐", "juice_bar": "🥤",
    "ice_cream": "🍦", "food_court": "🍱", "hypermarket": "🏬", "grocery": "🏪",
    "boutique": "👗", "clothing_store": "👕", "shoe_store": "👟", "jewelry": "💍",
    "electronics": "📱", "bookstore": "📚", "toy_store": "🧸", "gift_shop": "🎁",
    "market": "🏪", "clinic": "🩺", "dental": "🦷", "optical": "👓",
    "barber": "💈", "spa": "🧖", "beauty_center": "💅", "car_wash": "🚿",
    "garage": "🔧", "atm": "🏧", "post_office": "📮", "laundry": "🧺",
    "tailor": "🧵", "printing": "🖨️", "cinema": "🎬", "theater": "🎭",
    "museum": "🏛️", "park": "🏞️", "beach": "🏖️", "resort": "🏝️",
    "tourist_spot": "📸", "amusement_park": "🎢", "university": "🎓",
    "library": "📖", "training_center": "📋", "office": "🏢", "taxi": "🚖",
    "airport": "✈️", "bus_station": "🚏", "parking": "🅿️",
    "app_store": "📲", "subscription": "🔄", "government": "🏛️",
    "mosque": "🕌", "charity": "🤲",
}

# ═══════════════════════════════════════════════════════════════════════
#  SQLITE SCHEMA MIGRATION  (adds category_rules + place_type columns)
# ═══════════════════════════════════════════════════════════════════════

def _migrate_schema():
    """Run once at startup — safe to call repeatedly (idempotent)."""
    conn = db_conn()
    # category_rules table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS category_rules (
            merchant_key  TEXT PRIMARY KEY,
            category      TEXT NOT NULL,
            place_type    TEXT DEFAULT '',
            hit_count     INTEGER DEFAULT 1,
            updated_at    TEXT
        )
    """)
    # vendor_locations table — stores corrected GPS per vendor
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vendor_locations (
            merchant_key  TEXT PRIMARY KEY,
            latitude      REAL NOT NULL,
            longitude     REAL NOT NULL,
            pinned_at     TEXT
        )
    """)
    # Add place_type column to expenses if missing
    for col, defn in [
        ("place_type", "TEXT DEFAULT ''"),
        ("edit_history", "TEXT DEFAULT ''"),
    ]:
        try:
            conn.execute(f"ALTER TABLE expenses ADD COLUMN {col} {defn}")
        except Exception:
            pass
    conn.commit()
    conn.close()
    print("[Schema] ✅ Migration complete (category_rules, vendor_locations, place_type)")

_migrate_schema()


# ═══════════════════════════════════════════════════════════════════════
#  TELEGRAM HELPERS
# ═══════════════════════════════════════════════════════════════════════

def tg_send(chat_id, text, reply_markup=None):
    """Send a plain text message, optionally with an inline keyboard."""
    if not BOT_TOKEN:
        return
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=10,
        )
    except Exception as e:
        print(f"[TG] sendMessage error: {e}")


def tg_edit_message(chat_id, message_id, text, reply_markup=None):
    """Edit an existing bot message (used to update the inline keyboard state)."""
    if not BOT_TOKEN:
        return
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup is not None:
        payload["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            json=payload,
            timeout=10,
        )
    except Exception as e:
        print(f"[TG] editMessageText error: {e}")


def tg_answer_callback(callback_query_id, text="✅"):
    """Acknowledge a callback_query (removes the loading spinner)."""
    if not BOT_TOKEN:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
            json={"callback_query_id": callback_query_id, "text": text},
            timeout=5,
        )
    except Exception as e:
        print(f"[TG] answerCallbackQuery error: {e}")


# ═══════════════════════════════════════════════════════════════════════
#  CONFIRMATION MESSAGE BUILDER
# ═══════════════════════════════════════════════════════════════════════

def _build_confirmation(doc: dict, method_tag: str = "🤖 AI") -> tuple[str, dict]:
    """
    Returns (message_text, inline_keyboard) for a saved expense.
    All current field values are displayed and an Edit button is provided.
    """
    cat_em   = CAT_EMOJI.get(doc.get("category", "other"), "📦")
    place_em = PLACE_EMOJI.get(doc.get("place_type", ""), "📍")
    gps_status = "✅ GPS" if doc.get("latitude") else "❌ No GPS"
    tx_type    = doc.get("type", "debit")
    eid        = doc.get("id", "")

    if tx_type == "transfer_out":
        type_label = "💸 تحويل صادر"
    elif tx_type == "credit":
        type_label = "💚 وارد"
    else:
        type_label = "✅ مصروف"

    bal_line   = f"\n💳 الرصيد: <b>{doc['available_balance']:.3f} {doc.get('currency','OMR')}</b>" \
                 if doc.get("available_balance") is not None else ""
    bank_line  = f"\n🏦 {doc['bank_name']}" if doc.get("bank_name") else ""
    gps_line   = (f"\n📍 GPS: <code>{doc['latitude']:.6f}, {doc['longitude']:.6f}</code>"
                  if doc.get("latitude") else "\n📍 GPS: ❌ غير مسجّل")
    place_line = (f"\n{place_em} النوع: {doc['place_type']}"
                  if doc.get("place_type") else "")

    text = (
        f"{type_label}\n\n"
        f"💰 المبلغ: <b>{doc['amount']:.3f} {doc.get('currency','OMR')}</b>\n"
        f"🏪 المتجر: <b>{doc.get('name','؟')}</b>\n"
        f"{cat_em} الفئة: <b>{doc.get('category','other')}</b>"
        f"{place_line}"
        f"{bank_line}"
        f"{bal_line}"
        f"{gps_line}\n"
        f"📅 التاريخ: {doc.get('date','')}\n\n"
        f"<i>حُلِّلت بـ: <b>{method_tag}</b></i>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🏷️ الفئة",      "callback_data": f"edit_cat|{eid}"},
                {"text": "📍 النوع",       "callback_data": f"edit_place|{eid}"},
            ],
            [
                {"text": "✏️ الاسم",       "callback_data": f"edit_name|{eid}"},
                {"text": "💰 المبلغ",      "callback_data": f"edit_amount|{eid}"},
            ],
            [
                {"text": "📌 تثبيت الموقع", "callback_data": f"edit_gps|{eid}"},
            ],
        ]
    }
    return text, keyboard


# ═══════════════════════════════════════════════════════════════════════
#  PENDING EDIT STATE  (in-memory; keyed by chat_id)
# ═══════════════════════════════════════════════════════════════════════
# Structure: { chat_id: {"field": str, "expense_id": str, "msg_id": int} }
_pending_edits: dict = {}
_pending_lock  = threading.Lock()


def _set_pending(chat_id, field: str, expense_id: str, msg_id: int = 0):
    with _pending_lock:
        _pending_edits[str(chat_id)] = {
            "field":      field,
            "expense_id": expense_id,
            "msg_id":     msg_id,
        }


def _get_pending(chat_id) -> dict | None:
    return _pending_edits.get(str(chat_id))


def _clear_pending(chat_id):
    _pending_edits.pop(str(chat_id), None)


# ═══════════════════════════════════════════════════════════════════════
#  CATEGORY RULES  (learning engine)
# ═══════════════════════════════════════════════════════════════════════

def save_category_rule(merchant_name: str, category: str, place_type: str = "") -> int:
    """
    Persist a category (and optional place_type) rule for a vendor.
    Back-fills all matching expenses in SQLite and Firestore.
    Returns the number of SQLite rows updated.
    """
    if not merchant_name or not category:
        return 0
    key = merchant_name.strip().lower()
    now = datetime.datetime.now().isoformat()

    # ── SQLite ────────────────────────────────────────────────────────
    conn = db_conn()
    conn.execute("""
        INSERT INTO category_rules (merchant_key, category, place_type, hit_count, updated_at)
        VALUES (?, ?, ?, 1, ?)
        ON CONFLICT(merchant_key) DO UPDATE SET
            category   = excluded.category,
            place_type = CASE WHEN excluded.place_type != '' THEN excluded.place_type ELSE place_type END,
            hit_count  = hit_count + 1,
            updated_at = excluded.updated_at
    """, (key, category, place_type, now))

    # Also update legacy merchant_categories table for backwards compat
    conn.execute(
        "INSERT OR REPLACE INTO merchant_categories (merchant_key, category, updated_at) VALUES (?,?,?)",
        (key, category, now)
    )

    # Back-fill expenses
    result = conn.execute(
        "UPDATE expenses SET category=?, place_type=? WHERE LOWER(name)=? AND type='debit'",
        (category, place_type, key)
    ) if place_type else conn.execute(
        "UPDATE expenses SET category=? WHERE LOWER(name)=? AND type='debit'",
        (category, key)
    )
    updated = result.rowcount
    conn.commit()
    conn.close()

    # ── Firestore ─────────────────────────────────────────────────────
    if firebase_db:
        try:
            firebase_db.collection("category_rules").document(key).set({
                "merchant_key": key,
                "category":     category,
                "place_type":   place_type,
                "updated_at":   now,
            }, merge=True)

            # Back-fill Firebase expenses
            docs = (firebase_db.collection("expenses")
                    .where("type", "==", "debit")
                    .stream())
            batch = firebase_db.batch()
            count = 0
            for doc in docs:
                d = doc.to_dict()
                if (d.get("name") or "").lower() == key:
                    update_fields = {"category": category}
                    if place_type:
                        update_fields["place_type"] = place_type
                    batch.update(doc.reference, update_fields)
                    count += 1
                    if count % 500 == 0:
                        batch.commit()
                        batch = firebase_db.batch()
            batch.commit()
            print(f"[Rules] ✅ Saved rule: {key} → {category} ({place_type}), back-filled {count} Firebase docs")
        except Exception as e:
            print(f"[Rules] Firebase sync error: {e}")

    broadcast_event("category_rule_learned", {
        "merchant": merchant_name,
        "category": category,
        "place_type": place_type,
    })
    return updated


def lookup_category_rule(merchant_name: str) -> dict | None:
    """Return {'category': ..., 'place_type': ...} for a vendor, or None."""
    if not merchant_name:
        return None
    key = merchant_name.strip().lower()

    # Check Firestore first (live source of truth)
    if firebase_db:
        try:
            doc = firebase_db.collection("category_rules").document(key).get()
            if doc.exists:
                d = doc.to_dict()
                return {"category": d.get("category"), "place_type": d.get("place_type", "")}
        except Exception:
            pass

    # Fallback to SQLite
    try:
        conn = db_conn()
        row = conn.execute(
            "SELECT category, place_type FROM category_rules WHERE merchant_key=?", (key,)
        ).fetchone()
        conn.close()
        if row:
            return {"category": row["category"], "place_type": row["place_type"] or ""}
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════════════════
#  VENDOR LOCATION PINNING
# ═══════════════════════════════════════════════════════════════════════

def pin_vendor_location(merchant_name: str, lat: float, lon: float) -> int:
    """
    Save a corrected GPS coordinate for a vendor and back-fill all existing
    expenses that reference that vendor name.
    Returns the number of SQLite rows updated.
    """
    if not merchant_name:
        return 0
    key = merchant_name.strip().lower()
    now = datetime.datetime.now().isoformat()

    conn = db_conn()
    conn.execute("""
        INSERT OR REPLACE INTO vendor_locations (merchant_key, latitude, longitude, pinned_at)
        VALUES (?, ?, ?, ?)
    """, (key, lat, lon, now))
    result = conn.execute(
        "UPDATE expenses SET latitude=?, longitude=? WHERE LOWER(name)=?",
        (lat, lon, key)
    )
    updated = result.rowcount
    conn.commit()
    conn.close()

    if firebase_db:
        try:
            firebase_db.collection("vendor_locations").document(key).set({
                "merchant_key": key,
                "latitude":     lat,
                "longitude":    lon,
                "pinned_at":    now,
            })
            # Back-fill Firebase expenses
            docs = firebase_db.collection("expenses").where("name", "==", merchant_name).stream()
            batch = firebase_db.batch()
            count = 0
            for doc in docs:
                batch.update(doc.reference, {"latitude": lat, "longitude": lon})
                count += 1
                if count % 500 == 0:
                    batch.commit()
                    batch = firebase_db.batch()
            batch.commit()
            print(f"[Pin] ✅ Pinned {key} → ({lat:.6f}, {lon:.6f}), updated {count} Firebase docs")
        except Exception as e:
            print(f"[Pin] Firebase error: {e}")

    broadcast_event("location_pinned", {
        "merchant": merchant_name,
        "latitude": lat,
        "longitude": lon,
    })
    return updated


def lookup_pinned_location(merchant_name: str) -> tuple[float, float] | tuple[None, None]:
    """Return (lat, lon) if a pinned location exists for this vendor, else (None, None)."""
    if not merchant_name:
        return None, None
    key = merchant_name.strip().lower()
    if firebase_db:
        try:
            doc = firebase_db.collection("vendor_locations").document(key).get()
            if doc.exists:
                d = doc.to_dict()
                return d.get("latitude"), d.get("longitude")
        except Exception:
            pass
    try:
        conn = db_conn()
        row = conn.execute(
            "SELECT latitude, longitude FROM vendor_locations WHERE merchant_key=?", (key,)
        ).fetchone()
        conn.close()
        if row:
            return row["latitude"], row["longitude"]
    except Exception:
        pass
    return None, None


# ═══════════════════════════════════════════════════════════════════════
#  EXPENSE FIELD UPDATER  (single source of truth for all edits)
# ═══════════════════════════════════════════════════════════════════════

def _update_expense_field(expense_id: str, field: str, value) -> bool:
    """
    Update one field on an expense in both SQLite and Firestore.
    Logs the edit in the edit_history JSON column.
    """
    now = datetime.datetime.now().isoformat()
    conn = db_conn()
    # Append to edit_history
    existing = (conn.execute(
        "SELECT edit_history FROM expenses WHERE id=?", (expense_id,)
    ).fetchone() or {})
    history = []
    try:
        history = json.loads(existing.get("edit_history") or "[]")
    except Exception:
        pass
    history.append({"field": field, "value": str(value), "at": now})
    conn.execute(
        f"UPDATE expenses SET {field}=?, edit_history=? WHERE id=?",
        (value, json.dumps(history), expense_id)
    )
    conn.commit()
    conn.close()

    if firebase_db:
        try:
            firebase_db.collection("expenses").document(expense_id).update({
                field:         value,
                "edit_history": history,
                "updated_at":   now,
            })
        except Exception as e:
            print(f"[Edit] Firebase update error: {e}")
            return False
    return True


def _get_expense(expense_id: str) -> dict | None:
    """Fetch a single expense from Firestore (or SQLite fallback)."""
    if firebase_db:
        try:
            doc = firebase_db.collection("expenses").document(expense_id).get()
            if doc.exists:
                return {**doc.to_dict(), "id": doc.id}
        except Exception:
            pass
    try:
        conn = db_conn()
        row = conn.execute(
            "SELECT * FROM expenses WHERE id=?", (expense_id,)
        ).fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════════════════
#  CALLBACK QUERY DISPATCHER  (handles button presses)
# ═══════════════════════════════════════════════════════════════════════

def handle_callback_query(cq: dict):
    """
    Process a Telegram callback_query from an inline keyboard button.
    cq = the full callback_query object from the Telegram API.
    """
    cq_id    = cq.get("id")
    chat_id  = cq.get("message", {}).get("chat", {}).get("id")
    msg_id   = cq.get("message", {}).get("message_id")
    data     = (cq.get("data") or "").strip()

    if not chat_id or not data:
        return

    tg_answer_callback(cq_id)

    # ── Parse callback data  format: "action|expense_id[|value]" ──────
    parts      = data.split("|")
    action     = parts[0] if parts else ""
    expense_id = parts[1] if len(parts) > 1 else ""
    extra      = parts[2] if len(parts) > 2 else ""

    # ── "edit_cat|<eid>" — show category SECTIONS ─────────────────────
    if action == "edit_cat":
        _set_pending(chat_id, "category", expense_id, msg_id)
        
        # عرض الأقسام الرئيسية
        sections = [
            ("🍽️ مطاعم ومقاهي", "sec_dining"),
            ("🛒 بقالة", "sec_groceries"),
            ("👔 موضة", "sec_fashion"),
            ("💄 جمال", "sec_beauty"),
            ("⚕️ صحة", "sec_health"),
            ("🚗 مواصلات", "sec_transport"),
            ("📄 فواتير", "sec_bills"),
            ("🎮 ترفيه", "sec_entertainment"),
            ("🎓 تعليم", "sec_education"),
            ("📱 إلكترونيات", "sec_electronics"),
            ("🏠 منزل", "sec_home"),
            ("✈️ سفر", "sec_travel"),
            ("📦 أخرى", "sec_other"),
        ]
        
        buttons = []
        for text, callback in sections:
            buttons.append([{"text": text, "callback_data": f"{callback}|{expense_id}"}])
        buttons.append([{"text": "❌ إلغاء", "callback_data": f"cancel|{expense_id}"}])
        
        tg_send(chat_id, "🏷️ اختر القسم:", reply_markup={"inline_keyboard": buttons})
        return
    
    # ── Show categories in a section ──────────────────────────────────
    section_categories = {
        "sec_dining": ["restaurants", "cafes", "hot_drinks", "cold_drinks", "fastfood", "desserts", "bakery"],
        "sec_groceries": ["supermarkets", "monthly_ration", "vegetables", "meat", "dairy", "snacks"],
        "sec_fashion": ["clothing", "shoes", "bags", "accessories", "jewelry", "watches"],
        "sec_beauty": ["perfumes", "cosmetics", "skincare", "haircare"],
        "sec_health": ["pharmacy", "hospital", "dental", "fitness"],
        "sec_transport": ["fuel", "taxi", "parking", "maintenance"],
        "sec_bills": ["utilities", "telecom", "insurance", "subscriptions"],
        "sec_entertainment": ["cinema", "gaming", "books", "hobbies"],
        "sec_education": ["school", "university", "courses", "tutoring"],
        "sec_electronics": ["phones", "computers", "accessories_tech", "appliances"],
        "sec_home": ["rent", "furniture", "decor", "cleaning"],
        "sec_travel": ["flights", "hotels", "tourism", "visa"],
        "sec_other": ["transfer", "savings", "charity", "other"],
    }
    
    if action in section_categories:
        cats = section_categories[action]
        buttons = []
        row = []
        for cat in cats:
            row.append({"text": f"{CAT_EMOJI.get(cat,'📦')} {cat}",
                        "callback_data": f"set_cat|{expense_id}|{cat}"})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([{"text": "🔙 رجوع", "callback_data": f"edit_cat|{expense_id}"}])
        buttons.append([{"text": "❌ إلغاء", "callback_data": f"cancel|{expense_id}"}])
        
        tg_send(chat_id, "🏷️ اختر الفئة:", reply_markup={"inline_keyboard": buttons})
        return

    # ── "set_cat|<eid>|<category>" — save the chosen category ─────────
    if action == "set_cat" and expense_id and extra:
        exp = _get_expense(expense_id)
        if not exp:
            tg_send(chat_id, "❌ لم أجد المعاملة.")
            return

        _update_expense_field(expense_id, "category", extra)

        # Learn the rule for this vendor
        rule = lookup_category_rule(exp.get("name", ""))
        place_type = (rule or {}).get("place_type", "")
        save_category_rule(exp.get("name", ""), extra, place_type)
        _clear_pending(chat_id)

        tg_edit_message(
            chat_id, msg_id,
            f"✅ تم تحديث الفئة إلى <b>{CAT_EMOJI.get(extra,'📦')} {extra}</b>\n"
            f"🧠 <i>تم تعليم النظام: {exp.get('name','')} → {extra}</i>"
        )
        broadcast_event("expense_edited", {"id": expense_id, "field": "category", "value": extra})
        return

    # ── "edit_place|<eid>" — show place-type picker ───────────────────
    if action == "edit_place":
        _set_pending(chat_id, "place_type", expense_id, msg_id)
        buttons = []
        row = []
        for i, pt in enumerate(VALID_PLACE_TYPES):
            row.append({"text": f"{PLACE_EMOJI.get(pt,'📍')} {pt}",
                        "callback_data": f"set_place|{expense_id}|{pt}"})
            if len(row) == 3:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([{"text": "❌ إلغاء", "callback_data": f"cancel|{expense_id}"}])
        tg_send(chat_id, "📍 اختر نوع المكان:", reply_markup={"inline_keyboard": buttons})
        return

    # ── "set_place|<eid>|<type>" — save place type ────────────────────
    if action == "set_place" and expense_id and extra:
        exp = _get_expense(expense_id)
        if not exp:
            tg_send(chat_id, "❌ لم أجد المعاملة.")
            return
        _update_expense_field(expense_id, "place_type", extra)
        # Update the rule with place_type too
        rule = lookup_category_rule(exp.get("name", ""))
        category = (rule or {}).get("category") or exp.get("category", "other")
        save_category_rule(exp.get("name", ""), category, extra)
        _clear_pending(chat_id)
        tg_edit_message(
            chat_id, msg_id,
            f"✅ تم تحديث نوع المكان إلى <b>{PLACE_EMOJI.get(extra,'📍')} {extra}</b>"
        )
        broadcast_event("expense_edited", {"id": expense_id, "field": "place_type", "value": extra})
        return

    # ── "edit_name|<eid>" — prompt for new vendor name ────────────────
    if action == "edit_name":
        _set_pending(chat_id, "name", expense_id, msg_id)
        tg_send(chat_id, "✏️ أرسل الاسم الجديد للمتجر:")
        return

    # ── "edit_amount|<eid>" — prompt for corrected amount ─────────────
    if action == "edit_amount":
        _set_pending(chat_id, "amount", expense_id, msg_id)
        tg_send(chat_id, "💰 أرسل المبلغ الصحيح (مثال: 5.200):")
        return

    # ── "edit_gps|<eid>" — prompt to re-send location ─────────────────
    if action == "edit_gps":
        _set_pending(chat_id, "gps", expense_id, msg_id)
        tg_send(
            chat_id,
            "📌 أرسل موقعك الحالي عبر Telegram (📎 → Location) وسيتم تثبيته\n"
            "كموقع صحيح لهذا المتجر وتحديث جميع مصروفاته السابقة."
        )
        return

    # ── "cancel|<eid>" ─────────────────────────────────────────────────
    if action == "cancel":
        _clear_pending(chat_id)
        tg_edit_message(chat_id, msg_id, "❌ تم الإلغاء.")
        return


# ═══════════════════════════════════════════════════════════════════════
#  EXTEND handle_telegram TO INTERCEPT PENDING EDITS
#  We monkey-patch after the original import so we don't touch
#  telegram_handler.py at all.
# ═══════════════════════════════════════════════════════════════════════

import telegram_handler as _th_module

_original_handle_telegram = _th_module.handle_telegram


def _patched_handle_telegram(chat_id, text, latitude=None, longitude=None):
    """
    Intercepts messages when a pending edit is awaited, otherwise
    falls through to the original handle_telegram.
    """
    pending = _get_pending(chat_id)

    if pending:
        field      = pending["field"]
        expense_id = pending["expense_id"]
        msg_id     = pending["msg_id"]

        # ── GPS correction ─────────────────────────────────────────────
        if field == "gps":
            if latitude is not None and longitude is not None:
                exp = _get_expense(expense_id)
                vendor_name = (exp or {}).get("name", "")
                _update_expense_field(expense_id, "latitude",  latitude)
                _update_expense_field(expense_id, "longitude", longitude)
                if vendor_name:
                    pin_vendor_location(vendor_name, latitude, longitude)
                _clear_pending(chat_id)
                tg_send(
                    chat_id,
                    f"📌 تم تثبيت الموقع الصحيح:\n"
                    f"<code>{latitude:.6f}, {longitude:.6f}</code>\n"
                    f"🏪 <b>{vendor_name}</b>\n"
                    f"🔄 تم تحديث جميع مصروفات هذا المتجر."
                )
                broadcast_event("location_pinned", {
                    "id": expense_id,
                    "merchant": vendor_name,
                    "latitude": latitude,
                    "longitude": longitude,
                })
                return
            else:
                # Text message while waiting for GPS — remind the user
                tg_send(chat_id,
                    "📍 أرسل موقعك كـ Location من Telegram (وليس نصاً).\n"
                    "أو أرسل /cancel لإلغاء العملية.")
                return

        # ── Text-based field edits ─────────────────────────────────────
        text = text.strip()
        if text.lower() in ("/cancel", "إلغاء", "cancel"):
            _clear_pending(chat_id)
            tg_send(chat_id, "❌ تم إلغاء التعديل.")
            return

        if field == "name":
            if len(text) < 2:
                tg_send(chat_id, "⚠️ الاسم قصير جداً. أعد المحاولة أو أرسل /cancel.")
                return
            exp = _get_expense(expense_id)
            _update_expense_field(expense_id, "name", text)
            # Migrate any rule from old name to new name
            if exp:
                old_rule = lookup_category_rule(exp.get("name", ""))
                if old_rule:
                    save_category_rule(text, old_rule["category"], old_rule.get("place_type", ""))
            _clear_pending(chat_id)
            tg_send(chat_id, f"✅ تم تحديث اسم المتجر إلى <b>{text}</b>")
            broadcast_event("expense_edited", {"id": expense_id, "field": "name", "value": text})
            return

        if field == "amount":
            try:
                amount = float(text.replace(",", "."))
                if amount <= 0:
                    raise ValueError("non-positive")
            except ValueError:
                tg_send(chat_id, "⚠️ رقم غير صحيح. مثال: 5.200 — أعد المحاولة أو أرسل /cancel.")
                return
            _update_expense_field(expense_id, "amount", amount)
            _clear_pending(chat_id)
            tg_send(chat_id, f"✅ تم تحديث المبلغ إلى <b>{amount:.3f}</b>")
            broadcast_event("expense_edited", {"id": expense_id, "field": "amount", "value": amount})
            return

        # Unknown field — clear and fall through
        _clear_pending(chat_id)

    # ── Normal SMS / command flow ──────────────────────────────────────
    _original_handle_telegram(chat_id, text, latitude=latitude, longitude=longitude)


# Patch the module so bot_polling.py picks up the new function
_th_module.handle_telegram = _patched_handle_telegram


# ═══════════════════════════════════════════════════════════════════════
#  PATCH save_expense TO ATTACH EDIT BUTTONS + APPLY LEARNED RULES
#  We wrap db_helpers.save_expense so every new transaction automatically:
#   1. Applies a learned category/place_type rule (if one exists).
#   2. Applies a pinned GPS location (if one exists).
#   3. Attaches the enriched confirmation + inline keyboard via Telegram.
# ═══════════════════════════════════════════════════════════════════════

import db_helpers as _db_module

_original_save_expense = _db_module.save_expense


def _patched_save_expense(parsed, source="manual", latitude=None, longitude=None,
                          map_url=None, raw_text="", chat_id=None):
    """
    Wraps save_expense to:
    • Apply learned category / place_type rules before saving.
    • Apply pinned GPS if no live GPS was provided.
    • Send the enriched Telegram confirmation with inline edit buttons.
    """
    # ── 1. Apply category rule if we have one ─────────────────────────
    vendor = (parsed.get("merchant") or parsed.get("name") or "").strip()
    rule   = lookup_category_rule(vendor) if vendor else None

    if rule and parsed.get("type", "debit") == "debit":
        if rule.get("category"):
            parsed = {**parsed, "category": rule["category"]}
        if rule.get("place_type") and not parsed.get("place_type"):
            parsed = {**parsed, "place_type": rule["place_type"]}

    # ── 2. Apply pinned GPS if no live coordinates ────────────────────
    if latitude is None and longitude is None and vendor:
        p_lat, p_lon = lookup_pinned_location(vendor)
        if p_lat is not None:
            latitude  = p_lat
            longitude = p_lon

    # ── 3. Call original save ─────────────────────────────────────────
    doc = _original_save_expense(
        parsed, source,
        latitude=latitude, longitude=longitude,
        map_url=map_url, raw_text=raw_text, chat_id=chat_id
    )

    # Store place_type in the returned doc for the confirmation builder
    doc["place_type"] = parsed.get("place_type", "")

    # ── 4. Send enriched Telegram confirmation with inline keyboard ──────
    # Always send for telegram/webhook/ios — Firebase status doesn't block buttons.
    # telegram_handler.py sends a separate warning if Firebase failed.
    if chat_id and source in ("telegram", "webhook", "ios"):
        parse_method = doc.get("parse_method", "ai")
        ai_provider  = parsed.get("ai_provider", "")
        PROVIDER_ICONS = {
            "Grok": "⚡ Grok", "DeepSeek": "🌊 DeepSeek",
            "Gemini": "♊ Gemini", "ChatGPT": "🟢 ChatGPT",
            "OpenRouter": "🔀 OpenRouter",
        }
        METHOD_ICONS = {
            "regex": "📐 Regex", "template": "📚 Template",
            "learning": "🧠 Learning", "fallback": "🔁 Fallback", "ai": "🤖 AI",
        }
        if parse_method == "ai" and ai_provider:
            method_tag = PROVIDER_ICONS.get(ai_provider, f"🤖 {ai_provider}")
        else:
            method_tag = METHOD_ICONS.get(parse_method, "🤖 AI")

        msg_text, keyboard = _build_confirmation(doc, method_tag)
        tg_send(chat_id, msg_text, reply_markup=keyboard)

    return doc


# Patch db_helpers so telegram_handler.py (which imports save_expense from
# db_helpers) automatically gets the wrapped version.
_db_module.save_expense = _patched_save_expense


# ═══════════════════════════════════════════════════════════════════════
#  EXTEND bot_polling TO ALSO DISPATCH callback_query UPDATES
# ═══════════════════════════════════════════════════════════════════════

import bot_polling as _bp_module

_original_process_update = _bp_module._process_update


def _patched_process_update(update: dict):
    """Handle both regular messages and inline keyboard callbacks."""
    if "callback_query" in update:
        try:
            handle_callback_query(update["callback_query"])
        except Exception as e:
            print(f"[Callback] Error: {e}")
        return
    _original_process_update(update)


_bp_module._process_update = _patched_process_update


# ═══════════════════════════════════════════════════════════════════════
#  NEW REST ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

@app.route("/api/callback", methods=["POST"])
def api_callback():
    """
    Receive raw Telegram update payloads forwarded from the webhook endpoint
    (if you prefer webhook mode over long-polling).
    Dispatches callback_query items to handle_callback_query().
    """
    update = request.json or {}
    if "callback_query" in update:
        threading.Thread(
            target=handle_callback_query,
            args=(update["callback_query"],),
            daemon=True,
        ).start()
    return jsonify({"ok": True})


@app.route("/api/category-rules", methods=["GET"])
def api_get_category_rules():
    """List all learned category rules."""
    try:
        conn = db_conn()
        rows = conn.execute(
            "SELECT merchant_key, category, place_type, hit_count, updated_at "
            "FROM category_rules ORDER BY hit_count DESC"
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/category-rules", methods=["POST"])
def api_set_category_rule():
    """
    Manually create or update a category rule (also usable from the dashboard).
    Body: {"merchant": "Dallat Kookh", "category": "food", "place_type": "cafe"}
    """
    data        = request.json or {}
    merchant    = (data.get("merchant") or "").strip()
    category    = (data.get("category") or "").strip().lower()
    place_type  = (data.get("place_type") or "").strip().lower()

    if not merchant:
        return jsonify({"error": "merchant required"}), 400
    if category and category not in VALID_CATEGORIES:
        return jsonify({"error": f"invalid category. valid: {VALID_CATEGORIES}"}), 400
    if place_type and place_type not in VALID_PLACE_TYPES:
        return jsonify({"error": f"invalid place_type. valid: {VALID_PLACE_TYPES}"}), 400
    if not category:
        return jsonify({"error": "category required"}), 400

    updated = save_category_rule(merchant, category, place_type)
    return jsonify({"ok": True, "merchant": merchant, "category": category,
                    "place_type": place_type, "expenses_updated": updated})


@app.route("/api/category-rules/<path:merchant_key>", methods=["DELETE"])
def api_delete_category_rule(merchant_key):
    """Remove a learned rule (category reverts to AI auto-detection)."""
    key = merchant_key.strip().lower()
    conn = db_conn()
    conn.execute("DELETE FROM category_rules WHERE merchant_key=?", (key,))
    conn.commit()
    conn.close()
    if firebase_db:
        try:
            firebase_db.collection("category_rules").document(key).delete()
        except Exception:
            pass
    return jsonify({"ok": True})


@app.route("/api/pin-location", methods=["POST"])
def api_pin_location():
    """
    Dashboard endpoint — pin the correct GPS for a vendor.
    Body: {"merchant": "Dallat Kookh", "latitude": 23.588, "longitude": 58.383}
    Also accepts {"expense_id": "...", "latitude": ..., "longitude": ...}
    to derive the vendor from an existing expense.
    """
    data       = request.json or {}
    merchant   = (data.get("merchant") or "").strip()
    lat        = data.get("latitude")
    lon        = data.get("longitude")
    expense_id = (data.get("expense_id") or "").strip()

    # Resolve vendor from expense_id if merchant not provided
    if not merchant and expense_id:
        exp = _get_expense(expense_id)
        if exp:
            merchant = exp.get("name", "")

    if not merchant:
        return jsonify({"error": "merchant or expense_id required"}), 400
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return jsonify({"error": "latitude and longitude must be numbers"}), 400

    updated = pin_vendor_location(merchant, lat, lon)
    return jsonify({"ok": True, "merchant": merchant, "latitude": lat,
                    "longitude": lon, "expenses_updated": updated})


@app.route("/api/vendor-locations", methods=["GET"])
def api_vendor_locations():
    """List all pinned vendor locations."""
    try:
        conn = db_conn()
        rows = conn.execute(
            "SELECT merchant_key, latitude, longitude, pinned_at "
            "FROM vendor_locations ORDER BY pinned_at DESC"
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/expense/<eid>/edit", methods=["POST"])
def api_expense_edit(eid):
    """
    Full-field expense editor usable from the dashboard.
    Body: any subset of {name, amount, category, place_type, latitude, longitude, notes}
    When category or place_type change, the rule is learned automatically.
    """
    data = request.json or {}
    allowed = {
        "name", "amount", "category", "place_type",
        "latitude", "longitude", "notes", "currency",
    }
    updates = {k: v for k, v in data.items() if k in allowed and v is not None}
    if not updates:
        return jsonify({"error": "no valid fields"}), 400

    exp = _get_expense(eid)
    if not exp:
        return jsonify({"error": "expense not found"}), 404

    for field, value in updates.items():
        _update_expense_field(eid, field, value)

    # Learn rule if category or place_type changed
    vendor = updates.get("name") or exp.get("name", "")
    if "category" in updates or "place_type" in updates:
        cat   = updates.get("category") or exp.get("category", "other")
        ptype = updates.get("place_type") or exp.get("place_type", "")
        if vendor:
            save_category_rule(vendor, cat, ptype)

    # Pin location if coordinates updated
    if ("latitude" in updates or "longitude" in updates) and vendor:
        new_lat = updates.get("latitude") or exp.get("latitude")
        new_lon = updates.get("longitude") or exp.get("longitude")
        if new_lat and new_lon:
            pin_vendor_location(vendor, float(new_lat), float(new_lon))

    broadcast_event("expense_edited", {"id": eid, "updates": updates})
    return jsonify({"ok": True, "id": eid, "updated_fields": list(updates.keys())})


# ═══════════════════════════════════════════════════════════════════════
#  STARTUP — restore learning data from Firebase into SQLite
# ═══════════════════════════════════════════════════════════════════════

def _restore_learning_data():
    """
    On every boot, pull collections from Firebase into SQLite.
    Expenses for the current + previous month are restored so all
    dashboard reads hit SQLite (fast) instead of Firestore (slow).
    Runs in a background thread to avoid blocking startup.
    """
    from firebase import firebase_db as _fb
    import datetime as _dt
    if not _fb:
        return
    try:
        def _write_batch(rows, sql):
            """Open a fresh connection, write rows, commit, close — releases lock immediately."""
            if not rows:
                return
            c = db_conn()
            try:
                for row in rows:
                    try:
                        c.execute(sql, row)
                    except Exception:
                        pass
                c.commit()
            finally:
                c.close()

        # ── 0. Expenses — current + previous month ──────────────────────
        _now = _dt.datetime.utcnow() + _dt.timedelta(hours=4)
        _months = [
            _now.strftime("%Y-%m"),
            (_now.replace(day=1) - _dt.timedelta(days=1)).strftime("%Y-%m"),
        ]
        count_ex = 0
        for _m in _months:
            try:
                _docs = (
                    _fb.collection("expenses")
                    .where("date_only", ">=", _m + "-01")
                    .where("date_only", "<=", _m + "-32")
                    .stream()
                )
                def _to_coord(v):
                    """Convert Firestore coord (float/str/GeoPoint) to float or None."""
                    if v is None:
                        return None
                    if hasattr(v, "latitude"):   # GeoPoint object
                        return None              # caller handles GeoPoint separately
                    try:
                        from decimal import Decimal
                        return float(Decimal(str(v)))
                    except Exception:
                        return None

                rows = []
                for doc in _docs:
                    d = doc.to_dict()
                    _ts = d.get("created_at") or d.get("timestamp") or _m + "-01T00:00:00"
                    if hasattr(_ts, "isoformat"):
                        _ts = _ts.isoformat()
                    _date_only = (d.get("date_only") or str(d.get("date",""))[:10])

                    # lat/lon: support latitude/longitude, lat/lng, and GeoPoint fields
                    _lat_raw = d.get("latitude") or d.get("lat")
                    _lon_raw = d.get("longitude") or d.get("lng")
                    _geo = d.get("location") or d.get("geopoint")
                    if _geo is not None and hasattr(_geo, "latitude"):
                        _lat_raw, _lon_raw = _geo.latitude, _geo.longitude
                    elif _lat_raw is not None and hasattr(_lat_raw, "latitude"):
                        _lat_raw, _lon_raw = _lat_raw.latitude, _lat_raw.longitude
                    _lat = _to_coord(_lat_raw)
                    _lon = _to_coord(_lon_raw)

                    rows.append((
                        doc.id,
                        d.get("type","debit"), d.get("name",""), d.get("sender",""),
                        float(d.get("amount") or 0), d.get("currency","OMR"),
                        d.get("category","other"),
                        _date_only,
                        _date_only,
                        d.get("notes",""), d.get("source","telegram"),
                        d.get("bank_name",""),
                        float(d.get("available_balance") or 0) if d.get("available_balance") is not None else None,
                        d.get("card_last4",""),
                        _lat, _lon,
                        d.get("map_url",""), d.get("parse_method","ai"), _ts
                    ))
                _write_batch(rows,
                    """INSERT OR REPLACE INTO expenses
                    (id,type,name,sender,amount,currency,category,date,date_only,notes,
                     source,bank_name,available_balance,card_last4,
                     latitude,longitude,map_url,parse_method,created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""")
                count_ex += len(rows)
            except Exception as _me:
                print(f"[Startup] ⚠️  expenses restore month {_m}: {_me}")
        print(f"[Startup] ✅ Expenses restored: {count_ex} rows")

        # ── 1. merchant_categories ──────────────────────────────────────
        rows = []
        count_mc = 0
        for doc in _fb.collection("merchant_categories").stream():
            d = doc.to_dict()
            rows.append((d.get("merchant_key") or doc.id, d.get("category","other"), d.get("updated_at","")))
            count_mc += 1
        _write_batch(rows, "INSERT OR REPLACE INTO merchant_categories (merchant_key, category, updated_at) VALUES (?,?,?)")

        # ── 2. regex_templates ──────────────────────────────────────────
        rows = []
        count_rt = 0
        for doc in _fb.collection("regex_templates").stream():
            d = doc.to_dict()
            if d.get("pattern"):
                rows.append((d["pattern"], d.get("bank_name",""), d.get("description",""), d.get("hit_count",0), d.get("created_at","")))
                count_rt += 1
        _write_batch(rows, "INSERT OR IGNORE INTO regex_templates (pattern, bank_name, description, hit_count, created_at) VALUES (?,?,?,?,?)")

        # ── 3. merchant_name_overrides ──────────────────────────────────
        rows = []
        count_mn = 0
        for doc in _fb.collection("merchant_name_overrides").stream():
            d = doc.to_dict()
            if d.get("original_name") and d.get("preferred_name"):
                rows.append(("~name~" + d["original_name"].lower(), d["preferred_name"], d.get("updated_at","")))
                count_mn += 1
        _write_batch(rows, "INSERT OR REPLACE INTO merchant_categories (merchant_key, category, updated_at) VALUES (?,?,?)")

        # ── 4. daily_insights ───────────────────────────────────────────
        rows = []
        for doc in _fb.collection("daily_insights").stream():
            d = doc.to_dict()
            rows.append((doc.id, d.get("insight",""), d.get("created_at","")))
        _write_batch(rows, "INSERT OR REPLACE INTO daily_insights (date, insight, created_at) VALUES (?,?,?)")

        # ── 5. bank_balances ────────────────────────────────────────────
        rows = []
        count_bb = 0
        for doc in _fb.collection("bank_balances").stream():
            d = doc.to_dict()
            rows.append((doc.id, d.get("bank_name",""), d.get("card_last4",""),
                         float(d.get("balance") or 0), d.get("currency","OMR"), d.get("updated_at","")))
            count_bb += 1
        _write_batch(rows, "INSERT OR REPLACE INTO bank_balances (account_id, bank_name, card_last4, balance, currency, updated_at) VALUES (?,?,?,?,?,?)")

        # ── 6. messages (last 100) ──────────────────────────────────────
        count_msg = 0
        try:
            rows = []
            for doc in _fb.collection("messages").limit(100).stream():
                d = doc.to_dict()
                rows.append((d.get("chat_id",""), d.get("raw_text",""), d.get("source","telegram"), d.get("created_at","")))
                count_msg += 1
            _write_batch(rows, "INSERT OR IGNORE INTO messages (chat_id, raw_text, source, created_at) VALUES (?,?,?,?)")
        except Exception as _me:
            print(f"[Startup] ⚠️  messages restore: {_me}")
        print(f"[Startup] ✅ Restored from Firebase — "
              f"merchant_categories: {count_mc}, regex_templates: {count_rt}, "
              f"name_overrides: {count_mn}, bank_balances: {count_bb}, messages: {count_msg}")
    except Exception as e:
        print(f"[Startup] ⚠️  restore_learning_data error: {e}")


threading.Thread(target=_restore_learning_data, daemon=True).start()

from merchant_routes import setup
setup()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
