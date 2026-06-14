from config import *

# ── Database (Turso or SQLite) ────────────────────────────
def turso_exec(sql, params=()):
    """Execute SQL on Turso via HTTP API."""
    args = [{"type": "null"} if p is None else {"type": "text", "value": str(p)} for p in params]
    payload = {"requests": [{"type": "execute", "stmt": {"sql": sql, "args": args}}, {"type": "close"}]}
    # Fix URL: libsql:// -> https://
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
        args = [{"type":"null"} if p is None else {"type":"text","value":str(p)} for p in params]
        requests_list.append({"type":"execute","stmt":{"sql":sql,"args":args}})
    requests_list.append({"type":"close"})
    url = TURSO_URL.replace("libsql://","https://")
    try:
        r = requests.post(
            f"{url}/v2/pipeline",
            headers={"Authorization":f"Bearer {TURSO_TOKEN}","Content-Type":"application/json"},
            json={"requests": requests_list},
            timeout=15
        )
        r.raise_for_status()
        results = r.json()["results"]
        out = []
        for i, res in enumerate(results[:-1]):  # آخر واحد هو close
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
                    v = row[j]; t = v.get("type","text"); val = v.get("value")
                    if t == "null" or val is None: d[col] = None
                    elif t == "integer":
                        try: d[col] = int(val)
                        except: d[col] = val
                    elif t in ("float","real"):
                        try: d[col] = float(val)
                        except: d[col] = val
                    else: d[col] = val
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
                t = v.get("type","text")
                val = v.get("value")
                if t == "null" or val is None:
                    d[col] = None
                elif t in ("integer",):
                    try: d[col] = int(val)
                    except: d[col] = val
                elif t in ("float","real"):
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

def init_db():
    sqls = [
        """CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, desc TEXT NOT NULL,
            amt REAL NOT NULL, date TEXT NOT NULL,
            month TEXT NOT NULL, img TEXT,
            paid_by TEXT, payment_method TEXT,
            sale_time TEXT, shelf_id INTEGER,
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS shelves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            color TEXT DEFAULT '#e8547a',
            rent REAL DEFAULT 0)""",
        """CREATE TABLE IF NOT EXISTS shelf_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shelf_id INTEGER NOT NULL, name TEXT NOT NULL,
            price REAL NOT NULL, qty INTEGER DEFAULT 0,
            img TEXT, created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL)""",
    ]
    shelf_rows = [
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('ريحان','#f07090',10)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('فتحية','#4ecdc4',8)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('فطوم','#b794f4',8)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('اكسسوارات','#f5c842',18)),
    ]
    migrations = [
        "ALTER TABLE entries ADD COLUMN paid_by TEXT",
        "ALTER TABLE entries ADD COLUMN payment_method TEXT",
        "ALTER TABLE entries ADD COLUMN sale_time TEXT",
        "ALTER TABLE entries ADD COLUMN shelf_id INTEGER",
        "ALTER TABLE shelves ADD COLUMN rent REAL DEFAULT 0",
        "ALTER TABLE entries ADD COLUMN category TEXT",
    ]
    # Flowers inventory table
    flowers_sql = """CREATE TABLE IF NOT EXISTS flowers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        count INTEGER DEFAULT 0,
        unit TEXT DEFAULT 'وردة',
        updated TEXT DEFAULT (datetime('now')))"""
    flower_inv_sql = """CREATE TABLE IF NOT EXISTS flower_invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT DEFAULT '',
        invoice_number TEXT DEFAULT NULL,
        inv_date TEXT DEFAULT '',
        month TEXT DEFAULT '',
        total REAL DEFAULT 0,
        items TEXT DEFAULT '[]',
        created TEXT DEFAULT (datetime('now')))"""
    if USE_TURSO:
        turso_run(flowers_sql)
        turso_run(flower_inv_sql)
        try: turso_run("ALTER TABLE flowers ADD COLUMN unit TEXT DEFAULT 'وردة'")
        except: pass
        try: turso_run("ALTER TABLE flower_invoices ADD COLUMN invoice_number TEXT DEFAULT NULL")
        except: pass
        try: turso_run("ALTER TABLE flower_invoices ADD COLUMN is_paid INTEGER DEFAULT 0")
        except: pass
    else:
        for _sql in (flowers_sql, flower_inv_sql):
            try:
                conn4=sqlite3.connect(DB_PATH); conn4.execute(_sql); conn4.commit(); conn4.close()
            except: pass
        try:
            conn4=sqlite3.connect(DB_PATH); conn4.execute("ALTER TABLE flower_invoices ADD COLUMN invoice_number TEXT DEFAULT NULL"); conn4.commit(); conn4.close()
        except: pass
        try:
            conn4=sqlite3.connect(DB_PATH); conn4.execute("ALTER TABLE flower_invoices ADD COLUMN is_paid INTEGER DEFAULT 0"); conn4.commit(); conn4.close()
        except: pass
        try:
            conn4=sqlite3.connect(DB_PATH); conn4.execute("ALTER TABLE flowers ADD COLUMN unit TEXT DEFAULT 'وردة'"); conn4.commit(); conn4.close()
        except: pass
    # Customers, Catalog, Debts tables
    new_tables = [
        """CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            notes TEXT,
            last_purchase TEXT,
            total_spent REAL DEFAULT 0,
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS catalog_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            img TEXT,
            available INTEGER DEFAULT 1,
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            due_date TEXT,
            paid INTEGER DEFAULT 0,
            paid_date TEXT,
            notified INTEGER DEFAULT 0,
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT,
            description TEXT NOT NULL,
            price REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            img_file_id TEXT,
            img_url TEXT,
            notes TEXT,
            date TEXT NOT NULL,
            done_date TEXT,
            source TEXT DEFAULT 'web',
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS cash_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            ref_id INTEGER,
            date TEXT NOT NULL,
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS catalog_slides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img_url TEXT NOT NULL,
            title TEXT DEFAULT '',
            subtitle TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            created TEXT DEFAULT (datetime('now')))""",
    ]
    for sql in new_tables:
        if USE_TURSO: turso_run(sql)
        else:
            try:
                conn5=sqlite3.connect(DB_PATH); conn5.execute(sql); conn5.commit(); conn5.close()
            except: pass

    # Store products table
    store_products_sql = """CREATE TABLE IF NOT EXISTS store_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        price REAL NOT NULL DEFAULT 0,
        category TEXT DEFAULT 'باقات',
        img TEXT DEFAULT '',
        available INTEGER DEFAULT 1,
        sort_order INTEGER DEFAULT 0,
        created TEXT DEFAULT (datetime('now')))"""
    store_migrations = [
        "ALTER TABLE orders ADD COLUMN product_id INTEGER",
        "ALTER TABLE orders ADD COLUMN delivery_type TEXT DEFAULT 'pickup'",
        "ALTER TABLE orders ADD COLUMN address TEXT",
        "ALTER TABLE store_products ADD COLUMN occasion TEXT DEFAULT ''",
    ]
    if USE_TURSO:
        turso_run(store_products_sql)
        for sql in store_migrations:
            try: turso_run(sql)
            except: pass
    else:
        try:
            conn6=sqlite3.connect(DB_PATH); conn6.execute(store_products_sql); conn6.commit(); conn6.close()
        except: pass
        for sql in store_migrations:
            try:
                conn6=sqlite3.connect(DB_PATH); conn6.execute(sql); conn6.commit(); conn6.close()
            except: pass

    # Expenses table
    fixed_sqls = [
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            type TEXT DEFAULT 'monthly',
            last_paid TEXT,
            month TEXT,
            note TEXT,
            created TEXT DEFAULT (datetime('now')))""",
    ]
    for sql in fixed_sqls:
        if USE_TURSO: turso_run(sql)
        else:
            try:
                conn2=sqlite3.connect(DB_PATH); conn2.execute(sql); conn2.commit(); conn2.close()
            except: pass
    # Clean duplicate expenses first, then insert defaults
    if USE_TURSO:
        all_exp = turso_get("SELECT * FROM expenses ORDER BY id")
        seen = {}
        for e in all_exp:
            if e["name"] in seen:
                turso_run("DELETE FROM expenses WHERE id=?", (e["id"],))
            else:
                seen[e["name"]] = e["id"]
    defaults = [
        ("راتب العامل", 220, "monthly"),
        ("إيجار المحل", 100, "monthly"),
        ("تعبئة كهرباء", 0, "variable"),
    ]
    for name, amt, typ in defaults:
        if USE_TURSO:
            existing = turso_get("SELECT id FROM expenses WHERE name=?", (name,))
            if not existing:
                turso_run("INSERT INTO expenses (name,amount,type) VALUES (?,?,?)", (name, amt, typ))
        else:
            try:
                conn3=sqlite3.connect(DB_PATH)
                conn3.execute("INSERT OR IGNORE INTO expenses (name,amount,type) VALUES (?,?,?)", (name, amt, typ))
                conn3.commit(); conn3.close()
            except: pass
    if USE_TURSO:
        for sql in sqls:
            turso_run(sql)
        for sql, params in shelf_rows:
            turso_run(sql, params)
        for sql in migrations:
            turso_run(sql)  # Ignore errors for existing columns
    else:
        conn = sqlite3.connect(DB_PATH)
        for sql in sqls:
            conn.execute(sql)
        for sql, params in shelf_rows:
            try: conn.execute(sql, params)
            except: pass
        for sql in migrations:
            try: conn.execute(sql)
            except: pass
        conn.commit(); conn.close()

# init_db() is called from app.py — do not call here

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
    conn.commit(); conn.close()

# ── Helpers ───────────────────────────────────────────────
