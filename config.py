# config.py — Environment variables, SQLite schema, db_conn()
import os, sqlite3, datetime

# ==================== CONFIG ====================
BOT_TOKEN         = os.environ.get("BOT_TOKEN", "")
RENDER_URL        = os.environ.get("RENDER_EXTERNAL_URL", "")
PASSWORD          = os.environ.get("PASSWORD", "1234")
FIREBASE_KEY_JSON = os.environ.get("FIREBASE_KEY_JSON", "")
ALLOWED_CHAT_IDS  = [x.strip() for x in os.environ.get("ALLOWED_CHAT_IDS", "").split(",") if x.strip()]
ADMIN_CHAT_ID     = os.environ.get("ADMIN_CHAT_ID", "")

# SQLite path — persists on Render disk or local
SQLITE_PATH = os.environ.get("SQLITE_PATH", "masarifati.db")

# ==================== SQLITE INIT ====================
def init_db():
    conn = sqlite3.connect(SQLITE_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")   # allow concurrent reads during writes
    conn.execute("PRAGMA synchronous=NORMAL") # faster writes, still safe
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id     TEXT,
            raw_text    TEXT,
            source      TEXT DEFAULT 'telegram',
            created_at  TEXT,
            processed   INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id                TEXT PRIMARY KEY,
            type              TEXT DEFAULT 'debit',
            name              TEXT,
            sender            TEXT,
            amount            REAL,
            currency          TEXT DEFAULT 'OMR',
            category          TEXT DEFAULT 'other',
            date              TEXT,
            notes             TEXT,
            source            TEXT DEFAULT 'telegram',
            bank_name         TEXT,
            available_balance REAL,
            card_last4        TEXT,
            latitude          REAL,
            longitude         REAL,
            map_url           TEXT,
            parse_method      TEXT DEFAULT 'ai',
            created_at        TEXT
        )
    """)
    # Migration: add new columns if upgrading from older schema
    for col, defn in [
        ("map_url",      "TEXT"),
        ("parse_method", "TEXT DEFAULT 'ai'"),
        ("recipient",    "TEXT"),
        ("txn_id",       "TEXT"),
        ("date_only",    "TEXT"),
        ("chat_id",      "TEXT"),
    ]:
        try:
            c.execute(f"ALTER TABLE expenses ADD COLUMN {col} {defn}")
        except Exception:
            pass  # column already exists
    # Ensure amount column is REAL — SQLite is flexible but cast on read is our real fix
    c.execute("""
        CREATE TABLE IF NOT EXISTS bank_balances (
            account_id   TEXT PRIMARY KEY,
            bank_name    TEXT,
            card_last4   TEXT,
            balance      REAL,
            currency     TEXT DEFAULT 'OMR',
            updated_at   TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_insights (
            date       TEXT PRIMARY KEY,
            insight    TEXT,
            created_at TEXT
        )
    """)
    # ── Merchant category overrides — user-defined, applied on every future save ──
    c.execute("""
        CREATE TABLE IF NOT EXISTS merchant_categories (
            merchant_key TEXT PRIMARY KEY,
            category     TEXT NOT NULL,
            updated_at   TEXT
        )
    """)
    # ── Self-learning regex templates (created by AI from unrecognised messages) ──
    c.execute("""
        CREATE TABLE IF NOT EXISTS regex_templates (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern      TEXT NOT NULL UNIQUE,
            bank_name    TEXT,
            description  TEXT,
            hit_count    INTEGER DEFAULT 0,
            created_at   TEXT,
            last_used_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ SQLite ready:", SQLITE_PATH)

init_db()

def db_conn():
    try:
        conn = sqlite3.connect(SQLITE_PATH, timeout=30)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.DatabaseError as _e:
        if "malformed" in str(_e).lower() or "disk image" in str(_e).lower():
            print(f"[SQLite] ⚠️ Corrupted DB detected — rebuilding: {_e}", flush=True)
            import os as _os
            for _suffix in ["", "-wal", "-shm"]:
                try: _os.remove(SQLITE_PATH + _suffix)
                except Exception: pass
            init_db()
            conn = sqlite3.connect(SQLITE_PATH, timeout=30)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.row_factory = sqlite3.Row
            return conn
        raise

