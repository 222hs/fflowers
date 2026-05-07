from config import *

HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl" data-theme="rose">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>فيروز فلورز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
/* ══════════════════════════════════════════
   THEMES
══════════════════════════════════════════ */
:root, [data-theme="rose"] {
  --bg:#fdf8f2;--bg2:#f5ede0;--card:rgba(255,255,255,0.75);
  --border:rgba(232,121,138,0.2);--border2:rgba(255,255,255,0.9);
  --text:#3d2c24;--text2:#7a6458;--text3:#b09888;
  --accent:#e8798a;--accent2:#c4566a;--accent-glow:rgba(232,121,138,0.25);
  --green:#7aab8a;--green2:#5a8a6a;--gold:#d4a557;
  --glass:rgba(255,255,255,0.6);--shadow:rgba(107,76,59,0.12);
  --nav-bg:rgba(253,248,242,0.92);
  --orb1:#fce4ec;--orb2:#e8f5e9;--orb3:#fff8e1;
}
[data-theme="bloom"] {
  --bg1:#fff5f7;--bg2:#ffeef2;--nav-bg:rgba(255,240,245,0.92);
  --card:#fff8fa;--border:rgba(232,150,170,0.25);
  --text1:#5a1a2a;--text2:#7a3040;--text3:#b06070;
  --shadow:rgba(200,80,110,0.15);--gold:#e8789a;--green2:#c87898;
  --accent:#e8789a;--accent2:#c4566a;--accent-glow:rgba(232,120,154,0.3);
}

/* خلفية الورود المتحركة */
.rose-bg{display:none;position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;}
[data-theme="bloom"] .rose-bg{display:block;}
.rose-bg .petal{position:absolute;font-size:22px;opacity:0;animation:fall linear infinite;}
@keyframes fall{
  0%  {opacity:0;transform:translateY(-60px) rotate(0deg);}
  10% {opacity:0.7;}
  90% {opacity:0.5;}
  100%{opacity:0;transform:translateY(110vh) rotate(360deg);}
}
/* عشان الصفحة تكون فوق الخلفية */
[data-theme="bloom"] .app-wrap,
[data-theme="bloom"] .nav-bar,
[data-theme="bloom"] .header-top{position:relative;z-index:1;}

[data-theme="ocean"] {
  --bg:#0d1f2d;--bg2:#112436;--card:rgba(255,255,255,0.06);
  --border:rgba(78,174,205,0.25);--border2:rgba(255,255,255,0.1);
  --text:#e0f0ff;--text2:#8ab4cc;--text3:#4a7a96;
  --accent:#4eaccd;--accent2:#2d8aad;--accent-glow:rgba(78,172,205,0.3);
  --green:#4ecdc4;--green2:#2aada4;--gold:#f5c842;
  --glass:rgba(255,255,255,0.05);--shadow:rgba(0,0,0,0.4);
  --nav-bg:rgba(13,31,45,0.95);
  --orb1:rgba(78,172,205,0.15);--orb2:rgba(78,205,196,0.1);--orb3:rgba(245,200,66,0.08);
}
[data-theme="forest"] {
  --bg:#f0f4f0;--bg2:#e4ede4;--card:rgba(255,255,255,0.72);
  --border:rgba(90,138,106,0.25);--border2:rgba(255,255,255,0.9);
  --text:#1e3224;--text2:#4a6a54;--text3:#8aaa94;
  --accent:#5a8a6a;--accent2:#3d6b4d;--accent-glow:rgba(90,138,106,0.25);
  --green:#5a8a6a;--green2:#3d6b4d;--gold:#c4962a;
  --glass:rgba(255,255,255,0.6);--shadow:rgba(30,50,36,0.12);
  --nav-bg:rgba(240,244,240,0.95);
  --orb1:#d4edda;--orb2:#c8e6c9;--orb3:#fff8e1;
}
[data-theme="gold"] {
  --bg:#1a1208;--bg2:#221808;--card:rgba(255,255,255,0.05);
  --border:rgba(212,165,67,0.3);--border2:rgba(212,165,67,0.15);
  --text:#f5e6c0;--text2:#c4a86a;--text3:#7a6030;
  --accent:#d4a843;--accent2:#b8891f;--accent-glow:rgba(212,168,67,0.35);
  --green:#8aaa5a;--green2:#6a8a3a;--gold:#d4a843;
  --glass:rgba(212,168,67,0.06);--shadow:rgba(0,0,0,0.5);
  --nav-bg:rgba(26,18,8,0.97);
  --orb1:rgba(212,168,67,0.12);--orb2:rgba(138,170,90,0.08);--orb3:rgba(212,100,67,0.06);
}
[data-theme="lavender"] {
  --bg:#f5f0ff;--bg2:#ede4ff;--card:rgba(255,255,255,0.72);
  --border:rgba(150,100,220,0.2);--border2:rgba(255,255,255,0.9);
  --text:#2d1a4a;--text2:#6a4a96;--text3:#a888cc;
  --accent:#9664dc;--accent2:#7a44c0;--accent-glow:rgba(150,100,220,0.25);
  --green:#64aad4;--green2:#4488b8;--gold:#d4a843;
  --glass:rgba(255,255,255,0.65);--shadow:rgba(45,26,74,0.12);
  --nav-bg:rgba(245,240,255,0.95);
  --orb1:#f3e5ff;--orb2:#e5f0ff;--orb3:#fff5e5;
}

/* ══════════════════════════════════════════
   BASE
══════════════════════════════════════════ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;}
body{font-family:'Tajawal',sans-serif;background:var(--bg);color:var(--text);
  min-height:100vh;overflow-x:hidden;transition:background .4s,color .4s;}

.bg-scene{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;}
.orb{position:absolute;border-radius:50%;filter:blur(70px);opacity:0.7;animation:drift 18s ease-in-out infinite alternate;}
.orb1{width:400px;height:400px;background:var(--orb1);top:-10%;right:-5%;animation-delay:0s;}
.orb2{width:350px;height:350px;background:var(--orb2);bottom:0;left:-8%;animation-delay:-8s;}
.orb3{width:250px;height:250px;background:var(--orb3);top:45%;left:35%;animation-delay:-15s;}
@keyframes drift{to{transform:translate(25px,35px) scale(1.06);}}

#app{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;}

/* ══════════════════════════════════════════
   HEADER — Mobile First
══════════════════════════════════════════ */
header{
  background:var(--nav-bg);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;
  transition:background .4s;
}
.header-top{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 14px;height:56px;
}
.brand{display:flex;align-items:center;gap:9px;}
.emblem{
  width:36px;height:36px;background:linear-gradient(135deg,var(--accent),var(--accent2));
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:17px;
  box-shadow:0 3px 12px var(--accent-glow);animation:glow 3s ease-in-out infinite;flex-shrink:0;
}
@keyframes glow{0%,100%{box-shadow:0 3px 12px var(--accent-glow);}50%{box-shadow:0 3px 24px var(--accent-glow);}}
.bname{font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:var(--accent2);}
.bsub{font-size:9px;color:var(--text3);display:none;}
.header-actions{display:flex;align-items:center;gap:7px;}

/* Theme picker */
.theme-btn{
  width:32px;height:32px;border-radius:50%;border:2px solid var(--border);
  cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;
  background:var(--glass);transition:.2s;flex-shrink:0;
}
.theme-btn:hover{transform:scale(1.1);}
.theme-panel{
  display:none;position:absolute;top:58px;left:50%;transform:translateX(-50%);
  background:var(--nav-bg);border:1px solid var(--border);border-radius:16px;
  padding:14px;box-shadow:0 8px 32px var(--shadow);z-index:200;
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  min-width:260px;
}
.theme-panel.open{display:block;animation:fadeIn .2s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateX(-50%) translateY(-8px);}to{opacity:1;transform:translateX(-50%) translateY(0);}}
.theme-panel h4{font-size:10px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;text-align:center;}
.themes-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.th-opt{
  display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;
  padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;
}
.th-opt:hover,.th-opt.active{background:rgba(255,255,255,0.1);border-color:var(--accent);}
.th-circle{width:32px;height:32px;border-radius:50%;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,0.2);}
.th-name{font-size:9px;color:var(--text3);font-weight:600;white-space:nowrap;}

/* Reports UI */
.rpt-type-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;}
.rpt-type-btn{padding:12px;border:2px solid var(--border);border-radius:12px;background:var(--card);color:var(--text2);font-family:'Tajawal',sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:.2s;}
.rpt-type-btn.active{border-color:var(--accent);background:rgba(var(--accent-rgb,200,100,110),.1);color:var(--accent);}
.rpt-picker{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px;margin-bottom:14px;}
.rpt-day-label{text-align:center;font-size:12px;color:var(--text3);margin-top:8px;}
input[type="date"]{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg2);color:var(--text1);font-family:'Tajawal',sans-serif;font-size:13px;}

/* Daily KPI */
.day-section{margin-bottom:16px;}
.day-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
.day-title{font-size:13px;font-weight:800;color:var(--text2);}
.day-date{font-size:11px;color:var(--text3);}
.day-chart-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:14px;margin-bottom:12px;}
.day-chart-card h3{font-size:12px;color:var(--text3);margin:0 0 10px;font-weight:600;}

/* Refresh spin */
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

/* Skeleton loading */
.skl{height:14px;background:linear-gradient(90deg,var(--border) 25%,var(--bg2) 50%,var(--border) 75%);background-size:200% 100%;animation:skl-shine 1.2s infinite;border-radius:6px;margin:4px 0;}
.skl-sm{width:60%;height:10px;}
.skl-row{display:flex;flex-direction:column;padding:10px;border-bottom:1px solid var(--border);}
@keyframes skl-shine{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* Mobile nav tabs */
.mobile-tabs{
  display:flex;border-top:1px solid var(--border);overflow-x:auto;
  scrollbar-width:none;padding:0 6px;
}
.mobile-tabs::-webkit-scrollbar{display:none;}
.mtab{
  flex:0 0 auto;padding:9px 14px;border:none;background:transparent;
  font-family:'Tajawal',sans-serif;font-size:12px;font-weight:600;color:var(--text3);
  cursor:pointer;transition:.2s;border-bottom:2px solid transparent;white-space:nowrap;
}
.mtab.on{color:var(--accent);border-bottom-color:var(--accent);}

/* Month pill — compact */
.mpill{
  display:flex;align-items:center;gap:5px;
  background:var(--glass);border:1px solid var(--border);
  padding:5px 10px;border-radius:40px;
}
.mpill select{background:transparent;border:none;color:var(--text);
  font-family:'Tajawal',sans-serif;font-size:11px;font-weight:600;cursor:pointer;outline:none;max-width:90px;}
.mpill select option{background:var(--bg);}

/* Logout */
.logout-btn{
  width:32px;height:32px;border-radius:50%;border:1px solid var(--border);
  background:var(--glass);cursor:pointer;font-size:14px;
  display:flex;align-items:center;justify-content:center;text-decoration:none;
  color:var(--text3);transition:.2s;flex-shrink:0;
}
.logout-btn:hover{border-color:var(--accent);color:var(--accent);}

/* Flower pill */
#flowerPill{
  display:flex;align-items:center;gap:4px;
  background:rgba(212,168,67,0.1);border:1px solid rgba(212,168,67,0.3);
  padding:5px 9px;border-radius:40px;cursor:pointer;flex-shrink:0;
}
#flowerPill span:first-child{font-size:14px;}
#flowerCount{font-size:11px;font-weight:700;color:var(--gold);}
.exp-badge{font-size:8px;color:var(--text3);background:rgba(212,168,67,0.15);
  padding:1px 4px;border-radius:6px;}

/* ══════════════════════════════════════════
   PAGES
══════════════════════════════════════════ */
.page{display:none;flex:1;padding:14px 12px 80px;}
.page.active{display:block;}
.slbl{font-size:9px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;
  margin-bottom:10px;display:flex;align-items:center;gap:8px;}
.slbl::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent);}

/* GLASS CARD */
.gc{
  background:var(--glass);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border:1px solid var(--border2);border-radius:18px;
  box-shadow:0 2px 20px var(--shadow),inset 0 1px 0 rgba(255,255,255,0.5);
  transition:background .4s,border-color .4s;
}

/* ══════════════════════════════════════════
   KPI — Mobile Stack
══════════════════════════════════════════ */
.kpi-row{display:grid;gap:10px;margin-bottom:16px;}
.kpi-row.row2{grid-template-columns:1fr 1fr;}
.kpi-row.row3{grid-template-columns:1fr 1fr 1fr;}
.kpi{padding:16px 14px;cursor:default;
  transition:transform .3s cubic-bezier(.34,1.56,.64,1),box-shadow .3s;
  animation:fadeUp .5s ease both;overflow:hidden;position:relative;}
.kpi:hover{transform:translateY(-2px);}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
.kpi-ico{font-size:22px;margin-bottom:8px;}
.kpi-lbl{font-size:10px;color:var(--text3);margin-bottom:3px;}
.kpi-val{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;line-height:1;margin-bottom:4px;color:var(--accent);}
.kpi.green .kpi-val{color:var(--green2);}
.kpi.gold .kpi-val{color:var(--gold);}
.kpi-sub{font-size:9px;color:var(--text3);}
.badge{padding:2px 7px;border-radius:20px;font-size:9px;font-weight:700;}
.bp{background:rgba(90,138,106,.15);color:var(--green2);}
.bn{background:rgba(232,121,138,.15);color:var(--accent);}
.chips{display:flex;gap:3px;margin-top:6px;flex-wrap:wrap;}
.chip{padding:2px 6px;border-radius:10px;font-size:9px;font-weight:600;
  background:rgba(255,255,255,0.5);color:var(--text2);}

/* ══════════════════════════════════════════
   ADD FORM — Mobile
══════════════════════════════════════════ */
.add-card{padding:16px;margin-bottom:16px;}
.type-tabs{display:flex;gap:4px;background:rgba(0,0,0,0.04);
  border-radius:10px;padding:3px;margin-bottom:14px;}
.ttab{flex:1;padding:8px;border:none;border-radius:8px;font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;cursor:pointer;transition:.2s;background:transparent;
  color:var(--text3);display:flex;align-items:center;justify-content:center;gap:4px;}
.tt-s{background:rgba(255,255,255,0.8);color:var(--green2);box-shadow:0 2px 8px var(--shadow);}
.tt-b{background:rgba(255,255,255,0.8);color:var(--accent2);box-shadow:0 2px 8px var(--shadow);}

/* Stack fields on mobile */
.fgrid{display:flex;flex-direction:column;gap:8px;margin-bottom:10px;}
.fld{display:flex;flex-direction:column;gap:4px;}
.fld label{font-size:10px;font-weight:700;color:var(--text3);letter-spacing:.5px;}
.fld input,.fld select{
  background:rgba(255,255,255,0.7);border:1px solid var(--border);
  border-radius:10px;padding:10px 12px;font-family:'Tajawal',sans-serif;
  font-size:14px;color:var(--text);outline:none;transition:.2s;width:100%;
  -webkit-appearance:none;
}
.fld input:focus,.fld select:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow);}
.fld input::placeholder{color:var(--text3);}
.fld select option{background:var(--bg);}
.sbtn{width:100%;padding:13px;border:none;border-radius:10px;font-family:'Tajawal',sans-serif;
  font-size:14px;font-weight:700;cursor:pointer;transition:all .25s cubic-bezier(.34,1.56,.64,1);
  display:flex;align-items:center;justify-content:center;gap:6px;
  -webkit-appearance:none;}
.sb-s{background:linear-gradient(135deg,var(--green),var(--green2));color:white;box-shadow:0 3px 12px rgba(90,138,106,.3);}
.sb-s:hover,.sb-s:active{transform:scale(1.02);}
.sb-b{background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;box-shadow:0 3px 12px var(--accent-glow);}
.sb-b:hover,.sb-b:active{transform:scale(1.02);}

/* ══════════════════════════════════════════
   PANELS — Mobile Single Column
══════════════════════════════════════════ */
.panels{display:flex;flex-direction:column;gap:12px;margin-bottom:16px;}
.panel{overflow:hidden;display:flex;flex-direction:column;min-height:200px;}
.ph{padding:12px 14px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);}
.ph-l{display:flex;align-items:center;gap:8px;}
.pico{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;
  justify-content:center;font-size:14px;background:rgba(255,255,255,0.6);}
.ptitle{font-size:12px;font-weight:700;color:var(--accent);}
.pb-title .ptitle{color:var(--green2);}
.pcnt{font-size:9px;font-weight:800;padding:2px 7px;border-radius:12px;
  background:rgba(255,255,255,0.5);color:var(--text2);}
.pbody{padding:6px;flex:1;overflow-y:auto;max-height:240px;
  scrollbar-width:thin;scrollbar-color:var(--border) transparent;}

.empty{padding:24px;text-align:center;color:var(--text3);}
.empty .ei{font-size:28px;margin-bottom:6px;opacity:0.3;}
.empty p{font-size:11px;line-height:1.8;}
.entry{display:flex;align-items:center;gap:7px;padding:9px 6px;border-radius:9px;
  margin-bottom:2px;transition:.2s;animation:ei .3s ease both;}
@keyframes ei{from{opacity:0;transform:scale(.94);}to{opacity:1;transform:scale(1);}}
.entry:hover,.entry:active{background:rgba(255,255,255,0.4);}
.edot{width:5px;height:5px;border-radius:50%;flex-shrink:0;background:var(--accent);}
.es .edot{background:var(--green);}
.eph{width:30px;height:30px;border-radius:7px;background:rgba(255,255,255,0.5);
  border:1px solid var(--border);display:flex;align-items:center;justify-content:center;
  font-size:13px;flex-shrink:0;}
.einfo{flex:1;min-width:0;}
.edesc{font-size:12px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.emeta{display:flex;gap:3px;margin-top:2px;flex-wrap:wrap;align-items:center;}
.edate{font-size:9px;color:var(--text3);}
.epb{font-size:8px;font-weight:700;padding:1px 5px;border-radius:7px;
  background:rgba(255,255,255,0.5);color:var(--text2);}
.eamt{font-family:'Playfair Display',serif;font-size:13px;font-weight:700;white-space:nowrap;flex-shrink:0;color:var(--green2);}
.eamt.exp{color:var(--accent);}
.delbtn{background:none;border:none;cursor:pointer;color:var(--text3);font-size:12px;
  width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center;
  transition:.2s;flex-shrink:0;}
.delbtn:hover,.delbtn:active{background:rgba(232,121,138,.15);color:var(--accent);}

/* ══════════════════════════════════════════
   EXPENSES
══════════════════════════════════════════ */
.exp-row{display:flex;align-items:center;gap:9px;padding:11px 12px;border-radius:12px;
  margin-bottom:7px;background:var(--glass);backdrop-filter:blur(12px);
  border:1px solid var(--border2);transition:.2s;}
.exp-ico{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:17px;background:rgba(255,255,255,0.6);flex-shrink:0;}
.exp-info{flex:1;min-width:0;}
.exp-name{font-size:12px;font-weight:700;color:var(--text);}
.exp-last{font-size:9px;color:var(--text3);margin-top:2px;}
.exp-amt{font-family:'Playfair Display',serif;font-size:14px;font-weight:700;color:var(--accent2);flex-shrink:0;}
.exp-pay-btn{background:linear-gradient(135deg,var(--green),var(--green2));border:none;
  border-radius:8px;color:white;font-size:11px;font-weight:700;padding:6px 10px;
  cursor:pointer;font-family:'Tajawal',sans-serif;transition:.2s;flex-shrink:0;white-space:nowrap;}
.exp-pay-btn.paid{background:rgba(90,138,106,.15);color:var(--green2);box-shadow:none;}

/* ══════════════════════════════════════════
   CHARTS — Stacked on mobile
══════════════════════════════════════════ */
.charts-col{display:flex;flex-direction:column;gap:12px;margin-bottom:16px;}
.chart-card{padding:16px;}
.chart-card h3{font-size:11px;font-weight:700;color:var(--text2);margin-bottom:12px;display:flex;align-items:center;gap:6px;}

/* ══════════════════════════════════════════
   SHELVES — Mobile Cards
══════════════════════════════════════════ */
.shelf-summary{display:flex;flex-direction:column;gap:10px;margin-bottom:16px;}
.shelf-kpi{padding:14px;position:relative;overflow:hidden;animation:fadeUp .5s ease both;}
.shelf-kpi-bar{position:absolute;top:0;right:0;left:0;height:3px;border-radius:18px 18px 0 0;}
.shelf-kpi-name{font-size:13px;font-weight:800;margin-bottom:10px;
  display:flex;align-items:center;gap:7px;color:var(--text);}
.shelf-dot{width:8px;height:8px;border-radius:50%;}
.shelf-kpi-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.skv{text-align:center;padding:7px;background:rgba(255,255,255,0.4);border-radius:8px;}
.skv .v{font-family:'Playfair Display',serif;font-size:13px;font-weight:700;color:var(--text);}
.skv .l{font-size:9px;color:var(--text3);margin-top:2px;}
.shelf-net{margin-top:9px;padding:8px 10px;border-radius:9px;
  display:flex;justify-content:space-between;align-items:center;}
.shelf-net-pos{background:rgba(90,138,106,.1);border:1px solid rgba(90,138,106,.2);}
.shelf-net-neg{background:rgba(232,121,138,.08);border:1px solid var(--border);}
.shelf-net .nl{font-size:9px;color:var(--text3);}
.shelf-net .nv{font-family:'Playfair Display',serif;font-size:14px;font-weight:700;}
.rent-btn{background:rgba(255,255,255,0.4);border:1px solid var(--border);border-radius:7px;
  color:var(--text3);font-size:9px;font-family:'Tajawal',sans-serif;padding:4px 9px;
  cursor:pointer;transition:.2s;margin-top:7px;width:100%;}
.shelf-prods-section{display:flex;flex-direction:column;gap:10px;}
.shelf-prod-card{overflow:hidden;}
.sp-head{padding:12px 14px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);}
.sp-name{font-size:12px;font-weight:700;display:flex;align-items:center;gap:6px;color:var(--text);}
.sp-count{font-size:9px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(255,255,255,0.5);}
.sp-body{padding:5px;max-height:200px;overflow-y:auto;scrollbar-width:thin;}
.prod-row{display:flex;align-items:center;gap:7px;padding:8px 5px;border-radius:8px;
  border-bottom:1px solid rgba(255,255,255,0.3);transition:.2s;}
.prod-row:last-child{border-bottom:none;}
.prod-row:active{background:rgba(255,255,255,0.4);}
.prod-ph{width:30px;height:30px;border-radius:7px;background:rgba(255,255,255,0.5);
  border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.prod-info{flex:1;min-width:0;}
.prod-name{font-size:11px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.prod-price{font-size:9px;color:var(--text3);margin-top:1px;}
.prod-right{display:flex;align-items:center;gap:4px;flex-shrink:0;}
.qty-badge{min-width:24px;padding:2px 6px;border-radius:6px;font-size:10px;font-weight:800;
  text-align:center;background:rgba(90,138,106,.15);color:var(--green2);}
.qty-badge.zero{background:rgba(232,121,138,.12);color:var(--accent);}
.sell-btn{background:linear-gradient(135deg,var(--green),var(--green2));border:none;
  border-radius:7px;color:white;font-size:10px;font-weight:700;padding:5px 9px;
  cursor:pointer;font-family:'Tajawal',sans-serif;transition:.2s;}
.sell-btn:disabled{opacity:.3;cursor:not-allowed;}
.prod-del{background:none;border:none;cursor:pointer;color:var(--text3);font-size:11px;
  width:22px;height:22px;border-radius:5px;display:flex;align-items:center;justify-content:center;}
.prod-del:active{background:rgba(232,121,138,.15);}
.sp-foot{padding:9px 12px;border-top:1px solid var(--border);}
.add-prod-btn{width:100%;padding:8px;border:1px dashed var(--border);border-radius:9px;
  background:transparent;color:var(--text3);font-family:'Tajawal',sans-serif;
  font-size:11px;font-weight:600;cursor:pointer;transition:.2s;}
.add-prod-btn:active{border-color:var(--accent);color:var(--accent);}

/* ══════════════════════════════════════════
   REPORTS / BACKUP
══════════════════════════════════════════ */
.reports-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.rpt-btn{padding:13px 8px;border-radius:12px;border:1px solid var(--border);
  background:var(--glass);font-family:'Tajawal',sans-serif;font-size:11px;font-weight:700;
  color:var(--text2);cursor:pointer;transition:.2s;text-align:center;line-height:1.4;}
.rpt-btn:active{transform:scale(0.97);}
.backup-row{display:flex;gap:8px;margin-bottom:16px;}
.backup-row button,.backup-row label{
  flex:1;padding:11px;border-radius:10px;border:1px solid var(--border);
  background:var(--glass);font-family:'Tajawal',sans-serif;font-size:11px;font-weight:700;
  color:var(--text2);cursor:pointer;text-align:center;display:flex;align-items:center;justify-content:center;gap:5px;}

/* ══════════════════════════════════════════
   MODAL
══════════════════════════════════════════ */
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);
  backdrop-filter:blur(12px);z-index:500;align-items:flex-end;justify-content:center;padding:0;}
.overlay.open{display:flex;}
.modal{
  background:var(--bg);border:1px solid var(--border);
  border-radius:22px 22px 0 0;padding:28px 20px;
  width:100%;max-width:520px;
  box-shadow:0 -8px 40px var(--shadow);
  animation:slideUp2 .35s cubic-bezier(.34,1.56,.64,1);
  max-height:85vh;overflow-y:auto;
}
@keyframes slideUp2{from{opacity:0;transform:translateY(40px);}to{opacity:1;transform:translateY(0);}}
.modal-handle{width:36px;height:4px;background:var(--border);border-radius:4px;margin:0 auto 20px;}
.mico{font-size:40px;margin-bottom:10px;text-align:center;}
.modal h3{font-size:16px;font-weight:800;color:var(--text);margin-bottom:6px;text-align:center;}
.modal p{font-size:12px;color:var(--text2);margin-bottom:16px;text-align:center;line-height:1.7;}
.minput{width:100%;background:rgba(255,255,255,0.5);border:1px solid var(--border);
  border-radius:10px;padding:11px 13px;font-family:'Tajawal',sans-serif;font-size:15px;
  font-weight:700;text-align:center;color:var(--text);outline:none;margin-bottom:10px;transition:.2s;}
.minput:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow);}
.minput.sm{font-size:13px;font-weight:500;text-align:right;}
.mbtns{display:flex;gap:8px;}
.mbtns button{flex:1;padding:12px;border:none;border-radius:10px;font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;cursor:pointer;transition:.2s;}
.bc{background:rgba(255,255,255,0.4);border:1px solid var(--border)!important;color:var(--text2);}
.bcs{background:linear-gradient(135deg,var(--green),var(--green2));color:white;}
.bcp{background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;}

/* ══════════════════════════════════════════
   FLOWER PANEL
══════════════════════════════════════════ */
#flowerPanel{
  display:none;position:fixed;top:0;left:0;right:0;bottom:0;
  z-index:400;background:rgba(0,0,0,0.5);backdrop-filter:blur(8px);
  align-items:flex-end;justify-content:center;
}
#flowerPanel.open{display:flex;}
.flower-sheet{
  background:var(--bg);border-radius:22px 22px 0 0;
  padding:20px;width:100%;max-width:520px;
  max-height:70vh;overflow-y:auto;
  box-shadow:0 -8px 40px var(--shadow);
}

/* TOAST */
.toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%) translateY(80px);
  background:var(--bg);border:1px solid var(--border);color:var(--text);
  padding:9px 20px;border-radius:40px;font-size:12px;font-weight:600;
  box-shadow:0 8px 28px var(--shadow);transition:transform .4s cubic-bezier(.34,1.56,.64,1);
  z-index:9999;white-space:nowrap;max-width:90vw;text-overflow:ellipsis;overflow:hidden;}
.toast.show{transform:translateX(-50%) translateY(0);}

.lb{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:9000;
  align-items:center;justify-content:center;cursor:zoom-out;}
.lb.open{display:flex;}
.lb img{max-width:95vw;max-height:90vh;border-radius:12px;}

/* ══════════════════════════════════════════
   DESKTOP ENHANCEMENTS
══════════════════════════════════════════ */
@media(min-width:768px){
  .header-top{padding:10px 24px;height:62px;}
  .bsub{display:block;}
  .bname{font-size:17px;}
  .page{padding:24px 20px 60px;max-width:1100px;margin:0 auto;}
  .kpi-row.row2{grid-template-columns:1fr 1fr;}
  .kpi-row.row3{grid-template-columns:repeat(3,1fr);}
  .panels{flex-direction:row;}
  .panel{flex:1;}
  .charts-col{display:grid;grid-template-columns:2fr 1fr 1fr;flex-direction:unset;}
  .shelf-summary{display:grid;grid-template-columns:repeat(2,1fr);}
  .shelf-prods-section{display:grid;grid-template-columns:repeat(2,1fr);}
  .reports-grid{grid-template-columns:repeat(4,1fr);}
  .overlay{align-items:center;padding:20px;}
  .modal{border-radius:22px;max-height:90vh;}
  .modal-handle{display:none;}
  #flowerPanel{align-items:center;}
  .flower-sheet{border-radius:22px;max-height:80vh;}
  .fgrid.fg2{flex-direction:row;}
  .fgrid.fg3{flex-direction:row;}
  .fgrid.fg2 .fld,.fgrid.fg3 .fld{flex:1;}
  .toast{bottom:28px;}
}
</style>
</head>
<body>
<div class="bg-scene">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
</div>
<div id="app">

<header>
  <!-- خلفية ورود متحركة للثيم bloom -->
  <div class="rose-bg" id="roseBg"></div>

  <div class="header-top">
    <div class="brand">
      <div class="emblem">🌹</div>
      <div>
        <div class="bname">فيروز فلورز</div>
        <div class="bsub">إدارة المبيعات</div>
      </div>
    </div>
    <div class="header-actions">
      <div id="flowerPill" onclick="toggleFlowerPanel()">
        <span>🌸</span>
        <span id="flowerCount">0</span>
        <span class="exp-badge">تجريبي</span>
      </div>
      <div class="mpill">
        <label>📅</label>
        <select id="msel" onchange="changeMonth()">
          <option value="2025-01">يناير 2025</option><option value="2025-02">فبراير 2025</option>
          <option value="2025-03">مارس 2025</option><option value="2025-04">أبريل 2025</option>
          <option value="2025-05">مايو 2025</option><option value="2025-06">يونيو 2025</option>
          <option value="2025-07">يوليو 2025</option><option value="2025-08">أغسطس 2025</option>
          <option value="2025-09">سبتمبر 2025</option><option value="2025-10">أكتوبر 2025</option>
          <option value="2025-11">نوفمبر 2025</option><option value="2025-12">ديسمبر 2025</option>
          <option value="2026-01">يناير 2026</option><option value="2026-02">فبراير 2026</option>
          <option value="2026-03">مارس 2026</option><option value="2026-04">أبريل 2026</option>
          <option value="2026-05">مايو 2026</option><option value="2026-06">يونيو 2026</option>
          <option value="2026-07">يوليو 2026</option><option value="2026-08">أغسطس 2026</option>
          <option value="2026-09">سبتمبر 2026</option><option value="2026-10">أكتوبر 2026</option>
          <option value="2026-11">نوفمبر 2026</option><option value="2026-12">ديسمبر 2026</option>
        </select>
      </div>
      <button class="theme-btn" id="refreshBtn" onclick="refreshData()" title="تحديث البيانات">🔄</button>
      <button class="theme-btn" onclick="toggleThemePanel()" title="تغيير الثيم">🎨</button>
      <button class="theme-btn" id="langBtn" onclick="toggleLang()" title="تغيير اللغة" style="font-size:12px;font-weight:700;font-family:'Tajawal',sans-serif;">EN</button>
      <a href="/logout" class="logout-btn" title="خروج">🔒</a>
    </div>
  </div>

  <!-- Theme Panel -->
  <div class="theme-panel" id="themePanel">
    <h4>اختر الثيم</h4>
    <div class="themes-grid">
      <div class="th-opt" onclick="setTheme('rose')" id="th-rose">
        <div class="th-circle" style="background:linear-gradient(135deg,#f9c8d0,#e8798a)"></div>
        <span class="th-name">وردي</span>
      </div>
      <div class="th-opt" onclick="setTheme('ocean')" id="th-ocean">
        <div class="th-circle" style="background:linear-gradient(135deg,#0d2233,#4eaccd)"></div>
        <span class="th-name">أزرق</span>
      </div>
      <div class="th-opt" onclick="setTheme('forest')" id="th-forest">
        <div class="th-circle" style="background:linear-gradient(135deg,#e4ede4,#5a8a6a)"></div>
        <span class="th-name">أخضر</span>
      </div>
      <div class="th-opt" onclick="setTheme('gold')" id="th-gold">
        <div class="th-circle" style="background:linear-gradient(135deg,#1a1208,#d4a843)"></div>
        <span class="th-name">ذهبي</span>
      </div>
      <div class="th-opt" onclick="setTheme('lavender')" id="th-lavender">
        <div class="th-circle" style="background:linear-gradient(135deg,#f5f0ff,#9664dc)"></div>
        <span class="th-name">بنفسج</span>
      </div>
      <div class="th-opt" onclick="setTheme('bloom')" id="th-bloom">
        <div class="th-circle" style="background:linear-gradient(135deg,#fff0f5,#e8789a);border:2px solid #e8789a;"></div>
        <span class="th-name">🌸 ورود</span>
      </div>
    </div>
  </div>

  <!-- Nav Tabs -->
  <div class="mobile-tabs">
    <button class="mtab on" onclick="switchTab('home')">📊 الرئيسية</button>
    <button class="mtab" onclick="switchTab('shelves')">🗄️ الرفوف</button>
    <button class="mtab" onclick="switchTab('flowerinv')">🧾 فواتير الورد</button>
    <button class="mtab" onclick="switchTab('reports')">📄 التقارير</button>
  </div>
</header>

<!-- HOME -->
<div id="tab-home" class="page active">
  <div class="slbl"><span data-t="home">ملخص الشهر</span></div>

  <!-- ── قسم اليوم ── -->
  <div class="day-section">
    <div class="day-header">
      <span class="day-title">📅 اليوم</span>
      <span class="day-date" id="todayLabel">—</span>
    </div>
    <div class="kpi-row row2">
      <div class="kpi green gc"><div class="kpi-ico">🌸</div>
        <div class="kpi-lbl">مبيعات اليوم</div>
        <div class="kpi-val" id="dS">0 ر.ع</div>
        <div class="kpi-sub" id="dSc">0 عملية</div></div>
      <div class="kpi gc" style="--kc:var(--accent)"><div class="kpi-ico">🛒</div>
        <div class="kpi-lbl">مشتريات اليوم</div>
        <div class="kpi-val" id="dB" style="color:var(--accent)">0 ر.ع</div>
        <div class="kpi-sub" id="dBc">0 عملية</div></div>
    </div>

  </div>
  <div style="height:1px;background:var(--border);margin-bottom:16px;"></div>

  <!-- ── ملخص الشهر ── -->
  <div class="kpi-row row2">
    <div class="kpi green gc"><div class="kpi-ico">💰</div>
      <div class="kpi-lbl" data-t="sales">المبيعات</div>
      <div class="kpi-val" id="kS">0 ر.ع</div>
      <div class="kpi-sub" id="kSc">0 عملية</div>
      <div class="chips" id="payChips"></div></div>
    <div class="kpi gc" style="--kc:var(--accent)"><div class="kpi-ico">🛒</div>
      <div class="kpi-lbl" data-t="purchases">المشتريات</div>
      <div class="kpi-val" id="kB" style="color:var(--accent)">0 ر.ع</div>
      <div class="kpi-sub" id="kBc">0 عملية</div>
      <div class="chips" id="payerChips"></div></div>
  </div>

  <div class="kpi-row row3">
    <div class="kpi gc"><div class="kpi-ico">💸</div>
      <div class="kpi-lbl" data-t="expenses">المصاريف</div>
      <div class="kpi-val" id="kE" style="color:var(--accent)">0 ر.ع</div>
      <div class="kpi-sub" id="kEd">ثابتة</div></div>
    <div class="kpi gold gc"><div class="kpi-ico">📊</div>
      <div class="kpi-lbl" data-t="grossProfit">ربح قبل المصاريف</div>
      <div class="kpi-val" id="kP">0 ر.ع</div>
      <div class="kpi-sub"><span id="kPb" class="badge">—</span></div></div>
    <div class="kpi green gc"><div class="kpi-ico">🏆</div>
      <div class="kpi-lbl" data-t="netProfit">الربح الصافي</div>
      <div class="kpi-val" id="kN">0 ر.ع</div>
      <div class="kpi-sub"><span id="kNb" class="badge">—</span></div></div>
  </div>

  <!-- ── ملخص فواتير الورد ── -->
  <div class="slbl">🧾 فواتير الورد</div>
  <div class="gc" style="padding:14px;margin-bottom:16px;">
    <div class="kpi-row row2" style="margin-bottom:0;">
      <div class="kpi gc" style="padding:12px 10px;">
        <div class="kpi-ico">✅</div>
        <div class="kpi-lbl">فواتير مدفوعة</div>
        <div class="kpi-val" id="hFiPaidCount" style="color:var(--green2);font-size:15px;">0</div>
        <div class="kpi-sub" id="hFiPaidTotal">0.000 ر.ع</div>
      </div>
      <div class="kpi gc" style="padding:12px 10px;">
        <div class="kpi-ico">⏳</div>
        <div class="kpi-lbl">فواتير غير مدفوعة</div>
        <div class="kpi-val" id="hFiUnpaidCount" style="color:var(--accent);font-size:15px;">0</div>
        <div class="kpi-sub" id="hFiUnpaidTotal">0.000 ر.ع</div>
      </div>
    </div>
  </div>

  <div class="slbl"><span data-t="addNew">إضافة جديد</span></div>
  <div class="add-card gc">
    <div class="type-tabs">
      <button class="ttab tt-s" id="tt-s" onclick="setFT('s')">🌸 مبيعات</button>
      <button class="ttab" id="tt-b" onclick="setFT('b')">📦 مشتريات</button>
    </div>
    <div id="form-s">
      <div class="fgrid fg2">
        <div class="fld"><label>اسم المنتج</label><input id="sDesc" type="text" placeholder="باقة ورد..."/></div>
        <div class="fld"><label>السعر (ر.ع)</label><input id="sAmt" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/></div>
      </div>
      <div class="fgrid fg2">
        <div class="fld"><label>🏷️ الفئة</label>
          <select id="sCat"><option value="">— اختر —</option>
            <option value="ورد وباقات">🌸 ورد وباقات</option>
            <option value="طباعة">🖨️ طباعة 3D</option>
            <option value="تاجات">👑 تاجات</option>
            <option value="عطور">🌿 عطور</option>
            <option value="اكسسوارات">💍 اكسسوارات</option>
            <option value="هدايا">🎁 هدايا</option>
            <option value="تجفيف">🌾 مجفف</option>
            <option value="صناعي">🎨 صناعي</option>
            <option value="أخرى">✨ أخرى</option></select></div>
        <div class="fld"><label>💳 الدفع</label>
          <select id="sPay"><option value="">— اختر —</option>
            <option value="كاش 💵">💵 كاش</option>
            <option value="فيزا 💳">💳 فيزا</option>
            <option value="تحويل 🏦">🏦 تحويل</option></select></div>
      </div>
      <button class="sbtn sb-s" onclick="addSale()" data-tb="addSale">🌸 إضافة مبيعة</button>
    </div>
    <div id="form-b" style="display:none;">
      <div class="fgrid fg2">
        <div class="fld"><label>الوصف / المورد</label><input id="bDesc" type="text" placeholder="نانا هايبر..."/></div>
        <div class="fld"><label>المبلغ (ر.ع)</label><input id="bAmt" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/></div>
      </div>
      <div class="fgrid">
        <div class="fld"><label>👤 من دفع؟</label>
          <select id="bPayer"><option value="">— اختر —</option>
            <option value="حسين">👤 حسين</option>
            <option value="شوق">👤 شوق</option>
            <option value="أخرى">➕ أخرى</option></select></div>
      </div>
      <div id="bOtherWrap" style="display:none;">
        <div class="fld" style="margin-bottom:8px;"><label>الاسم</label><input id="bOther" type="text" placeholder="اكتب الاسم"/></div>
      </div>
      <button class="sbtn sb-b" onclick="addBuy()" data-tb="addBuy">📦 إضافة مشتريات</button>
    </div>
  </div>

  <div class="slbl"><span data-t="fixedExp">المصاريف الثابتة</span></div>
  <div id="expensesWrap" style="margin-bottom:16px;"></div>

  <div class="slbl"><span data-t="records">السجلات</span></div>
  <div class="panels">
    <div class="panel gc">
      <div class="ph"><div class="ph-l"><div class="pico">🌸</div><div class="ptitle">المبيعات</div></div><div class="pcnt" id="sbadge">0</div></div>
      <div class="pbody" id="sl"></div>
    </div>
    <div class="panel gc pb-title">
      <div class="ph"><div class="ph-l"><div class="pico">📦</div><div class="ptitle" style="color:var(--green2)">المشتريات</div></div><div class="pcnt" id="bbadge">0</div></div>
      <div class="pbody" id="bl"></div>
    </div>
  </div>

  <div class="slbl"><span data-t="stats">الإحصائيات</span></div>
  <div class="charts-col">
    <div class="chart-card gc"><h3>📅 مبيعات آخر 14 يوم</h3><canvas id="dayChart" height="170"></canvas></div>
    <div class="chart-card gc"><h3>📈 مبيعات ومشتريات 2026</h3><canvas id="barChart" height="160"></canvas></div>
    <div class="chart-card gc"><h3>💳 طريقة الدفع</h3><canvas id="payChart" height="160"></canvas></div>
    <div class="chart-card gc"><h3>👤 من دفع</h3><canvas id="payerChart" height="160"></canvas></div>
  </div>
</div>

<!-- SHELVES -->
<div id="tab-shelves" class="page">
  <div class="slbl">ملخص الرفوف</div>
  <div class="shelf-summary" id="shelfSummary"></div>
  <div class="slbl">منتجات الرفوف</div>
  <div class="shelf-prods-section" id="shelfProds"></div>
</div>

<!-- FLOWER INVOICES -->
<div id="tab-flowerinv" class="page">
  <div class="slbl">فواتير شركات الورد</div>

  <!-- اختيار الشهر + ملخص -->
  <div class="gc" style="padding:14px;margin-bottom:16px;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
      <select id="fi-month-sel" onchange="loadFlowerInvPage()" style="flex:1;padding:9px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg2);color:var(--text);font-family:'Tajawal',sans-serif;font-size:13px;font-weight:600;"></select>
      <button onclick="loadFlowerInvPage()" style="padding:9px 14px;border:1px solid var(--border);border-radius:10px;background:var(--glass);color:var(--text2);font-family:'Tajawal',sans-serif;font-size:12px;cursor:pointer;">🔄</button>
    </div>
    <!-- KPIs -->
    <div class="kpi-row row3" id="fi-kpis">
      <div class="kpi gc"><div class="kpi-ico">🧾</div><div class="kpi-lbl">عدد الفواتير</div><div class="kpi-val" id="fi-count">—</div></div>
      <div class="kpi gc"><div class="kpi-ico">🏪</div><div class="kpi-lbl">عدد الشركات</div><div class="kpi-val" id="fi-companies">—</div></div>
      <div class="kpi gc gold"><div class="kpi-ico">💰</div><div class="kpi-lbl">إجمالي الشهر</div><div class="kpi-val" id="fi-total">—</div></div>
    </div>
  </div>

  <!-- زر إضافة يدوي + زر رفع صورة -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;">
    <button onclick="openAddFlowerInvModal()" style="padding:13px;border:none;border-radius:14px;background:linear-gradient(135deg,var(--gold),#b8891f);color:white;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 3px 14px rgba(212,168,67,.35);display:flex;align-items:center;justify-content:center;gap:6px;transition:transform .2s;" onmousedown="this.style.transform='scale(0.97)'" onmouseup="this.style.transform='scale(1)'">
      ➕ إضافة يدوياً
    </button>
    <button onclick="triggerFlowerInvScan()" style="padding:13px;border:none;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 3px 14px var(--accent-glow);display:flex;align-items:center;justify-content:center;gap:6px;transition:transform .2s;" onmousedown="this.style.transform='scale(0.97)'" onmouseup="this.style.transform='scale(1)'">
      📷 رفع صورة فاتورة
    </button>
  </div>
  <!-- Input مخفي لرفع الصورة -->
  <input type="file" id="fi-scan-input" accept="image/*" style="display:none" onchange="handleFlowerInvScan(this)">

  <!-- قائمة الفواتير -->
  <div class="slbl">الفواتير</div>
  <div id="fi-list"></div>

  <div style="font-size:10px;color:var(--text3);text-align:center;margin-top:12px;line-height:1.9;">
    📸 أرسل للبوت صورة الفاتورة + تعليق <b>"فاتورة ورد"</b><br>
    البوت يقرأ الأصناف والأسعار والشركة تلقائياً
  </div>
</div>

<!-- MODAL: إضافة فاتورة ورد يدوياً -->
<div class="overlay" id="addFlowerInvOv" onclick="if(event.target===this)closeAddFlowerInvModal()">
  <div class="modal" style="max-height:92vh;">
    <div class="modal-handle"></div>
    <div class="mico">🧾</div>
    <h3>إضافة فاتورة ورد</h3>

    <div class="fgrid fg2" style="margin-bottom:10px;">
      <div class="fld">
        <label>🏪 اسم الشركة / المورد</label>
        <input id="fi-company" type="text" placeholder="مثال: نانا هايبر" style="background:rgba(255,255,255,0.7);border:1px solid var(--border);border-radius:10px;padding:10px 12px;font-family:'Tajawal',sans-serif;font-size:14px;color:var(--text);outline:none;width:100%;"/>
      </div>
      <div class="fld">
        <label>📅 تاريخ الفاتورة</label>
        <input id="fi-date" type="date" style="background:rgba(255,255,255,0.7);border:1px solid var(--border);border-radius:10px;padding:10px 12px;font-family:'Tajawal',sans-serif;font-size:14px;color:var(--text);outline:none;width:100%;"/>
      </div>
    </div>
    <div class="fld" style="margin-bottom:14px;">
      <label>🔖 رقم الفاتورة <span style="font-weight:400;color:var(--text3);">(اختياري)</span></label>
      <input id="fi-invno" type="text" placeholder="مثال: INV-2024-001" style="background:rgba(255,255,255,0.7);border:1px solid var(--border);border-radius:10px;padding:10px 12px;font-family:'Tajawal',sans-serif;font-size:14px;color:var(--text);outline:none;width:100%;direction:ltr;text-align:left;letter-spacing:.5px;"/>
    </div>

    <!-- الأصناف -->
    <div style="font-size:10px;font-weight:700;color:var(--text3);letter-spacing:1px;margin-bottom:8px;">🌹 الأصناف</div>
    <div id="fi-items-list" style="margin-bottom:8px;"></div>
    <button onclick="addFlowerInvItem()" style="width:100%;padding:9px;border:1px dashed var(--border);border-radius:10px;background:transparent;color:var(--text3);font-family:'Tajawal',sans-serif;font-size:12px;font-weight:600;cursor:pointer;margin-bottom:14px;">+ إضافة صنف</button>

    <!-- الإجمالي -->
    <div style="background:rgba(212,168,67,.08);border:1px solid rgba(212,168,67,.25);border-radius:12px;padding:12px 14px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;">
      <span style="font-size:12px;font-weight:700;color:var(--text2);">💰 الإجمالي</span>
      <div style="display:flex;align-items:center;gap:6px;">
        <input id="fi-total-input" type="number" step="0.001" placeholder="0.000" inputmode="decimal"
          style="width:110px;background:rgba(255,255,255,0.7);border:1px solid rgba(212,168,67,.4);border-radius:8px;padding:7px 10px;font-family:'Tajawal',sans-serif;font-size:15px;font-weight:800;color:var(--gold);outline:none;text-align:center;"
          oninput="syncFlowerInvTotal()"/>
        <span style="font-size:11px;font-weight:700;color:var(--text3);">ر.ع</span>
      </div>
    </div>

    <div class="mbtns">
      <button class="bc" onclick="closeAddFlowerInvModal()">إلغاء</button>
      <button class="bcp" onclick="saveFlowerInvManual()" style="background:linear-gradient(135deg,var(--gold),#b8891f);">💾 حفظ الفاتورة</button>
    </div>
  </div>
</div>

<!-- REPORTS -->
<div id="tab-reports" class="page">

  <!-- نوع التقرير -->
  <div class="slbl">نوع التقرير</div>
  <div class="rpt-type-row">
    <button class="rpt-type-btn active" id="rpt-t-day"   onclick="setRptPeriod('day')">📅 يومي</button>
    <button class="rpt-type-btn"        id="rpt-t-month" onclick="setRptPeriod('month')">📆 شهري</button>
  </div>

  <!-- اختيار اليوم -->
  <div id="rpt-day-picker" class="rpt-picker">
    <div class="fld"><label>📅 اختر اليوم</label>
      <input type="date" id="rptDayInput" onchange="updateRptDayLabel()"/>
    </div>
    <div class="rpt-day-label" id="rptDayLabel">اليوم</div>
  </div>

  <!-- اختيار الشهر -->
  <div id="rpt-month-picker" class="rpt-picker" style="display:none">
    <div class="fld"><label>📆 اختر الشهر</label>
      <select id="rptMonthInput">
        <option value="2025-01">يناير 2025</option><option value="2025-02">فبراير 2025</option>
        <option value="2025-03">مارس 2025</option><option value="2025-04">أبريل 2025</option>
        <option value="2025-05">مايو 2025</option><option value="2025-06">يونيو 2025</option>
        <option value="2025-07">يوليو 2025</option><option value="2025-08">أغسطس 2025</option>
        <option value="2025-09">سبتمبر 2025</option><option value="2025-10">أكتوبر 2025</option>
        <option value="2025-11">نوفمبر 2025</option><option value="2025-12">ديسمبر 2025</option>
        <option value="2026-01">يناير 2026</option><option value="2026-02">فبراير 2026</option>
        <option value="2026-03">مارس 2026</option><option value="2026-04">أبريل 2026</option>
        <option value="2026-05" selected>مايو 2026</option><option value="2026-06">يونيو 2026</option>
        <option value="2026-07">يوليو 2026</option><option value="2026-08">أغسطس 2026</option>
        <option value="2026-09">سبتمبر 2026</option><option value="2026-10">أكتوبر 2026</option>
        <option value="2026-11">نوفمبر 2026</option><option value="2026-12">ديسمبر 2026</option>
      </select>
    </div>
  </div>

  <!-- نوع المحتوى -->
  <div class="slbl">محتوى التقرير</div>
  <div class="reports-grid">
    <button class="rpt-btn gc" onclick="openReport('all')">📊<br>شامل</button>
    <button class="rpt-btn gc" onclick="openReport('sales')">🌸<br>المبيعات</button>
    <button class="rpt-btn gc" onclick="openReport('buys')">📦<br>المشتريات</button>
    <button class="rpt-btn gc" onclick="openReport('expenses')">💸<br>المصاريف</button>
  </div>
  <div class="slbl">النسخ الاحتياطي</div>
  <div class="backup-row">
    <button class="gc" onclick="doBackup()">💾 تصدير JSON</button>
    <label class="gc">📂 استعادة<input type="file" accept=".json" onchange="doRestore(event)" style="display:none"/></label>
  </div>
</div>
</div>

<!-- THEME PANEL -->
<div id="themePanel" style="display:none;position:fixed;top:62px;left:50%;transform:translateX(-50%);
  z-index:300;background:var(--bg);border:1px solid var(--border2);border-radius:16px;
  padding:16px;box-shadow:0 8px 32px var(--shadow);min-width:280px;">
  <div style="font-size:10px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;text-align:center;margin-bottom:12px;">اختر الثيم</div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">
    <div onclick="setTheme('rose')" id="th-rose" style="cursor:pointer;text-align:center;padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;">
      <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#f9c8d0,#e8798a);margin:0 auto 4px;box-shadow:0 2px 8px rgba(0,0,0,.2);"></div>
      <span style="font-size:9px;color:var(--text3);font-weight:600;">وردي</span>
    </div>
    <div onclick="setTheme('ocean')" id="th-ocean" style="cursor:pointer;text-align:center;padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;">
      <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#0d2233,#4eaccd);margin:0 auto 4px;box-shadow:0 2px 8px rgba(0,0,0,.2);"></div>
      <span style="font-size:9px;color:var(--text3);font-weight:600;">أزرق</span>
    </div>
    <div onclick="setTheme('forest')" id="th-forest" style="cursor:pointer;text-align:center;padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;">
      <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#e4ede4,#5a8a6a);margin:0 auto 4px;box-shadow:0 2px 8px rgba(0,0,0,.2);"></div>
      <span style="font-size:9px;color:var(--text3);font-weight:600;">أخضر</span>
    </div>
    <div onclick="setTheme('gold')" id="th-gold" style="cursor:pointer;text-align:center;padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;">
      <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#1a1208,#d4a843);margin:0 auto 4px;box-shadow:0 2px 8px rgba(0,0,0,.2);"></div>
      <span style="font-size:9px;color:var(--text3);font-weight:600;">ذهبي</span>
    </div>
    <div onclick="setTheme('lavender')" id="th-lavender" style="cursor:pointer;text-align:center;padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;">
      <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#f5f0ff,#9664dc);margin:0 auto 4px;box-shadow:0 2px 8px rgba(0,0,0,.2);"></div>
      <span style="font-size:9px;color:var(--text3);font-weight:600;">بنفسجي</span>
    </div>
  </div>
</div>

<!-- MODALS -->
<div class="overlay" id="addProdOv">
  <div class="modal">
    <div class="modal-handle"></div>
    <div class="mico">📦</div>
    <h3 id="addProdTitle">إضافة منتج</h3>
    <input class="minput sm" id="pName" type="text" placeholder="اسم المنتج" style="margin-bottom:8px;"/>
    <div class="fgrid fg2" style="margin-bottom:12px;">
      <div class="fld"><label>السعر (ر.ع)</label><input id="pPrice" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/></div>
      <div class="fld"><label>الكمية</label><input id="pQty" type="number" placeholder="0" min="0" inputmode="numeric"/></div>
    </div>
    <div class="mbtns"><button class="bc" onclick="closeProdModal()">إلغاء</button><button class="bcs" onclick="saveProduct()">✅ إضافة</button></div>
  </div>
</div>

<div class="overlay" id="sellOv">
  <div class="modal">
    <div class="modal-handle"></div>
    <div class="mico">🌸</div>
    <h3>تسجيل مبيعة</h3>
    <p id="sellDesc" style="font-weight:700;color:var(--text);margin-bottom:3px;"></p>
    <p id="sellInfo" style="color:var(--text3);margin-bottom:14px;"></p>
    <div class="fgrid fg2" style="margin-bottom:12px;">
      <div class="fld"><label>الكمية</label><input id="sellQty" type="number" value="1" min="1" inputmode="numeric"/></div>
      <div class="fld"><label>💳 الدفع</label>
        <select id="sellPay"><option value="">— اختر —</option>
          <option value="كاش 💵">💵 كاش</option>
          <option value="فيزا 💳">💳 فيزا</option>
          <option value="تحويل 🏦">🏦 تحويل</option></select></div>
    </div>
    <div class="mbtns"><button class="bc" onclick="closeSellModal()">إلغاء</button><button class="bcs" onclick="confirmSell()">💰 تأكيد</button></div>
  </div>
</div>

<div class="overlay" id="rentOv">
  <div class="modal">
    <div class="modal-handle"></div>
    <div class="mico">🏷️</div>
    <h3 id="rentTitle">تعديل الإيجار</h3>
    <p>الإيجار الشهري للرف</p>
    <input class="minput" id="rentVal" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/>
    <div class="mbtns"><button class="bc" onclick="closeRentModal()">إلغاء</button><button class="bcs" onclick="saveRent()">✅ حفظ</button></div>
  </div>
</div>

<div class="overlay" id="ov"><div class="modal"><div class="modal-handle"></div><div id="mb"></div></div></div>

<!-- FLOWER PANEL -->
<div id="flowerPanel" onclick="if(event.target===this)toggleFlowerPanel()">
  <div class="flower-sheet">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
      <div style="font-size:13px;font-weight:800;color:var(--text);">🌸 مخزون الورد</div>
      <button onclick="toggleFlowerPanel()" style="background:none;border:none;font-size:18px;cursor:pointer;color:var(--text3);">✕</button>
    </div>
    <div id="flowerList"></div>
    <div style="font-size:10px;color:var(--text3);text-align:center;margin-top:10px;line-height:1.8;">
      📸 صورة + <b>"عد الورد"</b> &nbsp;|&nbsp; ✏️ <b>"عندي ورد روز 20"</b>
    </div>
  </div>
</div>

<div class="lb" id="lb" onclick="this.classList.remove('open')"><img id="lbImg" src=""/></div>
<div class="toast" id="toast"></div>

<script>
/* ── THEME ── */
const THEMES = ['rose','ocean','forest','gold','lavender'];
let currentTheme = localStorage.getItem('fairuz_theme') || 'rose';

// ── خلفية الورود المتحركة ──
function initRoseBg(){
  const bg = document.getElementById('roseBg');
  if(!bg || bg.children.length > 0) return;
  const petals = ['🌸','🌹','🌺','🌼','🌷','💮','🏵️'];
  for(let i=0;i<22;i++){
    const p = document.createElement('div');
    p.className = 'petal';
    p.textContent = petals[Math.floor(Math.random()*petals.length)];
    const left = Math.random()*100;
    const dur  = 6 + Math.random()*10;
    const delay= Math.random()*12;
    const size = 14 + Math.random()*16;
    p.style.cssText = `left:${left}%;font-size:${size}px;animation-duration:${dur}s;animation-delay:-${delay}s;`;
    bg.appendChild(p);
  }
}

function setTheme(t){
  currentTheme = t;
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('fairuz_theme', t);
  document.querySelectorAll('.th-opt').forEach(el => el.classList.remove('active'));
  const el = document.getElementById('th-'+t);
  if(el) el.classList.add('active');
  if(t==='bloom') initRoseBg();
  if(barCI) loadCharts();
}

function toggleThemePanel(){
  document.getElementById('themePanel').classList.toggle('open');
}

// Init theme
setTheme(currentTheme);
document.addEventListener('click', e => {
  if(!e.target.closest('.theme-btn') && !e.target.closest('.theme-panel'))
    document.getElementById('themePanel').classList.remove('open');
});

/* ── STATE ── */
let formTab='s';
const _now = new Date();
let month = `${_now.getFullYear()}-${String(_now.getMonth()+1).padStart(2,'0')}`;
let barCI=null,payCI=null,payerCI=null,dayCI=null;

// ── بيانات اليوم ──
function getTodayStr(){
  const d=new Date();
  const dd=String(d.getDate()).padStart(2,'0');
  const mm=String(d.getMonth()+1).padStart(2,'0');
  const yyyy=d.getFullYear();
  return `${dd}/${mm}/${yyyy}`;
}

function renderDayKPI(todaySales, todayBuys, allSales, allBuys){
  const today = getTodayStr();
  document.getElementById('todayLabel').textContent = today;
  const ts = todaySales.reduce((a,e)=>a+e.amt,0);
  const tb = todayBuys.reduce((a,e)=>a+e.amt,0);
  const cur = t('currency');
  document.getElementById('dS').textContent = fmt(ts)+' '+cur;
  document.getElementById('dSc').textContent = todaySales.length+' '+t('operations');
  document.getElementById('dB').textContent = fmt(tb)+' '+cur;
  document.getElementById('dBc').textContent = todayBuys.length+' '+t('operations');
  // الرسم البياني يستخدم كل بيانات الشهر
  renderDayChart(allSales, allBuys);
}

function renderDayChart(allSales, allBuys){
  // نبني قاموس بكل أيام آخر 14 يوم
  const days = {};
  for(let i=13;i>=0;i--){
    const d = new Date(); d.setDate(d.getDate()-i);
    const dd=String(d.getDate()).padStart(2,'0');
    const mm=String(d.getMonth()+1).padStart(2,'0');
    const yyyy=d.getFullYear();
    const key=`${dd}/${mm}/${yyyy}`;
    const short=i===0?'اليوم':i===1?'أمس':`${dd}/${mm}`;
    days[key]={label:short, s:0, b:0};
  }
  // نجمع المبيعات
  (allSales||[]).forEach(e=>{ if(days[e.date]) days[e.date].s+=e.amt; });
  // نجمع المشتريات
  (allBuys||[]).forEach(e=>{ if(e.type!=='expense' && days[e.date]) days[e.date].b+=e.amt; });

  const labels = Object.values(days).map(d=>d.label);
  const salesVals = Object.values(days).map(d=>d.s);
  const buysVals  = Object.values(days).map(d=>d.b);

  if(dayCI) dayCI.destroy();
  const ctx = document.getElementById('dayChart');
  if(!ctx) return;
  dayCI = new Chart(ctx,{
    type:'bar',
    data:{
      labels,
      datasets:[
        {
          label:'مبيعات',
          data:salesVals,
          backgroundColor:'rgba(100,200,120,0.75)',
          borderRadius:5,
          borderSkipped:false,
        },
        {
          label:'مشتريات',
          data:buysVals,
          backgroundColor:'rgba(220,80,80,0.6)',
          borderRadius:5,
          borderSkipped:false,
        }
      ]
    },
    options:{
      responsive:true,
      plugins:{
        legend:{display:true,position:'top',labels:{font:{size:10},boxWidth:12}},
        tooltip:{callbacks:{label:i=>`${i.dataset.label}: ${fmt(i.raw)} ر.ع`}}
      },
      scales:{
        x:{grid:{display:false},ticks:{font:{size:9}}},
        y:{grid:{color:'rgba(128,128,128,0.1)'},ticks:{font:{size:9},callback:v=>v>0?fmt(v):''},beginAtZero:true}
      }
    }
  });
}
let activeProdShelf=null,activeSellProd=null,activeRentShelf=null;
let flowerOpen=false;

/* ── API ── */
async function api(url,opts){const r=await fetch(url,opts);return r.json();}
function fmt(n){return (+n).toLocaleString('ar-OM',{minimumFractionDigits:3,maximumFractionDigits:3});}

/* ── TAB ── */
function switchTab(t){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.mtab').forEach(b=>b.classList.remove('on'));
  document.getElementById('tab-'+t).classList.add('active');
  document.querySelectorAll('.mtab').forEach(b=>{
    if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes("'"+t+"'"))b.classList.add('on');
  });
  if(t==='shelves') loadShelves();
  if(t==='flowerinv') loadFlowerInvPage();
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

/* ── LOAD ── */
function showSkeleton(){
  // skeleton يظهر فوراً بينما تجي البيانات
  const skl = `<div class="skl-row"><div class="skl"></div><div class="skl skl-sm"></div></div>`;
  const kpis = document.querySelectorAll('.kpi-val');
  kpis.forEach(el=>{ el.style.opacity='0.3'; });
  ['sl','bl'].forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.innerHTML=skl.repeat(3);
  });
}
function hideSkeleton(){
  document.querySelectorAll('.kpi-val').forEach(el=>{ el.style.opacity='1'; });
}

async function load(){
  showSkeleton();
  try {
    const dash = await api(`/api/dashboard?month=${month}`);
    _lastData = dash;
    _lastExpData = dash.expenses;
    hideSkeleton();
    renderKPI(dash.sales, dash.buys, dash.expenses);
    renderLists(dash.sales, dash.buys);
    loadExpensesPanel(dash, dash.expenses);
    // بيانات اليوم
    const todayStr = getTodayStr();
    const todaySales = dash.sales.filter(e=>e.date===todayStr);
    const todayBuys  = dash.buys.filter(e=>e.date===todayStr && e.type!=='expense');
    renderDayKPI(todaySales, todayBuys, dash.sales, dash.buys);
    const ms = ['01','02','03','04','05','06','07','08','09','10','11','12'];
    const yr = month.split('-')[0];
    const all = ms.map(m => dash.charts[`${yr}-${m}`] || {sales:[],buys:[]});
    renderBarChart(
      all.map(d=>d.sales.reduce((a,e)=>a+e.amt,0)),
      all.map(d=>d.buys.filter(e=>e.type!=='expense').reduce((a,e)=>a+e.amt,0))
    );
    const cur = all[parseInt(month.split('-')[1])-1];
    if(cur){ renderPayChart(cur.sales); renderPayerChart(cur.buys.filter(e=>e.type!=='expense')); }
    if(dash.flowers) document.getElementById('flowerCount').textContent = dash.flowers.total || 0;
  } catch(e){ hideSkeleton(); console.error('load error', e); }
}

// تحديث تلقائي كل 60 ثانية
setInterval(()=>{load();if(document.getElementById('tab-shelves').classList.contains('active'))loadShelves();},60000);

async function refreshData(){
  const btn = document.getElementById('refreshBtn');
  if(!btn) return;
  btn.style.animation = 'spin 0.7s linear infinite';
  btn.disabled = true;
  await load();
  if(document.getElementById('tab-shelves').classList.contains('active')) await loadShelves();
  btn.style.animation = '';
  btn.disabled = false;
  showToast('✅ تم تحديث البيانات');
}

/* ── KPI ── */
function renderKPI(sales,buys,expD){
  const ts=sales.reduce((a,e)=>a+e.amt,0);
  const tb=buys.filter(e=>e.type!=='expense').reduce((a,e)=>a+e.amt,0);
  const tp=ts-tb;
  const paidExps=(expD&&expD.paid)||[];
  const te=paidExps.reduce((a,e)=>a+e.amt,0);
  const tn=tp-te;
  const cur=t('currency');
  document.getElementById('kS').textContent=fmt(ts)+' '+cur;
  document.getElementById('kSc').textContent=sales.length+' '+t('operations');
  document.getElementById('kB').textContent=fmt(tb)+' '+cur;
  document.getElementById('kBc').textContent=buys.filter(e=>e.type!=='expense').length+' '+t('operations');
  document.getElementById('kE').textContent=fmt(te)+' '+cur;
  document.getElementById('kEd').textContent=te>0?paidExps.length+' '+t('paid'):t('notPaid');
  document.getElementById('kP').textContent=(tp>=0?'+':'')+fmt(tp)+' '+cur;
  document.getElementById('kP').style.color=tp>=0?'var(--gold)':'var(--accent)';
  const b=document.getElementById('kPb');
  b.textContent=tp>0?t('profit'):tp<0?t('loss'):'—';
  b.className='badge '+(tp>0?'bp':tp<0?'bn':'');
  document.getElementById('kN').textContent=(tn>=0?'+':'')+fmt(tn)+' '+cur;
  document.getElementById('kN').style.color=tn>=0?'var(--green2)':'var(--accent)';
  const nb=document.getElementById('kNb');
  nb.textContent=tn>0?t('net'):tn<0?t('loss'):'—';
  nb.className='badge '+(tn>0?'bp':tn<0?'bn':'');
  const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};
  sales.forEach(e=>{if(e.payment_method&&pm[e.payment_method]!==undefined)pm[e.payment_method]+=e.amt;});
  document.getElementById('payChips').innerHTML=Object.entries(pm).filter(([,v])=>v>0)
    .map(([k,v])=>`<span class="chip">${k} ${fmt(v)}</span>`).join('');
  const py={};buys.filter(e=>e.type!=='expense').forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});
  document.getElementById('payerChips').innerHTML=Object.entries(py)
    .map(([k,v])=>`<span class="chip">👤${k} ${fmt(v)}</span>`).join('');
}

/* ── LISTS ── */
function pb(pm){if(!pm)return'';return`<span class="epb">${pm}</span>`;}
function renderLists(sales,buys){
  const catIcons={"ورد وباقات":"🌸","طباعة":"🖨️","تاجات":"👑","عطور":"🌿","اكسسوارات":"💍","هدايا":"🎁","تجفيف":"🌾","صناعي":"🎨","أخرى":"✨"};
  const cur=t('currency');
  document.getElementById('sl').innerHTML=sales.length?sales.map(e=>`
    <div class="entry es">
      <div class="eph">${catIcons[e.category]||'🌸'}</div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${pb(e.payment_method)}${e.category?`<span class="epb">${e.category}</span>`:''}</div></div>
      <div class="eamt">+${fmt(e.amt)}</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button>
    </div>`).join(''):`<div class="empty"><div class="ei">🌷</div><p>${lang==='en'?'No sales yet':'لا توجد مبيعات'}</p></div>`;
  const buysOnly=buys.filter(e=>e.type!=='expense');
  document.getElementById('bl').innerHTML=buysOnly.length?buysOnly.map(e=>`
    <div class="entry">
      <div class="edot"></div>
      <div class="einfo"><div class="edesc">${e.desc}</div>
        <div class="emeta"><span class="edate">${e.date}</span>${e.paid_by?`<span class="epb">👤${e.paid_by}</span>`:''}</div></div>
      <div class="eamt exp">-${fmt(e.amt)}</div>
      <button class="delbtn" onclick="del(${e.id})">🗑</button>
    </div>`).join(''):`<div class="empty"><div class="ei">🌿</div><p>${lang==='en'?'No purchases yet':'لا توجد مشتريات'}</p></div>`;
  document.getElementById('sbadge').textContent=sales.length;
  document.getElementById('bbadge').textContent=buysOnly.length;
}

/* ── CHARTS ── */
const mnames=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
function getCC(){
  const s=getComputedStyle(document.documentElement);
  return{green:s.getPropertyValue('--green').trim(),accent:s.getPropertyValue('--accent').trim(),gold:s.getPropertyValue('--gold').trim(),text3:s.getPropertyValue('--text3').trim()};
}
const co={responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(128,128,128,.08)'},ticks:{color:'#888',font:{family:'Tajawal',size:9}}},y:{grid:{color:'rgba(128,128,128,.08)'},ticks:{color:'#888',font:{family:'Tajawal',size:9}}}}};
function renderBarChart(aS,aB){
  if(barCI)barCI.destroy();
  const c=getCC();
  barCI=new Chart(document.getElementById('barChart'),{type:'bar',
    data:{labels:mnames.map(m=>m.slice(0,3)),datasets:[
      {label:'مبيعات',data:aS,backgroundColor:c.green+'bb',borderRadius:4},
      {label:'مشتريات',data:aB,backgroundColor:c.accent+'aa',borderRadius:4}]},
    options:{...co,plugins:{legend:{display:true,labels:{color:'#888',font:{family:'Tajawal',size:10}}}}}});
}
function renderPayChart(sales){
  const pm={'كاش 💵':0,'فيزا 💳':0,'تحويل 🏦':0};
  sales.forEach(e=>{if(e.payment_method&&pm[e.payment_method]!==undefined)pm[e.payment_method]+=e.amt;});
  if(payCI)payCI.destroy();
  payCI=new Chart(document.getElementById('payChart'),{type:'doughnut',
    data:{labels:Object.keys(pm),datasets:[{data:Object.values(pm),
      backgroundColor:['rgba(90,138,106,.8)','rgba(78,140,200,.8)','rgba(155,100,220,.8)'],borderWidth:0}]},
    options:{responsive:true,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:'#888',font:{family:'Tajawal',size:9},padding:6}}}}});
}
function renderPayerChart(buys){
  const py={};buys.forEach(e=>{if(e.paid_by){py[e.paid_by]=(py[e.paid_by]||0)+e.amt;}});
  const clrs=['rgba(232,121,138,.8)','rgba(90,138,106,.8)','rgba(212,168,67,.8)','rgba(150,100,220,.8)'];
  if(payerCI)payerCI.destroy();
  payerCI=new Chart(document.getElementById('payerChart'),{type:'doughnut',
    data:{labels:Object.keys(py).length?Object.keys(py):['لا يوجد'],
      datasets:[{data:Object.keys(py).length?Object.values(py):[1],
        backgroundColor:Object.keys(py).length?clrs.slice(0,Object.keys(py).length):['rgba(128,128,128,.2)'],borderWidth:0}]},
    options:{responsive:true,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:'#888',font:{family:'Tajawal',size:9},padding:6}}}}});
}

/* ── ADD ── */
async function addSale(){
  const desc=document.getElementById('sDesc').value.trim()||'مبيعة';
  const amt=parseFloat(document.getElementById('sAmt').value);
  const pay=document.getElementById('sPay').value;
  const cat=document.getElementById('sCat').value;
  if(!amt||amt<=0){showToast(t('errAmt'));return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'s',desc,amt,payment_method:pay||null,category:cat||null,month})});
  document.getElementById('sDesc').value='';document.getElementById('sAmt').value='';
  document.getElementById('sPay').value='';document.getElementById('sCat').value='';
  load();showToast(t('addToast'));
}

async function addBuy(){
  const desc=document.getElementById('bDesc').value.trim()||'مشتريات';
  const amt=parseFloat(document.getElementById('bAmt').value);
  let payer=document.getElementById('bPayer').value;
  if(payer==='أخرى')payer=document.getElementById('bOther').value.trim()||null;
  if(!amt||amt<=0){showToast(t('errAmt'));return;}
  await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'b',desc,amt,paid_by:payer||null,month})});
  document.getElementById('bDesc').value='';document.getElementById('bAmt').value='';
  document.getElementById('bPayer').value='';
  load();showToast(t('addToast'));
}

async function del(id){await api(`/api/entries/${id}`,{method:'DELETE'});load();showToast(t('delToast'));}

/* ── EXPENSES ── */
async function loadExpensesPanel(d, expD){
  if(!expD) expD = await api(`/api/expenses?month=${month}`);
  const icons={"راتب العامل":"👷","إيجار المحل":"🏪","تعبئة كهرباء":"⚡"};
  const wrap=document.getElementById('expensesWrap');
  if(!wrap)return;
  let html='';
  for(const e of (expD.expenses||[])){
    const isElec=e.name.includes('كهرباء')||e.name.includes('تعبئة');
    const icon=icons[e.name]||'💼';
    const myPaid=(expD.paid||[]).filter(p=>p.desc&&p.desc.includes(e.name.replace('فاتورة ','').split(' ')[0]));
    const totalPaid=myPaid.reduce((a,p)=>a+p.amt,0);
    const isPaid=myPaid.length>0;
    const lastDate=myPaid.length?myPaid[myPaid.length-1].date:null;
    const defaultNames=['راتب العامل','إيجار المحل','تعبئة كهرباء'];
    const canDel=!defaultNames.includes(e.name);
    html+=`<div class="exp-row">
      <div class="exp-ico">${icon}</div>
      <div class="exp-info">
        <div class="exp-name">${e.name}</div>
        <div class="exp-last">${isPaid?'✅ آخر دفع: '+lastDate:(e.last_paid?'آخر تعبئة: '+e.last_paid:'لم يُدفع بعد')}</div>
      </div>
      <div class="exp-amt" style="color:${isPaid?'var(--green2)':'var(--accent)'};">${isPaid?fmt(totalPaid):fmt(e.amount)} ر.ع</div>
      <div style="display:flex;gap:4px;flex-shrink:0;">
        <button class="exp-pay-btn ${isPaid?'paid':''}" onclick="${isElec?`addElecBill(${e.id})`:`payExpense(${e.id},'${e.name}',${e.amount})`}">
          ${isElec?'⚡':'💳'} ${isElec?'تعبئة':'دفع'}
        </button>
        ${canDel?`<button onclick="delExpenseDef(${e.id},'${e.name}')" style="background:rgba(232,121,138,.1);border:1px solid rgba(232,121,138,.2);border-radius:7px;color:var(--accent);font-size:11px;padding:5px 7px;cursor:pointer;">🗑</button>`:''}
      </div>
    </div>`;
    if(myPaid.length){
      html+=`<div style="margin:-4px 0 8px;padding:6px 10px;background:rgba(90,138,106,.06);border-radius:0 0 10px 10px;border:1px solid rgba(90,138,106,.15);border-top:none;">`;
      for(const p of myPaid){
        html+=`<div style="display:flex;align-items:center;gap:6px;padding:4px 0;border-bottom:1px solid rgba(0,0,0,.04);">
          <span style="font-size:11px;color:var(--text2);flex:1;">📅 ${p.date} — ${fmt(p.amt)} ر.ع</span>
          <button onclick="delSingleExpEntry(${p.id},${e.id})" style="background:rgba(232,121,138,.1);border:1px solid rgba(232,121,138,.2);border-radius:6px;color:var(--accent);font-size:9px;padding:2px 7px;cursor:pointer;font-family:Tajawal,sans-serif;">🗑</button>
        </div>`;
      }
      html+=`</div>`;
    }
  }
  html+=`<button onclick="addExpensePrompt()" style="width:100%;padding:9px;border:1px dashed var(--border);border-radius:10px;background:transparent;color:var(--text3);font-family:Tajawal,sans-serif;font-size:11px;font-weight:600;cursor:pointer;margin-top:4px;">+ إضافة مصروف ثابت</button>`;
  wrap.innerHTML=html;
}

async function delSingleExpEntry(entryId,expId){
  if(!confirm('حذف هذه الفاتورة؟'))return;
  await api(`/api/expense_entries/${entryId}`,{method:'DELETE'});
  const d2=await api(`/api/expenses?month=${month}`);
  const exp=(d2.expenses||[]).find(e=>e.id===expId);
  if(exp){
    const rem=(d2.paid||[]).filter(p=>p.desc&&p.desc.includes(exp.name.replace('فاتورة ','').split(' ')[0]));
    if(!rem.length) await api(`/api/expenses/${expId}/reset`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month})});
  }
  load();showToast('✅ تم حذف الفاتورة');
}

async function delExpenseDef(id,name){
  if(!confirm(`حذف مصروف "${name}" نهائياً؟`))return;
  await api(`/api/expenses/${id}`,{method:'DELETE'});
  load();showToast(`✅ تم حذف ${name}`);
}

async function cancelExpense(expId,name){
  const d2=await api(`/api/expenses?month=${month}`);
  const entries=(d2.paid||[]).filter(p=>p.desc&&p.desc.includes(name.split(' ')[0]));
  for(const e of entries) await api(`/api/expense_entries/${e.id}`,{method:'DELETE'});
  await api(`/api/expenses/${expId}/reset`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month})});
  load();showToast('✅ تم إلغاء الدفع');
}

async function payExpense(id,name,defaultAmt){
  const amt=prompt(`ادفع ${name}\nالمبلغ (ر.ع):`,defaultAmt.toFixed(3));
  if(!amt)return;
  const a=parseFloat(amt);
  if(isNaN(a)||a<=0){showToast('⚠️ مبلغ غير صحيح');return;}
  await api(`/api/expenses/${id}/pay`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month,amount:a})});
  load();showToast(`✅ تم تسجيل دفع ${name}`);
}

async function addElecBill(expId){
  const amt=prompt('مبلغ التعبئة (ر.ع):','');
  if(!amt)return;
  const a=parseFloat(amt);
  if(isNaN(a)||a<=0){showToast('⚠️ مبلغ غير صحيح');return;}
  const dateStr=prompt('تاريخ التعبئة (DD/MM/YYYY):',new Date().toLocaleDateString('en-GB'));
  if(!dateStr)return;
  let em=month;
  try{const p=dateStr.split('/');if(p.length===3)em=`${p[2]}-${p[1].padStart(2,'0')}`;}catch(e){}
  await api(`/api/expenses/${expId}/pay`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month:em,amount:a,date:dateStr})});
  load();showToast(`⚡ تم تسجيل تعبئة ${fmt(a)} ر.ع`);
}

async function addExpensePrompt(){
  const name=prompt('اسم المصروف:');if(!name)return;
  const amt=prompt('المبلغ الشهري (ر.ع):','0.000');if(!amt)return;
  await api('/api/expenses',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,amount:parseFloat(amt)||0})});
  load();showToast('✅ تمت إضافة المصروف');
}

/* ── SHELVES ── */
async function loadShelves(){
  const shelves=await api(`/api/shelves?month=${month}`);
  document.getElementById('shelfSummary').innerHTML=shelves.map(s=>{
    const netPos=s.net>=0;
    return `<div class="shelf-kpi gc">
      <div class="shelf-kpi-bar" style="background:${s.color}"></div>
      <div class="shelf-kpi-name"><div class="shelf-dot" style="background:${s.color}"></div>رف ${s.name}</div>
      <div class="shelf-kpi-grid">
        <div class="skv"><div class="v" style="color:var(--green2)">${fmt(s.monthly_sales)}</div><div class="l">مبيعات</div></div>
        <div class="skv"><div class="v" style="color:var(--accent)">${fmt(s.rent)}</div><div class="l">إيجار</div></div>
        <div class="skv"><div class="v">${s.sales_count}</div><div class="l">عمليات</div></div>
        <div class="skv"><div class="v">${s.products.reduce((a,p)=>a+p.qty,0)}</div><div class="l">قطع</div></div>
      </div>
      <div class="shelf-net ${netPos?'shelf-net-pos':'shelf-net-neg'}">
        <span class="nl">صافي بعد الإيجار</span>
        <span class="nv" style="color:${netPos?'var(--green2)':'var(--accent)'}">${s.net>=0?'+':''}${fmt(s.net)} ر.ع</span>
      </div>
      <button class="rent-btn" onclick="openRent(${s.id},'${s.name}',${s.rent})">✏️ إيجار: ${fmt(s.rent)} ر.ع</button>
    </div>`;}).join('');
  document.getElementById('shelfProds').innerHTML=shelves.map(s=>`
    <div class="shelf-prod-card gc">
      <div class="sp-head" style="border-bottom:2px solid ${s.color}44;">
        <div class="sp-name"><div class="shelf-dot" style="background:${s.color}"></div>رف ${s.name}</div>
        <span class="sp-count">${s.products.length} منتج</span>
      </div>
      <div class="sp-body">
        ${s.products.length?s.products.map(p=>`
          <div class="prod-row">
            <div class="prod-ph">🌸</div>
            <div class="prod-info"><div class="prod-name">${p.name}</div><div class="prod-price">${fmt(p.price)} ر.ع</div></div>
            <div class="prod-right">
              <div class="qty-badge ${p.qty===0?'zero':''}">${p.qty}</div>
              <button class="sell-btn" ${p.qty===0?'disabled':''} onclick="openSell(${p.id},'${p.name.replace(/'/g,"\\'")}',${p.price},${p.qty})">بيع</button>
              <button class="prod-del" onclick="delProd(${p.id})">🗑</button>
            </div>
          </div>`).join(''):`<div style="padding:16px;text-align:center;color:var(--text3);font-size:11px;">لا توجد منتجات</div>`}
      </div>
      <div class="sp-foot"><button class="add-prod-btn" onclick="openAddProd(${s.id},'${s.name}')">+ إضافة منتج</button></div>
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
async function delProd(pid){await api(`/api/shelf_products/${pid}`,{method:'DELETE'});loadShelves();showToast(t('delToast'));}
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
  const rent=parseFloat(document.getElementById('rentVal').value);if(isNaN(rent)||rent<0){showToast('⚠️ مبلغ غير صحيح');return;}
  await api(`/api/shelves/${activeRentShelf}/rent`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({rent})});
  closeRentModal();loadShelves();showToast('✅ تم تحديث الإيجار');
}

/* ── FLOWERS ── */
async function loadFlowers(){
  try{
    const d=await api('/api/flowers');
    const totalStems=(d.flowers||[]).filter(f=>f.unit!=='بندلة').reduce((s,f)=>s+f.count,0);
    const totalBundles=(d.flowers||[]).filter(f=>f.unit==='بندلة').reduce((s,f)=>s+f.count,0);
    document.getElementById('flowerCount').textContent=d.total||0;
    document.getElementById('flowerList').innerHTML=d.flowers&&d.flowers.length?
      d.flowers.map(f=>{
        const isBundle=f.unit==='بندلة';
        const ico=isBundle?'🌸':'🌹';
        const unitLabel=isBundle?'بندلة':'وردة';
        return `<div style="display:flex;align-items:center;gap:8px;padding:8px 4px;border-bottom:1px solid var(--border);">
          <span style="font-size:18px;">${ico}</span>
          <div style="flex:1;">
            <div style="font-size:12px;font-weight:600;">${f.name}</div>
            <div style="font-size:9px;color:var(--text3);">${unitLabel}</div>
          </div>
          <button onclick="updateFlowerCount(${f.id},${f.count-1},'${f.unit||'وردة'}')" style="width:26px;height:26px;border-radius:50%;border:1px solid var(--border);background:var(--glass);cursor:pointer;">−</button>
          <span style="font-size:14px;font-weight:800;min-width:28px;text-align:center;color:${isBundle?'var(--gold)':'var(--accent)'};">${f.count}</span>
          <button onclick="updateFlowerCount(${f.id},${f.count+1},'${f.unit||'وردة'}')" style="width:26px;height:26px;border-radius:50%;border:1px solid var(--border);background:var(--glass);cursor:pointer;">+</button>
          <button onclick="delFlower(${f.id})" style="background:none;border:none;cursor:pointer;color:var(--text3);">🗑</button>
        </div>`;
      }).join('')+
      `<div style="display:flex;gap:8px;padding:10px 4px 4px;justify-content:center;">
        ${totalStems?`<span style="font-size:10px;background:rgba(232,121,138,.12);color:var(--accent);padding:3px 10px;border-radius:20px;font-weight:700;">🌹 ${totalStems} وردة</span>`:''}
        ${totalBundles?`<span style="font-size:10px;background:rgba(212,168,67,.12);color:var(--gold);padding:3px 10px;border-radius:20px;font-weight:700;">🌸 ${totalBundles} بندلة</span>`:''}
      </div>
      <div style="font-size:9px;color:var(--text3);text-align:center;margin-top:4px;">آخر تحديث: ${d.updated||'—'}</div>`:
      `<div style="padding:20px;text-align:center;color:var(--text3);font-size:12px;">لا يوجد مخزون<br>أرسل للبوت: <b>عندي ورد روز أحمر 20</b><br>أو صورة مع "عد الورد"</div>`;
  }catch(e){}
}
function toggleFlowerPanel(){
  flowerOpen=!flowerOpen;
  document.getElementById('flowerPanel').classList.toggle('open',flowerOpen);
  if(flowerOpen) loadFlowers();
}
async function updateFlowerCount(id,n,unit){if(n<0)return;await api(`/api/flowers/${id}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({count:n,unit:unit||'وردة'})});loadFlowers();}
async function delFlower(id){await api(`/api/flowers/${id}`,{method:'DELETE'});loadFlowers();showToast(t('delToast'));}

/* ── FLOWER INVOICES PAGE ── */
async function loadFlowerInvPage(){
  try{
    const sel=document.getElementById('fi-month-sel');
    const m=sel.value||'';
    const d=await api('/api/flower_invoices'+(m?'?month='+m:''));
    // populate month selector
    if(d.months&&d.months.length){
      const cur=sel.value||d.month;
      sel.innerHTML=d.months.map(mo=>`<option value="${mo}"${mo===cur?' selected':''}>${mo}</option>`).join('');
      if(!sel.value&&d.month) sel.value=d.month;
    } else if(!sel.innerHTML) {
      const now=new Date(); const mo=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0');
      sel.innerHTML=`<option value="${mo}">${mo}</option>`;
    }
    const invs=d.invoices||[];
    // KPIs
    const companies=[...new Set(invs.map(i=>i.company).filter(Boolean))];
    document.getElementById('fi-count').textContent=invs.length;
    document.getElementById('fi-companies').textContent=companies.length;
    document.getElementById('fi-total').textContent=d.total?(+d.total).toFixed(3)+' ر.ع':'0.000 ر.ع';
    // Update home page summary
    const hPaidCount=document.getElementById('hFiPaidCount');
    const hPaidTotal=document.getElementById('hFiPaidTotal');
    const hUnpaidCount=document.getElementById('hFiUnpaidCount');
    const hUnpaidTotal=document.getElementById('hFiUnpaidTotal');
    if(hPaidCount){hPaidCount.textContent=d.paid_count||0;}
    if(hPaidTotal){hPaidTotal.textContent=(+(d.paid_total||0)).toFixed(3)+' ر.ع';}
    if(hUnpaidCount){hUnpaidCount.textContent=d.unpaid_count||0;}
    if(hUnpaidTotal){hUnpaidTotal.textContent=(+(d.unpaid_total||0)).toFixed(3)+' ر.ع';}
    // List
    const list=document.getElementById('fi-list');
    if(!invs.length){
      list.innerHTML=`<div class="gc" style="padding:24px;text-align:center;color:var(--text3);font-size:12px;line-height:2;">
        لا توجد فواتير هذا الشهر<br>
        📸 أرسل صورة الفاتورة للبوت مع تعليق <b>"فاتورة ورد"</b><br>
        أو استخدم زر <b>📷 رفع صورة</b> أعلاه لتحليل الفاتورة تلقائياً
      </div>`;
      return;
    }
    list.innerHTML=invs.map(inv=>{
      const items=inv.items||[];
      const isPaid=inv.is_paid?1:0;
      const itemsHtml=items.map(i=>`
        <div style="display:flex;justify-content:space-between;align-items:center;padding:5px 12px;border-bottom:1px solid var(--border);">
          <span style="font-size:11px;color:var(--text2);">${i.unit==='بندلة'?'🌸':'🌹'} ${i.name}: <b>${i.count}</b> ${i.unit||'وردة'}</span>
          ${parseFloat(i.unit_price||0)>0?`<span style="font-size:11px;color:var(--text3);">${(+i.line_total||0).toFixed(3)} ر.ع</span>`:''}
        </div>`).join('');
      return `<div class="gc" style="margin-bottom:12px;overflow:hidden;${isPaid?'opacity:0.85;':''}">
        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 14px;border-bottom:1px solid var(--border);">
          <div>
            <div style="font-size:13px;font-weight:800;">🏪 ${inv.company||'غير محدد'}</div>
            ${inv.invoice_number?`<div style="font-size:10px;color:var(--gold);margin-top:2px;letter-spacing:.5px;direction:ltr;text-align:right;">🔖 ${inv.invoice_number}</div>`:''}
            <div style="font-size:11px;color:var(--text3);margin-top:2px;">📅 ${inv.inv_date}</div>
          </div>
          <div style="display:flex;align-items:center;gap:7px;">
            <div style="font-size:15px;font-weight:900;color:var(--accent);">${(+inv.total||0).toFixed(3)} <span style="font-size:10px;font-weight:600;">ر.ع</span></div>
            <button onclick="toggleFlowerInvPaid(${inv.id})" style="background:${isPaid?'rgba(90,138,106,.2)':'rgba(107,76,59,.08)'};border:1px solid ${isPaid?'rgba(90,138,106,.4)':'var(--border)'};border-radius:8px;color:${isPaid?'var(--green2)':'var(--text3)'};font-size:11px;font-weight:700;padding:4px 8px;cursor:pointer;white-space:nowrap;">${isPaid?'✅ مدفوعة':'⏳ غير مدفوعة'}</button>
            <button onclick="delFlowerInv(${inv.id})" style="background:rgba(232,121,138,.1);border:1px solid rgba(232,121,138,.2);border-radius:8px;color:var(--accent);font-size:13px;width:30px;height:30px;cursor:pointer;">🗑</button>
          </div>
        </div>
        ${items.length?`<div style="padding:4px 0;">${itemsHtml}</div>`:''}
      </div>`;
    }).join('');
  }catch(e){console.error(e);}
}
async function delFlowerInv(id){
  if(!confirm('حذف هذه الفاتورة؟'))return;
  await api('/api/flower_invoices/'+id,{method:'DELETE'});
  loadFlowerInvPage();
  showToast('✅ تم حذف الفاتورة');
}
async function toggleFlowerInvPaid(id){
  try{
    const r=await api('/api/flower_invoices/'+id+'/toggle_paid',{method:'POST'});
    loadFlowerInvPage();
    showToast(r.is_paid?'✅ تم تحديدها كمدفوعة':'⏳ تم تحديدها كغير مدفوعة');
  }catch(e){showToast('❌ خطأ في التحديث');}
}

/* ── رفع صورة فاتورة ورد للتحليل التلقائي ── */
function triggerFlowerInvScan(){
  const inp = document.getElementById('fi-scan-input');
  if(inp) inp.click();
}

async function handleFlowerInvScan(input){
  const file = input.files && input.files[0];
  if(!file) return;
  input.value='';
  showToast('⏳ جاري تحليل الفاتورة...');
  try{
    const fd = new FormData();
    fd.append('file', file);
    const res = await fetch('/api/flower_invoices/scan', {
      method:'POST',
      credentials:'same-origin',
      body: fd
    });
    const d = await res.json();
    if(!res.ok || d.error){
      showToast('❌ ' + (d.error||'خطأ في التحليل'));
      return;
    }
    showToast('✅ تم حفظ الفاتورة: ' + (d.company||'') + ' — ' + (d.total||0).toFixed(3) + ' ر.ع');
    loadFlowerInvPage();
  }catch(e){
    showToast('❌ خطأ في الرفع');
  }
}

/* ── إضافة فاتورة ورد يدوياً ── */
let fiItems=[];

function openAddFlowerInvModal(){
  fiItems=[];
  // تاريخ اليوم
  const now=new Date();
  const dd=String(now.getDate()).padStart(2,'0');
  const mm=String(now.getMonth()+1).padStart(2,'0');
  const yyyy=now.getFullYear();
  document.getElementById('fi-date').value=`${yyyy}-${mm}-${dd}`;
  document.getElementById('fi-company').value='';
  document.getElementById('fi-total-input').value='';
  document.getElementById('fi-invno').value='';
  renderFiItems();
  document.getElementById('addFlowerInvOv').classList.add('open');
  setTimeout(()=>document.getElementById('fi-company').focus(),300);
}

function closeAddFlowerInvModal(){
  document.getElementById('addFlowerInvOv').classList.remove('open');
}

function renderFiItems(){
  const cont=document.getElementById('fi-items-list');
  if(!fiItems.length){
    cont.innerHTML=`<div style="text-align:center;color:var(--text3);font-size:11px;padding:10px 0;">لا توجد أصناف — اضغط "إضافة صنف"</div>`;
    return;
  }
  cont.innerHTML=fiItems.map((it,i)=>`
    <div style="display:flex;gap:6px;align-items:center;margin-bottom:8px;background:rgba(255,255,255,0.4);border:1px solid var(--border);border-radius:10px;padding:8px 10px;">
      <div style="flex:2;">
        <input type="text" value="${it.name||''}" placeholder="اسم الصنف" 
          oninput="fiItems[${i}].name=this.value"
          style="width:100%;background:transparent;border:none;outline:none;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:600;color:var(--text);" />
        <div style="display:flex;gap:6px;margin-top:4px;">
          <select onchange="fiItems[${i}].unit=this.value;renderFiItems()" 
            style="flex:1;background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:4px 6px;font-family:'Tajawal',sans-serif;font-size:11px;color:var(--text2);">
            <option value="وردة"${it.unit==='وردة'?' selected':''}>🌹 وردة</option>
            <option value="بندلة"${it.unit==='بندلة'?' selected':''}>🌸 بندلة</option>
            <option value="علبة"${it.unit==='علبة'?' selected':''}>📦 علبة</option>
          </select>
          <input type="number" min="0" value="${it.count||''}" placeholder="العدد"
            oninput="fiItems[${i}].count=+this.value;calcFiItemTotal(${i})"
            style="width:60px;background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:4px 6px;font-family:'Tajawal',sans-serif;font-size:12px;text-align:center;" />
          <input type="number" step="0.001" value="${it.unit_price||''}" placeholder="السعر"
            oninput="fiItems[${i}].unit_price=+this.value;calcFiItemTotal(${i})"
            style="width:75px;background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:4px 6px;font-family:'Tajawal',sans-serif;font-size:12px;text-align:center;" />
        </div>
      </div>
      <div style="text-align:center;min-width:52px;">
        <div style="font-size:11px;font-weight:800;color:var(--gold);">${((it.line_total)||0).toFixed(3)}</div>
        <div style="font-size:9px;color:var(--text3);">ر.ع</div>
      </div>
      <button onclick="fiItems.splice(${i},1);renderFiItems();recalcFiTotal()" 
        style="background:rgba(232,121,138,.12);border:1px solid rgba(232,121,138,.2);border-radius:8px;color:var(--accent);font-size:14px;width:28px;height:28px;cursor:pointer;flex-shrink:0;">🗑</button>
    </div>
  `).join('');
}

function addFlowerInvItem(){
  fiItems.push({name:'',unit:'وردة',count:0,unit_price:0,line_total:0});
  renderFiItems();
  // focus على آخر input اسم
  setTimeout(()=>{
    const inputs=document.querySelectorAll('#fi-items-list input[type="text"]');
    if(inputs.length) inputs[inputs.length-1].focus();
  },50);
}

function calcFiItemTotal(i){
  const it=fiItems[i];
  it.line_total=(it.count||0)*(it.unit_price||0);
  recalcFiTotal();
  renderFiItems();
}

function recalcFiTotal(){
  const sum=fiItems.reduce((a,it)=>a+(it.line_total||0),0);
  if(sum>0) document.getElementById('fi-total-input').value=sum.toFixed(3);
}

function syncFlowerInvTotal(){/* يسمح للمستخدم يغير الإجمالي يدوياً */}

async function saveFlowerInvManual(){
  const company=(document.getElementById('fi-company').value||'').trim()||'غير محدد';
  const dateRaw=document.getElementById('fi-date').value;
  const totalRaw=document.getElementById('fi-total-input').value;
  const invNo=(document.getElementById('fi-invno').value||'').trim()||null;
  if(!dateRaw){showToast('⚠️ اختر تاريخ الفاتورة');return;}
  if(!totalRaw||parseFloat(totalRaw)<=0){showToast('⚠️ أدخل الإجمالي');return;}
  // تحويل التاريخ من yyyy-mm-dd إلى dd/mm/yyyy
  const [y,m,d]=dateRaw.split('-');
  const inv_date=`${d}/${m}/${y}`;
  // تحضير الأصناف
  const items=fiItems.filter(it=>it.name||it.count).map(it=>({
    name:it.name||'—',unit:it.unit||'وردة',count:it.count||0,
    unit_price:it.unit_price||0,line_total:it.line_total||0
  }));
  const total=parseFloat(totalRaw)||0;
  try{
    await api('/api/flower_invoices',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({company,invoice_number:invNo,inv_date,total,items})});
    closeAddFlowerInvModal();
    loadFlowerInvPage();
    showToast('✅ تم حفظ الفاتورة بنجاح');
  }catch(e){showToast('❌ خطأ في الحفظ');}
}

/* ── REPORTS ── */
// ── التقارير ──
let rptPeriod = 'day';

function setRptPeriod(p){
  rptPeriod = p;
  document.querySelectorAll('.rpt-type-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('rpt-t-'+p).classList.add('active');
  document.getElementById('rpt-day-picker').style.display   = p==='day'  ?'':'none';
  document.getElementById('rpt-month-picker').style.display = p==='month'?'':'none';
}

function updateRptDayLabel(){
  const v = document.getElementById('rptDayInput').value;
  if(!v){ document.getElementById('rptDayLabel').textContent='اليوم'; return; }
  const d = new Date(v);
  const days=['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت'];
  document.getElementById('rptDayLabel').textContent = days[d.getDay()]+' '+d.toLocaleDateString('ar-OM');
}

function openReport(type){
  showToast('⏳ جاري فتح التقرير...');
  let url;
  if(rptPeriod==='day'){
    let dayVal = document.getElementById('rptDayInput').value;
    if(!dayVal){
      // افتراضي: اليوم
      const n=new Date();
      dayVal=`${n.getFullYear()}-${String(n.getMonth()+1).padStart(2,'0')}-${String(n.getDate()).padStart(2,'0')}`;
    }
    // تحويل yyyy-mm-dd → dd/mm/yyyy
    const [y,m,d]=dayVal.split('-');
    const dayStr=`${d}/${m}/${y}`;
    url=`/api/report/pdf?day=${encodeURIComponent(dayStr)}&type=${type}&period=day`;
  } else {
    const m = document.getElementById('rptMonthInput').value;
    url=`/api/report/pdf?month=${m}&type=${type}&period=month`;
  }
  window.open(url,'_blank');
}

// تهيئة تاريخ اليوم
(function(){
  const n=new Date();
  const dayVal=`${n.getFullYear()}-${String(n.getMonth()+1).padStart(2,'0')}-${String(n.getDate()).padStart(2,'0')}`;
  const el=document.getElementById('rptDayInput');
  if(el){ el.value=dayVal; updateRptDayLabel(); }
  // تحديد الشهر الحالي في select
  const ms=document.getElementById('rptMonthInput');
  if(ms) ms.value=month;
})();

/* ── BACKUP ── */
async function doBackup(){
  showToast('⏳ جاري تصدير البيانات...');
  const r=await fetch('/api/backup');const blob=await r.blob();
  const url=URL.createObjectURL(blob);const a=document.createElement('a');
  a.href=url;a.download=`fairuz_backup_${new Date().toISOString().slice(0,10)}.json`;a.click();
  URL.revokeObjectURL(url);showToast('✅ تم التصدير');
}
async function doRestore(ev){
  const file=ev.target.files[0];if(!file)return;ev.target.value='';
  if(!confirm('استيراد البيانات من الملف؟'))return;
  showToast('⏳ جاري الاستيراد...');
  const text=await file.text();const data=JSON.parse(text);
  const r=await api('/api/restore',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  if(r.ok){showToast(`✅ تم الاستيراد — ${r.restored.entries} إدخال`);load();}
  else showToast('❌ '+(r.error||'خطأ'));
}

/* ── MISC ── */
document.querySelectorAll('.overlay').forEach(o=>o.addEventListener('click',function(e){if(e.target===this)this.classList.remove('open');}));
function changeMonth(){
  const prev = month;
  month = document.getElementById('msel').value;
  // امسح الـ cache لو تغيرت السنة
  if(prev.split('-')[0] !== month.split('-')[0]){ _chartsCache={}; _chartsCacheYear=null; }
  load();loadFlowers();
  if(document.getElementById('tab-shelves').classList.contains('active'))loadShelves();
}
function showToast(msg){const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3000);}

// Set month selector to current month
(function(){
  const sel = document.getElementById('msel');
  if(sel){
    sel.value = month;
    // If not found, default to first available
    if(!sel.value) sel.selectedIndex = 0;
  }
})();

/* ── THEMES ── */
function setTheme(t){
  document.documentElement.setAttribute('data-theme',t);
  localStorage.setItem('fairuz_theme',t);
  document.querySelectorAll('[id^="th-"]').forEach(el=>{
    el.style.borderColor=el.id==='th-'+t?'var(--accent)':'transparent';
    el.style.background=el.id==='th-'+t?'rgba(255,255,255,0.15)':'transparent';
  });
}
function toggleThemePanel(){
  const p=document.getElementById('themePanel');
  p.style.display=p.style.display==='none'?'block':'none';
}
document.addEventListener('click',e=>{
  if(!e.target.closest('#themePanel')&&!e.target.closest('button[onclick*="toggleThemePanel"]'))
    document.getElementById('themePanel').style.display='none';
});
// Init saved theme
const savedTheme=localStorage.getItem('fairuz_theme')||'rose';
setTheme(savedTheme);

/* ── BILINGUAL ── */
const T = {
  ar: {
    home:'📊 الرئيسية', shelves:'🗄️ الرفوف', reports:'📄 تقارير',
    sales:'المبيعات', purchases:'المشتريات', expenses:'المصاريف',
    grossProfit:'ربح قبل المصاريف', netProfit:'الربح الصافي',
    addNew:'إضافة جديد', addSale:'🌸 إضافة مبيعة', addBuy:'📦 إضافة مشتريات',
    productName:'اسم المنتج', price:'السعر (ر.ع)', category:'🏷️ الفئة',
    payment:'💳 الدفع', supplier:'الوصف', whoPaid:'👤 من دفع؟',
    records:'السجلات', stats:'الإحصائيات', fixedExp:'المصاريف الثابتة',
    shelfSummary:'ملخص الرفوف', shelfProds:'منتجات الرفوف',
    operations:'عملية', paid:'مدفوع', notPaid:'لم تُدفع',
    currency:'ر.ع', profit:'✅ ربح', loss:'⚠️ خسارة', net:'🏆 صافي',
    reports2:'تقارير', salesRpt:'المبيعات', buysRpt:'المشتريات', expRpt:'المصاريف', allRpt:'شامل',
    backup:'النسخ الاحتياطي', export:'💾 تصدير', restore:'📂 استعادة',
    addToast:'✅ تمت الإضافة', delToast:'🗑️ تم الحذف', errAmt:'⚠️ أدخل مبلغاً صحيحاً',
    choosePay:'— اختر —', cash:'💵 كاش', visa:'💳 فيزا', transfer:'🏦 تحويل',
    chooseWho:'— اختر —', other:'➕ أخرى', name:'الاسم',
    jan:'يناير',feb:'فبراير',mar:'مارس',apr:'أبريل',may:'مايو',jun:'يونيو',
    jul:'يوليو',aug:'أغسطس',sep:'سبتمبر',oct:'أكتوبر',nov:'نوفمبر',dec:'ديسمبر',
  },
  en: {
    home:'📊 Dashboard', shelves:'🗄️ Shelves', reports:'📄 Reports',
    sales:'Sales', purchases:'Purchases', expenses:'Expenses',
    grossProfit:'Gross Profit', netProfit:'Net Profit',
    addNew:'Add New', addSale:'🌸 Add Sale', addBuy:'📦 Add Purchase',
    productName:'Product Name', price:'Price (OMR)', category:'🏷️ Category',
    payment:'💳 Payment', supplier:'Description', whoPaid:'👤 Paid By?',
    records:'Records', stats:'Statistics', fixedExp:'Fixed Expenses',
    shelfSummary:'Shelf Summary', shelfProds:'Shelf Products',
    operations:'ops', paid:'Paid', notPaid:'Not paid',
    currency:'OMR', profit:'✅ Profit', loss:'⚠️ Loss', net:'🏆 Net',
    reports2:'Reports', salesRpt:'Sales', buysRpt:'Purchases', expRpt:'Expenses', allRpt:'Full Report',
    backup:'Backup', export:'💾 Export', restore:'📂 Restore',
    addToast:'✅ Added successfully', delToast:'🗑️ Deleted', errAmt:'⚠️ Enter a valid amount',
    choosePay:'— Select —', cash:'💵 Cash', visa:'💳 Visa', transfer:'🏦 Transfer',
    chooseWho:'— Select —', other:'➕ Other', name:'Name',
    jan:'Jan',feb:'Feb',mar:'Mar',apr:'Apr',may:'May',jun:'Jun',
    jul:'Jul',aug:'Aug',sep:'Sep',oct:'Oct',nov:'Nov',dec:'Dec',
  }
};
let lang = localStorage.getItem('fairuz_lang') || 'ar';

// cache آخر بيانات محملة عشان نستخدمها عند تغيير اللغة بدون API call جديد
let _lastData = null;
let _lastExpData = null;

function setLang(l){
  lang = l;
  localStorage.setItem('fairuz_lang', l);
  document.documentElement.setAttribute('dir', l==='ar'?'rtl':'ltr');
  document.documentElement.setAttribute('lang', l);
  applyTranslations();
  updateLangBtn();
  // أعد رسم البيانات من الـ cache بدون API call جديد
  if(_lastData && _lastExpData){
    renderKPI(_lastData.sales, _lastData.buys, _lastExpData);
    renderLists(_lastData.sales, _lastData.buys);
    loadExpensesPanel(_lastData, _lastExpData);
    const todayStr = getTodayStr();
    const todaySales = _lastData.sales.filter(e=>e.date===todayStr);
    const todayBuys  = _lastData.buys.filter(e=>e.date===todayStr && e.type!=='expense');
    renderDayKPI(todaySales, todayBuys, _lastData.sales, _lastData.buys);
  }
}

function t(key){ return T[lang][key] || T['ar'][key] || key; }

function applyTranslations(){
  // Nav tabs
  document.getElementById('nt-home').textContent = t('home');
  document.getElementById('nt-shelves').textContent = t('shelves');
  document.getElementById('nt-reports').textContent = t('reports');
  // Section labels
  const labels = document.querySelectorAll('[data-t]');
  labels.forEach(el => { if(T[lang][el.dataset.t]) el.textContent = t(el.dataset.t); });
  // Buttons
  const btns = document.querySelectorAll('[data-tb]');
  btns.forEach(el => { if(T[lang][el.dataset.tb]) el.textContent = t(el.dataset.tb); });
}

function updateLangBtn(){
  const btn = document.getElementById('langBtn');
  if(btn) btn.textContent = lang === 'ar' ? 'EN' : 'ع';
}

function toggleLang(){
  setLang(lang === 'ar' ? 'en' : 'ar');
}

// Init language
setLang(lang);

load(); // طلب واحد يجيب كل شيء
loadFlowerInvPage(); // تحميل ملخص فواتير الورد في الصفحة الرئيسية
</script>
</body>
</html>"""
