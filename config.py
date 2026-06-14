import os
import re
import sqlite3
import json
import requests
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# ── Secret Key (مطلوب للـ sessions) ──────────────────────────
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# ── Keep-Alive ────────────────────────────────────────────────
APP_URL = os.environ.get("RENDER_EXTERNAL_URL", "")

def _keep_alive():
    time.sleep(60)
    while True:
        try:
            if APP_URL:
                requests.get(f"{APP_URL}/ping", timeout=10)
        except:
            pass
        time.sleep(600)

_t = threading.Thread(target=_keep_alive, daemon=True)
_t.start()

# ── مسح كاش التحليل الذكي كل يوم الساعة 22:00 بتوقيت عُمان (18:00 UTC) ──
def _insights_scheduler():
    time.sleep(30)  # انتظر حتى تكتمل تهيئة قاعدة البيانات
    while True:
        try:
            from datetime import timezone
            oman_offset = timedelta(hours=4)
            now_oman = datetime.now(timezone.utc) + oman_offset
            # إذا الساعة 23:40 بتوقيت عُمان → امسح الكاش لإجبار التجديد
            if now_oman.hour == 23 and 40 <= now_oman.minute < 50:
                from database import db_run
                db_run("DELETE FROM app_settings WHERE key IN ('insights_text','insights_date')")
            # افحص كل 5 دقائق
            time.sleep(300)
        except:
            time.sleep(300)

_ti = threading.Thread(target=_insights_scheduler, daemon=True)
_ti.start()

# ── Smart Bot Notifications Scheduler ────────────────────────
def _notifications_scheduler():
    time.sleep(60)  # انتظر تهيئة كل شيء
    last_no_sales_alert = None   # يوم آخر تنبيه "لا مبيعات"
    last_goal_alert = None       # يوم آخر تنبيه "تجاوزت الهدف"
    last_debt_check = None       # يوم آخر فحص ديون
    while True:
        try:
            from datetime import timezone
            from database import db_get, db_one, db_run
            oman_offset = timedelta(hours=4)
            now_oman = datetime.now(timezone.utc) + oman_offset
            today_str = now_oman.strftime("%d/%m/%Y")
            today_date = now_oman.strftime("%Y-%m-%d")

            # ── 1. تنبيه "لا مبيعات" الساعة 6 مساءً عُمان (18:00) ──
            if now_oman.hour == 18 and 0 <= now_oman.minute < 10 and last_no_sales_alert != today_date:
                entries = db_get("SELECT id FROM entries WHERE type='s' AND date=?", (today_str,))
                if not entries:
                    token = os.environ.get("BOT_TOKEN","")
                    chat_id = os.environ.get("OWNER_CHAT_ID","")
                    if token and chat_id:
                        try:
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                json={"chat_id":int(chat_id),"text":"⚠️ <b>تنبيه!</b>\n\nالساعة 6 مساءً ولا توجد مبيعات مسجلة حتى الآن 😟\nهل هناك مبيعات لم تُسجّل؟","parse_mode":"HTML"},
                                timeout=10)
                        except: pass
                    last_no_sales_alert = today_date

            # ── 2. تنبيه "تجاوزت الهدف" ──
            goal_row = db_one("SELECT value FROM app_settings WHERE key='daily_goal'")
            if goal_row:
                try:
                    goal_val = float(goal_row["value"])
                    if goal_val > 0 and last_goal_alert != today_date:
                        entries = db_get("SELECT amt FROM entries WHERE type='s' AND date=? AND shelf_id IS NULL", (today_str,))
                        total = sum(float(e["amt"]) for e in entries)
                        if total >= goal_val:
                            token = os.environ.get("BOT_TOKEN","")
                            chat_id = os.environ.get("OWNER_CHAT_ID","")
                            if token and chat_id:
                                try:
                                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                        json={"chat_id":int(chat_id),"text":f"🎉 <b>تجاوزت الهدف اليومي!</b>\n\n🌸 مبيعات اليوم: {total:,.3f} ر.ع\n🎯 الهدف: {goal_val:,.3f} ر.ع\n\nعمل رائع! 🏆","parse_mode":"HTML"},
                                        timeout=10)
                                except: pass
                            last_goal_alert = today_date
                except: pass

            # ── 3. تنبيه الديون بعد أسبوع (فحص مرة يومياً الساعة 9 صباحاً) ──
            if now_oman.hour == 9 and 0 <= now_oman.minute < 10 and last_debt_check != today_date:
                token = os.environ.get("BOT_TOKEN","")
                chat_id = os.environ.get("OWNER_CHAT_ID","")
                if token and chat_id:
                    try:
                        week_ago = (now_oman - timedelta(days=7)).strftime("%Y-%m-%d")
                        overdue = db_get(
                            "SELECT * FROM debts WHERE paid=0 AND created<=? AND notified=0",
                            (week_ago,))
                        for debt in overdue:
                            msg = (f"💳 <b>تذكير: دين غير مسدد</b>\n\n"
                                   f"👤 {debt['customer_name']}\n"
                                   f"💰 {float(debt['amount']):,.3f} ر.ع\n"
                                   f"📝 {debt.get('description','') or ''}\n"
                                   f"📅 منذ: {debt.get('date','')}\n\n"
                                   f"مضى أسبوع — هل تسددّ؟")
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                json={"chat_id":int(chat_id),"text":msg,"parse_mode":"HTML"},
                                timeout=10)
                            db_run("UPDATE debts SET notified=1 WHERE id=?", (debt["id"],))
                    except: pass
                last_debt_check = today_date

            time.sleep(300)  # افحص كل 5 دقائق
        except:
            time.sleep(300)

_tn = threading.Thread(target=_notifications_scheduler, daemon=True)
_tn.start()

# ── Config ────────────────────────────────────────────────────
BOT_TOKEN       = os.environ.get("BOT_TOKEN", "")
GROQ_KEY        = os.environ.get("GROQ_API_KEY", "")
OPENAI_KEY      = os.environ.get("OPENAI_API_KEY", "")
OPENROUTER_KEY  = os.environ.get("OPENROUTER_API_KEY", "")
GEMINI_KEY      = os.environ.get("GEMINI_API_KEY", "")
DB_PATH         = os.environ.get("DB_PATH", "fairuz.db")
TURSO_URL       = os.environ.get("TURSO_URL", "")
TURSO_TOKEN     = os.environ.get("TURSO_TOKEN", "")
USE_TURSO       = bool(TURSO_URL and TURSO_TOKEN)
APP_PASSWORD    = os.environ.get("APP_PASSWORD", "1233")
WORKER_PASSWORD = os.environ.get("WORKER_PASSWORD", "1233")

# ── Cloudinary ────────────────────────────────────────────────
_cld_url = os.environ.get("CLOUDINARY_URL", "")
if _cld_url.startswith("cloudinary://"):
    _parts = _cld_url[len("cloudinary://"):].split("@")
    _cloud_name = _parts[1] if len(_parts) > 1 else ""
    _key_secret = _parts[0].split(":")
    CLOUDINARY_CLOUD  = _cloud_name
    CLOUDINARY_KEY    = _key_secret[0] if _key_secret else ""
    CLOUDINARY_SECRET = _key_secret[1] if len(_key_secret) > 1 else ""
else:
    CLOUDINARY_CLOUD  = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_KEY    = os.environ.get("CLOUDINARY_API_KEY", "")
    CLOUDINARY_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")

USE_CLOUDINARY = bool(CLOUDINARY_CLOUD and CLOUDINARY_KEY and CLOUDINARY_SECRET)

def cloudinary_upload(img_bytes, folder="fflowers"):
    """Upload image bytes to Cloudinary, return secure_url or empty string."""
    if not USE_CLOUDINARY:
        return ""
    import hashlib, time as _time
    ts = int(_time.time())
    params_str = f"folder={folder}&timestamp={ts}"
    signature = hashlib.sha1((params_str + CLOUDINARY_SECRET).encode()).hexdigest()
    try:
        r = requests.post(
            f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD}/image/upload",
            files={"file": ("image.jpg", img_bytes, "image/jpeg")},
            data={"api_key": CLOUDINARY_KEY, "timestamp": ts,
                  "folder": folder, "signature": signature},
            timeout=30
        )
        return r.json().get("secure_url", "")
    except Exception as e:
        print("Cloudinary upload error:", e)
        return ""
