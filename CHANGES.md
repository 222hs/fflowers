# سجل التعديلات — Fairuz Flowers

## المشاكل المُصلَحة

### 1. `settings init error: name 'db_exec' is not defined`
- **السبب:** كود يستدعي `db_exec` وهي غير موجودة
- **الحل:** توحيد الدوال إلى `db_run` و `db_get` فقط في كل مكان

### 2. `no such table: app_settings`
- **السبب:** الجدول لم يُنشأ في `init_db()`
- **الحل:** أُضيف `CREATE TABLE IF NOT EXISTS app_settings` مع دالتين جديدتين:
  - `db_setting(key, default)` — لقراءة الإعدادات
  - `db_setting_set(key, value)` — لحفظ الإعدادات

### 3. `init_db()` يُستدعى مرتين
- **السبب:** كان في آخر `database.py` سطر مباشر + في `app.py`
- **الحل:** حُذف الاستدعاء التلقائي من `database.py`، يبقى فقط في `app.py`

### 4. `SECRET_KEY` مفقود
- **السبب:** Flask يحتاج secret_key للـ sessions وإلا تتكسر
- **الحل:** أُضيف في `config.py`:
  ```python
  app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
  ```

### 5. `render.yaml` ناقص
- **السبب:** `TURSO_URL` و `TURSO_TOKEN` و `SECRET_KEY` غير موجودين
- **الحل:** أُضيفت المتغيرات الثلاثة مع `generateValue: true` للـ SECRET_KEY

### 6. `worker_routes.py` imports داخل الدوال
- **السبب:** imports كانت داخل كل route (بطيء + غير نظيف)
- **الحل:** نُقلت كلها للأعلى

### 7. تنظيف عام
- إزالة connections SQLite المتعددة غير المغلقة
- توحيد `_sqlite_run` لمعالجة الأخطاء بشكل نظيف
- تبسيط `init_db` مع جمع كل الـ migrations في مكان واحد

## الملفات المُعدَّلة
| الملف | التغييرات |
|-------|-----------|
| `config.py` | إضافة `SECRET_KEY` |
| `database.py` | إضافة `app_settings`، إصلاح `init_db`، إزالة الاستدعاء التلقائي |
| `app.py` | تنظيف imports |
| `render.yaml` | إضافة `SECRET_KEY`, `TURSO_URL`, `TURSO_TOKEN` |
| `helpers.py` | تنظيف عام |
| `auth.py` | تنظيف عام |
| `worker_routes.py` | نقل imports للأعلى، إصلاح الاستيراد من الملفات الصحيحة |
