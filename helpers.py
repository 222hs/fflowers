from config import *
from database import db_get, db_one, db_run


def fmt_omr(n):
    return f"{n:,.3f} ر.ع"


def cur_month():
    return datetime.now().strftime("%Y-%m")


def get_month_data(month):
    rows = db_get("SELECT * FROM entries WHERE month=? ORDER BY created DESC", (month,))
    return (
        [r for r in rows if r["type"] == "s"],
        [r for r in rows if r["type"] in ("b", "expense")]
    )


def month_summary(month):
    s, b = get_month_data(month)
    ts = sum(e["amt"] for e in s)
    tb = sum(e["amt"] for e in b)
    return ts, tb, ts - tb, len(s), len(b)


def get_day_data(day_str):
    """جيب بيانات يوم معين — day_str بصيغة dd/mm/yyyy"""
    rows = db_get("SELECT * FROM entries WHERE date=? ORDER BY created DESC", (day_str,))
    return (
        [r for r in rows if r["type"] == "s"],
        [r for r in rows if r["type"] == "b"],
        [r for r in rows if r["type"] == "expense"]
    )


def day_summary(day_str):
    s, b, e = get_day_data(day_str)
    ts = sum(r["amt"] for r in s)
    tb = sum(r["amt"] for r in b)
    te = sum(r["amt"] for r in e)
    return ts, tb, te, ts - tb - te, len(s), len(b)


def format_day_report(day_str):
    s, b, e = get_day_data(day_str)
    # فصل مبيعات الرفوف عن مبيعات المحل
    store_s = [r for r in s if not r.get("shelf_id")]
    shelf_s = [r for r in s if r.get("shelf_id")]
    ts = sum(r["amt"] for r in store_s)
    ts_shelf = sum(r["amt"] for r in shelf_s)
    tb = sum(r["amt"] for r in b)
    te = sum(r["amt"] for r in e)
    net = ts - tb - te
    emoji = "✅" if net >= 0 else "⚠️"
    lines = [f"📅 <b>تقرير يوم {day_str}</b>\n"]
    lines.append(f"🌸 مبيعات المحل: {fmt_omr(ts)} ({len(store_s)} عملية)")
    if store_s:
        for r in store_s:
            pay = f" — {r['payment_method']}" if r.get("payment_method") else ""
            lines.append(f"  • {r['desc']}: {fmt_omr(r['amt'])}{pay}")
    if shelf_s:
        lines.append(f"\n🗄️ مبيعات الرفوف: {fmt_omr(ts_shelf)} ({len(shelf_s)} عملية)")
        for r in shelf_s:
            pay = f" — {r['payment_method']}" if r.get("payment_method") else ""
            lines.append(f"  • {r['desc']}: {fmt_omr(r['amt'])}{pay}")
    lines.append(f"\n📦 المشتريات: {fmt_omr(tb)} ({len(b)} عملية)")
    if b:
        for r in b:
            who = f" — {r['paid_by']}" if r.get("paid_by") else ""
            lines.append(f"  • {r['desc']}: {fmt_omr(r['amt'])}{who}")
    if e:
        lines.append(f"\n💸 المصاريف: {fmt_omr(te)}")
        for r in e:
            lines.append(f"  • {r['desc']}: {fmt_omr(r['amt'])}")
    lines.append("\n━━━━━━")
    lines.append(f"{emoji} صافي المحل: {fmt_omr(net)}")
    if ts_shelf:
        lines.append(f"🗄️ إجمالي الرفوف: {fmt_omr(ts_shelf)}")
    return "\n".join(lines)


def format_month_report(month):
    s, b = get_month_data(month)
    exps = db_get(
        "SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC",
        (month,)
    )
    # فصل مبيعات الرفوف
    store_s = [r for r in s if not r.get("shelf_id")]
    shelf_s = [r for r in s if r.get("shelf_id")]
    ts = sum(r["amt"] for r in store_s)
    ts_shelf = sum(r["amt"] for r in shelf_s)
    tb = sum(r["amt"] for r in b if r["type"] != "expense")
    te = sum(r["amt"] for r in exps)
    net = ts - tb - te
    emoji = "✅" if net >= 0 else "⚠️"
    days = {}
    for r in store_s:
        d = r.get("date", "")
        if d not in days:
            days[d] = {"s": 0, "b": 0, "sc": 0, "bc": 0}
        days[d]["s"] += r["amt"]
        days[d]["sc"] += 1
    for r in b:
        if r["type"] == "b":
            d = r.get("date", "")
            if d not in days:
                days[d] = {"s": 0, "b": 0, "sc": 0, "bc": 0}
            days[d]["b"] += r["amt"]
            days[d]["bc"] += 1
    days_sorted = sorted(days.items(), key=lambda x: x[0])
    lines = [f"📊 <b>تقرير شهر {month}</b>\n"]
    lines.append(f"🌸 مبيعات المحل: {fmt_omr(ts)} ({len(store_s)} عملية)")
    if ts_shelf > 0:
        lines.append(f"🗄️ مبيعات الرفوف: {fmt_omr(ts_shelf)} ({len(shelf_s)} عملية)")
    lines.append(f"📦 إجمالي المشتريات: {fmt_omr(tb)}")
    lines.append(f"💸 إجمالي المصاريف: {fmt_omr(te)}")
    lines.append(f"{emoji} صافي المحل: {fmt_omr(net)}\n")
    lines.append("📆 <b>تفصيل يومي:</b>")
    for day, v in days_sorted:
        if day:
            day_net = v["s"] - v["b"]
            e2 = "✅" if day_net >= 0 else "🔴"
            lines.append(f"{e2} {day}: مبيعات {fmt_omr(v['s'])} | مشتريات {fmt_omr(v['b'])}")
    return "\n".join(lines)
