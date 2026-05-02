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
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root {
  --cream:#fdf8f2;--warm:#f5ede0;--petal:#f9c8d0;--rose:#e8798a;--rose-d:#c4566a;
  --green:#7aab8a;--green-d:#5a8a6a;--gold:#d4a557;--brown:#6b4c3b;
  --text:#3d2c24;--text2:#7a6458;--text3:#b09888;
  --glass:rgba(255,255,255,0.55);--glass2:rgba(255,255,255,0.35);
  --glass-border:rgba(255,255,255,0.8);--glass-border2:rgba(255,255,255,0.5);
  --shadow:rgba(107,76,59,0.12);--shadow2:rgba(107,76,59,0.08);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}

body {
  font-family:'Tajawal',sans-serif;
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
  background: var(--cream);
}

/* ── Beautiful floral background ── */
.bg-scene {
  position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;
}
.bg-gradient {
  position:absolute;inset:0;
  background:
    radial-gradient(ellipse 80% 60% at 10% 0%, #fce4ec 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 100%, #e8f5e9 0%, transparent 60%),
    radial-gradient(ellipse 70% 50% at 50% 50%, #fff8f0 0%, transparent 70%),
    linear-gradient(160deg, #fdf3f0 0%, #f0f7f2 50%, #fef9f0 100%);
}
/* Decorative flower SVG elements */
.flower {
  position:absolute;opacity:0.18;animation:sway 8s ease-in-out infinite;
}
.flower:nth-child(1){top:-5%;right:5%;width:320px;animation-delay:0s;}
.flower:nth-child(2){bottom:-3%;left:-3%;width:280px;animation-delay:-3s;animation-duration:10s;}
.flower:nth-child(3){top:35%;right:-4%;width:200px;animation-delay:-5s;animation-duration:12s;opacity:0.12;}
.flower:nth-child(4){top:10%;left:3%;width:160px;animation-delay:-2s;animation-duration:9s;opacity:0.1;}
@keyframes sway {
  0%,100%{transform:rotate(-3deg) scale(1);}
  50%{transform:rotate(3deg) scale(1.02);}
}
/* Floating petals */
.petals-wrap{position:absolute;inset:0;}
.fp{position:absolute;border-radius:50% 0;animation:fpFall linear infinite;opacity:0;}
@keyframes fpFall {
  0%{transform:translateY(-20px) rotate(0deg) scale(0.8);opacity:0;}
  10%{opacity:0.6;}
  90%{opacity:0.2;}
  100%{transform:translateY(100vh) rotate(720deg) scale(0.4);opacity:0;}
}

/* ── App wrapper ── */
#app{position:relative;z-index:1;}

/* ── Header ── */
header {
  padding:0 32px;height:68px;
  display:flex;align-items:center;justify-content:space-between;
  background:var(--glass);
  backdrop-filter:blur(24px) saturate(1.8);
  -webkit-backdrop-filter:blur(24px) saturate(1.8);
  border-bottom:1px solid var(--glass-border);
  position:sticky;top:0;z-index:100;
  box-shadow:0 2px 24px var(--shadow2);
}
.brand{display:flex;align-items:center;gap:12px;}
.emblem{
  width:42px;height:42px;border-radius:14px;
  background:linear-gradient(135deg,#f9c8d0,#e8798a);
  display:flex;align-items:center;justify-content:center;font-size:20px;
  box-shadow:0 4px 16px rgba(232,121,138,0.35);
  animation:emblemFloat 4s ease-in-out infinite;
}
@keyframes emblemFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-3px);}}
.bname{
  font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:600;
  color:var(--brown);letter-spacing:0.5px;
}
.bsub{font-size:10px;color:var(--text3);letter-spacing:1px;}
.hright{display:flex;align-items:center;gap:10px;}

/* NAV TABS */
.main-tabs{
  display:flex;gap:3px;
  background:rgba(255,255,255,0.5);
  border:1px solid var(--glass-border);
  padding:3px;border-radius:12px;
  backdrop-filter:blur(10px);
}
.mtab{
  padding:7px 16px;border:none;border-radius:9px;
  font-family:'Tajawal',sans-serif;font-size:12px;font-weight:700;
  cursor:pointer;transition:all .25s;background:transparent;color:var(--text3);
}
.mtab.on{
  background:white;color:var(--rose-d);
  box-shadow:0 2px 12px var(--shadow);
}

/* MONTH PILL */
.mpill{
  display:flex;align-items:center;gap:7px;
  background:var(--glass);backdrop-filter:blur(10px);
  border:1px solid var(--glass-border);
  padding:6px 14px;border-radius:40px;
  box-shadow:0 2px 10px var(--shadow2);
}
.mpill label{font-size:11px;color:var(--text3);}
.mpill select{background:transparent;border:none;color:var(--text);font-family:'Tajawal',sans-serif;font-size:13px;font-weight:600;cursor:pointer;outline:none;}
.mpill select option{background:white;color:var(--text);}

/* PAGES */
.page{display:none;max-width:1200px;margin:0 auto;padding:28px 18px 64px;}
.page.active{display:block;}

/* SECTION LABEL */
.slbl{
  font-size:10px;font-weight:700;color:var(--text3);
  letter-spacing:2.5px;text-transform:uppercase;
  margin-bottom:12px;display:flex;align-items:center;gap:10px;
}
.slbl::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(212,165,87,.3),transparent);}

/* GLASS CARD */
.gc{
  background:var(--glass);
  backdrop-filter:blur(20px) saturate(1.6);
  -webkit-backdrop-filter:blur(20px) saturate(1.6);
  border:1px solid var(--glass-border);
  border-radius:22px;
  box-shadow:0 4px 32px var(--shadow2), inset 0 1px 0 rgba(255,255,255,0.9);
}

/* KPI */
.kpi-row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:22px;}
.kpi{
  padding:22px 20px;cursor:default;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1),box-shadow .3s;
  animation:fadeUp .6s ease both;position:relative;overflow:hidden;
}
.kpi::before{
  content:'';position:absolute;top:-30px;right:-30px;
  width:80px;height:80px;border-radius:50%;opacity:0.15;
  transition:transform .3s;
}
.kpi:hover{transform:translateY(-4px);box-shadow:0 12px 40px var(--shadow);}
.kpi:hover::before{transform:scale(1.4);}
.ks::before{background:var(--green);}
.kb::before{background:var(--rose);}
.kp::before{background:var(--gold);}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
.kpi:nth-child(2){animation-delay:.08s;}.kpi:nth-child(3){animation-delay:.16s;}
.kpi-ico{
  width:44px;height:44px;border-radius:12px;
  display:flex;align-items:center;justify-content:center;font-size:20px;
  margin-bottom:12px;
  background:rgba(255,255,255,0.7);
  box-shadow:0 2px 10px var(--shadow2);
}
.kpi-lbl{font-size:10px;color:var(--text3);margin-bottom:4px;letter-spacing:.5px;}
.kpi-val{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:600;line-height:1;margin-bottom:6px;letter-spacing:-0.5px;}
.ks .kpi-val{color:var(--green-d);}
.kb .kpi-val{color:var(--rose-d);}
.kp .kpi-val{color:var(--gold);}
.kpi-sub{font-size:10px;color:var(--text3);}
.badge{padding:2px 8px;border-radius:20px;font-size:9px;font-weight:700;}
.bp{background:rgba(122,171,138,.15);color:var(--green-d);}
.bn{background:rgba(232,121,138,.15);color:var(--rose-d);}
.chips{display:flex;gap:4px;margin-top:8px;flex-wrap:wrap;}
.chip{padding:2px 8px;border-radius:20px;font-size:9px;font-weight:600;background:rgba(255,255,255,0.7);}
.ch-c{color:var(--green-d);}
.ch-v{color:#6b8fc4;}
.ch-t{color:#9b7bc4;}
.ch-p{color:var(--rose-d);}

/* FORM CARD */
.add-card{padding:22px;margin-bottom:22px;}
.type-tabs{
  display:flex;gap:5px;
  background:rgba(255,255,255,0.5);
  border:1px solid var(--glass-border);
  border-radius:12px;padding:4px;margin-bottom:18px;
}
.ttab{
  flex:1;padding:9px;border:none;border-radius:9px;
  font-family:'Tajawal',sans-serif;font-size:13px;font-weight:700;
  cursor:pointer;transition:all .25s;background:transparent;
  color:var(--text3);display:flex;align-items:center;justify-content:center;gap:6px;
}
.tt-s{background:white;color:var(--green-d);box-shadow:0 2px 10px var(--shadow2);}
.tt-b{background:white;color:var(--rose-d);box-shadow:0 2px 10px var(--shadow2);}

/* FIELDS */
.fgrid{display:grid;gap:10px;margin-bottom:12px;}
.fg2{grid-template-columns:1fr 1fr;}
.fg3{grid-template-columns:1fr 1fr 1fr;}
.fld{display:flex;flex-direction:column;gap:4px;}
.fld label{font-size:10px;font-weight:700;color:var(--text3);letter-spacing:.8px;text-transform:uppercase;}
.fld input,.fld select{
  background:rgba(255,255,255,0.7);
  border:1px solid var(--glass-border);
  border-radius:10px;padding:9px 13px;
  font-family:'Tajawal',sans-serif;font-size:13px;color:var(--text);
  outline:none;transition:.2s;width:100%;
  box-shadow:0 2px 8px var(--shadow2);
}
.fld input:focus,.fld select:focus{
  border-color:var(--rose);background:white;
  box-shadow:0 0 0 3px rgba(232,121,138,0.15);
}
.fld input::placeholder{color:var(--text3);}
.fld select option{background:white;color:var(--text);}

/* BUTTONS */
.sbtn{
  height:42px;padding:0 22px;border:none;border-radius:10px;
  font-family:'Tajawal',sans-serif;font-size:13px;font-weight:700;
  cursor:pointer;transition:all .25s cubic-bezier(.34,1.56,.64,1);
  display:flex;align-items:center;gap:6px;
  box-shadow:0 4px 14px var(--shadow);
}
.sb-s{background:linear-gradient(135deg,#7aab8a,#5a8a6a);color:white;}
.sb-s:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 8px 22px rgba(90,138,106,.35);}
.sb-b{background:linear-gradient(135deg,#e8798a,#c4566a);color:white;}
.sb-b:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 8px 22px rgba(196,86,106,.35);}

/* PANELS */
.panels{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:22px;}
.panel{overflow:hidden;display:flex;flex-direction:column;}
.ph{
  padding:14px 18px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--glass-border2);
}
.ph-l{display:flex;align-items:center;gap:9px;}
.pico{
  width:32px;height:32px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;font-size:15px;
  background:rgba(255,255,255,0.7);box-shadow:0 2px 8px var(--shadow2);
}
.ptitle{font-size:13px;font-weight:700;}
.ps .ptitle{color:var(--green-d);}
.pb .ptitle{color:var(--rose-d);}
.pcnt{font-size:9px;font-weight:800;padding:2px 8px;border-radius:14px;}
.ps .pcnt{background:rgba(122,171,138,.15);color:var(--green-d);}
.pb .pcnt{background:rgba(232,121,138,.15);color:var(--rose-d);}
.pbody{padding:8px;flex:1;overflow-y:auto;max-height:270px;scrollbar-width:thin;scrollbar-color:rgba(212,165,87,.3) transparent;}
.pbody::-webkit-scrollbar{width:3px;}
.pbody::-webkit-scrollbar-thumb{background:rgba(212,165,87,.3);border-radius:4px;}

.empty{padding:28px;text-align:center;color:var(--text3);}
.empty .ei{font-size:32px;margin-bottom:8px;opacity:0.4;}
.empty p{font-size:12px;line-height:1.9;}

.entry{
  display:flex;align-items:center;gap:8px;padding:10px 8px;
  border-radius:10px;margin-bottom:2px;transition:.2s;
  animation:entryIn .35s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes entryIn{from{opacity:0;transform:scale(.94) translateY(-4px);}to{opacity:1;transform:scale(1) translateY(0);}}
.entry:hover{background:rgba(255,255,255,0.6);}
.edot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.es .edot{background:var(--green);box-shadow:0 0 5px rgba(122,171,138,.5);}
.eb .edot{background:var(--rose);box-shadow:0 0 5px rgba(232,121,138,.4);}
.eph{width:32px;height:32px;border-radius:7px;background:rgba(255,255,255,0.7);border:1px solid var(--glass-border2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.einfo{flex:1;min-width:0;}
.edesc{font-size:12px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text);}
.emeta{display:flex;gap:4px;margin-top:2px;flex-wrap:wrap;align-items:center;}
.edate{font-size:9px;color:var(--text3);}
.epb{font-size:9px;font-weight:700;padding:1px 6px;border-radius:8px;background:rgba(255,255,255,0.7);}
.epb-c{color:var(--green-d);}
.epb-v{color:#6b8fc4;}
.epb-t{color:#9b7bc4;}
.epb-p{color:var(--rose-d);}
.epb-s{color:var(--gold);}
.eamt{font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:600;white-space:nowrap;flex-shrink:0;}
.eamt.inc{color:var(--green-d);}
.eamt.exp{color:var(--rose-d);}
.delbtn{background:none;border:none;cursor:pointer;color:var(--text3);font-size:12px;width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;transition:.2s;flex-shrink:0;}
.delbtn:hover{background:rgba(232,121,138,.15);color:var(--rose-d);}

/* CHARTS */
.charts-row{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;margin-bottom:22px;}
.chart-card{padding:20px;}
.chart-card h3{font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:600;color:var(--text2);margin-bottom:14px;display:flex;align-items:center;gap:7px;}

/* SHELVES */
.shelf-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;}
.shelf-kpi{padding:18px 16px;position:relative;overflow:hidden;animation:fadeUp .5s ease both;cursor:default;transition:transform .3s cubic-bezier(.34,1.56,.64,1),box-shadow .3s;}
.shelf-kpi:hover{transform:translateY(-4px);box-shadow:0 12px 36px var(--shadow);}
.shelf-kpi-bar{position:absolute;top:0;right:0;left:0;height:3px;border-radius:22px 22px 0 0;}
.shelf-kpi-name{font-size:13px;font-weight:800;margin-bottom:12px;display:flex;align-items:center;gap:7px;color:var(--brown);}
.shelf-dot{width:8px;height:8px;border-radius:50%;}
.shelf-kpi-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.skv{text-align:center;padding:8px 6px;background:rgba(255,255,255,0.55);border-radius:9px;border:1px solid var(--glass-border);}
.skv .v{font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:600;line-height:1;color:var(--brown);}
.skv .l{font-size:9px;color:var(--text3);margin-top:2px;}
.shelf-net{margin-top:10px;padding:8px 12px;border-radius:10px;display:flex;justify-content:space-between;align-items:center;}
.shelf-net-pos{background:rgba(122,171,138,.12);border:1px solid rgba(122,171,138,.25);}
.shelf-net-neg{background:rgba(232,121,138,.1);border:1px solid rgba(232,121,138,.2);}
.shelf-net .nl{font-size:9px;color:var(--text3);}
.shelf-net .nv{font-family:'Cormorant Garamond',serif;font-size:15px;font-weight:600;}
.rent-btn{background:rgba(255,255,255,0.6);border:1px solid var(--glass-border);border-radius:8px;color:var(--text3);font-size:9px;font-family:'Tajawal',sans-serif;padding:4px 10px;cursor:pointer;transition:.2s;margin-top:8px;width:100%;}
.rent-btn:hover{border-color:var(--gold);color:var(--gold);background:rgba(212,165,87,.08);}
.shelf-prods-section{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;}
.shelf-prod-card{overflow:hidden;}
.sp-head{padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--glass-border2);}
.sp-name{font-size:13px;font-weight:700;display:flex;align-items:center;gap:7px;color:var(--brown);}
.sp-count{font-size:9px;font-weight:700;padding:2px 9px;border-radius:12px;background:rgba(255,255,255,0.7);}
.sp-body{padding:6px;max-height:220px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:rgba(212,165,87,.3) transparent;}
.prod-row{display:flex;align-items:center;gap:8px;padding:8px 6px;border-radius:9px;border-bottom:1px solid rgba(255,255,255,0.5);transition:.2s;}
.prod-row:last-child{border-bottom:none;}
.prod-row:hover{background:rgba(255,255,255,0.5);}
.prod-ph{width:32px;height:32px;border-radius:7px;background:rgba(255,255,255,0.7);border:1px solid var(--glass-border);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.prod-info{flex:1;min-width:0;}
.prod-name{font-size:12px;font-weight:600;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.prod-price{font-size:9px;color:var(--text3);margin-top:1px;}
.prod-right{display:flex;align-items:center;gap:5px;flex-shrink:0;}
.qty-badge{min-width:26px;padding:2px 7px;border-radius:7px;font-size:10px;font-weight:800;text-align:center;background:rgba(122,171,138,.15);color:var(--green-d);}
.qty-badge.zero{background:rgba(232,121,138,.12);color:var(--rose-d);}
.sell-btn{background:linear-gradient(135deg,var(--green),var(--green-d));border:none;border-radius:7px;color:white;font-size:10px;font-weight:700;padding:4px 10px;cursor:pointer;font-family:'Tajawal',sans-serif;transition:.2s;box-shadow:0 2px 8px rgba(90,138,106,.25);}
.sell-btn:hover{transform:scale(1.06);}
.sell-btn:disabled{opacity:.3;cursor:not-allowed;transform:none;}
.prod-del{background:none;border:none;cursor:pointer;color:var(--text3);font-size:11px;width:22px;height:22px;border-radius:5px;display:flex;align-items:center;justify-content:center;transition:.2s;flex-shrink:0;}
.prod-del:hover{background:rgba(232,121,138,.15);color:var(--rose-d);}
.sp-foot{padding:10px 14px;border-top:1px solid var(--glass-border2);}
.add-prod-btn{width:100%;padding:8px;border:1px dashed rgba(212,165,87,.4);border-radius:9px;background:rgba(255,255,255,0.4);color:var(--text3);font-family:'Tajawal',sans-serif;font-size:11px;font-weight:600;cursor:pointer;transition:.2s;}
.add-prod-btn:hover{border-color:var(--gold);color:var(--gold);background:rgba(212,165,87,.06);}

/* MODAL */
.overlay{display:none;position:fixed;inset:0;background:rgba(107,76,59,0.25);backdrop-filter:blur(16px) saturate(1.5);z-index:500;align-items:center;justify-content:center;padding:20px;}
.overlay.open{display:flex;}
.modal{
  background:rgba(255,255,255,0.85);
  backdrop-filter:blur(30px) saturate(2);
  -webkit-backdrop-filter:blur(30px) saturate(2);
  border:1px solid var(--glass-border);
  border-radius:22px;padding:28px;
  max-width:380px;width:100%;text-align:center;
  box-shadow:0 24px 80px rgba(107,76,59,0.2), inset 0 1px 0 rgba(255,255,255,1);
  animation:modalIn .4s cubic-bezier(.34,1.56,.64,1);
}
@keyframes modalIn{from{opacity:0;transform:scale(.88) translateY(16px);}to{opacity:1;transform:scale(1) translateY(0);}}
.mico{font-size:44px;margin-bottom:12px;}
.modal h3{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:600;color:var(--brown);margin-bottom:6px;}
.modal p{font-size:12px;color:var(--text2);margin-bottom:18px;line-height:1.7;}
.minput{width:100%;background:rgba(255,255,255,0.8);border:1px solid var(--glass-border);border-radius:10px;padding:11px 14px;font-family:'Tajawal',sans-serif;font-size:16px;font-weight:700;text-align:center;color:var(--text);outline:none;margin-bottom:12px;transition:.2s;box-shadow:0 2px 8px var(--shadow2);}
.minput:focus{border-color:var(--rose);box-shadow:0 0 0 3px rgba(232,121,138,.15);}
.minput.sm{font-size:13px;font-weight:500;text-align:right;}
.mbtns{display:flex;gap:8px;}
.mbtns button{flex:1;padding:10px;border:none;border-radius:10px;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:.2s;box-shadow:0 2px 10px var(--shadow2);}
.bc{background:rgba(255,255,255,0.8);border:1px solid var(--glass-border)!important;color:var(--text2);}
.bc:hover{background:white;}
.bcs{background:linear-gradient(135deg,var(--green),var(--green-d));color:white;}
.bcs:hover{transform:scale(1.02);}
.bcp{background:linear-gradient(135deg,var(--rose),var(--rose-d));color:white;}
.bcp:hover{transform:scale(1.02);}

.lb{display:none;position:fixed;inset:0;background:rgba(107,76,59,0.6);backdrop-filter:blur(10px);z-index:9000;align-items:center;justify-content:center;cursor:zoom-out;}
.lb.open{display:flex;}
.lb img{max-width:90vw;max-height:88vh;border-radius:16px;box-shadow:0 24px 80px rgba(0,0,0,.3);}

.toast{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(80px);background:rgba(255,255,255,0.9);backdrop-filter:blur(20px);border:1px solid var(--glass-border);color:var(--text);padding:10px 24px;border-radius:40px;font-size:13px;font-weight:600;box-shadow:0 8px 32px var(--shadow);transition:transform .4s cubic-bezier(.34,1.56,.64,1);z-index:9999;white-space:nowrap;}
.toast.show{transform:translateX(-50%) translateY(0);}

@media(max-width:768px){
  header{padding:0 12px;}
  .kpi-row,.panels,.charts-row,.shelf-summary,.shelf-prods-section{grid-template-columns:1fr;gap:10px;}
  .fg2,.fg3{grid-template-columns:1fr;}
  .kpi-val{font-size:22px;}
  .add-card{padding:16px;}
  .mtab{font-size:11px;padding:5px 10px;}
}
</style>
</head>
<body>

<!-- BG SCENE -->
<div class="bg-scene">
  <div class="bg-gradient"></div>

  <!-- Decorative flowers using SVG -->
  <svg class="flower" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g opacity="1">
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f9c8d0" transform="rotate(0 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f5a8b8" transform="rotate(45 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f9c8d0" transform="rotate(90 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f5a8b8" transform="rotate(135 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f9c8d0" transform="rotate(180 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f5a8b8" transform="rotate(225 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f9c8d0" transform="rotate(270 200 200)"/>
      <ellipse cx="200" cy="120" rx="40" ry="70" fill="#f5a8b8" transform="rotate(315 200 200)"/>
      <circle cx="200" cy="200" r="35" fill="#f5c842" opacity="0.8"/>
      <circle cx="200" cy="200" r="22" fill="#e8a832"/>
    </g>
  </svg>

  <svg class="flower" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g>
      <ellipse cx="200" cy="110" rx="35" ry="65" fill="#c8e6c9" transform="rotate(0 200 200)"/>
      <ellipse cx="200" cy="110" rx="35" ry="65" fill="#a5d6a7" transform="rotate(60 200 200)"/>
      <ellipse cx="200" cy="110" rx="35" ry="65" fill="#c8e6c9" transform="rotate(120 200 200)"/>
      <ellipse cx="200" cy="110" rx="35" ry="65" fill="#a5d6a7" transform="rotate(180 200 200)"/>
      <ellipse cx="200" cy="110" rx="35" ry="65" fill="#c8e6c9" transform="rotate(240 200 200)"/>
      <ellipse cx="200" cy="110" rx="35" ry="65" fill="#a5d6a7" transform="rotate(300 200 200)"/>
      <circle cx="200" cy="200" r="32" fill="#fff9c4" opacity="0.9"/>
      <circle cx="200" cy="200" r="18" fill="#f5c842"/>
    </g>
  </svg>

  <svg class="flower" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g>
      <ellipse cx="150" cy="85" rx="28" ry="55" fill="#fce4ec" transform="rotate(0 150 150)"/>
      <ellipse cx="150" cy="85" rx="28" ry="55" fill="#f8bbd9" transform="rotate(72 150 150)"/>
      <ellipse cx="150" cy="85" rx="28" ry="55" fill="#fce4ec" transform="rotate(144 150 150)"/>
      <ellipse cx="150" cy="85" rx="28" ry="55" fill="#f8bbd9" transform="rotate(216 150 150)"/>
      <ellipse cx="150" cy="85" rx="28" ry="55" fill="#fce4ec" transform="rotate(288 150 150)"/>
      <circle cx="150" cy="150" r="28" fill="#fff3e0" opacity="0.9"/>
      <circle cx="150" cy="150" r="16" fill="#ffb74d"/>
    </g>
  </svg>

  <svg class="flower" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g>
      <ellipse cx="100" cy="55" rx="20" ry="40" fill="#e8eaf6" transform="rotate(0 100 100)"/>
      <ellipse cx="100" cy="55" rx="20" ry="40" fill="#c5cae9" transform="rotate(90 100 100)"/>
      <ellipse cx="100" cy="55" rx="20" ry="40" fill="#e8eaf6" transform="rotate(180 100 100)"/>
      <ellipse cx="100" cy="55" rx="20" ry="40" fill="#c5cae9" transform="rotate(270 100 100)"/>
      <circle cx="100" cy="100" r="22" fill="#fff9c4"/>
      <circle cx="100" cy="100" r="12" fill="#f5c842"/>
    </g>
  </svg>

  <!-- Floating petals -->
  <div class="petals-wrap" id="petalsWrap"></div>
</div>

<div id="app">
<header>
  <div class="brand">
    <div class="emblem">🌸</div>
    <div><div class="bname">فيروز فلورز</div><div class="bsub">إدارة المبيعات والمشتريات</div></div>
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
    <div class="kpi ks gc"><div class="kpi-ico">💰</div><div class="kpi-lbl">إجمالي المبيعات</div>
      <div class="kpi-val" id="kS">0 ر.ع</div><div class="kpi-sub" id="kSc">0 عملية</div>
      <div class="chips" id="payChips"></div></div>
    <div class="kpi kb gc"><div class="kpi-ico">🛒</div><div class="kpi-lbl">إجمالي المشتريات</div>
      <div class="kpi-val" id="kB">0 ر.ع</div><div class="kpi-sub" id="kBc">0 عملية</div>
      <div class="chips" id="payerChips"></div></div>
    <div class="kpi kp gc"><div class="kpi-ico">📊</div><div class="kpi-lbl">صافي الربح</div>
      <div class="kpi-val" id="kP">0 ر.ع</div><div class="kpi-sub"><span id="kPb" class="badge">—</span></div></div>
  </div>

  <div class="slbl">إضافة جديد</div>
  <div class="add-card gc">
    <div class="type-tabs">
      <button class="ttab tt-s" id="tt-s" onclick="setFT('s')">🌸 مبيعات</button>
      <button class="ttab" id="tt-b" onclick="setFT('b')">📦 مشتريات</button>
    </div>
    <div id="form-s">
      <div class="fgrid fg2"><div class="fld"><label>اسم المنتج</label><input id="sDesc" type="text" placeholder="باقة ورد، عطر..."/></div>
        <div class="fld"><label>السعر (ر.ع)</label><input id="sAmt" type="number" placeholder="0.000" step="0.001"/></div></div>
      <div class="fgrid fg2" style="margin-bottom:14px;">
        <div class="fld"><label>💳 طريقة الدفع</label>
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
    <div class="panel ps gc"><div class="ph"><div class="ph-l"><div class="pico">🌸</div><div class="ptitle">المبيعات</div></div><div class="pcnt" id="sbadge">0</div></div><div class="pbody" id="sl"></div></div>
    <div class="panel pb gc"><div class="ph"><div class="ph-l"><div class="pico">📦</div><div class="ptitle">المشتريات</div></div><div class="pcnt" id="bbadge">0</div></div><div class="pbody" id="bl"></div></div>
  </div>

  <div class="slbl">الإحصائيات</div>
  <div class="charts-row">
    <div class="chart-card gc"><h3>📈 مبيعات ومشتريات 2026</h3><canvas id="barChart" height="150"></canvas></div>
    <div class="chart-card gc"><h3>💳 طريقة الدفع</h3><canvas id="payChart" height="150"></canvas></div>
    <div class="chart-card gc"><h3>👤 من دفع المشتريات</h3><canvas id="payerChart" height="150"></canvas></div>
  </div>
</div>

<!-- SHELVES -->
<div id="tab-shelves" class="page">
  <div class="slbl">ملخص الرفوف</div>
  <div class="shelf-summary" id="shelfSummary"></div>
  <div class="slbl">منتجات الرفوف</div>
  <div class="shelf-prods-section" id="shelfProds"></div>
</div>
</div>

<!-- MODALS -->
<div class="overlay" id="addProdOv">
  <div class="modal">
    <div class="mico">🌷</div>
    <h3 id="addProdTitle">إضافة منتج</h3>
    <input class="minput sm" id="pName" type="text" placeholder="اسم المنتج" style="margin-bottom:10px;"/>
    <div class="fgrid fg2" style="margin-bottom:14px;">
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
    <p id="sellDesc" style="font-size:14px;font-weight:700;color:var(--brown);margin-bottom:3px;"></p>
    <p id="sellInfo" style="font-size:11px;color:var(--text3);margin-bottom:14px;"></p>
    <div class="fgrid fg2" style="margin-bottom:14px;">
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
let barCI=null,payCI=null,payerCI=null;
let activeProdShelf=null,activeSellProd=null,activeRentShelf=null;

/* Petals */
(function(){
  const wrap=document.getElementById('petalsWrap');
  const colors=['#f9c8d0','#f5a8b8','#c8e6c9','#a5d6a7','#fce4ec','#fff9c4'];
  for(let i=0;i<18;i++){
    const p=document.createElement('div');p.className='fp';
    const c=colors[Math.floor(Math.random()*colors.length)];
    const size=6+Math.random()*10;
    p.style.cssText=`left:${Math.random()*100}vw;width:${size}px;height:${size*1.4}px;background:${c};animation-duration:${12+Math.random()*16}s;animation-delay:${Math.random()*20}s;`;
    wrap.appendChild(p);
  }
})();

async function api(url,opts){const r=await fetch(url,opts);return r.json();}
function fmt(n){return (+n).toLocaleString('ar-OM',{minimumFractionDigits:3,maximumFractionDigits:3});}

function switchTab(t){
  document.getElementById('tab-home').className='page'+(t==='home'?' active':'');
  document.getElementById('tab-shelves').className='page'+(t==='shelves'?' active':'');
  document.querySelectorAll('.mtab').forEach((b,i)=>b.className='mtab'+(i===(t==='home'?0:1)?' on':''));
  if(t==='shelves')loadShelves();
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

async function load(){
  const d=await api(`/api/entries?month=${month}`);
  renderKPI(d.sales,d.buys);renderLists(d.sales,d.buys);loadCharts();
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

function renderKPI(sales,buys){
  const ts=sales.reduce((a,e)=>a+e.amt,0);
  const tb=buys.reduce((a,e)=>a+e.amt,0);
  const tp=ts-tb;
  document.getElementById('kS').textContent=fmt(ts)+' ر.ع';
  document.getElementById('kSc').textContent=sales.length+' عملية';
  document.getElementById('kB').textContent=fmt(tb)+' ر.ع';
  document.getElementById('kBc').textContent=buys.length+' عملية';
  document.getElementById('kP').textContent=(tp>=0?'+':'')+fmt(tp)+' ر.ع';
  document.getElementById('kP').style.color=tp>=0?'var(--gold)':'var(--rose-d)';
  const b=document.getElementById('kPb');
  b.textContent=tp>0?'✅ في الربح':tp<0?'⚠️ في الخسارة':'—';
  b.className='badge '+(tp>0?'bp':tp<0?'bn':'');
  const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};
  sales.forEach(e=>{if(e.payment_method&&pm[e.payment_method]!==undefined)pm[e.payment_method]+=e.amt;});
  document.getElementById('payChips').innerHTML=Object.entries(pm).filter(([,v])=>v>0)
    .map(([k,v])=>`<span class="chip ch-c">${k} ${fmt(v)}</span>`).join('');
  const py={};buys.forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});
  document.getElementById('payerChips').innerHTML=Object.entries(py)
    .map(([k,v])=>`<span class="chip ch-p">👤${k} ${fmt(v)}</span>`).join('');
}

function pb(pm){if(!pm)return'';const c=pm.includes('كاش')?'epb-c':pm.includes('فيزا')?'epb-v':'epb-t';return`<span class="epb ${c}">${pm}</span>`;}
function renderLists(sales,buys){
  document.getElementById('sl').innerHTML=sales.length?sales.map(e=>`
    <div class="entry es"><div class="eph">🌸</div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${pb(e.payment_method)}${e.shelf_id?`<span class="epb epb-s">🗄️رف</span>`:''}</div></div>
      <div class="eamt inc">+${fmt(e.amt)} ر.ع</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button></div>`).join('')
    :`<div class="empty"><div class="ei">🌷</div><p>لا توجد مبيعات<br>أضف من هنا أو عبر التيليغرام</p></div>`;
  document.getElementById('bl').innerHTML=buys.length?buys.map(e=>`
    <div class="entry eb"><div class="edot"></div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${e.paid_by?`<span class="epb epb-p">👤${e.paid_by}</span>`:''}</div></div>
      <div class="eamt exp">-${fmt(e.amt)} ر.ع</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button></div>`).join('')
    :`<div class="empty"><div class="ei">🌿</div><p>لا توجد مشتريات<br>أضف من هنا أو عبر التيليغرام</p></div>`;
  document.getElementById('sbadge').textContent=sales.length;
  document.getElementById('bbadge').textContent=buys.length;
}

const mnames=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
const co={responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(107,76,59,.06)'},ticks:{color:'#b09888',font:{family:'Tajawal',size:9}}},y:{grid:{color:'rgba(107,76,59,.06)'},ticks:{color:'#b09888',font:{family:'Tajawal',size:9}}}}};
function renderBarChart(aS,aB){if(barCI)barCI.destroy();barCI=new Chart(document.getElementById('barChart'),{type:'bar',data:{labels:mnames.map(m=>m.slice(0,3)),datasets:[{label:'مبيعات',data:aS,backgroundColor:'rgba(122,171,138,.7)',borderRadius:5},{label:'مشتريات',data:aB,backgroundColor:'rgba(232,121,138,.65)',borderRadius:5}]},options:{...co,plugins:{legend:{display:true,labels:{color:'#7a6458',font:{family:'Tajawal',size:10}}}}}});}
function renderPayChart(sales){const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};sales.forEach(e=>{if(e.payment_method&&pm[e.payment_method]!==undefined)pm[e.payment_method]+=e.amt;});if(payCI)payCI.destroy();payCI=new Chart(document.getElementById('payChart'),{type:'doughnut',data:{labels:Object.keys(pm),datasets:[{data:Object.values(pm),backgroundColor:['rgba(122,171,138,.8)','rgba(107,143,196,.8)','rgba(155,123,196,.8)'],borderWidth:0,hoverOffset:6}]},options:{responsive:true,cutout:'64%',plugins:{legend:{position:'bottom',labels:{color:'#7a6458',font:{family:'Tajawal',size:9},padding:6}}}}});}
function renderPayerChart(buys){const py={};buys.forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});const clrs=['rgba(232,121,138,.8)','rgba(122,171,138,.8)','rgba(212,165,87,.8)','rgba(155,123,196,.8)'];if(payerCI)payerCI.destroy();payerCI=new Chart(document.getElementById('payerChart'),{type:'doughnut',data:{labels:Object.keys(py).length?Object.keys(py):['لا يوجد'],datasets:[{data:Object.keys(py).length?Object.values(py):[1],backgroundColor:Object.keys(py).length?clrs.slice(0,Object.keys(py).length):['rgba(176,152,136,.2)'],borderWidth:0,hoverOffset:6}]},options:{responsive:true,cutout:'64%',plugins:{legend:{position:'bottom',labels:{color:'#7a6458',font:{family:'Tajawal',size:9},padding:6}}}}});}

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

async function loadShelves(){
  const shelves=await api(`/api/shelves?month=${month}`);
  document.getElementById('shelfSummary').innerHTML=shelves.map(s=>{
    const netPos=s.net>=0;
    return `<div class="shelf-kpi gc">
      <div class="shelf-kpi-bar" style="background:${s.color}"></div>
      <div class="shelf-kpi-name"><div class="shelf-dot" style="background:${s.color};box-shadow:0 0 8px ${s.color}88"></div>رف ${s.name}</div>
      <div class="shelf-kpi-grid">
        <div class="skv"><div class="v" style="color:var(--green-d)">${fmt(s.monthly_sales)}</div><div class="l">مبيعات ر.ع</div></div>
        <div class="skv"><div class="v" style="color:var(--rose-d)">${fmt(s.rent)}</div><div class="l">إيجار ر.ع</div></div>
        <div class="skv"><div class="v">${s.sales_count}</div><div class="l">عمليات</div></div>
        <div class="skv"><div class="v">${s.products.reduce((a,p)=>a+p.qty,0)}</div><div class="l">قطع</div></div>
      </div>
      <div class="shelf-net ${netPos?'shelf-net-pos':'shelf-net-neg'}">
        <span class="nl">صافي بعد الإيجار</span>
        <span class="nv" style="color:${netPos?'var(--green-d)':'var(--rose-d)'}">${s.net>=0?'+':''}${fmt(s.net)} ر.ع</span>
      </div>
      <button class="rent-btn" onclick="openRent(${s.id},'${s.name}',${s.rent})">✏️ إيجار: ${fmt(s.rent)} ر.ع</button>
    </div>`;}).join('');

  document.getElementById('shelfProds').innerHTML=shelves.map(s=>`
    <div class="shelf-prod-card gc">
      <div class="sp-head" style="border-bottom:2px solid ${s.color}44;">
        <div class="sp-name"><div class="shelf-dot" style="background:${s.color}"></div>رف ${s.name}</div>
        <span class="sp-count" style="color:${s.color}">${s.products.length} منتج</span>
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
          </div>`).join(''):`<div style="padding:20px;text-align:center;color:var(--text3);font-size:12px;">لا توجد منتجات بعد</div>`}
      </div>
      <div class="sp-foot"><button class="add-prod-btn" onclick="openAddProd(${s.id},'${s.name}')">+ إضافة منتج لرف ${s.name}</button></div>
    </div>`).join('');
}

function openAddProd(sid,name){activeProdShelf=sid;document.getElementById('addProdTitle').textContent=`إضافة منتج — رف ${name}`;['pName','pPrice','pQty'].forEach(id=>document.getElementById(id).value='');document.getElementById('addProdOv').classList.add('open');}
function closeProdModal(){document.getElementById('addProdOv').classList.remove('open');}
async function saveProduct(){
  const name=document.getElementById('pName').value.trim();const price=parseFloat(document.getElementById('pPrice').value);const qty=parseInt(document.getElementById('pQty').value)||0;
  if(!name||!price){showToast('⚠️ أدخل الاسم والسعر');return;}
  await api(`/api/shelves/${activeProdShelf}/products`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,price,qty})});
  closeProdModal();loadShelves();showToast('✅ تم إضافة المنتج');
}
async function delProd(pid){await api(`/api/shelf_products/${pid}`,{method:'DELETE'});loadShelves();showToast('🗑️ تم الحذف');}
function openSell(pid,name,price,qty){activeSellProd={pid,name,price,qty};document.getElementById('sellDesc').textContent=name;document.getElementById('sellInfo').textContent=`السعر: ${fmt(price)} ر.ع | المتاح: ${qty} قطعة`;document.getElementById('sellQty').value=1;document.getElementById('sellQty').max=qty;document.getElementById('sellPay').value='';document.getElementById('sellOv').classList.add('open');}
function closeSellModal(){document.getElementById('sellOv').classList.remove('open');}
async function confirmSell(){
  const qty=parseInt(document.getElementById('sellQty').value)||1;const pay=document.getElementById('sellPay').value;
  if(!activeSellProd)return;if(qty>activeSellProd.qty){showToast('⚠️ الكمية أكبر من المتاح');return;}
  await api(`/api/shelf_products/${activeSellProd.pid}/sell`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({qty,payment_method:pay})});
  closeSellModal();showToast(`✅ بيع ${qty}× ${activeSellProd.name} — ${fmt(activeSellProd.price*qty)} ر.ع`);loadShelves();load();
}
function openRent(sid,name,current){activeRentShelf=sid;document.getElementById('rentTitle').textContent=`إيجار رف ${name}`;document.getElementById('rentVal').value=current;document.getElementById('rentOv').classList.add('open');}
function closeRentModal(){document.getElementById('rentOv').classList.remove('open');}
async function saveRent(){
  const rent=parseFloat(document.getElementById('rentVal').value);if(isNaN(rent)||rent<0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
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

# ── DB query helper ──────────────────────────────────────
def db_exec(sql, params=(), fetch=None):
    """Unified DB execute — handles both pg8000 and SQLite."""
    if USE_PG:
        sql_pg = sql.replace("?", "%s")
        conn = get_db()
        try:
            # pg8000 native uses $1,$2,... placeholders
            i = 0
            def replacer(m):
                nonlocal i
                i += 1
                return f"${i}"
            sql_final = re.sub(r'%s', replacer, sql_pg)
            rows = conn.run(sql_final, *list(params))
            cols = [c["name"] for c in conn.columns] if conn.columns else []
            if fetch == "one":
                if rows:
                    row = dict(zip(cols, rows[0]))
                    if "description" in row: row["desc"] = row.pop("description")
                    return row
                return None
            elif fetch == "all":
                result = []
                for r in rows:
                    row = dict(zip(cols, r))
                    if "description" in row: row["desc"] = row.pop("description")
                    result.append(row)
                return result
            return None
        except Exception as e:
            print(f"DB Error: {e} | SQL: {sql_pg} | Params: {params}")
            raise
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


def init_db():
    if USE_PG:
        sqls = [
            """CREATE TABLE IF NOT EXISTS entries (
                id SERIAL PRIMARY KEY, type TEXT NOT NULL,
                description TEXT NOT NULL, amt REAL NOT NULL,
                date TEXT NOT NULL, month TEXT NOT NULL, img TEXT,
                paid_by TEXT DEFAULT NULL, payment_method TEXT DEFAULT NULL,
                sale_time TEXT DEFAULT NULL, shelf_id INTEGER DEFAULT NULL,
                created TIMESTAMP DEFAULT NOW())""",
            """CREATE TABLE IF NOT EXISTS shelves (
                id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#e8547a', rent REAL DEFAULT 0)""",
            """CREATE TABLE IF NOT EXISTS shelf_products (
                id SERIAL PRIMARY KEY, shelf_id INTEGER NOT NULL,
                name TEXT NOT NULL, price REAL NOT NULL,
                qty INTEGER NOT NULL DEFAULT 0, img TEXT,
                created TIMESTAMP DEFAULT NOW())""",
            """INSERT INTO shelves (name,color,rent) VALUES
                ('ريحان','#f07090',10),('فتحية','#4ecdc4',8),
                ('فطوم','#b794f4',8),('اكسسوارات','#f5c842',18)
                ON CONFLICT (name) DO UPDATE SET rent=EXCLUDED.rent""",
        ]
        optional_sqls = [
            "ALTER TABLE entries RENAME COLUMN desc TO description",
            "ALTER TABLE shelves ADD COLUMN IF NOT EXISTS rent REAL DEFAULT 0",
            "ALTER TABLE entries ADD COLUMN IF NOT EXISTS paid_by TEXT DEFAULT NULL",
            "ALTER TABLE entries ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT NULL",
            "ALTER TABLE entries ADD COLUMN IF NOT EXISTS sale_time TEXT DEFAULT NULL",
            "ALTER TABLE entries ADD COLUMN IF NOT EXISTS shelf_id TEXT DEFAULT NULL",
        ]
        for sql in sqls:
            db_exec(sql)
        for sql in optional_sqls:
            try: db_exec(sql)
            except: pass
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

# ── Helpers ───────────────────────────────────────────────
def fmt_omr(n):
    return f"{n:,.3f} ر.ع"

def cur_month():
    return datetime.now().strftime("%Y-%m")

def get_month_data(month):
    rows = db_exec("SELECT * FROM entries WHERE month=? ORDER BY created DESC", (month,), fetch="all") or []
    sales = [r for r in rows if r.get("type") == "s"]
    buys  = [r for r in rows if r.get("type") == "b"]
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
        db_exec("INSERT INTO entries (type,description,amt,date,month,img,paid_by,payment_method,sale_time) VALUES (?,?,?,?,?,?,?,?,?)", vals)
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
        db_exec("DELETE FROM entries WHERE id=?", (eid,))
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
    db_exec("INSERT INTO entries (type,description,amt,date,month,shelf_id,payment_method) VALUES (?,?,?,?,?,?,?)",
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
                    db_exec(                             "INSERT INTO entries (type,description,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                             ("b", desc, amt, dt, month_s, paid_by)                         )
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
                db_exec(                         "INSERT INTO entries (type,description,amt,date,month) VALUES (?,?,?,?,?)",                         ("b", desc, amt, date, month)                     )
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
                db_exec(                         "INSERT INTO entries (type,description,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                         ("b", desc, amt, dt, month_s, paid_by)                     )
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
            db_exec(                     "INSERT INTO entries (type,description,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                     ("b", desc, amt, state["date"], month_s, paid_by)                 )
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
                db_exec(                         "INSERT INTO entries (type,description,amt,date,month) VALUES (?,?,?,?,?)",                         ("b", desc, amt, date, month)                     )
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
                db_exec(                         "INSERT INTO entries (type,description,amt,date,month) VALUES (?,?,?,?,?)",                         ("s", desc, amt, date, month)                     )
                pending[chat_id] = {"waiting": "sale_payment", "desc": desc, "amt": amt, "date": date, "month": month}
                tg_buttons(chat_id,
                   f"🌸 <b>مبيعة {fmt_omr(amt)}</b> — تم التسجيل!\n\n💳 <b>طريقة الدفع؟</b>",
                   [[{"label": "💵 كاش",    "data": "pay:كاش 💵"},
                     {"label": "💳 فيزا",   "data": "pay:فيزا 💳"},
                     {"label": "🏦 تحويل",  "data": "pay:تحويل 🏦"}]])
                return "ok"
            else:
                db_exec(                         "INSERT INTO entries (type,description,amt,date,month,payment_method) VALUES (?,?,?,?,?,?)",                         ("s", desc, amt, date, month, pay_method)                     )
                tg(chat_id,
                   f"✅ <b>تم التسجيل!</b>\n\n"
                   f"🌸 مبيعة\n📝 {desc}\n💰 {fmt_omr(amt)}\n💳 {pay_method}\n📅 {date}")
                return "ok"

        db_exec(                 "INSERT INTO entries (type,description,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",                 (etype, desc, amt, date, month, paid_by)             )
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
