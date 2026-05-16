from config import *

WORKER_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>فيروز فلورز — العامل</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
body{font-family:'Tajawal',sans-serif;background:#fdf8f2;color:#3d2c24;min-height:100vh;overflow-x:hidden;}

/* Header */
.wh{background:#fff;border-bottom:2px solid #f9c8d0;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:50;box-shadow:0 2px 12px rgba(232,121,138,.12);}
.wh-brand{display:flex;align-items:center;gap:10px;}
.wh-logo{width:42px;height:42px;background:linear-gradient(135deg,#e8798a,#c4566a);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;}
.wh-title{font-size:16px;font-weight:900;color:#c4566a;}
.wh-sub{font-size:13px;color:#b09888;}
.logout-w{background:#fce4ec;border:none;border-radius:10px;color:#c4566a;font-size:14px;font-weight:700;padding:9px 16px;cursor:pointer;font-family:'Tajawal',sans-serif;}

/* Toast */
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(90px);background:#3d2c24;color:#fff;padding:12px 28px;border-radius:40px;font-size:14px;font-weight:700;z-index:9999;transition:transform .4s cubic-bezier(.34,1.56,.64,1);white-space:nowrap;}
.toast.show{transform:translateX(-50%) translateY(0);}

/* Main screens */
.screen{display:none;padding:16px 14px 100px;}
.screen.on{display:block;}

/* Home nav buttons */
.nav-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px;}
.nav-btn{border:none;border-radius:22px;padding:28px 16px 22px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:10px;font-family:'Tajawal',sans-serif;transition:transform .2s cubic-bezier(.34,1.56,.64,1),box-shadow .2s;box-shadow:0 4px 20px rgba(0,0,0,.1);-webkit-appearance:none;}
.nav-btn:active{transform:scale(0.95);}
.nav-btn .nb-ico{font-size:48px;line-height:1;}
.nav-btn .nb-txt{font-size:17px;font-weight:900;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.2);}
.nav-btn .nb-sub{font-size:13px;color:rgba(255,255,255,0.8);font-weight:600;}
.nb-sale{background:linear-gradient(135deg,#7aab8a,#5a8a6a);box-shadow:0 6px 24px rgba(90,138,106,.35);}
.nb-buy{background:linear-gradient(135deg,#e8798a,#c4566a);box-shadow:0 6px 24px rgba(232,121,138,.35);}
.nb-flower{background:linear-gradient(135deg,#d4a843,#b8891f);box-shadow:0 6px 24px rgba(212,168,67,.35);}
.nb-inv{background:linear-gradient(135deg,#9664dc,#7a44c0);box-shadow:0 6px 24px rgba(150,100,220,.35);}

/* Screen header */
.sc-hdr{display:flex;align-items:center;gap:12px;margin-bottom:20px;}
.sc-back{background:#fff;border:1px solid #f9c8d0;border-radius:12px;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;flex-shrink:0;}
.sc-title{font-size:20px;font-weight:900;}

/* Big input fields */
.big-field{background:#fff;border:2px solid #f9c8d0;border-radius:16px;padding:16px;margin-bottom:14px;}
.big-field label{font-size:13px;font-weight:700;color:#b09888;letter-spacing:1px;display:block;margin-bottom:8px;}
.big-field input{width:100%;border:none;outline:none;font-family:'Tajawal',sans-serif;font-size:22px;font-weight:900;color:#3d2c24;background:transparent;}
.big-field input::placeholder{color:#d4c4b8;font-size:18px;font-weight:600;}

/* Big choice buttons */
.choice-lbl{font-size:13px;font-weight:700;color:#b09888;letter-spacing:1px;margin-bottom:10px;display:block;}
.choice-grid{display:grid;gap:10px;margin-bottom:16px;}
.choice-grid.g2{grid-template-columns:1fr 1fr;}
.choice-grid.g3{grid-template-columns:1fr 1fr 1fr;}
.choice-btn{border:2px solid #f9c8d0;border-radius:16px;background:#fff;padding:12px 8px;cursor:pointer;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:800;color:#7a6458;display:flex;flex-direction:column;align-items:center;gap:7px;transition:.2s;-webkit-appearance:none;}
.choice-btn .cb-ico{font-size:28px;}
.choice-btn .cb-img{width:54px;height:54px;border-radius:12px;object-fit:cover;display:block;background:#f5ede0;}
.choice-btn.sel{border-color:var(--sel-clr,#e8798a);background:var(--sel-bg,#fce4ec);color:var(--sel-clr,#c4566a);}
.choice-btn.sel .cb-img{box-shadow:0 0 0 3px var(--sel-clr,#e8798a);}

/* Submit button */
.sub-btn{width:100%;padding:18px;border:none;border-radius:16px;font-family:'Tajawal',sans-serif;font-size:18px;font-weight:900;cursor:pointer;transition:all .3s cubic-bezier(.34,1.56,.64,1);-webkit-appearance:none;display:flex;align-items:center;justify-content:center;gap:8px;margin-top:6px;}
.sub-btn:active{transform:scale(0.97);}
.sub-s{background:linear-gradient(135deg,#7aab8a,#5a8a6a);color:#fff;box-shadow:0 6px 24px rgba(90,138,106,.4);}
.sub-b{background:linear-gradient(135deg,#e8798a,#c4566a);color:#fff;box-shadow:0 6px 24px rgba(232,121,138,.4);}
.sub-gold{background:linear-gradient(135deg,#d4a843,#b8891f);color:#fff;box-shadow:0 6px 24px rgba(212,168,67,.4);}
.sub-purple{background:linear-gradient(135deg,#9664dc,#7a44c0);color:#fff;box-shadow:0 6px 24px rgba(150,100,220,.4);}

/* Success card */
.done-card{background:#fff;border:2px solid #c8e6c9;border-radius:20px;padding:28px;text-align:center;margin-bottom:20px;display:none;}
.done-card .done-ico{font-size:60px;margin-bottom:10px;}
.done-card .done-txt{font-size:18px;font-weight:900;color:#5a8a6a;margin-bottom:6px;}
.done-card .done-sub{font-size:13px;color:#7a6458;}
.done-card .done-again{margin-top:16px;padding:13px 28px;border:none;border-radius:12px;background:#e8f5e9;color:#5a8a6a;font-family:'Tajawal',sans-serif;font-size:14px;font-weight:800;cursor:pointer;}

/* Flower count screen */
.flower-type-card{background:#fff;border:2px solid #f9c8d0;border-radius:16px;padding:14px;margin-bottom:10px;display:flex;align-items:center;gap:12px;}
.flower-type-ico{font-size:30px;flex-shrink:0;}
.flower-type-name{flex:1;font-size:15px;font-weight:800;color:#3d2c24;}
.flower-qty-wrap{display:flex;align-items:center;gap:8px;}
.qty-btn{width:38px;height:38px;border-radius:10px;border:2px solid #f9c8d0;background:#fff;font-size:22px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#c4566a;-webkit-appearance:none;}
.qty-inp{width:52px;text-align:center;border:2px solid #f9c8d0;border-radius:10px;font-family:'Tajawal',sans-serif;font-size:17px;font-weight:900;color:#3d2c24;padding:6px 4px;outline:none;}

/* Invoice items */
.inv-item-row{background:#fff;border:1px solid #f9c8d0;border-radius:14px;padding:12px 14px;margin-bottom:8px;display:flex;align-items:center;gap:10px;}
.inv-item-name{flex:1;font-size:13px;font-weight:700;color:#3d2c24;}
.inv-item-qty-wrap{display:flex;align-items:center;gap:6px;}
.inv-item-qty{width:46px;text-align:center;border:1px solid #f9c8d0;border-radius:8px;font-family:'Tajawal',sans-serif;font-size:14px;font-weight:800;color:#3d2c24;padding:5px 4px;outline:none;}
.add-inv-item-btn{width:100%;padding:12px;border:2px dashed #f9c8d0;border-radius:14px;background:transparent;color:#b09888;font-family:'Tajawal',sans-serif;font-size:14px;font-weight:700;cursor:pointer;margin-bottom:14px;}

/* Day summary bar */
.day-bar{background:#fff;border:1px solid #f9c8d0;border-radius:16px;padding:14px 16px;display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}
.day-stat{text-align:center;}
.day-stat .ds-val{font-size:20px;font-weight:900;}
.day-stat .ds-lbl{font-size:13px;color:#b09888;margin-top:2px;}
.ds-s .ds-val{color:#5a8a6a;}
.ds-b .ds-val{color:#c4566a;}
</style>
</head>
<body>

<div class="wh">
  <div class="wh-brand">
    <div class="wh-logo">🌹</div>
    <div>
      <div class="wh-title">فيروز فلورز</div>
      <div class="wh-sub">واجهة العامل</div>
    </div>
  </div>
  <button class="logout-w" onclick="location.href='/worker-logout'">خروج 🔒</button>
</div>

<!-- HOME -->
<div class="screen on" id="sc-home">
  <div style="text-align:center;padding:20px 0 16px;">
    <div style="font-size:28px;font-weight:900;color:#c4566a;">مرحباً 👋</div>
    <div style="font-size:13px;color:#b09888;margin-top:4px;">اختر العملية</div>
  </div>

  <!-- إجمالي اليوم -->
  <div class="day-bar" id="dayBar">
    <div class="day-stat ds-s"><div class="ds-val" id="wDaySales">—</div><div class="ds-lbl">💰 مبيعات اليوم</div></div>
    <div class="day-stat ds-b"><div class="ds-val" id="wDayBuys">—</div><div class="ds-lbl">🛒 مشتريات اليوم</div></div>
  </div>

  <div class="nav-grid">
    <button class="nav-btn nb-sale" onclick="go('sale')">
      <div class="nb-ico">🌸</div>
      <div class="nb-txt">مبيعة</div>
      <div class="nb-sub">تسجيل بيع</div>
    </button>
    <button class="nav-btn nb-buy" onclick="go('buy')">
      <div class="nb-ico">📦</div>
      <div class="nb-txt">مشتريات</div>
      <div class="nb-sub">تسجيل شراء</div>
    </button>
    <button class="nav-btn nb-flower" onclick="go('flower')">
      <div class="nb-ico">🌹</div>
      <div class="nb-txt">عد الورد</div>
      <div class="nb-sub">تحديث المخزون</div>
    </button>
    <button class="nav-btn nb-inv" onclick="go('invoice')">
      <div class="nb-ico">🧾</div>
      <div class="nb-txt">فاتورة ورد</div>
      <div class="nb-sub">إضافة فاتورة</div>
    </button>
  </div>
</div>

<!-- SALE SCREEN -->
<div class="screen" id="sc-sale">
  <div class="sc-hdr">
    <div class="sc-back" onclick="go('home')">←</div>
    <div class="sc-title" style="color:#5a8a6a;">🌸 تسجيل مبيعة</div>
  </div>

  <!-- بطاقة النجاح -->
  <div class="done-card" id="sale-done">
    <div class="done-ico">✅</div>
    <div class="done-txt" id="sale-done-txt">تم التسجيل!</div>
    <div class="done-sub" id="sale-done-sub"></div>
    <button class="done-again" onclick="resetSale()">➕ تسجيل مبيعة أخرى</button>
  </div>

  <div id="sale-form">
    <span class="choice-lbl">📦 نوع المنتج</span>
    <div class="choice-grid g2" id="cat-grid"></div>

    <div class="big-field">
      <label>💰 السعر (ر.ع)</label>
      <input type="number" id="s-amt" placeholder="0.000" step="0.001" inputmode="decimal"/>
    </div>

    <span class="choice-lbl">💳 طريقة الدفع</span>
    <div class="choice-grid g3">
      <button class="choice-btn" style="--sel-clr:#5a8a6a;--sel-bg:#e8f5e9;" data-pay="كاش 💵" onclick="selPay(this)"><div class="cb-ico">💵</div>كاش</button>
      <button class="choice-btn" style="--sel-clr:#4a7ab0;--sel-bg:#e3f2fd;" data-pay="فيزا 💳" onclick="selPay(this)"><div class="cb-ico">💳</div>فيزا</button>
      <button class="choice-btn" style="--sel-clr:#7a44c0;--sel-bg:#f3e5ff;" data-pay="تحويل 🏦" onclick="selPay(this)"><div class="cb-ico">🏦</div>تحويل</button>
    </div>

    <button class="sub-btn sub-s" onclick="submitSale()">✅ تسجيل المبيعة</button>
  </div>
</div>

<!-- BUY SCREEN -->
<div class="screen" id="sc-buy">
  <div class="sc-hdr">
    <div class="sc-back" onclick="go('home')">←</div>
    <div class="sc-title" style="color:#c4566a;">📦 تسجيل مشتريات</div>
  </div>

  <div class="done-card" id="buy-done">
    <div class="done-ico">✅</div>
    <div class="done-txt">تم التسجيل!</div>
    <div class="done-sub" id="buy-done-sub"></div>
    <button class="done-again" onclick="resetBuy()">➕ تسجيل مشتريات أخرى</button>
  </div>

  <div id="buy-form">
    <span class="choice-lbl">📦 نوع المشتريات</span>
    <div class="choice-grid g2" id="buy-cat-grid"></div>

    <div class="big-field">
      <label>💰 المبلغ (ر.ع)</label>
      <input type="number" id="b-amt" placeholder="0.000" step="0.001" inputmode="decimal"/>
    </div>

    <span class="choice-lbl">👤 من دفع؟</span>
    <div class="choice-grid g2">
      <button class="choice-btn" style="--sel-clr:#5a8a6a;--sel-bg:#e8f5e9;" data-payer="حسين" onclick="selPayer(this)"><div class="cb-ico">👤</div>حسين</button>
      <button class="choice-btn" style="--sel-clr:#9664dc;--sel-bg:#f3e5ff;" data-payer="شوق" onclick="selPayer(this)"><div class="cb-ico">👤</div>شوق</button>
    </div>

    <button class="sub-btn sub-b" onclick="submitBuy()">✅ تسجيل المشتريات</button>
  </div>
</div>

<!-- FLOWER SCREEN -->
<div class="screen" id="sc-flower">
  <div class="sc-hdr">
    <div class="sc-back" onclick="go('home')">←</div>
    <div class="sc-title" style="color:#d4a843;">🌹 عد الورد</div>
  </div>

  <div class="done-card" id="flower-done">
    <div class="done-ico">🌹</div>
    <div class="done-txt">تم تحديث المخزون!</div>
    <div class="done-sub">تم حفظ عدد الورود</div>
    <button class="done-again" onclick="resetFlower()">🔄 تحديث مرة أخرى</button>
  </div>

  <div id="flower-form">
    <!-- زر رفع صورة الورد -->
    <div style="background:#fff7f0;border:2px dashed #f9c8d0;border-radius:16px;padding:16px;margin-bottom:16px;text-align:center;">
      <div style="font-size:13px;font-weight:800;color:#7a6458;margin-bottom:10px;">📷 رفع صورة الورد للتحليل التلقائي</div>
      <div style="font-size:11px;color:#b09888;margin-bottom:12px;">صوّر الورد وسيتم احتساب العدد تلقائياً</div>
      <input type="file" id="flower-img-input" accept="image/*" capture="environment" style="display:none;" onchange="handleFlowerImage(this)"/>
      <button class="sub-btn sub-gold" style="margin:0;padding:12px 20px;font-size:13px;" onclick="document.getElementById('flower-img-input').click()">
        📸 التقط / اختر صورة
      </button>
      <div id="flower-scan-status" style="margin-top:10px;font-size:12px;color:#9664dc;min-height:18px;"></div>
    </div>

    <div style="font-size:12px;color:#b09888;margin-bottom:14px;text-align:center;line-height:1.8;">
      أو أدخل العدد يدوياً 👇
    </div>
    <div id="flower-list"></div>
    <button class="sub-btn sub-gold" onclick="submitFlower()">💾 حفظ العدد</button>
  </div>
</div>

<!-- INVOICE SCREEN -->
<div class="screen" id="sc-invoice">
  <div class="sc-hdr">
    <div class="sc-back" onclick="go('home')">←</div>
    <div class="sc-title" style="color:#9664dc;">🧾 فاتورة ورد</div>
  </div>

  <!-- حالة النجاح -->
  <div class="done-card" id="inv-done" style="display:none;">
    <div class="done-ico">✅</div>
    <div class="done-txt">تم حفظ الفاتورة!</div>
    <div class="done-sub" id="inv-done-sub"></div>
    <button class="done-again" onclick="resetInvoice()">📷 رفع فاتورة أخرى</button>
  </div>

  <!-- زر الرفع -->
  <div id="inv-upload-area" style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px;gap:20px;">
    <div style="font-size:72px;line-height:1;">📷</div>
    <div style="text-align:center;color:var(--text2);font-size:15px;font-weight:700;">ارفع صورة فاتورة الورد</div>
    <div style="text-align:center;color:var(--text3);font-size:12px;">سيتم تحليلها تلقائياً وتسجيلها في فواتير الورد</div>
    <input type="file" id="inv-img-input" accept="image/*" capture="environment" style="display:none;" onchange="handleInvImage(this)"/>
    <button class="sub-btn sub-purple" style="max-width:280px;width:100%;" onclick="document.getElementById('inv-img-input').click()">
      📸 اختر صورة / التقط
    </button>
  </div>

  <!-- حالة التحليل -->
  <div id="inv-scanning" style="display:none;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;gap:16px;">
    <div style="font-size:48px;animation:spin 1s linear infinite;display:inline-block;">⏳</div>
    <div style="color:var(--text2);font-weight:700;font-size:15px;">جاري تحليل الفاتورة...</div>
    <div style="color:var(--text3);font-size:12px;">لحظة من فضلك</div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const CAT_SALE=[
  {img:'https://images.unsplash.com/photo-1490750967868-88df5691cc41?w=120&q=70',name:'ورد وباقات',val:'ورد وباقات'},
  {img:'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=120&q=70',name:'تاجات',val:'تاجات'},
  {img:'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=120&q=70',name:'هدايا',val:'هدايا'},
  {img:'https://images.unsplash.com/photo-1541643600914-78b084683702?w=120&q=70',name:'عطور',val:'عطور'},
  {img:'https://images.unsplash.com/photo-1611085583191-a3b181a88401?w=120&q=70',name:'اكسسوارات',val:'اكسسوارات'},
  {img:'https://images.unsplash.com/photo-1612838320302-4b3b3996765e?w=120&q=70',name:'طباعة',val:'طباعة'},
  {img:'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?w=120&q=70',name:'مجفف',val:'تجفيف'},
  {img:'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=120&q=70',name:'أخرى',val:'أخرى'},
];
const CAT_BUY=[
  {ico:'🌹',name:'ورد طازج',val:'ورد طازج'},
  {ico:'🌿',name:'نباتات',val:'نباتات'},
  {ico:'🎀',name:'لوازم باقات',val:'لوازم باقات'},
  {ico:'🧴',name:'مواد عطرية',val:'مواد عطرية'},
  {ico:'📦',name:'تغليف',val:'تغليف'},
  {ico:'✨',name:'أخرى',val:'أخرى'},
];
const COMPANIES=[
  {ico:'🏪',name:'نانا هايبر',val:'نانا هايبر'},
  {ico:'🌺',name:'سوق الورد',val:'سوق الورد'},
  {ico:'🌸',name:'مورد آخر',val:''},
];
const FLOWER_TYPES=[
  {ico:'🌹',name:'ورد أحمر'},
  {ico:'🌸',name:'ورد وردي'},
  {ico:'🤍',name:'ورد أبيض'},
  {ico:'🌼',name:'ورد أصفر'},
  {ico:'🌺',name:'ورد برتقالي'},
  {ico:'💜',name:'ورد بنفسجي'},
  {ico:'🌿',name:'جبسون (بندلة)'},
  {ico:'🌾',name:'ليموناي (بندلة)'},
];

let selCat='', selPay_='', selPayer_='', selCompany='';
const fmt=n=>(+n).toLocaleString('ar-OM',{minimumFractionDigits:3,maximumFractionDigits:3});

function go(sc){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('on'));
  document.getElementById('sc-'+(sc==='home'?'home':sc)).classList.add('on');
  if(sc==='home') loadDaySummary();
  if(sc==='flower') loadFlowerTypes();
}

function showToast(msg,ms=3000){
  const t=document.getElementById('toast');
  t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),ms);
}

async function api(url,opts){
  const r=await fetch(url,opts);
  return r.json();
}

// ── DAY SUMMARY ──
async function loadDaySummary(){
  try{
    const today=new Date();
    const day=String(today.getDate()).padStart(2,'0')+'/'+String(today.getMonth()+1).padStart(2,'0')+'/'+today.getFullYear();
    const month=today.getFullYear()+'-'+String(today.getMonth()+1).padStart(2,'0');
    const d=await api('/api/entries?month='+month);
    const sales=(d.sales||[]).filter(e=>e.date===day);
    const buys=(d.buys||[]).filter(e=>e.date===day);
    const ts=sales.reduce((a,e)=>a+e.amt,0);
    const tb=buys.reduce((a,e)=>a+e.amt,0);
    document.getElementById('wDaySales').textContent=fmt(ts)+' ر.ع';
    document.getElementById('wDayBuys').textContent=fmt(tb)+' ر.ع';
  }catch(e){}
}

// ── BUILD GRIDS ──
function buildCatGrid(){
  document.getElementById('cat-grid').innerHTML=CAT_SALE.map(c=>`
    <button class="choice-btn" style="--sel-clr:#5a8a6a;--sel-bg:#e8f5e9;" data-cat="${c.val}" onclick="selCatBtn(this)">
      <img class="cb-img" src="${c.img}" alt="${c.name}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='block'"/><span class="cb-ico" style="display:none">🌸</span>${c.name}
    </button>`).join('');
  document.getElementById('buy-cat-grid').innerHTML=CAT_BUY.map(c=>`
    <button class="choice-btn" style="--sel-clr:#c4566a;--sel-bg:#fce4ec;" data-cat="${c.val}" onclick="selBuyCat(this)">
      <div class="cb-ico">${c.ico}</div>${c.name}
    </button>`).join('');
  if(document.getElementById('company-grid'))
  document.getElementById('company-grid').innerHTML=COMPANIES.map(c=>`
    <button class="choice-btn" style="--sel-clr:#9664dc;--sel-bg:#f3e5ff;" data-company="${c.val}" onclick="selCompanyBtn(this)">
      <div class="cb-ico">${c.ico}</div>${c.name}
    </button>`).join('');
}

function selCatBtn(el){selCat=el.dataset.cat;document.querySelectorAll('#cat-grid .choice-btn').forEach(b=>b.classList.remove('sel'));el.classList.add('sel');}
function selBuyCat(el){selCat=el.dataset.cat;document.querySelectorAll('#buy-cat-grid .choice-btn').forEach(b=>b.classList.remove('sel'));el.classList.add('sel');}
function selPay(el){selPay_=el.dataset.pay;document.querySelectorAll('[data-pay]').forEach(b=>b.classList.remove('sel'));el.classList.add('sel');}
function selPayer(el){selPayer_=el.dataset.payer;document.querySelectorAll('[data-payer]').forEach(b=>b.classList.remove('sel'));el.classList.add('sel');}
function selCompanyBtn(el){selCompany=el.dataset.company;document.getElementById('inv-company-other').value='';document.querySelectorAll('[data-company]').forEach(b=>b.classList.remove('sel'));el.classList.add('sel');}

// ── FLOWER TYPES ──
async function loadFlowerTypes(){
  try{
    const d=await api('/api/flowers');
    const existing=d.flowers||[];
    const types=FLOWER_TYPES.map(ft=>{
      const found=existing.find(f=>f.name===ft.name);
      return {...ft,qty:found?found.count:0,unit:ft.name.includes('بندلة')?'بندلة':'وردة'};
    });
    document.getElementById('flower-list').innerHTML=types.map((ft,i)=>`
      <div class="flower-type-card">
        <div class="flower-type-ico">${ft.ico}</div>
        <div class="flower-type-name">${ft.name}</div>
        <div class="flower-qty-wrap">
          <button class="qty-btn" onclick="adjQty(${i},-1)">−</button>
          <input class="qty-inp" id="fq-${i}" type="number" value="${ft.qty}" min="0" inputmode="numeric" data-unit="${ft.unit}"/>
          <button class="qty-btn" onclick="adjQty(${i},+1)">+</button>
        </div>
      </div>`).join('');
  }catch(e){
    document.getElementById('flower-list').innerHTML=FLOWER_TYPES.map((ft,i)=>`
      <div class="flower-type-card">
        <div class="flower-type-ico">${ft.ico}</div>
        <div class="flower-type-name">${ft.name}</div>
        <div class="flower-qty-wrap">
          <button class="qty-btn" onclick="adjQty(${i},-1)">−</button>
          <input class="qty-inp" id="fq-${i}" type="number" value="0" min="0" inputmode="numeric" data-unit="${ft.name.includes('بندلة')?'بندلة':'وردة'}"/>
          <button class="qty-btn" onclick="adjQty(${i},+1)">+</button>
        </div>
      </div>`).join('');
  }
}

function adjQty(i,d){
  const inp=document.getElementById('fq-'+i);
  const v=Math.max(0,(parseInt(inp.value)||0)+d);
  inp.value=v;
}

// ── SUBMIT SALE ──
async function submitSale(){
  const amt=parseFloat(document.getElementById('s-amt').value);
  if(!amt||amt<=0){showToast('⚠️ أدخل السعر');return;}
  if(!selCat){showToast('⚠️ اختر نوع المنتج');return;}
  if(!selPay_){showToast('⚠️ اختر طريقة الدفع');return;}
  try{
    const month=new Date().getFullYear()+'-'+String(new Date().getMonth()+1).padStart(2,'0');
    await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type:'s',desc:selCat,amt,payment_method:selPay_,category:selCat,month})});
    document.getElementById('sale-done-txt').textContent='✅ تم تسجيل المبيعة!';
    document.getElementById('sale-done-sub').textContent=selCat+' — '+fmt(amt)+' ر.ع — '+selPay_;
    document.getElementById('sale-form').style.display='none';
    document.getElementById('sale-done').style.display='block';
    loadDaySummary();
  }catch(e){showToast('❌ خطأ في التسجيل');}
}

function resetSale(){
  selCat='';selPay_='';
  document.getElementById('s-amt').value='';
  document.querySelectorAll('#sc-sale .choice-btn').forEach(b=>b.classList.remove('sel'));
  document.getElementById('sale-form').style.display='block';
  document.getElementById('sale-done').style.display='none';
}

// ── SUBMIT BUY ──
async function submitBuy(){
  const amt=parseFloat(document.getElementById('b-amt').value);
  if(!amt||amt<=0){showToast('⚠️ أدخل المبلغ');return;}
  if(!selCat){showToast('⚠️ اختر نوع المشتريات');return;}
  try{
    const month=new Date().getFullYear()+'-'+String(new Date().getMonth()+1).padStart(2,'0');
    await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type:'b',desc:selCat,amt,paid_by:selPayer_||null,category:selCat,month})});
    document.getElementById('buy-done-sub').textContent=selCat+' — '+fmt(amt)+' ر.ع'+(selPayer_?' — '+selPayer_:'');
    document.getElementById('buy-form').style.display='none';
    document.getElementById('buy-done').style.display='block';
    loadDaySummary();
  }catch(e){showToast('❌ خطأ في التسجيل');}
}

function resetBuy(){
  selCat='';selPayer_='';
  document.getElementById('b-amt').value='';
  document.querySelectorAll('#sc-buy .choice-btn').forEach(b=>b.classList.remove('sel'));
  document.getElementById('buy-form').style.display='block';
  document.getElementById('buy-done').style.display='none';
}

// ── FLOWER IMAGE SCAN ──
async function handleFlowerImage(input){
  const file=input.files[0];
  if(!file)return;
  const status=document.getElementById('flower-scan-status');
  status.textContent='⏳ جاري تحليل الصورة...';
  const scanBtn=input.previousElementSibling;
  scanBtn.disabled=true;
  try{
    const b64=await new Promise((res,rej)=>{
      const r=new FileReader();
      r.onload=()=>res(r.result.split(',')[1]);
      r.onerror=()=>rej(new Error('read error'));
      r.readAsDataURL(file);
    });
    const resp=await fetch('/api/flowers/scan',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({image:b64})
    });
    const d=await resp.json();
    if(d.ok||d.flowers){
      const flowers=d.flowers||[];
      // ملء الحقول تلقائياً
      FLOWER_TYPES.forEach((ft,i)=>{
        const found=flowers.find(f=>f.name===ft.name||f.name.includes(ft.name.split(' ')[0]));
        if(found){
          const inp=document.getElementById('fq-'+i);
          if(inp) inp.value=found.count||0;
        }
      });
      const total=flowers.reduce((a,f)=>a+(f.count||0),0);
      status.textContent='✅ تم التحليل! '+(total>0?'عُد '+total+' وردة':'تحقق من الأرقام يدوياً');
      status.style.color='#5a8a6a';
    }else{
      status.textContent='⚠️ '+(d.error||'لم يتمكن من التحليل، أدخل العدد يدوياً');
      status.style.color='#c4566a';
    }
  }catch(e){
    status.textContent='❌ خطأ في الاتصال';
    status.style.color='#c4566a';
  }
  scanBtn.disabled=false;
  input.value='';
}

// ── SUBMIT FLOWER ──
async function submitFlower(){
  const flowers=FLOWER_TYPES.map((ft,i)=>{
    const inp=document.getElementById('fq-'+i);
    const cnt=parseInt(inp?.value||0)||0;
    return {name:ft.name,count:cnt,unit:inp?.dataset?.unit||'وردة'};
  }).filter(f=>f.count>0);
  try{
    await api('/api/flowers',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({flowers})});
    document.getElementById('flower-form').style.display='none';
    document.getElementById('flower-done').style.display='block';
  }catch(e){showToast('❌ خطأ في الحفظ');}
}

function resetFlower(){
  document.getElementById('flower-form').style.display='block';
  document.getElementById('flower-done').style.display='none';
  loadFlowerTypes();
}

// ── SUBMIT INVOICE via image scan ──
async function handleInvImage(input){
  const file=input.files[0];
  if(!file)return;
  document.getElementById('inv-upload-area').style.display='none';
  document.getElementById('inv-scanning').style.display='flex';
  try{
    const b64=await new Promise((res,rej)=>{
      const r=new FileReader();
      r.onload=()=>res(r.result.split(',')[1]);
      r.onerror=()=>rej(new Error('read error'));
      r.readAsDataURL(file);
    });
    const resp=await fetch('/api/flower_invoices/scan',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({image:b64})
    });
    const d=await resp.json();
    if(d.ok||d.id){
      const company=d.company||'';
      const total=parseFloat(d.total||0);
      document.getElementById('inv-done-sub').textContent=(company||'مورد')+(total?' — '+fmt(total)+' ر.ع':'');
      document.getElementById('inv-scanning').style.display='none';
      document.getElementById('inv-done').style.display='flex';
    }else{
      showToast('❌ '+(d.error||'فشل التحليل، حاول مرة أخرى'));
      resetInvoice();
    }
  }catch(e){
    showToast('❌ خطأ في الاتصال');
    resetInvoice();
  }
  input.value='';
}

function resetInvoice(){
  document.getElementById('inv-upload-area').style.display='flex';
  document.getElementById('inv-scanning').style.display='none';
  document.getElementById('inv-done').style.display='none';
}

// Init
buildCatGrid();
loadDaySummary();
</script>
</body>
</html>"""
