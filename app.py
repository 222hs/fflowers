"""
نقطة الدخول الرئيسية — Render يشغّل هذا الملف
"""
from config import app
from database import init_db
import routes  # noqa: يسجّل كل الـ routes تلقائياً

# تهيئة قاعدة البيانات عند البدء
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)), debug=False)
