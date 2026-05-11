from config import *


# ── Database (Turso or SQLite) ────────────────────────────────

def turso_exec(sql, params=()):
    """Execute SQL on Turso via HTTP API."""
    args = [{"type": "null"} if p is None else {"type": "text", "value": str(p)} for p in params]
    payload = {
        "requests": [
            {"type": "execute", "stmt": {"sql": sql, "args": args}},
            {"type": "close"}
        ]
    }
    url = TURSO_URL.replace("libsql://", "https://")
    r = requests.post(
        f"{url}/v2/pipeline",
        headers={"Authorization": f"Bearer {TURSO_TOKEN}", "Content-Type": "application/json"},
        json=payload, timeout=15
    )
    r.raise_for_status()
    return r.json()


def turso_multi(queries):
    """تنفيذ عدة queries في request HTTP واحد — أسرع بكثير"""
    if not USE_TURSO:
        return None
    requests_list = []
    for sql, params in queries:
        args = [{"type": "null"} if p is None else {"type": "text", "value": str(p)} for p in params]
        requests_list.append({"type": "execute", "stmt": {"sql": sql, "args": args}})
    requests_list.append({"type": "close"})
    url = TURSO_URL.replace("libsql://", "https://")
    try:
        r = requests.post(
            f"{url}/v2/pipeline",
            headers={"Authorization": f"Bearer {TURSO_TOKEN}", "Content-Type": "application/json"},
            json={"requests": requests_list},
            timeout=15
        )
        r.raise_for_status()
        results = r.json()["results"]
        out = []
        for res in results[:-1]:  # آخر واحد هو close
            if res.get("type") == "error":
                print("Turso multi error:", res)
                out.append([])
                continue
            data = res["response"]["result"]
            cols = [c["name"] for c in data["cols"]]
            rows = []
            for row in data["rows"]:
                d = {}
                for j, col in enumerate(cols):
                    v = row[j]
                    t = v.get("type", "text")
                    val = v.get("value")
                    if t == "null" or val is None:
                        d[col] = None
                    elif t == "integer":
                        try: d[col] = int(val)
                        except: d[col] = val
                    elif t in ("float", "real"):
                        try: d[col] = float(val)
                        except: d[col] = val
                    else:
                        d[col] = val
                rows.append(d)
            out.append(rows)
        return out
    except Exception as e:
        print("turso_multi error:", e)
        return None


def turso_get(sql, params=()):
    """Query rows from Turso."""
    try:
        res = turso_exec(sql, params)
        result = res["results"][0]
        if result.get("type") == "error":
            print("Turso error:", result)
            return []
        data = result["response"]["result"]
        cols = [c["name"] for c in data["cols"]]
        rows = []
        for row in data["rows"]:
            d = {}
            for i, col in enumerate(cols):
                v = row[i]
                t = v.get("type", "text")
                val = v.get("value")
                if t == "null" or val is None:
                    d[col] = None
                elif t in ("integer",):
                    try: d[col] = int(val)
                    except: d[col] = val
                elif t in ("float", "real"):
                    try: d[col] = float(val)
                    except: d[col] = val
                else:
                    d[col] = val
            rows.append(d)
        return rows
    except Exception as e:
        print("Turso get error:", e)
        return []


def turso_run(sql, params=()):
    """Execute write SQL on Turso."""
    try:
        res = turso_exec(sql, params)
        if res["results"][0].get("type") == "error":
            print("Turso run error:", res["results"][0])
    except Exception as e:
        print("Turso run error:", e)


def _sqlite_run(sql, params=()):
    """تشغيل SQL على SQLite المحلي."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(sql, params)
        conn.commit()
        conn.close()
    except Exception as e:
        pass  # يتجاهل أخطاء الـ migrations (عمود موجود مسبقاً)


def init_db():
    """تهيئة قاعدة البيانات — يُستدعى مرة واحدة فقط من app.py"""

    main_tables = [
        """CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            desc TEXT NOT NULL,
            amt REAL NOT NULL,
            date TEXT NOT NULL,
            month TEXT NOT NULL,
            img TEXT,
            paid_by TEXT,
            payment_method TEXT,
            sale_time TEXT,
            shelf_id INTEGER,
            category TEXT,
            created TEXT DEFAULT (datetime('now')))""",

        """CREATE TABLE IF NOT EXISTS shelves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            color TEXT DEFAULT '#e8547a',
            rent REAL DEFAULT 0)""",

        """CREATE TABLE IF NOT EXISTS shelf_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shelf_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER DEFAULT 0,
            img TEXT,
            created TEXT DEFAULT (datetime('now')))""",

        """CREATE TABLE IF NOT EXISTS flowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            unit TEXT DEFAULT 'وردة',
            updated TEXT DEFAULT (datetime('now')))""",

        """CREATE TABLE IF NOT EXISTS flower_invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT DEFAULT '',
            invoice_number TEXT DEFAULT NULL,
            inv_date TEXT DEFAULT '',
            month TEXT DEFAULT '',
            total REAL DEFAULT 0,
            is_paid INTEGER DEFAULT 0,
            items TEXT DEFAULT '[]',
            created TEXT DEFAULT (datetime('now')))""",

        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            type TEXT DEFAULT 'monthly',
            last_paid TEXT,
            month TEXT,
            note TEXT,
            created TEXT DEFAULT (datetime('now')))""",

        # ✅ إصلاح: جدول app_settings كان مفقوداً
        """CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL)""",
    ]

    shelf_defaults = [
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('ريحان',   '#f07090', 10)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('فتحية',   '#4ecdc4',  8)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('فطوم',    '#b794f4',  8)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('اكسسوارات','#f5c842', 18)),
    ]

    expense_defaults = [
        ("راتب العامل",  220, "monthly"),
        ("إيجار المحل",  100, "monthly"),
        ("تعبئة كهرباء",   0, "variable"),
    ]

    # Migrations — تُجاهل إذا العمود موجود
    migrations = [
        "ALTER TABLE entries ADD COLUMN paid_by TEXT",
        "ALTER TABLE entries ADD COLUMN payment_method TEXT",
        "ALTER TABLE entries ADD COLUMN sale_time TEXT",
        "ALTER TABLE entries ADD COLUMN shelf_id INTEGER",
        "ALTER TABLE entries ADD COLUMN category TEXT",
        "ALTER TABLE shelves ADD COLUMN rent REAL DEFAULT 0",
        "ALTER TABLE flowers ADD COLUMN unit TEXT DEFAULT 'وردة'",
        "ALTER TABLE flower_invoices ADD COLUMN invoice_number TEXT DEFAULT NULL",
        "ALTER TABLE flower_invoices ADD COLUMN is_paid INTEGER DEFAULT 0",
    ]

    if USE_TURSO:
        for sql in main_tables:
            turso_run(sql)
        for sql, params in shelf_defaults:
            turso_run(sql, params)
        for sql in migrations:
            turso_run(sql)  # أخطاء "column already exists" تُتجاهل تلقائياً
        # تنظيف المصاريف المكررة
        all_exp = turso_get("SELECT id, name FROM expenses ORDER BY id")
        seen = {}
        for e in all_exp:
            if e["name"] in seen:
                turso_run("DELETE FROM expenses WHERE id=?", (e["id"],))
            else:
                seen[e["name"]] = e["id"]
        # إضافة المصاريف الافتراضية
        for name, amt, typ in expense_defaults:
            if not turso_get("SELECT id FROM expenses WHERE name=?", (name,)):
                turso_run("INSERT INTO expenses (name,amount,type) VALUES (?,?,?)", (name, amt, typ))
    else:
        conn = sqlite3.connect(DB_PATH)
        for sql in main_tables:
            conn.execute(sql)
        for sql, params in shelf_defaults:
            try: conn.execute(sql, params)
            except: pass
        for sql in migrations:
            try: conn.execute(sql)
            except: pass
        for name, amt, typ in expense_defaults:
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO expenses (name,amount,type) VALUES (?,?,?)",
                    (name, amt, typ)
                )
            except: pass
        conn.commit()
        conn.close()


# ── Public API ────────────────────────────────────────────────

def db_get(sql, params=()):
    if USE_TURSO:
        return turso_get(sql, params)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def db_one(sql, params=()):
    rows = db_get(sql, params)
    return rows[0] if rows else None


def db_run(sql, params=()):
    if USE_TURSO:
        turso_run(sql, params)
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute(sql, params)
    conn.commit()
    conn.close()


def db_setting(key, default=None):
    """اقرأ إعداد من app_settings."""
    try:
        row = db_one("SELECT value FROM app_settings WHERE key=?", (key,))
        return row["value"] if row else default
    except Exception as e:
        print(f"settings get error: {e}")
        return default


def db_setting_set(key, value):
    """احفظ إعداد في app_settings."""
    try:
        db_run(
            "INSERT INTO app_settings (key,value) VALUES (?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value))
        )
    except Exception as e:
        print(f"settings set error: {e}")
