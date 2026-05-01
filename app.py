import os
import sqlite3
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DB_PATH   = os.environ.get("DB_PATH", "fairuz.db")

# ── Database ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                type    TEXT NOT NULL,
                desc    TEXT NOT NULL,
                amt     REAL NOT NULL,
                date    TEXT NOT NULL,
                month   TEXT NOT NULL,
                img     TEXT,
                created TEXT DEFAULT (datetime('now'))
            )
        """)
        db.commit()

init_db()

# ── Helpers ───────────────────────────────────────────────
def fmt_omr(n):
    return f"{n:,.3f} ر.ع"

def cur_month():
    return datetime.now().strftime("%Y-%m")

def get_month_data(month):
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM entries WHERE month=? ORDER BY created DESC", (month,)
        ).fetchall()
    sales = [dict(r) for r in rows if r["type"] == "s"]
    buys  = [dict(r) for r in rows if r["type"] == "b"]
    return sales, buys

def month_summary(month):
    sales, buys = get_month_data(month)
    ts = sum(e["amt"] for e in sales)
    tb = sum(e["amt"] for e in buys)
    return ts, tb, ts - tb, len(sales), len(buys)

# ── Simple NLP — no AI needed ─────────────────────────────
SALE_WORDS  = ["بعت","بعت","مبيعة","بيع","بعثت","باعت","وصل","استلم العميل"]
BUY_WORDS   = ["اشتريت","شريت","مشتريات","شراء","دفعت","فاتورة","طلبية"]

def parse_text(text):
    """Parse Arabic text to extract type, description and amount."""
    import re
    text = text.strip()

    # Detect type
    etype = None
    for w in SALE_WORDS:
        if w in text:
            etype = "s"
            break
    if not etype:
        for w in BUY_WORDS:
            if w in text:
                etype = "b"
                break

    # Extract amount — look for numbers (supports Arabic decimal)
    nums = re.findall(r'\d+(?:[.,]\d+)?', text.replace('٫','.'))
    amt = None
    for n in nums:
        try:
            v = float(n.replace(',', '.'))
            if v > 0:
                amt = v
                break
        except:
            pass

    if etype and amt:
        # Clean description — remove amount and trigger words
        desc = text
        for w in SALE_WORDS + BUY_WORDS + ["بـ","ب","ريال","ر.ع","ومان"]:
            desc = desc.replace(w, " ")
        desc = re.sub(r'\d+(?:[.,]\d+)?', '', desc).strip()
        desc = ' '.join(desc.split()) or ("مبيعة" if etype == "s" else "مشتريات")
        return {"type": etype, "desc": desc, "amt": amt, "found": True}

    return {"found": False}

# ── Telegram helpers ──────────────────────────────────────
def tg(chat_id, text):
    if not BOT_TOKEN:
        return
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=10
    )

# Store pending photo entries per chat
pending = {}

# ── Web API ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/entries")
def api_get():
    month = request.args.get("month", cur_month())
    sales, buys = get_month_data(month)
    return jsonify({"sales": sales, "buys": buys})

@app.route("/api/entries", methods=["POST"])
def api_add():
    d = request.json
    month = d.get("month", cur_month())
    with get_db() as db:
        db.execute(
            "INSERT INTO entries (type,desc,amt,date,month,img) VALUES (?,?,?,?,?,?)",
            (d["type"], d["desc"], float(d["amt"]),
             d.get("date", datetime.now().strftime("%d/%m/%Y")),
             month, d.get("img"))
        )
        db.commit()
    return jsonify({"ok": True})

@app.route("/api/entries/<int:eid>", methods=["DELETE"])
def api_del(eid):
    with get_db() as db:
        db.execute("DELETE FROM entries WHERE id=?", (eid,))
        db.commit()
    return jsonify({"ok": True})

# ── Telegram Webhook ──────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    msg  = data.get("message") or data.get("edited_message")
    if not msg:
        return "ok"

    chat_id = msg["chat"]["id"]
    month   = cur_month()
    date    = datetime.now().strftime("%d/%m/%Y")

    # ── Photo received ──
    if "photo" in msg:
        caption = msg.get("caption", "").strip()

        if caption:
            # User sent photo + caption with amount
            parsed = parse_text(caption)
            if parsed["found"]:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",
                        ("b", parsed["desc"] or "مشتريات", parsed["amt"], date, month)
                    )
                    db.commit()
                tg(chat_id,
                   f"✅ <b>تم تسجيل الفاتورة</b>\n\n"
                   f"📦 مشتريات\n"
                   f"📝 {parsed['desc']}\n"
                   f"💰 {fmt_omr(parsed['amt'])}")
            else:
                # Store photo, ask for amount
                pending[chat_id] = {"waiting": "buy_amt", "desc": caption or "مشتريات"}
                tg(chat_id,
                   "🧾 وصلت الفاتورة!\n\n"
                   "كم <b>المبلغ الإجمالي</b>؟\n"
                   "أرسل الرقم فقط مثل: <code>3.520</code>")
        else:
            # No caption — ask for amount
            pending[chat_id] = {"waiting": "buy_amt", "desc": "مشتريات"}
            tg(chat_id,
               "🧾 وصلت الفاتورة!\n\n"
               "كم <b>المبلغ الإجمالي</b>؟\n"
               "أرسل الرقم فقط مثل: <code>3.520</code>")
        return "ok"

    # ── Text message ──
    text = msg.get("text", "").strip()
    if not text:
        return "ok"

    # Handle pending state
    if chat_id in pending:
        state = pending[chat_id]

        if state["waiting"] == "buy_amt":
            try:
                amt = float(text.replace(",", "."))
                desc = state.get("desc", "مشتريات")
                with get_db() as db:
                    db.execute(
                        "INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",
                        ("b", desc, amt, date, month)
                    )
                    db.commit()
                del pending[chat_id]
                tg(chat_id,
                   f"✅ <b>تم التسجيل!</b>\n\n"
                   f"📦 مشتريات\n"
                   f"📝 {desc}\n"
                   f"💰 {fmt_omr(amt)}")
            except:
                tg(chat_id, "⚠️ أرسل رقم صحيح مثل: <code>3.520</code>")
            return "ok"

    # Commands
    if text in ["/start", "/help"]:
        tg(chat_id,
           "🌹 <b>أهلاً بك في فيروز فلورز!</b>\n\n"
           "📌 <b>كيف تسجّل؟</b>\n\n"
           "🌸 <b>مبيعة:</b>\n"
           "<code>بعت باقة ورد بـ 5.500</code>\n\n"
           "📦 <b>مشتريات:</b>\n"
           "<code>اشتريت زهور بـ 12.000</code>\n\n"
           "🧾 <b>فاتورة:</b>\n"
           "أرسل صورة الفاتورة وسأسألك عن المبلغ\n\n"
           "📊 <b>تقرير:</b>\n"
           "<code>/report</code>")
        return "ok"

    if text == "/report":
        ts, tb, tp, sc, bc = month_summary(month)
        emoji = "✅" if tp >= 0 else "⚠️"
        tg(chat_id,
           f"📊 <b>تقرير {month}</b>\n\n"
           f"🌸 <b>المبيعات:</b> {fmt_omr(ts)} ({sc} عملية)\n"
           f"📦 <b>المشتريات:</b> {fmt_omr(tb)} ({bc} عملية)\n"
           f"━━━━━━━━━━━━━\n"
           f"{emoji} <b>صافي الربح:</b> {fmt_omr(tp)}")
        return "ok"

    # Natural language
    parsed = parse_text(text)
    if parsed["found"]:
        etype = parsed["type"]
        desc  = parsed["desc"]
        amt   = parsed["amt"]
        with get_db() as db:
            db.execute(
                "INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",
                (etype, desc, amt, date, month)
            )
            db.commit()
        label = "مبيعة 🌸" if etype == "s" else "مشتريات 📦"
        tg(chat_id,
           f"✅ <b>تم التسجيل!</b>\n\n"
           f"🏷 {label}\n"
           f"📝 {desc}\n"
           f"💰 {fmt_omr(amt)}\n"
           f"📅 {date}")
    else:
        tg(chat_id,
           "لم أفهم الرسالة 🤔\n\n"
           "جرّب:\n"
           "<code>بعت باقة بـ 4.500</code>\n"
           "<code>اشتريت ورد بـ 8.000</code>\n\n"
           "أو /help للمساعدة")

    return "ok"

@app.route("/set_webhook")
def set_webhook():
    host = request.host_url.rstrip("/")
    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
        params={"url": f"{host}/webhook"},
        timeout=10
    )
    return jsonify(r.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
