from config import *
from database import *
from helpers import *
from telegram_bot import *
from html_pages import HTML_PAGE, WORKER_PAGE
from html_login import LOGIN_PAGE
from html_store import STORE_PAGE


from functools import wraps
from flask import make_response, redirect, send_from_directory, request as flask_request
import hashlib

def get_token():
    return hashlib.md5((APP_PASSWORD + "_fairuz_token").encode()).hexdigest()

def get_worker_token():
    return hashlib.md5((WORKER_PASSWORD + "_worker_token").encode()).hexdigest()

def check_auth():
    return request.cookies.get("fairuz_auth") == get_token()

def check_worker_auth():
    return request.cookies.get("fairuz_worker") == get_worker_token()

def auth(f):
    @wraps(f)
    def w(*a,**k):
        if not check_auth():
            return redirect('/login')
        return f(*a,**k)
    return w

def worker_auth(f):
    @wraps(f)
    def w(*a,**k):
        if not check_worker_auth() and not check_auth():
            return redirect('/login')
        return f(*a,**k)
    return w

@app.route("/ping")
def ping():
    return "ok", 200

@app.route('/background.jpg')
def background_image():
    return send_from_directory('.', 'background.jpg', mimetype='image/jpeg')

@app.route('/upload-background', methods=['POST'])
@auth
def upload_background():
    """Upload a new background image"""
    try:
        if 'file' not in request.files:
            return jsonify({"ok": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"ok": False, "error": "No file selected"}), 400
        
        # Check if file is an image
        if not file.content_type or not file.content_type.startswith('image/'):
            return jsonify({"ok": False, "error": "File must be an image"}), 400
        
        # Save as background.jpg
        file.save('background.jpg')
        return jsonify({"ok": True, "message": "Background updated successfully"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/login")
def login():
    return Response(LOGIN_PAGE, mimetype="text/html")

@app.route("/auth", methods=["POST"])
def do_auth():
    d = request.json or {}
    if d.get("p") == APP_PASSWORD:
        resp = make_response(jsonify({"ok": True}))
        resp.set_cookie("fairuz_auth", get_token(),
                       max_age=60*60*24*30, httponly=True, samesite="Lax")
        return resp
    return jsonify({"ok": False})

@app.route("/logout")
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie("fairuz_auth")
    return resp

@app.route("/worker-auth", methods=["POST"])
def worker_do_auth():
    d = request.json or {}
    if d.get("p") == WORKER_PASSWORD:
        resp = make_response(jsonify({"ok": True}))
        resp.set_cookie("fairuz_worker", get_worker_token(),
                       max_age=60*60*24*7, httponly=True, samesite="Lax")
        return resp
    return jsonify({"ok": False})

@app.route("/worker-logout")
def worker_logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie("fairuz_worker")
    return resp

@app.route("/worker")
def worker_index():
    if not check_worker_auth() and not check_auth():
        return redirect('/login')
    return Response(WORKER_PAGE, mimetype="text/html")

@app.route("/")
def index():
    return Response(STORE_PAGE, mimetype="text/html")

@app.route("/admin")
@auth
def admin_index(): return Response(HTML_PAGE, mimetype="text/html")

# ── Store API ─────────────────────────────────────────────────

@app.route("/api/store/products")
def store_products_list():
    cat = request.args.get("category", "all")
    occ = request.args.get("occasion", "")
    if occ:
        rows = db_get("SELECT * FROM store_products WHERE available=1 AND occasion=? ORDER BY sort_order,id", (occ,))
    elif cat == "all":
        rows = db_get("SELECT * FROM store_products WHERE available=1 ORDER BY sort_order,id")
    else:
        rows = db_get("SELECT * FROM store_products WHERE available=1 AND category=? ORDER BY sort_order,id", (cat,))
    return jsonify(rows)

@app.route("/api/store/order", methods=["POST"])
def store_place_order():
    d = request.json or {}
    name = (d.get("customer_name") or "").strip()
    phone = (d.get("customer_phone") or "").strip()
    product_name = (d.get("product_name") or "").strip()
    product_id = d.get("product_id")
    delivery_type = d.get("delivery_type", "pickup")
    address = (d.get("address") or "").strip()
    notes = (d.get("notes") or "").strip()
    if not name or not phone:
        return jsonify({"ok": False, "error": "الاسم والهاتف مطلوبان"}), 400
    from datetime import timezone
    oman_offset = timedelta(hours=4)
    now_oman = datetime.now(timezone.utc) + oman_offset
    date_str = now_oman.strftime("%d/%m/%Y")
    # Get product price
    price = 0
    if product_id:
        p = db_one("SELECT price FROM store_products WHERE id=?", (product_id,))
        if p: price = p["price"]
    db_run(
        "INSERT INTO orders (customer_name,customer_phone,description,price,status,notes,date,source,product_id,delivery_type,address) VALUES (?,?,?,?,'pending',?,?,'store',?,?,?)",
        (name, phone, product_name, price, notes, date_str, product_id, delivery_type, address)
    )
    # Telegram notification
    delivery_label = "🚗 توصيل" if delivery_type == "delivery" else "🏪 استلام من المحل"
    addr_line = f"\n📍 العنوان: {address}" if address else ""
    notes_line = f"\n📝 ملاحظات: {notes}" if notes else ""
    msg = (
        f"🌸 <b>طلب جديد من المتجر!</b>\n\n"
        f"👤 {name}\n"
        f"📞 {phone}\n"
        f"🛍️ {product_name}\n"
        f"💰 {price:,.3f} ر.ع\n"
        f"{delivery_label}{addr_line}{notes_line}"
    )
    chat_id = os.environ.get("OWNER_CHAT_ID", "")
    if BOT_TOKEN and chat_id:
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": int(chat_id), "text": msg, "parse_mode": "HTML"}, timeout=10)
        except: pass
    return jsonify({"ok": True})

# ── Admin Store Management ────────────────────────────────────

@app.route("/api/admin/store/products", methods=["GET"])
@auth
def admin_store_products():
    rows = db_get("SELECT * FROM store_products ORDER BY category,sort_order,id")
    return jsonify(rows)

@app.route("/api/admin/store/products", methods=["POST"])
@auth
def admin_store_add_product():
    d = request.json or {}
    name = (d.get("name") or "").strip()
    if not name:
        return jsonify({"ok": False, "error": "الاسم مطلوب"}), 400
    price = float(d.get("price") or 0)
    category = d.get("category", "باقات")
    description = (d.get("description") or "").strip()
    img = (d.get("img") or "").strip()
    db_run(
        "INSERT INTO store_products (name,description,price,category,img) VALUES (?,?,?,?,?)",
        (name, description, price, category, img)
    )
    return jsonify({"ok": True})

@app.route("/api/admin/store/products/<int:pid>", methods=["PUT"])
@auth
def admin_store_edit_product(pid):
    d = request.json or {}
    name = (d.get("name") or "").strip()
    price = float(d.get("price") or 0)
    category = d.get("category", "باقات")
    description = (d.get("description") or "").strip()
    img = (d.get("img") or "").strip()
    available = 1 if d.get("available", True) else 0
    db_run(
        "UPDATE store_products SET name=?,description=?,price=?,category=?,img=?,available=? WHERE id=?",
        (name, description, price, category, img, available, pid)
    )
    return jsonify({"ok": True})

@app.route("/api/admin/store/products/<int:pid>", methods=["DELETE"])
@auth
def admin_store_delete_product(pid):
    db_run("DELETE FROM store_products WHERE id=?", (pid,))
    return jsonify({"ok": True})

@app.route("/api/admin/store/products/<int:pid>/image", methods=["POST"])
@auth
def admin_store_upload_image(pid):
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "لا يوجد ملف"}), 400
    f = request.files["file"]
    import uuid, os
    ext = os.path.splitext(f.filename)[1] or ".jpg"
    fname = f"product_{pid}_{uuid.uuid4().hex[:8]}{ext}"
    os.makedirs("static/products", exist_ok=True)
    f.save(f"static/products/{fname}")
    url = f"/static/products/{fname}"
    db_run("UPDATE store_products SET img=? WHERE id=?", (url, pid))
    return jsonify({"ok": True, "url": url})

@app.route("/api/admin/orders", methods=["GET"])
@auth
def admin_orders_list():
    rows = db_get("SELECT * FROM orders WHERE source='store' ORDER BY id DESC LIMIT 100")
    return jsonify(rows)

@app.route("/api/admin/orders/<int:oid>/status", methods=["POST"])
@auth
def admin_order_status(oid):
    status = (request.json or {}).get("status", "pending")
    db_run("UPDATE orders SET status=? WHERE id=?", (status, oid))
    return jsonify({"ok": True})

@app.route("/debug")
def debug():
    try:
        total = db_one("SELECT COUNT(*) as c FROM entries")
        cnt = int(total["c"]) if total and total.get("c") is not None else 0
    except Exception as e:
        cnt = str(e)
    return jsonify({
        "database": "Turso ✅" if USE_TURSO else "SQLite (local)",
        "total_entries": cnt,
        "turso": USE_TURSO,
        "bot": bool(BOT_TOKEN),
        "groq": bool(GROQ_KEY),
        "groq_key_prefix": GROQ_KEY[:8]+"..." if GROQ_KEY else "NOT SET"
    })

@app.route("/api/dashboard")
@auth
def api_dashboard():
    """كل البيانات في request واحد لـ Turso"""
    month = request.args.get("month", cur_month())
    yr = month.split("-")[0]

    queries = [
        ("SELECT * FROM entries WHERE month=? ORDER BY created DESC",          (month,)),
        ("SELECT * FROM expenses ORDER BY id",                                  ()),
        ("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month,)),
        ("SELECT * FROM entries WHERE month LIKE ? ORDER BY created DESC",      (f"{yr}-%",)),
        ("SELECT * FROM flowers ORDER BY count DESC",                           ()),
    ]

    # محاولة batch — request واحد لـ Turso
    batch = turso_multi(queries) if USE_TURSO else None

    if batch:
        cur_entries, expenses, paid, all_entries, flowers = batch
    else:
        # fallback للـ SQLite أو لو فشل الـ batch
        cur_entries = db_get("SELECT * FROM entries WHERE month=? ORDER BY created DESC", (month,))
        expenses    = db_get("SELECT * FROM expenses ORDER BY id")
        paid        = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month,))
        all_entries = db_get("SELECT * FROM entries WHERE month LIKE ? ORDER BY created DESC", (f"{yr}-%",))
        flowers     = db_get("SELECT * FROM flowers ORDER BY count DESC")

    all_s = [e for e in cur_entries if e["type"] == "s"]
    b = [e for e in cur_entries if e["type"] in ("b","expense")]
    # فصل مبيعات الرفوف عن مبيعات المحل
    s = [e for e in all_s if not e.get("shelf_id")]
    shelf_sales = [e for e in all_s if e.get("shelf_id")]

    months_data = {}
    for mm in [f"{yr}-{str(i).zfill(2)}" for i in range(1,13)]:
        ms = [e for e in all_entries if e["month"] == mm]
        months_data[mm] = {
            "sales": [e for e in ms if e["type"] == "s" and not e.get("shelf_id")],
            "buys":  [e for e in ms if e["type"] in ("b","expense")]
        }

    flowers_total = sum(f["count"] for f in flowers) if flowers else 0

    # ملخص مبيعات الرفوف للصفحة الرئيسية
    shelves_info = db_get("SELECT * FROM shelves ORDER BY id")
    shelves_summary = []
    for sh in shelves_info:
        sh_sales = [e for e in shelf_sales if e.get("shelf_id") == sh["id"]]
        shelves_summary.append({
            "id": sh["id"], "name": sh["name"], "color": sh["color"],
            "total": sum(e["amt"] for e in sh_sales),
            "count": len(sh_sales)
        })

    now = datetime.now()
    today_str     = now.strftime("%d/%m/%Y")
    yesterday_str = (now - timedelta(days=1)).strftime("%d/%m/%Y")
    today_s   = [e for e in s if e.get("date") == today_str]
    yest_s    = [e for e in s if e.get("date") == yesterday_str]

    return jsonify({
        "month":           month,
        "sales":           s,
        "buys":            b,
        "shelf_sales":     shelf_sales,
        "shelves_summary": shelves_summary,
        "expenses":        {"expenses": expenses, "paid": paid},
        "charts":          months_data,
        "flowers":         {"flowers": flowers, "total": flowers_total},
        "today_sales":     round(sum(e["amt"] for e in today_s), 3),
        "today_count":     len(today_s),
        "yesterday_sales": round(sum(e["amt"] for e in yest_s), 3),
    })

def call_ai(prompt, max_tokens=900, temperature=0.85):
    """يجرّب النماذج بالترتيب: Groq → Gemini → OpenRouter → OpenAI"""
    msg = [{"role":"system","content":prompt}, {"role":"user","content":"اكتب التحليل الآن"}]

    # 1. Groq
    if GROQ_KEY:
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile","messages":msg,
                      "max_tokens":max_tokens,"temperature":temperature}, timeout=12)
            txt = res.json()["choices"][0]["message"]["content"].strip()
            if txt: return txt, "Groq"
        except: pass

    # 2. Gemini
    if GEMINI_KEY:
        try:
            gemini_body = {
                "contents":[{"parts":[{"text": prompt + "\n\nاكتب التحليل الآن"}]}],
                "generationConfig":{"maxOutputTokens":max_tokens,"temperature":temperature}
            }
            res = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}",
                headers={"Content-Type":"application/json"},
                json=gemini_body, timeout=15)
            txt = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            if txt: return txt, "Gemini"
        except: pass

    # 3. OpenRouter
    if OPENROUTER_KEY:
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type":"application/json"},
                json={"model":"meta-llama/llama-3.3-70b-instruct","messages":msg,
                      "max_tokens":max_tokens,"temperature":temperature}, timeout=15)
            txt = res.json()["choices"][0]["message"]["content"].strip()
            if txt: return txt, "OpenRouter"
        except: pass

    # 4. OpenAI
    if OPENAI_KEY:
        try:
            res = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type":"application/json"},
                json={"model":"gpt-4o-mini","messages":msg,
                      "max_tokens":max_tokens,"temperature":temperature}, timeout=15)
            txt = res.json()["choices"][0]["message"]["content"].strip()
            if txt: return txt, "OpenAI"
        except: pass

    return None, None


@app.route("/api/ai-status")
def api_ai_status():
    """حالة المفاتيح — بدون auth لأنها معلومات غير حساسة"""
    results = {
        "groq":       "ok" if GROQ_KEY else "no_key",
        "gemini":     "ok" if GEMINI_KEY else "no_key",
        "openrouter": "ok" if OPENROUTER_KEY else "no_key",
        "openai":     "ok" if OPENAI_KEY else "no_key",
    }
    results["any_ok"] = any(v == "ok" for v in results.values())
    r = jsonify(results)
    r.headers["Cache-Control"] = "no-cache"
    return r


@app.route("/api/insights")
@auth
def api_insights():
    today = datetime.now().strftime("%Y-%m-%d")
    cached      = db_one("SELECT value FROM app_settings WHERE key='insights_text'")
    cached_date = db_one("SELECT value FROM app_settings WHERE key='insights_date'")
    # نستخدم الكاش فقط إذا: نفس اليوم + يحتوي || + تم توليده بـ AI حقيقي (ليس fallback قصير)
    cached_val = cached.get("value","") if cached else ""
    force_refresh = request.args.get("refresh") == "1"
    has_ai_key = bool(GROQ_KEY or GEMINI_KEY or OPENROUTER_KEY or OPENAI_KEY)
    cache_valid = (cached_date and cached_date.get("value") == today
                   and "||" in cached_val and len(cached_val) > 400
                   and not force_refresh)
    if cache_valid:
        return jsonify({"text": cached_val, "fresh": False})

    now = datetime.now()
    today_str     = now.strftime("%d/%m/%Y")
    yesterday_str = (now - timedelta(days=1)).strftime("%d/%m/%Y")

    today_s, today_b, today_e = get_day_data(today_str)
    yest_s,  yest_b,  yest_e  = get_day_data(yesterday_str)

    store_today = [r for r in today_s if not r.get("shelf_id")]
    store_yest  = [r for r in yest_s  if not r.get("shelf_id")]

    ts_today  = sum(r["amt"] for r in store_today)
    ts_yest   = sum(r["amt"] for r in store_yest)
    tb_today  = sum(r["amt"] for r in today_b)
    te_today  = sum(r["amt"] for r in today_e)
    net_today = ts_today - tb_today - te_today

    today_items = "، ".join(r["desc"] for r in store_today) if store_today else "لا توجد مبيعات بعد"
    yest_items  = "، ".join(r["desc"] for r in store_yest)  if store_yest  else "لم تكن هناك مبيعات"

    diff_pct = "يوم جديد بلا مقارنة"
    if ts_yest > 0:
        pct = ((ts_today - ts_yest) / ts_yest) * 100
        diff_pct = f"ارتفعت بنسبة {abs(pct):.0f}٪ عن أمس 📈" if pct >= 0 else f"انخفضت بنسبة {abs(pct):.0f}٪ عن أمس 📉"

    # احسب الشهرين القادمين
    next1 = now + timedelta(days=30)
    next2 = now + timedelta(days=60)
    month_names_ar = {1:"يناير",2:"فبراير",3:"مارس",4:"أبريل",5:"مايو",6:"يونيو",
                      7:"يوليو",8:"أغسطس",9:"سبتمبر",10:"أكتوبر",11:"نوفمبر",12:"ديسمبر"}
    cur_month_name   = month_names_ar[now.month]
    next1_month_name = month_names_ar[next1.month]
    next2_month_name = month_names_ar[next2.month]

    # حساب التاريخ الهجري التقريبي
    def gregorian_to_hijri_approx(g_date):
        # خوارزمية تقريبية دقيقة بما يكفي للـ prompt
        jd = (367 * g_date.year - (7 * (g_date.year + (g_date.month + 9) // 12)) // 4
              + (275 * g_date.month) // 9 + g_date.day + 1721013)
        l = jd - 1948440 + 10632
        n = (l - 1) // 10631
        l = l - 10631 * n + 354
        j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
        l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
        h_month = (24 * l) // 709
        h_day   = l - (709 * h_month) // 24
        h_year  = 30 * n + j - 30
        hijri_months = ["محرم","صفر","ربيع الأول","ربيع الثاني","جمادى الأولى","جمادى الآخرة",
                        "رجب","شعبان","رمضان","شوال","ذو القعدة","ذو الحجة"]
        return f"{h_day} {hijri_months[h_month-1]} {h_year} هـ"

    hijri_today = gregorian_to_hijri_approx(now)
    hijri_next1 = gregorian_to_hijri_approx(next1)
    hijri_next2 = gregorian_to_hijri_approx(next2)

    # fallback دائماً يستخدم الفاصل ||
    fallback = (
        f"اليوم حققنا مبيعات بقيمة {fmt_omr(ts_today)} من {len(store_today)} عملية 🌸، "
        f"وأمس كانت المبيعات {fmt_omr(ts_yest)}، و{diff_pct}، "
        f"استمر في التركيز على الجودة والتواصل مع عملائك الدائمين."
        f"||"
        f"بناءً على مبيعات اليوم التي شملت {today_items}، "
        f"أنصحك بالتركيز على المنتجات الأكثر طلباً وتحضير عروض مبكرة للمناسبات القادمة 💡، "
        f"والتواصل مع عملائك عبر واتساب لتذكيرهم بالطلبات."
        f"||"
        f"نحن الآن في شهر مايو 2026 🗓️، وهذا الوقت مناسب جداً لتحضير عروض خاصة، "
        f"راجع التقويم الرسمي لسلطنة عُمان للمناسبات القادمة واستغلها مبكراً."
    )

    system_p = f"""أنت مستشار تجاري شخصي ومتخصص في سوق الزهور والهدايا في سلطنة عُمان.
تاريخ اليوم الميلادي: {today_str} ({cur_month_name} {now.year})
التاريخ الهجري التقريبي: {hijri_today}
الشهران القادمان: {next1_month_name} {next1.year} (≈ {hijri_next1}) و{next2_month_name} {next2.year} (≈ {hijri_next2})

═══ بيانات المحل ═══
اليوم ({today_str}):
• مبيعات المحل: {fmt_omr(ts_today)} ({len(store_today)} عملية) — المنتجات: {today_items}
• المشتريات: {fmt_omr(tb_today)} | المصاريف: {fmt_omr(te_today)} | الصافي: {fmt_omr(net_today)}

أمس ({yesterday_str}):
• مبيعات: {fmt_omr(ts_yest)} ({len(store_yest)} عملية) — المنتجات: {yest_items}
• المقارنة: {diff_pct}

═══ تعليمات الإخراج ═══
اكتب ثلاثة أقسام مفصولة بـ || فقط، بدون أي نص خارج الأقسام:

القسم الأول — تحليل اليوم:
تكلم كصديق مقرب يحلل الأداء بصدق ودفء، اذكر الأرقام الحقيقية، قارن باليوم السابق، أخبره بصراحة إذا كان اليوم جيداً أم يحتاج تحسين.

القسم الثاني — نصائح عملية:
بناءً على ما بيع فعلاً اليوم وأمس، أعطِ نصائح مخصصة وذكية لزيادة المبيعات غداً والأيام القادمة، فكّر معه في عروض وأفكار تجارية محددة.

القسم الثالث — المناسبات القادمة (الشهرين القادمين: {next1_month_name} و{next2_month_name}):
ابحث في معرفتك الكاملة عن كل المناسبات في الفترة القادمة، شاملاً:

🇴🇲 المناسبات العُمانية الرسمية والشعبية:
- الأعياد الوطنية: عيد النهضة 23 يوليو، اليوم الوطني 18 نوفمبر
- الأعياد الإسلامية من التقويم الهجري — استخدم التاريخ الهجري أعلاه لتحديد أي منها يقع في الشهرين القادمين:
  • رأس السنة الهجرية (1 محرم)
  • المولد النبوي الشريف (12 ربيع الأول)
  • ليلة الإسراء والمعراج (27 رجب)
  • النصف من شعبان
  • شهر رمضان المبارك وليلة القدر
  • عيد الفطر المبارك (1 شوال)
  • موسم الحج (8-13 ذو الحجة) وما يسبقه
  • عيد الأضحى المبارك (10 ذو الحجة) وأيام التشريق
  • عودة الحجاج والفرح بقدومهم بعد العيد
- المناسبات الاجتماعية: موسم الأعراس (ربيع وصيف)، التخرجات (مايو-يونيو)، بداية العام الدراسي (سبتمبر)

🌍 المناسبات العالمية:
- عيد الأم (الأحد الثاني من مايو عالمياً، 21 مارس عربياً)
- عيد الأب (الأحد الثالث من يونيو)
- عيد الحب (14 فبراير)
- رأس السنة الميلادية (1 يناير)
- اليوم العالمي للمرأة (8 مارس)
- عيد الميلاد (25 ديسمبر)
- الجمعة السوداء وموسم التخفيضات

لكل مناسبة تذكر: متى تقريباً، وكيف يستعد لها المحل مبكراً من حيث المخزون والعروض والتواصل مع العملاء، واقترح أفكاراً محددة للزهور والهدايا المناسبة.

═══ أسلوب الكتابة ═══
• جمل طويلة طبيعية كالحديث بين أصدقاء
• لا قوائم ولا أرقام مرقمة ولا عناوين داخل الأقسام
• emoji داخل النص بشكل طبيعي وليس في البداية فقط
• لا تبدأ بـ "بالطبع" أو "إليك" أو أي مقدمة رسمية
• كن محدداً وعملياً وليس عاماً"""

    ai_text, model_used = call_ai(system_p, max_tokens=1400)
    insights_text = ai_text if ai_text else fallback

    db_run("INSERT OR REPLACE INTO app_settings (key,value) VALUES (?,?)", ("insights_text", insights_text))
    db_run("INSERT OR REPLACE INTO app_settings (key,value) VALUES (?,?)", ("insights_date", today))
    return jsonify({"text": insights_text, "fresh": True, "model": model_used or "fallback"})

@app.route("/api/entries")
@worker_auth
def api_get():
    month=request.args.get("month",cur_month())
    s,b=get_month_data(month)
    return jsonify({"sales":s,"buys":b})

def auto_cash_log(entry_type, amt, desc, pay_method, date_val, ref_id=None):
    """تسجيل تلقائي في الخزينة عند بيع أو شراء كاش"""
    pay = (pay_method or "").lower()
    is_cash = any(w in pay for w in ["كاش","نقد","cash","💵"])
    if not is_cash: return
    if entry_type == "s":
        db_run("INSERT INTO cash_log (type,amount,description,date,ref_id) VALUES (?,?,?,?,?)",
               ("in", amt, f"بيعة: {desc}", date_val, ref_id))
    elif entry_type in ("b","expense"):
        db_run("INSERT INTO cash_log (type,amount,description,date,ref_id) VALUES (?,?,?,?,?)",
               ("out", amt, f"مصروف: {desc}", date_val, ref_id))

@app.route("/api/entries",methods=["POST"])
def api_add():
    d=request.json
    month=d.get("month",cur_month())
    date_val = d.get("date",datetime.now().strftime("%d/%m/%Y"))
    db_run("INSERT INTO entries (type,desc,amt,date,month,img,paid_by,payment_method,sale_time,category) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (d["type"],d["desc"],float(d["amt"]),
         date_val, month,d.get("img"),d.get("paid_by"),d.get("payment_method"),d.get("sale_time"),d.get("category")))
    # تسجيل تلقائي في الخزينة
    try:
        row = db_one("SELECT id FROM entries ORDER BY id DESC LIMIT 1")
        auto_cash_log(d["type"], float(d["amt"]), d["desc"], d.get("payment_method",""), date_val, row["id"] if row else None)
    except: pass
    return jsonify({"ok":True})

@app.route("/api/entries/<int:eid>",methods=["DELETE"])
@worker_auth
def api_del(eid):
    db_run("DELETE FROM entries WHERE id=?",(eid,))
    return jsonify({"ok":True})

@app.route("/api/entries/<int:eid>", methods=["PATCH"])
@worker_auth
def api_edit_entry(eid):
    d = request.json or {}
    fields, vals = [], []
    if "amt"  in d: fields.append("amt=?");  vals.append(float(d["amt"]))
    if "desc" in d: fields.append("desc=?"); vals.append(d["desc"])
    if not fields: return jsonify({"ok":False,"error":"nothing to update"})
    vals.append(eid)
    db_run(f"UPDATE entries SET {','.join(fields)} WHERE id=?", vals)
    return jsonify({"ok":True})

@app.route("/api/shelves")
def api_shelves():
    month=request.args.get("month",cur_month())
    shelves=db_get("SELECT * FROM shelves ORDER BY id")
    result=[]
    for s in shelves:
        prods=db_get("SELECT * FROM shelf_products WHERE shelf_id=? ORDER BY created DESC",(s["id"],))
        row=db_one("SELECT COALESCE(SUM(amt),0) as total,COUNT(*) as cnt FROM entries WHERE type='s' AND shelf_id=? AND month=?",(s["id"],month))
        sales_entries=db_get("SELECT id,desc,amt,date,payment_method FROM entries WHERE type='s' AND shelf_id=? AND month=? ORDER BY created DESC",(s["id"],month))
        ms=float(row["total"]) if row else 0
        rent=float(s.get("rent") or 0)
        result.append({**s,"products":prods,"monthly_sales":ms,"sales_count":int(row["cnt"]) if row else 0,"rent":rent,"net":ms-rent,"sales_entries":sales_entries})
    return jsonify(result)

@app.route("/api/shelves/<int:sid>/products",methods=["POST"])
def api_add_prod(sid):
    d=request.json
    db_run("INSERT INTO shelf_products (shelf_id,name,price,qty) VALUES (?,?,?,?)",
        (sid,d["name"],float(d["price"]),int(d.get("qty",0))))
    return jsonify({"ok":True})

@app.route("/api/shelf_products/<int:pid>",methods=["DELETE"])
def api_del_prod(pid):
    db_run("DELETE FROM shelf_products WHERE id=?",(pid,)); return jsonify({"ok":True})

@app.route("/api/shelf_products/<int:pid>/sell",methods=["POST"])
def api_sell(pid):
    d=request.json; qty=int(d.get("qty",1)); pay=d.get("payment_method")
    prod=db_one("SELECT * FROM shelf_products WHERE id=?",(pid,))
    if not prod: return jsonify({"ok":False}),404
    new_qty=max(0,prod["qty"]-qty)
    db_run("UPDATE shelf_products SET qty=? WHERE id=?",(new_qty,pid))
    month=cur_month(); date=datetime.now().strftime("%d/%m/%Y")
    shelf=db_one("SELECT name FROM shelves WHERE id=?",(prod["shelf_id"],))
    sname=shelf["name"] if shelf else ""
    db_run("INSERT INTO entries (type,desc,amt,date,month,shelf_id,payment_method) VALUES (?,?,?,?,?,?,?)",
        ("s",f'{prod["name"]} — رف {sname}',prod["price"]*qty,date,month,prod["shelf_id"],pay))
    return jsonify({"ok":True,"new_qty":new_qty,"total":prod["price"]*qty})

@app.route("/api/shelves/<int:sid>/rent",methods=["POST"])
def api_rent(sid):
    db_run("UPDATE shelves SET rent=? WHERE id=?",(float(request.json["rent"]),sid))
    return jsonify({"ok":True})

# ── Telegram Webhook ──────────────────────────────────────
pending={}

@app.route("/webhook",methods=["POST"])
def webhook():
    data=request.json or {}
    
    cb=data.get("callback_query")
    if cb:
        cid=cb["id"]; chat=cb["message"]["chat"]["id"]; cbd=cb["data"]
        month=cur_month(); date=datetime.now().strftime("%d/%m/%Y")
        try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={"callback_query_id":cid},timeout=5)
        except: pass
        try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",json={"chat_id":chat,"message_id":cb["message"]["message_id"],"reply_markup":{"inline_keyboard":[]}},timeout=5)
        except: pass
        
        if cbd == "cancel_del":
            tg(chat, "✅ تم الإلغاء، المبيعة محفوظة")
            return "ok"

        elif cbd.startswith("del_entry:"):
            eid = int(cbd.split(":",1)[1])
            entry = db_one("SELECT * FROM entries WHERE id=?", (eid,))
            if entry:
                db_run("DELETE FROM entries WHERE id=?", (eid,))
                # أعد الكمية للمنتج إذا كانت مبيعة رف
                if entry.get("shelf_id"):
                    prod = db_one("SELECT id FROM shelf_products WHERE shelf_id=? AND name=?",
                                  (entry["shelf_id"], entry.get("desc","")))
                    if prod:
                        db_run("UPDATE shelf_products SET qty=qty+1 WHERE id=?", (prod["id"],))
                tg(chat, f"🗑️ تم حذف المبيعة: {entry.get('desc','')} — {fmt_omr(entry.get('amt',0))}")
            else:
                tg(chat, "⚠️ لم يُعثر على المبيعة، ربما حُذفت مسبقاً")
            return "ok"

        elif cbd.startswith("pay:"):
            pay=cbd.split("pay:",1)[1]
            last=db_one("SELECT id FROM entries WHERE type='s' AND month=? ORDER BY created DESC LIMIT 1",(month,))
            if last: db_run("UPDATE entries SET payment_method=? WHERE id=?",(pay,last["id"]))
            if chat in pending and pending[chat].get("waiting")=="sale_payment": del pending[chat]
            tg(chat,f"✅ طريقة الدفع: {pay}")
            
        elif cbd.startswith("payer:"):
            val=cbd.split("payer:",1)[1]
            if val=="skip": paid_by=None; tg(chat,"⏭ تم التخطي")
            elif val=="other":
                if chat not in pending: pending[chat]={}
                pending[chat]["waiting_name"]=True
                tg(chat,"✏️ اكتب اسم الشخص:"); return "ok"
            else: paid_by=val; tg(chat,f"✅ دفع: {paid_by}")
            
            state=pending.get(chat,{})
            if state.get("waiting") in ("paid_by","paid_by_photo"):
                if state.get("waiting")=="paid_by":
                    db_run("INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",
                        ("b",state.get("desc","مشتريات"),state.get("amt",0),state.get("date",date),state.get("month",month),paid_by))
                    if chat in pending: del pending[chat]
                    tg(chat,f"✅ تم التسجيل!\n📦 {state.get('desc')}\n💰 {fmt_omr(state.get('amt',0))}" + (f"\n👤 {paid_by}" if paid_by else ""))
                else:
                    last=db_one("SELECT id FROM entries WHERE month=? ORDER BY created DESC LIMIT 1",(month,))
                    if last: db_run("UPDATE entries SET paid_by=? WHERE id=?",(paid_by,last["id"]))
                    if chat in pending: del pending[chat]
        return "ok"

    msg=data.get("message") or data.get("edited_message")
    if not msg: return "ok"
    chat=msg["chat"]["id"]; month=cur_month(); date=datetime.now().strftime("%d/%m/%Y")

    if "photo" in msg:
        file_id=msg["photo"][-1]["file_id"]; caption=msg.get("caption","").strip()

        # ── إضافة منتج للمتجر: "باقات | 8.500 | زواج" ──
        STORE_CATS = ["باقات","استاندات","مجسمات","شرايط"]
        STORE_OCCASIONS = ["زواج","عيد ميلاد","تخرج","هدية","افتتاح","تخص"]
        detected_cat = next((c for c in STORE_CATS if c in caption), None)
        detected_occ = next((o for o in STORE_OCCASIONS if o in caption), None)
        price_match = re.search(r'(\d+(?:[.,]\d+)?)', caption)
        if detected_cat and price_match:
            tg(chat, "🌸 جاري إضافة المنتج للمتجر...")
            try:
                prod_price = float(price_match.group(1).replace(',', '.'))
                # تحميل الصورة وحفظها
                r_file = requests.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
                    params={"file_id": file_id}, timeout=10).json()
                fp = r_file.get("result",{}).get("file_path","")
                img_bytes = requests.get(
                    f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}", timeout=15).content
                import uuid, os as _os
                _os.makedirs("static/products", exist_ok=True)
                fname = f"product_{uuid.uuid4().hex[:10]}.jpg"
                img_path = f"static/products/{fname}"
                with open(img_path, "wb") as f:
                    f.write(img_bytes)
                img_url = f"/static/products/{fname}"
                # توليد اسم ووصف بالذكاء الاصطناعي
                prod_name = detected_cat  # اسم افتراضي
                prod_desc = ""
                if GROQ_KEY or OPENROUTER_KEY or GEMINI_KEY:
                    import base64
                    b64 = base64.b64encode(img_bytes).decode()
                    ai_prompt = [
                        {"role":"user","content":[
                            {"type":"text","text":f"""أنت كاتب إعلاني محترف لمحل ورد راقٍ اسمه "فيروز فلورز".
انظر لهذه الصورة وأعطني JSON فقط بهذا الشكل:
{{
  "name": "اسم المنتج بالعربي (مثال: باقة ورد حمراء ملكية)",
  "description": "نص تسويقي جميل ومفصّل من 3-4 جمل يصف المنتج بأسلوب راقٍ ويبرز جماله وتميّزه ومناسباته"
}}
الفئة: {detected_cat}
اجعل الوصف شاعرياً وجذاباً يشجّع العميل على الشراء.
لا تكتب أي شيء خارج JSON."""},
                            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
                        ]}
                    ]
                    try:
                        if GROQ_KEY:
                            r_ai = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                headers={"Authorization":f"Bearer {GROQ_KEY}"},
                                json={"model":"meta-llama/llama-4-scout-17b-16e-instruct","messages":ai_prompt,"max_tokens":400,"temperature":0.7},
                                timeout=20).json()
                            ai_text = r_ai["choices"][0]["message"]["content"].strip()
                        elif OPENROUTER_KEY:
                            r_ai = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                headers={"Authorization":f"Bearer {OPENROUTER_KEY}"},
                                json={"model":"google/gemini-2.0-flash-001","messages":ai_prompt,"max_tokens":400},
                                timeout=20).json()
                            ai_text = r_ai["choices"][0]["message"]["content"].strip()
                        elif GEMINI_KEY:
                            r_ai = requests.post(
                                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}",
                                json={"contents":[{"parts":[
                                    {"text":f"أنت مساعد لمحل ورد. انظر لهذه الصورة وأعطني JSON فقط:\n{{\"name\":\"اسم المنتج بالعربي\",\"description\":\"وصف قصير جذاب 10-15 كلمة\"}}\nالفئة: {detected_cat}"},
                                    {"inline_data":{"mime_type":"image/jpeg","data":b64}}
                                ]}]},
                                timeout=20).json()
                            ai_text = r_ai["candidates"][0]["content"]["parts"][0]["text"].strip()
                        # استخراج JSON
                        import json as _json
                        json_m = re.search(r'\{[^}]+\}', ai_text, re.DOTALL)
                        if json_m:
                            parsed = _json.loads(json_m.group())
                            prod_name = parsed.get("name", detected_cat) or detected_cat
                            prod_desc = parsed.get("description", "") or ""
                    except Exception as e:
                        prod_name = detected_cat
                # حفظ المنتج في قاعدة البيانات
                db_run(
                    "INSERT INTO store_products (name,description,price,category,occasion,img) VALUES (?,?,?,?,?,?)",
                    (prod_name, prod_desc, prod_price, detected_cat, detected_occ or "", img_url)
                )
                occ_line = f"🎀 المناسبة: {detected_occ}\n" if detected_occ else ""
                tg(chat,
                    f"✅ <b>تم إضافة المنتج للمتجر!</b>\n\n"
                    f"🌸 <b>{prod_name}</b>\n"
                    f"📂 الفئة: {detected_cat}\n"
                    f"{occ_line}"
                    f"💰 السعر: {prod_price:,.3f} ر.ع\n\n"
                    f"📝 <b>الوصف:</b>\n{prod_desc}\n\n"
                    f"——\n"
                    f"يظهر الآن في المتجر تلقائياً 🛍️\n"
                    f"لتعديله: افتح لوحة الإدارة ← تبويبة المتجر")
            except Exception as e:
                tg(chat, f"⚠️ حدث خطأ أثناء الإضافة: {str(e)[:100]}")
            return "ok"

        # ── طلب عميل جديد ──
        caption_is_order = any(w in caption for w in ["طلب","order","طلبية","اوردر","زبون","عميل"])
        if caption_is_order:
            # استخرج اسم العميل والوصف من الكابشن بالذكاء الاصطناعي
            tg(chat, "📋 جاري حفظ الطلب...")
            order_desc = caption
            cust_name = "غير محدد"
            cust_phone = ""
            # حاول استخراج الاسم والرقم من الكابشن
            if GROQ_KEY or GEMINI_KEY or OPENROUTER_KEY or OPENAI_KEY:
                parse_prompt = f"""من النص التالي استخرج بالعربي:
النص: "{caption}"
أعطني JSON فقط بهذا الشكل:
{{"name":"اسم العميل أو غير محدد","phone":"رقم الهاتف أو فارغ","desc":"وصف الطلب بشكل مختصر"}}
لا تكتب شيء غير JSON."""
                ai_txt, _ = call_ai(parse_prompt, max_tokens=150, temperature=0.1)
                if ai_txt:
                    try:
                        import json as _json
                        parsed_order = _json.loads(ai_txt.strip())
                        cust_name  = parsed_order.get("name","غير محدد") or "غير محدد"
                        cust_phone = parsed_order.get("phone","") or ""
                        order_desc = parsed_order.get("desc", caption) or caption
                    except: pass
            date_val = datetime.now().strftime("%d/%m/%Y")
            db_run("INSERT INTO orders (customer_name,customer_phone,description,date,img_file_id,source) VALUES (?,?,?,?,?,?)",
                   (cust_name, cust_phone, order_desc, date_val, file_id, "bot"))
            order_row = db_one("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            oid = order_row["id"] if order_row else "?"
            tg(chat,
               f"✅ <b>تم حفظ الطلب #{oid}!</b>\n\n"
               f"👤 العميل: {cust_name}\n"
               f"📝 الطلب: {order_desc}\n"
               f"📅 التاريخ: {date_val}\n\n"
               f"لعرض جميع الطلبات: /طلبات\n"
               f"للتعديل على الطلب افتح الموقع → العملاء")
            return "ok"

        # Check if flower counting request
        # ── كابشن تسويقي بالذكاء الاصطناعي ──
        caption_is_caption = any(w in caption.lower() for w in [
            "كابشن","كابشن","caption","وصف","بوست","post","نشر","انستقرام",
            "instagram","واتس اب","whatsapp","اكتب","اكتبي","اكتبلي"])
        if caption_is_caption:
            style = ""
            if any(w in caption for w in ["رومانسي","رومانسية","حب","حبيب"]): style="رومانسي"
            elif any(w in caption for w in ["رسمي","فعالية","تهنئة"]): style="رسمي"
            elif any(w in caption for w in ["مرح","مضحك","فن","هدية"]): style="مرح"
            elif any(w in caption for w in ["عيد","رمضان","مبارك"]): style="عيد"
            tg(chat, "✍️ جاري كتابة الكابشن...")
            from telegram_bot import generate_caption
            result_txt = generate_caption(file_id, style)
            if result_txt:
                tg(chat,
                   f"✨ <b>كابشن جاهز للنشر:</b>\n\n"
                   f"{result_txt}\n\n"
                   f"——\n"
                   f"💡 أرسل الصورة مع كلمة <code>كابشن رومانسي</code> أو <code>كابشن رسمي</code> أو <code>كابشن مرح</code> لتغيير الأسلوب")
            else:
                tg(chat, "⚠️ تعذر توليد الكابشن، تأكد من ضبط مفاتيح AI في الإعدادات.")
            return "ok"

        caption_is_flowers = any(w in caption for w in ["عد الورد","عد ورد","عد زهور","مخزون ورد","count flower"])
        # Check if flower supplier invoice
        caption_is_flower_inv = any(w in caption for w in [
            "فاتورة ورد","فاتورة زهور","فاتورة شركة","مورد ورد","شركة ورد",
            "flower invoice","supplier","فاتورة مورد","فاتوره ورد","فاتوره زهور"])
        # Pre-detect electricity from caption
        caption_is_elec = any(w in caption for w in ["كهرباء","كهربا","تعبئة","تعبئه","⚡","electric","kwh","prepaid"])

        if caption_is_flower_inv:
            tg(chat,"🧾 جاري قراءة فاتورة الورد...")
            inv = groq_read_flower_supplier_invoice(file_id)
            if inv and inv.get("found") and inv.get("items"):
                items     = inv.get("items", [])
                company   = inv.get("company","").strip() or "غير محدد"
                inv_no    = inv.get("invoice_number")  # رقم الفاتورة (قد يكون None)
                std_date  = inv.get("date","").strip()  # صيغة YYYY-MM-DD

                # تحويل التاريخ لحفظه وعرضه
                if std_date:
                    try:
                        # من YYYY-MM-DD إلى DD/MM/YYYY للعرض
                        dt = datetime.strptime(std_date, "%Y-%m-%d")
                        inv_date_display = dt.strftime("%d/%m/%Y")
                        inv_month = dt.strftime("%Y-%m")
                    except:
                        inv_date_display = std_date
                        inv_month = month
                else:
                    inv_date_display = date
                    inv_month = month

                total = float(inv.get("total") or sum(float(i.get("line_total",0)) for i in items))
                items_json = json.dumps(items, ensure_ascii=False)
                db_run(
                    "INSERT INTO flower_invoices (company,inv_date,month,total,items) VALUES (?,?,?,?,?)",
                    (company, inv_date_display, inv_month, total, items_json))

                lines = "\n".join(
                    f"  🌹 {i['name']}: {i['count']} {i.get('unit','وردة')}"
                    + (f" × {i['unit_price']} = {fmt_omr(float(i.get('line_total',0)))}" if float(i.get('unit_price',0))>0 else "")
                    for i in items)

                inv_no_line = f"🔖 رقم الفاتورة: <code>{inv_no}</code>\n" if inv_no else ""
                tg(chat,
                   f"✅ <b>تم حفظ فاتورة الورد!</b>\n\n"
                   f"🏪 الشركة: <b>{company}</b>\n"
                   f"{inv_no_line}"
                   f"📅 التاريخ: {inv_date_display}\n\n"
                   f"<b>الأصناف:</b>\n{lines}\n\n"
                   f"💰 الإجمالي: {fmt_omr(total)}\n\n"
                   f"لعرض الفواتير: /فواتير_الورد")
            else:
                tg(chat, "⚠️ ما قدرت أقرأ فاتورة الورد بوضوح.\nجرّب صورة أوضح أو أضفها يدوياً من الموقع في قسم فواتير الورد.")
            return "ok"  # فاتورة الورد لا تُضاف كمشتريات

        if caption_is_flowers:
            tg(chat,"🌸 جاري عد الورد وتحديد الأنواع...")
            flowers = groq_count_flowers(file_id)
            if flowers and len(flowers) > 0:
                now = datetime.now().strftime("%d/%m/%Y %H:%M")
                db_run("DELETE FROM flowers")
                for f in flowers:
                    name = f.get("name_ar") or f.get("name","ورد")
                    cnt = int(f.get("count",0))
                    unit = f.get("unit","وردة")
                    db_run("INSERT INTO flowers (name,count,unit,updated) VALUES (?,?,?,?)",(name,cnt,unit,now))
                total_stems = sum(int(f.get("count",0)) for f in flowers if f.get("unit","وردة")=="وردة")
                total_bundles = sum(int(f.get("count",0)) for f in flowers if f.get("unit","")=="بندلة")
                lines = "\n".join(
                    f"🌹 {f.get('name_ar') or f.get('name')}: {f.get('count')} {f.get('unit','وردة')}"
                    for f in flowers)
                summary = f"📊 الورود: {total_stems} وردة"
                if total_bundles: summary += f" | {total_bundles} بندلة"
                tg(chat,
                   f"✅ <b>تم عد الورد!</b>\n\n{lines}\n\n"
                   f"{summary}\n"
                   f"🕐 {now}\n\n"
                   f"لعرض المخزون: /ورد")
            else:
                tg(chat,"⚠️ ما قدرت أعد الورد بوضوح. جرّب صورة أوضح.")
            return "ok"

        tg(chat,"⏳ جاري قراءة الفاتورة...")
        result=groq_read_invoice(file_id)
        if result and result.get("found") and result.get("amt"):
            amt=float(result["amt"]); desc=result.get("desc","مشتريات")
            is_elec=result.get("is_electricity",False) or caption_is_elec
            # Auto-detect electricity from description
            if not is_elec:
                is_elec=any(w in (desc+caption).lower() for w in ["كهرب","تعبئ","prepaid","electric","kwh","electricity","power"])
            if is_elec:
                # Use date from receipt if available, else today
                receipt_date = result.get("date","").strip()
                if receipt_date and len(receipt_date) >= 8:
                    entry_date = receipt_date
                    try:
                        entry_month = datetime.strptime(receipt_date, "%d/%m/%Y").strftime("%Y-%m")
                    except:
                        entry_date = date; entry_month = month
                else:
                    entry_date = date; entry_month = month
                # Save as expense (NOT as buy)
                db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                       ("expense","تعبئة كهرباء",amt,entry_date,entry_month,"مصاريف ثابتة"))
                exp=db_one("SELECT id FROM expenses WHERE name=?",("تعبئة كهرباء",))
                if exp: db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",(entry_date,entry_month,amt,exp["id"]))
                tg(chat,
                   f"⚡ <b>تم تسجيل تعبئة كهرباء!</b>\n"
                   f"💰 {fmt_omr(amt)}\n"
                   f"📅 {entry_date}\n"
                   f"✅ أُضيفت في المصاريف الثابتة (ليس المشتريات)")
            else:
                db_run("INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",("b",desc,amt,date,month))
                pending[chat]={"waiting":"paid_by_photo","amt":amt}
                tg_buttons(chat,f"✅ تم قراءة الفاتورة!\n📦 {desc}\n💰 {fmt_omr(amt)}\n\n👤 من دفع؟",
                    [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                     [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
        else:
            if caption_is_elec:
                pending[chat]={"waiting":"elec_amt"}
                tg(chat,"⚡ ما قدرت أقرأ الفاتورة بوضوح\nكم مبلغ تعبئة كهرباء؟\nأرسل الرقم فقط: <code>45.500</code>")
            else:
                pending[chat]={"waiting":"buy_amt","desc":caption or "مشتريات"}
                tg(chat,"🧾 ما قدرت أقرأ الفاتورة بوضوح\nكم المبلغ الإجمالي؟\nأرسل الرقم فقط: <code>3.520</code>")
        return "ok"

    text=msg.get("text","").strip()
    if not text: return "ok"

    # Handle electricity manual amount
    if pending.get(chat,{}).get("waiting") == "elec_amt":
        try:
            amt = float(text.replace(",","."))
            date_now = datetime.now().strftime("%d/%m/%Y")
            db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                   ("expense","تعبئة كهرباء",amt,date_now,month,"مصاريف ثابتة"))
            exp=db_one("SELECT id FROM expenses WHERE name=?",("تعبئة كهرباء",))
            if exp: db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",(date_now,month,amt,exp["id"]))
            del pending[chat]
            tg(chat,f"⚡ <b>تم تسجيل تعبئة كهرباء!</b>\n💰 {fmt_omr(amt)}\n📅 {date_now}")
        except:
            tg(chat,"⚠️ أرسل رقم صحيح مثل: <code>45.500</code>")
        return "ok"

    if pending.get(chat,{}).get("waiting_name"):
        paid_by=text.strip(); state=pending[chat]; del state["waiting_name"]
        if state.get("waiting")=="paid_by":
            db_run("INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",
                ("b",state.get("desc"),state.get("amt"),state.get("date",date),state.get("month",month),paid_by))
            del pending[chat]
            tg(chat,f"✅ تم!\n📦 {state.get('desc')}\n💰 {fmt_omr(state.get('amt',0))}\n👤 {paid_by}")
        else:
            last=db_one("SELECT id FROM entries WHERE month=? ORDER BY created DESC LIMIT 1",(month,))
            if last: db_run("UPDATE entries SET paid_by=? WHERE id=?",(paid_by,last["id"]))
            if chat in pending: del pending[chat]
            tg(chat,f"✅ دفع: {paid_by}")
        return "ok"

    state=pending.get(chat,{})

    if state.get("waiting")=="expense_amt":
        try:
            amt=float(text.replace(",","."))
            exp_name=state.get("exp_name","مصروف")
            exp_id=state.get("exp_id")
            date_now=datetime.now().strftime("%d/%m/%Y")
            db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                   ("expense",exp_name,amt,date_now,month,"مصاريف ثابتة"))
            if exp_id:
                db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",
                       (date_now,month,amt,exp_id))
            del pending[chat]
            tg(chat,f"✅ <b>تم تسجيل {exp_name}</b>\n💰 {fmt_omr(amt)}\n📅 {date_now}")
        except:
            tg(chat,"⚠️ أرسل رقم صحيح مثل: <code>220.000</code>")
        return "ok"

    if state.get("waiting")=="sale_amt":
        try:
            amt=float(text.replace(",","."))
            desc=state.get("desc","مبيعة")
            del pending[chat]
            pending[chat]={"waiting":"sale_payment"}
            db_run("INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",("s",desc,amt,date,month))
            tg_buttons(chat,f"🌸 <b>مبيعة {fmt_omr(amt)}</b>\n📝 {desc}\n\n💳 طريقة الدفع؟",
                [[{"label":"💵 كاش","data":"pay:كاش 💵"},{"label":"💳 فيزا","data":"pay:فيزا 💳"},{"label":"🏦 تحويل","data":"pay:تحويل 🏦"}]])
        except:
            tg(chat,"⚠️ أرسل رقم صحيح مثل: <code>4.500</code>")
        return "ok"

    if state.get("waiting")=="buy_amt":
        try:
            amt=float(text.replace(",","."))
            desc=state.get("desc","مشتريات")
            db_run("INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",("b",desc,amt,date,month))
            pending[chat]={"waiting":"paid_by_photo","amt":amt}
            tg_buttons(chat,f"✅ تم التسجيل!\n📦 {desc}\n💰 {fmt_omr(amt)}\n\n👤 من دفع؟",
                [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                 [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
        except: tg(chat,"⚠️ أرسل رقم: <code>3.520</code>")
        return "ok"
    
    if state.get("waiting")=="sale_payment":
        pay=text.strip()
        if pay in ["1","كاش","نقد"]: pay="كاش 💵"
        elif pay in ["2","فيزا","بطاقة"]: pay="فيزا 💳"
        elif pay in ["3","تحويل"]: pay="تحويل 🏦"
        last=db_one("SELECT id FROM entries WHERE type='s' AND month=? ORDER BY created DESC LIMIT 1",(month,))
        if last: db_run("UPDATE entries SET payment_method=? WHERE id=?",(pay,last["id"]))
        del pending[chat]
        tg(chat,f"✅ طريقة الدفع: {pay}"); return "ok"

    # ── إضافة ورد يدوي: انتظار العدد والوحدة ──
    if state.get("waiting") == "flower_manual_count":
        m = re.match(r'^(\d+)\s*(بندلة|بنادل|حزمة|حزم|وردة|وردات|قطعة)?$', text.strip())
        if m:
            cnt = int(m.group(1))
            raw_unit = m.group(2) or ""
            unit = "بندلة" if raw_unit in ("بندلة","بنادل","حزمة","حزم") else "وردة"
            name = state.get("flower_name", "ورد")
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            existing = db_one("SELECT id FROM flowers WHERE name=?", (name,))
            if existing:
                db_run("UPDATE flowers SET count=?,unit=?,updated=? WHERE id=?", (cnt, unit, now, existing["id"]))
            else:
                db_run("INSERT INTO flowers (name,count,unit,updated) VALUES (?,?,?,?)", (name, cnt, unit, now))
            del pending[chat]
            flowers = db_get("SELECT * FROM flowers ORDER BY count DESC")
            total_s = sum(f["count"] for f in flowers if f.get("unit","وردة")=="وردة")
            total_b = sum(f["count"] for f in flowers if f.get("unit","")=="بندلة")
            summary = f"📊 الإجمالي: {total_s} وردة" + (f" | {total_b} بندلة" if total_b else "")
            tg(chat, f"✅ تم تحديث المخزون!\n🌹 {name}: {cnt} {unit}\n{summary}")
        else:
            tg(chat, "⚠️ أرسل عدد صحيح، مثل:\n<code>25</code> أو <code>5 بندلة</code>")
        return "ok"

    # ── إضافة ورد يدوي: انتظار الاسم ──
    if state.get("waiting") == "flower_manual_name":
        name = text.strip()
        if not name:
            tg(chat, "⚠️ أرسل اسم الورد"); return "ok"
        _bundle_flowers = ["جبسون","جبسوفيلا","gypsophila","ايوروبسم","ليموناي","limonium","baby breath"]
        is_bundle = any(b in name.lower() for b in _bundle_flowers)
        pending[chat] = {"waiting": "flower_manual_count", "flower_name": name}
        hint = "مثال: <code>5 بندلة</code>" if is_bundle else "مثال: <code>25</code> أو <code>10 بندلة</code>"
        tg(chat, f"🌹 كم عدد <b>{name}</b>؟\n{hint}")
        return "ok"

    # ── تعرّف تلقائي على الورد المسمّى والمجموعات ──
    _flower_keywords = ["ورد","وردة","وردات","زهور","زهرة","باقة","بوكيه","روز","جبسون","جبسوفيلا",
                        "دوار","زنبق","ليلوم","ارانوس","ليموناي","ايوروبسم","أوركيد","توليب"]
    _has_flower_kw  = any(kw in text for kw in _flower_keywords)
    _has_number     = bool(re.search(r'\d+', text))
    _is_bulk        = len(re.findall(r'\d+', text)) >= 3

    if _has_flower_kw and _has_number:
        if _is_bulk or "\n" in text or len(text) > 60:
            tg(chat, "🌸 جاري تحليل قائمة الورد...")
            parsed = groq_parse_flower_text(text)
            if parsed and len(parsed) > 0:
                now = datetime.now().strftime("%d/%m/%Y %H:%M")
                db_run("DELETE FROM flowers")
                for f in parsed:
                    nm  = f.get("name","ورد")
                    cnt = int(f.get("count",0))
                    un  = f.get("unit","وردة")
                    db_run("INSERT INTO flowers (name,count,unit,updated) VALUES (?,?,?,?)",(nm,cnt,un,now))
                total_s = sum(int(f.get("count",0)) for f in parsed if f.get("unit","وردة")=="وردة")
                total_b = sum(int(f.get("count",0)) for f in parsed if f.get("unit","")=="بندلة")
                lines = "\n".join(
                    f"{'🌸' if f.get('unit')=='بندلة' else '🌹'} {f['name']}: {f['count']} {f.get('unit','وردة')}"
                    for f in parsed)
                summary = f"📊 الورود: {total_s} وردة" + (f" | {total_b} بندلة" if total_b else "")
                tg(chat, f"✅ <b>تم تحديث مخزون الورد!</b>\n\n{lines}\n\n{summary}\n🕐 {now}")
            else:
                tg(chat, "⚠️ ما قدرت أحلل القائمة. جرّب /ورد_يدوي لإضافة كل نوع على حدة.")
            return "ok"

        _single = re.search(
            r'(?:عندي|معي|لدي|عدد)\s*'
            r'(?:ورد\s*|زهور\s*|وردة\s*)?'
            r'([^\d]{2,30?}?)\s*'
            r'(\d+)\s*'
            r'(بندلة|بنادل|حزمة|وردة|وردات)?',
            text)
        if _single:
            raw_name = _single.group(1).strip().strip('ال').strip()
            cnt = int(_single.group(2))
            raw_unit = _single.group(3) or ""
            unit = "بندلة" if raw_unit in ("بندلة","بنادل","حزمة") else "وردة"
            for stop in ["ورد","وردة","زهور","الي","اللي","معي","عندي","لدي","عدد","من","في","و"]:
                raw_name = raw_name.replace(stop,"").strip()
            name = raw_name if len(raw_name) >= 2 else "ورد"
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            existing = db_one("SELECT id FROM flowers WHERE name=?", (name,))
            if existing:
                db_run("UPDATE flowers SET count=?,unit=?,updated=? WHERE id=?", (cnt,unit,now,existing["id"]))
            else:
                db_run("INSERT INTO flowers (name,count,unit,updated) VALUES (?,?,?,?)", (name,cnt,unit,now))
            flowers = db_get("SELECT * FROM flowers ORDER BY count DESC")
            total_s = sum(f["count"] for f in flowers if f.get("unit","وردة")=="وردة")
            total_b = sum(f["count"] for f in flowers if f.get("unit","")=="بندلة")
            summary = f"📊 الإجمالي: {total_s} وردة" + (f" | {total_b} بندلة" if total_b else "")
            tg(chat, f"✅ تم تحديث المخزون!\n🌹 {name}: {cnt} {unit}\n{summary}")
            return "ok"

    if text in ["/start","/help"]:
        tg(chat,
           "🌹 <b>فيروز فلورز</b>\n\n"
           "🌸 <b>مبيعة:</b>\n"
           "<code>بعت باقة بـ 5.500</code>\n"
           "<code>بعت طباعة 3d بـ 8.000 كاش</code>\n"
           "<code>بعت تاج بـ 3.000 فيزا</code>\n\n"
           "📦 <b>مشتريات:</b>\n"
           "<code>اشتريت زهور بـ 12.000</code>\n\n"
           "💸 <b>مصاريف:</b>\n"
           "<code>دفعت راتب</code>\n"
           "<code>دفعت إيجار</code>\n"
           "<code>دفعت كهرباء 45.000</code>\n\n"
           "🗄️ <b>الرفوف:</b>\n"
           "<code>بعت عطر من رف ريحان</code> — بيع من رف\n"
           "<code>بعت ساعة من رف فتحية بـ 8 كاش</code>\n"
           "<code>/رف ريحان</code> — عرض منتجات الرف\n"
           "<code>/رفوف</code> — ملخص جميع الرفوف\n"
           "<code>/ايجار_الرفوف</code> — تسجيل الإيجارات\n\n"
           "🗑️ <b>حذف مبيعة:</b>\n"
           "<code>/حذف</code> — حذف آخر مبيعة مسجلة\n"
           "أو اضغط زر الحذف أسفل رسالة التأكيد مباشرة\n\n"
           "🌸 <b>مخزون الورد:</b>\n"
           "أرسل صورة + تعليق <code>عد الورد</code>\n"
           "أو: <code>عندي ورد روز احمر 20</code>\n"
           "أو: <code>عندي جبسون 3 بندلة</code>\n"
           "/ورد — عرض المخزون | /ورد_يدوي — إضافة يدوي\n\n"
           "🧾 <b>فواتير شركات الورد:</b>\n"
           "أرسل صورة الفاتورة + تعليق <code>فاتورة ورد</code>\n"
           "/فواتير_الورد — فواتير الشهر الحالي\n\n"
           "📅 /اليوم — تقرير اليوم\n"
           "📅 /يوم 01/05/2026 — تقرير يوم معين\n"
           "📊 /شهر — تقرير الشهر الكامل مع تفصيل يومي\n"
           "📊 /report — تقرير الشهر\n"
           "📈 /فئات — مبيعات حسب الفئة\n"
           "👤 /من_دفع — تفصيل المشتريات\n"
           "💼 /مصاريف — المصاريف الثابتة\n\n"
           "👥 /عملائي — عرض العملاء الدائمين\n"
           "💳 /ديوني — الديون غير المسددة\n\n"
           "📋 <b>الطلبات:</b>\n"
           "أرسل صورة + تعليق <code>طلب اسم العميل - وصف الطلب</code>\n"
           "مثال: <code>طلب أم خالد - باقة ورد أحمر كبيرة</code>\n"
           "/طلبات — عرض الطلبات قيد الانتظار")
        return "ok"

    # ── تقرير اليوم ──
    if text in ["/اليوم", "/today", "/يوم"]:
        today_str = datetime.now().strftime("%d/%m/%Y")
        tg(chat, format_day_report(today_str))
        return "ok"

    # ── تقرير يوم معين مثل /يوم 01/05/2026 ──
    if text.startswith("/يوم "):
        day_str = text.replace("/يوم ","").strip()
        try:
            datetime.strptime(day_str, "%d/%m/%Y")
            tg(chat, format_day_report(day_str))
        except:
            tg(chat, "⚠️ صيغة التاريخ غلط، مثال: <code>/يوم 01/05/2026</code>")
        return "ok"

    # ── تقرير الشهر ──
    if text in ["/شهر", "/monthly", "/month_report"]:
        tg(chat, format_month_report(month))
        return "ok"

    if text=="/report":
        ts,tb,tp,sc,bc=month_summary(month)
        e="✅" if tp>=0 else "⚠️"
        _,buys=get_month_data(month)
        pd={}
        for en in buys:
            p=en.get("paid_by") or "غير محدد"
            pd[p]=pd.get(p,0)+en["amt"]
        pl="\n".join(f"  👤 {k}: {fmt_omr(v)}" for k,v in pd.items()) or "  غير محدد"
        # Expenses summary
        exps = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month,))
        exp_total = sum(e2["amt"] for e2 in exps)
        exp_lines = "\n".join(f"  💸 {e2['desc']}: {fmt_omr(e2['amt'])}" for e2 in exps) or "  لا يوجد"
        net_after_exp = tp - exp_total
        emoji2 = "✅" if net_after_exp >= 0 else "⚠️"
        tg(chat,
           f"📊 <b>تقرير {month}</b>\n\n"
           f"🌸 المبيعات: {fmt_omr(ts)} ({sc})\n"
           f"📦 المشتريات: {fmt_omr(tb)} ({bc})\n"
           f"💸 المصاريف: {fmt_omr(exp_total)}\n"
           f"━━━━━━\n"
           f"{e} الربح قبل المصاريف: {fmt_omr(tp)}\n"
           f"{emoji2} الربح الصافي: {fmt_omr(net_after_exp)}\n\n"
           f"💳 من دفع:\n{pl}\n\n"
           f"💼 المصاريف المدفوعة:\n{exp_lines}")
        return "ok"

    if text in ["/ورد_يدوي", "/add_flower"]:
        pending[chat] = {"waiting": "flower_manual_name"}
        tg(chat, "🌹 <b>إضافة ورد يدوياً</b>\n\nاكتب اسم نوع الورد:\nمثال: <code>ورد أحمر</code> أو <code>زنبق</code>")
        return "ok"

    if text in ["/فواتير_الورد", "/flower_invoices"]:
        cur = cur_month()
        invs = db_get("SELECT * FROM flower_invoices WHERE month=? ORDER BY inv_date DESC", (cur,))
        if not invs:
            tg(chat,
               f"🧾 <b>فواتير الورد — {cur}</b>\n\n"
               "لا توجد فواتير هذا الشهر.\n\n"
               "أرسل صورة الفاتورة مع تعليق:\n<code>فاتورة ورد</code>")
        else:
            total_month = sum(float(i["total"]) for i in invs)
            lines = []
            for i in invs:
                lines.append(
                    f"📄 <b>{i['company']}</b> — {i['inv_date']}\n"
                    f"   💰 {fmt_omr(float(i['total']))}"
                )
            tg(chat,
               f"🧾 <b>فواتير الورد — {cur}</b>\n\n"
               + "\n\n".join(lines)
               + f"\n\n{'━'*18}\n💰 الإجمالي: {fmt_omr(total_month)}")
        return "ok"

    if text in ["/ورد", "/flowers", "/عد_الورد"]:
        flowers = db_get("SELECT * FROM flowers ORDER BY count DESC")
        if not flowers:
            tg(chat,
               "🌸 لا يوجد مخزون ورد مسجل بعد\n\n"
               "<b>طرق التسجيل:</b>\n"
               "📸 صورة + تعليق <code>عد الورد</code>\n"
               "✏️ <code>عندي ورد روز أحمر 20</code>\n"
               "✏️ <code>عندي جبسون 3 بندلة</code>\n"
               "📋 أرسل قائمة كاملة وسيحللها الذكاء الاصطناعي\n"
               "➕ /ورد_يدوي — إضافة نوع بالخطوات")
        else:
            total_s = sum(f["count"] for f in flowers if f.get("unit","وردة")!="بندلة")
            total_b = sum(f["count"] for f in flowers if f.get("unit","")=="بندلة")
            updated = flowers[0]["updated"] if flowers else ""
            lines = "\n".join(
                f"{'🌸' if f.get('unit')=='بندلة' else '🌹'} {f['name']}: {f['count']} {f.get('unit','وردة')}"
                for f in flowers)
            summary = f"📊 الإجمالي: {total_s} وردة" + (f" | {total_b} بندلة" if total_b else "")
            tg(chat, f"🌸 <b>مخزون الورد</b>\n\n{lines}\n\n{summary}\n🕐 آخر تحديث: {updated}")
        return "ok"

    if text in ["/مصاريف","/expenses"]:
        expenses = db_get("SELECT * FROM expenses ORDER BY id")
        lines = []
        for e in expenses:
            last = f" — آخر دفع: {e['last_paid']}" if e.get("last_paid") else " — لم يُدفع بعد"
            lines.append(f"{'⚡' if 'كهرب' in e['name'] else '🏪' if 'إيجار' in e['name'] else '👷'} <b>{e['name']}</b>: {fmt_omr(e['amount'])}{last}")
        tg(chat, f"💼 <b>المصاريف الثابتة</b>\n\n" + "\n".join(lines) +
           "\n\nللتسجيل: <code>دفعت راتب</code> أو <code>دفعت إيجار</code> أو <code>دفعت كهرباء 45.000</code>")
        return "ok"

    if text in ["/حذف", "/undo", "/del"]:
        last = db_one("SELECT * FROM entries WHERE type='s' ORDER BY id DESC LIMIT 1")
        if not last:
            tg(chat, "⚠️ لا توجد مبيعات مسجلة لحذفها")
        else:
            tg_buttons(chat,
                f"🗑️ <b>حذف آخر مبيعة؟</b>\n\n📝 {last['desc']}\n💰 {fmt_omr(last['amt'])}\n📅 {last.get('date','')}",
                [[{"label":"✅ نعم، احذفها","data":f"del_entry:{last['id']}"},
                  {"label":"❌ لا، إلغاء","data":"cancel_del"}]])
        return "ok"

    if text in ["/ايجار_الرفوف", "/shelf_rent"]:
        shelves = db_get("SELECT * FROM shelves ORDER BY id")
        total_rent = sum(float(s.get("rent",0)) for s in shelves)
        lines = "\n".join(f"🗄️ رف {s['name']}: {fmt_omr(float(s.get('rent',0)))}" for s in shelves)
        # Auto-register shelf rents as expenses for this month
        now_date = datetime.now().strftime("%d/%m/%Y")
        registered = 0
        for s in shelves:
            rent = float(s.get("rent",0))
            if rent > 0:
                existing = db_one(
                    "SELECT id FROM entries WHERE type='expense' AND desc=? AND month=?",
                    (f"إيجار رف {s['name']}", month))
                if not existing:
                    db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                           ("expense", f"إيجار رف {s['name']}", rent, now_date, month, "مصاريف ثابتة"))
                    registered += 1
        msg = f"🗄️ <b>إيجارات الرفوف — {month}</b>\n\n{lines}\n\n📊 الإجمالي: {fmt_omr(total_rent)}"
        if registered > 0:
            msg += f"\n\n✅ تم تسجيل {registered} إيجار تلقائياً"
        tg(chat, msg)
        return "ok"

    if text in ["/رفوف", "/shelf_summary", "/ملخص_الرفوف"]:
        shelves = db_get("SELECT * FROM shelves ORDER BY id")
        lines = []
        total_shelf_sales = 0
        for sh in shelves:
            row = db_one("SELECT COALESCE(SUM(amt),0) as total, COUNT(*) as cnt FROM entries WHERE type='s' AND shelf_id=? AND month=?", (sh["id"], month))
            sh_total = float(row["total"]) if row else 0
            sh_cnt = int(row["cnt"]) if row else 0
            rent = float(sh.get("rent") or 0)
            net = sh_total - rent
            net_emoji = "✅" if net >= 0 else "🔴"
            total_shelf_sales += sh_total
            # آخر 3 مبيعات
            recent = db_get("SELECT desc,amt FROM entries WHERE type='s' AND shelf_id=? AND month=? ORDER BY created DESC LIMIT 3", (sh["id"], month))
            recent_lines = "\n".join(f"    • {e['desc']}: {fmt_omr(e['amt'])}" for e in recent) if recent else "    لا توجد مبيعات"
            lines.append(
                f"🗄️ <b>رف {sh['name']}</b>\n"
                f"💰 مبيعات: {fmt_omr(sh_total)} ({sh_cnt} عملية)\n"
                f"🏷️ إيجار: {fmt_omr(rent)}\n"
                f"{net_emoji} صافي: {fmt_omr(net)}\n"
                f"آخر مبيعات:\n{recent_lines}"
            )
        tg(chat,
           f"🗄️ <b>ملخص الرفوف — {month}</b>\n\n" +
           "\n\n".join(lines) +
           f"\n\n{'━'*18}\n💰 إجمالي مبيعات الرفوف: {fmt_omr(total_shelf_sales)}")
        return "ok"

    if text == "/فئات":
        s,_=get_month_data(month)
        cats={}
        for e in s:
            c=e.get("category") or "أخرى"
            if c not in cats: cats[c]={"t":0,"c":0}
            cats[c]["t"]+=e["amt"]; cats[c]["c"]+=1
        cats_sorted=sorted(cats.items(),key=lambda x:-x[1]["t"])
        lines="\n".join(f"🏷️ <b>{k}</b>: {fmt_omr(v['t'])} ({v['c']} مبيعة)" for k,v in cats_sorted) if cats_sorted else "لا توجد مبيعات"
        tg(chat,f"📈 <b>مبيعات حسب الفئة — {month}</b>\n\n{lines}")
        return "ok"

    # Shelf commands: /رف ريحان etc
    if text.startswith("/رف"):
        shelf_name=text.replace("/رف","").strip()
        if not shelf_name:
            shelves=db_get("SELECT * FROM shelves ORDER BY id")
            lines="\n".join(f"🗄️ /رف {s['name']} — إيجار {fmt_omr(s.get('rent',0))}" for s in shelves)
            tg(chat,f"🗄️ <b>الرفوف المتاحة:</b>\n\n{lines}"); return "ok"
        shelf=db_one("SELECT * FROM shelves WHERE name=?",(shelf_name,))
        if not shelf:
            tg(chat,f"❌ ما وجدت رف اسمه '{shelf_name}'\n\nالرفوف: ريحان، فتحية، فطوم، اكسسوارات")
            return "ok"
        prods=db_get("SELECT * FROM shelf_products WHERE shelf_id=? AND qty>0 ORDER BY name",(shelf["id"],))
        if not prods:
            tg(chat,f"🗄️ رف <b>{shelf_name}</b> — لا توجد منتجات متاحة")
            return "ok"
        lines="\n".join(f"{'▫️'} {p['name']} — {fmt_omr(p['price'])} × {p['qty']} قطعة" for p in prods)
        tg(chat,
           f"🗄️ <b>رف {shelf_name}</b>\n\n{lines}\n\n"
           f"للبيع أرسل مثلاً:\n<code>بعت {prods[0]['name']} من رف {shelf_name} بـ {prods[0]['price']}</code>")
        return "ok"

    if text in ["/طلبات", "/orders", "/pending"]:
        orders = db_get("SELECT * FROM orders WHERE status='pending' ORDER BY created DESC")
        if not orders:
            tg(chat, "✅ لا توجد طلبات قيد الانتظار حالياً 🎉")
        else:
            lines = []
            for o in orders:
                ph = f" — {o['customer_phone']}" if o.get("customer_phone") else ""
                price_line = f"\n💰 السعر: {fmt_omr(float(o['price']))}" if o.get("price") and float(o['price']) > 0 else ""
                img_note = " 📸" if o.get("img_file_id") else ""
                lines.append(
                    f"📋 <b>طلب #{o['id']}</b>{img_note}\n"
                    f"👤 {o['customer_name']}{ph}\n"
                    f"📝 {o['description']}{price_line}\n"
                    f"📅 {o['date']}"
                )
            tg(chat,
               f"📋 <b>الطلبات قيد الانتظار ({len(orders)})</b>\n\n" +
               "\n\n".join(lines) +
               "\n\nلإنجاز طلب: افتح الموقع → العملاء → الطلبات")
        return "ok"

    if text in ["/عملائي", "/customers"]:
        customers = db_get("SELECT * FROM customers ORDER BY name")
        if not customers:
            tg(chat, "👥 لا يوجد عملاء مسجلون بعد.\n\nأضف من الموقع في قسم العملاء.")
        else:
            lines = []
            for c in customers:
                ph = f"\n📞 {c['phone']}" if c.get("phone") else ""
                nt = f"\n📝 {c['notes']}" if c.get("notes") else ""
                lp = f"\n🛍️ آخر شراء: {c['last_purchase']}" if c.get("last_purchase") else ""
                lines.append(f"👤 <b>{c['name']}</b>{ph}{nt}{lp}")
            tg(chat, f"👥 <b>العملاء الدائمون ({len(customers)})</b>\n\n" + "\n\n".join(lines))
        return "ok"

    if text in ["/ديوني", "/debts"]:
        debts = db_get("SELECT * FROM debts WHERE paid=0 ORDER BY created DESC")
        if not debts:
            tg(chat, "✅ لا توجد ديون غير مسددة 🎉")
        else:
            total = sum(float(d["amount"]) for d in debts)
            lines = []
            for d in debts:
                ph = f" — {d['customer_phone']}" if d.get("customer_phone") else ""
                desc = f"\n📝 {d['description']}" if d.get("description") else ""
                lines.append(f"💳 <b>{d['customer_name']}</b>{ph}\n💰 {fmt_omr(float(d['amount']))}{desc}\n📅 {d['date']}")
            tg(chat, f"💳 <b>الديون غير المسددة ({len(debts)})</b>\n\n" + "\n\n".join(lines) + f"\n\n{'━'*18}\n💰 الإجمالي: {fmt_omr(total)}")
        return "ok"

    if text in ["/من_دفع","/mandafa3"]:
        _,buys=get_month_data(month)
        pd={}
        for en in buys:
            p=en.get("paid_by") or "غير محدد"
            if p not in pd: pd[p]={"t":0,"c":0}
            pd[p]["t"]+=en["amt"]; pd[p]["c"]+=1
        lines="\n".join(f"👤 <b>{k}</b>: {fmt_omr(v['t'])} ({v['c']} عمليات)" for k,v in pd.items()) if pd else "لا يوجد"
        tg(chat,f"💳 <b>من دفع — {month}</b>\n\n{lines}"); return "ok"

    # Expense detection
    exp_keywords = {
        "راتب": ("راتب العامل", 220),
        "إيجار المحل": ("إيجار المحل", 100),
        "إيجار": ("إيجار المحل", 100),
        "كهرباء": ("تعبئة كهرباء", 0),
        "كهربا": ("تعبئة كهرباء", 0),
        "تعبئة": ("تعبئة كهرباء", 0),
    }
    for kw, (exp_name, default_amt) in exp_keywords.items():
        if kw in text and any(w in text for w in ["دفعت","دفع","سددت","سديت"]):
            import re as _re
            nums = _re.findall(r'\d+[.,]\d+|\d+', text)
            amt = float(nums[0].replace(',','.')) if nums else default_amt
            if amt > 0:
                exp = db_one("SELECT * FROM expenses WHERE name=?", (exp_name,))
                date_now = datetime.now().strftime("%d/%m/%Y")
                db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                       ("expense", exp_name, amt, date_now, month, "مصاريف ثابتة"))
                if exp:
                    db_run("UPDATE expenses SET last_paid=?, month=?, amount=? WHERE id=?",
                           (date_now, month, amt, exp["id"]))
                tg(chat, f"✅ <b>تم تسجيل {exp_name}</b>\n💰 {fmt_omr(amt)}\n📅 {date_now}")
                return "ok"

    # ── الذكاء الاصطناعي الكامل ──
    ai = groq_chat(text, chat) if GROQ_KEY else None
    if ai:
        action = ai.get("action","unknown")
        data   = ai.get("data",{})
        reply  = ai.get("reply","")

        # رد مباشر على سؤال أو كلام عام
        if action == "answer":
            tg(chat, reply or "كيف أقدر أساعدك؟")
            return "ok"

        # تقرير
        if action == "report":
            period = data.get("period","month")
            custom_date = data.get("date","")
            if period == "today" or "اليوم" in text:
                today_str = datetime.now().strftime("%d/%m/%Y")
                tg(chat, format_day_report(today_str))
            elif period == "custom" and custom_date:
                try:
                    datetime.strptime(custom_date, "%d/%m/%Y")
                    tg(chat, format_day_report(custom_date))
                except:
                    tg(chat, format_month_report(month))
            else:
                tg(chat, format_month_report(month))
            return "ok"

        # تسجيل مصروف
        if action == "register_expense":
            exp_name = data.get("expense_name") or data.get("desc","مصروف")
            amt = data.get("amt") or 0
            exp = db_one("SELECT * FROM expenses WHERE name=?",(exp_name,))
            if not exp:
                all_exp = db_get("SELECT * FROM expenses ORDER BY id")
                for e in all_exp:
                    if any(w in exp_name for w in e["name"].split()[:2]):
                        exp = e; exp_name = e["name"]; break
            final_amt = float(amt) if amt and float(amt)>0 else (float(exp["amount"]) if exp else 0)
            if final_amt <= 0:
                tg(chat, f"💸 كم مبلغ {exp_name}؟\nأرسل الرقم فقط: <code>220.000</code>")
                pending[chat] = {"waiting":"expense_amt","exp_name":exp_name,"exp_id":exp["id"] if exp else None}
                return "ok"
            date_now = datetime.now().strftime("%d/%m/%Y")
            db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                   ("expense",exp_name,final_amt,date_now,month,"مصاريف ثابتة"))
            if exp:
                db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",
                       (date_now,month,final_amt,exp["id"]))
            tg(chat,f"✅ <b>تم تسجيل {exp_name}</b>\n💰 {fmt_omr(final_amt)}\n📅 {date_now}")
            return "ok"

        # تسجيل مشتريات
        if action == "register_buy":
            desc   = data.get("desc","مشتريات")
            amt    = float(data.get("amt") or 0)
            paid_by = data.get("paid_by")
            if not amt or amt<=0:
                pending[chat]={"waiting":"buy_amt","desc":desc,"month":month}
                tg(chat,f"📦 <b>{desc}</b>\nكم المبلغ؟ أرسل الرقم فقط:")
                return "ok"
            if paid_by:
                db_run("INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",
                       ("b",desc,amt,date,month,paid_by))
                tg(chat,f"✅ <b>مشتريات مسجلة!</b>\n📦 {desc}\n💰 {fmt_omr(amt)}\n👤 {paid_by}")
            else:
                pending[chat]={"waiting":"paid_by","desc":desc,"amt":amt,"date":date,"month":month}
                tg_buttons(chat,f"📦 <b>مشتريات {fmt_omr(amt)}</b>\n📝 {desc}\n\n👤 من دفع؟",
                    [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                     [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
            return "ok"

        # تسجيل مبيعة
        if action == "register_sale":
            desc  = data.get("desc","مبيعة")
            amt   = float(data.get("amt") or 0)
            qty   = max(1, int(data.get("qty") or 1))
            pay   = data.get("payment")
            cat   = data.get("category") or detect_category(text)
            shelf_id_detected = None
            shelf_name = data.get("shelf")
            if not shelf_name:
                for sname in ["ريحان","فتحية","فطوم","اكسسوارات"]:
                    if sname in text:
                        shelf_name = sname; break
            if shelf_name:
                sh = db_one("SELECT id FROM shelves WHERE name=?",(shelf_name,))
                if sh: shelf_id_detected = sh["id"]
            # لو ما ذُكر مبلغ وفيه رف، نجيب سعر المنتج من قاعدة البيانات
            if shelf_id_detected and (not amt or amt<=0):
                prod_kw = desc.split()[0] if desc else ""
                prod = db_one("SELECT * FROM shelf_products WHERE shelf_id=? AND name LIKE ? AND qty>0",
                              (shelf_id_detected, f"%{prod_kw}%"))
                if prod: amt = prod["price"] * qty
            if not amt or amt<=0:
                pending[chat]={"waiting":"sale_amt","desc":desc,"qty":qty,"shelf_id":shelf_id_detected}
                tg(chat,f"🌸 <b>{desc}</b>" + (f" × {qty}" if qty>1 else "") + "\nكم المبلغ الإجمالي؟ أرسل الرقم فقط:")
                return "ok"
            unit_price = round(amt / qty, 3)
            cat_line = f"\n🏷️ {cat}" if cat else ""
            shelf_line = f"\n🗄️ رف {shelf_name}" if shelf_name else ""
            # تسجيل كل قطعة بسجل منفصل
            last_id = None
            for _ in range(qty):
                db_run("INSERT INTO entries (type,desc,amt,date,month,payment_method,category,shelf_id) VALUES (?,?,?,?,?,?,?,?)",
                       ("s",desc,unit_price,date,month,pay,cat,shelf_id_detected))
                if last_id is None:
                    row = db_one("SELECT id FROM entries ORDER BY id DESC LIMIT 1")
                    if row: last_id = row["id"]
            # تحديث كمية المنتج في الرف
            if shelf_id_detected and desc:
                prod_kw = desc.split()[0] if desc else ""
                prod = db_one("SELECT * FROM shelf_products WHERE shelf_id=? AND name LIKE ? AND qty>0",
                              (shelf_id_detected, f"%{prod_kw}%"))
                if prod: db_run("UPDATE shelf_products SET qty=MAX(0,qty-?) WHERE id=?",(qty, prod["id"]))
            qty_line = f" × {qty} = {fmt_omr(amt)}" if qty > 1 else f" = {fmt_omr(amt)}"
            confirm_text = f"✅ <b>{'مبيعات' if qty>1 else 'مبيعة'} مسجلة!</b>\n🌸 {qty}× {desc}\n💰 {fmt_omr(unit_price)} للقطعة{qty_line}{' — '+pay if pay else ''}{cat_line}{shelf_line}"
            if pay:
                tg_sale_confirm(chat, confirm_text, last_id)
            else:
                pending[chat]={"waiting":"sale_payment","shelf_id":shelf_id_detected,"shelf_name":shelf_name,"qty":qty,"desc":desc,"unit_price":unit_price,"cat_line":cat_line}
                tg_buttons(chat,f"🌸 <b>{'مبيعات' if qty>1 else 'مبيعة'} {fmt_omr(unit_price)}{'×'+str(qty) if qty>1 else ''}</b>\n📝 {qty}× {desc}{cat_line}{shelf_line}\n\n💳 طريقة الدفع؟",
                    [[{"label":"💵 كاش","data":"pay:كاش 💵"},{"label":"💳 فيزا","data":"pay:فيزا 💳"},{"label":"🏦 تحويل","data":"pay:تحويل 🏦"}]])
            return "ok"

        # unknown
        tg(chat, "لم أفهم 🤔\n\nجرّب:\n<code>بعت باقة بـ 4.500 كاش</code>\n<code>اشتريت ورد بـ 8.000</code>\n<code>دفعت الراتب</code>\n\n/help للمساعدة")
        return "ok"

    # fallback لو Groq ما شتغل
    parsed=groq_parse_text(text)
    if parsed.get("found"):
        etype=parsed.get("type"); desc=parsed.get("desc",""); amt=parsed.get("amt") or 0

        # مصروف ثابت
        if etype=="expense":
            exp_name = parsed.get("expense_name") or desc
            exp = db_one("SELECT * FROM expenses WHERE name=?", (exp_name,))
            if not exp:
                # حاول بمطابقة جزئية
                all_exp = db_get("SELECT * FROM expenses ORDER BY id")
                for e in all_exp:
                    if any(w in exp_name for w in e["name"].split()[:2]):
                        exp = e; exp_name = e["name"]; break
            final_amt = amt if amt and amt > 0 else (float(exp["amount"]) if exp else 0)
            if final_amt <= 0:
                tg(chat, f"💸 كم مبلغ {exp_name}؟\nأرسل الرقم فقط: <code>220.000</code>")
                pending[chat] = {"waiting":"expense_amt","exp_name":exp_name,"exp_id":exp["id"] if exp else None}
                return "ok"
            date_now = datetime.now().strftime("%d/%m/%Y")
            db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                   ("expense", exp_name, final_amt, date_now, month, "مصاريف ثابتة"))
            if exp:
                db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",
                       (date_now, month, final_amt, exp["id"]))
            tg(chat, f"✅ <b>تم تسجيل {exp_name}</b>\n💰 {fmt_omr(final_amt)}\n📅 {date_now}")
            return "ok"

        # مشتريات
        if etype=="b":
            if not amt or amt<=0:
                pending[chat]={"waiting":"buy_amt","desc":desc,"month":month}
                tg(chat,f"📦 <b>{desc}</b>\nكم المبلغ؟ أرسل الرقم فقط:")
                return "ok"
            paid_by = parsed.get("paid_by")
            if paid_by:
                db_run("INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",
                       ("b",desc,amt,date,month,paid_by))
                tg(chat, f"✅ <b>مشتريات مسجلة!</b>\n📦 {desc}\n💰 {fmt_omr(amt)}\n👤 {paid_by}")
            else:
                pending[chat]={"waiting":"paid_by","desc":desc,"amt":amt,"date":date,"month":month}
                tg_buttons(chat,f"📦 <b>مشتريات {fmt_omr(amt)}</b>\n📝 {desc}\n\n👤 من دفع؟",
                    [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                     [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
            return "ok"

        # مبيعة
        if etype=="s":
            qty = max(1, int(parsed.get("qty") or detect_qty_from_text(text)))
            if not amt or amt<=0:
                pending[chat]={"waiting":"sale_amt","desc":desc,"qty":qty}
                tg(chat,f"🌸 <b>{desc}</b>" + (f" × {qty}" if qty>1 else "") + "\nكم المبلغ الإجمالي؟ أرسل الرقم فقط:")
                return "ok"
            cat = parsed.get("category") or detect_category(text) or detect_category(desc)
            pay = parsed.get("payment")
            # كشف الرف
            shelf_id_detected = None
            shelf_name = parsed.get("shelf")
            if shelf_name:
                shelf = db_one("SELECT id FROM shelves WHERE name=?", (shelf_name,))
                if shelf: shelf_id_detected = shelf["id"]
            else:
                for sname in ["ريحان","فتحية","فطوم","اكسسوارات"]:
                    if sname in text:
                        shelf = db_one("SELECT id FROM shelves WHERE name=?", (sname,))
                        if shelf: shelf_id_detected = shelf["id"]; break
            unit_price = round(amt / qty, 3)
            cat_line = f"\n🏷️ {cat}" if cat else ""
            for _ in range(qty):
                db_run("INSERT INTO entries (type,desc,amt,date,month,payment_method,category,shelf_id) VALUES (?,?,?,?,?,?,?,?)",
                       ("s",desc,unit_price,date,month,pay,cat,shelf_id_detected))
            if shelf_id_detected and desc:
                prod=db_one("SELECT * FROM shelf_products WHERE shelf_id=? AND name LIKE ? AND qty>0",
                           (shelf_id_detected,f"%{desc.split()[0]}%"))
                if prod: db_run("UPDATE shelf_products SET qty=MAX(0,qty-?) WHERE id=?",(qty, prod["id"]))
            if pay:
                tg(chat, f"✅ <b>{'مبيعات' if qty>1 else 'مبيعة'} مسجلة!</b>\n🌸 {qty}× {desc}\n💰 {fmt_omr(unit_price)} للقطعة = {fmt_omr(amt)} — {pay}{cat_line}")
            else:
                pending[chat]={"waiting":"sale_payment","qty":qty,"desc":desc,"unit_price":unit_price,"cat_line":cat_line}
                tg_buttons(chat,f"🌸 <b>{'مبيعات' if qty>1 else 'مبيعة'} {fmt_omr(unit_price)}{'×'+str(qty) if qty>1 else ''}</b>\n📝 {qty}× {desc}{cat_line}\n\n💳 طريقة الدفع؟",
                    [[{"label":"💵 كاش","data":"pay:كاش 💵"},{"label":"💳 فيزا","data":"pay:فيزا 💳"},{"label":"🏦 تحويل","data":"pay:تحويل 🏦"}]])
            return "ok"
    else:
        tg(chat, "لم أفهم 🤔\n\nجرّب مثلاً:\n<code>بعت باقة بـ 4.500 كاش</code>\n<code>اشتريت ورد بـ 8.000</code>\n<code>دفعت الراتب</code>\n<code>دفعت الإيجار</code>\n\n/help للمساعدة")
    return "ok"

# ══════════════════════════════════════════════════════════════
# ── Daily Goal API ────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
@app.route("/api/settings/goal", methods=["GET"])
@auth
def api_get_goal():
    row = db_one("SELECT value FROM app_settings WHERE key='daily_goal'")
    goal = float(row["value"]) if row else 50.0
    today_str = datetime.now().strftime("%d/%m/%Y")
    entries = db_get("SELECT amt FROM entries WHERE type='s' AND date=? AND shelf_id IS NULL", (today_str,))
    today_total = round(sum(float(e["amt"]) for e in entries), 3)
    return jsonify({"goal": goal, "today": today_total})

@app.route("/api/settings/goal", methods=["POST"])
@auth
def api_set_goal():
    d = request.json or {}
    goal = float(d.get("goal", 50))
    db_run("INSERT OR REPLACE INTO app_settings (key,value) VALUES (?,?)", ("daily_goal", str(goal)))
    return jsonify({"ok": True})

# ══════════════════════════════════════════════════════════════
# ── Customers API ────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
@app.route("/api/customers", methods=["GET"])
@auth
def api_get_customers():
    q = request.args.get("q","").strip()
    if q:
        rows = db_get("SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY name", (f"%{q}%", f"%{q}%"))
    else:
        rows = db_get("SELECT * FROM customers ORDER BY name")
    return jsonify(rows)

@app.route("/api/customers", methods=["POST"])
@auth
def api_add_customer():
    d = request.json or {}
    if not d.get("name"): return jsonify({"ok":False,"error":"name required"}), 400
    db_run("INSERT INTO customers (name,phone,notes) VALUES (?,?,?)",
           (d["name"].strip(), d.get("phone","").strip(), d.get("notes","").strip()))
    return jsonify({"ok": True})

@app.route("/api/customers/<int:cid>", methods=["PATCH"])
@auth
def api_edit_customer(cid):
    d = request.json or {}
    fields, vals = [], []
    if "name"  in d: fields.append("name=?");  vals.append(d["name"].strip())
    if "phone" in d: fields.append("phone=?"); vals.append(d["phone"].strip())
    if "notes" in d: fields.append("notes=?"); vals.append(d["notes"].strip())
    if not fields: return jsonify({"ok":False})
    vals.append(cid)
    db_run(f"UPDATE customers SET {','.join(fields)} WHERE id=?", vals)
    return jsonify({"ok": True})

@app.route("/api/customers/<int:cid>", methods=["DELETE"])
@auth
def api_del_customer(cid):
    db_run("DELETE FROM customers WHERE id=?", (cid,))
    return jsonify({"ok": True})

# ══════════════════════════════════════════════════════════════
# ── Product Catalog API ───────────────────────────────────────
# ══════════════════════════════════════════════════════════════
@app.route("/api/catalog", methods=["GET"])
def api_get_catalog():
    rows = db_get("SELECT * FROM catalog_products ORDER BY available DESC, name")
    return jsonify(rows)

@app.route("/api/catalog", methods=["POST"])
@auth
def api_add_catalog():
    d = request.json or {}
    if not d.get("name"): return jsonify({"ok":False}), 400
    db_run("INSERT INTO catalog_products (name,price,description,img,available) VALUES (?,?,?,?,?)",
           (d["name"].strip(), float(d.get("price",0)), d.get("description","").strip(),
            d.get("img",""), int(d.get("available",1))))
    return jsonify({"ok": True})

@app.route("/api/catalog/<int:pid>", methods=["PATCH"])
@auth
def api_edit_catalog(pid):
    d = request.json or {}
    fields, vals = [], []
    for col in ["name","price","description","img","available"]:
        if col in d:
            fields.append(f"{col}=?")
            vals.append(float(d[col]) if col in ("price",) else int(d[col]) if col=="available" else d[col])
    if not fields: return jsonify({"ok":False})
    vals.append(pid)
    db_run(f"UPDATE catalog_products SET {','.join(fields)} WHERE id=?", vals)
    return jsonify({"ok": True})

@app.route("/api/catalog/<int:pid>", methods=["DELETE"])
@auth
def api_del_catalog(pid):
    db_run("DELETE FROM catalog_products WHERE id=?", (pid,))
    return jsonify({"ok": True})

# ══════════════════════════════════════════════════════════════
# ── Debts API ─────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
@app.route("/api/debts", methods=["GET"])
@auth
def api_get_debts():
    show_paid = request.args.get("paid","0") == "1"
    if show_paid:
        rows = db_get("SELECT * FROM debts ORDER BY paid ASC, created DESC")
    else:
        rows = db_get("SELECT * FROM debts WHERE paid=0 ORDER BY created DESC")
    total_unpaid = db_one("SELECT COALESCE(SUM(amount),0) as t FROM debts WHERE paid=0")
    return jsonify({"debts": rows, "total_unpaid": float(total_unpaid["t"]) if total_unpaid else 0})

@app.route("/api/debts", methods=["POST"])
@auth
def api_add_debt():
    d = request.json or {}
    if not d.get("customer_name") or not d.get("amount"):
        return jsonify({"ok":False,"error":"name and amount required"}), 400
    date_val = d.get("date", datetime.now().strftime("%d/%m/%Y"))
    db_run("INSERT INTO debts (customer_name,customer_phone,amount,description,date) VALUES (?,?,?,?,?)",
           (d["customer_name"].strip(), d.get("customer_phone","").strip(),
            float(d["amount"]), d.get("description","").strip(), date_val))
    return jsonify({"ok": True})

@app.route("/api/debts/<int:did>/pay", methods=["POST"])
@auth
def api_pay_debt(did):
    paid_date = datetime.now().strftime("%d/%m/%Y")
    db_run("UPDATE debts SET paid=1, paid_date=? WHERE id=?", (paid_date, did))
    return jsonify({"ok": True})

@app.route("/api/debts/<int:did>", methods=["DELETE"])
@auth
def api_del_debt(did):
    db_run("DELETE FROM debts WHERE id=?", (did,))
    return jsonify({"ok": True})

# ══════════════════════════════════════════════════════════════
# ── Print Feed (للطباعة التلقائية من الماك) ──────────────────
@app.route("/api/voice-order", methods=["POST"])
def api_voice_order():
    """
    Endpoint للطلبات الصوتية من سيري / Shortcuts
    POST JSON: { token, customer_name, customer_phone, description, price, notes }
    """
    d = request.json or {}
    token    = d.get("token","")
    expected = os.environ.get("VOICE_TOKEN","")
    if not expected or token != expected:
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    name = (d.get("customer_name") or "").strip()
    desc = (d.get("description")   or "").strip()
    if not name or not desc:
        return jsonify({"ok": False, "error": "customer_name and description required"}), 400
    date_val = datetime.now().strftime("%d/%m/%Y")
    db_run(
        "INSERT INTO orders (customer_name,customer_phone,description,price,notes,date,source) VALUES (?,?,?,?,?,?,?)",
        (name,
         (d.get("customer_phone") or "").strip(),
         desc,
         float(d.get("price") or 0),
         (d.get("notes") or "").strip(),
         date_val,
         "siri")
    )
    # إشعار تيليغرام
    try:
        order_id = db_one("SELECT last_insert_rowid() as id")
        oid = order_id["id"] if order_id else "?"
        msg = (f"🎤 طلب صوتي جديد #{oid}\n"
               f"👤 {name}\n"
               f"📞 {d.get('customer_phone','—') or '—'}\n"
               f"📝 {desc}\n"
               + (f"💰 {float(d['price']):.3f} OMR\n" if d.get("price") and float(d.get("price",0))>0 else "")
               + (f"📌 {d['notes']}\n" if d.get("notes") else ""))
        send_telegram(msg)
    except Exception as e:
        print("voice-order telegram error:", e)
    return jsonify({"ok": True, "message": "تم تسجيل الطلب بنجاح ✅"})

@app.route("/api/print-feed")
def api_print_feed():
    """Endpoint آمن بـ token للسكريبت على الماك"""
    token = request.args.get("token","")
    expected = os.environ.get("PRINT_TOKEN","")
    if not expected or token != expected:
        return jsonify({"error":"unauthorized"}), 401
    orders = db_get("SELECT * FROM orders WHERE status='pending' ORDER BY created DESC")
    return jsonify({"orders": orders, "count": len(orders)})

# ── Orders API ───────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
@app.route("/api/orders", methods=["GET"])
@worker_auth
def api_get_orders():
    status = request.args.get("status", "")
    if status:
        rows = db_get("SELECT * FROM orders WHERE status=? ORDER BY created DESC", (status,))
    else:
        rows = db_get("SELECT * FROM orders ORDER BY created DESC")
    pending_count = db_one("SELECT COUNT(*) as c FROM orders WHERE status='pending'")
    return jsonify({"orders": rows, "pending_count": int(pending_count["c"]) if pending_count else 0})

@app.route("/api/orders", methods=["POST"])
@auth
def api_add_order():
    d = request.json or {}
    if not d.get("customer_name") or not d.get("description"):
        return jsonify({"ok": False, "error": "name and description required"}), 400
    date_val = datetime.now().strftime("%d/%m/%Y")
    db_run("INSERT INTO orders (customer_name,customer_phone,description,price,notes,date,source) VALUES (?,?,?,?,?,?,?)",
           (d["customer_name"].strip(), d.get("customer_phone","").strip(),
            d["description"].strip(), float(d.get("price",0)),
            d.get("notes","").strip(), date_val, "web"))
    return jsonify({"ok": True})

@app.route("/api/orders/<int:oid>", methods=["PATCH"])
@worker_auth
def api_edit_order(oid):
    d = request.json or {}
    fields, vals = [], []
    for col in ["customer_name","customer_phone","description","price","notes","status"]:
        if col in d:
            fields.append(f"{col}=?")
            vals.append(float(d[col]) if col == "price" else d[col])
    if "status" in d and d["status"] == "done":
        fields.append("done_date=?")
        vals.append(datetime.now().strftime("%d/%m/%Y"))
    if not fields: return jsonify({"ok": False})
    vals.append(oid)
    db_run(f"UPDATE orders SET {','.join(fields)} WHERE id=?", vals)
    # إذا تم الطلب → أرسل إشعار للبوت
    if d.get("status") == "done":
        order = db_one("SELECT * FROM orders WHERE id=?", (oid,))
        if order:
            token = BOT_TOKEN
            chat_id = os.environ.get("OWNER_CHAT_ID","")
            if token and chat_id:
                try:
                    price_line = f"\n💰 السعر: {fmt_omr(float(order['price']))}" if order.get('price') and float(order['price']) > 0 else ""
                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                        json={"chat_id": int(chat_id),
                              "text": f"✅ <b>تم إنجاز طلب!</b>\n\n👤 {order['customer_name']}\n📝 {order['description']}{price_line}",
                              "parse_mode": "HTML"}, timeout=10)
                except: pass
    return jsonify({"ok": True})

@app.route("/api/orders/<int:oid>", methods=["DELETE"])
@auth
def api_del_order(oid):
    db_run("DELETE FROM orders WHERE id=?", (oid,))
    return jsonify({"ok": True})

@app.route("/api/orders/<int:oid>/image")
def api_order_image(oid):
    """إعادة توجيه صورة الطلب من تيليغرام"""
    order = db_one("SELECT img_file_id FROM orders WHERE id=?", (oid,))
    if not order or not order.get("img_file_id"):
        return "", 404
    try:
        r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
                         params={"file_id": order["img_file_id"]}, timeout=10)
        file_path = r.json()["result"]["file_path"]
        img_r = requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}", timeout=15)
        return Response(img_r.content, mimetype="image/jpeg")
    except:
        return "", 404

# ══════════════════════════════════════════════════════════════
# ── Cash Register API (خزينة الكاش) ─────────────────────────
# ══════════════════════════════════════════════════════════════
def get_cash_balance():
    """احسب رصيد الخزينة الحالي"""
    row = db_one("SELECT COALESCE(SUM(CASE WHEN type='in' THEN amount ELSE -amount END),0) as bal FROM cash_log")
    return float(row["bal"]) if row else 0.0

@app.route("/api/cash")
@worker_auth
def api_get_cash():
    balance = get_cash_balance()
    today_str = datetime.now().strftime("%d/%m/%Y")
    log = db_get("SELECT * FROM cash_log ORDER BY created DESC LIMIT 30")
    today_in  = sum(r["amount"] for r in log if r["type"]=="in"  and r["date"]==today_str)
    today_out = sum(r["amount"] for r in log if r["type"]=="out" and r["date"]==today_str)
    return jsonify({"balance": round(balance,3), "log": log,
                    "today_in": round(today_in,3), "today_out": round(today_out,3)})

@app.route("/api/cash/adjust", methods=["POST"])
@worker_auth
def api_cash_adjust():
    """إضافة أو سحب يدوي من الخزينة"""
    d = request.json or {}
    amt   = float(d.get("amount", 0))
    typ   = d.get("type", "in")   # in / out
    desc  = d.get("description", "تعديل يدوي")
    if amt <= 0: return jsonify({"ok": False, "error": "invalid amount"}), 400
    date_val = datetime.now().strftime("%d/%m/%Y")
    db_run("INSERT INTO cash_log (type,amount,description,date) VALUES (?,?,?,?)",
           (typ, amt, desc, date_val))
    return jsonify({"ok": True, "balance": round(get_cash_balance(), 3)})

@app.route("/api/cash/reset", methods=["POST"])
@auth
def api_cash_reset():
    """مسح سجل الخزينة (للمدير فقط)"""
    db_run("DELETE FROM cash_log")
    return jsonify({"ok": True})

@app.route("/api/cash/log/<int:lid>", methods=["DELETE"])
@auth
def api_cash_del_log(lid):
    row = db_one("SELECT * FROM cash_log WHERE id=?", (lid,))
    if not row: return jsonify({"ok": False}), 404
    db_run("DELETE FROM cash_log WHERE id=?", (lid,))
    return jsonify({"ok": True, "balance": round(get_cash_balance(), 3)})

@app.route("/turso_debug")
def turso_debug():
    """Show raw Turso response for debugging."""
    try:
        res = turso_exec("SELECT * FROM shelves")
        return jsonify({"raw": res})
    except Exception as e:
        return jsonify({"error": str(e)})

# ── Expenses API ─────────────────────────────────────────
@app.route("/api/expenses")
def api_get_expenses():
    month = request.args.get("month", cur_month())
    expenses = db_get("SELECT * FROM expenses ORDER BY id")
    # Get paid expenses for this month
    paid = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month,))
    return jsonify({"expenses": expenses, "paid": paid})

@app.route("/api/expenses/<int:eid>/pay", methods=["POST"])
def api_pay_expense(eid):
    d = request.json
    month_val = d.get("month", cur_month())
    custom_date = d.get("date", "").strip()
    date_val = custom_date if custom_date else datetime.now().strftime("%d/%m/%Y")
    exp = db_one("SELECT * FROM expenses WHERE id=?", (eid,))
    if not exp: return jsonify({"ok": False}), 404
    amt = float(d.get("amount", exp["amount"]))
    db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
           ("expense", exp["name"], amt, date_val, month_val, "مصاريف ثابتة"))
    db_run("UPDATE expenses SET last_paid=?, month=?, amount=? WHERE id=?",
           (date_val, month_val, amt, eid))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>", methods=["POST"])
def api_update_expense(eid):
    d = request.json
    db_run("UPDATE expenses SET amount=? WHERE id=?", (float(d["amount"]), eid))
    return jsonify({"ok": True})

@app.route("/api/expenses", methods=["POST"])
def api_add_expense():
    d = request.json
    db_run("INSERT INTO expenses (name,amount,type) VALUES (?,?,?)",
           (d["name"], float(d.get("amount",0)), d.get("type","monthly")))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>", methods=["DELETE"])
def api_del_expense(eid):
    db_run("DELETE FROM expenses WHERE id=?", (eid,))
    return jsonify({"ok": True})

@app.route("/api/expense_entries/<int:eid>", methods=["DELETE"])
def api_del_expense_entry(eid):
    """Delete a specific expense entry."""
    db_run("DELETE FROM entries WHERE id=? AND type='expense'", (eid,))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>/reset", methods=["POST"])
def api_reset_expense(eid):
    """Reset expense paid status."""
    d = request.json or {}
    month_val = d.get("month", cur_month())
    exp = db_one("SELECT * FROM expenses WHERE id=?", (eid,))
    if exp and exp.get("month") == month_val:
        db_run("UPDATE expenses SET last_paid=NULL, month=NULL WHERE id=?", (eid,))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>", methods=["DELETE"])
def api_delete_expense_def(eid):
    """Delete an expense definition entirely."""
    db_run("DELETE FROM expenses WHERE id=?", (eid,))
    return jsonify({"ok": True})

@app.route("/api/report/pdf")
@auth
def api_report_pdf():
    try:
        period    = request.args.get("period", "month")
        rtype     = request.args.get("type", "all")
        month_val = request.args.get("month", cur_month())
        day_val   = request.args.get("day", "")

        def fr(n): return f"{float(n):,.3f}"
        def rc(i): return "even" if i%2==0 else ""

        type_labels = {"all":"شامل","sales":"مبيعات","buys":"مشتريات","expenses":"مصاريف"}
        period_label = f"يوم {day_val}" if period=="day" else f"شهر {month_val}"
        title = f"فيروز فلورز — تقرير {type_labels.get(rtype,rtype)} — {period_label}"

        # ── جلب البيانات ──
        if period == "day" and day_val:
            s_all, b_all, e_all = get_day_data(day_val)
        else:
            s_all, b_all = get_month_data(month_val)
            e_all = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY date DESC", (month_val,))

        buys_only = [b for b in b_all if b.get("type")=="b"]
        exp_defs  = db_get("SELECT * FROM expenses ORDER BY id")

        ts = sum(e["amt"] for e in s_all)
        tb = sum(e["amt"] for e in buys_only)
        te = sum(e["amt"] for e in e_all)
        tp = ts - tb
        tn = tp - te

        # ── ملخص ──
        summary_html = ""
        if rtype == "all":
            net_color = "green" if tn>=0 else "red"
            summary_html = f"""
            <div class="sum-grid">
              <div class="sum-card green"><div class="sum-ico">💰</div><div class="sum-val">{fr(ts)}</div><div class="sum-lbl">المبيعات<br><span>{len(s_all)} عملية</span></div></div>
              <div class="sum-card red"><div class="sum-ico">🛒</div><div class="sum-val">{fr(tb)}</div><div class="sum-lbl">المشتريات<br><span>{len(buys_only)} عملية</span></div></div>
              <div class="sum-card gold"><div class="sum-ico">💸</div><div class="sum-val">{fr(te)}</div><div class="sum-lbl">المصاريف<br><span>{len(e_all)} عملية</span></div></div>
              <div class="sum-card blue"><div class="sum-ico">📊</div><div class="sum-val">{fr(tp)}</div><div class="sum-lbl">ربح قبل المصاريف<br><span>{"✅" if tp>=0 else "⚠️"}</span></div></div>
              <div class="sum-card {net_color} span2"><div class="sum-ico">🏆</div><div class="sum-val big">{fr(tn)}</div><div class="sum-lbl">الربح الصافي النهائي<br><span>{"✅ ربح" if tn>=0 else "⚠️ خسارة"}</span></div></div>
            </div>"""

        # ── إضافة تفصيل يومي للتقرير الشهري ──
        daily_html = ""
        if period == "month" and rtype in ("all","sales"):
            day_map = {}
            for e in s_all:
                d = e.get("date","")
                if d not in day_map: day_map[d] = {"s":0,"b":0,"sc":0,"bc":0}
                day_map[d]["s"]+=e["amt"]; day_map[d]["sc"]+=1
            for e in buys_only:
                d = e.get("date","")
                if d not in day_map: day_map[d] = {"s":0,"b":0,"sc":0,"bc":0}
                day_map[d]["b"]+=e["amt"]; day_map[d]["bc"]+=1
            if day_map:
                day_rows = "".join(f"""<tr class="{rc(i)}">
                    <td>{d}</td>
                    <td class="num green-t">{fr(v["s"])}</td><td class="cnt">{v["sc"]}</td>
                    <td class="num red-t">{fr(v["b"])}</td><td class="cnt">{v["bc"]}</td>
                    <td class="num {"green-t" if v["s"]-v["b"]>=0 else "red-t"}">{fr(v["s"]-v["b"])}</td>
                    </tr>"""
                    for i,(d,v) in enumerate(sorted(day_map.items()),1))
                daily_html = f"""
                <h2 class="sec-title blue-t">📆 التفصيل اليومي</h2>
                <table><thead><tr><th>اليوم</th><th>المبيعات</th><th>#</th><th>المشتريات</th><th>#</th><th>الصافي</th></tr></thead>
                <tbody>{day_rows}</tbody></table>"""

        # ── جدول المبيعات ──
        sales_html = ""
        if rtype in ("all","sales") and s_all:
            # تجميع حسب الفئة
            cats = {}
            for e in s_all:
                c = e.get("category","أخرى") or "أخرى"
                cats[c] = cats.get(c,0) + e["amt"]
            cat_summary = "".join(f'<span class="cat-chip">{c}: {fr(v)}</span>' for c,v in sorted(cats.items(),key=lambda x:-x[1]))
            rows = "".join(f"""<tr class="{rc(i)}">
                <td>{i}</td><td><b>{e.get("desc","")}</b></td>
                <td><span class="chip">{e.get("category","-") or "-"}</span></td>
                <td><span class="chip pay">{e.get("payment_method","-") or "-"}</span></td>
                <td>{e.get("date","")}</td>
                <td class="num green-t">{fr(e["amt"])}</td></tr>"""
                for i,e in enumerate(s_all,1))
            sales_html = f"""
            <h2 class="sec-title green-t">🌸 المبيعات ({len(s_all)} عملية)</h2>
            <div class="cat-row">{cat_summary}</div>
            <table><thead><tr><th>#</th><th>الوصف</th><th>الفئة</th><th>طريقة الدفع</th><th>التاريخ</th><th>المبلغ</th></tr></thead>
            <tbody>{rows}</tbody>
            <tfoot><tr><td colspan="5"><b>الإجمالي</b></td><td class="num"><b>{fr(ts)}</b></td></tr></tfoot></table>"""

        # ── جدول المشتريات ──
        buys_html = ""
        if rtype in ("all","buys") and buys_only:
            # تجميع حسب من دفع
            payers = {}
            for e in buys_only:
                p = e.get("paid_by","غير محدد") or "غير محدد"
                payers[p] = payers.get(p,0) + e["amt"]
            payer_summary = "".join(f'<span class="cat-chip red-chip">{p}: {fr(v)}</span>' for p,v in sorted(payers.items(),key=lambda x:-x[1]))
            rows = "".join(f"""<tr class="{rc(i)}">
                <td>{i}</td><td><b>{e.get("desc","")}</b></td>
                <td><span class="chip">{e.get("paid_by","-") or "-"}</span></td>
                <td>{e.get("date","")}</td>
                <td class="num red-t">{fr(e["amt"])}</td></tr>"""
                for i,e in enumerate(buys_only,1))
            buys_html = f"""
            <h2 class="sec-title red-t">📦 المشتريات ({len(buys_only)} عملية)</h2>
            <div class="cat-row">{payer_summary}</div>
            <table><thead><tr><th>#</th><th>الوصف</th><th>من دفع</th><th>التاريخ</th><th>المبلغ</th></tr></thead>
            <tbody>{rows}</tbody>
            <tfoot><tr><td colspan="4"><b>الإجمالي</b></td><td class="num"><b>{fr(tb)}</b></td></tr></tfoot></table>"""

        # ── جدول المصاريف ──
        exps_html = ""
        if rtype in ("all","expenses"):
            def_rows = "".join(f"""<tr class="{rc(i)}">
                <td><b>{e["name"]}</b></td>
                <td class="num">{fr(float(e["amount"]))}</td>
                <td>{e.get("last_paid") or "لم يُدفع"}</td>
                <td><span class="badge {"paid" if e.get("month")==month_val else "unpaid"}">{("✅ مدفوع" if e.get("month")==month_val else "⏳ لم يُدفع")}</span></td></tr>"""
                for i,e in enumerate(exp_defs,1))
            exp_rows = "".join(f"""<tr class="{rc(i)}">
                <td>{i}</td><td><b>{e.get("desc","")}</b></td>
                <td>{e.get("date","")}</td>
                <td class="num gold-t">{fr(e["amt"])}</td></tr>"""
                for i,e in enumerate(e_all,1))
            exps_html = f"""
            <h2 class="sec-title gold-t">💸 المصاريف الثابتة</h2>
            <table><thead><tr><th>المصروف</th><th>المبلغ الشهري</th><th>آخر دفع</th><th>الحالة</th></tr></thead>
            <tbody>{def_rows}</tbody></table>
            {f'<h3 class="sub-h">سجل الدفعات</h3><table><thead><tr><th>#</th><th>الوصف</th><th>التاريخ</th><th>المبلغ</th></tr></thead><tbody>'+exp_rows+'</tbody><tfoot><tr><td colspan="3"><b>الإجمالي</b></td><td class="num"><b>'+fr(te)+'</b></td></tr></tfoot></table>' if e_all else '<p class="no-data">لا توجد دفعات مسجلة</p>'}"""

        html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Tajawal',sans-serif;background:#fdf8f2;color:#3d2c24;padding:20px 16px;direction:rtl;}}
.header{{text-align:center;margin-bottom:24px;padding:18px;background:linear-gradient(135deg,#f9c8d0,#fdf8f2);border-radius:14px;border:1px solid rgba(232,121,138,.25);}}
.header h1{{font-size:20px;font-weight:900;color:#c4566a;margin-bottom:3px;}}
.header p{{font-size:11px;color:#b09888;}}
.sum-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:20px;}}
.sum-card{{padding:14px 12px;border-radius:12px;text-align:center;border:1px solid rgba(0,0,0,.07);}}
.sum-card.span2{{grid-column:span 2;}}
.sum-card.green{{background:#e8f5e9;border-color:rgba(122,171,138,.3);}}
.sum-card.red{{background:#fce4ec;border-color:rgba(232,121,138,.3);}}
.sum-card.gold{{background:#fff8e1;border-color:rgba(212,165,87,.3);}}
.sum-card.blue{{background:#e3f2fd;border-color:rgba(100,150,200,.3);}}
.sum-ico{{font-size:18px;margin-bottom:4px;}}
.sum-val{{font-size:16px;font-weight:900;margin-bottom:2px;}}
.sum-val.big{{font-size:20px;}}
.green .sum-val{{color:#5a8a6a;}}.red .sum-val{{color:#c4566a;}}.gold .sum-val{{color:#d4a557;}}.blue .sum-val{{color:#4a7ab0;}}
.sum-lbl{{font-size:10px;color:#7a6458;line-height:1.5;}}
.sum-lbl span{{font-size:11px;font-weight:700;}}
.sec-title{{font-size:13px;font-weight:800;margin:20px 0 8px;padding:7px 12px;border-radius:8px;}}
.green-t{{background:rgba(122,171,138,.1);color:#5a8a6a;border-right:3px solid #7aab8a;}}
.red-t{{background:rgba(232,121,138,.1);color:#c4566a;border-right:3px solid #e8798a;}}
.gold-t{{background:rgba(212,165,87,.1);color:#d4a557;border-right:3px solid #d4a557;}}
.blue-t{{background:rgba(100,150,200,.1);color:#4a7ab0;border-right:3px solid #6a9fd0;}}
.cat-row{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;}}
.cat-chip{{background:rgba(122,171,138,.15);color:#5a8a6a;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;}}
.red-chip{{background:rgba(232,121,138,.15);color:#c4566a;}}
table{{width:100%;border-collapse:collapse;font-size:11px;margin-bottom:6px;}}
thead tr{{background:linear-gradient(135deg,#6b4c3b,#8b6c5b);color:white;}}
th{{padding:8px 8px;text-align:right;font-weight:700;font-size:11px;}}
td{{padding:7px 8px;border-bottom:1px solid rgba(107,76,59,.07);}}
tr.even td{{background:rgba(253,248,242,.7);}}
tfoot td{{font-weight:700;background:rgba(107,76,59,.05);border-top:2px solid rgba(107,76,59,.12);}}
.num{{text-align:left;font-weight:600;}}
.cnt{{text-align:center;color:#999;font-size:10px;}}
.chip{{background:rgba(107,76,59,.08);padding:2px 7px;border-radius:10px;font-size:10px;}}
.chip.pay{{background:rgba(122,171,138,.15);color:#5a8a6a;}}
.badge{{padding:2px 7px;border-radius:10px;font-size:10px;font-weight:700;}}
.badge.paid{{background:rgba(122,171,138,.2);color:#5a8a6a;}}
.badge.unpaid{{background:rgba(232,121,138,.12);color:#c4566a;}}
.sub-h{{font-size:12px;color:#7a6458;margin:14px 0 6px;font-weight:700;}}
.no-data{{color:#b09888;font-size:11px;text-align:center;padding:10px;}}
.print-btn{{position:fixed;bottom:18px;left:16px;background:linear-gradient(135deg,#e8798a,#c4566a);color:white;border:none;padding:11px 20px;border-radius:40px;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 4px 16px rgba(232,121,138,.4);}}
@media print{{.print-btn{{display:none;}}body{{background:white;padding:8px;}}}}
</style>
</head>
<body>
<div class="header">
  <h1>🌹 فيروز فلورز</h1>
  <p>تقرير {type_labels.get(rtype,rtype)} — {period_label} &nbsp;|&nbsp; {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
</div>
{summary_html}
{daily_html}
{sales_html}
{buys_html}
{exps_html}
<button class="print-btn" onclick="window.print()">🖨️ طباعة / PDF</button>
</body></html>"""

        return Response(html, mimetype="text/html; charset=utf-8")

    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route("/api/expense_entries")
def api_list_expense_entries():
    """List all expense entries."""
    month_val = request.args.get("month", "")
    if month_val:
        entries = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month_val,))
    else:
        entries = db_get("SELECT * FROM entries WHERE type='expense' ORDER BY created DESC LIMIT 50")
    return jsonify(entries)

# ── Flowers API ──────────────────────────────────────────
@app.route("/api/flowers")
def api_get_flowers():
    flowers = db_get("SELECT * FROM flowers ORDER BY count DESC")
    total = sum(f["count"] for f in flowers)
    updated = flowers[0]["updated"] if flowers else None
    return jsonify({"flowers": flowers, "total": total, "updated": updated})

@app.route("/api/flowers", methods=["POST"])
def api_set_flowers():
    """Save flower inventory from AI scan."""
    d = request.json
    flowers = d.get("flowers", [])
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    db_run("DELETE FROM flowers")
    for f in flowers:
        db_run("INSERT INTO flowers (name, count, unit, updated) VALUES (?,?,?,?)",
               (f["name"], int(f["count"]), f.get("unit","وردة"), now))
    return jsonify({"ok": True, "count": len(flowers)})

@app.route("/api/flowers/<int:fid>", methods=["DELETE"])
def api_del_flower(fid):
    db_run("DELETE FROM flowers WHERE id=?", (fid,))
    return jsonify({"ok": True})

@app.route("/api/flowers/<int:fid>", methods=["POST"])
def api_update_flower(fid):
    d = request.json
    if "unit" in d:
        db_run("UPDATE flowers SET count=?,unit=? WHERE id=?", (int(d["count"]), d["unit"], fid))
    else:
        db_run("UPDATE flowers SET count=? WHERE id=?", (int(d["count"]), fid))
    return jsonify({"ok": True})

@app.route("/fix_elec")
def fix_elec():
    """Fix duplicate electricity expenses."""
    try:
        db_run("UPDATE expenses SET name='تعبئة كهرباء', amount=0 WHERE name='فاتورة الكهرباء'")
        db_run("UPDATE entries SET desc='تعبئة كهرباء' WHERE desc='فاتورة الكهرباء'")
        # Remove duplicates - keep only first one
        all_elec = db_get("SELECT * FROM expenses WHERE name='تعبئة كهرباء' ORDER BY id")
        if len(all_elec) > 1:
            for dup in all_elec[1:]:
                db_run("DELETE FROM expenses WHERE id=?", (dup["id"],))
        result = db_get("SELECT * FROM expenses ORDER BY id")
        return jsonify({"ok": True, "expenses": result})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/fix_expenses")
def fix_expenses():
    """Remove duplicate expenses keeping only latest per name."""
    try:
        all_exp = db_get("SELECT * FROM expenses ORDER BY id")
        seen = {}
        to_delete = []
        for e in all_exp:
            if e["name"] in seen:
                to_delete.append(e["id"])
            else:
                seen[e["name"]] = e["id"]
        for eid in to_delete:
            db_run("DELETE FROM expenses WHERE id=?", (eid,))
        remaining = db_get("SELECT * FROM expenses ORDER BY id")
        return jsonify({"ok": True, "deleted": len(to_delete), "remaining": remaining})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/init_shelves")
def init_shelves():
    shelves = [
        ('ريحان','#f07090',10),
        ('فتحية','#4ecdc4',8),
        ('فطوم','#b794f4',8),
        ('اكسسوارات','#f5c842',18),
    ]
    results = []
    for name, color, rent in shelves:
        existing = db_one("SELECT id FROM shelves WHERE name=?", (name,))
        if existing:
            db_run("UPDATE shelves SET color=?, rent=? WHERE name=?", (color, rent, name))
            results.append(f"updated: {name}")
        else:
            db_run("INSERT INTO shelves (name,color,rent) VALUES (?,?,?)", (name, color, rent))
            results.append(f"inserted: {name}")
    all_shelves = db_get("SELECT * FROM shelves")
    return jsonify({"ok": True, "results": results, "shelves": all_shelves})

@app.route("/api/backup")
def api_backup():
    """Export all data as JSON."""
    try:
        entries = db_get("SELECT * FROM entries ORDER BY created")
        shelves = db_get("SELECT * FROM shelves ORDER BY id")
        products = db_get("SELECT * FROM shelf_products ORDER BY id")
        data = {
            "version": 1,
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "entries": entries,
            "shelves": shelves,
            "shelf_products": products
        }
        import json as _json
        response = Response(
            _json.dumps(data, ensure_ascii=False, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": f"attachment; filename=fairuz_backup_{datetime.now().strftime('%Y%m%d')}.json"}
        )
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/restore", methods=["POST"])
def api_restore():
    """Restore data from JSON backup."""
    try:
        data = request.json
        if not data or data.get("version") != 1:
            return jsonify({"error": "ملف غير صالح"}), 400

        restored = {"entries": 0, "shelves": 0, "products": 0}

        # Restore shelves
        for s in data.get("shelves", []):
            existing = db_one("SELECT id FROM shelves WHERE name=?", (s["name"],))
            if existing:
                db_run("UPDATE shelves SET color=?, rent=? WHERE name=?",
                       (s.get("color","#e8547a"), s.get("rent",0), s["name"]))
            else:
                db_run("INSERT INTO shelves (name,color,rent) VALUES (?,?,?)",
                       (s["name"], s.get("color","#e8547a"), s.get("rent",0)))
            restored["shelves"] += 1

        # Restore entries
        for e in data.get("entries", []):
            existing = db_one("SELECT id FROM entries WHERE id=?", (e["id"],))
            if not existing:
                db_run("""INSERT INTO entries (type,desc,amt,date,month,img,paid_by,payment_method,sale_time,shelf_id)
                          VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (e["type"], e["desc"], e["amt"], e["date"], e["month"],
                     e.get("img"), e.get("paid_by"), e.get("payment_method"),
                     e.get("sale_time"), e.get("shelf_id")))
                restored["entries"] += 1

        # Restore shelf products
        for p in data.get("shelf_products", []):
            existing = db_one("SELECT id FROM shelf_products WHERE id=?", (p["id"],))
            if not existing:
                db_run("INSERT INTO shelf_products (shelf_id,name,price,qty) VALUES (?,?,?,?)",
                       (p["shelf_id"], p["name"], p["price"], p.get("qty",0)))
                restored["products"] += 1

        return jsonify({"ok": True, "restored": restored})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/daily_summary")
def daily_summary():
    """Send daily summary to Telegram. Call this via cron at 10pm."""
    if not BOT_TOKEN:
        return jsonify({"error": "No BOT_TOKEN"})
    chat_id = request.args.get("chat_id") or os.environ.get("OWNER_CHAT_ID","")
    if not chat_id:
        return jsonify({"error": "No chat_id. Add OWNER_CHAT_ID to Render env or pass ?chat_id=xxx"})
    try:
        today = datetime.now().strftime("%d/%m/%Y")
        month = cur_month()
        rows = db_get("SELECT * FROM entries WHERE date=? AND month=? ORDER BY created DESC", (today, month))
        sales = [r for r in rows if r["type"]=="s"]
        buys  = [r for r in rows if r["type"]=="b"]
        exps  = [r for r in rows if r["type"]=="expense"]
        ts = sum(e["amt"] for e in sales)
        tb = sum(e["amt"] for e in buys)
        te = sum(e["amt"] for e in exps)
        if not sales and not buys and not exps:
            msg = f"🌙 <b>ملخص يوم {today}</b>\n\n😴 لا توجد حركات اليوم"
        else:
            msg = (f"🌙 <b>ملخص يوم {today}</b>\n\n"
                   f"🌸 مبيعات: {fmt_omr(ts)} ({len(sales)} عملية)\n"
                   f"📦 مشتريات: {fmt_omr(tb)} ({len(buys)} عملية)\n"
                   f"💸 مصاريف: {fmt_omr(te)}\n"
                   f"━━━━━━\n"
                   f"{'✅' if ts-tb-te>=0 else '⚠️'} صافي اليوم: {fmt_omr(ts-tb-te)}")
        tg(chat_id, msg)
        return jsonify({"ok": True, "sent": msg[:50]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/set_webhook")
def set_webhook():
    host = request.host_url.rstrip("/").replace("http://", "https://")
    r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
                     params={"url": f"{host}/webhook"}, timeout=10)
    return jsonify(r.json())

# ── Flower Invoices API ───────────────────────────────────
@app.route("/api/flower_invoices")
@auth
def api_get_flower_invoices():
    m = request.args.get("month", cur_month())
    invs = db_get("SELECT * FROM flower_invoices WHERE month=? ORDER BY inv_date DESC", (m,))
    for inv in invs:
        try: inv["items"] = json.loads(inv["items"] or "[]")
        except: inv["items"] = []
    total = sum(float(i["total"]) for i in invs)
    paid_invs = [i for i in invs if i.get("is_paid")]
    unpaid_invs = [i for i in invs if not i.get("is_paid")]
    months = db_get("SELECT DISTINCT month FROM flower_invoices ORDER BY month DESC")
    return jsonify({"invoices": invs, "total": total, "month": m,
                    "months": [r["month"] for r in months],
                    "paid_total": sum(float(i["total"]) for i in paid_invs),
                    "unpaid_total": sum(float(i["total"]) for i in unpaid_invs),
                    "paid_count": len(paid_invs),
                    "unpaid_count": len(unpaid_invs)})

@app.route("/api/flower_invoices/<int:iid>/toggle_paid", methods=["POST"])
@auth
def api_toggle_flower_invoice_paid(iid):
    inv = db_one("SELECT * FROM flower_invoices WHERE id=?", (iid,))
    if not inv:
        return jsonify({"ok": False, "error": "not found"}), 404
    new_val = 0 if inv.get("is_paid") else 1
    db_run("UPDATE flower_invoices SET is_paid=? WHERE id=?", (new_val, iid))
    return jsonify({"ok": True, "is_paid": new_val})

@app.route("/api/flower_invoices/<int:iid>", methods=["DELETE"])
@auth
def api_del_flower_invoice(iid):
    db_run("DELETE FROM flower_invoices WHERE id=?", (iid,))
    return jsonify({"ok": True})

@app.route("/api/flower_invoices", methods=["POST"])
@worker_auth
def api_add_flower_invoice():
    d = request.json or {}
    company      = d.get("company","").strip() or "غير محدد"
    # توحيد اسم الشركة Title Case
    company      = " ".join(w.capitalize() for w in company.split()) if company else "غير محدد"
    invoice_number = d.get("invoice_number") or None
    inv_date     = d.get("inv_date", datetime.now().strftime("%d/%m/%Y"))
    try: inv_month = datetime.strptime(inv_date,"%d/%m/%Y").strftime("%Y-%m")
    except: inv_month = cur_month()
    total        = float(d.get("total",0))
    # تصحيح المبالغ: 4 أرقام صحيحة → كسر عشري
    if total == int(total) and total >= 1000:
        total = total / 1000.0
    raw_items = d.get("items",[])
    for item in raw_items:
        for key in ("unit_price","line_total"):
            try:
                v = float(item.get(key,0))
                if v == int(v) and v >= 1000:
                    item[key] = round(v / 1000.0, 3)
            except: pass
    items = json.dumps(raw_items, ensure_ascii=False)
    db_run("INSERT INTO flower_invoices (company,invoice_number,inv_date,month,total,items) VALUES (?,?,?,?,?,?)",
           (company, invoice_number, inv_date, inv_month, total, items))
    return jsonify({"ok": True})

@app.route("/api/flower_invoices/scan", methods=["POST"])
@auth
def api_scan_flower_invoice():
    """قراءة صورة فاتورة ورد مرفوعة (multipart أو base64 JSON) وحفظها تلقائياً."""
    import base64 as _b64
    try:
        # دعم الرفع بـ base64 JSON أو multipart
        if request.is_json:
            b64 = request.json.get("image","")
            mime = "image/jpeg"
            if not b64:
                return jsonify({"error": "لم يتم إرسال صورة"}), 400
        elif "file" in request.files:
            f = request.files["file"]
            if not f.filename:
                return jsonify({"error": "ملف غير صالح"}), 400
            img_bytes = f.read()
            b64 = _b64.b64encode(img_bytes).decode()
            mime = f.content_type or "image/jpeg"
        else:
            return jsonify({"error": "لم يتم رفع ملف"}), 400
        if not GROQ_KEY:
            return jsonify({"error": "GROQ_API_KEY غير مضبوط"}), 500
        prompt = """This is a flower supplier invoice (may be handwritten, in Arabic or English). Extract ALL data carefully.
Return ONLY a valid JSON object — no explanation, no markdown:
{"invoice_number":"INV-001 or null","company":"supplier name","date":"date as written","items":[{"name":"flower name","count":10,"unit":"وردة","unit_price":0.500,"line_total":5.000}],"total":25.500,"found":true}
Rules: invoice_number from header (null if absent). unit: "بندلة" for gypsophila/جبسون/limonium/ليموناي, else "وردة". found:false if not a flower invoice."""
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages": [{"role": "user", "content": [
                      {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                      {"type": "text", "text": prompt}
                  ]}],
                  "max_tokens": 1200, "temperature": 0}, timeout=35)
        resp = res.json()
        if "error" in resp:
            return jsonify({"error": str(resp["error"])}), 500
        raw = resp["choices"][0]["message"]["content"]
        raw = re.sub(r"```json\s*","",raw); raw = re.sub(r"```\s*","",raw).strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return jsonify({"error": "ما قدرت أقرأ الفاتورة، جرب صورة أوضح"}), 422
        data = json.loads(match.group())
        data = _normalize_invoice_data(data)
        if not data.get("found"):
            return jsonify({"error": "الصورة لا تبدو فاتورة ورد"}), 422
        company = data.get("company","").strip() or "غير محدد"
        invoice_number = data.get("invoice_number") or None
        std_date = data.get("date","").strip()
        if std_date:
            try:
                dt = datetime.strptime(std_date, "%Y-%m-%d")
                inv_date_display = dt.strftime("%d/%m/%Y"); inv_month = dt.strftime("%Y-%m")
            except:
                inv_date_display = std_date; inv_month = cur_month()
        else:
            inv_date_display = datetime.now().strftime("%d/%m/%Y"); inv_month = cur_month()
        items = data.get("items", [])
        total = float(data.get("total") or 0) or sum(float(i.get("line_total",0)) for i in items)
        items_json = json.dumps(items, ensure_ascii=False)
        db_run("INSERT INTO flower_invoices (company,invoice_number,inv_date,month,total,items) VALUES (?,?,?,?,?,?)",
               (company, invoice_number, inv_date_display, inv_month, total, items_json))
        return jsonify({"ok": True, "company": company, "inv_date": inv_date_display,
                        "total": total, "items": items, "invoice_number": invoice_number})
    except Exception as e:
        print("scan flower invoice error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/flowers/scan", methods=["POST"])
@auth
def api_scan_flowers():
    """تحليل صورة الورد وإرجاع عدد كل نوع تلقائياً."""
    import base64 as _b64
    try:
        b64 = request.json.get("image","")
        if not b64:
            return jsonify({"error": "لم يتم إرسال صورة"}), 400
        if not GROQ_KEY:
            return jsonify({"error": "GROQ_API_KEY غير مضبوط"}), 500
        prompt = """This is a photo of flowers in a flower shop. Count each type of flower visible.
Return ONLY a valid JSON object — no explanation, no markdown:
{"flowers":[{"name":"ورد أحمر","count":20,"unit":"وردة"},{"name":"ورد أبيض","count":15,"unit":"وردة"}],"found":true}
Flower name must be one of: ورد أحمر, ورد وردي, ورد أبيض, ورد أصفر, ورد برتقالي, ورد بنفسجي, جبسون (بندلة), ليموناي (بندلة).
unit: "بندلة" for جبسون/ليموناي, else "وردة". Only include flowers you can see. found:false if no flowers visible."""
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages": [{"role": "user", "content": [
                      {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                      {"type": "text", "text": prompt}
                  ]}],
                  "max_tokens": 600, "temperature": 0}, timeout=35)
        resp = res.json()
        if "error" in resp:
            return jsonify({"error": str(resp["error"])}), 500
        raw = resp["choices"][0]["message"]["content"]
        raw = re.sub(r"```json\s*","",raw); raw = re.sub(r"```\s*","",raw).strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return jsonify({"error": "ما قدرت أحلل الصورة"}), 422
        data = json.loads(match.group())
        if not data.get("found"):
            return jsonify({"error": "ما شُفت ورد في الصورة، أدخل العدد يدوياً"}), 422
        return jsonify({"ok": True, "flowers": data.get("flowers", [])})
    except Exception as e:
        print("scan flowers error:", e)
        return jsonify({"error": str(e)}), 500

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=False)


# ── Theme & Settings API ──────────────────────────────────

@app.route("/api/theme")
def api_get_theme():
    """إرجاع الثيم المحفوظ من قاعدة البيانات."""
    try:
        row = db_one("SELECT value FROM app_settings WHERE key='theme'")
        theme = row["value"] if row else "rose"
    except Exception:
        theme = "rose"
    return jsonify({"theme": theme})

@app.route("/api/theme", methods=["POST"])
@auth
def api_set_theme():
    """حفظ الثيم المختار."""
    d = request.json or {}
    theme = d.get("theme", "rose")
    valid = {"rose", "bloom", "ocean", "forest", "gold", "lavender"}
    if theme not in valid:
        theme = "rose"
    try:
        db_run(
            "INSERT INTO app_settings (key,value) VALUES ('theme',?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (theme,)
        )
    except Exception as e:
        print("theme save error:", e)
    return jsonify({"ok": True, "theme": theme})

@app.route("/api/theme/reset", methods=["POST"])
@auth
def api_reset_theme():
    """إعادة الثيم للأصلي (وردي)."""
    try:
        db_run(
            "INSERT INTO app_settings (key,value) VALUES ('theme','rose') "
            "ON CONFLICT(key) DO UPDATE SET value='rose'"
        )
    except Exception as e:
        print("theme reset error:", e)
    return jsonify({"ok": True, "theme": "rose"})

@app.route("/api/bg-image")
def api_bg_image():
    """إرجاع صورة الخلفية مع Cache headers لتخفيف الحمل."""
    import os as _os
    bg_path = "background.jpg"
    if not _os.path.exists(bg_path):
        return jsonify({"error": "not found"}), 404
    mtime = int(_os.path.getmtime(bg_path))
    etag = str(mtime)
    if request.headers.get("If-None-Match") == etag:
        return Response(status=304)
    with open(bg_path, "rb") as f:
        data = f.read()
    resp = Response(data, mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "public, max-age=86400"
    resp.headers["ETag"] = etag
    return resp
