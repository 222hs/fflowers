"""
صفحات تسجيل الدخول — أضفها في html_pages.py
"""

# ── صفحة الاختيار (مالك / عامل) ──────────────────────────────
def login_select_page():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>فيروز للزهور</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{
    min-height:100vh;
    background: #0f0a14;
    display:flex;align-items:center;justify-content:center;
    font-family:'Tajawal',sans-serif;
    overflow:hidden;
    position:relative;
  }
  /* خلفية زهور متحركة */
  .bg-flowers{
    position:fixed;inset:0;pointer-events:none;z-index:0;
    overflow:hidden;
  }
  .petal{
    position:absolute;
    font-size:1.8rem;
    opacity:0.12;
    animation: fall linear infinite;
  }
  @keyframes fall{
    0%{transform:translateY(-60px) rotate(0deg);opacity:0.12}
    100%{transform:translateY(110vh) rotate(360deg);opacity:0.04}
  }

  .card{
    position:relative;z-index:1;
    text-align:center;
    padding:2.5rem 2rem;
    max-width:400px;width:90%;
  }
  .logo{
    font-size:3.5rem;margin-bottom:.5rem;
    animation: pulse 3s ease-in-out infinite;
  }
  @keyframes pulse{
    0%,100%{transform:scale(1)}
    50%{transform:scale(1.08)}
  }
  h1{
    color:#f9d4e0;
    font-size:2.2rem;font-weight:900;
    letter-spacing:2px;margin-bottom:.3rem;
  }
  .subtitle{color:#9b7ea0;font-size:1rem;margin-bottom:2.5rem;font-weight:300}

  .btn-group{display:flex;flex-direction:column;gap:1rem}

  .btn{
    display:flex;align-items:center;justify-content:center;gap:.8rem;
    padding:1.1rem 2rem;
    border-radius:16px;border:none;cursor:pointer;
    font-family:'Tajawal',sans-serif;font-size:1.2rem;font-weight:700;
    text-decoration:none;
    transition:transform .18s, box-shadow .18s;
    position:relative;overflow:hidden;
  }
  .btn::after{
    content:'';position:absolute;inset:0;
    background:rgba(255,255,255,0.08);
    opacity:0;transition:opacity .2s;
  }
  .btn:hover::after{opacity:1}
  .btn:hover{transform:translateY(-3px);box-shadow:0 12px 35px rgba(0,0,0,.4)}
  .btn:active{transform:translateY(0)}

  .btn-owner{
    background:linear-gradient(135deg,#c0395e,#8b1a3a);
    color:#fff;
    box-shadow:0 6px 24px rgba(192,57,94,.35);
  }
  .btn-worker{
    background:linear-gradient(135deg,#2d7d62,#1a5444);
    color:#fff;
    box-shadow:0 6px 24px rgba(45,125,98,.35);
  }
  .btn-icon{font-size:1.5rem}

  .divider{
    display:flex;align-items:center;gap:1rem;
    color:#3d2a45;font-size:.85rem;
  }
  .divider::before,.divider::after{
    content:'';flex:1;height:1px;background:#3d2a45;
  }
</style>
</head>
<body>

<div class="bg-flowers" id="bgFlowers"></div>

<div class="card">
  <div class="logo">🌸</div>
  <h1>فيروز</h1>
  <p class="subtitle">محل الزهور والهدايا</p>

  <div class="btn-group">
    <a href="/login/owner" class="btn btn-owner">
      <span class="btn-icon">👑</span>
      <span>دخول المالكة</span>
    </a>
    <div class="divider">أو</div>
    <a href="/login/worker" class="btn btn-worker">
      <span class="btn-icon">🌿</span>
      <span>دخول العاملة</span>
    </a>
  </div>
</div>

<script>
const emojis = ['🌸','🌹','🌺','💐','🌷','🌼','🏵️'];
const bg = document.getElementById('bgFlowers');
for(let i=0;i<18;i++){
  const d = document.createElement('div');
  d.className='petal';
  d.textContent = emojis[i % emojis.length];
  d.style.left = Math.random()*100+'%';
  d.style.fontSize = (.8+Math.random()*1.8)+'rem';
  d.style.animationDuration = (8+Math.random()*12)+'s';
  d.style.animationDelay = (-Math.random()*12)+'s';
  bg.appendChild(d);
}
</script>
</body>
</html>"""


# ── صفحة دخول المالكة ─────────────────────────────────────────
def owner_login_page(error=False):
    err_html = """
    <div class="error-msg">
      <span>❌</span> كلمة السر غلط، حاولي ثاني
    </div>""" if error else ""

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>دخول المالكة — فيروز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{
    min-height:100vh;
    background:linear-gradient(145deg,#1a0812 0%,#2d0f22 50%,#1a0812 100%);
    display:flex;align-items:center;justify-content:center;
    font-family:'Tajawal',sans-serif;
  }}
  .card{{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(192,57,94,0.25);
    border-radius:24px;
    padding:2.5rem 2.2rem;
    max-width:380px;width:90%;
    backdrop-filter:blur(12px);
    box-shadow:0 20px 60px rgba(0,0,0,.5);
    text-align:center;
  }}
  .back{{
    display:inline-flex;align-items:center;gap:.4rem;
    color:#9b7ea0;font-size:.9rem;text-decoration:none;
    margin-bottom:1.5rem;
    transition:color .2s;
  }}
  .back:hover{{color:#f9d4e0}}
  .icon{{font-size:3rem;margin-bottom:.5rem}}
  h2{{color:#f9d4e0;font-size:1.9rem;font-weight:900;margin-bottom:.2rem}}
  .sub{{color:#9b7ea0;font-size:.95rem;margin-bottom:2rem;font-weight:300}}

  .input-wrap{{position:relative;margin-bottom:1.2rem}}
  input[type=password]{{
    width:100%;padding:1rem 1.2rem;
    background:rgba(255,255,255,0.06);
    border:1.5px solid rgba(192,57,94,0.3);
    border-radius:12px;
    color:#f9d4e0;font-family:'Tajawal',sans-serif;font-size:1.1rem;
    outline:none;text-align:center;letter-spacing:4px;
    transition:border-color .2s,background .2s;
  }}
  input[type=password]:focus{{
    border-color:#c0395e;
    background:rgba(192,57,94,0.08);
  }}
  input[type=password]::placeholder{{letter-spacing:1px;color:#5a3a4a}}

  .btn{{
    width:100%;padding:1rem;
    background:linear-gradient(135deg,#c0395e,#8b1a3a);
    color:#fff;border:none;border-radius:12px;
    font-family:'Tajawal',sans-serif;font-size:1.2rem;font-weight:700;
    cursor:pointer;
    box-shadow:0 6px 24px rgba(192,57,94,.4);
    transition:transform .18s,box-shadow .18s;
  }}
  .btn:hover{{transform:translateY(-2px);box-shadow:0 10px 30px rgba(192,57,94,.5)}}
  .btn:active{{transform:translateY(0)}}

  .error-msg{{
    background:rgba(220,50,50,0.15);
    border:1px solid rgba(220,50,50,0.3);
    border-radius:10px;padding:.8rem;
    color:#ff8a8a;font-size:.95rem;
    margin-bottom:1.2rem;
  }}
</style>
</head>
<body>
<div class="card">
  <a href="/" class="back">← العودة</a>
  <div class="icon">👑</div>
  <h2>لوحة المالكة</h2>
  <p class="sub">أدخلي كلمة السر للدخول</p>

  {err_html}

  <form method="POST">
    <div class="input-wrap">
      <input type="password" name="password" placeholder="كلمة السر" autofocus autocomplete="current-password">
    </div>
    <button type="submit" class="btn">دخول 🌸</button>
  </form>
</div>
</body>
</html>"""


# ── صفحة دخول العاملة ─────────────────────────────────────────
def worker_login_page(error=False):
    err_html = """
    <div class="error-msg">
      <span>❌</span> كلمة السر غلط، حاولي ثاني
    </div>""" if error else ""

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>دخول العاملة — فيروز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{
    min-height:100vh;
    background:linear-gradient(145deg,#071a14 0%,#0f2d22 50%,#071a14 100%);
    display:flex;align-items:center;justify-content:center;
    font-family:'Tajawal',sans-serif;
  }}
  .card{{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(45,125,98,0.25);
    border-radius:24px;
    padding:2.5rem 2.2rem;
    max-width:380px;width:90%;
    backdrop-filter:blur(12px);
    box-shadow:0 20px 60px rgba(0,0,0,.5);
    text-align:center;
  }}
  .back{{
    display:inline-flex;align-items:center;gap:.4rem;
    color:#6b9e8a;font-size:.9rem;text-decoration:none;
    margin-bottom:1.5rem;
    transition:color .2s;
  }}
  .back:hover{{color:#a8e6cf}}
  .icon{{font-size:3rem;margin-bottom:.5rem}}
  h2{{color:#a8e6cf;font-size:1.9rem;font-weight:900;margin-bottom:.2rem}}
  .sub{{color:#6b9e8a;font-size:.95rem;margin-bottom:2rem;font-weight:300}}

  .input-wrap{{position:relative;margin-bottom:1.2rem}}
  input[type=password]{{
    width:100%;padding:1rem 1.2rem;
    background:rgba(255,255,255,0.06);
    border:1.5px solid rgba(45,125,98,0.3);
    border-radius:12px;
    color:#a8e6cf;font-family:'Tajawal',sans-serif;font-size:1.1rem;
    outline:none;text-align:center;letter-spacing:4px;
    transition:border-color .2s,background .2s;
  }}
  input[type=password]:focus{{
    border-color:#2d7d62;
    background:rgba(45,125,98,0.08);
  }}
  input[type=password]::placeholder{{letter-spacing:1px;color:#2a4a3a}}

  .btn{{
    width:100%;padding:1rem;
    background:linear-gradient(135deg,#2d7d62,#1a5444);
    color:#fff;border:none;border-radius:12px;
    font-family:'Tajawal',sans-serif;font-size:1.2rem;font-weight:700;
    cursor:pointer;
    box-shadow:0 6px 24px rgba(45,125,98,.4);
    transition:transform .18s,box-shadow .18s;
  }}
  .btn:hover{{transform:translateY(-2px);box-shadow:0 10px 30px rgba(45,125,98,.5)}}
  .btn:active{{transform:translateY(0)}}

  .error-msg{{
    background:rgba(220,50,50,0.15);
    border:1px solid rgba(220,50,50,0.3);
    border-radius:10px;padding:.8rem;
    color:#ff8a8a;font-size:.95rem;
    margin-bottom:1.2rem;
  }}
</style>
</head>
<body>
<div class="card">
  <a href="/" class="back">← العودة</a>
  <div class="icon">🌿</div>
  <h2>لوحة العاملة</h2>
  <p class="sub">أدخلي كلمة السر للدخول</p>

  {err_html}

  <form method="POST">
    <div class="input-wrap">
      <input type="password" name="password" placeholder="كلمة السر" autofocus autocomplete="current-password">
    </div>
    <button type="submit" class="btn">دخول 🌿</button>
  </form>
</div>
</body>
</html>"""


# ── لوحة العاملة (تسجيل مبيعات فقط) ─────────────────────────
def worker_page(shelves=None, success=None, error=None):
    shelves = shelves or []
    shelves_opts = "".join(
        f'<option value="{s["id"]}">{s["name"]}</option>'
        for s in shelves
    )
    success_html = f'<div class="msg msg-ok">✅ {success}</div>' if success else ""
    error_html   = f'<div class="msg msg-err">❌ {error}</div>'   if error   else ""

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>تسجيل مبيعات — فيروز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{
    min-height:100vh;
    background:linear-gradient(160deg,#071a14 0%,#0f2d22 100%);
    font-family:'Tajawal',sans-serif;color:#cde8d8;
    padding:1.5rem 1rem 4rem;
  }}
  header{{
    display:flex;align-items:center;justify-content:space-between;
    margin-bottom:2rem;
  }}
  .logo-title{{display:flex;align-items:center;gap:.6rem}}
  .logo-title span{{font-size:1.6rem}}
  h1{{color:#a8e6cf;font-size:1.4rem;font-weight:900}}
  .logout{{
    color:#6b9e8a;font-size:.9rem;text-decoration:none;
    border:1px solid rgba(45,125,98,0.3);
    border-radius:8px;padding:.4rem .8rem;
    transition:all .2s;
  }}
  .logout:hover{{background:rgba(45,125,98,0.15);color:#a8e6cf}}

  .date-bar{{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(45,125,98,0.2);
    border-radius:12px;padding:.8rem 1rem;
    font-size:.9rem;color:#6b9e8a;
    margin-bottom:1.5rem;
    text-align:center;
  }}

  .card{{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(45,125,98,0.2);
    border-radius:20px;padding:1.5rem;
    margin-bottom:1.5rem;
  }}
  .card-title{{
    font-size:1.1rem;font-weight:700;color:#a8e6cf;
    margin-bottom:1.2rem;display:flex;align-items:center;gap:.5rem;
  }}

  .field{{margin-bottom:1rem}}
  label{{display:block;color:#6b9e8a;font-size:.9rem;margin-bottom:.4rem}}
  input[type=text],input[type=number],select,textarea{{
    width:100%;padding:.8rem 1rem;
    background:rgba(255,255,255,0.06);
    border:1.5px solid rgba(45,125,98,0.25);
    border-radius:10px;
    color:#cde8d8;font-family:'Tajawal',sans-serif;font-size:1rem;
    outline:none;transition:border-color .2s;
  }}
  input:focus,select:focus,textarea:focus{{border-color:#2d7d62}}
  select option{{background:#0f2d22}}
  textarea{{resize:vertical;min-height:70px}}

  .payment-opts{{
    display:flex;gap:.8rem;flex-wrap:wrap;margin-top:.3rem;
  }}
  .pay-btn{{
    flex:1;min-width:80px;
    padding:.7rem .5rem;
    background:rgba(255,255,255,0.04);
    border:1.5px solid rgba(45,125,98,0.25);
    border-radius:10px;color:#6b9e8a;
    font-family:'Tajawal',sans-serif;font-size:.95rem;
    cursor:pointer;text-align:center;transition:all .2s;
  }}
  .pay-btn.active{{
    background:rgba(45,125,98,0.2);
    border-color:#2d7d62;color:#a8e6cf;font-weight:700;
  }}

  .submit-btn{{
    width:100%;padding:1.1rem;
    background:linear-gradient(135deg,#2d7d62,#1a5444);
    color:#fff;border:none;border-radius:14px;
    font-family:'Tajawal',sans-serif;font-size:1.2rem;font-weight:700;
    cursor:pointer;
    box-shadow:0 6px 20px rgba(45,125,98,.35);
    transition:transform .18s,box-shadow .18s;
    margin-top:.5rem;
  }}
  .submit-btn:hover{{transform:translateY(-2px);box-shadow:0 10px 28px rgba(45,125,98,.5)}}

  .msg{{
    border-radius:12px;padding:.9rem 1rem;
    font-size:1rem;margin-bottom:1rem;text-align:center;
  }}
  .msg-ok{{background:rgba(45,125,98,.18);border:1px solid rgba(45,125,98,.4);color:#a8e6cf}}
  .msg-err{{background:rgba(200,50,50,.15);border:1px solid rgba(200,50,50,.3);color:#ff8a8a}}

  /* Today's sales quick view */
  .today-sales{{margin-top:1rem}}
  .sale-item{{
    display:flex;justify-content:space-between;align-items:center;
    padding:.7rem .5rem;
    border-bottom:1px solid rgba(45,125,98,0.1);
    font-size:.95rem;
  }}
  .sale-item:last-child{{border-bottom:none}}
  .sale-amt{{color:#2d7d62;font-weight:700}}
  .empty-state{{
    text-align:center;padding:2rem;color:#2a4a3a;font-size:.95rem;
  }}
</style>
</head>
<body>

<header>
  <div class="logo-title">
    <span>🌿</span>
    <h1>تسجيل المبيعات</h1>
  </div>
  <a href="/logout" class="logout">خروج ↩</a>
</header>

<div class="date-bar" id="dateBar">📅 جاري تحميل التاريخ...</div>

{success_html}
{error_html}

<div class="card">
  <div class="card-title">🛒 بيع جديد</div>
  <form method="POST" action="/worker/add-sale">
    <div class="field">
      <label>وصف البيع</label>
      <textarea name="desc" placeholder="مثال: باقة ورد أحمر، زهور مختلطة..." required></textarea>
    </div>
    <div class="field">
      <label>المبلغ (ر.ع)</label>
      <input type="number" name="amt" step="0.001" min="0" placeholder="0.000" required>
    </div>
    <div class="field">
      <label>الرف</label>
      <select name="shelf_id">
        <option value="">-- اختاري الرف (اختياري) --</option>
        {shelves_opts}
      </select>
    </div>
    <div class="field">
      <label>طريقة الدفع</label>
      <div class="payment-opts">
        <div class="pay-btn active" onclick="selectPay(this,'نقد')">💵 نقد</div>
        <div class="pay-btn" onclick="selectPay(this,'بطاقة')">💳 بطاقة</div>
        <div class="pay-btn" onclick="selectPay(this,'تحويل')">📲 تحويل</div>
      </div>
      <input type="hidden" name="payment_method" id="payMethod" value="نقد">
    </div>
    <button type="submit" class="submit-btn">تسجيل البيع ✓</button>
  </form>
</div>

<div class="card">
  <div class="card-title">📋 مبيعات اليوم</div>
  <div id="todaySales" class="today-sales">
    <div class="empty-state">جاري التحميل...</div>
  </div>
</div>

<script>
// التاريخ
const now = new Date();
const opts = {{weekday:'long',year:'numeric',month:'long',day:'numeric'}};
document.getElementById('dateBar').textContent =
  '📅 ' + now.toLocaleDateString('ar-OM', opts);

// اختيار طريقة الدفع
function selectPay(el, val){{
  document.querySelectorAll('.pay-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('payMethod').value = val;
}}

// تحميل مبيعات اليوم
async function loadTodaySales(){{
  try{{
    const res = await fetch('/worker/today-sales');
    const data = await res.json();
    const wrap = document.getElementById('todaySales');
    if(!data.sales || data.sales.length === 0){{
      wrap.innerHTML = '<div class="empty-state">لا توجد مبيعات اليوم بعد</div>';
      return;
    }}
    let html = '';
    let total = 0;
    data.sales.forEach(s=>{{
      total += s.amt;
      const pay = s.payment_method ? ` · ${{s.payment_method}}` : '';
      html += `<div class="sale-item">
        <span>${{s.desc}}${{pay}}</span>
        <span class="sale-amt">${{s.amt.toFixed(3)}} ر.ع</span>
      </div>`;
    }});
    html += `<div class="sale-item" style="font-weight:700;color:#a8e6cf;border-top:1px solid rgba(45,125,98,0.3);margin-top:.5rem">
      <span>الإجمالي (${{data.sales.length}} عمليات)</span>
      <span class="sale-amt">${{total.toFixed(3)}} ر.ع</span>
    </div>`;
    wrap.innerHTML = html;
  }}catch(e){{
    document.getElementById('todaySales').innerHTML =
      '<div class="empty-state">تعذّر تحميل البيانات</div>';
  }}
}}
loadTodaySales();
</script>
</body>
</html>"""
