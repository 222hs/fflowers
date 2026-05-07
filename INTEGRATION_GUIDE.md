# دليل التطبيق — نظام الدخول المنفصل

## الملفات الجديدة / المعدّلة

| الملف | الوصف |
|-------|-------|
| `config.py` | أُضيف `app.secret_key` |
| `auth.py` | ملف جديد — decorators + auth routes |
| `login_pages.py` | ملف جديد — صفحات HTML |
| `worker_routes.py` | routes العاملة — أضفها لـ routes.py |

---

## خطوات التطبيق

### 1. استبدل config.py بالملف الجديد
السطر الوحيد المضاف:
```python
app.secret_key = os.environ.get("SECRET_KEY", "fairuz-secret-2026-xK9m")
```

### 2. أضف الملفين الجديدين للمشروع
```
auth.py
login_pages.py
```

### 3. عدّل routes.py

في **أعلى الملف** بعد الـ imports الموجودة، أضف:
```python
from auth import owner_required, worker_required, register_auth_routes
from login_pages import (login_select_page, owner_login_page,
                          worker_login_page, worker_page)

register_auth_routes(app)   # يسجّل: / و /login/owner و /login/worker و /logout
```

في **نهاية الملف**، أضف محتوى worker_routes.py

### 4. أضف @owner_required على routes المالك الموجودة

مثال:
```python
# قبل
@app.route("/dashboard")
def dashboard():
    ...

# بعد
@app.route("/dashboard")
@owner_required
def dashboard():
    ...
```

طبّقها على كل route لا تريدين أن تراها العاملة.

### 5. أضف SECRET_KEY في Render (اختياري لكن مستحسن)
```
SECRET_KEY = any-random-string-here
```

---

## منطق الصلاحيات

| الـ Route | من يدخل |
|-----------|---------|
| `/` | الجميع (صفحة الاختيار) |
| `/login/owner` | الجميع |
| `/login/worker` | الجميع |
| `/worker` | العاملة والمالكة |
| `/dashboard` وكل pages المالك | المالكة فقط |

---

## ما تقدر تفعله العاملة

✅ تسجيل مبيعات
✅ رؤية مبيعات اليوم
❌ لا تقدر تشوف التقارير
❌ لا تقدر تضيف مصاريف أو مشتريات
❌ لا تقدر تدخل لوحة المالكة
