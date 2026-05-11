"""
auth.py — نظام المصادقة (مالك / عامل)
"""
from functools import wraps
from flask import session, redirect, request
from config import app, APP_PASSWORD, WORKER_PASSWORD
from html_pages import login_select_page, owner_login_page, worker_login_page


# ── Helpers ───────────────────────────────────────────────────
def is_owner():
    return session.get("role") == "owner"


def is_worker():
    return session.get("role") in ("owner", "worker")


# ── Decorators ────────────────────────────────────────────────
def owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_owner():
            return redirect("/login/owner")
        return f(*args, **kwargs)
    return decorated


def worker_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_worker():
            return redirect("/login/worker")
        return f(*args, **kwargs)
    return decorated


# ── Auth Routes ───────────────────────────────────────────────
def register_auth_routes(app):

    @app.route("/")
    def index():
        if session.get("role") == "owner":
            return redirect("/dashboard")
        if session.get("role") == "worker":
            return redirect("/worker")
        return login_select_page()

    @app.route("/login/owner", methods=["GET", "POST"])
    def login_owner():
        if request.method == "POST":
            if request.form.get("password") == APP_PASSWORD:
                session["role"] = "owner"
                return redirect("/dashboard")
            return owner_login_page(error=True)
        return owner_login_page()

    @app.route("/login/worker", methods=["GET", "POST"])
    def login_worker():
        if request.method == "POST":
            if request.form.get("password") == WORKER_PASSWORD:
                session["role"] = "worker"
                return redirect("/worker")
            return worker_login_page(error=True)
        return worker_login_page()

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")

    @app.route("/ping")
    def ping():
        return "ok"
