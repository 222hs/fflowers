#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌹 فيروز فلورز — نظام الطباعة التلقائية
────────────────────────────────────────
يفحص الطلبات الجديدة كل 30 ثانية ويطبعها تلقائياً

التشغيل:
  python3 auto_print.py

المتطلبات:
  pip3 install requests
"""

import requests, json, subprocess, os, time, tempfile, base64
from datetime import datetime

# ══════════════════════════════════════
# ⚙️  الإعدادات — عدّلها قبل التشغيل
# ══════════════════════════════════════
APP_URL          = "https://fairose.up.railway.app"   # رابط التطبيق
PRINT_TOKEN      = "CHANGE_ME_123"                    # نفس PRINT_TOKEN في Railway
PRINTER_NAME     = ""          # اسم الطابعة (فارغ = الافتراضية). مثال: "HP_LaserJet"
CHECK_EVERY      = 30          # ثواني بين كل فحص
PAPER_WIDTH      = "A4"        # A4 أو A5 أو "80mm" لطابعة حرارية
LANGUAGE         = "tri"       # ar=عربي | en=English | bn=বাংলা | tri=الثلاثة معاً
TELEGRAM_BOT_TOKEN = ""        # توكن البوت لتحميل صور الطلبات (اختياري)
PRINT_ORDER_IMAGE  = True      # طباعة صورة الطلب إن وجدت
# ══════════════════════════════════════

PRINTED_FILE = os.path.expanduser("~/.fairuz_printed_ids.json")

def load_printed():
    try:
        with open(PRINTED_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_printed(ids):
    with open(PRINTED_FILE, "w") as f:
        json.dump(sorted(ids), f)

def get_new_orders(printed):
    try:
        r = requests.get(f"{APP_URL}/api/print-feed",
                         params={"token": PRINT_TOKEN}, timeout=12)
        if r.status_code == 401:
            print("❌ خطأ: PRINT_TOKEN غير صحيح")
            return []
        r.raise_for_status()
        orders = r.json().get("orders", [])
        return [o for o in orders if o["id"] not in printed]
    except Exception as e:
        print(f"⚠️  خطأ في الاتصال: {e}")
        return []

# ── قاموس الترجمات ──
TR = {
    "ar": {
        "new_order":  "● طلب جديد",
        "order_num":  "رقم الطلب",
        "customer":   "العميل",
        "phone":      "الهاتف",
        "date":       "التاريخ",
        "price":      "السعر المتفق",
        "notes":      "ملاحظات",
        "printed_at": "طُبع",
        "status_new": "طلب جديد ●",
        "web":        "🌐 موقع",
        "telegram":   "💬 تيليغرام",
        "omr":        "OMR",
        "dir":        "rtl",
    },
    "en": {
        "new_order":  "● New Order",
        "order_num":  "Order Number",
        "customer":   "Customer",
        "phone":      "Phone",
        "date":       "Date",
        "price":      "Agreed Price",
        "notes":      "Notes",
        "printed_at": "Printed",
        "status_new": "New Order ●",
        "web":        "🌐 Website",
        "telegram":   "💬 Telegram",
        "omr":        "OMR",
        "dir":        "ltr",
    },
    "bn": {
        "new_order":  "● নতুন অর্ডার",
        "order_num":  "অর্ডার নম্বর",
        "customer":   "গ্রাহক",
        "phone":      "ফোন",
        "date":       "তারিখ",
        "price":      "সম্মত মূল্য",
        "notes":      "নোট",
        "printed_at": "মুদ্রিত",
        "status_new": "নতুন অর্ডার ●",
        "web":        "🌐 ওয়েবসাইট",
        "telegram":   "💬 টেলিগ্রাম",
        "omr":        "OMR",
        "dir":        "ltr",
    },
}

def t(key, lang=None):
    """ترجمة مفتاح حسب اللغة المحددة"""
    lg = lang or LANGUAGE
    if lg == "tri":
        lg = "ar"
    return TR.get(lg, TR["en"]).get(key, key)

def label_row(ar_key, value, lang):
    """صف مع الترجمة المناسبة"""
    if lang == "tri":
        ar  = TR["ar"].get(ar_key, ar_key)
        en  = TR["en"].get(ar_key, ar_key)
        bn  = TR["bn"].get(ar_key, ar_key)
        lbl = f'{ar}<br><small style="color:#aaa;font-size:9pt;">{en} / {bn}</small>'
    else:
        lbl = TR.get(lang, TR["ar"]).get(ar_key, ar_key)
    return lbl

def fetch_order_image_b64(order):
    """يحاول تحميل صورة الطلب ويعيدها كـ base64 data-URI، أو None"""
    if not PRINT_ORDER_IMAGE:
        return None
    # محاولة 1: img_url مباشر
    img_url = order.get("img_url") or ""
    if img_url and img_url.startswith("http"):
        try:
            r = requests.get(img_url, timeout=15)
            if r.status_code == 200:
                ct = r.headers.get("Content-Type","image/jpeg").split(";")[0].strip()
                b64 = base64.b64encode(r.content).decode()
                return f"data:{ct};base64,{b64}"
        except Exception as e:
            print(f"  ⚠️  لم يمكن تحميل img_url: {e}")
    # محاولة 2: img_file_id من تيليغرام
    file_id = order.get("img_file_id") or ""
    if file_id and TELEGRAM_BOT_TOKEN:
        try:
            api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
            r = requests.get(f"{api}/getFile", params={"file_id": file_id}, timeout=10)
            path = r.json()["result"]["file_path"]
            img_r = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{path}", timeout=20)
            if img_r.status_code == 200:
                ct = img_r.headers.get("Content-Type","image/jpeg").split(";")[0].strip()
                b64 = base64.b64encode(img_r.content).decode()
                return f"data:{ct};base64,{b64}"
        except Exception as e:
            print(f"  ⚠️  لم يمكن تحميل صورة تيليغرام: {e}")
    return None

def make_receipt_html(order):
    lang = LANGUAGE

    # تحميل صورة الطلب
    img_b64 = fetch_order_image_b64(order)
    if img_b64:
        img_html = f'''<div class="order-img-wrap">
          <div class="order-img-lbl">📸 صورة الطلب</div>
          <img class="order-img" src="{img_b64}" alt="order image">
        </div>'''
    else:
        img_html = ""

    price_html = ""
    if order.get("price") and float(order.get("price", 0)) > 0:
        price_lbl = label_row("price", "", lang)
        price_html = f'''<div class="price-box">
          <span class="price-lbl">💰 {price_lbl}</span>
          <span class="price-val">{float(order["price"]):.3f} OMR</span>
        </div>'''

    notes_html = ""
    if order.get("notes"):
        notes_lbl = TR.get(lang if lang != "tri" else "ar", TR["ar"]).get("notes","Notes")
        notes_html = f'<div class="notes">📝 {notes_lbl}: {order["notes"]}</div>'

    src = order.get("source","")
    if src == "telegram":
        source_badge = "💬 تيليغرام"
    elif src == "siri":
        source_badge = "🎤 سيري"
    else:
        source_badge = "🌐 موقع"

    # اتجاه الصفحة
    page_dir = "rtl" if lang in ("ar","tri") else "ltr"

    # ترجمة التسميات
    lbl_customer  = label_row("customer",  "", lang)
    lbl_phone     = label_row("phone",     "", lang)
    lbl_date      = label_row("date",      "", lang)
    lbl_order_num = label_row("order_num", "", lang)
    lbl_new_order = TR.get(lang if lang != "tri" else "ar", TR["ar"]).get("new_order","New Order")
    lbl_printed   = TR.get(lang if lang != "tri" else "ar", TR["ar"]).get("printed_at","Printed")

    now = datetime.now().strftime("%H:%M  %d/%m/%Y")

    return f"""<!DOCTYPE html>
<html dir="{page_dir}" lang="{lang if lang != 'tri' else 'ar'}">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&family=Noto+Sans+Bengali:wght@400;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Tajawal','Noto Sans Bengali', Arial, sans-serif;
    width: 100%;
    max-width: 200mm;
    margin: 0 auto;
    padding: 12mm 10mm;
    font-size: 13pt;
    color: #1a1a1a;
  }}
  .header {{
    text-align: center;
    border-bottom: 3px double #c4566a;
    padding-bottom: 10px;
    margin-bottom: 14px;
  }}
  .logo {{ font-size: 28pt; }}
  .shop-name {{ font-size: 20pt; font-weight: 900; color: #c4566a; margin-top: 4px; }}
  .shop-en {{ font-size: 10pt; color: #888; letter-spacing: 2px; }}
  .order-badge {{
    text-align: center;
    background: #fff0f3;
    border: 2px solid #e8798a;
    border-radius: 12px;
    padding: 10px;
    margin: 12px 0;
  }}
  .order-num {{ font-size: 28pt; font-weight: 900; color: #c4566a; line-height: 1; }}
  .order-lbl {{ font-size: 10pt; color: #888; margin-top: 2px; }}
  .source {{ display:inline-block; font-size:9pt; background:#f5ede0; padding:2px 8px; border-radius:6px; color:#7a6458; margin-top:4px; }}
  .section {{ margin: 12px 0; }}
  .row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 6px 0;
    border-bottom: 1px solid #f0e0e8;
  }}
  .row:last-child {{ border-bottom: none; }}
  .lbl {{ color: #888; font-size: 11pt; }}
  .val {{ font-weight: 700; font-size: 13pt; }}
  .phone-val {{ font-size: 15pt; font-weight: 900; color: #1d4ed8; direction: ltr; }}
  .desc-box {{
    background: #fdf8f2;
    border: 1.5px solid #f9c8d0;
    border-radius: 10px;
    padding: 10px 12px;
    margin: 10px 0;
    font-size: 13pt;
    line-height: 1.7;
    white-space: pre-wrap;
  }}
  .price-box {{
    background: #f0fdf4;
    border: 2px solid #86efac;
    border-radius: 10px;
    padding: 10px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0;
  }}
  .price-lbl {{ color: #16a34a; font-weight: 700; }}
  .price-val {{ font-size: 20pt; font-weight: 900; color: #16a34a; }}
  .notes {{ font-size: 11pt; color: #666; margin: 6px 0; padding: 6px 10px; border-right: 3px solid #f9c8d0; }}
  .footer {{
    text-align: center;
    border-top: 3px double #c4566a;
    padding-top: 10px;
    margin-top: 14px;
    font-size: 10pt;
    color: #888;
  }}
  .status-new {{
    display: inline-block;
    background: #ef4444;
    color: white;
    font-size: 10pt;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 6px;
    letter-spacing: 1px;
  }}
  .order-img-wrap {{
    margin: 12px 0;
    text-align: center;
    border: 1.5px solid #f9c8d0;
    border-radius: 12px;
    overflow: hidden;
    background: #fdf8f2;
    padding: 8px;
  }}
  .order-img-lbl {{
    font-size: 10pt;
    color: #c4566a;
    font-weight: 700;
    margin-bottom: 6px;
  }}
  .order-img {{
    max-width: 100%;
    max-height: 180mm;
    border-radius: 8px;
    object-fit: contain;
    display: block;
    margin: 0 auto;
  }}
  @media print {{
    body {{ margin: 0; padding: 8mm; }}
    .order-img {{ max-height: 160mm; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="logo">🌹</div>
  <div class="shop-name">فيروز فلورز</div>
  <div class="shop-en">FAIRUZ FLOWERS</div>
</div>

<div class="order-badge">
  <div class="status-new">{lbl_new_order}</div>
  <div class="order-num">#{order["id"]}</div>
  <div class="order-lbl">{lbl_order_num}</div>
  <div class="source">{source_badge}</div>
</div>

<div class="section">
  <div class="row">
    <span class="lbl">👤 {lbl_customer}</span>
    <span class="val">{order.get("customer_name","—")}</span>
  </div>
  <div class="row">
    <span class="lbl">📞 {lbl_phone}</span>
    <span class="phone-val">{order.get("customer_phone","—") or "—"}</span>
  </div>
  <div class="row">
    <span class="lbl">📅 {lbl_date}</span>
    <span class="val">{order.get("date","")}</span>
  </div>
</div>

<div class="desc-box">{order.get("description","")}</div>

{price_html}

{notes_html}

{img_html}

<div class="footer">
  🕐 {lbl_printed}: {now}<br>
  🌹 Fairuz Flowers | فيروز فلورز | ফেরুজ ফ্লাওয়ার্স
</div>

</body>
</html>"""

def print_order(order):
    """يطبع الطلب على الطابعة"""
    html = make_receipt_html(order)
    html_path = f"/tmp/fairuz_order_{order['id']}.html"
    pdf_path  = f"/tmp/fairuz_order_{order['id']}.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # ── محاولة 1: wkhtmltopdf (brew install wkhtmltopdf) ──
    has_wk = subprocess.run(["which","wkhtmltopdf"],
                            capture_output=True).returncode == 0
    if has_wk:
        page_args = []
        if PAPER_WIDTH == "80mm":
            page_args = ["--page-width","80mm","--page-height","200mm"]
        else:
            page_args = [f"--page-size", PAPER_WIDTH]

        result = subprocess.run(
            ["wkhtmltopdf","--quiet","--encoding","utf-8",
             "--margin-top","5mm","--margin-right","5mm",
             "--margin-bottom","5mm","--margin-left","5mm"]
            + page_args + [html_path, pdf_path],
            capture_output=True
        )
        _do_lpr(pdf_path, order)
        return

    # ── محاولة 2: weasyprint (pip3 install weasyprint) ──
    try:
        from weasyprint import HTML as WH
        WH(filename=html_path).write_pdf(pdf_path)
        _do_lpr(pdf_path, order)
        return
    except ImportError:
        pass

    # ── محاولة 3: macOS open للطباعة اليدوية ──
    print(f"⚠️  لا يوجد محول PDF — فتح الطلب #{order['id']} في المتصفح للطباعة يدوياً")
    print(f"   💡 ثبّت wkhtmltopdf: brew install wkhtmltopdf")
    subprocess.run(["open", html_path])

def _do_lpr(path, order):
    cmd = ["lpr"]
    if PRINTER_NAME:
        cmd += ["-P", PRINTER_NAME]
    cmd.append(path)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"  🖨️  طُبع بنجاح")
    else:
        print(f"  ❌ خطأ في الطباعة: {result.stderr.decode()}")

def get_printer_name():
    """اعرض قائمة الطابعات المتاحة"""
    result = subprocess.run(["lpstat","-a"], capture_output=True, text=True)
    if result.stdout:
        print("\n🖨️  الطابعات المتاحة:")
        for line in result.stdout.strip().split("\n"):
            name = line.split()[0]
            print(f"   • {name}")
    else:
        print("⚠️  لا طابعات مكوّنة — تحقق من إعدادات الطباعة في macOS")

def main():
    print("=" * 50)
    print("🌹  فيروز فلورز — نظام الطباعة التلقائية")
    print("=" * 50)
    print(f"🔗  {APP_URL}")
    print(f"🖨️  الطابعة: {PRINTER_NAME or 'الافتراضية'}")
    print(f"⏱️  فحص كل {CHECK_EVERY} ثانية")

    # تحقق من الإعدادات
    if PRINT_TOKEN == "CHANGE_ME_123":
        print("\n⚠️  تحذير: لم تغيّر PRINT_TOKEN!")
        print("   عدّله في أعلى السكريبت ثم أضفه في Railway → Variables")
        return

    # عرض الطابعات
    get_printer_name()
    print("-" * 50)
    print("✅  جاهز للطباعة التلقائية... (Ctrl+C للإيقاف)\n")

    printed = load_printed()

    while True:
        try:
            new_orders = get_new_orders(printed)

            if new_orders:
                for order in new_orders:
                    print(f"\n{'='*40}")
                    print(f"🆕  طلب جديد! #{order['id']}")
                    print(f"    👤 {order.get('customer_name','—')}")
                    print(f"    📞 {order.get('customer_phone','—') or '—'}")
                    print(f"    📝 {(order.get('description','') or '')[:60]}...")
                    if order.get("price") and float(order.get("price",0)) > 0:
                        print(f"    💰 {float(order['price']):.3f} OMR")
                    print(f"    🕐 {datetime.now().strftime('%H:%M:%S')}")
                    print_order(order)
                    printed.add(order["id"])
                    save_printed(printed)
            else:
                t = datetime.now().strftime("%H:%M:%S")
                print(f"\r⏳  {t} — لا طلبات جديدة ({len(printed)} مطبوع إجمالاً)    ",
                      end="", flush=True)

            time.sleep(CHECK_EVERY)

        except KeyboardInterrupt:
            print("\n\n👋  تم إيقاف نظام الطباعة")
            break
        except Exception as e:
            print(f"\n⚠️  خطأ: {e}")
            time.sleep(CHECK_EVERY)

if __name__ == "__main__":
    main()
