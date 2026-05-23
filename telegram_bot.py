from config import *
from database import db_get, db_one, db_run
from helpers import cur_month
from helpers import fmt_omr, get_month_data, month_summary, get_day_data, day_summary, format_day_report, format_month_report

def tg(chat_id, text):
    if not BOT_TOKEN: return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id":chat_id,"text":text,"parse_mode":"HTML"}, timeout=10)
    except: pass

def tg_buttons(chat_id, text, buttons):
    if not BOT_TOKEN: return
    kb={"inline_keyboard":[[{"text":b["label"],"callback_data":b["data"]} for b in row] for row in buttons]}
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id":chat_id,"text":text,"parse_mode":"HTML","reply_markup":kb}, timeout=10)
    except: pass

def tg_sale_confirm(chat_id, text, entry_id):
    """رسالة تأكيد مبيعة مع زر حذف"""
    if not BOT_TOKEN: return
    kb = {"inline_keyboard":[[{"text":"🗑️ حذف هذه المبيعة","callback_data":f"del_entry:{entry_id}"}]]}
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id":chat_id,"text":text,"parse_mode":"HTML","reply_markup":kb}, timeout=10)
    except: pass

SALE_WORDS=["بعت","مبيعة","بيع","بعثت","باعت"]
BUY_WORDS=["اشتريت","شريت","مشتريات","شراء","دفعت","فاتورة","طلبية"]

CATEGORIES = {
    "طباعة": ["طباعة","طابعة","3d","ثري دي","ثلاثية","طباعه"],
    "تاجات": ["تاج","تاجات","كراون","crown"],
    "ورد وباقات": ["ورد","باقة","باقه","وردة","زهور","زهرة","بوكيه","بوكيه"],
    "عطور": ["عطر","عطور","برفان","perfume","بخور"],
    "اكسسوارات": ["اكسسوار","اكسسوارات","خاتم","سوار","عقد","قلادة","حلق"],
    "هدايا": ["هدية","هدايا","gift","تغليف","تغليفه"],
    "تجفيف": ["مجفف","مجففة","dried","ورد مجفف"],
    "صناعي": ["صناعي","اصطناعي","فوم","foam"],
}

def detect_category(text):
    text_lower = text.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text_lower:
                return cat
    return None

# كلمات الكميات بالعربي
QTY_WORDS = {
    "واحد":1,"واحده":1,"وحده":1,
    "اثنين":2,"اثنتين":2,"ثنتين":2,"اتنين":2,"باقتين":2,"تاجين":2,"عطرين":2,"قطعتين":2,"وردتين":2,"هديتين":2,"طباعتين":2,"ساعتين":2,"خاتمين":2,"سوارين":2,
    "ثلاث":3,"ثلاثة":3,"ثلث":3,
    "أربع":4,"اربع":4,"أربعة":4,"اربعة":4,
    "خمس":5,"خمسة":5,
    "ست":6,"ستة":6,
    "سبع":7,"سبعة":7,
    "ثمان":8,"ثمانية":8,
    "تسع":9,"تسعة":9,
    "عشر":10,"عشرة":10,
}

def detect_qty_from_text(text):
    """استخراج الكمية من النص العربي"""
    text_lower = text.strip()
    # أولاً: ابحث عن رقم + وحدة مثل "3 باقات"
    import re as _re
    m = _re.search(r'(\d+)\s*(باقة|باقات|تاج|تيجان|عطر|عطور|قطعة|قطع|وردة|ورود|هدية|هدايا|ساعة|ساعات|خاتم|خواتم|سوار|أساور)', text_lower)
    if m:
        return int(m.group(1))
    # ثانياً: ابحث عن كلمات الكمية
    for word, n in QTY_WORDS.items():
        if word in text_lower:
            return n
    return 1

def parse_text(text):
    text=text.strip()
    etype=None
    for w in SALE_WORDS:
        if w in text: etype="s"; break
    if not etype:
        for w in BUY_WORDS:
            if w in text: etype="b"; break
    amt=None
    for pat in [r'الإجمالي[^\d]*(\d+[.,]\d+)',r'Net Total[^\d]*(\d+[.,]\d+)',r'بـ\s*(\d+[.,]\d+)',r'بـ\s*(\d+)']:
        m=re.search(pat,text)
        if m:
            try: amt=float(m.group(1).replace(',','.')); break
            except: pass
    if not amt:
        nums=re.findall(r'\d+[.,]\d+|\d+',text)
        candidates=[float(n.replace(',','.')) for n in nums if float(n.replace(',','.'))>0]
        if candidates: amt=max(candidates)
    if etype and amt:
        first=text.split("\n")[0].strip()
        desc=first
        for w in SALE_WORDS+BUY_WORDS+["بـ","ب","ريال","ر.ع","اغراض","أغراض"]:
            desc=desc.replace(w," ")
        desc=re.sub(r'\d+(?:[.,]\d+)?','',desc).strip()
        desc=' '.join(desc.split()) or ("مبيعة" if etype=="s" else "مشتريات")
        return {"type":etype,"desc":desc,"amt":amt,"found":True}
    return {"found":False}

def groq_chat(text, chat_id):
    """ذكاء اصطناعي كامل — يفهم أي كلام ويقرر الإجراء المناسب"""
    if not GROQ_KEY:
        return None
    try:
        today = datetime.now().strftime("%d/%m/%Y")
        cur_m = cur_month()
        # نجيب بيانات الشهر الحالي للسياق
        s, b = get_month_data(cur_m)
        ts = sum(e["amt"] for e in s)
        tb = sum(e["amt"] for e in b if e["type"] != "expense")
        exps_list = db_get("SELECT name, amount, last_paid FROM expenses ORDER BY id")
        shelves = db_get("SELECT name FROM shelves ORDER BY id")
        exp_names = ", ".join(f"{e['name']} ({fmt_omr(e['amount'])})" for e in exps_list)
        shelf_names = ", ".join(s2["name"] for s2 in shelves)

        # نجيب منتجات الرفوف للسياق
        shelf_products_ctx = ""
        try:
            shelves_with_prods = []
            for sh in db_get("SELECT * FROM shelves ORDER BY id"):
                prods = db_get("SELECT name,price,qty FROM shelf_products WHERE shelf_id=? AND qty>0 ORDER BY name", (sh["id"],))
                if prods:
                    prod_list = ", ".join(f"{p['name']} ({fmt_omr(p['price'])})" for p in prods)
                    shelves_with_prods.append(f"رف {sh['name']}: {prod_list}")
            shelf_products_ctx = "\n".join(shelves_with_prods) if shelves_with_prods else "لا توجد منتجات"
        except:
            shelf_products_ctx = ""

        system = f"""أنت مساعد ذكي لمحل فيروز فلورز لبيع الزهور في عُمان.
اليوم: {today} | الشهر الحالي: {cur_m}
إجمالي مبيعات هذا الشهر: {fmt_omr(ts)} ({len(s)} عملية)
إجمالي مشتريات هذا الشهر: {fmt_omr(tb)} ({len(b)} عملية)
المصاريف الثابتة: {exp_names}
الرفوف: {shelf_names}
منتجات الرفوف المتاحة:
{shelf_products_ctx}

مهمتك: حلل رسالة المستخدم وأخرج JSON فقط بهذا الشكل:

{{
  "action": "register_sale" | "register_buy" | "register_expense" | "answer" | "report" | "unknown",
  "data": {{...}},
  "reply": "رد نصي للمستخدم إذا action=answer"
}}

قواعد كل action:
- register_sale: مبيعة → data: {{desc, amt, qty, payment, category, shelf}}
  - desc: اسم المنتج المفرد (مثل "باقة ورد" لا "باقتين")
  - amt: السعر الإجمالي لكل الكميات (كما ذُكر)
  - qty: الكمية (افتراضي 1). استخرجها من: "باقتين"=2، "ثلاث"=3، "أربع"=4، "3 باقات"=3 إلخ
  - إذا كان البيع من رف، ضع اسم الرف في shelf وضع اسم المنتج في desc
  - المبلغ amt: إذا ذُكر صراحة خذه، وإلا اتركه 0
- register_buy: مشتريات → data: {{desc, amt, qty, paid_by}}
- register_expense: مصروف → data: {{expense_name, amt}}
- answer: سؤال أو كلام عام → data: {{}} + reply بالعربي
- report: طلب تقرير → data: {{period: "today"|"month"|"custom"}}

تصنيفات المبيعات: ورد وباقات, طباعة, تاجات, عطور, اكسسوارات, هدايا, تجفيف, صناعي, أخرى
طرق الدفع: "كاش 💵" أو "فيزا 💳" أو "تحويل 🏦" أو null
المبالغ: أرقام عشرية مثل 5.5 أو 12.0

أمثلة:
"بعت باقة بـ 5.5 كاش" → {{"action":"register_sale","data":{{"desc":"باقة ورد","amt":5.5,"qty":1,"payment":"كاش 💵","category":"ورد وباقات"}}}}
"بعت باقتين بـ 8" → {{"action":"register_sale","data":{{"desc":"باقة ورد","amt":8.0,"qty":2,"payment":null,"category":"ورد وباقات"}}}}
"بعت 3 باقات بـ 12 كاش" → {{"action":"register_sale","data":{{"desc":"باقة ورد","amt":12.0,"qty":3,"payment":"كاش 💵","category":"ورد وباقات"}}}}
"بعت تاجين بـ 6 فيزا" → {{"action":"register_sale","data":{{"desc":"تاج","amt":6.0,"qty":2,"payment":"فيزا 💳","category":"تاجات"}}}}
"بعت عطر من رف ريحان" → {{"action":"register_sale","data":{{"desc":"عطر","amt":0,"qty":1,"payment":null,"shelf":"ريحان"}}}}
"بعت عطرين من رف ريحان" → {{"action":"register_sale","data":{{"desc":"عطر","amt":0,"qty":2,"payment":null,"shelf":"ريحان"}}}}
"بعت ثلاث عطور من رف ريحان بـ 15 كاش" → {{"action":"register_sale","data":{{"desc":"عطر","amt":15.0,"qty":3,"payment":"كاش 💵","shelf":"ريحان"}}}}
"بعت ساعة من رف فتحية بـ 8 كاش" → {{"action":"register_sale","data":{{"desc":"ساعة","amt":8.0,"qty":1,"payment":"كاش 💵","shelf":"فتحية"}}}}
"بعت ساعتين من رف فتحية" → {{"action":"register_sale","data":{{"desc":"ساعة","amt":0,"qty":2,"payment":null,"shelf":"فتحية"}}}}
"اشتريت ورد 12 ريال" → {{"action":"register_buy","data":{{"desc":"ورد","amt":12.0,"qty":1,"paid_by":null}}}}
"دفعت الراتب" → {{"action":"register_expense","data":{{"expense_name":"راتب العامل","amt":null}}}}
"كم مبيعات اليوم؟" → {{"action":"answer","data":{{}},"reply":"مبيعات اليوم..."}}
"كيف الأرباح هذا الشهر؟" → {{"action":"report","data":{{"period":"month"}}}}
"مرحبا" → {{"action":"answer","data":{{}},"reply":"أهلاً! كيف أقدر أساعدك اليوم؟"}}

أخرج JSON فقط بدون شرح:"""

        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": text}
                ],
                "max_tokens": 300,
                "temperature": 0.1
            }, timeout=12)
        raw = res.json()["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```json\s*", "", raw)
        raw = re.sub(r"```\s*", "", raw)
        raw = raw.strip()
        return json.loads(raw)
    except Exception as e:
        print(f"groq_chat error: {e}")
        return None

def groq_parse_text(text):
    """fallback بسيط لو Groq ما شتغل"""
    if not GROQ_KEY:
        return parse_text(text)
    result = groq_chat(text, None)
    if not result:
        return parse_text(text)
    action = result.get("action","unknown")
    data = result.get("data",{})
    if action == "register_sale":
        return {"found":True,"type":"s","desc":data.get("desc","مبيعة"),"amt":data.get("amt",0),"payment":data.get("payment"),"category":data.get("category"),"shelf":data.get("shelf")}
    elif action == "register_buy":
        return {"found":True,"type":"b","desc":data.get("desc","مشتريات"),"amt":data.get("amt",0),"paid_by":data.get("paid_by")}
    elif action == "register_expense":
        return {"found":True,"type":"expense","desc":data.get("expense_name","مصروف"),"amt":data.get("amt",0),"expense_name":data.get("expense_name")}
    return {"found":False}

def groq_count_flowers(file_id):
    """Use Groq to count and identify flowers in image."""
    if not GROQ_KEY or not BOT_TOKEN: return None
    try:
        import base64
        r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
                        params={"file_id": file_id}, timeout=10)
        fp = r.json()["result"]["file_path"]
        img = requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}", timeout=15).content
        b64 = base64.b64encode(img).decode()
        prompt = 'Count and identify all flowers in this image. For each flower type, count stems/flowers. Some flowers come in bundles (like gypsophila/baby\'s breath = بندلة). Reply ONLY with JSON array: [{"name":"روز أحمر","count":5,"unit":"وردة"},{"name":"جبسون","count":2,"unit":"بندلة"}]. Use Arabic names. unit is "وردة" for individual stems, "بندلة" for bundle flowers.'
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages": [{"role": "user", "content": [
                      {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                      {"type": "text", "text": prompt}
                  ]}],
                  "max_tokens": 500, "temperature": 0}, timeout=30)
        resp = res.json()
        if "error" in resp:
            print("Groq flower error:", resp["error"]); return None
        raw = resp["choices"][0]["message"]["content"]
        import re as _re
        match = _re.search(r'\[.*?\]', raw, _re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        print("Groq flower error:", e); return None

def _normalize_invoice_data(data):
    """
    معالجة بيانات الفاتورة بعد استخراجها من الذكاء الاصطناعي:
    1. رقم الفاتورة: يُحفظ كما هو أو null
    2. اسم الشركة: Title Case
    3. المبالغ: 4 أرقام بدون فاصلة → كسر عشري (7200 → 7.200)
    4. التاريخ: أي صيغة → YYYY-MM-DD
    """
    import re as _re

    # ── 1. رقم الفاتورة ──────────────────────────────────────
    inv_no = data.get("invoice_number") or data.get("invoice_no") or data.get("inv_no")
    data["invoice_number"] = str(inv_no).strip() if inv_no else None

    # ── 2. توحيد اسم الشركة (Title Case) ────────────────────
    company = data.get("company") or ""
    if company:
        # Title Case مع الحفاظ على الأرقام والرموز
        data["company"] = " ".join(w.capitalize() for w in company.split())

    # ── 3. معالجة المبالغ (قاعدة الـ 3 خانات) ───────────────
    def fix_amount(val):
        """4 أرقام صحيحة بدون كسر → اقسم على 1000 (7200 → 7.200)"""
        if val is None:
            return 0.0
        try:
            f = float(val)
            # لو الرقم صحيح (بدون كسر) و≥ 1000 → نعتبره فلوس بالبيسة
            if f == int(f) and f >= 1000:
                f = f / 1000.0
            return round(f, 3)
        except:
            return 0.0

    # إجمالي الفاتورة
    data["total"] = fix_amount(data.get("total"))

    # أسعار وإجماليات الأصناف
    for item in data.get("items", []):
        item["unit_price"]  = fix_amount(item.get("unit_price"))
        item["line_total"]  = fix_amount(item.get("line_total"))
        # إعادة حساب line_total لو كان صفر وعندنا unit_price × count
        if item["line_total"] == 0 and item["unit_price"] > 0:
            try:
                item["line_total"] = round(item["unit_price"] * float(item.get("count", 0)), 3)
            except:
                pass

    # ── 4. توحيد التاريخ → YYYY-MM-DD ───────────────────────
    raw_date = data.get("date") or ""
    std_date = ""
    if raw_date:
        # جرب صيغ مختلفة
        patterns = [
            (r'(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})', '{}-{:02d}-{:02d}', lambda m: (int(m[0]), int(m[1]), int(m[2]))),  # YYYY-MM-DD
            (r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})',  '{}-{:02d}-{:02d}', lambda m: (int(m[2]), int(m[1]), int(m[0]))),  # DD/MM/YYYY
            (r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2})$', '{}-{:02d}-{:02d}', lambda m: (2000+int(m[2]), int(m[1]), int(m[0]))),  # DD/MM/YY
        ]
        for pat, fmt_str, extractor in patterns:
            m = _re.search(pat, raw_date)
            if m:
                try:
                    y, mo, d = extractor(m.groups())
                    std_date = f"{y}-{mo:02d}-{d:02d}"
                    break
                except:
                    pass
        if not std_date:
            std_date = raw_date  # لو فشل التحويل احتفظ بالأصل

    data["date"] = std_date
    return data


def groq_read_flower_supplier_invoice(file_id):
    """
    قراءة فاتورة مورد الورد من صورة عبر Groq Vision مع:
    - استخراج رقم الفاتورة
    - توحيد اسم الشركة (Title Case)
    - تصحيح المبالغ (قاعدة الـ 3 خانات)
    - توحيد التاريخ (YYYY-MM-DD)
    """
    if not GROQ_KEY or not BOT_TOKEN: return None
    try:
        import base64
        r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
                        params={"file_id": file_id}, timeout=10)
        fp = r.json()["result"]["file_path"]
        img = requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}", timeout=15).content
        b64 = base64.b64encode(img).decode()

        prompt = """This is a flower supplier invoice (may be handwritten, in Arabic or English). Extract ALL data carefully.

Return ONLY a valid JSON object — no explanation, no markdown:
{
  "invoice_number": "INV-2024-001 or null if not found",
  "company": "Supplier / company name exactly as written",
  "date": "date exactly as written on invoice (any format)",
  "items": [
    {"name": "flower name in Arabic", "count": 10, "unit": "وردة", "unit_price": 0.500, "line_total": 5.000}
  ],
  "total": 25.500,
  "found": true
}

Rules:
- invoice_number: look for "رقم الفاتورة", "Invoice No", "Invoice #", "ID", "Inv No". Keep original format (e.g. INV-2024-001). Set null if absent.
- company: extract from header, stamp, or any label. Preserve the name as-is; post-processing will normalize casing.
- date: copy the date exactly as printed — do NOT reformat it.
- unit: use "بندلة" for bundle flowers (gypsophila/جبسون, limonium/ليموناي, statice, etc.), otherwise "وردة".
- unit_price / line_total: if a number looks like 4 digits with no decimal (e.g. 7200), write it as-is and post-processing will fix it.
- total: grand total of the invoice.
- found: false if this is NOT a flower/plant invoice."""

        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages": [{"role": "user", "content": [
                      {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                      {"type": "text", "text": prompt}
                  ]}],
                  "max_tokens": 1200, "temperature": 0}, timeout=30)

        resp = res.json()
        if "error" in resp:
            print("Groq flower invoice error:", resp["error"]); return None

        raw = resp["choices"][0]["message"]["content"]
        # تنظيف markdown
        raw = re.sub(r"```json\s*", "", raw)
        raw = re.sub(r"```\s*", "", raw).strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return None

        data = json.loads(match.group())
        # تطبيق قواعد المعالجة الأربع
        return _normalize_invoice_data(data)

    except Exception as e:
        print("Groq flower invoice error:", e); return None

def groq_parse_flower_text(text):
    """Send bulk flower text to Groq to parse into structured list."""
    if not GROQ_KEY: return None
    try:
        prompt = f"""أنت خبير في تصنيف الورود. المستخدم أرسل قائمة ورود. حوّلها إلى JSON منظّم.
قواعد مهمة:
- استخرج كل نوع ورد مع عدده ووحدته
- الوحدات المتاحة: "وردة" للورود الفردية، "بندلة" للورود التي تجي في حزم (مثل جبسون، ايوروبسم، ليموناي)
- إذا ذكر "بندلة" أو "بنادل" أو "حزمة" استخدم unit: "بندلة"
- اللون جزء من الاسم (مثل: "روز أحمر" ← name: "روز أحمر")
- رد فقط بـ JSON array هكذا بدون أي كلام آخر:
[{{"name":"روز أحمر","count":20,"unit":"وردة"}},{{"name":"دوار الشمس","count":6,"unit":"وردة"}},{{"name":"جبسون","count":3,"unit":"بندلة"}}]

النص المُرسل:
{text}"""
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 800, "temperature": 0}, timeout=20)
        resp = res.json()
        if "error" in resp:
            print("Groq flower text error:", resp["error"]); return None
        raw = resp["choices"][0]["message"]["content"]
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        print("Groq flower text error:", e); return None

def groq_read_invoice(file_id):
    if not GROQ_KEY or not BOT_TOKEN: return None
    try:
        import base64
        r=requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",params={"file_id":file_id},timeout=10)
        fp=r.json()["result"]["file_path"]
        img=requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}",timeout=15).content
        b64=base64.b64encode(img).decode()
        prompt = 'This is a receipt/invoice. Extract total amount, description, and if it is an electricity bill. Reply ONLY with JSON like: {"amt":3.52,"desc":"shop name","is_electricity":false,"found":true}'
        res=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages":[{"role":"user","content":[
                      {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
                      {"type":"text","text":prompt}
                  ]}],
                  "max_tokens":300,"temperature":0},timeout=25)
        resp = res.json()
        if "error" in resp:
            print("Groq API error:", resp["error"])
            return None
        raw = resp["choices"][0]["message"]["content"]
        import re as _re
        match = _re.search(r'\{.*?\}', raw, _re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw.replace("```json","").replace("```","").strip())
    except Exception as e:
        print("Groq error:", e)
        return None

def generate_caption(file_id, style=""):
    """توليد كابشن تسويقي للصورة بالذكاء الاصطناعي — يدعم Groq Vision + Gemini Vision"""
    import base64, re as _re
    try:
        r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
                         params={"file_id": file_id}, timeout=10)
        fp = r.json()["result"]["file_path"]
        img = requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}", timeout=15).content
        b64 = base64.b64encode(img).decode()
    except Exception as e:
        print("Caption: image download error:", e)
        return None

    style_map = {
        "رومانسي": "رومانسي وعاطفي يناسب باقات الأزواج والمناسبات الرومانسية",
        "رسمي":    "رسمي وأنيق يناسب الفعاليات والتهاني الرسمية",
        "مرح":     "مرح وخفيف يناسب الأعياد والمفاجآت",
        "عيد":     "مناسب للأعياد والمناسبات الدينية، دافئ ومحتفل",
    }
    style_desc = style_map.get(style, "راقٍ وجذاب يناسب محل ورد فاخر")

    prompt = f"""أنت خبير تسويق رقمي لمحل ورد فاخر اسمه "فيروز فلورز" في عُمان.
انظر إلى هذه الصورة واكتب كابشن {style_desc} للنشر على انستغرام وواتساب.

المتطلبات:
- باللغة العربية الفصيحة أو الخليجية اللطيفة
- من سطرين إلى أربعة أسطر كحد أقصى
- يبدأ بجملة تشويقية مؤثرة
- يحتوي على إيموجي مناسبة (2-3 كحد أقصى)
- في النهاية هاشتاق واحد أو اثنين مناسبين لعُمان
- لا تذكر الأسعار

اكتب الكابشن فقط بدون أي شرح إضافي."""

    # 1. Groq Vision
    if GROQ_KEY:
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
                json={"model": "meta-llama/llama-4-scout-17b-16e-instruct",
                      "messages": [{"role": "user", "content": [
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                          {"type": "text", "text": prompt}
                      ]}],
                      "max_tokens": 300, "temperature": 0.85}, timeout=25)
            txt = res.json()["choices"][0]["message"]["content"].strip()
            if txt: return txt
        except Exception as e:
            print("Caption Groq error:", e)

    # 2. Gemini Vision
    if GEMINI_KEY:
        try:
            body = {"contents": [{"parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
                {"text": prompt}
            ]}], "generationConfig": {"maxOutputTokens": 300, "temperature": 0.85}}
            res = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}",
                headers={"Content-Type": "application/json"}, json=body, timeout=20)
            txt = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            if txt: return txt
        except Exception as e:
            print("Caption Gemini error:", e)

    return None

# ── Web API ───────────────────────────────────────────────
