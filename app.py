import os
import requests
from datetime import datetime
from flask import Flask, request, jsonify, Response

# PostgreSQL support
try:
    import psycopg2
    import psycopg2.extras
    USE_PG = bool(os.environ.get("DATABASE_URL"))
except ImportError:
    USE_PG = False

if not USE_PG:
    import sqlite3

app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>فيروز فلورز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root{
  --ink:#0d0a0e;--deep:#130f18;--surface:#1a1424;--card:#211932;--card2:#261d38;
  --border:rgba(255,255,255,.07);--border2:rgba(255,255,255,.13);
  --rose:#e8547a;--rose2:#f07090;--rglow:rgba(232,84,122,.25);
  --mint:#4ecdc4;--mglow:rgba(78,205,196,.2);
  --gold:#f5c842;--gglow:rgba(245,200,66,.2);
  --lav:#b794f4;--text:#f0eaf8;--text2:#a89bc2;--text3:#6b5f85;
  --pos:#4ade80;--neg:#fb7185;--cash:#34d399;--visa:#60a5fa;--transfer:#a78bfa;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Tajawal',sans-serif;background:var(--ink);color:var(--text);min-height:100vh;}
.bg{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;}
.orb{position:absolute;border-radius:50%;filter:blur(80px);opacity:.15;animation:drift 20s ease-in-out infinite alternate;}
.orb:nth-child(1){width:500px;height:500px;background:radial-gradient(circle,#e8547a,transparent);top:-10%;right:-5%;}
.orb:nth-child(2){width:400px;height:400px;background:radial-gradient(circle,#4ecdc4,transparent);bottom:5%;left:-5%;animation-delay:-10s;}
.orb:nth-child(3){width:280px;height:280px;background:radial-gradient(circle,#b794f4,transparent);top:45%;left:35%;animation-delay:-18s;}
@keyframes drift{to{transform:translate(30px,40px) scale(1.08);}}
#app{position:relative;z-index:1;}

/* HEADER */
header{padding:0 32px;height:70px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);background:rgba(13,10,14,.8);backdrop-filter:blur(20px);
  position:sticky;top:0;z-index:100;}
.brand{display:flex;align-items:center;gap:12px;}
.emblem{width:42px;height:42px;background:linear-gradient(135deg,var(--rose),var(--lav));border-radius:12px;
  display:flex;align-items:center;justify-content:center;font-size:20px;
  box-shadow:0 0 24px var(--rglow);animation:glow 3s ease-in-out infinite;}
@keyframes glow{0%,100%{box-shadow:0 0 24px var(--rglow);}50%{box-shadow:0 0 44px rgba(232,84,122,.5);}}
.bname{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;
  background:linear-gradient(90deg,#fff,var(--rose2),var(--lav));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.bsub{font-size:10px;color:var(--text3);letter-spacing:1px;}
.mpill{display:flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--border2);
  padding:7px 14px;border-radius:40px;transition:.2s;cursor:pointer;}
.mpill:hover{border-color:var(--rose);box-shadow:0 0 14px var(--rglow);}
.mpill label{font-size:11px;color:var(--text3);cursor:pointer;}
.mpill select{background:transparent;border:none;color:var(--text);font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;cursor:pointer;outline:none;}
.mpill select option{background:var(--deep);}

main{max-width:1200px;margin:0 auto;padding:32px 20px 64px;}

/* SECTION LABEL */
.slbl{font-size:10px;font-weight:700;color:var(--text3);letter-spacing:2.5px;text-transform:uppercase;
  margin-bottom:12px;display:flex;align-items:center;gap:10px;}
.slbl::after{content:'';flex:1;height:1px;background:var(--border);}

/* KPI */
.kpi-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:28px;}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:22px 20px;
  position:relative;overflow:hidden;cursor:default;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1),border-color .3s,box-shadow .3s;
  animation:fadeUp .5s ease both;}
.kpi:nth-child(2){animation-delay:.08s;}.kpi:nth-child(3){animation-delay:.16s;}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}
.kpi:hover{transform:translateY(-4px) scale(1.01);}
.ks:hover{border-color:var(--mint);box-shadow:0 8px 36px var(--mglow);}
.kb:hover{border-color:var(--rose);box-shadow:0 8px 36px var(--rglow);}
.kp:hover{border-color:var(--gold);box-shadow:0 8px 36px var(--gglow);}
.kpi-ico{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:14px;}
.ks .kpi-ico{background:rgba(78,205,196,.12);}
.kb .kpi-ico{background:rgba(232,84,122,.12);}
.kp .kpi-ico{background:rgba(245,200,66,.12);}
.kpi-lbl{font-size:11px;color:var(--text3);margin-bottom:5px;}
.kpi-val{font-size:28px;font-weight:900;letter-spacing:-1px;line-height:1;margin-bottom:8px;}
.ks .kpi-val{color:var(--mint);}
.kb .kpi-val{color:var(--rose2);}
.kp .kpi-val{color:var(--gold);}
.kpi-sub{font-size:11px;color:var(--text3);}
.badge{padding:2px 8px;border-radius:20px;font-size:10px;font-weight:700;}
.bp{background:rgba(74,222,128,.12);color:var(--pos);}
.bn{background:rgba(251,113,133,.12);color:var(--neg);}

/* PAY METHOD MINI STATS */
.pay-stats{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;}
.pay-chip{display:flex;align-items:center;gap:5px;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.pc-cash{background:rgba(52,211,153,.12);color:var(--cash);}
.pc-visa{background:rgba(96,165,250,.12);color:var(--visa);}
.pc-trans{background:rgba(167,139,250,.12);color:var(--transfer);}

/* PAYER STATS */
.payer-stats{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;}
.payer-chip{display:flex;align-items:center;gap:5px;padding:3px 10px;border-radius:20px;
  font-size:11px;font-weight:600;background:rgba(232,84,122,.1);color:var(--rose2);}

/* ADD CARD */
.add-card{background:var(--card);border:1px solid var(--border);border-radius:22px;padding:26px;
  margin-bottom:28px;animation:fadeUp .5s .2s ease both;}
.tabs{display:flex;gap:8px;background:var(--deep);border:1px solid var(--border);
  border-radius:12px;padding:4px;margin-bottom:22px;}
.tbtn{flex:1;padding:10px 16px;border:none;border-radius:9px;font-family:'Tajawal',sans-serif;
  font-size:14px;font-weight:700;cursor:pointer;transition:all .3s cubic-bezier(.34,1.56,.64,1);
  background:transparent;color:var(--text3);display:flex;align-items:center;justify-content:center;gap:7px;}
.ts{background:linear-gradient(135deg,rgba(78,205,196,.18),rgba(78,205,196,.08));color:var(--mint);
  box-shadow:inset 0 0 0 1px rgba(78,205,196,.25);}
.tb{background:linear-gradient(135deg,rgba(232,84,122,.18),rgba(232,84,122,.08));color:var(--rose2);
  box-shadow:inset 0 0 0 1px rgba(232,84,122,.25);}

/* FORM FIELDS */
.form-grid{display:grid;gap:12px;}
.fgs{grid-template-columns:1fr 1fr;}
.fg3{grid-template-columns:1fr 140px 160px;}
.fg4{grid-template-columns:1fr 140px 160px 160px;}
.fld{display:flex;flex-direction:column;gap:5px;}
.fld label{font-size:10px;font-weight:700;color:var(--text3);letter-spacing:1px;text-transform:uppercase;}
.fld input,.fld select{background:var(--deep);border:1px solid var(--border2);border-radius:10px;
  padding:10px 14px;font-family:'Tajawal',sans-serif;font-size:14px;color:var(--text);
  outline:none;transition:.2s;width:100%;}
.fld input:focus,.fld select:focus{border-color:var(--rose);box-shadow:0 0 0 3px var(--rglow);}
.fld input::placeholder{color:var(--text3);}
.fld select option{background:var(--deep);}

/* IMG UPLOAD */
.img-zone{border:2px dashed var(--border2);border-radius:12px;padding:14px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;
  cursor:pointer;position:relative;transition:.3s;text-align:center;min-height:80px;}
.img-zone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;}
.img-zone:hover{border-color:var(--mint);background:rgba(78,205,196,.04);}
.img-zone .iz-ico{font-size:22px;}
.img-zone .iz-txt{font-size:11px;color:var(--text2);}
.img-prev{position:relative;}
.img-prev img{width:100%;height:80px;object-fit:cover;border-radius:10px;border:1px solid var(--mint);}
.img-prev button{position:absolute;top:4px;left:4px;background:rgba(13,10,14,.85);border:none;
  border-radius:5px;color:#fff;font-size:12px;width:22px;height:22px;cursor:pointer;}

/* SUBMIT BTN */
.sbtn{height:44px;padding:0 24px;border:none;border-radius:10px;font-family:'Tajawal',sans-serif;
  font-size:14px;font-weight:700;cursor:pointer;transition:all .3s cubic-bezier(.34,1.56,.64,1);
  white-space:nowrap;display:flex;align-items:center;gap:6px;align-self:end;}
.sbs{background:linear-gradient(135deg,var(--mint),#2ba8a0);color:#0d0a0e;
  box-shadow:0 4px 16px var(--mglow);}
.sbs:hover{transform:translateY(-2px) scale(1.03);box-shadow:0 8px 24px rgba(78,205,196,.5);}
.sbb{background:linear-gradient(135deg,var(--rose),#c03060);color:#fff;
  box-shadow:0 4px 16px var(--rglow);}
.sbb:hover{transform:translateY(-2px) scale(1.03);box-shadow:0 8px 24px rgba(232,84,122,.5);}

/* PANELS */
.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:28px;}
.panel{background:var(--card);border:1px solid var(--border);border-radius:20px;
  overflow:hidden;animation:fadeUp .5s .35s ease both;display:flex;flex-direction:column;}
.ph{padding:16px 20px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);}
.ph-l{display:flex;align-items:center;gap:10px;}
.pico{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;}
.ps .pico{background:rgba(78,205,196,.14);}
.pb .pico{background:rgba(232,84,122,.14);}
.ptitle{font-size:13px;font-weight:700;}
.ps .ptitle{color:var(--mint);}
.pb .ptitle{color:var(--rose2);}
.pcnt{font-size:10px;font-weight:800;padding:2px 9px;border-radius:20px;}
.ps .pcnt{background:rgba(78,205,196,.14);color:var(--mint);}
.pb .pcnt{background:rgba(232,84,122,.14);color:var(--rose2);}
.pbody{padding:8px;flex:1;overflow-y:auto;max-height:300px;
  scrollbar-width:thin;scrollbar-color:var(--border2) transparent;}
.pbody::-webkit-scrollbar{width:3px;}
.pbody::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}
.empty{padding:32px 16px;text-align:center;color:var(--text3);}
.empty .ei{font-size:32px;margin-bottom:8px;opacity:.3;}
.empty p{font-size:12px;line-height:1.8;}

/* ENTRY ROW */
.entry{display:flex;align-items:center;gap:9px;padding:10px 8px;border-radius:10px;
  margin-bottom:2px;transition:background .2s;animation:ei .3s cubic-bezier(.34,1.56,.64,1) both;}
@keyframes ei{from{opacity:0;transform:scale(.9) translateY(-4px);}to{opacity:1;transform:scale(1) translateY(0);}}
.entry:hover{background:rgba(255,255,255,.03);}
.edot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.es .edot{background:var(--mint);box-shadow:0 0 6px var(--mint);}
.eb .edot{background:var(--rose2);box-shadow:0 0 6px var(--rose2);}
.eimg{width:38px;height:38px;border-radius:8px;object-fit:cover;flex-shrink:0;
  border:1px solid var(--border2);cursor:pointer;transition:transform .2s;}
.eimg:hover{transform:scale(1.1);}
.eph{width:38px;height:38px;border-radius:8px;background:var(--surface);
  border:1px solid var(--border);display:flex;align-items:center;justify-content:center;
  font-size:16px;flex-shrink:0;}
.einfo{flex:1;min-width:0;}
.edesc{font-size:12px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.emeta{display:flex;gap:6px;align-items:center;margin-top:3px;flex-wrap:wrap;}
.edate{font-size:10px;color:var(--text3);}
.epay-badge{font-size:9px;font-weight:700;padding:1px 6px;border-radius:10px;}
.epb-cash{background:rgba(52,211,153,.15);color:var(--cash);}
.epb-visa{background:rgba(96,165,250,.15);color:var(--visa);}
.epb-trans{background:rgba(167,139,250,.15);color:var(--transfer);}
.epb-payer{background:rgba(232,84,122,.12);color:var(--rose2);}
.eamt{font-size:13px;font-weight:800;white-space:nowrap;flex-shrink:0;}
.eamt.inc{color:var(--mint);}
.eamt.exp{color:var(--rose2);}
.delbtn{background:none;border:none;cursor:pointer;color:var(--text3);font-size:13px;
  width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;
  transition:.2s;flex-shrink:0;}
.delbtn:hover{background:rgba(251,113,133,.14);color:var(--neg);}

/* CHARTS ROW */
.charts-row{display:grid;grid-template-columns:2fr 1fr 1fr;gap:20px;margin-bottom:28px;}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:20px;
  padding:24px;animation:fadeUp .5s .45s ease both;}
.chart-card h3{font-size:13px;font-weight:700;margin-bottom:20px;display:flex;align-items:center;gap:8px;}
.chart-wrap{position:relative;}

/* LIGHTBOX */
.lb{display:none;position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:9000;
  align-items:center;justify-content:center;cursor:zoom-out;}
.lb.open{display:flex;}
.lb img{max-width:90vw;max-height:88vh;border-radius:14px;}

/* OVERLAY */
.overlay{display:none;position:fixed;inset:0;background:rgba(13,10,14,.88);
  backdrop-filter:blur(14px);z-index:500;align-items:center;justify-content:center;padding:20px;}
.overlay.open{display:flex;}
.modal{background:var(--card2);border:1px solid var(--border2);border-radius:22px;padding:32px;
  max-width:400px;width:100%;text-align:center;box-shadow:0 40px 100px rgba(0,0,0,.6);
  animation:mi .4s cubic-bezier(.34,1.56,.64,1);}
@keyframes mi{from{opacity:0;transform:scale(.82) translateY(20px);}to{opacity:1;transform:scale(1) translateY(0);}}
.mico{font-size:46px;margin-bottom:12px;}
.modal h3{font-size:18px;font-weight:800;margin-bottom:8px;}
.modal p{font-size:13px;color:var(--text2);margin-bottom:20px;line-height:1.7;}
.minput{width:100%;background:var(--surface);border:1px solid var(--border2);border-radius:10px;
  padding:12px 14px;font-family:'Tajawal',sans-serif;font-size:18px;font-weight:800;
  text-align:center;color:var(--text);outline:none;margin-bottom:16px;transition:.2s;}
.minput:focus{border-color:var(--rose);box-shadow:0 0 0 3px var(--rglow);}
.mbtns{display:flex;gap:10px;}
.mbtns button{flex:1;padding:11px;border:none;border-radius:10px;font-family:'Tajawal',sans-serif;
  font-size:14px;font-weight:700;cursor:pointer;transition:all .25s cubic-bezier(.34,1.56,.64,1);}
.bc{background:var(--surface);border:1px solid var(--border2)!important;color:var(--text2);}
.bcs{background:linear-gradient(135deg,var(--mint),#2ba8a0);color:#0d0a0e;}
.bcp{background:linear-gradient(135deg,var(--rose),#c03060);color:#fff;}

/* TOAST */
.toast{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(80px);
  background:var(--card2);border:1px solid var(--border2);color:var(--text);
  padding:10px 24px;border-radius:40px;font-size:13px;font-weight:600;
  box-shadow:0 12px 40px rgba(0,0,0,.5);transition:transform .4s cubic-bezier(.34,1.56,.64,1);
  z-index:9999;white-space:nowrap;}
.toast.show{transform:translateX(-50%) translateY(0);}

@media(max-width:768px){
  header{padding:0 14px;}
  main{padding:20px 12px 52px;}
  .kpi-row,.panels,.charts-row{grid-template-columns:1fr;gap:12px;}
  .fg3,.fg4,.fgs{grid-template-columns:1fr;}
  .kpi-val{font-size:22px;}
  .add-card{padding:18px;}
}
</style>
</head>
<body>
<div class="bg"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>
<div id="app">

<header>
  <div class="brand">
    <div class="emblem">🌹</div>
    <div><div class="bname">فيروز فلورز</div><div class="bsub">إدارة المشتريات والمبيعات</div></div>
  </div>
  <div class="mpill">
    <label>📅</label>
    <select id="msel" onchange="changeMonth()">
      <option value="2026-01">يناير 2026</option><option value="2026-02">فبراير 2026</option>
      <option value="2026-03">مارس 2026</option><option value="2026-04">أبريل 2026</option>
      <option value="2026-05" selected>مايو 2026</option><option value="2026-06">يونيو 2026</option>
      <option value="2026-07">يوليو 2026</option><option value="2026-08">أغسطس 2026</option>
      <option value="2026-09">سبتمبر 2026</option><option value="2026-10">أكتوبر 2026</option>
      <option value="2026-11">نوفمبر 2026</option><option value="2026-12">ديسمبر 2026</option>
    </select>
  </div>
</header>

<main>
  <!-- KPI -->
  <div class="slbl">ملخص الشهر</div>
  <div class="kpi-row">
    <div class="kpi ks">
      <div class="kpi-ico">💰</div>
      <div class="kpi-lbl">إجمالي المبيعات</div>
      <div class="kpi-val" id="kS">0 ر.ع</div>
      <div class="kpi-sub" id="kSc">0 عملية</div>
      <div class="pay-stats" id="payStats"></div>
    </div>
    <div class="kpi kb">
      <div class="kpi-ico">🛒</div>
      <div class="kpi-lbl">إجمالي المشتريات</div>
      <div class="kpi-val" id="kB">0 ر.ع</div>
      <div class="kpi-sub" id="kBc">0 عملية</div>
      <div class="payer-stats" id="payerStats"></div>
    </div>
    <div class="kpi kp">
      <div class="kpi-ico">📊</div>
      <div class="kpi-lbl">صافي الربح</div>
      <div class="kpi-val" id="kP">0 ر.ع</div>
      <div class="kpi-sub"><span id="kPb" class="badge">—</span></div>
    </div>
  </div>

  <!-- ADD -->
  <div class="slbl">إضافة جديد</div>
  <div class="add-card">
    <div class="tabs">
      <button class="tbtn ts" id="ts" onclick="setTab('s')">🌸 مبيعات</button>
      <button class="tbtn" id="tb" onclick="setTab('b')">📦 مشتريات</button>
    </div>

    <!-- SALES FORM -->
    <div id="sf">
      <div class="form-grid fgs" style="margin-bottom:12px;">
        <div class="fld">
          <label>صورة المنتج</label>
          <div class="img-zone" id="siz">
            <input type="file" accept="image/*" onchange="onSaleImg(event)"/>
            <div class="iz-ico">📸</div>
            <div class="iz-txt">صورة اختيارية</div>
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div class="fld">
            <label>اسم المنتج</label>
            <input id="sDesc" type="text" placeholder="باقة ورد، عطر..."/>
          </div>
          <div class="fld">
            <label>السعر (ر.ع)</label>
            <input id="sAmt" type="number" placeholder="0.000" step="0.001"/>
          </div>
        </div>
      </div>
      <div class="form-grid fgs" style="margin-bottom:16px;">
        <div class="fld">
          <label>💳 طريقة الدفع</label>
          <select id="sPay">
            <option value="">— اختر —</option>
            <option value="كاش 💵">💵 كاش</option>
            <option value="فيزا 💳">💳 فيزا</option>
            <option value="تحويل 🏦">🏦 تحويل</option>
          </select>
        </div>
        <div class="fld">
          <label>📝 ملاحظة</label>
          <input id="sNote" type="text" placeholder="اختياري"/>
        </div>
      </div>
      <button class="sbtn sbs" onclick="addSale()" style="width:100%;justify-content:center;">🌸 إضافة مبيعة</button>
    </div>

    <!-- BUYS FORM -->
    <div id="bf" style="display:none;">
      <div class="form-grid fg3" style="margin-bottom:12px;">
        <div class="fld">
          <label>الوصف / المورد</label>
          <input id="bDesc" type="text" placeholder="نانا هايبر، زهور..."/>
        </div>
        <div class="fld">
          <label>المبلغ (ر.ع)</label>
          <input id="bAmt" type="number" placeholder="0.000" step="0.001"/>
        </div>
        <div class="fld">
          <label>👤 من دفع؟</label>
          <select id="bPayer">
            <option value="">— اختر —</option>
            <option value="حسين">👤 حسين</option>
            <option value="شوق">👤 شوق</option>
            <option value="أخرى">➕ أخرى</option>
          </select>
        </div>
      </div>
      <div id="bOtherWrap" style="display:none;margin-bottom:12px;">
        <div class="fld">
          <label>اسم الشخص</label>
          <input id="bOther" type="text" placeholder="اكتب الاسم"/>
        </div>
      </div>
      <div class="form-grid fgs" style="margin-bottom:16px;">
        <div class="fld">
          <label>🧾 ارفع الفاتورة</label>
          <div style="border:2px dashed var(--border2);border-radius:10px;padding:10px;
            position:relative;text-align:center;font-size:12px;color:var(--text2);cursor:pointer;
            transition:.3s;" onmouseover="this.style.borderColor='var(--rose)'" onmouseout="this.style.borderColor='var(--border2)'">
            <input type="file" accept="image/*,.pdf" onchange="pickFile(event)"
              style="position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;"/>
            🧾 اختر صورة الفاتورة
          </div>
        </div>
        <div class="fld">
          <label>📝 ملاحظة</label>
          <input id="bNote" type="text" placeholder="اختياري"/>
        </div>
      </div>
      <button class="sbtn sbb" onclick="addBuy()" style="width:100%;justify-content:center;">📦 إضافة مشتريات</button>
    </div>
  </div>

  <!-- LISTS -->
  <div class="slbl">السجلات</div>
  <div class="panels">
    <div class="panel ps">
      <div class="ph">
        <div class="ph-l"><div class="pico">🌸</div><div class="ptitle">المبيعات</div></div>
        <div class="pcnt" id="sbadge">0</div>
      </div>
      <div class="pbody" id="sl"></div>
    </div>
    <div class="panel pb">
      <div class="ph">
        <div class="ph-l"><div class="pico">📦</div><div class="ptitle">المشتريات</div></div>
        <div class="pcnt" id="bbadge">0</div>
      </div>
      <div class="pbody" id="bl"></div>
    </div>
  </div>

  <!-- CHARTS -->
  <div class="slbl">الإحصائيات</div>
  <div class="charts-row">
    <div class="chart-card">
      <h3>📈 المبيعات والمشتريات — 2026</h3>
      <div class="chart-wrap"><canvas id="barChart" height="180"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>💳 طريقة الدفع</h3>
      <div class="chart-wrap"><canvas id="payChart" height="180"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>👤 من دفع المشتريات</h3>
      <div class="chart-wrap"><canvas id="payerChart" height="180"></canvas></div>
    </div>
  </div>
</main>
</div>

<div class="lb" id="lb" onclick="this.classList.remove('open')"><img id="lbImg" src=""/></div>
<div class="overlay" id="ov"><div class="modal" id="mb"></div></div>
<div class="toast" id="toast"></div>

<script>
let tab='s', month='2026-05';
let barChartInst=null, payChartInst=null, payerChartInst=null;

/* ── API ── */
async function api(url,opts){const r=await fetch(url,opts);return r.json();}

async function load(){
  const d=await api(`/api/entries?month=${month}`);
  renderKPI(d.sales,d.buys);
  renderLists(d.sales,d.buys);
  loadCharts();
}

async function loadCharts(){
  const ms=['01','02','03','04','05','06','07','08','09','10','11','12'];
  const yr=month.split('-')[0];
  const all=await Promise.all(ms.map(m=>api(`/api/entries?month=${yr}-${m}`)));
  const aS=all.map(d=>d.sales.reduce((a,e)=>a+e.amt,0));
  const aB=all.map(d=>d.buys.reduce((a,e)=>a+e.amt,0));
  renderBarChart(aS,aB);

  // Pay method breakdown for current month
  const cur=all[parseInt(month.split('-')[1])-1];
  renderPayChart(cur.sales);
  renderPayerChart(cur.buys);
}

setInterval(load,15000);

/* ── KPI ── */
function fmt(n){return (+n).toLocaleString('ar-OM',{minimumFractionDigits:3,maximumFractionDigits:3});}

function renderKPI(sales,buys){
  const ts=sales.reduce((a,e)=>a+e.amt,0);
  const tb=buys.reduce((a,e)=>a+e.amt,0);
  const tp=ts-tb;
  document.getElementById('kS').textContent=fmt(ts)+' ر.ع';
  document.getElementById('kSc').textContent=sales.length+' عملية';
  document.getElementById('kB').textContent=fmt(tb)+' ر.ع';
  document.getElementById('kBc').textContent=buys.length+' عملية';
  document.getElementById('kP').textContent=(tp>=0?'+':'')+fmt(tp)+' ر.ع';
  document.getElementById('kP').style.color=tp>=0?'var(--gold)':'var(--neg)';
  const b=document.getElementById('kPb');
  b.textContent=tp>0?'✅ في الربح':tp<0?'⚠️ في الخسارة':'—';
  b.className='badge '+(tp>0?'bp':tp<0?'bn':'');

  // Pay method chips
  const pm={};
  sales.forEach(e=>{const k=e.payment_method||'غير محدد';pm[k]=(pm[k]||0)+e.amt;});
  const psCls={'كاش 💵':'pc-cash','فيزا 💳':'pc-visa','تحويل 🏦':'pc-trans'};
  document.getElementById('payStats').innerHTML=Object.entries(pm)
    .filter(([k])=>k!=='غير محدد')
    .map(([k,v])=>`<div class="pay-chip ${psCls[k]||'pc-cash'}">${k} ${fmt(v)}</div>`).join('');

  // Payer chips
  const py={};
  buys.forEach(e=>{const k=e.paid_by||'غير محدد';py[k]=(py[k]||0)+e.amt;});
  document.getElementById('payerStats').innerHTML=Object.entries(py)
    .filter(([k])=>k!=='غير محدد')
    .map(([k,v])=>`<div class="payer-chip">👤 ${k}: ${fmt(v)}</div>`).join('');
}

/* ── LISTS ── */
function payBadge(pm){
  if(!pm) return '';
  const cls=pm.includes('كاش')?'epb-cash':pm.includes('فيزا')?'epb-visa':pm.includes('تحويل')?'epb-trans':'epb-cash';
  return `<span class="epay-badge ${cls}">${pm}</span>`;
}

function renderLists(sales,buys){
  document.getElementById('sl').innerHTML=sales.length?sales.map(e=>`
    <div class="entry es">
      ${e.img?`<img class="eimg" src="${e.img}" onclick="openLB('${e.img}')"/>`:`<div class="eph">🌸</div>`}
      <div class="einfo">
        <div class="edesc">${e.desc}</div>
        <div class="emeta">
          <span class="edate">${e.date}</span>
          ${payBadge(e.payment_method)}
          ${e.sale_time?`<span class="edate">🕐${e.sale_time}</span>`:''}
        </div>
      </div>
      <div class="eamt inc">+${fmt(e.amt)} ر.ع</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button>
    </div>`).join('')
    :`<div class="empty"><div class="ei">🌷</div><p>لا توجد مبيعات<br>أضف من هنا أو عبر التيليغرام</p></div>`;

  document.getElementById('bl').innerHTML=buys.length?buys.map(e=>`
    <div class="entry eb">
      <div class="edot"></div>
      <div class="einfo">
        <div class="edesc">${e.desc}</div>
        <div class="emeta">
          <span class="edate">${e.date}</span>
          ${e.paid_by?`<span class="epay-badge epb-payer">👤 ${e.paid_by}</span>`:''}
        </div>
      </div>
      <div class="eamt exp">-${fmt(e.amt)} ر.ع</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button>
    </div>`).join('')
    :`<div class="empty"><div class="ei">🌿</div><p>لا توجد مشتريات<br>أضف من هنا أو عبر التيليغرام</p></div>`;

  document.getElementById('sbadge').textContent=sales.length;
  document.getElementById('bbadge').textContent=buys.length;
}

/* ── CHARTS ── */
const months=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
const chartOpts={responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(255,255,255,.05)'},ticks:{color:'#6b5f85',font:{family:'Tajawal',size:10}}},y:{grid:{color:'rgba(255,255,255,.05)'},ticks:{color:'#6b5f85',font:{family:'Tajawal',size:10}}}}};

function renderBarChart(aS,aB){
  if(barChartInst) barChartInst.destroy();
  barChartInst=new Chart(document.getElementById('barChart'),{
    type:'bar',
    data:{
      labels:months.map(m=>m.slice(0,3)),
      datasets:[
        {label:'مبيعات',data:aS,backgroundColor:'rgba(78,205,196,.7)',borderRadius:4,borderSkipped:false},
        {label:'مشتريات',data:aB,backgroundColor:'rgba(232,84,122,.7)',borderRadius:4,borderSkipped:false}
      ]
    },
    options:{...chartOpts,plugins:{legend:{display:true,labels:{color:'#a89bc2',font:{family:'Tajawal',size:11}}}}}
  });
}

function renderPayChart(sales){
  const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};
  sales.forEach(e=>{const k=e.payment_method;if(k&&pm[k]!==undefined)pm[k]+=e.amt;});
  if(payChartInst) payChartInst.destroy();
  payChartInst=new Chart(document.getElementById('payChart'),{
    type:'doughnut',
    data:{
      labels:Object.keys(pm),
      datasets:[{data:Object.values(pm),backgroundColor:['rgba(52,211,153,.8)','rgba(96,165,250,.8)','rgba(167,139,250,.8)'],borderWidth:0,hoverOffset:6}]
    },
    options:{responsive:true,cutout:'65%',plugins:{legend:{position:'bottom',labels:{color:'#a89bc2',font:{family:'Tajawal',size:10},padding:8}}}}
  });
}

function renderPayerChart(buys){
  const py={};
  buys.forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});
  const colors=['rgba(232,84,122,.8)','rgba(78,205,196,.8)','rgba(245,200,66,.8)','rgba(183,148,244,.8)'];
  if(payerChartInst) payerChartInst.destroy();
  payerChartInst=new Chart(document.getElementById('payerChart'),{
    type:'doughnut',
    data:{
      labels:Object.keys(py).length?Object.keys(py):['لا يوجد'],
      datasets:[{data:Object.keys(py).length?Object.values(py):[1],backgroundColor:Object.keys(py).length?colors.slice(0,Object.keys(py).length):['rgba(107,95,133,.3)'],borderWidth:0,hoverOffset:6}]
    },
    options:{responsive:true,cutout:'65%',plugins:{legend:{position:'bottom',labels:{color:'#a89bc2',font:{family:'Tajawal',size:10},padding:8}}}}
  });
}

/* ── ADD ── */
function setTab(t){
  tab=t;
  document.getElementById('ts').className='tbtn'+(t==='s'?' ts':'');
  document.getElementById('tb').className='tbtn'+(t==='b'?' tb':'');
  document.getElementById('sf').style.display=t==='s'?'block':'none';
  document.getElementById('bf').style.display=t==='b'?'block':'none';
}

document.getElementById('bPayer').addEventListener('change',function(){
  document.getElementById('bOtherWrap').style.display=this.value==='أخرى'?'block':'none';
});

async function addSale(){
  const desc=document.getElementById('sDesc').value.trim()||'مبيعة';
  const amt=parseFloat(document.getElementById('sAmt').value);
  const pay=document.getElementById('sPay').value;
  const note=document.getElementById('sNote').value.trim();
  if(!amt||amt<=0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'s',desc:note?`${desc} — ${note}`:desc,amt,payment_method:pay||null,month})});
  document.getElementById('sDesc').value='';
  document.getElementById('sAmt').value='';
  document.getElementById('sPay').value='';
  document.getElementById('sNote').value='';
  window._sImg=null;
  resetSaleImg();
  load();showToast('✅ تمت إضافة المبيعة');
}

async function addBuy(){
  const desc=document.getElementById('bDesc').value.trim()||'مشتريات';
  const amt=parseFloat(document.getElementById('bAmt').value);
  let payer=document.getElementById('bPayer').value;
  if(payer==='أخرى') payer=document.getElementById('bOther').value.trim()||null;
  const note=document.getElementById('bNote').value.trim();
  if(!amt||amt<=0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'b',desc:note?`${desc} — ${note}`:desc,amt,paid_by:payer||null,month})});
  document.getElementById('bDesc').value='';
  document.getElementById('bAmt').value='';
  document.getElementById('bPayer').value='';
  document.getElementById('bNote').value='';
  load();showToast('✅ تمت إضافة المشتريات');
}

async function del(id){
  await api(`/api/entries/${id}`,{method:'DELETE'});
  load();showToast('🗑️ تم الحذف');
}

/* ── IMAGE ── */
function onSaleImg(ev){
  const file=ev.target.files[0];if(!file)return;
  const r=new FileReader();
  r.onload=e=>{
    window._sImg=e.target.result;
    document.getElementById('siz').innerHTML=`
      <div class="img-prev" style="width:100%">
        <img src="${e.target.result}"/>
        <button onclick="resetSaleImg(event)">✕</button>
      </div>`;
  };
  r.readAsDataURL(file);
}

function resetSaleImg(ev){
  if(ev)ev.stopPropagation();
  window._sImg=null;
  document.getElementById('siz').innerHTML=`
    <input type="file" accept="image/*" onchange="onSaleImg(event)"/>
    <div class="iz-ico">📸</div><div class="iz-txt">صورة اختيارية</div>`;
}

async function pickFile(ev){
  const file=ev.target.files[0];if(!file)return;ev.target.value='';
  const isImg=file.type.startsWith('image/');
  const isPdf=file.type==='application/pdf';
  if(!isImg&&!isPdf){showToast('⚠️ نوع الملف غير مدعوم');return;}
  let mediaHtml=isPdf
    ?`<div style="padding:20px;text-align:center;font-size:13px;color:var(--text2)">📄 ${file.name}</div>`
    :`<img src="${URL.createObjectURL(file)}" style="width:100%;border-radius:12px;max-height:300px;object-fit:contain;"/>`;
  openModal(`
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;text-align:right">
      <span style="font-size:24px">🧾</span>
      <div><div style="font-size:16px;font-weight:800">تفاصيل الفاتورة</div>
      <div style="font-size:11px;color:var(--text3)">اطّلع على الفاتورة وأدخل البيانات</div></div>
    </div>
    <div style="margin-bottom:14px">${mediaHtml}</div>
    <input class="minput" style="font-size:14px;margin-bottom:10px;text-align:right" id="mDesc" type="text" placeholder="اسم المورد / الوصف"/>
    <input class="minput" id="mAmt" type="number" placeholder="المبلغ الإجمالي (ر.ع)" step="0.001"/>
    <div class="mbtns">
      <button class="bc" onclick="closeModal()">إلغاء</button>
      <button class="bcp" onclick="confirmBuy()">➕ إضافة</button>
    </div>`);
}

async function confirmBuy(){
  const amt=parseFloat(document.getElementById('mAmt').value);
  const desc=document.getElementById('mDesc').value.trim()||'مشتريات';
  if(!amt||amt<=0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  let payer=document.getElementById('bPayer').value;
  if(payer==='أخرى') payer=document.getElementById('bOther').value.trim()||null;
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'b',desc,amt,paid_by:payer||null,month})});
  closeModal();load();showToast('✅ تمت إضافة الفاتورة');
}

/* ── MISC ── */
function changeMonth(){month=document.getElementById('msel').value;load();}
function openLB(src){document.getElementById('lbImg').src=src;document.getElementById('lb').classList.add('open');}
function openModal(html){document.getElementById('mb').innerHTML=html;document.getElementById('ov').classList.add('open');}
function closeModal(){document.getElementById('ov').classList.remove('open');}
document.getElementById('ov').addEventListener('click',function(e){if(e.target===this)closeModal();});
function showToast(msg){const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3000);}

load();
</script>
</body>
</html>
"""


BOT_TOKEN   = os.environ.get("BOT_TOKEN", "")
DB_PATH     = os.environ.get("DB_PATH", "fairuz.db")
GEMINI_KEY  = os.environ.get("GEMINI_API_KEY", "")
GROQ_KEY    = os.environ.get("GROQ_API_KEY", "")

# ── Database ──────────────────────────────────────────────
def get_db():
    if USE_PG:
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        return conn
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.row_factory = _sq.Row
        return conn

def init_db():
    if USE_PG:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id             SERIAL PRIMARY KEY,
                type           TEXT NOT NULL,
                desc           TEXT NOT NULL,
                amt            REAL NOT NULL,
                date           TEXT NOT NULL,
                month          TEXT NOT NULL,
                img            TEXT,
                paid_by        TEXT DEFAULT NULL,
                payment_method TEXT DEFAULT NULL,
                sale_time      TEXT DEFAULT NULL,
                created        TIMESTAMP DEFAULT NOW()
            )
        """)
        # Migrations
        for col in ["paid_by","payment_method","sale_time"]:
            try:
                cur.execute(f"ALTER TABLE entries ADD COLUMN IF NOT EXISTS {col} TEXT DEFAULT NULL")
            except:
                pass
        conn.commit()
        cur.close()
        conn.close()
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                type           TEXT NOT NULL,
                desc           TEXT NOT NULL,
                amt            REAL NOT NULL,
                date           TEXT NOT NULL,
                month          TEXT NOT NULL,
                img            TEXT,
                paid_by        TEXT DEFAULT NULL,
                payment_method TEXT DEFAULT NULL,
                sale_time      TEXT DEFAULT NULL,
                created        TEXT DEFAULT (datetime('now'))
            )
        """)
        for col in ["paid_by","payment_method","sale_time"]:
            try:
                conn.execute(f"ALTER TABLE entries ADD COLUMN {col} TEXT DEFAULT NULL")
            except:
                pass
        conn.commit()
        conn.close()

init_db()

# ── DB query helper ──────────────────────────────────────
def db_exec(sql, params=(), fetch=None):
    """Unified DB execute — handles both PG and SQLite."""
    if USE_PG:
        sql_pg = sql.replace("?", "%s")
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql_pg, params)
        result = None
        if fetch == "one":
            result = dict(cur.fetchone()) if cur.rowcount or cur.description else None
        elif fetch == "all":
            result = [dict(r) for r in cur.fetchall()]
        conn.commit(); cur.close(); conn.close()
        return result
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.row_factory = _sq.Row
        cur = conn.execute(sql, params)
        result = None
        if fetch == "one":
            row = cur.fetchone()
            result = dict(row) if row else None
        elif fetch == "all":
            result = [dict(r) for r in cur.fetchall()]
        conn.commit(); conn.close()
        return result

# ── Helpers ───────────────────────────────────────────────
def fmt_omr(n):
    return f"{n:,.3f} ر.ع"

def cur_month():
    return datetime.now().strftime("%Y-%m")

def get_month_data(month):
    if USE_PG:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM entries WHERE month=%s ORDER BY created DESC", (month,))
        rows = cur.fetchall()
        cur.close(); conn.close()
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.row_factory = _sq.Row
        rows = conn.execute(
            "SELECT * FROM entries WHERE month=? ORDER BY created DESC", (month,)
        ).fetchall()
        conn.close()
    sales = [dict(r) for r in rows if r["type"] == "s"]
    buys  = [dict(r) for r in rows if r["type"] == "b"]
    return sales, buys

def month_summary(month):
    sales, buys = get_month_data(month)
    ts = sum(e["amt"] for e in sales)
    tb = sum(e["amt"] for e in buys)
    return ts, tb, ts - tb, len(sales), len(buys)

# ── Simple NLP — no AI needed ─────────────────────────────
SALE_WORDS  = ["بعت","بعت","مبيعة","بيع","بعثت","باعت","وصل","استلم العميل"]
BUY_WORDS   = ["اشتريت","شريت","مشتريات","شراء","دفعت","فاتورة","طلبية"]

def parse_text(text):
    """Parse Arabic text to extract type, description and amount."""
    import re
    text = text.strip()

    # Detect type
    etype = None
    for w in SALE_WORDS:
        if w in text:
            etype = "s"
            break
    if not etype:
        for w in BUY_WORDS:
            if w in text:
                etype = "b"
                break

    # Extract amount smartly:
    # 1. Look for keywords like "الإجمالي" or "المجموع" or "بـ" followed by number
    # 2. Otherwise take the LARGEST number (likely the total)
    amt = None

    # Priority 1: explicit total keywords
    total_patterns = [
        r'الإجمالي[^\d]*(\d+[.,]\d+)',
        r'صافي الإجمالي[^\d]*(\d+[.,]\d+)',
        r'Net Total[^\d]*(\d+[.,]\d+)',
        r'المجموع[^\d]*(\d+[.,]\d+)',
        r'بـ\s*(\d+[.,]\d+)',
        r'بـ\s*(\d+)',
        r'ب\s*(\d+[.,]\d+)',
    ]
    for pat in total_patterns:
        m = re.search(pat, text)
        if m:
            try:
                amt = float(m.group(1).replace(',', '.'))
                if amt > 0:
                    break
            except:
                pass

    # Priority 2: largest number in text (likely the total)
    if not amt:
        nums = re.findall(r'\d+[.,]\d+|\d+', text.replace('٫','.'))
        candidates = []
        for n in nums:
            try:
                v = float(n.replace(',', '.'))
                if v > 0:
                    candidates.append(v)
            except:
                pass
        if candidates:
            amt = max(candidates)

    if etype and amt:
        # Build description from first line or key words
        first_line = text.split("\n")[0].strip()
        desc = first_line

        # Extract paid_by — look for "دفع X" or "من X" or "حسين" "شوق" etc
        paid_by = None
        paid_patterns = [
            r'دفع(?:ت)?\s+([\u0600-\u06FFa-zA-Z]+)',
            r'من\s+حساب\s+([\u0600-\u06FFa-zA-Z]+)',
            r'على\s+([\u0600-\u06FFa-zA-Z]+)',
        ]
        for pat in paid_patterns:
            m = re.search(pat, text)
            if m:
                paid_by = m.group(1).strip()
                break

        for w in SALE_WORDS + BUY_WORDS + ["بـ","ب","ريال","ر.ع","ومان","اغراض","أغراض"]:
            desc = desc.replace(w, " ")
        desc = re.sub(r'\d+(?:[.,]\d+)?', '', desc).strip()
        desc = ' '.join(desc.split()) or ("مبيعة" if etype == "s" else "مشتريات")
        return {"type": etype, "desc": desc, "amt": amt, "paid_by": paid_by, "found": True}

    return {"found": False}

# ── Gemini invoice reader (free) ─────────────────────────
def gemini_read_invoice(file_id):
    """Download image from Telegram and read it with Gemini (free)."""
    if not GEMINI_KEY or not BOT_TOKEN:
        return None
    try:
        import base64, json as _json
        # Get file from Telegram
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id}, timeout=10
        )
        file_path = r.json()["result"]["file_path"]
        img_bytes = requests.get(
            f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}",
            timeout=15
        ).content
        b64 = base64.b64encode(img_bytes).decode()

        # Call Gemini API (free tier)
        prompt = """هذه فاتورة. استخرج منها:
1. المبلغ الإجمالي (Net Total أو الإجمالي شامل الضريبة)
2. اسم المتجر أو وصف المشتريات

أجب فقط بـ JSON هكذا بدون أي نص إضافي:
{"amt": 3.520, "desc": "نانا هايبر - أدوات", "found": true}
إذا لم تكن فاتورة: {"found": false}"""

        res = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}",
            json={
                "contents": [{
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
                        {"text": prompt}
                    ]
                }]
            },
            timeout=20
        )
        raw = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        raw = raw.replace("```json","").replace("```","").strip()
        return _json.loads(raw)
    except Exception as e:
        print("Gemini error:", e)
        return None

# ── Groq sale receipt reader ─────────────────────────────
def groq_read_sale_receipt(file_id):
    """Read a sales receipt image and extract full details."""
    if not GROQ_KEY or not BOT_TOKEN:
        return None
    try:
        import base64, json as _json
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id}, timeout=10
        )
        file_path = r.json()["result"]["file_path"]
        img_bytes = requests.get(
            f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}",
            timeout=15
        ).content
        b64 = base64.b64encode(img_bytes).decode()

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                        {"type": "text", "text": """هذا إيصال بيع. استخرج منه كل التفاصيل التالية:
1. المبلغ الإجمالي
2. وصف المنتجات المباعة
3. طريقة الدفع (كاش أو فيزا أو تحويل أو غير محدد)
4. الوقت إن وجد
5. التاريخ إن وجد

أجب فقط بـ JSON بدون أي نص إضافي:
{"amt": 5.500, "desc": "باقة ورد حمراء", "payment": "كاش", "time": "10:30 AM", "date": "01/05/2026", "found": true}
إذا لم يكن إيصال بيع: {"found": false}"""}
                    ]
                }],
                "max_tokens": 300,
                "temperature": 0.1
            },
            timeout=20
        )
        raw = res.json()["choices"][0]["message"]["content"]
        raw = raw.replace("```json","").replace("```","").strip()
        return _json.loads(raw)
    except Exception as e:
        print("Groq sale error:", e)
        return None

# ── Groq invoice reader (free, no card needed) ───────────
def groq_read_invoice(file_id):
    """Download image from Telegram and read it with Groq (free)."""
    if not GROQ_KEY or not BOT_TOKEN:
        return None
    try:
        import base64, json as _json
        # Get file from Telegram
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
            params={"file_id": file_id}, timeout=10
        )
        file_path = r.json()["result"]["file_path"]
        img_bytes = requests.get(
            f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}",
            timeout=15
        ).content
        b64 = base64.b64encode(img_bytes).decode()

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                        },
                        {
                            "type": "text",
                            "text": """هذه فاتورة. استخرج منها:
1. المبلغ الإجمالي (Net Total أو الإجمالي شامل الضريبة)
2. اسم المتجر أو وصف المشتريات

أجب فقط بـ JSON هكذا بدون أي نص إضافي:
{"amt": 3.520, "desc": "نانا هايبر - أدوات", "found": true}
إذا لم تكن فاتورة: {"found": false}"""
                        }
                    ]
                }],
                "max_tokens": 200,
                "temperature": 0.1
            },
            timeout=20
        )
        raw = res.json()["choices"][0]["message"]["content"]
        raw = raw.replace("```json","").replace("```","").strip()
        return _json.loads(raw)
    except Exception as e:
        print("Groq error:", e)
        return None

# ── Telegram helpers ──────────────────────────────────────
def tg(chat_id, text):
    if not BOT_TOKEN:
        return
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=10
    )

def tg_buttons(chat_id, text, buttons):
    """Send message with inline keyboard buttons."""
    if not BOT_TOKEN:
        return
    keyboard = {"inline_keyboard": [[{"text": b["label"], "callback_data": b["data"]} for b in row] for row in buttons]}
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML", "reply_markup": keyboard},
        timeout=10
    )

# Store pending photo entries per chat
pending = {}

# ── Web API ───────────────────────────────────────────────
@app.route("/")
def index():
    return Response(HTML_PAGE, mimetype="text/html")

@app.route("/api/entries")
def api_get():
    month = request.args.get("month", cur_month())
    sales, buys = get_month_data(month)
    return jsonify({"sales": sales, "buys": buys})

@app.route("/api/entries", methods=["POST"])
def api_add():
    d = request.json
    month = d.get("month", cur_month())
    vals = (d["type"], d["desc"], float(d["amt"]),
            d.get("date", datetime.now().strftime("%d/%m/%Y")),
            month, d.get("img"), d.get("paid_by"),
            d.get("payment_method"), d.get("sale_time"))
    if USE_PG:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO entries (type,desc,amt,date,month,img,paid_by,payment_method,sale_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            vals)
        conn.commit(); cur.close(); conn.close()
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.execute(
            "INSERT INTO entries (type,desc,amt,date,month,img,paid_by,payment_method,sale_time) VALUES (?,?,?,?,?,?,?,?,?)",
            vals)
        conn.commit(); conn.close()
    return jsonify({"ok": True})

@app.route("/api/entries/<int:eid>", methods=["DELETE"])
def api_del(eid):
    if USE_PG:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM entries WHERE id=%s", (eid,))
        conn.commit(); cur.close(); conn.close()
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.execute("DELETE FROM entries WHERE id=?", (eid,))
        conn.commit(); conn.close()
    return jsonify({"ok": True})

# ── Telegram Webhook ──────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    msg  = data.get("message") or data.get("edited_message")
    # ── Callback query (button press) ──
    cb = data.get("callback_query")
    if cb:
        cb_id      = cb["id"]
        cb_chat    = cb["message"]["chat"]["id"]
        cb_data    = cb["data"]
        cb_month   = cur_month()
        cb_date    = datetime.now().strftime("%d/%m/%Y")

        # Answer callback to remove loading spinner
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
            json={"callback_query_id": cb_id}, timeout=5
        )

        # Payment method button
        if cb_data.startswith("pay:"):
            payment = cb_data.split("pay:", 1)[1]
            last = db_exec("SELECT id FROM entries WHERE type='s' AND month=?  ORDER BY created DESC LIMIT 1", (cb_month,), fetch="one")
            if last:
                db_exec("UPDATE entries SET payment_method=? WHERE id=?", (payment, last["id"]))
            # Remove buttons by editing message
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
                json={"chat_id": cb_chat, "message_id": cb["message"]["message_id"], "reply_markup": {"inline_keyboard": []}},
                timeout=5
            )
            tg(cb_chat, f"✅ طريقة الدفع: {payment}")
            if cb_chat in pending and pending[cb_chat].get("waiting") == "sale_payment":
                del pending[cb_chat]

        # Payer button
        elif cb_data.startswith("payer:"):
            payer_val = cb_data.split("payer:", 1)[1]

            if payer_val == "skip":
                paid_by = None
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
                    json={"chat_id": cb_chat, "message_id": cb["message"]["message_id"], "reply_markup": {"inline_keyboard": []}},
                    timeout=5
                )
                tg(cb_chat, "⏭ تم التخطي — لم يُحدد الدافع")

            elif payer_val == "other":
                pending[cb_chat] = pending.get(cb_chat, {})
                pending[cb_chat]["waiting_name"] = True
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
                    json={"chat_id": cb_chat, "message_id": cb["message"]["message_id"], "reply_markup": {"inline_keyboard": []}},
                    timeout=5
                )
                tg(cb_chat, "✏️ اكتب اسم الشخص:")
                return "ok"

            else:
                paid_by = payer_val
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
                    json={"chat_id": cb_chat, "message_id": cb["message"]["message_id"], "reply_markup": {"inline_keyboard": []}},
                    timeout=5
                )

            # Save paid_by to last buy entry or pending
            state = pending.get(cb_chat, {})
            if state.get("waiting") in ("paid_by", "paid_by_photo"):
                waiting = state["waiting"]
                if waiting == "paid_by":
                    desc  = state.get("desc", "مشتريات")
                    amt   = state.get("amt", 0)
                    month_s = state.get("month", cb_month)
                    dt    = state.get("date", cb_date)
                    db_exec(                             "INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                             ("b", desc, amt, dt, month_s, paid_by)                         )
                    del pending[cb_chat]
                    paid_line = f"\n👤 دفع: <b>{paid_by}</b>" if paid_by else ""
                    tg(cb_chat,
                       f"✅ <b>تم التسجيل!</b>\n\n"
                       f"📦 مشتريات\n📝 {desc}\n💰 {fmt_omr(amt)}{paid_line}")
                else:
                    # paid_by_photo — update last entry
                    last = db_exec("SELECT id FROM entries WHERE month=? ORDER BY created DESC LIMIT 1", (cb_month,), fetch="one")
                    if last:
                        db_exec("UPDATE entries SET paid_by=? WHERE id=?", (paid_by, last["id"]))
                    if cb_chat in pending:
                        del pending[cb_chat]
                    paid_line = f"👤 دفع: <b>{paid_by}</b>" if paid_by else "⏭ بدون دافع محدد"
                    tg(cb_chat, f"✅ {paid_line}")

        return "ok"

    if not msg:
        return "ok"

    chat_id = msg["chat"]["id"]
    month   = cur_month()
    date    = datetime.now().strftime("%d/%m/%Y")

    # ── Photo received ──
    if "photo" in msg:
        file_id = msg["photo"][-1]["file_id"]
        caption = msg.get("caption", "").strip()
        # Detect if sales receipt (caption has بيع/مبيعة keyword)
        is_sale_receipt = any(w in caption for w in ["بيع","مبيعة","بعت","فاتورة بيع","sale"])

        if is_sale_receipt and (GROQ_KEY or GEMINI_KEY):
            tg(chat_id, "⏳ جاري قراءة إيصال البيع...")
            result = groq_read_sale_receipt(file_id) if GROQ_KEY else None
            if result and result.get("found") and result.get("amt"):
                amt     = float(result["amt"])
                desc    = result.get("desc", "مبيعة")
                payment = result.get("payment", "غير محدد")
                stime   = result.get("time", "")
                sdate   = result.get("date", date)
                smonth  = sdate[-7:].replace("/","") if len(sdate)==10 else month
                # Normalize month from date
                try:
                    from datetime import datetime as _dt
                    d_obj = _dt.strptime(sdate, "%d/%m/%Y")
                    smonth = d_obj.strftime("%Y-%m")
                except:
                    smonth = month
                db_exec(                         "INSERT INTO entries (type,desc,amt,date,month,payment_method,sale_time) VALUES (?,?,?,?,?,?,?)",                         ("s", desc, amt, sdate, smonth, payment, stime)                     )
                pay_icon = "💵" if "كاش" in payment else "💳" if "فيزا" in payment else "🏦" if "تحويل" in payment else "💰"
                tg(chat_id,
                   f"✅ <b>تم تسجيل المبيعة!</b>\n\n"
                   f"🌸 مبيعة\n"
                   f"📝 {desc}\n"
                   f"💰 {fmt_omr(amt)}\n"
                   f"{pay_icon} <b>الدفع:</b> {payment}\n"
                   f"{'🕐 ' + stime if stime else ''}\n"
                   f"📅 {sdate}\n\n"
                   f"إذا المبلغ غلط أرسل: <code>تصحيح {amt}</code>")
            else:
                pending[chat_id] = {"waiting": "buy_amt", "desc": caption or "مبيعة", "force_type": "s"}
                tg(chat_id, "🌸 ما قدرت أقرأ الإيصال بوضوح\n\nكم <b>المبلغ</b>؟ أرسل الرقم:")
            return "ok"

        if GROQ_KEY or GEMINI_KEY:
            # Auto-read with AI (Groq first, then Gemini) — purchase invoice
            tg(chat_id, "⏳ جاري قراءة الفاتورة تلقائياً...")
            result = groq_read_invoice(file_id) if GROQ_KEY else None
            if not result or not result.get("found"):
                result = gemini_read_invoice(file_id) if GEMINI_KEY else None

            if result and result.get("found") and result.get("amt"):
                amt  = float(result["amt"])
                desc = result.get("desc", caption or "مشتريات")
                db_exec(                         "INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",                         ("b", desc, amt, date, month)                     )
                # Ask who paid
                pending[chat_id] = {"waiting": "paid_by_photo", "last_id": None, "amt": amt}
                tg_buttons(chat_id,
                   f"✅ <b>تم قراءة الفاتورة!</b>\n\n📦 {desc}\n💰 {fmt_omr(amt)}\n\n👤 <b>من دفع؟</b>",
                   [[{"label": "👤 حسين", "data": "payer:حسين"},
                     {"label": "👤 شوق",  "data": "payer:شوق"}],
                    [{"label": "➕ شخص آخر", "data": "payer:other"},
                     {"label": "⏭ تخطي",    "data": "payer:skip"}]])
            else:
                # Gemini couldn't read — ask manually
                pending[chat_id] = {"waiting": "buy_amt", "desc": caption or "مشتريات"}
                tg(chat_id,
                   "🧾 وصلت الفاتورة بس ما قدرت أقرأها بوضوح\n\n"
                   "كم <b>المبلغ الإجمالي</b>؟\n"
                   "أرسل الرقم فقط: <code>3.520</code>")
        else:
            # No AI key — ask manually
            pending[chat_id] = {"waiting": "buy_amt", "desc": caption or "مشتريات"}
            tg(chat_id,
               "🧾 وصلت الفاتورة!\n\n"
               "كم <b>المبلغ الإجمالي</b>؟\n"
               "أرسل الرقم فقط مثل: <code>3.520</code>")
        return "ok"

    # ── Text message ──
    text = msg.get("text", "").strip()
    if not text:
        return "ok"

    # Handle "تصحيح X" correction after auto-read
    import re as _re
    corr = _re.match(r'تصحيح\s+(\d+[.,]\d+|\d+)', text.strip())
    if corr:
        try:
            amt = float(corr.group(1).replace(",","."))
            # Update last entry
            last = db_exec("UPDATE entries SET amt=? WHERE id=?", (amt, last["id"]), fetch="one")
            if last:
                db_exec("UPDATE entries SET amt=? WHERE id=?", (amt, last["id"]))
        except:
            tg(chat_id, "⚠️ تنسيق خاطئ، مثال: <code>تصحيح 3.500</code>")
        return "ok"

    # Handle pending state
    if chat_id in pending:
        state = pending[chat_id]

        if state["waiting"] == "paid_by_photo":
            paid_by = None if text.strip() == "-" else text.strip()
            last = db_exec("UPDATE entries SET paid_by=? WHERE id=?", (paid_by, last["id"]), fetch="one")
            if last:
                db_exec("UPDATE entries SET paid_by=? WHERE id=?", (paid_by, last["id"]))
            del pending[chat_id]
            paid_line = f"👤 دفع: {paid_by}" if paid_by else ""
            tg(chat_id, f"✅ تم التسجيل! {paid_line}")
            return "ok"

        if state["waiting"] == "sale_payment":
            # User chose payment method after sale receipt read
            pay = text.strip()
            if pay in ["1", "كاش", "نقد"]:
                payment = "كاش 💵"
            elif pay in ["2", "فيزا", "بطاقة"]:
                payment = "فيزا 💳"
            elif pay in ["3", "تحويل"]:
                payment = "تحويل 🏦"
            else:
                payment = pay or "غير محدد"
            last = db_exec("UPDATE entries SET payment_method=? WHERE id=?", (payment, last["id"]), fetch="one")
            if last:
                db_exec("UPDATE entries SET payment_method=? WHERE id=?", (payment, last["id"]))
            del pending[chat_id]
            tg(chat_id, f"✅ تم تسجيل طريقة الدفع: {payment}")
            return "ok"

        if state.get("waiting_name"):
            # User typing custom payer name
            paid_by = text.strip()
            del state["waiting_name"]
            # Now handle as if payer was selected
            if state.get("waiting") == "paid_by":
                desc  = state.get("desc", "مشتريات")
                amt   = state.get("amt", 0)
                month_s = state.get("month", month)
                dt    = state.get("date", date)
                db_exec(                         "INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                         ("b", desc, amt, dt, month_s, paid_by)                     )
                del pending[chat_id]
                tg(chat_id,
                   f"✅ <b>تم التسجيل!</b>\n\n"
                   f"📦 مشتريات\n📝 {desc}\n💰 {fmt_omr(amt)}\n👤 دفع: <b>{paid_by}</b>")
            else:
                last = db_exec("UPDATE entries SET paid_by=? WHERE id=?", (paid_by, last["id"]), fetch="one")
                if last:
                    db_exec("UPDATE entries SET paid_by=? WHERE id=?", (paid_by, last["id"]))
                if chat_id in pending:
                    del pending[chat_id]
                tg(chat_id, f"✅ تم تسجيل الدافع: <b>{paid_by}</b>")
            return "ok"

        if state["waiting"] == "paid_by":
            paid_by = None if text.strip() == "-" else text.strip()
            desc  = state["desc"]
            amt   = state["amt"]
            month_s = state["month"]
            db_exec(                     "INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                     ("b", desc, amt, state["date"], month_s, paid_by)                 )
            del pending[chat_id]
            paid_line = f"\n👤 <b>دفع:</b> {paid_by}" if paid_by else ""
            tg(chat_id,
               f"✅ <b>تم التسجيل!</b>\n\n"
               f"📦 مشتريات\n"
               f"📝 {desc}\n"
               f"💰 {fmt_omr(amt)}{paid_line}")
            return "ok"

        if state["waiting"] == "buy_amt":
            try:
                amt = float(text.replace(",", "."))
                desc = state.get("desc", "مشتريات")
                db_exec(                         "INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",                         ("b", desc, amt, date, month)                     )
                del pending[chat_id]
                tg(chat_id,
                   f"✅ <b>تم التسجيل!</b>\n\n"
                   f"📦 مشتريات\n"
                   f"📝 {desc}\n"
                   f"💰 {fmt_omr(amt)}")
            except:
                tg(chat_id, "⚠️ أرسل رقم صحيح مثل: <code>3.520</code>")
            return "ok"

    # Commands
    if text in ["/start", "/help"]:
        tg(chat_id,
           "🌹 <b>أهلاً بك في فيروز فلورز!</b>\n\n"
           "📌 <b>كيف تسجّل؟</b>\n\n"
           "🌸 <b>مبيعة نصية:</b>\n"
           "<code>بعت باقة ورد بـ 5.500</code>\n"
           "<code>بعت عطر بـ 8.000 فيزا</code>\n\n"
           "🧾 <b>إيصال مبيعة بالصورة:</b>\n"
           "أرسل صورة + اكتب في التعليق: <code>بيع</code>\n\n"
           "📦 <b>مشتريات:</b>\n"
           "<code>اشتريت زهور بـ 12.000</code>\n\n"
           "🧾 <b>فاتورة مشتريات:</b>\n"
           "أرسل صورة الفاتورة بدون تعليق\n\n"
           "📊 <b>تقارير:</b>\n"
           "<code>/report</code> — ملخص الشهر\n"
           "<code>/من_دفع</code> — تفصيل المشتريات")
        return "ok"

    if text == "/report":
        ts, tb, tp, sc, bc = month_summary(month)
        emoji = "✅" if tp >= 0 else "⚠️"
        # Paid by breakdown
        _, buys = get_month_data(month)
        paid_summary = {}
        for e in buys:
            p = e.get("paid_by") or "غير محدد"
            paid_summary[p] = paid_summary.get(p, 0) + e["amt"]
        paid_lines = ""
        for name, total in paid_summary.items():
            paid_lines += f"  👤 {name}: {fmt_omr(total)}\n"
        tg(chat_id,
           f"📊 <b>تقرير {month}</b>\n\n"
           f"🌸 <b>المبيعات:</b> {fmt_omr(ts)} ({sc} عملية)\n"
           f"📦 <b>المشتريات:</b> {fmt_omr(tb)} ({bc} عملية)\n"
           f"━━━━━━━━━━━━━\n"
           f"{emoji} <b>صافي الربح:</b> {fmt_omr(tp)}\n\n"
           f"💳 <b>من دفع المشتريات:</b>\n{paid_lines if paid_lines else '  غير محدد'}")
        return "ok"

    if text == "/من_دفع" or text == "/mandafa3":
        _, buys = get_month_data(month)
        paid_summary = {}
        for e in buys:
            p = e.get("paid_by") or "غير محدد"
            if p not in paid_summary:
                paid_summary[p] = {"total": 0, "count": 0}
            paid_summary[p]["total"] += e["amt"]
            paid_summary[p]["count"] += 1
        if not paid_summary:
            tg(chat_id, "📭 ما في مشتريات هذا الشهر")
            return "ok"
        lines = f"💳 <b>من دفع المشتريات — {month}</b>\n\n"
        for name, info in paid_summary.items():
            lines += f"👤 <b>{name}</b>\n"
            lines += f"   المبلغ: {fmt_omr(info['total'])} ({info['count']} عملية)\n\n"
        tg(chat_id, lines)
        return "ok"

    # Natural language
    parsed = parse_text(text)
    if parsed["found"]:
        etype   = parsed["type"]
        desc    = parsed["desc"]
        amt     = parsed["amt"]
        paid_by = parsed.get("paid_by")

        # For buys: ask who paid
        if etype == "b" and not paid_by:
            pending[chat_id] = {"waiting": "paid_by", "desc": desc, "amt": amt, "date": date, "month": month}
            tg(chat_id,
               f"📦 <b>مشتريات {fmt_omr(amt)}</b>\n\n"
               f"👤 <b>من دفع؟</b>\n"
               f"اكتب الاسم: <code>حسين</code> أو <code>شوق</code>\n"
               f"أو <code>-</code> إذا ما تبي تحدد")
            return "ok"

        # For sales: ask payment method
        if etype == "s":
            # Check if payment method mentioned in text
            pay_method = None
            if any(w in text for w in ["كاش","نقد","كاشن"]):
                pay_method = "كاش 💵"
            elif any(w in text for w in ["فيزا","بطاقة","كارد"]):
                pay_method = "فيزا 💳"
            elif any(w in text for w in ["تحويل","تحويلة"]):
                pay_method = "تحويل 🏦"

            if not pay_method:
                db_exec(                         "INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",                         ("s", desc, amt, date, month)                     )
                pending[chat_id] = {"waiting": "sale_payment", "desc": desc, "amt": amt, "date": date, "month": month}
                tg_buttons(chat_id,
                   f"🌸 <b>مبيعة {fmt_omr(amt)}</b> — تم التسجيل!\n\n💳 <b>طريقة الدفع؟</b>",
                   [[{"label": "💵 كاش",    "data": "pay:كاش 💵"},
                     {"label": "💳 فيزا",   "data": "pay:فيزا 💳"},
                     {"label": "🏦 تحويل",  "data": "pay:تحويل 🏦"}]])
                return "ok"
            else:
                db_exec(                         "INSERT INTO entries (type,desc,amt,date,month,payment_method) VALUES (?,?,?,?,?,?)",                         ("s", desc, amt, date, month, pay_method)                     )
                tg(chat_id,
                   f"✅ <b>تم التسجيل!</b>\n\n"
                   f"🌸 مبيعة\n📝 {desc}\n💰 {fmt_omr(amt)}\n💳 {pay_method}\n📅 {date}")
                return "ok"

        db_exec(                 "INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                 (etype, desc, amt, date, month, paid_by)             )
        label = "مبيعة 🌸" if etype == "s" else "مشتريات 📦"
        paid_line = f"\n👤 <b>دفع:</b> {paid_by}" if paid_by else ""
        tg(chat_id,
           f"✅ <b>تم التسجيل!</b>\n\n"
           f"🏷 {label}\n"
           f"📝 {desc}\n"
           f"💰 {fmt_omr(amt)}\n"
           f"📅 {date}{paid_line}")
    else:
        tg(chat_id,
           "لم أفهم الرسالة 🤔\n\n"
           "جرّب:\n"
           "<code>بعت باقة بـ 4.500</code>\n"
           "<code>اشتريت ورد بـ 8.000</code>\n\n"
           "أو /help للمساعدة")

    return "ok"

@app.route("/set_webhook")
def set_webhook():
    host = request.host_url.rstrip("/")
    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
        params={"url": f"{host}/webhook"},
        timeout=10
    )
    return jsonify(r.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
