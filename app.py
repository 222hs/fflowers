import os
import re
import sqlite3
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────
BOT_TOKEN   = os.environ.get("BOT_TOKEN", "")
GROQ_KEY    = os.environ.get("GROQ_API_KEY", "")
DB_PATH     = os.environ.get("DB_PATH", "fairuz.db")
TURSO_URL   = os.environ.get("TURSO_URL", "")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN", "")
USE_TURSO   = bool(TURSO_URL and TURSO_TOKEN)

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

.exp-row{display:flex;align-items:center;gap:10px;padding:12px 16px;border-radius:12px;margin-bottom:8px;background:var(--glass);backdrop-filter:blur(12px);border:1px solid var(--glass-border);transition:.2s;}
.exp-row:hover{box-shadow:0 4px 16px var(--shadow);}
.exp-ico{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;background:rgba(255,255,255,0.7);flex-shrink:0;}
.exp-info{flex:1;min-width:0;}
.exp-name{font-size:13px;font-weight:700;color:var(--brown);}
.exp-last{font-size:10px;color:var(--text3);margin-top:2px;}
.exp-amt{font-size:16px;font-weight:800;font-family:"Cormorant Garamond",serif;color:var(--rose-d);flex-shrink:0;}
.exp-pay-btn{background:linear-gradient(135deg,var(--green),var(--green-d));border:none;border-radius:8px;color:white;font-size:11px;font-weight:700;padding:6px 12px;cursor:pointer;font-family:"Tajawal",sans-serif;transition:.2s;flex-shrink:0;box-shadow:0 2px 8px rgba(90,138,106,.25);}
.exp-pay-btn.paid{background:rgba(122,171,138,.15);color:var(--green-d);box-shadow:none;}
.exp-pay-btn:hover{transform:scale(1.04);}
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
  <div class="kpi-row" style="grid-template-columns:repeat(2,1fr);margin-bottom:10px;">
    <div class="kpi ks gc"><div class="kpi-ico">💰</div><div class="kpi-lbl">إجمالي المبيعات</div>
      <div class="kpi-val" id="kS">0 ر.ع</div><div class="kpi-sub" id="kSc">0 عملية</div>
      <div class="chips" id="payChips"></div></div>
    <div class="kpi kb gc"><div class="kpi-ico">🛒</div><div class="kpi-lbl">إجمالي المشتريات</div>
      <div class="kpi-val" id="kB">0 ر.ع</div><div class="kpi-sub" id="kBc">0 عملية</div>
      <div class="chips" id="payerChips"></div></div>
  </div>
  <div class="kpi-row" style="grid-template-columns:repeat(3,1fr);margin-bottom:22px;">
    <div class="kpi gc" style="border-right:3px solid rgba(232,121,138,.3);">
      <div class="kpi-ico">💸</div><div class="kpi-lbl">المصاريف الثابتة</div>
      <div class="kpi-val" id="kE" style="color:var(--rose-d)">0 ر.ع</div>
      <div class="kpi-sub" id="kEd">راتب + إيجار + كهرباء</div>
    </div>
    <div class="kpi kp gc">
      <div class="kpi-ico">📊</div><div class="kpi-lbl">ربح قبل المصاريف</div>
      <div class="kpi-val" id="kP">0 ر.ع</div>
      <div class="kpi-sub"><span id="kPb" class="badge">—</span></div>
    </div>
    <div class="kpi gc" style="border-right:3px solid rgba(122,171,138,.3);">
      <div class="kpi-ico">🏆</div><div class="kpi-lbl">الربح الصافي النهائي</div>
      <div class="kpi-val" id="kN">0 ر.ع</div>
      <div class="kpi-sub"><span id="kNb" class="badge">—</span></div>
    </div>
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
      <div class="fgrid fg3" style="margin-bottom:14px;">
        <div class="fld"><label>🏷️ الفئة</label>
          <select id="sCat"><option value="">— اختر —</option>
            <option value="ورد وباقات">🌸 ورد وباقات</option>
            <option value="طباعة">🖨️ طباعة 3D</option>
            <option value="تاجات">👑 تاجات</option>
            <option value="عطور">🌿 عطور</option>
            <option value="اكسسوارات">💍 اكسسوارات</option>
            <option value="هدايا">🎁 هدايا وتغليف</option>
            <option value="تجفيف">🌾 ورد مجفف</option>
            <option value="صناعي">🎨 صناعي وفوم</option>
            <option value="أخرى">✨ أخرى</option></select></div>
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

  <!-- EXPENSES -->
  <div class="slbl">المصاريف الثابتة</div>
  <div id="expensesWrap" style="margin-bottom:22px;"></div>

  <!-- PDF REPORTS -->
  <div class="slbl">التقارير والنسخ الاحتياطية</div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:10px;">
    <button onclick="dlPDF('sales')" style="padding:12px 8px;background:rgba(122,171,138,.1);border:1px solid rgba(122,171,138,.25);border-radius:12px;font-family:Tajawal,sans-serif;font-size:12px;font-weight:700;color:#5a8a6a;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">📄 تقرير المبيعات</button>
    <button onclick="dlPDF('buys')" style="padding:12px 8px;background:rgba(232,121,138,.08);border:1px solid rgba(232,121,138,.2);border-radius:12px;font-family:Tajawal,sans-serif;font-size:12px;font-weight:700;color:#c4566a;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">📄 تقرير المشتريات</button>
    <button onclick="dlPDF('expenses')" style="padding:12px 8px;background:rgba(212,165,87,.08);border:1px solid rgba(212,165,87,.2);border-radius:12px;font-family:Tajawal,sans-serif;font-size:12px;font-weight:700;color:#d4a557;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">📄 تقرير المصاريف</button>
    <button onclick="dlPDF('all')" style="padding:12px 8px;background:rgba(107,76,59,.08);border:1px solid rgba(107,76,59,.2);border-radius:12px;font-family:Tajawal,sans-serif;font-size:12px;font-weight:700;color:var(--brown);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">📊 تقرير شامل</button>
  </div>
  <div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;">
    <button onclick="doBackup()" style="flex:1;padding:10px;background:rgba(122,171,138,.08);border:1px solid rgba(122,171,138,.2);border-radius:10px;font-family:Tajawal,sans-serif;font-size:12px;font-weight:700;color:#5a8a6a;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">
      💾 نسخة احتياطية JSON
    </button>
    <label style="flex:1;padding:10px;background:rgba(212,165,87,.07);border:1px solid rgba(212,165,87,.2);border-radius:10px;font-family:Tajawal,sans-serif;font-size:12px;font-weight:700;color:#d4a557;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">
      📂 استعادة من ملف
      <input type="file" accept=".json" onchange="doRestore(event)" style="display:none"/>
    </label>
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
  const [d, expD] = await Promise.all([
    api(`/api/entries?month=${month}`),
    api(`/api/expenses?month=${month}`)
  ]);
  renderKPI(d.sales, d.buys, expD);
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

function renderKPI(sales, buys, expD){
  const ts=sales.reduce((a,e)=>a+e.amt,0);
  const tb=buys.filter(e=>e.type!=='expense').reduce((a,e)=>a+e.amt,0);
  const tp=ts-tb;

  // Fixed expenses: sum from paid entries this month
  const paidExps=(expD&&expD.paid)||[];
  const te=paidExps.reduce((a,e)=>a+e.amt,0);
  // Also sum monthly expense amounts for display
  const allExps=(expD&&expD.expenses)||[];
  const expNames=allExps.map(e=>e.name).join(' + ');
  const tn=tp-te; // net after expenses

  document.getElementById('kS').textContent=fmt(ts)+' ر.ع';
  document.getElementById('kSc').textContent=sales.length+' عملية';
  document.getElementById('kB').textContent=fmt(tb)+' ر.ع';
  document.getElementById('kBc').textContent=buys.filter(e=>e.type!=='expense').length+' عملية';

  document.getElementById('kE').textContent=fmt(te)+' ر.ع';
  document.getElementById('kEd').textContent=te>0?`${paidExps.length} مصروف مدفوع`:'لم تُدفع بعد';

  document.getElementById('kP').textContent=(tp>=0?'+':'')+fmt(tp)+' ر.ع';
  document.getElementById('kP').style.color=tp>=0?'var(--gold)':'var(--rose-d)';
  const b=document.getElementById('kPb');
  b.textContent=tp>0?'✅ ربح':tp<0?'⚠️ خسارة':'—';
  b.className='badge '+(tp>0?'bp':tp<0?'bn':'');

  document.getElementById('kN').textContent=(tn>=0?'+':'')+fmt(tn)+' ر.ع';
  document.getElementById('kN').style.color=tn>=0?'var(--green-d)':'var(--rose-d)';
  const nb=document.getElementById('kNb');
  nb.textContent=tn>0?'🏆 صافي الربح':tn<0?'⚠️ خسارة صافية':'—';
  nb.className='badge '+(tn>0?'bp':tn<0?'bn':'');

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
  const catIcons={"ورد وباقات":"🌸","طباعة":"🖨️","تاجات":"👑","عطور":"🌿","اكسسوارات":"💍","هدايا":"🎁","تجفيف":"🌾","صناعي":"🎨","أخرى":"✨"};
  document.getElementById('sl').innerHTML=sales.length?sales.map(e=>`
    <div class="entry es"><div class="eph">${catIcons[e.category]||'🌸'}</div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${pb(e.payment_method)}${e.category?`<span class="epb" style="background:rgba(212,165,87,.12);color:#d4a557">${e.category}</span>`:''}${e.shelf_id?`<span class="epb epb-s">🗄️رف</span>`:''}</div></div>
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
  const cat=document.getElementById('sCat').value;
  const note=document.getElementById('sNote').value.trim();
  if(!amt||amt<=0){showToast('⚠️ أدخل مبلغاً صحيحاً');return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'s',desc:note?`${desc} — ${note}`:desc,amt,payment_method:pay||null,category:cat||null,month})});
  document.getElementById('sDesc').value='';document.getElementById('sAmt').value='';
  document.getElementById('sPay').value='';document.getElementById('sCat').value='';document.getElementById('sNote').value='';
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
function changeMonth(){month=document.getElementById('msel').value;load();loadExpensesPanel();if(document.getElementById('tab-shelves').classList.contains('active'))loadShelves();}
function showToast(msg){const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3000);}

load();
loadExpensesPanel();

/* ── EXPENSES ── */
async function loadExpensesPanel(){
  const d = await api(`/api/expenses?month=${month}`);
  const icons = {"راتب العامل":"👷","إيجار المحل":"🏪","فاتورة الكهرباء":"⚡"};
  const wrap = document.getElementById('expensesWrap');
  if(!wrap) return;

  let html = '';

  // Each expense definition
  for(const e of (d.expenses||[])){
    const isElec = e.name.includes('كهرباء');
    const icon = icons[e.name] || '💼';
    // Get all paid entries for this expense this month
    const myPaid = (d.paid||[]).filter(p => p.desc && p.desc.includes(e.name.replace('فاتورة ','').split(' ')[0]));
    const totalPaid = myPaid.reduce((a,p)=>a+p.amt, 0);
    const isPaid = myPaid.length > 0;
    const lastDate = myPaid.length ? myPaid[myPaid.length-1].date : null;

    html += `<div class="exp-row" style="${isPaid?'border-color:rgba(122,171,138,.3);':''}" >
      <div class="exp-ico">${icon}</div>
      <div class="exp-info">
        <div class="exp-name">${e.name}</div>
        <div class="exp-last">${isPaid ? '✅ آخر دفع: '+lastDate : (e.last_paid ? 'آخر تعبئة: '+e.last_paid : 'لم يُدفع بعد')}</div>
      </div>
      <div class="exp-amt" style="color:${isPaid?'var(--green-d)':'var(--rose-d)'};">${isPaid?fmt(totalPaid):fmt(e.amount)} ر.ع</div>
      <button class="exp-pay-btn" onclick="${isElec?`addElecBill(${e.id})`:`payExpense(${e.id},'${e.name}',${e.amount})`}">
        ${isElec?'⚡ إضافة تعبئة':'💳 دفع'}
      </button>
    </div>`;

    // Show all paid entries for this expense with delete button
    if(myPaid.length){
      html += `<div style="margin:-4px 0 8px 0;padding:6px 10px;background:rgba(122,171,138,.06);border-radius:0 0 10px 10px;border:1px solid rgba(122,171,138,.15);border-top:none;">`;
      for(const p of myPaid){
        html += `<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid rgba(0,0,0,.04);">
          <span style="font-size:11px;color:var(--text2);flex:1;">📅 ${p.date} — ${fmt(p.amt)} ر.ع</span>
          <button onclick="delSingleExpEntry(${p.id},${e.id})" style="background:rgba(232,121,138,.1);border:1px solid rgba(232,121,138,.25);border-radius:6px;color:var(--rose-d);font-size:10px;padding:3px 8px;cursor:pointer;font-family:Tajawal,sans-serif;">🗑 حذف</button>
        </div>`;
      }
      html += `</div>`;
    }
  }

  html += `<button onclick="addExpensePrompt()" style="width:100%;padding:9px;border:1px dashed rgba(212,165,87,.4);border-radius:10px;background:rgba(255,255,255,0.4);color:var(--text3);font-family:Tajawal,sans-serif;font-size:12px;font-weight:600;cursor:pointer;margin-top:8px;">+ إضافة مصروف ثابت</button>`;

  wrap.innerHTML = html;
}

async function delSingleExpEntry(entryId, expId){
  if(!confirm('حذف هذه الفاتورة؟')) return;
  await api(`/api/expense_entries/${entryId}`, {method:'DELETE'});
  // Check if any paid entries remain, if not reset expense
  const d2 = await api(`/api/expenses?month=${month}`);
  const exp = (d2.expenses||[]).find(e=>e.id===expId);
  if(exp){
    const remaining = (d2.paid||[]).filter(p=>p.desc&&p.desc.includes(exp.name.replace('فاتورة ','').split(' ')[0]));
    if(!remaining.length){
      await api(`/api/expenses/${expId}/reset`,{method:'POST',
        headers:{'Content-Type':'application/json'},body:JSON.stringify({month})});
    }
  }
  loadExpensesPanel(); load();
  showToast('✅ تم حذف الفاتورة');
}

async function addElecBill(expId){
  const amt = prompt('مبلغ التعبئة (ر.ع):', '');
  if(!amt) return;
  const a = parseFloat(amt);
  if(isNaN(a)||a<=0){showToast('⚠️ مبلغ غير صحيح');return;}
  const dateStr = prompt('تاريخ التعبئة (DD/MM/YYYY):', new Date().toLocaleDateString('en-GB'));
  if(!dateStr) return;
  // Parse month from date
  let entryMonth = month;
  try{
    const parts = dateStr.split('/');
    if(parts.length===3) entryMonth = `${parts[2]}-${parts[1].padStart(2,'0')}`;
  }catch(e){}
  await api(`/api/expenses/${expId}/pay`,{method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({month:entryMonth, amount:a, date:dateStr})});
  loadExpensesPanel(); load();
  showToast(`⚡ تم تسجيل تعبئة ${fmt(a)} ر.ع`);
}

async function delExpenseEntry(entryId, name, expId){
  if(!confirm(`إلغاء دفع "${name}"؟`)) return;
  await api(`/api/expense_entries/${entryId}`, {method:'DELETE'});
  await api(`/api/expenses/${expId}/reset`, {method:'POST',
    headers:{'Content-Type':'application/json'},body:JSON.stringify({month})});
  loadExpensesPanel(); load();
  showToast('✅ تم إلغاء الدفع');
}

async function cancelExpense(expId, name){
  if(!confirm(`إلغاء دفع "${name}"؟\nسيتم حذف الفاتورة وإعادتها لغير مدفوع`)) return;
  // Find and delete all expense entries for this name this month
  const d = await api(`/api/expenses?month=${month}`);
  const entries = (d.paid||[]).filter(p => p.desc && p.desc.includes(name.split(' ')[0]));
  for(const e of entries){
    await api(`/api/expense_entries/${e.id}`, {method:'DELETE'});
  }
  await api(`/api/expenses/${expId}/reset`, {method:'POST',
    headers:{'Content-Type':'application/json'},body:JSON.stringify({month})});
  loadExpensesPanel(); load();
  showToast('✅ تم إلغاء الدفع');
}

async function payExpense(id, name, defaultAmt){
  const amt = prompt(`ادفع ${name}\nالمبلغ (ر.ع):`, defaultAmt.toFixed(3));
  if(!amt) return;
  const a = parseFloat(amt);
  if(isNaN(a)||a<=0){showToast('⚠️ مبلغ غير صحيح');return;}
  await api(`/api/expenses/${id}/pay`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month,amount:a})});
  loadExpensesPanel(); load();
  showToast(`✅ تم تسجيل دفع ${name} — ${fmt(a)} ر.ع`);
}

async function addExpensePrompt(){
  const name = prompt('اسم المصروف (مثال: صيانة، تأمين...):');
  if(!name) return;
  const amt = prompt('المبلغ الشهري (ر.ع):','0.000');
  if(!amt) return;
  await api('/api/expenses',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,amount:parseFloat(amt)||0})});
  loadExpenses();
  showToast('✅ تمت إضافة المصروف');
}

/* ── PDF REPORTS ── */
function dlPDF(type){
  showToast('⏳ جاري إنشاء التقرير...');
  const url = `/api/report/pdf?month=${month}&type=${type}`;
  const a = document.createElement('a');
  a.href = url;
  a.download = `fairuz_${type}_${month}.pdf`;
  a.click();
}

/* ── BACKUP / RESTORE ── */
async function doBackup(){
  try {
    showToast('⏳ جاري تصدير البيانات...');
    const r = await fetch('/api/backup');
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fairuz_backup_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('✅ تم تصدير النسخة الاحتياطية');
  } catch(e) {
    showToast('❌ خطأ في التصدير');
  }
}

async function doRestore(ev){
  const file = ev.target.files[0];
  if(!file) return;
  ev.target.value = '';
  if(!confirm('هل أنت متأكد؟ سيتم استيراد البيانات من الملف.')) return;
  try {
    showToast('⏳ جاري الاستيراد...');
    const text = await file.text();
    const data = JSON.parse(text);
    const r = await api('/api/restore', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if(r.ok) {
      showToast(`✅ تم الاستيراد — ${r.restored.entries} إدخال، ${r.restored.products} منتج`);
      load();
    } else {
      showToast('❌ ' + (r.error || 'خطأ في الاستيراد'));
    }
  } catch(e) {
    showToast('❌ ملف غير صالح');
  }
}
</script>
</body>
</html>
"""

# ── Database (Turso or SQLite) ────────────────────────────
def turso_exec(sql, params=()):
    """Execute SQL on Turso via HTTP API."""
    args = [{"type": "null"} if p is None else {"type": "text", "value": str(p)} for p in params]
    payload = {"requests": [{"type": "execute", "stmt": {"sql": sql, "args": args}}, {"type": "close"}]}
    # Fix URL: libsql:// -> https://
    url = TURSO_URL.replace("libsql://", "https://")
    r = requests.post(
        f"{url}/v2/pipeline",
        headers={"Authorization": f"Bearer {TURSO_TOKEN}", "Content-Type": "application/json"},
        json=payload, timeout=15
    )
    r.raise_for_status()
    return r.json()

def turso_get(sql, params=()):
    """Query rows from Turso."""
    try:
        res = turso_exec(sql, params)
        result = res["results"][0]
        if result.get("type") == "error":
            print("Turso error:", result)
            return []
        data = result["response"]["result"]
        cols = [c["name"] for c in data["cols"]]
        rows = []
        for row in data["rows"]:
            d = {}
            for i, col in enumerate(cols):
                v = row[i]
                t = v.get("type","text")
                val = v.get("value")
                if t == "null" or val is None:
                    d[col] = None
                elif t in ("integer",):
                    try: d[col] = int(val)
                    except: d[col] = val
                elif t in ("float","real"):
                    try: d[col] = float(val)
                    except: d[col] = val
                else:
                    d[col] = val
            rows.append(d)
        return rows
    except Exception as e:
        print("Turso get error:", e)
        return []

def turso_run(sql, params=()):
    """Execute write SQL on Turso."""
    try:
        res = turso_exec(sql, params)
        if res["results"][0].get("type") == "error":
            print("Turso run error:", res["results"][0])
    except Exception as e:
        print("Turso run error:", e)

def init_db():
    sqls = [
        """CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, desc TEXT NOT NULL,
            amt REAL NOT NULL, date TEXT NOT NULL,
            month TEXT NOT NULL, img TEXT,
            paid_by TEXT, payment_method TEXT,
            sale_time TEXT, shelf_id INTEGER,
            created TEXT DEFAULT (datetime('now')))""",
        """CREATE TABLE IF NOT EXISTS shelves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            color TEXT DEFAULT '#e8547a',
            rent REAL DEFAULT 0)""",
        """CREATE TABLE IF NOT EXISTS shelf_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shelf_id INTEGER NOT NULL, name TEXT NOT NULL,
            price REAL NOT NULL, qty INTEGER DEFAULT 0,
            img TEXT, created TEXT DEFAULT (datetime('now')))""",
    ]
    shelf_rows = [
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('ريحان','#f07090',10)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('فتحية','#4ecdc4',8)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('فطوم','#b794f4',8)),
        ("INSERT OR IGNORE INTO shelves (name,color,rent) VALUES (?,?,?)", ('اكسسوارات','#f5c842',18)),
    ]
    migrations = [
        "ALTER TABLE entries ADD COLUMN paid_by TEXT",
        "ALTER TABLE entries ADD COLUMN payment_method TEXT",
        "ALTER TABLE entries ADD COLUMN sale_time TEXT",
        "ALTER TABLE entries ADD COLUMN shelf_id INTEGER",
        "ALTER TABLE shelves ADD COLUMN rent REAL DEFAULT 0",
        "ALTER TABLE entries ADD COLUMN category TEXT",
    ]
    # Expenses table
    fixed_sqls = [
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            type TEXT DEFAULT 'monthly',
            last_paid TEXT,
            month TEXT,
            note TEXT,
            created TEXT DEFAULT (datetime('now')))""",
    ]
    for sql in fixed_sqls:
        if USE_TURSO: turso_run(sql)
        else:
            try:
                conn2=sqlite3.connect(DB_PATH); conn2.execute(sql); conn2.commit(); conn2.close()
            except: pass
    # Clean duplicate expenses first, then insert defaults
    if USE_TURSO:
        all_exp = turso_get("SELECT * FROM expenses ORDER BY id")
        seen = {}
        for e in all_exp:
            if e["name"] in seen:
                turso_run("DELETE FROM expenses WHERE id=?", (e["id"],))
            else:
                seen[e["name"]] = e["id"]
    defaults = [
        ("راتب العامل", 220, "monthly"),
        ("إيجار المحل", 100, "monthly"),
        ("فاتورة الكهرباء", 0, "variable"),
    ]
    for name, amt, typ in defaults:
        if USE_TURSO:
            existing = turso_get("SELECT id FROM expenses WHERE name=?", (name,))
            if not existing:
                turso_run("INSERT INTO expenses (name,amount,type) VALUES (?,?,?)", (name, amt, typ))
        else:
            try:
                conn3=sqlite3.connect(DB_PATH)
                conn3.execute("INSERT OR IGNORE INTO expenses (name,amount,type) VALUES (?,?,?)", (name, amt, typ))
                conn3.commit(); conn3.close()
            except: pass
    if USE_TURSO:
        for sql in sqls:
            turso_run(sql)
        for sql, params in shelf_rows:
            turso_run(sql, params)
        for sql in migrations:
            turso_run(sql)  # Ignore errors for existing columns
    else:
        conn = sqlite3.connect(DB_PATH)
        for sql in sqls:
            conn.execute(sql)
        for sql, params in shelf_rows:
            try: conn.execute(sql, params)
            except: pass
        for sql in migrations:
            try: conn.execute(sql)
            except: pass
        conn.commit(); conn.close()

init_db()

def db_get(sql, params=()):
    if USE_TURSO:
        return turso_get(sql, params)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows

def db_one(sql, params=()):
    rows = db_get(sql, params)
    return rows[0] if rows else None

def db_run(sql, params=()):
    if USE_TURSO:
        turso_run(sql, params)
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute(sql, params)
    conn.commit(); conn.close()

# ── Helpers ───────────────────────────────────────────────
def fmt_omr(n): return f"{n:,.3f} ر.ع"
def cur_month(): return datetime.now().strftime("%Y-%m")

def get_month_data(month):
    rows = db_get("SELECT * FROM entries WHERE month=? ORDER BY created DESC", (month,))
    return ([r for r in rows if r["type"]=="s"],
            [r for r in rows if r["type"] in ("b","expense")])

def month_summary(month):
    s,b = get_month_data(month)
    ts=sum(e["amt"] for e in s); tb=sum(e["amt"] for e in b)
    return ts,tb,ts-tb,len(s),len(b)

# ── Telegram ──────────────────────────────────────────────
def tg(chat_id, text):
    if not BOT_TOKEN: return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id":chat_id,"text":text,"parse_mode":"HTML"}, timeout=10)
    except: pass

def tg_buttons(chat_id, text, buttons):
    if not BOT_TOKEN: return
    kb={"inline_keyboard":[[{"text":b["label"],"callback_data":b["data"]} for b in row] for row in buttons]}
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id":chat_id,"text":text,"parse_mode":"HTML","reply_markup":kb}, timeout=10)
    except: pass

SALE_WORDS=["بعت","مبيعة","بيع","بعثت","باعت"]
BUY_WORDS=["اشتريت","شريت","مشتريات","شراء","دفعت","فاتورة","طلبية"]

CATEGORIES = {
    "طباعة": ["طباعة","طابعة","3d","ثري دي","ثلاثية","طباعه"],
    "تاجات": ["تاج","تاجات","كراون","crown"],
    "ورد وباقات": ["ورد","باقة","باقه","وردة","زهور","زهرة","بوكيه","بوكيه"],
    "عطور": ["عطر","عطور","برفان","perfume","بخور"],
    "اكسسوارات": ["اكسسوار","اكسسوارات","خاتم","سوار","عقد","قلادة","حلق"],
    "هدايا": ["هدية","هدايا","gift","تغليف","تغليفه"],
    "تجفيف": ["مجفف","مجففة","dried","ورد مجفف"],
    "صناعي": ["صناعي","اصطناعي","فوم","foam"],
}

def detect_category(text):
    text_lower = text.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text_lower:
                return cat
    return None

def parse_text(text):
    text=text.strip()
    etype=None
    for w in SALE_WORDS:
        if w in text: etype="s"; break
    if not etype:
        for w in BUY_WORDS:
            if w in text: etype="b"; break
    amt=None
    for pat in [r'الإجمالي[^\d]*(\d+[.,]\d+)',r'Net Total[^\d]*(\d+[.,]\d+)',r'بـ\s*(\d+[.,]\d+)',r'بـ\s*(\d+)']:
        m=re.search(pat,text)
        if m:
            try: amt=float(m.group(1).replace(',','.')); break
            except: pass
    if not amt:
        nums=re.findall(r'\d+[.,]\d+|\d+',text)
        candidates=[float(n.replace(',','.')) for n in nums if float(n.replace(',','.'))>0]
        if candidates: amt=max(candidates)
    if etype and amt:
        first=text.split("\n")[0].strip()
        desc=first
        for w in SALE_WORDS+BUY_WORDS+["بـ","ب","ريال","ر.ع","اغراض","أغراض"]:
            desc=desc.replace(w," ")
        desc=re.sub(r'\d+(?:[.,]\d+)?','',desc).strip()
        desc=' '.join(desc.split()) or ("مبيعة" if etype=="s" else "مشتريات")
        return {"type":etype,"desc":desc,"amt":amt,"found":True}
    return {"found":False}

def groq_read_invoice(file_id):
    if not GROQ_KEY or not BOT_TOKEN: return None
    try:
        import base64
        r=requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",params={"file_id":file_id},timeout=10)
        fp=r.json()["result"]["file_path"]
        img=requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}",timeout=15).content
        b64=base64.b64encode(img).decode()
        prompt = 'This is a receipt/invoice. Extract total amount, description, and if it is an electricity bill. Reply ONLY with JSON like: {"amt":3.52,"desc":"shop name","is_electricity":false,"found":true}'
        res=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"meta-llama/llama-4-scout-17b-16e-instruct",
                  "messages":[{"role":"user","content":[
                      {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
                      {"type":"text","text":prompt}
                  ]}],
                  "max_tokens":300,"temperature":0},timeout=25)
        resp = res.json()
        if "error" in resp:
            print("Groq API error:", resp["error"])
            return None
        raw = resp["choices"][0]["message"]["content"]
        import re as _re
        match = _re.search(r'\{.*?\}', raw, _re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw.replace("```json","").replace("```","").strip())
    except Exception as e:
        print("Groq error:", e)
        return None

# ── Web API ───────────────────────────────────────────────
@app.route("/")
def index(): return Response(HTML_PAGE, mimetype="text/html")

@app.route("/debug")
def debug():
    try:
        total = db_one("SELECT COUNT(*) as c FROM entries")
        cnt = int(total["c"]) if total and total.get("c") is not None else 0
    except Exception as e:
        cnt = str(e)
    return jsonify({
        "database": "Turso ✅" if USE_TURSO else "SQLite (local)",
        "total_entries": cnt,
        "turso": USE_TURSO,
        "bot": bool(BOT_TOKEN),
        "groq": bool(GROQ_KEY),
        "groq_key_prefix": GROQ_KEY[:8]+"..." if GROQ_KEY else "NOT SET"
    })

@app.route("/api/entries")
def api_get():
    month=request.args.get("month",cur_month())
    s,b=get_month_data(month)
    return jsonify({"sales":s,"buys":b})

@app.route("/api/entries",methods=["POST"])
def api_add():
    d=request.json
    month=d.get("month",cur_month())
    db_run("INSERT INTO entries (type,desc,amt,date,month,img,paid_by,payment_method,sale_time,category) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (d["type"],d["desc"],float(d["amt"]),
         d.get("date",datetime.now().strftime("%d/%m/%Y")),
         month,d.get("img"),d.get("paid_by"),d.get("payment_method"),d.get("sale_time"),d.get("category")))
    return jsonify({"ok":True})

@app.route("/api/entries/<int:eid>",methods=["DELETE"])
def api_del(eid):
    db_run("DELETE FROM entries WHERE id=?",(eid,))
    return jsonify({"ok":True})

@app.route("/api/shelves")
def api_shelves():
    month=request.args.get("month",cur_month())
    shelves=db_get("SELECT * FROM shelves ORDER BY id")
    result=[]
    for s in shelves:
        prods=db_get("SELECT * FROM shelf_products WHERE shelf_id=? ORDER BY created DESC",(s["id"],))
        row=db_one("SELECT COALESCE(SUM(amt),0) as total,COUNT(*) as cnt FROM entries WHERE type='s' AND shelf_id=? AND month=?",(s["id"],month))
        ms=float(row["total"]) if row else 0
        rent=float(s.get("rent") or 0)
        result.append({**s,"products":prods,"monthly_sales":ms,"sales_count":int(row["cnt"]) if row else 0,"rent":rent,"net":ms-rent})
    return jsonify(result)

@app.route("/api/shelves/<int:sid>/products",methods=["POST"])
def api_add_prod(sid):
    d=request.json
    db_run("INSERT INTO shelf_products (shelf_id,name,price,qty) VALUES (?,?,?,?)",
        (sid,d["name"],float(d["price"]),int(d.get("qty",0))))
    return jsonify({"ok":True})

@app.route("/api/shelf_products/<int:pid>",methods=["DELETE"])
def api_del_prod(pid):
    db_run("DELETE FROM shelf_products WHERE id=?",(pid,)); return jsonify({"ok":True})

@app.route("/api/shelf_products/<int:pid>/sell",methods=["POST"])
def api_sell(pid):
    d=request.json; qty=int(d.get("qty",1)); pay=d.get("payment_method")
    prod=db_one("SELECT * FROM shelf_products WHERE id=?",(pid,))
    if not prod: return jsonify({"ok":False}),404
    new_qty=max(0,prod["qty"]-qty)
    db_run("UPDATE shelf_products SET qty=? WHERE id=?",(new_qty,pid))
    month=cur_month(); date=datetime.now().strftime("%d/%m/%Y")
    shelf=db_one("SELECT name FROM shelves WHERE id=?",(prod["shelf_id"],))
    sname=shelf["name"] if shelf else ""
    db_run("INSERT INTO entries (type,desc,amt,date,month,shelf_id,payment_method) VALUES (?,?,?,?,?,?,?)",
        ("s",f'{prod["name"]} — رف {sname}',prod["price"]*qty,date,month,prod["shelf_id"],pay))
    return jsonify({"ok":True,"new_qty":new_qty,"total":prod["price"]*qty})

@app.route("/api/shelves/<int:sid>/rent",methods=["POST"])
def api_rent(sid):
    db_run("UPDATE shelves SET rent=? WHERE id=?",(float(request.json["rent"]),sid))
    return jsonify({"ok":True})

# ── Telegram Webhook ──────────────────────────────────────
pending={}

@app.route("/webhook",methods=["POST"])
def webhook():
    data=request.json or {}
    
    cb=data.get("callback_query")
    if cb:
        cid=cb["id"]; chat=cb["message"]["chat"]["id"]; cbd=cb["data"]
        month=cur_month(); date=datetime.now().strftime("%d/%m/%Y")
        try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={"callback_query_id":cid},timeout=5)
        except: pass
        try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",json={"chat_id":chat,"message_id":cb["message"]["message_id"],"reply_markup":{"inline_keyboard":[]}},timeout=5)
        except: pass
        
        if cbd.startswith("pay:"):
            pay=cbd.split("pay:",1)[1]
            last=db_one("SELECT id FROM entries WHERE type='s' AND month=? ORDER BY created DESC LIMIT 1",(month,))
            if last: db_run("UPDATE entries SET payment_method=? WHERE id=?",(pay,last["id"]))
            if chat in pending and pending[chat].get("waiting")=="sale_payment": del pending[chat]
            tg(chat,f"✅ طريقة الدفع: {pay}")
            
        elif cbd.startswith("payer:"):
            val=cbd.split("payer:",1)[1]
            if val=="skip": paid_by=None; tg(chat,"⏭ تم التخطي")
            elif val=="other":
                if chat not in pending: pending[chat]={}
                pending[chat]["waiting_name"]=True
                tg(chat,"✏️ اكتب اسم الشخص:"); return "ok"
            else: paid_by=val; tg(chat,f"✅ دفع: {paid_by}")
            
            state=pending.get(chat,{})
            if state.get("waiting") in ("paid_by","paid_by_photo"):
                if state.get("waiting")=="paid_by":
                    db_run("INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",
                        ("b",state.get("desc","مشتريات"),state.get("amt",0),state.get("date",date),state.get("month",month),paid_by))
                    if chat in pending: del pending[chat]
                    tg(chat,f"✅ تم التسجيل!\n📦 {state.get('desc')}\n💰 {fmt_omr(state.get('amt',0))}" + (f"\n👤 {paid_by}" if paid_by else ""))
                else:
                    last=db_one("SELECT id FROM entries WHERE month=? ORDER BY created DESC LIMIT 1",(month,))
                    if last: db_run("UPDATE entries SET paid_by=? WHERE id=?",(paid_by,last["id"]))
                    if chat in pending: del pending[chat]
        return "ok"

    msg=data.get("message") or data.get("edited_message")
    if not msg: return "ok"
    chat=msg["chat"]["id"]; month=cur_month(); date=datetime.now().strftime("%d/%m/%Y")

    if "photo" in msg:
        file_id=msg["photo"][-1]["file_id"]; caption=msg.get("caption","").strip()
        # Pre-detect electricity from caption
        caption_is_elec = any(w in caption for w in ["كهرباء","كهربا","تعبئة","تعبئه","⚡","electric","kwh","prepaid"])
        tg(chat,"⏳ جاري قراءة الفاتورة...")
        result=groq_read_invoice(file_id)
        if result and result.get("found") and result.get("amt"):
            amt=float(result["amt"]); desc=result.get("desc","مشتريات")
            is_elec=result.get("is_electricity",False) or caption_is_elec
            # Auto-detect electricity from description
            if not is_elec:
                is_elec=any(w in (desc+caption).lower() for w in ["كهرب","تعبئ","prepaid","electric","kwh","electricity","power"])
            if is_elec:
                # Use date from receipt if available, else today
                receipt_date = result.get("date","").strip()
                if receipt_date and len(receipt_date) >= 8:
                    entry_date = receipt_date
                    try:
                        entry_month = datetime.strptime(receipt_date, "%d/%m/%Y").strftime("%Y-%m")
                    except:
                        entry_date = date; entry_month = month
                else:
                    entry_date = date; entry_month = month
                # Save as expense (NOT as buy)
                db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                       ("expense","فاتورة الكهرباء",amt,entry_date,entry_month,"مصاريف ثابتة"))
                exp=db_one("SELECT id FROM expenses WHERE name=?",("فاتورة الكهرباء",))
                if exp: db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",(entry_date,entry_month,amt,exp["id"]))
                tg(chat,
                   f"⚡ <b>تم تسجيل فاتورة الكهرباء!</b>\n"
                   f"💰 {fmt_omr(amt)}\n"
                   f"📅 {entry_date}\n"
                   f"✅ أُضيفت في المصاريف الثابتة (ليس المشتريات)")
            else:
                db_run("INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",("b",desc,amt,date,month))
                pending[chat]={"waiting":"paid_by_photo","amt":amt}
                tg_buttons(chat,f"✅ تم قراءة الفاتورة!\n📦 {desc}\n💰 {fmt_omr(amt)}\n\n👤 من دفع؟",
                    [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                     [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
        else:
            if caption_is_elec:
                pending[chat]={"waiting":"elec_amt"}
                tg(chat,"⚡ ما قدرت أقرأ الفاتورة بوضوح\nكم مبلغ فاتورة الكهرباء؟\nأرسل الرقم فقط: <code>45.500</code>")
            else:
                pending[chat]={"waiting":"buy_amt","desc":caption or "مشتريات"}
                tg(chat,"🧾 ما قدرت أقرأ الفاتورة بوضوح\nكم المبلغ الإجمالي؟\nأرسل الرقم فقط: <code>3.520</code>")
        return "ok"

    text=msg.get("text","").strip()
    if not text: return "ok"

    # Handle electricity manual amount
    if pending.get(chat,{}).get("waiting") == "elec_amt":
        try:
            amt = float(text.replace(",","."))
            date_now = datetime.now().strftime("%d/%m/%Y")
            db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                   ("expense","فاتورة الكهرباء",amt,date_now,month,"مصاريف ثابتة"))
            exp=db_one("SELECT id FROM expenses WHERE name=?",("فاتورة الكهرباء",))
            if exp: db_run("UPDATE expenses SET last_paid=?,month=?,amount=? WHERE id=?",(date_now,month,amt,exp["id"]))
            del pending[chat]
            tg(chat,f"⚡ <b>تم تسجيل فاتورة الكهرباء!</b>\n💰 {fmt_omr(amt)}\n📅 {date_now}")
        except:
            tg(chat,"⚠️ أرسل رقم صحيح مثل: <code>45.500</code>")
        return "ok"

    if pending.get(chat,{}).get("waiting_name"):
        paid_by=text.strip(); state=pending[chat]; del state["waiting_name"]
        if state.get("waiting")=="paid_by":
            db_run("INSERT INTO entries (type,desc,amt,date,month,paid_by) VALUES (?,?,?,?,?,?)",
                ("b",state.get("desc"),state.get("amt"),state.get("date",date),state.get("month",month),paid_by))
            del pending[chat]
            tg(chat,f"✅ تم!\n📦 {state.get('desc')}\n💰 {fmt_omr(state.get('amt',0))}\n👤 {paid_by}")
        else:
            last=db_one("SELECT id FROM entries WHERE month=? ORDER BY created DESC LIMIT 1",(month,))
            if last: db_run("UPDATE entries SET paid_by=? WHERE id=?",(paid_by,last["id"]))
            if chat in pending: del pending[chat]
            tg(chat,f"✅ دفع: {paid_by}")
        return "ok"

    state=pending.get(chat,{})
    if state.get("waiting")=="buy_amt":
        try:
            amt=float(text.replace(",","."))
            desc=state.get("desc","مشتريات")
            db_run("INSERT INTO entries (type,desc,amt,date,month) VALUES (?,?,?,?,?)",("b",desc,amt,date,month))
            pending[chat]={"waiting":"paid_by_photo","amt":amt}
            tg_buttons(chat,f"✅ تم التسجيل!\n📦 {desc}\n💰 {fmt_omr(amt)}\n\n👤 من دفع؟",
                [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                 [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
        except: tg(chat,"⚠️ أرسل رقم: <code>3.520</code>")
        return "ok"
    
    if state.get("waiting")=="sale_payment":
        pay=text.strip()
        if pay in ["1","كاش","نقد"]: pay="كاش 💵"
        elif pay in ["2","فيزا","بطاقة"]: pay="فيزا 💳"
        elif pay in ["3","تحويل"]: pay="تحويل 🏦"
        last=db_one("SELECT id FROM entries WHERE type='s' AND month=? ORDER BY created DESC LIMIT 1",(month,))
        if last: db_run("UPDATE entries SET payment_method=? WHERE id=?",(pay,last["id"]))
        del pending[chat]
        tg(chat,f"✅ طريقة الدفع: {pay}"); return "ok"

    if text in ["/start","/help"]:
        tg(chat,
           "🌹 <b>فيروز فلورز</b>\n\n"
           "🌸 <b>مبيعة:</b>\n"
           "<code>بعت باقة بـ 5.500</code>\n"
           "<code>بعت طباعة 3d بـ 8.000 كاش</code>\n"
           "<code>بعت تاج بـ 3.000 فيزا</code>\n\n"
           "📦 <b>مشتريات:</b>\n"
           "<code>اشتريت زهور بـ 12.000</code>\n\n"
           "🗄️ <b>بيع من الرف:</b>\n"
           "<code>/رف ريحان</code> — عرض منتجات رف ريحان\n"
           "<code>/رف فتحية</code>\n"
           "<code>/رف فطوم</code>\n"
           "<code>/رف اكسسوارات</code>\n\n"
           "🧾 <b>فاتورة:</b> أرسل صورة\n\n"
           "📊 /report — تقرير الشهر\n"
           "👤 /من_دفع — تفصيل المشتريات\n"
           "📈 /فئات — مبيعات حسب الفئة")
        return "ok"

    if text=="/report":
        ts,tb,tp,sc,bc=month_summary(month)
        e="✅" if tp>=0 else "⚠️"
        _,buys=get_month_data(month)
        pd={}
        for en in buys:
            p=en.get("paid_by") or "غير محدد"
            pd[p]=pd.get(p,0)+en["amt"]
        pl="\n".join(f"  👤 {k}: {fmt_omr(v)}" for k,v in pd.items()) or "  غير محدد"
        # Expenses summary
        exps = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month,))
        exp_total = sum(e2["amt"] for e2 in exps)
        exp_lines = "\n".join(f"  💸 {e2['desc']}: {fmt_omr(e2['amt'])}" for e2 in exps) or "  لا يوجد"
        net_after_exp = tp - exp_total
        emoji2 = "✅" if net_after_exp >= 0 else "⚠️"
        tg(chat,
           f"📊 <b>تقرير {month}</b>\n\n"
           f"🌸 المبيعات: {fmt_omr(ts)} ({sc})\n"
           f"📦 المشتريات: {fmt_omr(tb)} ({bc})\n"
           f"💸 المصاريف: {fmt_omr(exp_total)}\n"
           f"━━━━━━\n"
           f"{e} الربح قبل المصاريف: {fmt_omr(tp)}\n"
           f"{emoji2} الربح الصافي: {fmt_omr(net_after_exp)}\n\n"
           f"💳 من دفع:\n{pl}\n\n"
           f"💼 المصاريف المدفوعة:\n{exp_lines}")
        return "ok"

    if text in ["/مصاريف","/expenses"]:
        expenses = db_get("SELECT * FROM expenses ORDER BY id")
        lines = []
        for e in expenses:
            last = f" — آخر دفع: {e['last_paid']}" if e.get("last_paid") else " — لم يُدفع بعد"
            lines.append(f"{'⚡' if 'كهرب' in e['name'] else '🏪' if 'إيجار' in e['name'] else '👷'} <b>{e['name']}</b>: {fmt_omr(e['amount'])}{last}")
        tg(chat, f"💼 <b>المصاريف الثابتة</b>\n\n" + "\n".join(lines) +
           "\n\nللتسجيل: <code>دفعت راتب</code> أو <code>دفعت إيجار</code> أو <code>دفعت كهرباء 45.000</code>")
        return "ok"

    if text == "/فئات":
        s,_=get_month_data(month)
        cats={}
        for e in s:
            c=e.get("category") or "أخرى"
            if c not in cats: cats[c]={"t":0,"c":0}
            cats[c]["t"]+=e["amt"]; cats[c]["c"]+=1
        cats_sorted=sorted(cats.items(),key=lambda x:-x[1]["t"])
        lines="\n".join(f"🏷️ <b>{k}</b>: {fmt_omr(v['t'])} ({v['c']} مبيعة)" for k,v in cats_sorted) if cats_sorted else "لا توجد مبيعات"
        tg(chat,f"📈 <b>مبيعات حسب الفئة — {month}</b>\n\n{lines}")
        return "ok"

    # Shelf commands: /رف ريحان etc
    if text.startswith("/رف"):
        shelf_name=text.replace("/رف","").strip()
        if not shelf_name:
            shelves=db_get("SELECT * FROM shelves ORDER BY id")
            lines="\n".join(f"🗄️ /رف {s['name']} — إيجار {fmt_omr(s.get('rent',0))}" for s in shelves)
            tg(chat,f"🗄️ <b>الرفوف المتاحة:</b>\n\n{lines}"); return "ok"
        shelf=db_one("SELECT * FROM shelves WHERE name=?",(shelf_name,))
        if not shelf:
            tg(chat,f"❌ ما وجدت رف اسمه '{shelf_name}'\n\nالرفوف: ريحان، فتحية، فطوم، اكسسوارات")
            return "ok"
        prods=db_get("SELECT * FROM shelf_products WHERE shelf_id=? AND qty>0 ORDER BY name",(shelf["id"],))
        if not prods:
            tg(chat,f"🗄️ رف <b>{shelf_name}</b> — لا توجد منتجات متاحة")
            return "ok"
        lines="\n".join(f"{'▫️'} {p['name']} — {fmt_omr(p['price'])} × {p['qty']} قطعة" for p in prods)
        tg(chat,
           f"🗄️ <b>رف {shelf_name}</b>\n\n{lines}\n\n"
           f"للبيع أرسل مثلاً:\n<code>بعت {prods[0]['name']} من رف {shelf_name} بـ {prods[0]['price']}</code>")
        return "ok"

    if text in ["/من_دفع","/mandafa3"]:
        _,buys=get_month_data(month)
        pd={}
        for en in buys:
            p=en.get("paid_by") or "غير محدد"
            if p not in pd: pd[p]={"t":0,"c":0}
            pd[p]["t"]+=en["amt"]; pd[p]["c"]+=1
        lines="\n".join(f"👤 <b>{k}</b>: {fmt_omr(v['t'])} ({v['c']} عمليات)" for k,v in pd.items()) if pd else "لا يوجد"
        tg(chat,f"💳 <b>من دفع — {month}</b>\n\n{lines}"); return "ok"

    # Expense detection
    exp_keywords = {
        "راتب": ("راتب العامل", 220),
        "إيجار المحل": ("إيجار المحل", 100),
        "إيجار": ("إيجار المحل", 100),
        "كهرباء": ("فاتورة الكهرباء", 0),
        "كهربا": ("فاتورة الكهرباء", 0),
        "تعبئة": ("فاتورة الكهرباء", 0),
    }
    for kw, (exp_name, default_amt) in exp_keywords.items():
        if kw in text and any(w in text for w in ["دفعت","دفع","سددت","سديت"]):
            import re as _re
            nums = _re.findall(r'\d+[.,]\d+|\d+', text)
            amt = float(nums[0].replace(',','.')) if nums else default_amt
            if amt > 0:
                exp = db_one("SELECT * FROM expenses WHERE name=?", (exp_name,))
                date_now = datetime.now().strftime("%d/%m/%Y")
                db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
                       ("expense", exp_name, amt, date_now, month, "مصاريف ثابتة"))
                if exp:
                    db_run("UPDATE expenses SET last_paid=?, month=?, amount=? WHERE id=?",
                           (date_now, month, amt, exp["id"]))
                tg(chat, f"✅ <b>تم تسجيل {exp_name}</b>\n💰 {fmt_omr(amt)}\n📅 {date_now}")
                return "ok"

    parsed=parse_text(text)
    if parsed["found"]:
        etype=parsed["type"]; desc=parsed["desc"]; amt=parsed["amt"]
        # Detect if sale is from a shelf
        shelf_id_detected=None
        for sname in ["ريحان","فتحية","فطوم","اكسسوارات"]:
            if sname in text:
                shelf=db_one("SELECT id FROM shelves WHERE name=?",(sname,))
                if shelf:
                    shelf_id_detected=shelf["id"]
                    # Auto-decrease qty if product name matches
                    prod=db_one("SELECT * FROM shelf_products WHERE shelf_id=? AND name LIKE ? AND qty>0",
                               (shelf["id"],f"%{desc}%"))
                    if prod and etype=="s":
                        db_run("UPDATE shelf_products SET qty=qty-1 WHERE id=? AND qty>0",(prod["id"],))
                    break
        if etype=="b":
            pending[chat]={"waiting":"paid_by","desc":desc,"amt":amt,"date":date,"month":month}
            tg_buttons(chat,f"📦 <b>مشتريات {fmt_omr(amt)}</b>\n\n👤 من دفع؟",
                [[{"label":"👤 حسين","data":"payer:حسين"},{"label":"👤 شوق","data":"payer:شوق"}],
                 [{"label":"➕ شخص آخر","data":"payer:other"},{"label":"⏭ تخطي","data":"payer:skip"}]])
        else:
            cat=detect_category(text) or detect_category(desc)
            pay=None
            if any(w in text for w in ["كاش","نقد"]): pay="كاش 💵"
            elif any(w in text for w in ["فيزا","بطاقة"]): pay="فيزا 💳"
            elif "تحويل" in text: pay="تحويل 🏦"
            db_run("INSERT INTO entries (type,desc,amt,date,month,payment_method,category,shelf_id) VALUES (?,?,?,?,?,?,?,?)",
                (etype,desc,amt,date,month,pay,cat,shelf_id_detected))
            cat_line=f"\n🏷️ {cat}" if cat else ""
            if pay:
                tg(chat,f"✅ مبيعة {fmt_omr(amt)} — {pay}{cat_line}")
            else:
                pending[chat]={"waiting":"sale_payment"}
                tg_buttons(chat,f"🌸 <b>مبيعة {fmt_omr(amt)}</b>{cat_line}\n\n💳 طريقة الدفع؟",
                    [[{"label":"💵 كاش","data":"pay:كاش 💵"},{"label":"💳 فيزا","data":"pay:فيزا 💳"},{"label":"🏦 تحويل","data":"pay:تحويل 🏦"}]])
    else:
        tg(chat,"لم أفهم 🤔\n\nجرّب:\n<code>بعت باقة بـ 4.500</code>\n<code>اشتريت ورد بـ 8.000</code>\n\n/help للمساعدة")
    return "ok"

@app.route("/turso_debug")
def turso_debug():
    """Show raw Turso response for debugging."""
    try:
        res = turso_exec("SELECT * FROM shelves")
        return jsonify({"raw": res})
    except Exception as e:
        return jsonify({"error": str(e)})

# ── Expenses API ─────────────────────────────────────────
@app.route("/api/expenses")
def api_get_expenses():
    month = request.args.get("month", cur_month())
    expenses = db_get("SELECT * FROM expenses ORDER BY id")
    # Get paid expenses for this month
    paid = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY created DESC", (month,))
    return jsonify({"expenses": expenses, "paid": paid})

@app.route("/api/expenses/<int:eid>/pay", methods=["POST"])
def api_pay_expense(eid):
    d = request.json
    month_val = d.get("month", cur_month())
    custom_date = d.get("date", "").strip()
    date_val = custom_date if custom_date else datetime.now().strftime("%d/%m/%Y")
    exp = db_one("SELECT * FROM expenses WHERE id=?", (eid,))
    if not exp: return jsonify({"ok": False}), 404
    amt = float(d.get("amount", exp["amount"]))
    db_run("INSERT INTO entries (type,desc,amt,date,month,category) VALUES (?,?,?,?,?,?)",
           ("expense", exp["name"], amt, date_val, month_val, "مصاريف ثابتة"))
    db_run("UPDATE expenses SET last_paid=?, month=?, amount=? WHERE id=?",
           (date_val, month_val, amt, eid))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>", methods=["POST"])
def api_update_expense(eid):
    d = request.json
    db_run("UPDATE expenses SET amount=? WHERE id=?", (float(d["amount"]), eid))
    return jsonify({"ok": True})

@app.route("/api/expenses", methods=["POST"])
def api_add_expense():
    d = request.json
    db_run("INSERT INTO expenses (name,amount,type) VALUES (?,?,?)",
           (d["name"], float(d.get("amount",0)), d.get("type","monthly")))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>", methods=["DELETE"])
def api_del_expense(eid):
    db_run("DELETE FROM expenses WHERE id=?", (eid,))
    return jsonify({"ok": True})

@app.route("/api/expense_entries/<int:eid>", methods=["DELETE"])
def api_del_expense_entry(eid):
    """Delete a specific expense entry."""
    db_run("DELETE FROM entries WHERE id=? AND type='expense'", (eid,))
    return jsonify({"ok": True})

@app.route("/api/expenses/<int:eid>/reset", methods=["POST"])
def api_reset_expense(eid):
    """Reset expense paid status."""
    d = request.json or {}
    month_val = d.get("month", cur_month())
    exp = db_one("SELECT * FROM expenses WHERE id=?", (eid,))
    if exp and exp.get("month") == month_val:
        db_run("UPDATE expenses SET last_paid=NULL, month=NULL WHERE id=?", (eid,))
    return jsonify({"ok": True})

@app.route("/api/report/pdf")
def api_report_pdf():
    """Generate PDF report."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import io

        month  = request.args.get("month", cur_month())
        rtype  = request.args.get("type", "all")  # all, sales, buys, expenses

        sales, buys = get_month_data(month)
        buys_only  = [b for b in buys if b.get("type") == "b"]
        exps       = db_get("SELECT * FROM entries WHERE type='expense' AND month=? ORDER BY date DESC", (month,))
        exp_defs   = db_get("SELECT * FROM expenses ORDER BY id")

        ts = sum(e["amt"] for e in sales)
        tb = sum(e["amt"] for e in buys_only)
        te = sum(e["amt"] for e in exps)
        tp = ts - tb
        tn = tp - te

        def fmt_r(n): return f"{n:,.3f}"

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
            rightMargin=1.5*cm, leftMargin=1.5*cm,
            topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        story  = []

        # Header style
        title_style = ParagraphStyle('title', fontName='Helvetica-Bold',
            fontSize=18, spaceAfter=6, alignment=1)
        sub_style = ParagraphStyle('sub', fontName='Helvetica',
            fontSize=10, spaceAfter=4, alignment=1, textColor=colors.HexColor('#888888'))
        h2_style = ParagraphStyle('h2', fontName='Helvetica-Bold',
            fontSize=13, spaceBefore=14, spaceAfter=6,
            textColor=colors.HexColor('#c4566a'))
        normal = ParagraphStyle('normal', fontName='Helvetica',
            fontSize=9, spaceAfter=3)

        # Title
        story.append(Paragraph("Fairuz Flowers - Monthly Report", title_style))
        story.append(Paragraph(f"Period: {month}", sub_style))
        story.append(HRFlowable(width="100%", thickness=1,
            color=colors.HexColor('#e8798a'), spaceAfter=12))

        # Summary box
        if rtype in ("all",):
            summary_data = [
                ["Category", "Amount (OMR)", "Count"],
                ["Total Sales", fmt_r(ts), str(len(sales))],
                ["Total Purchases", fmt_r(tb), str(len(buys_only))],
                ["Fixed Expenses", fmt_r(te), str(len(exps))],
                ["Gross Profit", fmt_r(tp), ""],
                ["Net Profit", fmt_r(tn), ""],
            ]
            t = Table(summary_data, colWidths=[8*cm, 5*cm, 3*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8798a')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('ALIGN', (1,0), (-1,-1), 'CENTER'),
                ('BACKGROUND', (0,-2), (-1,-2), colors.HexColor('#fff3e0')),
                ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e8f5e9')),
                ('FONTNAME', (0,-2), (-1,-1), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
                ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, colors.HexColor('#fafafa')]),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

        # Sales section
        if rtype in ("all", "sales") and sales:
            story.append(Paragraph("Sales", h2_style))
            sale_data = [["#", "Description", "Category", "Payment", "Date", "Amount"]]
            for i, e in enumerate(sales, 1):
                sale_data.append([
                    str(i), e.get("desc","")[:30],
                    e.get("category","")[:15] or "-",
                    e.get("payment_method","")[:10] or "-",
                    e.get("date",""),
                    fmt_r(e["amt"])
                ])
            sale_data.append(["", "TOTAL", "", "", "", fmt_r(ts)])
            t = Table(sale_data, colWidths=[1*cm, 7*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7aab8a')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e8f5e9')),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dddddd')),
                ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#f9fff9')]),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))

        # Purchases section
        if rtype in ("all", "buys") and buys_only:
            story.append(Paragraph("Purchases", h2_style))
            buy_data = [["#", "Description", "Paid By", "Date", "Amount"]]
            for i, e in enumerate(buys_only, 1):
                buy_data.append([
                    str(i), e.get("desc","")[:35],
                    e.get("paid_by","")[:12] or "-",
                    e.get("date",""),
                    fmt_r(e["amt"])
                ])
            buy_data.append(["", "TOTAL", "", "", fmt_r(tb)])
            t = Table(buy_data, colWidths=[1*cm, 9*cm, 3*cm, 2.5*cm, 3*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8798a')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#fce4ec')),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dddddd')),
                ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#fff9f9')]),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))

        # Expenses section
        if rtype in ("all", "expenses"):
            story.append(Paragraph("Fixed Expenses", h2_style))
            # Expense definitions
            exp_def_data = [["Expense", "Monthly Amount", "Last Paid", "Status"]]
            for e in exp_defs:
                last = e.get("last_paid") or "Not paid"
                paid_this = e.get("month") == month
                status = "PAID" if paid_this else "UNPAID"
                exp_def_data.append([e["name"], fmt_r(float(e["amount"])), last, status])
            if exps:
                exp_def_data.append(["", "", "TOTAL PAID", fmt_r(te)])

            t = Table(exp_def_data, colWidths=[6*cm, 4*cm, 4*cm, 3*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d4a557')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#fff8e1')),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dddddd')),
                ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#fffdf5')]),
            ]))
            story.append(t)

            # Paid expense entries
            if exps:
                story.append(Spacer(1, 6))
                story.append(Paragraph("Paid Expense Entries", ParagraphStyle('h3',
                    fontName='Helvetica-Bold', fontSize=10, spaceBefore=8, spaceAfter=4)))
                ep_data = [["#", "Description", "Date", "Amount"]]
                for i, e in enumerate(exps, 1):
                    ep_data.append([str(i), e.get("desc",""), e.get("date",""), fmt_r(e["amt"])])
                t = Table(ep_data, colWidths=[1*cm, 9*cm, 4*cm, 3*cm])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f5f5f5')),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 8),
                    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#eeeeee')),
                ]))
                story.append(t)

        doc.build(story)
        buf.seek(0)
        fname = f"fairuz_report_{month}_{rtype}.pdf"
        return Response(buf.read(), mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={fname}"})

    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route("/fix_expenses")
def fix_expenses():
    """Remove duplicate expenses keeping only latest per name."""
    try:
        all_exp = db_get("SELECT * FROM expenses ORDER BY id")
        seen = {}
        to_delete = []
        for e in all_exp:
            if e["name"] in seen:
                to_delete.append(e["id"])
            else:
                seen[e["name"]] = e["id"]
        for eid in to_delete:
            db_run("DELETE FROM expenses WHERE id=?", (eid,))
        remaining = db_get("SELECT * FROM expenses ORDER BY id")
        return jsonify({"ok": True, "deleted": len(to_delete), "remaining": remaining})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/init_shelves")
def init_shelves():
    shelves = [
        ('ريحان','#f07090',10),
        ('فتحية','#4ecdc4',8),
        ('فطوم','#b794f4',8),
        ('اكسسوارات','#f5c842',18),
    ]
    results = []
    for name, color, rent in shelves:
        existing = db_one("SELECT id FROM shelves WHERE name=?", (name,))
        if existing:
            db_run("UPDATE shelves SET color=?, rent=? WHERE name=?", (color, rent, name))
            results.append(f"updated: {name}")
        else:
            db_run("INSERT INTO shelves (name,color,rent) VALUES (?,?,?)", (name, color, rent))
            results.append(f"inserted: {name}")
    all_shelves = db_get("SELECT * FROM shelves")
    return jsonify({"ok": True, "results": results, "shelves": all_shelves})

@app.route("/api/backup")
def api_backup():
    """Export all data as JSON."""
    try:
        entries = db_get("SELECT * FROM entries ORDER BY created")
        shelves = db_get("SELECT * FROM shelves ORDER BY id")
        products = db_get("SELECT * FROM shelf_products ORDER BY id")
        data = {
            "version": 1,
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "entries": entries,
            "shelves": shelves,
            "shelf_products": products
        }
        import json as _json
        response = Response(
            _json.dumps(data, ensure_ascii=False, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": f"attachment; filename=fairuz_backup_{datetime.now().strftime('%Y%m%d')}.json"}
        )
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/restore", methods=["POST"])
def api_restore():
    """Restore data from JSON backup."""
    try:
        data = request.json
        if not data or data.get("version") != 1:
            return jsonify({"error": "ملف غير صالح"}), 400

        restored = {"entries": 0, "shelves": 0, "products": 0}

        # Restore shelves
        for s in data.get("shelves", []):
            existing = db_one("SELECT id FROM shelves WHERE name=?", (s["name"],))
            if existing:
                db_run("UPDATE shelves SET color=?, rent=? WHERE name=?",
                       (s.get("color","#e8547a"), s.get("rent",0), s["name"]))
            else:
                db_run("INSERT INTO shelves (name,color,rent) VALUES (?,?,?)",
                       (s["name"], s.get("color","#e8547a"), s.get("rent",0)))
            restored["shelves"] += 1

        # Restore entries
        for e in data.get("entries", []):
            existing = db_one("SELECT id FROM entries WHERE id=?", (e["id"],))
            if not existing:
                db_run("""INSERT INTO entries (type,desc,amt,date,month,img,paid_by,payment_method,sale_time,shelf_id)
                          VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (e["type"], e["desc"], e["amt"], e["date"], e["month"],
                     e.get("img"), e.get("paid_by"), e.get("payment_method"),
                     e.get("sale_time"), e.get("shelf_id")))
                restored["entries"] += 1

        # Restore shelf products
        for p in data.get("shelf_products", []):
            existing = db_one("SELECT id FROM shelf_products WHERE id=?", (p["id"],))
            if not existing:
                db_run("INSERT INTO shelf_products (shelf_id,name,price,qty) VALUES (?,?,?,?)",
                       (p["shelf_id"], p["name"], p["price"], p.get("qty",0)))
                restored["products"] += 1

        return jsonify({"ok": True, "restored": restored})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set_webhook")
def set_webhook():
    host=request.host_url.rstrip("/")
    r=requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",params={"url":f"{host}/webhook"},timeout=10)
    return jsonify(r.json())

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=False)
