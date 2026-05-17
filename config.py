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
