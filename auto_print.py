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

import requests, json, subprocess, os, time, tempfile
from datetime import datetime

# ══════════════════════════════════════
# ⚙️  الإعدادات — عدّلها قبل التشغيل
# ══════════════════════════════════════
APP_URL       = "https://fairose.up.railway.app"   # رابط التطبيق
PRINT_TOKEN   = "CHANGE_ME_123"                    # نفس PRINT_TOKEN في Railway
PRINTER_NAME  = ""          # اسم الطابعة (فارغ = الافتراضية). مثال: "HP_LaserJet"
CHECK_EVERY   = 30          # ثواني بين كل فحص
PAPER_WIDTH   = "A4"        # A4 أو A5 أو "80mm" لطابعة حرارية
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

def make_receipt_html(order):
    price_line = ""
    if order.get("price") and float(order.get("price", 0)) > 0:
        price_line = f'<div class="row"><span class="lbl">السعر</span><span class="val">{float(order["price"]):.3f} OMR</span></div>'

    notes_line = ""
    if order.get("notes"):
        notes_line = f'<div class="notes">📝 {order["notes"]}</div>'

    source_badge = "🌐 موقع"
    if order.get("source") == "telegram":
        source_badge = "💬 تيليغرام"

    now = datetime.now().strftime("%H:%M  %d/%m/%Y")

    return f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Tajawal', Arial, sans-serif;
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
  @media print {{
    body {{ margin: 0; padding: 8mm; }}
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
  <div class="status-new">● طلب جديد</div>
  <div class="order-num">#{order["id"]}</div>
  <div class="order-lbl">رقم الطلب</div>
  <div class="source">{source_badge}</div>
</div>

<div class="section">
  <div class="row">
    <span class="lbl">👤 العميل</span>
    <span class="val">{order.get("customer_name","—")}</span>
  </div>
  <div class="row">
    <span class="lbl">📞 الهاتف</span>
    <span class="phone-val">{order.get("customer_phone","—") or "—"}</span>
  </div>
  <div class="row">
    <span class="lbl">📅 التاريخ</span>
    <span class="val">{order.get("date","")}</span>
  </div>
</div>

<div class="desc-box">{order.get("description","")}</div>

{f'''<div class="price-box">
  <span class="price-lbl">💰 السعر المتفق</span>
  <span class="price-val">{float(order.get("price",0)):.3f} OMR</span>
</div>''' if order.get("price") and float(order.get("price",0)) > 0 else ""}

{notes_line}

<div class="footer">
  🕐 طُبع: {now}<br>
  فيروز فلورز — نظام إدارة المحل
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
