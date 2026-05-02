import os
import re
import requests
from datetime import datetime
from flask import Flask, request, jsonify, Response

# PostgreSQL via pg8000 (pure Python, works with any Python version)
if os.environ.get("DATABASE_URL"):
    try:
        import pg8000.native as pg
        USE_PG = True
    except ImportError:
        USE_PG = False
else:
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
  --pos:#4ade80;--neg:#fb7185;
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
header{padding:0 24px;height:62px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);background:rgba(13,10,14,.85);backdrop-filter:blur(20px);
  position:sticky;top:0;z-index:100;}
.brand{display:flex;align-items:center;gap:10px;}
.emblem{width:36px;height:36px;background:linear-gradient(135deg,var(--rose),var(--lav));border-radius:10px;
  display:flex;align-items:center;justify-content:center;font-size:17px;
  box-shadow:0 0 18px var(--rglow);animation:glow 3s ease-in-out infinite;}
@keyframes glow{0%,100%{box-shadow:0 0 18px var(--rglow);}50%{box-shadow:0 0 32px rgba(232,84,122,.5);}}
.bname{font-family:'Playfair Display',serif;font-size:16px;font-weight:700;
  background:linear-gradient(90deg,#fff,var(--rose2),var(--lav));-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;}
.bsub{font-size:9px;color:var(--text3);}
.hright{display:flex;align-items:center;gap:8px;}
.main-tabs{display:flex;gap:3px;background:var(--surface);border:1px solid var(--border2);
  padding:3px;border-radius:10px;}
.mtab{padding:6px 14px;border:none;border-radius:7px;font-family:'Tajawal',sans-serif;
  font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;background:transparent;color:var(--text3);}
.mtab.on{background:linear-gradient(135deg,rgba(232,84,122,.2),rgba(232,84,122,.08));
  color:var(--rose2);box-shadow:inset 0 0 0 1px rgba(232,84,122,.3);}
.mpill{display:flex;align-items:center;gap:7px;background:var(--card);border:1px solid var(--border2);
  padding:6px 11px;border-radius:40px;}
.mpill label{font-size:10px;color:var(--text3);}
.mpill select{background:transparent;border:none;color:var(--text);font-family:'Tajawal',sans-serif;
  font-size:12px;font-weight:600;cursor:pointer;outline:none;}
.mpill select option{background:var(--deep);}
.page{display:none;max-width:1200px;margin:0 auto;padding:24px 16px 60px;}
.page.active{display:block;}
.slbl{font-size:9px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;
  margin-bottom:10px;display:flex;align-items:center;gap:8px;}
.slbl::after{content:'';flex:1;height:1px;background:var(--border);}
/* KPI */
.kpi-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px 16px;
  cursor:default;transition:transform .3s cubic-bezier(.34,1.56,.64,1),border-color .3s,box-shadow .3s;
  animation:fadeUp .5s ease both;}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
.kpi:hover{transform:translateY(-3px);}
.ks:hover{border-color:var(--mint);box-shadow:0 6px 24px var(--mglow);}
.kb:hover{border-color:var(--rose);box-shadow:0 6px 24px var(--rglow);}
.kp:hover{border-color:var(--gold);box-shadow:0 6px 24px var(--gglow);}
.kpi-ico{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:10px;}
.ks .kpi-ico{background:rgba(78,205,196,.12);}
.kb .kpi-ico{background:rgba(232,84,122,.12);}
.kp .kpi-ico{background:rgba(245,200,66,.12);}
.kpi-lbl{font-size:10px;color:var(--text3);margin-bottom:4px;}
.kpi-val{font-size:24px;font-weight:900;letter-spacing:-1px;line-height:1;margin-bottom:6px;}
.ks .kpi-val{color:var(--mint);}
.kb .kpi-val{color:var(--rose2);}
.kp .kpi-val{color:var(--gold);}
.kpi-sub{font-size:10px;color:var(--text3);}
.badge{padding:2px 7px;border-radius:14px;font-size:9px;font-weight:700;}
.bp{background:rgba(74,222,128,.12);color:var(--pos);}
.bn{background:rgba(251,113,133,.12);color:var(--neg);}
.chips{display:flex;gap:4px;margin-top:6px;flex-wrap:wrap;}
.chip{padding:2px 7px;border-radius:12px;font-size:9px;font-weight:600;}
.ch-c{background:rgba(52,211,153,.12);color:#34d399;}
.ch-v{background:rgba(96,165,250,.12);color:#60a5fa;}
.ch-t{background:rgba(167,139,250,.12);color:#a78bfa;}
.ch-p{background:rgba(232,84,122,.1);color:var(--rose2);}
/* FORM */
.add-card{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:20px;margin-bottom:20px;}
.type-tabs{display:flex;gap:5px;background:var(--deep);border:1px solid var(--border);
  border-radius:10px;padding:3px;margin-bottom:16px;}
.ttab{flex:1;padding:8px;border:none;border-radius:8px;font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;cursor:pointer;transition:all .2s;background:transparent;
  color:var(--text3);display:flex;align-items:center;justify-content:center;gap:5px;}
.tt-s{background:linear-gradient(135deg,rgba(78,205,196,.18),rgba(78,205,196,.08));color:var(--mint);box-shadow:inset 0 0 0 1px rgba(78,205,196,.25);}
.tt-b{background:linear-gradient(135deg,rgba(232,84,122,.18),rgba(232,84,122,.08));color:var(--rose2);box-shadow:inset 0 0 0 1px rgba(232,84,122,.25);}
.fgrid{display:grid;gap:8px;margin-bottom:10px;}
.fg2{grid-template-columns:1fr 1fr;}
.fg3{grid-template-columns:1fr 1fr 1fr;}
.fld{display:flex;flex-direction:column;gap:4px;}
.fld label{font-size:9px;font-weight:700;color:var(--text3);letter-spacing:.8px;text-transform:uppercase;}
.fld input,.fld select{background:var(--deep);border:1px solid var(--border2);border-radius:8px;
  padding:8px 11px;font-family:'Tajawal',sans-serif;font-size:13px;color:var(--text);
  outline:none;transition:.2s;width:100%;}
.fld input:focus,.fld select:focus{border-color:var(--rose);box-shadow:0 0 0 2px var(--rglow);}
.fld input::placeholder{color:var(--text3);}
.fld select option{background:var(--deep);}
.sbtn{height:40px;padding:0 20px;border:none;border-radius:8px;font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;cursor:pointer;transition:all .25s cubic-bezier(.34,1.56,.64,1);
  display:flex;align-items:center;gap:5px;}
.sb-s{background:linear-gradient(135deg,var(--mint),#2ba8a0);color:#0d0a0e;box-shadow:0 3px 12px var(--mglow);}
.sb-s:hover{transform:translateY(-2px) scale(1.02);}
.sb-b{background:linear-gradient(135deg,var(--rose),#c03060);color:#fff;box-shadow:0 3px 12px var(--rglow);}
.sb-b:hover{transform:translateY(-2px) scale(1.02);}
/* PANELS */
.panels{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;}
.panel{background:var(--card);border:1px solid var(--border);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;}
.ph{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);}
.ph-l{display:flex;align-items:center;gap:8px;}
.pico{width:30px;height:30px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;}
.ps .pico{background:rgba(78,205,196,.14);}
.pb .pico{background:rgba(232,84,122,.14);}
.ptitle{font-size:12px;font-weight:700;}
.ps .ptitle{color:var(--mint);}
.pb .ptitle{color:var(--rose2);}
.pcnt{font-size:9px;font-weight:800;padding:2px 7px;border-radius:14px;}
.ps .pcnt{background:rgba(78,205,196,.14);color:var(--mint);}
.pb .pcnt{background:rgba(232,84,122,.14);color:var(--rose2);}
.pbody{padding:6px;flex:1;overflow-y:auto;max-height:260px;scrollbar-width:thin;scrollbar-color:var(--border2) transparent;}
.empty{padding:24px;text-align:center;color:var(--text3);}
.empty .ei{font-size:26px;margin-bottom:5px;opacity:.3;}
.empty p{font-size:11px;line-height:1.8;}
.entry{display:flex;align-items:center;gap:7px;padding:8px 5px;border-radius:8px;
  margin-bottom:1px;transition:.2s;animation:ei .3s cubic-bezier(.34,1.56,.64,1) both;}
@keyframes ei{from{opacity:0;transform:scale(.92);}to{opacity:1;transform:scale(1);}}
.entry:hover{background:rgba(255,255,255,.03);}
.edot{width:5px;height:5px;border-radius:50%;flex-shrink:0;}
.es .edot{background:var(--mint);}
.eb .edot{background:var(--rose2);}
.eph{width:30px;height:30px;border-radius:6px;background:var(--surface);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.einfo{flex:1;min-width:0;}
.edesc{font-size:11px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.emeta{display:flex;gap:4px;margin-top:1px;flex-wrap:wrap;align-items:center;}
.edate{font-size:9px;color:var(--text3);}
.epb{font-size:8px;font-weight:700;padding:1px 5px;border-radius:7px;}
.epb-c{background:rgba(52,211,153,.15);color:#34d399;}
.epb-v{background:rgba(96,165,250,.15);color:#60a5fa;}
.epb-t{background:rgba(167,139,250,.15);color:#a78bfa;}
.epb-p{background:rgba(232,84,122,.12);color:var(--rose2);}
.epb-s{background:rgba(245,200,66,.12);color:var(--gold);}
.eamt{font-size:12px;font-weight:800;white-space:nowrap;flex-shrink:0;}
.eamt.inc{color:var(--mint);}
.eamt.exp{color:var(--rose2);}
.delbtn{background:none;border:none;cursor:pointer;color:var(--text3);font-size:11px;
  width:22px;height:22px;border-radius:5px;display:flex;align-items:center;justify-content:center;transition:.2s;flex-shrink:0;}
.delbtn:hover{background:rgba(251,113,133,.14);color:var(--neg);}
/* CHARTS */
.charts-row{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;margin-bottom:20px;}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px;}
.chart-card h3{font-size:11px;font-weight:700;color:var(--text2);margin-bottom:14px;}
/* SHELVES SECTION */
.shelf-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;}
.shelf-kpi{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;
  position:relative;overflow:hidden;animation:fadeUp .5s ease both;cursor:default;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1);}
.shelf-kpi:hover{transform:translateY(-3px);}
.shelf-kpi-bar{position:absolute;top:0;right:0;left:0;height:3px;}
.shelf-kpi-name{font-size:13px;font-weight:800;margin-bottom:12px;display:flex;align-items:center;gap:7px;}
.shelf-dot{width:8px;height:8px;border-radius:50%;}
.shelf-kpi-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.skv{text-align:center;padding:8px 6px;background:var(--surface);border-radius:8px;}
.skv .v{font-size:13px;font-weight:800;line-height:1;}
.skv .l{font-size:9px;color:var(--text3);margin-top:3px;}
.shelf-net{margin-top:10px;padding:8px 10px;border-radius:8px;display:flex;justify-content:space-between;align-items:center;}
.shelf-net-pos{background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.15);}
.shelf-net-neg{background:rgba(251,113,133,.08);border:1px solid rgba(251,113,133,.15);}
.shelf-net .nl{font-size:10px;color:var(--text3);}
.shelf-net .nv{font-size:14px;font-weight:800;}
.rent-btn{background:none;border:1px solid var(--border2);border-radius:6px;color:var(--text3);
  font-size:9px;font-family:'Tajawal',sans-serif;padding:2px 7px;cursor:pointer;transition:.2s;margin-top:6px;width:100%;}
.rent-btn:hover{border-color:var(--gold);color:var(--gold);}
/* SHELF PRODUCTS */
.shelf-prods-section{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;}
.shelf-prod-card{background:var(--card);border:1px solid var(--border);border-radius:16px;overflow:hidden;}
.sp-head{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);}
.sp-name{font-size:13px;font-weight:700;display:flex;align-items:center;gap:7px;}
.sp-count{font-size:9px;font-weight:700;padding:2px 8px;border-radius:12px;}
.sp-body{padding:6px;max-height:220px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--border2) transparent;}
.prod-row{display:flex;align-items:center;gap:7px;padding:7px 5px;border-radius:8px;
  border-bottom:1px solid var(--border);transition:.2s;}
.prod-row:last-child{border-bottom:none;}
.prod-row:hover{background:rgba(255,255,255,.03);}
.prod-ph{width:30px;height:30px;border-radius:6px;background:var(--surface);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.prod-info{flex:1;min-width:0;}
.prod-name{font-size:11px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.prod-price{font-size:9px;color:var(--text3);margin-top:1px;}
.prod-right{display:flex;align-items:center;gap:5px;flex-shrink:0;}
.qty-badge{min-width:26px;padding:2px 6px;border-radius:6px;font-size:10px;font-weight:800;text-align:center;
  background:rgba(78,205,196,.12);color:var(--mint);}
.qty-badge.zero{background:rgba(251,113,133,.12);color:var(--neg);}
.sell-btn{background:linear-gradient(135deg,var(--mint),#2ba8a0);border:none;border-radius:6px;
  color:#0d0a0e;font-size:10px;font-weight:700;padding:3px 8px;cursor:pointer;
  font-family:'Tajawal',sans-serif;transition:.2s;}
.sell-btn:hover{transform:scale(1.06);}
.sell-btn:disabled{opacity:.3;cursor:not-allowed;transform:none;}
.prod-del{background:none;border:none;cursor:pointer;color:var(--text3);font-size:11px;
  width:20px;height:20px;border-radius:5px;display:flex;align-items:center;justify-content:center;transition:.2s;flex-shrink:0;}
.prod-del:hover{background:rgba(251,113,133,.14);color:var(--neg);}
.sp-foot{padding:8px 12px;border-top:1px solid var(--border);}
.add-prod-btn{width:100%;padding:7px;border:1px dashed var(--border2);border-radius:8px;
  background:transparent;color:var(--text3);font-family:'Tajawal',sans-serif;font-size:11px;
  font-weight:600;cursor:pointer;transition:.2s;}
.add-prod-btn:hover{border-color:var(--mint);color:var(--mint);}
/* MODAL */
.overlay{display:none;position:fixed;inset:0;background:rgba(13,10,14,.88);backdrop-filter:blur(14px);
  z-index:500;align-items:center;justify-content:center;padding:20px;}
.overlay.open{display:flex;}
.modal{background:var(--card2);border:1px solid var(--border2);border-radius:18px;padding:26px;
  max-width:360px;width:100%;text-align:center;box-shadow:0 40px 100px rgba(0,0,0,.6);
  animation:mi .4s cubic-bezier(.34,1.56,.64,1);}
@keyframes mi{from{opacity:0;transform:scale(.86) translateY(16px);}to{opacity:1;transform:scale(1) translateY(0);}}
.mico{font-size:40px;margin-bottom:10px;}
.modal h3{font-size:16px;font-weight:800;margin-bottom:7px;}
.modal p{font-size:12px;color:var(--text2);margin-bottom:16px;line-height:1.7;}
.minput{width:100%;background:var(--surface);border:1px solid var(--border2);border-radius:8px;
  padding:9px 12px;font-family:'Tajawal',sans-serif;font-size:15px;font-weight:700;
  text-align:center;color:var(--text);outline:none;margin-bottom:10px;transition:.2s;}
.minput:focus{border-color:var(--rose);box-shadow:0 0 0 2px var(--rglow);}
.minput.sm{font-size:12px;font-weight:500;text-align:right;}
.mbtns{display:flex;gap:8px;}
.mbtns button{flex:1;padding:9px;border:none;border-radius:8px;font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;cursor:pointer;transition:.2s;}
.bc{background:var(--surface);border:1px solid var(--border2)!important;color:var(--text2);}
.bcs{background:linear-gradient(135deg,var(--mint),#2ba8a0);color:#0d0a0e;}
.bcp{background:linear-gradient(135deg,var(--rose),#c03060);color:#fff;}
.lb{display:none;position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:9000;align-items:center;justify-content:center;cursor:zoom-out;}
.lb.open{display:flex;}
.lb img{max-width:90vw;max-height:88vh;border-radius:14px;}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);
  background:var(--card2);border:1px solid var(--border2);color:var(--text);
  padding:8px 20px;border-radius:40px;font-size:12px;font-weight:600;
  box-shadow:0 12px 32px rgba(0,0,0,.5);transition:transform .4s cubic-bezier(.34,1.56,.64,1);
  z-index:9999;white-space:nowrap;}
.toast.show{transform:translateX(-50%) translateY(0);}
@media(max-width:768px){
  header{padding:0 10px;}
  .kpi-row,.panels,.charts-row,.shelf-summary,.shelf-prods-section{grid-template-columns:1fr;gap:8px;}
  .fg2,.fg3{grid-template-columns:1fr;}
  .kpi-val{font-size:20px;}
  .add-card{padding:14px;}
  .mtab{font-size:11px;padding:5px 9px;}
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
  <div class="hright">
    <div class="main-tabs">
      <button class="mtab on" onclick="switchTab('home')">📊 الرئيسية</button>
      <button class="mtab" onclick="switchTab('shelves')">🗄️ الرفوف</button>
    </div>
    <div class="mpill" id="mpill">
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
  </div>
</header>

<!-- HOME -->
<div id="tab-home" class="page active">
  <div class="slbl">ملخص الشهر</div>
  <div class="kpi-row">
    <div class="kpi ks"><div class="kpi-ico">💰</div><div class="kpi-lbl">إجمالي المبيعات</div>
      <div class="kpi-val" id="kS">0 ر.ع</div><div class="kpi-sub" id="kSc">0 عملية</div>
      <div class="chips" id="payChips"></div></div>
    <div class="kpi kb"><div class="kpi-ico">🛒</div><div class="kpi-lbl">إجمالي المشتريات</div>
      <div class="kpi-val" id="kB">0 ر.ع</div><div class="kpi-sub" id="kBc">0 عملية</div>
      <div class="chips" id="payerChips"></div></div>
    <div class="kpi kp"><div class="kpi-ico">📊</div><div class="kpi-lbl">صافي الربح</div>
      <div class="kpi-val" id="kP">0 ر.ع</div><div class="kpi-sub"><span id="kPb" class="badge">—</span></div></div>
  </div>

  <div class="slbl">إضافة جديد</div>
  <div class="add-card">
    <div class="type-tabs">
      <button class="ttab tt-s" id="tt-s" onclick="setFT('s')">🌸 مبيعات</button>
      <button class="ttab" id="tt-b" onclick="setFT('b')">📦 مشتريات</button>
    </div>
    <div id="form-s">
      <div class="fgrid fg2"><div class="fld"><label>اسم المنتج</label><input id="sDesc" type="text" placeholder="باقة ورد، عطر..."/></div>
        <div class="fld"><label>السعر (ر.ع)</label><input id="sAmt" type="number" placeholder="0.000" step="0.001"/></div></div>
      <div class="fgrid fg2" style="margin-bottom:12px;"><div class="fld"><label>💳 طريقة الدفع</label>
          <select id="sPay"><option value="">— اختر —</option>
            <option value="كاش 💵">💵 كاش</option><option value="فيزا 💳">💳 فيزا</option><option value="تحويل 🏦">🏦 تحويل</option></select></div>
        <div class="fld"><label>📝 ملاحظة</label><input id="sNote" type="text" placeholder="اختياري"/></div></div>
      <button class="sbtn sb-s" onclick="addSale()" style="width:100%;justify-content:center;">🌸 إضافة مبيعة</button>
    </div>
    <div id="form-b" style="display:none;">
      <div class="fgrid fg3"><div class="fld"><label>الوصف / المورد</label><input id="bDesc" type="text" placeholder="نانا هايبر..."/></div>
        <div class="fld"><label>المبلغ (ر.ع)</label><input id="bAmt" type="number" placeholder="0.000" step="0.001"/></div>
        <div class="fld"><label>👤 من دفع؟</label>
          <select id="bPayer"><option value="">— اختر —</option>
            <option value="حسين">👤 حسين</option><option value="شوق">👤 شوق</option><option value="أخرى">➕ أخرى</option></select></div></div>
      <div id="bOtherWrap" style="display:none;margin-bottom:10px;">
        <div class="fld"><label>اسم الشخص</label><input id="bOther" type="text" placeholder="اكتب الاسم"/></div></div>
      <button class="sbtn sb-b" onclick="addBuy()" style="width:100%;justify-content:center;">📦 إضافة مشتريات</button>
    </div>
  </div>

  <div class="slbl">السجلات</div>
  <div class="panels">
    <div class="panel ps"><div class="ph"><div class="ph-l"><div class="pico">🌸</div><div class="ptitle">المبيعات</div></div><div class="pcnt" id="sbadge">0</div></div><div class="pbody" id="sl"></div></div>
    <div class="panel pb"><div class="ph"><div class="ph-l"><div class="pico">📦</div><div class="ptitle">المشتريات</div></div><div class="pcnt" id="bbadge">0</div></div><div class="pbody" id="bl"></div></div>
  </div>

  <div class="slbl">الإحصائيات</div>
  <div class="charts-row">
    <div class="chart-card"><h3>📈 مبيعات ومشتريات 2026</h3><canvas id="barChart" height="150"></canvas></div>
    <div class="chart-card"><h3>💳 طريقة الدفع</h3><canvas id="payChart" height="150"></canvas></div>
    <div class="chart-card"><h3>👤 من دفع المشتريات</h3><canvas id="payerChart" height="150"></canvas></div>
  </div>
</div>

<!-- SHELVES -->
<div id="tab-shelves" class="page">
  <div class="slbl">ملخص الرفوف — الشهر الحالي</div>
  <div class="shelf-summary" id="shelfSummary"></div>

  <div class="slbl">منتجات الرفوف</div>
  <div class="shelf-prods-section" id="shelfProds"></div>
</div>
</div>

<!-- MODALS -->
<div class="overlay" id="addProdOv">
  <div class="modal">
    <div class="mico">📦</div>
    <h3 id="addProdTitle">إضافة منتج</h3>
    <input class="minput sm" id="pName" type="text" placeholder="اسم المنتج" style="margin-bottom:8px;"/>
    <div class="fgrid fg2" style="margin-bottom:12px;">
      <div class="fld"><label>السعر (ر.ع)</label><input id="pPrice" type="number" placeholder="0.000" step="0.001"/></div>
      <div class="fld"><label>الكمية</label><input id="pQty" type="number" placeholder="0" min="0"/></div>
    </div>
    <div class="mbtns"><button class="bc" onclick="closeProdModal()">إلغاء</button><button class="bcs" onclick="saveProduct()">✅ إضافة</button></div>
  </div>
</div>

<div class="overlay" id="sellOv">
  <div class="modal">
    <div class="mico">🌸</div>
    <h3>تسجيل مبيعة</h3>
    <p id="sellDesc" style="font-size:13px;font-weight:700;color:var(--text);margin-bottom:3px;"></p>
    <p id="sellInfo" style="font-size:11px;color:var(--text3);margin-bottom:14px;"></p>
    <div class="fgrid fg2" style="margin-bottom:12px;">
      <div class="fld"><label>الكمية</label><input id="sellQty" type="number" value="1" min="1"/></div>
      <div class="fld"><label>💳 طريقة الدفع</label>
        <select id="sellPay"><option value="">— اختر —</option>
          <option value="كاش 💵">💵 كاش</option><option value="فيزا 💳">💳 فيزا</option><option value="تحويل 🏦">🏦 تحويل</option></select></div>
    </div>
    <div class="mbtns"><button class="bc" onclick="closeSellModal()">إلغاء</button><button class="bcs" onclick="confirmSell()">💰 تأكيد البيع</button></div>
  </div>
</div>

<div class="overlay" id="rentOv">
  <div class="modal">
    <div class="mico">🏷️</div>
    <h3 id="rentTitle">تعديل الإيجار</h3>
    <p>أدخل الإيجار الشهري للرف</p>
    <input class="minput" id="rentVal" type="number" placeholder="0.000" step="0.001"/>
    <div class="mbtns"><button class="bc" onclick="closeRentModal()">إلغاء</button><button class="bcs" onclick="saveRent()">✅ حفظ</button></div>
  </div>
</div>

<div class="overlay" id="ov"><div class="modal" id="mb"></div></div>
<div class="lb" id="lb" onclick="this.classList.remove('open')"><img id="lbImg" src=""/></div>
<div class="toast" id="toast"></div>

<script>
let formTab='s', month='2026-05';
let barCI=null, payCI=null, payerCI=null;
let activeProdShelf=null, activeSellProd=null, activeRentShelf=null;

async function api(url,opts){const r=await fetch(url,opts);return r.json();}
function fmt(n){return (+n).toLocaleString('ar-OM',{minimumFractionDigits:3,maximumFractionDigits:3});}

/* ── TABS ── */
function switchTab(t){
  document.getElementById('tab-home').className='page'+(t==='home'?' active':'');
  document.getElementById('tab-shelves').className='page'+(t==='shelves'?' active':'');
  document.querySelectorAll('.mtab').forEach((b,i)=>b.className='mtab'+(i===(t==='home'?0:1)?' on':''));
  if(t==='shelves') loadShelves();
}
function setFT(t){
  formTab=t;
  document.getElementById('tt-s').className='ttab'+(t==='s'?' tt-s':'');
  document.getElementById('tt-b').className='ttab'+(t==='b'?' tt-b':'');
  document.getElementById('form-s').style.display=t==='s'?'block':'none';
  document.getElementById('form-b').style.display=t==='b'?'block':'none';
}
document.getElementById('bPayer').addEventListener('change',function(){
  document.getElementById('bOtherWrap').style.display=this.value==='أخرى'?'block':'none';
});

/* ── LOAD HOME ── */
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
  renderBarChart(all.map(d=>d.sales.reduce((a,e)=>a+e.amt,0)),all.map(d=>d.buys.reduce((a,e)=>a+e.amt,0)));
  const cur=all[parseInt(month.split('-')[1])-1];
  renderPayChart(cur.sales);renderPayerChart(cur.buys);
}
setInterval(()=>{load();if(document.getElementById('tab-shelves').classList.contains('active'))loadShelves();},15000);

/* ── KPI ── */
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
  const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};
  sales.forEach(e=>{if(e.payment_method&&pm[e.payment_method]!==undefined)pm[e.payment_method]+=e.amt;});
  const pcls={'كاش 💵':'ch-c','فيزا 💳':'ch-v','تحويل 🏦':'ch-t'};
  document.getElementById('payChips').innerHTML=Object.entries(pm).filter(([,v])=>v>0)
    .map(([k,v])=>`<span class="chip ${pcls[k]}">${k} ${fmt(v)}</span>`).join('');
  const py={};buys.forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});
  document.getElementById('payerChips').innerHTML=Object.entries(py)
    .map(([k,v])=>`<span class="chip ch-p">👤${k} ${fmt(v)}</span>`).join('');
}

/* ── LISTS ── */
function pb(pm){if(!pm)return'';const c=pm.includes('كاش')?'epb-c':pm.includes('فيزا')?'epb-v':'epb-t';return`<span class="epb ${c}">${pm}</span>`;}
function renderLists(sales,buys){
  document.getElementById('sl').innerHTML=sales.length?sales.map(e=>`
    <div class="entry es">
      <div class="eph">🌸</div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${pb(e.payment_method)}${e.shelf_id?`<span class="epb epb-s">🗄️رف</span>`:''}</div></div>
      <div class="eamt inc">+${fmt(e.amt)} ر.ع</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button>
    </div>`).join(''):`<div class="empty"><div class="ei">🌷</div><p>لا توجد مبيعات<br>أضف من هنا أو عبر التيليغرام</p></div>`;
  document.getElementById('bl').innerHTML=buys.length?buys.map(e=>`
    <div class="entry eb">
      <div class="edot"></div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${e.paid_by?`<span class="epb epb-p">👤${e.paid_by}</span>`:''}</div></div>
      <div class="eamt exp">-${fmt(e.amt)} ر.ع</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button>
    </div>`).join(''):`<div class="empty"><div class="ei">🌿</div><p>لا توجد مشتريات<br>أضف من هنا أو عبر التيليغرام</p></div>`;
  document.getElementById('sbadge').textContent=sales.length;
  document.getElementById('bbadge').textContent=buys.length;
}

/* ── CHARTS ── */
const mnames=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
const co={responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(255,255,255,.04)'},ticks:{color:'#6b5f85',font:{family:'Tajawal',size:9}}},y:{grid:{color:'rgba(255,255,255,.04)'},ticks:{color:'#6b5f85',font:{family:'Tajawal',size:9}}}}};
function renderBarChart(aS,aB){if(barCI)barCI.destroy();barCI=new Chart(document.getElementById('barChart'),{type:'bar',data:{labels:mnames.map(m=>m.slice(0,3)),datasets:[{label:'مبيعات',data:aS,backgroundColor:'rgba(78,205,196,.7)',borderRadius:3},{label:'مشتريات',data:aB,backgroundColor:'rgba(232,84,122,.7)',borderRadius:3}]},options:{...co,plugins:{legend:{display:true,labels:{color:'#a89bc2',font:{family:'Tajawal',size:10}}}}}});}
function renderPayChart(sales){const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};sales.forEach(e=>{if(e.payment_method&&pm[e.payment_method]!==undefined)pm[e.payment_method]+=e.amt;});if(payCI)payCI.destroy();payCI=new Chart(document.getElementById('payChart'),{type:'doughnut',data:{labels:Object.keys(pm),datasets:[{data:Object.values(pm),backgroundColor:['rgba(52,211,153,.8)','rgba(96,165,250,.8)','rgba(167,139,250,.8)'],borderWidth:0}]},options:{responsive:true,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:'#a89bc2',font:{family:'Tajawal',size:9},padding:5}}}}});}
function renderPayerChart(buys){const py={};buys.forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});const clrs=['rgba(232,84,122,.8)','rgba(78,205,196,.8)','rgba(245,200,66,.8)','rgba(183,148,244,.8)'];if(payerCI)payerCI.destroy();payerCI=new Chart(document.getElementById('payerChart'),{type:'doughnut',data:{labels:Object.keys(py).length?Object.keys(py):['لا يوجد'],datasets:[{data:Object.keys(py).length?Object.values(py):[1],backgroundColor:Object.keys(py).length?clrs.slice(0,Object.keys(py).length):['rgba(107,95,133,.3)'],borderWidth:0}]},options:{responsive:true,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:'#a89bc2',font:{family:'Tajawal',size:9},padding:5}}}}});}

/* ── ADD ── */
async function addSale(){
  const desc=document.getElementById('sDesc').value.trim()||'مبيعة';
  const amt=parseFloat(document.getElementById('sAmt').value);
  const pay=document.getElementById('sPay').value;
  const note=document.getElementById('sNote').value.trim();
  if(!amt||amt<=0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'s',desc:note?`${desc} — ${note}`:desc,amt,payment_method:pay||null,month})});
  document.getElementById('sDesc').value='';document.getElementById('sAmt').value='';document.getElementById('sPay').value='';document.getElementById('sNote').value='';
  load();showToast('✅ تمت إضافة المبيعة');
}
async function addBuy(){
  const desc=document.getElementById('bDesc').value.trim()||'مشتريات';
  const amt=parseFloat(document.getElementById('bAmt').value);
  let payer=document.getElementById('bPayer').value;
  if(payer==='أخرى')payer=document.getElementById('bOther').value.trim()||null;
  if(!amt||amt<=0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'b',desc,amt,paid_by:payer||null,month})});
  document.getElementById('bDesc').value='';document.getElementById('bAmt').value='';document.getElementById('bPayer').value='';
  load();showToast('✅ تمت إضافة المشتريات');
}
async function del(id){await api(`/api/entries/${id}`,{method:'DELETE'});load();showToast('🗑️ تم الحذف');}

/* ── SHELVES ── */
async function loadShelves(){
  const shelves=await api(`/api/shelves?month=${month}`);
  // Summary cards
  document.getElementById('shelfSummary').innerHTML=shelves.map(s=>{
    const netPos=s.net>=0;
    return `<div class="shelf-kpi">
      <div class="shelf-kpi-bar" style="background:${s.color}"></div>
      <div class="shelf-kpi-name"><div class="shelf-dot" style="background:${s.color};box-shadow:0 0 6px ${s.color}66"></div>رف ${s.name}</div>
      <div class="shelf-kpi-grid">
        <div class="skv"><div class="v" style="color:var(--mint)">${fmt(s.monthly_sales)}</div><div class="l">مبيعات ر.ع</div></div>
        <div class="skv"><div class="v" style="color:var(--neg)">${fmt(s.rent)}</div><div class="l">إيجار ر.ع</div></div>
        <div class="skv"><div class="v" style="color:var(--text2)">${s.sales_count}</div><div class="l">عمليات</div></div>
        <div class="skv"><div class="v" style="color:var(--text2)">${s.products.reduce((a,p)=>a+p.qty,0)}</div><div class="l">قطع متبقية</div></div>
      </div>
      <div class="shelf-net ${netPos?'shelf-net-pos':'shelf-net-neg'}">
        <span class="nl">صافي بعد الإيجار</span>
        <span class="nv" style="color:${netPos?'var(--pos)':'var(--neg)'}">${s.net>=0?'+':''}${fmt(s.net)} ر.ع</span>
      </div>
      <button class="rent-btn" onclick="openRent(${s.id},'${s.name}',${s.rent})">✏️ تعديل الإيجار (${fmt(s.rent)} ر.ع)</button>
    </div>`;
  }).join('');
  // Products cards
  document.getElementById('shelfProds').innerHTML=shelves.map(s=>`
    <div class="shelf-prod-card">
      <div class="sp-head" style="border-bottom:2px solid ${s.color}33;">
        <div class="sp-name"><div class="shelf-dot" style="background:${s.color}"></div>رف ${s.name}</div>
        <span class="sp-count" style="background:${s.color}22;color:${s.color}">${s.products.length} منتج</span>
      </div>
      <div class="sp-body">
        ${s.products.length?s.products.map(p=>`
          <div class="prod-row">
            <div class="prod-ph">🌸</div>
            <div class="prod-info"><div class="prod-name">${p.name}</div><div class="prod-price">${fmt(p.price)} ر.ع/قطعة</div></div>
            <div class="prod-right">
              <div class="qty-badge ${p.qty===0?'zero':''}">${p.qty}</div>
              <button class="sell-btn" ${p.qty===0?'disabled':''} onclick="openSell(${p.id},'${p.name.replace(/'/g,"\\'")}',${p.price},${p.qty})">بيع</button>
              <button class="prod-del" onclick="delProd(${p.id})">🗑</button>
            </div>
          </div>`).join(''):`<div style="padding:18px;text-align:center;color:var(--text3);font-size:11px;">لا توجد منتجات بعد</div>`}
      </div>
      <div class="sp-foot"><button class="add-prod-btn" onclick="openAddProd(${s.id},'${s.name}')">+ إضافة منتج لرف ${s.name}</button></div>
    </div>`).join('');
}

function openAddProd(sid,name){
  activeProdShelf=sid;
  document.getElementById('addProdTitle').textContent=`إضافة منتج — رف ${name}`;
  ['pName','pPrice','pQty'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('addProdOv').classList.add('open');
}
function closeProdModal(){document.getElementById('addProdOv').classList.remove('open');}
async function saveProduct(){
  const name=document.getElementById('pName').value.trim();
  const price=parseFloat(document.getElementById('pPrice').value);
  const qty=parseInt(document.getElementById('pQty').value)||0;
  if(!name||!price){showToast('⚠️ أدخل الاسم والسعر');return;}
  await api(`/api/shelves/${activeProdShelf}/products`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,price,qty})});
  closeProdModal();loadShelves();showToast('✅ تم إضافة المنتج');
}
async function delProd(pid){await api(`/api/shelf_products/${pid}`,{method:'DELETE'});loadShelves();showToast('🗑️ تم الحذف');}

function openSell(pid,name,price,qty){
  activeSellProd={pid,name,price,qty};
  document.getElementById('sellDesc').textContent=name;
  document.getElementById('sellInfo').textContent=`السعر: ${fmt(price)} ر.ع | المتاح: ${qty} قطعة`;
  document.getElementById('sellQty').value=1;document.getElementById('sellQty').max=qty;
  document.getElementById('sellPay').value='';
  document.getElementById('sellOv').classList.add('open');
}
function closeSellModal(){document.getElementById('sellOv').classList.remove('open');}
async function confirmSell(){
  const qty=parseInt(document.getElementById('sellQty').value)||1;
  const pay=document.getElementById('sellPay').value;
  if(!activeSellProd)return;
  if(qty>activeSellProd.qty){showToast('⚠️ الكمية أكبر من المتاح');return;}
  await api(`/api/shelf_products/${activeSellProd.pid}/sell`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({qty,payment_method:pay})});
  closeSellModal();
  showToast(`✅ بيع ${qty}× ${activeSellProd.name} — ${fmt(activeSellProd.price*qty)} ر.ع`);
  loadShelves();load();
}

function openRent(sid,name,current){
  activeRentShelf=sid;
  document.getElementById('rentTitle').textContent=`إيجار رف ${name}`;
  document.getElementById('rentVal').value=current;
  document.getElementById('rentOv').classList.add('open');
}
function closeRentModal(){document.getElementById('rentOv').classList.remove('open');}
async function saveRent(){
  const rent=parseFloat(document.getElementById('rentVal').value);
  if(isNaN(rent)||rent<0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  await api(`/api/shelves/${activeRentShelf}/rent`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({rent})});
  closeRentModal();loadShelves();showToast('✅ تم تحديث الإيجار');
}

document.querySelectorAll('.overlay').forEach(o=>o.addEventListener('click',function(e){if(e.target===this)this.classList.remove('open');}));
function changeMonth(){month=document.getElementById('msel').value;load();if(document.getElementById('tab-shelves').classList.contains('active'))loadShelves();}
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
def parse_pg_url(url):
    """Parse postgres:// URL into pg8000 connection params."""
    m = re.match(r'postgres(?:ql)?://([^:]+):([^@]+)@([^:/]+):?(\d*)/(.+)', url)
    if not m:
        raise ValueError("Invalid DATABASE_URL")
    user, password, host, port, database = m.groups()
    return {
        "user": user,
        "password": password,
        "host": host,
        "port": int(port) if port else 5432,
        "database": database.split("?")[0],
        "ssl_context": True
    }

def get_db():
    if USE_PG:
        params = parse_pg_url(os.environ["DATABASE_URL"])
        conn = pg.Connection(**params)
        return conn
    else:
        import sqlite3 as _sq
        conn = _sq.connect(DB_PATH)
        conn.row_factory = _sq.Row
        return conn

def init_db():
    if USE_PG:
        conn = get_db()
        conn.run("""
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
                shelf_id       INTEGER DEFAULT NULL,
                created        TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS shelves (
                id      SERIAL PRIMARY KEY,
                name    TEXT NOT NULL UNIQUE,
                color   TEXT DEFAULT '#e8547a'
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS shelf_products (
                id       SERIAL PRIMARY KEY,
                shelf_id INTEGER NOT NULL REFERENCES shelves(id) ON DELETE CASCADE,
                name     TEXT NOT NULL,
                price    REAL NOT NULL,
                qty      INTEGER NOT NULL DEFAULT 0,
                img      TEXT,
                created  TIMESTAMP DEFAULT NOW()
            )
        """)
        # Insert default shelves
        # Add rent column if not exists
        try:
            cur.execute("ALTER TABLE shelves ADD COLUMN IF NOT EXISTS rent REAL DEFAULT 0")
        except: pass
        cur.execute("""
            INSERT INTO shelves (name, color, rent) VALUES
              ('ريحان',      '#f07090', 10),
              ('فتحية',      '#4ecdc4', 8),
              ('فطوم',       '#b794f4', 8),
              ('اكسسوارات', '#f5c842', 18)
            ON CONFLICT (name) DO UPDATE SET rent = EXCLUDED.rent
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
                shelf_id       INTEGER DEFAULT NULL,
                created        TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shelves (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#e8547a'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shelf_products (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                shelf_id INTEGER NOT NULL,
                name     TEXT NOT NULL,
                price    REAL NOT NULL,
                qty      INTEGER NOT NULL DEFAULT 0,
                img      TEXT,
                created  TEXT DEFAULT (datetime('now'))
            )
        """)
        try:
            conn.execute("ALTER TABLE shelves ADD COLUMN rent REAL DEFAULT 0")
        except: pass
        for row in [('ريحان','#f07090',10),('فتحية','#4ecdc4',8),('فطوم','#b794f4',8),('اكسسوارات','#f5c842',18)]:
            try:
                conn.execute("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", row)
                conn.execute("UPDATE shelves SET rent=? WHERE name=?", (row[2], row[0]))
            except: pass
        for col in ["paid_by","payment_method","sale_time","shelf_id"]:
            try:
                conn.execute(f"ALTER TABLE entries ADD COLUMN {col} TEXT DEFAULT NULL")
            except:
                pass
        conn.commit()
        conn.close()

init_db()

# ── DB query helper ──────────────────────────────────────
def db_exec(sql, params=(), fetch=None):
    """Unified DB execute — handles both pg8000 and SQLite."""
    if USE_PG:
        sql_pg = sql.replace("?", "%s")
        conn = get_db()
        try:
            if fetch == "one":
                rows = conn.run(sql_pg, *params)
                cols = [c["name"] for c in conn.columns]
                if rows:
                    return dict(zip(cols, rows[0]))
                return None
            elif fetch == "all":
                rows = conn.run(sql_pg, *params)
                cols = [c["name"] for c in conn.columns]
                return [dict(zip(cols, r)) for r in rows]
            else:
                conn.run(sql_pg, *params)
                return None
        finally:
            conn.close()
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
# ── Debug endpoint ───────────────────────────────────────
@app.route("/debug")
def debug():
    db_type = "PostgreSQL ✅" if USE_PG else "SQLite ⚠️"
    try:
        count = db_exec("SELECT COUNT(*) as c FROM entries", fetch="one")
        total = count["c"] if count else 0
    except Exception as e:
        total = f"Error: {e}"
    return jsonify({
        "database": db_type,
        "DATABASE_URL_set": bool(os.environ.get("DATABASE_URL")),
        "total_entries": total
    })

# ── Shelves API ───────────────────────────────────────────
@app.route("/api/shelves")
def api_shelves():
    month = request.args.get("month", cur_month())
    rows = db_exec("SELECT * FROM shelves ORDER BY id", fetch="all")
    result = []
    for s in (rows or []):
        prods = db_exec("SELECT * FROM shelf_products WHERE shelf_id=? ORDER BY created DESC", (s["id"],), fetch="all")
        # Calculate monthly sales for this shelf
        sales = db_exec(
            "SELECT COALESCE(SUM(amt),0) as total, COUNT(*) as cnt FROM entries WHERE type='s' AND shelf_id=? AND month=?",
            (s["id"], month), fetch="one"
        )
        total_sales = float(sales["total"]) if sales else 0
        sales_count = int(sales["cnt"]) if sales else 0
        rent = float(s.get("rent") or 0)
        result.append({
            **dict(s),
            "products": prods or [],
            "monthly_sales": total_sales,
            "sales_count": sales_count,
            "rent": rent,
            "net": total_sales - rent
        })
    return jsonify(result)

@app.route("/api/shelves/<int:sid>/products", methods=["POST"])
def api_add_product(sid):
    d = request.json
    db_exec("INSERT INTO shelf_products (shelf_id,name,price,qty,img) VALUES (?,?,?,?,?)",
            (sid, d["name"], float(d["price"]), int(d.get("qty",0)), d.get("img")))
    return jsonify({"ok": True})

@app.route("/api/shelf_products/<int:pid>", methods=["DELETE"])
def api_del_product(pid):
    db_exec("DELETE FROM shelf_products WHERE id=?", (pid,))
    return jsonify({"ok": True})

@app.route("/api/shelf_products/<int:pid>/sell", methods=["POST"])
def api_sell_product(pid):
    d = request.json
    qty = int(d.get("qty", 1))
    payment_method = d.get("payment_method") or None
    prod = db_exec("SELECT * FROM shelf_products WHERE id=?", (pid,), fetch="one")
    if not prod:
        return jsonify({"ok": False, "error": "not found"}), 404
    new_qty = max(0, prod["qty"] - qty)
    db_exec("UPDATE shelf_products SET qty=? WHERE id=?", (new_qty, pid))
    month = datetime.now().strftime("%Y-%m")
    date  = datetime.now().strftime("%d/%m/%Y")
    total = prod["price"] * qty
    shelf = db_exec("SELECT name FROM shelves WHERE id=?", (prod["shelf_id"],), fetch="one")
    shelf_name = shelf["name"] if shelf else ""
    db_exec("INSERT INTO entries (type,desc,amt,date,month,shelf_id,payment_method) VALUES (?,?,?,?,?,?,?)",
            ("s", f'{prod["name"]} — رف {shelf_name}', total, date, month, prod["shelf_id"], payment_method))
    return jsonify({"ok": True, "new_qty": new_qty, "total": total})

@app.route("/api/shelf_products/<int:pid>/qty", methods=["POST"])
def api_update_qty(pid):
    d = request.json
    db_exec("UPDATE shelf_products SET qty=? WHERE id=?", (int(d["qty"]), pid))
    return jsonify({"ok": True})

@app.route("/api/shelves/<int:sid>/rent", methods=["POST"])
def api_update_rent(sid):
    d = request.json
    db_exec("UPDATE shelves SET rent=? WHERE id=?", (float(d["rent"]), sid))
    return jsonify({"ok": True})

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
