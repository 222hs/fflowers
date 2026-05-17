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
