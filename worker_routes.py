"""
worker_routes.py — أضف هذه الـ routes داخل routes.py
(بعد ما تستورد auth.py)
"""

# ══════════════════════════════════════════════════════════════
# أضف هذه الـ imports في أعلى routes.py:
#
#   from auth import owner_required, worker_required, register_auth_routes
#   from login_pages import (login_select_page, owner_login_page,
#                             worker_login_page, worker_page)
#   register_auth_routes(app)   ← سطر واحد بعد الـ imports
#
# ثم أضف @owner_required على كل route موجودة تخص المالك
# ══════════════════════════════════════════════════════════════


# ── لوحة العاملة ─────────────────────────────────────────────
@app.route("/worker")
@worker_required
def worker_dashboard():
    from database import db_get
    from login_pages import worker_page
    shelves = db_get("SELECT id, name FROM shelves ORDER BY name")
    success = request.args.get("ok")
    error   = request.args.get("err")
    return worker_page(shelves=shelves, success=success, error=error)


# ── تسجيل بيع من العاملة ─────────────────────────────────────
@app.route("/worker/add-sale", methods=["POST"])
@worker_required
def worker_add_sale():
    from database import db_run
    from helpers import cur_month
    desc    = request.form.get("desc","").strip()
    amt_str = request.form.get("amt","0").strip()
    shelf_id= request.form.get("shelf_id") or None
    pay_method = request.form.get("payment_method","نقد")

    if not desc:
        return redirect("/worker?err=الوصف مطلوب")
    try:
        amt = float(amt_str)
        if amt <= 0:
            raise ValueError
    except:
        return redirect("/worker?err=المبلغ غير صحيح")

    today = datetime.now().strftime("%d/%m/%Y")
    month = cur_month()
    sale_time = datetime.now().strftime("%H:%M")

    db_run(
        """INSERT INTO entries
           (type,desc,amt,date,month,payment_method,sale_time,shelf_id)
           VALUES (?,?,?,?,?,?,?,?)""",
        ("s", desc, amt, today, month, pay_method, sale_time, shelf_id)
    )
    return redirect(f"/worker?ok=تم تسجيل البيع: {desc} — {amt:.3f} ر.ع")


# ── API: مبيعات اليوم للعاملة (JSON) ─────────────────────────
@app.route("/worker/today-sales")
@worker_required
def worker_today_sales():
    from database import db_get
    today = datetime.now().strftime("%d/%m/%Y")
    rows  = db_get(
        "SELECT desc, amt, payment_method, sale_time FROM entries "
        "WHERE type='s' AND date=? ORDER BY created DESC",
        (today,)
    )
    return jsonify({"sales": rows})
