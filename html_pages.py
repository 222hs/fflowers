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
   HEADER — إطار مستقل فاخر
══════════════════════════════════════════ */
header{
  position:sticky;top:0;z-index:100;
  padding:10px 12px 0;
  background:var(--bg);
  transition:background .4s;
}
.header-frame{
  background:linear-gradient(135deg,var(--accent2) 0%,var(--accent) 50%,var(--gold) 100%);
  border-radius:20px;
  padding:2px;
  box-shadow:0 6px 28px var(--accent-glow), 0 2px 8px var(--shadow);
  animation:glow 4s ease-in-out infinite;
}
.header-inner{
  background:var(--nav-bg);
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border-radius:18px;
  overflow:hidden;
}
/* الصف العلوي — اسم المحل */
.header-brand-row{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 14px 8px;gap:6px;
  border-bottom:1px solid var(--border);
}
.header-corner{display:flex;align-items:center;gap:5px;flex-shrink:0;min-width:50px;}
.header-corner-r{display:flex;align-items:center;gap:6px;flex-shrink:0;min-width:50px;justify-content:flex-end;}
.brand-center{display:flex;align-items:center;gap:8px;flex:1;justify-content:center;}
.emblem{
  width:34px;height:34px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:17px;
  box-shadow:0 3px 10px var(--accent-glow);flex-shrink:0;
  position:relative;overflow:hidden;
}
.emblem::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.3),transparent);
  border-radius:inherit;
}
@keyframes glow{0%,100%{box-shadow:0 6px 28px var(--accent-glow),0 2px 8px var(--shadow);}
  50%{box-shadow:0 6px 36px var(--accent-glow),0 0 50px var(--accent-glow),0 2px 8px var(--shadow);}}
.brand-titles{display:flex;flex-direction:column;align-items:center;}
.bname{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:var(--accent2);line-height:1.2;letter-spacing:.3px;}
.bsub{font-size:9px;color:var(--text3);letter-spacing:1.5px;font-weight:600;text-transform:uppercase;}
/* مؤشرات حالة الـ AI */
.ai-dots{display:flex;gap:5px;align-items:center;}
.ai-dot{
  width:10px;height:10px;border-radius:50%;
  background:#aaa;border:2px solid #888;
  transition:all .5s;position:relative;cursor:default;flex-shrink:0;
}
.ai-dot.ok{
  background:#22c55e;border-color:#16a34a;
  box-shadow:0 0 8px rgba(34,197,94,1);
}
.ai-dot.ok::after{
  content:'';position:absolute;inset:-4px;border-radius:50%;
  border:2px solid rgba(34,197,94,0.4);
  animation:dot-pulse 1.8s ease-in-out infinite;
}
.ai-dot.error{background:#ef4444;border-color:#dc2626;box-shadow:0 0 6px rgba(239,68,68,0.8);}
.ai-dot.no_key{background:#d1d5db;border-color:#9ca3af;}
@keyframes dot-pulse{0%,100%{transform:scale(1);opacity:0.7;}50%{transform:scale(1.7);opacity:0;}}
/* الصف الثاني — الأدوات */
.header-tools-row{
  display:flex;align-items:center;justify-content:space-between;
  padding:7px 14px;gap:6px;
}
.brand{display:none;}
.brand-text{display:none;}
.header-top{display:none;}
.header-actions{display:contents;}
.theme-btn{
  width:30px;height:30px;border-radius:50%;border:1px solid var(--border);
  cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;
  background:var(--glass);transition:.2s;flex-shrink:0;
}
.theme-btn:hover{transform:scale(1.1);}
.header-badge-btn{
  height:28px;padding:0 9px;border-radius:14px;border:none;
  background:rgba(245,200,66,0.18);color:#a07010;
  font-family:'Tajawal',sans-serif;font-size:12px;font-weight:800;
  cursor:pointer;display:flex;align-items:center;gap:4px;
  transition:.2s;flex-shrink:0;
}
.header-badge-btn.debt{background:rgba(232,121,138,0.15);color:var(--accent2);}
.header-badge-btn:hover{transform:scale(1.05);}

/* ── بطاقة التحليل الذكي ── */
.insights-card{
  margin:14px 0 0;border-radius:20px;overflow:hidden;
  border:1px solid var(--border);
  box-shadow:0 4px 20px var(--shadow);
  animation:fadeUp .6s ease both;
}
.insights-header{
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  padding:11px 16px;display:flex;align-items:center;gap:8px;
}
.insights-header-icon{font-size:18px;}
.insights-header-title{font-size:13px;font-weight:800;color:#fff;letter-spacing:.5px;}
.insights-header-badge{
  margin-right:auto;font-size:10px;font-weight:700;
  background:rgba(255,255,255,0.25);color:#fff;
  padding:2px 8px;border-radius:20px;
}
.insights-sections{background:var(--card);}
.insights-section{
  padding:14px 16px;border-bottom:1px solid var(--border);
}
.insights-section:last-child{border-bottom:none;}
.insights-section-label{
  font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  color:var(--text3);margin-bottom:7px;display:flex;align-items:center;gap:5px;
}
.insights-section-label span{
  background:var(--accent-glow);color:var(--accent2);
  padding:2px 7px;border-radius:8px;
}
.insights-text{
  font-size:14px;line-height:1.75;color:var(--text);font-weight:400;
}
.insights-loading{
  padding:20px 16px;text-align:center;color:var(--text3);font-size:13px;
}
.insights-skeleton{
  height:13px;background:linear-gradient(90deg,var(--border) 25%,var(--bg2) 50%,var(--border) 75%);
  background-size:200% 100%;animation:skl-shine 1.2s infinite;border-radius:6px;margin:6px 0;
}
.insights-skeleton.w80{width:80%;}
.insights-skeleton.w60{width:60%;}
.insights-skeleton.w90{width:90%;}

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
.theme-panel h4{font-size:12px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;text-align:center;}
.themes-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.th-opt{
  display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;
  padding:8px 4px;border-radius:10px;border:2px solid transparent;transition:.2s;
}
.th-opt:hover,.th-opt.active{background:rgba(255,255,255,0.1);border-color:var(--accent);}
.th-circle{width:32px;height:32px;border-radius:50%;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,0.2);}
.th-name{font-size:11px;color:var(--text3);font-weight:600;white-space:nowrap;}

/* Reports UI */
.rpt-type-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;}
.rpt-type-btn{padding:12px;border:2px solid var(--border);border-radius:12px;background:var(--card);color:var(--text2);font-family:'Tajawal',sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:.2s;}
.rpt-type-btn.active{border-color:var(--accent);background:rgba(var(--accent-rgb,200,100,110),.1);color:var(--accent);}
.rpt-picker{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px;margin-bottom:14px;}
.rpt-day-label{text-align:center;font-size:14px;color:var(--text3);margin-top:8px;}
input[type="date"]{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg2);color:var(--text1);font-family:'Tajawal',sans-serif;font-size:15px;}

/* Daily KPI */
.day-section{margin-bottom:16px;}
.day-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
.day-title{font-size:13px;font-weight:800;color:var(--text2);}
.day-date{font-size:13px;color:var(--text3);}
.day-chart-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:14px;margin-bottom:12px;}
.day-chart-card h3{font-size:14px;color:var(--text3);margin:0 0 10px;font-weight:600;}

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
.slbl{font-size:11px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;
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
.kpi-ico{font-size:26px;margin-bottom:8px;}
.kpi-lbl{font-size:12px;color:var(--text3);margin-bottom:3px;}
.kpi-val{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;line-height:1;margin-bottom:4px;color:var(--accent);}
.kpi.green .kpi-val{color:var(--green2);}
.kpi.gold .kpi-val{color:var(--gold);}
.kpi-sub{font-size:11px;color:var(--text3);}
.badge{padding:3px 8px;border-radius:20px;font-size:11px;font-weight:700;}
.bp{background:rgba(90,138,106,.15);color:var(--green2);}
.bn{background:rgba(232,121,138,.15);color:var(--accent);}
.chips{display:flex;gap:3px;margin-top:6px;flex-wrap:wrap;}
.chip{padding:3px 7px;border-radius:10px;font-size:11px;font-weight:600;
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
.fld label{font-size:13px;font-weight:700;color:var(--text3);letter-spacing:.5px;}
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
.ptitle{font-size:14px;font-weight:700;color:var(--accent);}
.pb-title .ptitle{color:var(--green2);}
.pcnt{font-size:11px;font-weight:800;padding:2px 8px;border-radius:12px;
  background:rgba(255,255,255,0.5);color:var(--text2);}
.pbody{padding:6px;flex:1;overflow-y:auto;max-height:240px;
  scrollbar-width:thin;scrollbar-color:var(--border) transparent;}

.empty{padding:24px;text-align:center;color:var(--text3);}
.empty .ei{font-size:28px;margin-bottom:6px;opacity:0.3;}
.empty p{font-size:13px;line-height:1.8;}
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
.edesc{font-size:14px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.emeta{display:flex;gap:3px;margin-top:2px;flex-wrap:wrap;align-items:center;}
.edate{font-size:11px;color:var(--text3);}
.epb{font-size:11px;font-weight:700;padding:2px 6px;border-radius:7px;
  background:rgba(255,255,255,0.5);color:var(--text2);}
.eamt{font-family:'Playfair Display',serif;font-size:15px;font-weight:700;white-space:nowrap;flex-shrink:0;color:var(--green2);}
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
.exp-name{font-size:14px;font-weight:700;color:var(--text);}
.exp-last{font-size:11px;color:var(--text3);margin-top:2px;}
.exp-amt{font-family:'Playfair Display',serif;font-size:16px;font-weight:700;color:var(--accent2);flex-shrink:0;}
.exp-pay-btn{background:linear-gradient(135deg,var(--green),var(--green2));border:none;
  border-radius:8px;color:white;font-size:13px;font-weight:700;padding:7px 12px;
  cursor:pointer;font-family:'Tajawal',sans-serif;transition:.2s;flex-shrink:0;white-space:nowrap;}
.exp-pay-btn.paid{background:rgba(90,138,106,.15);color:var(--green2);box-shadow:none;}

/* ══════════════════════════════════════════
   CHARTS — Stacked on mobile
══════════════════════════════════════════ */
.charts-col{display:flex;flex-direction:column;gap:12px;margin-bottom:16px;}
.chart-card{padding:16px;}
.chart-card h3{font-size:14px;font-weight:700;color:var(--text2);margin-bottom:12px;display:flex;align-items:center;gap:6px;}

/* ══════════════════════════════════════════
   SHELVES — Mobile Cards
══════════════════════════════════════════ */
.shelf-summary{display:flex;flex-direction:column;gap:10px;margin-bottom:16px;}
.shelf-kpi{padding:14px;position:relative;overflow:hidden;animation:fadeUp .5s ease both;}
.shelf-kpi-bar{position:absolute;top:0;right:0;left:0;height:3px;border-radius:18px 18px 0 0;}
.shelf-kpi-name{font-size:15px;font-weight:800;margin-bottom:10px;
  display:flex;align-items:center;gap:7px;color:var(--text);}
.shelf-dot{width:8px;height:8px;border-radius:50%;}
.shelf-kpi-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.skv{text-align:center;padding:7px;background:rgba(255,255,255,0.4);border-radius:8px;}
.skv .v{font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:var(--text);}
.skv .l{font-size:11px;color:var(--text3);margin-top:2px;}
.shelf-net{margin-top:9px;padding:8px 10px;border-radius:9px;
  display:flex;justify-content:space-between;align-items:center;}
.shelf-net-pos{background:rgba(90,138,106,.1);border:1px solid rgba(90,138,106,.2);}
.shelf-net-neg{background:rgba(232,121,138,.08);border:1px solid var(--border);}
.shelf-net .nl{font-size:11px;color:var(--text3);}
.shelf-net .nv{font-family:'Playfair Display',serif;font-size:16px;font-weight:700;}
.rent-btn{background:rgba(255,255,255,0.4);border:1px solid var(--border);border-radius:7px;
  color:var(--text3);font-size:9px;font-family:'Tajawal',sans-serif;padding:4px 9px;
  cursor:pointer;transition:.2s;margin-top:7px;width:100%;}
.shelf-prods-section{display:flex;flex-direction:column;gap:10px;}
.shelf-prod-card{overflow:hidden;}
.sp-head{padding:12px 14px;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);}
.sp-name{font-size:14px;font-weight:700;display:flex;align-items:center;gap:6px;color:var(--text);}
.sp-count{font-size:11px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(255,255,255,0.5);}
.sp-body{padding:5px;max-height:200px;overflow-y:auto;scrollbar-width:thin;}
.prod-row{display:flex;align-items:center;gap:7px;padding:8px 5px;border-radius:8px;
  border-bottom:1px solid rgba(255,255,255,0.3);transition:.2s;}
.prod-row:last-child{border-bottom:none;}
.prod-row:active{background:rgba(255,255,255,0.4);}
.prod-ph{width:30px;height:30px;border-radius:7px;background:rgba(255,255,255,0.5);
  border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.prod-info{flex:1;min-width:0;}
.prod-name{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.prod-price{font-size:11px;color:var(--text3);margin-top:1px;}
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
  padding:11px 22px;border-radius:40px;font-size:14px;font-weight:600;
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
  .header-top{padding:10px 24px;min-height:66px;}
  .emblem{width:44px;height:44px;font-size:21px;border-radius:14px;}
  .bname{font-size:19px;}
  .bsub{font-size:11px;}
  .ticker-text{font-size:14px;}
  .page{padding:24px 20px 60px;max-width:1100px;margin:0 auto;}
  .kpi-row.row2{grid-template-columns:1fr 1fr;}
  .kpi-row.row3{grid-template-columns:repeat(3,1fr);}
  .kpi-lbl{font-size:13px;}
  .kpi-val{font-size:24px;}
  .kpi-sub{font-size:12px;}
  .panels{flex-direction:row;}
  .panel{flex:1;}
  .ptitle{font-size:15px;}
  .edesc{font-size:15px;}
  .eamt{font-size:16px;}
  .edate{font-size:12px;}
  .charts-col{display:grid;grid-template-columns:2fr 1fr 1fr;flex-direction:unset;}
  .chart-card h3{font-size:15px;}
  .shelf-summary{display:grid;grid-template-columns:repeat(2,1fr);}
  .shelf-prods-section{display:grid;grid-template-columns:repeat(2,1fr);}
  .shelf-kpi-name{font-size:16px;}
  .skv .v{font-size:16px;}
  .skv .l{font-size:12px;}
  .shelf-net .nl{font-size:12px;}
  .shelf-net .nv{font-size:18px;}
  .prod-name{font-size:14px;}
  .prod-price{font-size:12px;}
  .qty-badge{font-size:13px;}
  .sell-btn{font-size:13px;}
  .exp-name{font-size:15px;}
  .exp-last{font-size:12px;}
  .exp-amt{font-size:17px;}
  .reports-grid{grid-template-columns:repeat(4,1fr);}
  .rpt-btn{font-size:14px;}
  .overlay{align-items:center;padding:20px;}
  .modal{border-radius:22px;max-height:90vh;}
  .modal h3{font-size:20px;}
  .modal p{font-size:15px;}
  .modal-handle{display:none;}
  #flowerPanel{align-items:center;}
  .flower-sheet{border-radius:22px;max-height:80vh;}
  .fgrid.fg2{flex-direction:row;}
  .fgrid.fg3{flex-direction:row;}
  .fgrid.fg2 .fld,.fgrid.fg3 .fld{flex:1;}
  .fld label{font-size:14px;}
  .mtab{font-size:15px;padding:11px 18px;}
  .slbl{font-size:12px;}
  .badge{font-size:12px;}
  .chip{font-size:12px;}
  .toast{bottom:28px;}
}
@media(min-width:1200px){
  .bname{font-size:21px;}
  .kpi-lbl{font-size:14px;}
  .kpi-val{font-size:26px;}
  .edesc{font-size:16px;}
  .eamt{font-size:17px;}
  .ptitle{font-size:16px;}
  .shelf-kpi-name{font-size:17px;}
  .skv .v{font-size:17px;}
  .exp-amt{font-size:18px;}
  .chart-card h3{font-size:16px;}
}
/* ── Customer & Catalog cards ── */
.cust-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px;position:relative;}
.cust-card-name{font-size:15px;font-weight:800;color:var(--text);}
.cust-card-sub{font-size:12px;color:var(--text3);margin-top:3px;}
.cust-card-actions{display:flex;gap:6px;margin-top:10px;}
.cust-btn{padding:6px 12px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text2);font-family:'Tajawal',sans-serif;font-size:12px;cursor:pointer;}
.cust-btn.red{color:var(--accent);border-color:rgba(232,121,138,.3);}
.debt-card{background:linear-gradient(135deg,rgba(232,121,138,.08),rgba(255,255,255,.4));border:1px solid rgba(232,121,138,.25);border-radius:12px;padding:12px;}
.debt-amt{font-size:18px;font-weight:900;color:var(--accent);}
.cat-prod-card{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;}
.cat-prod-img{width:100%;height:120px;object-fit:cover;background:var(--bg2);}
.cat-prod-img-placeholder{width:100%;height:120px;background:linear-gradient(135deg,var(--bg2),var(--border));display:flex;align-items:center;justify-content:center;font-size:36px;}
.cat-prod-info{padding:10px;}
.cat-prod-name{font-size:13px;font-weight:800;color:var(--text);}
.cat-prod-price{font-size:15px;font-weight:900;color:var(--green2);margin-top:3px;}
.cat-prod-desc{font-size:11px;color:var(--text3);margin-top:3px;}
.cat-prod-actions{display:flex;gap:4px;padding:8px;border-top:1px solid var(--border);}
.cat-toggle{padding:5px 10px;border:1px solid var(--border);border-radius:6px;font-size:11px;cursor:pointer;background:transparent;color:var(--text3);font-family:'Tajawal',sans-serif;}
.cat-del{padding:5px 10px;border:1px solid rgba(232,121,138,.3);border-radius:6px;font-size:11px;cursor:pointer;background:transparent;color:var(--accent);font-family:'Tajawal',sans-serif;}
.cat-unavail{opacity:0.4;}
/* Orders */
.order-card{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;}
.order-card.done{opacity:0.6;border-style:dashed;}
.order-img{width:100%;max-height:200px;object-fit:cover;cursor:pointer;display:block;}
.order-body{padding:12px;}
.order-id{font-size:10px;font-weight:800;color:var(--text3);letter-spacing:1px;}
.order-name{font-size:15px;font-weight:800;color:var(--text);margin-top:2px;}
.order-desc{font-size:13px;color:var(--text2);margin-top:4px;line-height:1.5;}
.order-meta{font-size:11px;color:var(--text3);margin-top:6px;display:flex;gap:10px;flex-wrap:wrap;}
.order-price{font-size:14px;font-weight:700;color:var(--green2);margin-top:4px;}
.order-actions{display:flex;gap:6px;padding:10px 12px;border-top:1px solid var(--border);background:var(--bg2);}
.ord-btn{flex:1;padding:7px;border:none;border-radius:8px;font-family:'Tajawal',sans-serif;font-size:12px;font-weight:700;cursor:pointer;}
.ord-btn.done{background:var(--green);color:#fff;}
.ord-btn.edit{background:rgba(212,168,67,.15);color:var(--gold);border:1px solid rgba(212,168,67,.3);}
.ord-btn.del{background:rgba(232,121,138,.1);color:var(--accent);border:1px solid rgba(232,121,138,.25);}
.ord-status-badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;}
.ord-status-pending{background:rgba(245,200,66,.2);color:#b8880a;}
.ord-status-done{background:rgba(122,171,138,.2);color:var(--green2);}
.ord-status-cancelled{background:rgba(232,121,138,.2);color:var(--accent);}
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

  <div class="header-frame">
    <div class="header-inner">

      <!-- الصف العلوي: اسم المحل في المنتصف -->
      <div class="header-brand-row">
        <div class="header-corner">
          <div id="flowerPill" onclick="toggleFlowerPanel()">
            <span>🌸</span>
            <span id="flowerCount">0</span>
          </div>
        </div>
        <div class="brand-center">
          <div class="emblem">🌹</div>
          <div class="brand-titles">
            <div class="bname">فيروز فلورز</div>
            <div class="bsub">إدارة المبيعات</div>
          </div>
        </div>
        <div class="header-corner-r">
          <div class="ai-dots" id="aiDots" title="حالة الذكاء الاصطناعي">
            <div class="ai-dot no_key" id="dot-groq" title="Groq"></div>
            <div class="ai-dot no_key" id="dot-gemini" title="Gemini"></div>
            <div class="ai-dot no_key" id="dot-openrouter" title="OpenRouter"></div>
            <div class="ai-dot no_key" id="dot-openai" title="OpenAI"></div>
          </div>
          <a href="/logout" class="logout-btn" title="خروج">🔒</a>
        </div>
      </div>

      <!-- الصف الثاني: الأدوات -->
      <div class="header-tools-row">
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
        <button class="header-badge-btn" id="hdrOrders" onclick="switchTab('customers')" title="الطلبات قيد الانتظار" style="display:none;">
          📋 <span id="hdrOrdersCount">0</span>
        </button>
        <button class="header-badge-btn debt" id="hdrDebts" onclick="switchTab('customers')" title="الديون غير المسددة" style="display:none;">
          💳 <span id="hdrDebtsCount">0</span>
        </button>
      </div>

    </div><!-- /header-inner -->
  </div><!-- /header-frame -->

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

  <!-- Background Image Upload Section -->
  <div class="theme-panel" id="bgPanel" style="display:none;margin-top:12px;">
    <h4>تغيير خلفية التطبيق</h4>
    <div style="padding:12px 0;">
      <input type="file" id="bgFileInput" accept="image/*" style="display:none;" onchange="uploadBackground(event)"/>
      <button class="login-btn" onclick="document.getElementById('bgFileInput').click()" style="width:100%;margin-bottom:8px;background:linear-gradient(135deg,#d4a843,#c49030);color:#1a1208;border:none;padding:12px;border-radius:8px;font-family:'Tajawal',sans-serif;font-weight:700;cursor:pointer;">📁 اختر صورة</button>
      <div id="bgStatus" style="font-size:12px;text-align:center;margin-top:8px;color:rgba(255,255,255,0.7);"></div>
    </div>
  </div>


  <!-- Nav Tabs -->
  <div class="mobile-tabs" style="margin-top:8px;padding-bottom:6px;">
    <button class="mtab on" onclick="switchTab('home')">📊 الرئيسية</button>
    <button class="mtab" onclick="switchTab('shelves')">🗄️ الرفوف</button>
    <button class="mtab" onclick="switchTab('customers')">👥 العملاء</button>
    <button class="mtab" onclick="switchTab('catalog')">📷 الكتالوج</button>
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

  <!-- ── الهدف اليومي ── -->
  <div class="gc" id="goalCard" style="padding:14px 16px;margin-bottom:12px;display:none;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
      <span style="font-size:13px;font-weight:800;color:var(--text2);">🎯 الهدف اليومي</span>
      <button onclick="editGoal()" style="font-size:11px;padding:4px 10px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--text3);cursor:pointer;">تعديل</button>
    </div>
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
      <span id="goalCurrentVal" style="font-size:20px;font-weight:900;color:var(--green2);">0</span>
      <span style="font-size:13px;color:var(--text3);">من</span>
      <span id="goalTargetVal" style="font-size:16px;font-weight:700;color:var(--text2);">50</span>
      <span style="font-size:11px;color:var(--text3);">ر.ع</span>
      <span id="goalStatusEmoji" style="font-size:16px;margin-right:auto;">⏳</span>
    </div>
    <div style="background:var(--border);border-radius:20px;height:10px;overflow:hidden;">
      <div id="goalProgressBar" style="height:100%;border-radius:20px;background:linear-gradient(90deg,var(--green),var(--gold));width:0%;transition:width 0.6s ease;"></div>
    </div>
    <div id="goalCaption" style="font-size:11px;color:var(--text3);margin-top:5px;text-align:center;"></div>
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

  <!-- ── بطاقة التحليل الذكي ── -->
  <div class="insights-card" id="insightsCard">
    <div class="insights-header">
      <span class="insights-header-icon">🤖</span>
      <span class="insights-header-title">تحليل اليوم والنصائح</span>
      <span class="insights-header-badge" id="insightsBadge">جاري التحليل...</span>
    </div>
    <div class="insights-sections" id="insightsSections">
      <div class="insights-section">
        <div class="insights-section-label"><span>📊 تحليل أداء اليوم</span></div>
        <div class="insights-text" style="color:var(--text3);font-style:italic;">⏳ جاري تحليل مبيعات اليوم...</div>
      </div>
      <div class="insights-section">
        <div class="insights-section-label"><span>💡 نصائح لزيادة المبيعات</span></div>
        <div class="insights-text" style="color:var(--text3);font-style:italic;">⏳ جاري تحضير النصائح المخصصة...</div>
      </div>
      <div class="insights-section">
        <div class="insights-section-label"><span>🗓️ المناسبات القادمة في عُمان</span></div>
        <div class="insights-text" style="color:var(--text3);font-style:italic;">⏳ جاري البحث عن المناسبات القريبة...</div>
      </div>
    </div>
  </div>

  <!-- ── ملخص فواتير الورد ── -->
  <div id="shelfSummaryCard" style="display:none;"></div>
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

<!-- CUSTOMERS -->
<div id="tab-customers" class="page">
  <div class="slbl">العملاء الدائمون</div>

  <!-- Search + Add -->
  <div class="gc" style="padding:14px;margin-bottom:14px;">
    <div style="display:flex;gap:8px;margin-bottom:12px;">
      <input id="custSearch" type="text" placeholder="🔍 ابحث باسم أو رقم..." oninput="searchCustomers()"
        style="flex:1;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg2);color:var(--text);font-family:'Tajawal',sans-serif;font-size:14px;"/>
      <button onclick="showAddCustomer()" style="padding:10px 14px;background:var(--accent);color:#fff;border:none;border-radius:10px;cursor:pointer;font-size:16px;">➕</button>
    </div>
    <!-- Add form (hidden by default) -->
    <div id="addCustForm" style="display:none;border-top:1px solid var(--border);padding-top:12px;">
      <div class="fgrid fg2">
        <div class="fld"><label>الاسم *</label><input id="custName" type="text" placeholder="اسم العميل"/></div>
        <div class="fld"><label>الهاتف</label><input id="custPhone" type="tel" placeholder="9XXXXXXXX"/></div>
      </div>
      <div class="fld"><label>ملاحظات / ماذا يشتري عادةً</label>
        <input id="custNotes" type="text" placeholder="مثال: يحب الورد الأحمر، يطلب باقات أسبوعياً"/></div>
      <div style="display:flex;gap:8px;margin-top:10px;">
        <button onclick="addCustomer()" class="sbtn sb-s" style="flex:1;padding:10px;">💾 حفظ</button>
        <button onclick="hideAddCustomer()" style="padding:10px 16px;border:1px solid var(--border);border-radius:10px;background:transparent;color:var(--text2);cursor:pointer;">إلغاء</button>
      </div>
    </div>
  </div>

  <!-- Customers list -->
  <div id="custList" style="display:flex;flex-direction:column;gap:10px;"></div>

  <!-- Orders section -->
  <div class="slbl" style="margin-top:16px;">📋 الطلبات قيد الانتظار</div>
  <div class="gc" style="padding:14px;margin-bottom:12px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
      <span id="pendingOrdersLabel" style="font-size:13px;color:var(--text3);">لا توجد طلبات</span>
      <button onclick="showAddOrder()" style="font-size:12px;padding:6px 12px;background:var(--accent);color:#fff;border:none;border-radius:8px;cursor:pointer;">+ طلب جديد</button>
    </div>
    <!-- Add order form -->
    <div id="addOrderForm" style="display:none;border-top:1px solid var(--border);padding-top:12px;margin-bottom:12px;">
      <div class="fgrid fg2">
        <div class="fld"><label>اسم العميل *</label><input id="orderCustName" type="text" placeholder="أم خالد..."/></div>
        <div class="fld"><label>الهاتف</label><input id="orderCustPhone" type="tel" placeholder="اختياري"/></div>
      </div>
      <div class="fld"><label>وصف الطلب *</label>
        <input id="orderDesc" type="text" placeholder="باقة ورد أحمر كبيرة، تاج عروس..."/></div>
      <div class="fgrid fg2">
        <div class="fld"><label>السعر (ر.ع)</label><input id="orderPrice" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/></div>
        <div class="fld"><label>ملاحظات</label><input id="orderNotes" type="text" placeholder="اختياري..."/></div>
      </div>
      <div style="display:flex;gap:8px;margin-top:10px;">
        <button onclick="addOrder()" class="sbtn sb-s" style="flex:1;padding:10px;">💾 حفظ الطلب</button>
        <button onclick="document.getElementById('addOrderForm').style.display='none'" style="padding:10px 16px;border:1px solid var(--border);border-radius:10px;background:transparent;color:var(--text2);cursor:pointer;">إلغاء</button>
      </div>
    </div>
    <!-- Filter tabs -->
    <div style="display:flex;gap:6px;margin-bottom:10px;">
      <button onclick="loadOrders('pending')" id="ord-f-pending" style="padding:5px 12px;border-radius:20px;border:1px solid var(--accent);background:var(--accent);color:#fff;font-family:'Tajawal',sans-serif;font-size:12px;cursor:pointer;">⏳ قيد الانتظار</button>
      <button onclick="loadOrders('done')"    id="ord-f-done"    style="padding:5px 12px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--text3);font-family:'Tajawal',sans-serif;font-size:12px;cursor:pointer;">✅ منجزة</button>
      <button onclick="loadOrders('')"        id="ord-f-all"     style="padding:5px 12px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--text3);font-family:'Tajawal',sans-serif;font-size:12px;cursor:pointer;">📋 الكل</button>
    </div>
    <div id="ordersList" style="display:flex;flex-direction:column;gap:10px;"></div>
  </div>

  <!-- Debts section -->
  <div class="slbl" style="margin-top:16px;">💳 الديون غير المسددة</div>
  <div class="gc" style="padding:14px;margin-bottom:12px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
      <span id="totalDebtLabel" style="font-size:13px;color:var(--text3);">إجمالي: 0.000 ر.ع</span>
      <button onclick="showAddDebt()" style="font-size:12px;padding:6px 12px;background:var(--accent);color:#fff;border:none;border-radius:8px;cursor:pointer;">+ دين جديد</button>
    </div>
    <!-- Add debt form -->
    <div id="addDebtForm" style="display:none;border-top:1px solid var(--border);padding-top:12px;margin-bottom:12px;">
      <div class="fgrid fg2">
        <div class="fld"><label>اسم العميل *</label><input id="debtName" type="text" placeholder="اسم من يدين"/></div>
        <div class="fld"><label>المبلغ (ر.ع) *</label><input id="debtAmt" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/></div>
      </div>
      <div class="fgrid fg2">
        <div class="fld"><label>الهاتف</label><input id="debtPhone" type="tel" placeholder="اختياري"/></div>
        <div class="fld"><label>الوصف</label><input id="debtDesc" type="text" placeholder="ما اشتراه..."/></div>
      </div>
      <div style="display:flex;gap:8px;margin-top:10px;">
        <button onclick="addDebt()" class="sbtn sb-s" style="flex:1;padding:10px;">💾 حفظ</button>
        <button onclick="document.getElementById('addDebtForm').style.display='none'" style="padding:10px 16px;border:1px solid var(--border);border-radius:10px;background:transparent;color:var(--text2);cursor:pointer;">إلغاء</button>
      </div>
    </div>
    <div id="debtList" style="display:flex;flex-direction:column;gap:10px;"></div>
  </div>
</div>

<!-- CATALOG -->
<div id="tab-catalog" class="page">
  <div class="slbl">كتالوج المنتجات</div>

  <!-- Add product form -->
  <div class="gc" style="padding:14px;margin-bottom:14px;">
    <div style="font-size:13px;font-weight:800;color:var(--text2);margin-bottom:10px;">➕ إضافة منتج للكتالوج</div>
    <div class="fgrid fg2">
      <div class="fld"><label>اسم المنتج *</label><input id="catName" type="text" placeholder="مثال: باقة ورد رومانسية"/></div>
      <div class="fld"><label>السعر (ر.ع) *</label><input id="catPrice" type="number" placeholder="0.000" step="0.001" inputmode="decimal"/></div>
    </div>
    <div class="fld"><label>وصف المنتج</label>
      <input id="catDesc" type="text" placeholder="مواصفات المنتج، الألوان، المناسبة..."/></div>
    <div class="fld"><label>🔗 رابط الصورة (اختياري)</label>
      <input id="catImg" type="url" placeholder="https://..."/></div>
    <button onclick="addCatalogProduct()" class="sbtn sb-s" style="width:100%;">🌸 إضافة للكتالوج</button>
  </div>

  <!-- Share button -->
  <div style="display:flex;gap:8px;margin-bottom:14px;">
    <button onclick="shareCatalog()" style="flex:1;padding:12px;background:linear-gradient(135deg,#25d366,#128c7e);color:#fff;border:none;border-radius:12px;font-family:'Tajawal',sans-serif;font-size:14px;font-weight:700;cursor:pointer;">📲 مشاركة الكتالوج عبر واتساب</button>
  </div>

  <!-- Products grid -->
  <div id="catalogGrid" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;"></div>
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

function toggleBgPanel(){
  document.getElementById('bgPanel').classList.toggle('open');
}

async function uploadBackground(event){
  const file = event.target.files[0];
  if(!file) return;
  
  const statusEl = document.getElementById('bgStatus');
  statusEl.textContent = 'جارٍ التحميل...';
  statusEl.style.color = 'rgba(255,255,255,0.7)';
  
  const formData = new FormData();
  formData.append('file', file);
  
  try{
    const response = await fetch('/upload-background', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    if(data.ok){
      statusEl.textContent = '✓ تم تحديث الخلفية بنجاح';
      statusEl.style.color = '#7aab8a';
      document.getElementById('bgFileInput').value = '';
      setTimeout(() => {
        document.getElementById('bgFileInput').value = '';
      }, 2000);
    } else {
      statusEl.textContent = '✗ خطأ: ' + (data.error || 'فشل التحميل');
      statusEl.style.color = '#ffb3b3';
    }
  } catch(e){
    statusEl.textContent = '✗ خطأ في الاتصال';
    statusEl.style.color = '#ffb3b3';
  }
}


// Init theme
setTheme(currentTheme);
document.addEventListener('click', e => {
  if(!e.target.closest('.theme-btn') && !e.target.closest('.theme-panel')){
    document.getElementById('themePanel').classList.remove('open');
    document.getElementById('bgPanel').classList.remove('open');
  }
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
  if(t==='customers') { loadCustomers(); loadOrders('pending'); loadDebts(); }
  if(t==='catalog') loadCatalog();
}

function setFT(t){
  formTab=t;
  document.getElementById('tt-s').className='ttab'+(t==='s'?' tt-s':'');
  document.getElementById('tt-b').className='ttab'+(t==='b'?' tt-b':'');
  document.getElementById('form-s').style.display=t==='s'?'block':'none';
  document.getElementById('form-b').style.display=t==='b'?'block':'none';
}
(function(){
  const bPayer=document.getElementById('bPayer');
  if(bPayer) bPayer.addEventListener('change',function(){
    const w=document.getElementById('bOtherWrap');
    if(w) w.style.display=this.value==='أخرى'?'block':'none';
  });
})();

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

let _loading=false;
async function load(){
  if(_loading) return;        // منع الاستدعاء المزدوج
  _loading=true;
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
    if(dash.shelves_summary) renderShelfSummaryCard(dash.shelves_summary, dash.shelf_sales||[]);
    try{ loadGoal(); }catch(e2){}
  } catch(e){ hideSkeleton(); console.error('load error', e); }
  finally { _loading=false; }
}

// تحديث تلقائي كل 60 ثانية
setInterval(()=>{load();if(document.getElementById('tab-shelves').classList.contains('active'))loadShelves();try{loadHeaderBadges();}catch(e){}},60000);

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

/* ── SHELF SUMMARY CARD ── */
function renderShelfSummaryCard(shelvesSummary, shelfSales){
  const el = document.getElementById('shelfSummaryCard');
  if(!el) return;
  const totalShelf = shelvesSummary.reduce((a,s)=>a+s.total,0);
  if(totalShelf === 0 && shelvesSummary.every(s=>s.count===0)){
    el.style.display='none'; return;
  }
  el.style.display='block';
  const rows = shelvesSummary.filter(s=>s.total>0||s.count>0).map(s=>`
    <div style="display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--border);">
      <div style="display:flex;align-items:center;gap:7px;">
        <div style="width:10px;height:10px;border-radius:50%;background:${s.color};flex-shrink:0;"></div>
        <span style="font-size:14px;font-weight:700;color:var(--text);">رف ${s.name}</span>
        <span style="font-size:11px;color:var(--text3);">(${s.count} عملية)</span>
      </div>
      <span style="font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:var(--green2);">${fmt(s.total)} ر.ع</span>
    </div>`).join('');
  el.innerHTML=`
    <div class="gc" style="padding:14px;margin-bottom:14px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
        <div style="font-size:12px;font-weight:700;color:var(--text3);letter-spacing:2px;text-transform:uppercase;">🗄️ مبيعات الرفوف</div>
        <span style="font-family:'Playfair Display',serif;font-size:16px;font-weight:800;color:var(--accent2);">${fmt(totalShelf)} ر.ع</span>
      </div>
      ${rows||'<div style="color:var(--text3);font-size:13px;text-align:center;padding:8px;">لا توجد مبيعات الرفوف هذا الشهر</div>'}
    </div>`;
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
async function delShelfSale(eid){
  if(!confirm('حذف هذه المبيعة؟')) return;
  await api(`/api/entries/${eid}`,{method:'DELETE'});
  showToast('🗑️ تم الحذف'); loadShelves(); load();
}
async function editShelfSale(eid, desc, amt){
  const newAmt = prompt(`تعديل سعر "${desc}"\nالسعر الحالي: ${amt} ر.ع\nأدخل السعر الجديد:`, amt);
  if(newAmt === null) return;
  const parsed = parseFloat(newAmt);
  if(isNaN(parsed) || parsed <= 0){ showToast('⚠️ سعر غير صحيح'); return; }
  await api(`/api/entries/${eid}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({amt:parsed})});
  showToast('✅ تم تعديل السعر'); loadShelves(); load();
}

async function loadShelves(){
  const shelves=await api(`/api/shelves?month=${month}`);
  document.getElementById('shelfSummary').innerHTML=shelves.map(s=>{
    const netPos=s.net>=0;
    const entries=s.sales_entries||[];
    const entriesHtml=entries.length?`
      <div style="margin-top:10px;border-top:1px solid var(--border);padding-top:8px;">
        <div style="font-size:11px;font-weight:700;color:var(--text3);letter-spacing:1px;margin-bottom:6px;">📋 المبيعات:</div>
        ${entries.map(e=>{
          const pay=e.payment_method?`<span style="font-size:10px;background:rgba(255,255,255,0.5);border-radius:6px;padding:1px 5px;">${e.payment_method}</span>`:'';
          return `<div style="display:flex;align-items:center;gap:6px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.3);">
            <div style="flex:1;min-width:0;">
              <div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;">
                ${pay}
                <span style="font-size:13px;color:var(--text);">${e.desc}</span>
              </div>
              <span style="font-family:'Playfair Display',serif;font-size:13px;font-weight:700;color:var(--green2);">${fmt(e.amt)} ر.ع</span>
            </div>
            <button onclick="editShelfSale(${e.id},'${e.desc.replace(/'/g,"\\'")}',${e.amt})"
              style="width:28px;height:28px;border:none;border-radius:8px;background:rgba(212,168,67,0.15);color:var(--gold);font-size:13px;cursor:pointer;flex-shrink:0;">✏️</button>
            <button onclick="delShelfSale(${e.id})"
              style="width:28px;height:28px;border:none;border-radius:8px;background:rgba(232,121,138,0.15);color:var(--accent);font-size:13px;cursor:pointer;flex-shrink:0;">🗑</button>
          </div>`;
        }).join('')}
      </div>`:'';
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
      ${entriesHtml}
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
  // Nav tabs (optional — might not exist)
  const ntHome = document.getElementById('nt-home');
  const ntShelves = document.getElementById('nt-shelves');
  const ntReports = document.getElementById('nt-reports');
  if(ntHome) ntHome.textContent = t('home');
  if(ntShelves) ntShelves.textContent = t('shelves');
  if(ntReports) ntReports.textContent = t('reports');
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

/* ── بطاقة التحليل الذكي ── */
function renderInsights(text, badge){
  try{
    const sec = document.getElementById('insightsSections');
    if(!sec) return;
    const parts = text.split('||');
    const labels = [
      {icon:'📊', title:'تحليل أداء اليوم'},
      {icon:'💡', title:'نصائح لزيادة المبيعات'},
      {icon:'🗓️', title:'المناسبات القادمة في عُمان'},
    ];
    let html = '';
    parts.forEach((part, i)=>{
      const lbl = labels[i] || {icon:'✨', title:'ملاحظات'};
      html += '<div class="insights-section">'
        + '<div class="insights-section-label"><span>' + lbl.icon + ' ' + lbl.title + '</span></div>'
        + '<div class="insights-text">' + part.trim() + '</div>'
        + '</div>';
    });
    sec.innerHTML = html;
    const b = document.getElementById('insightsBadge');
    if(b) b.textContent = badge || 'اليوم';
  }catch(err){ console.error('renderInsights error:', err); }
}

async function loadInsights(){
  try{
    const r = await fetch('/api/insights', {credentials:'include'});
    if(r.status === 302 || r.status === 401 || r.redirected){
      renderInsights('⚠️ انتهت جلسة الدخول||أعد تحميل الصفحة أو سجّل دخول من جديد||—', 'خطأ');
      return;
    }
    if(!r.ok){
      renderInsights('⚠️ خطأ في الخادم ('+r.status+')||تحقق من سجلات Render لمعرفة السبب||—', 'خطأ '+r.status);
      return;
    }
    const data = await r.json();
    if(data && data.text){
      const txt = data.text.indexOf('||') !== -1 ? data.text
        : data.text + '||💡 حافظ على التواصل مع عملائك وقدّم عروضاً خاصة في المناسبات.||🗓️ راجع التقويم الرسمي لسلطنة عُمان للمناسبات القادمة.';
      renderInsights(txt, data.fresh ? 'جديد ✨' : 'اليوم');
    }
  }catch(e){
    renderInsights(
      '⚠️ تعذّر الاتصال بالخادم: ' + e.message
      + '||💡 أضف مفتاح Groq أو Gemini مجاناً في إعدادات Render'
      + '||🗓️ بعد إضافة المفتاح أعد تحميل الصفحة',
      'خطأ'
    );
  }
}

/* ── حالة الذكاء الاصطناعي ── */
async function loadAiStatus(){
  try{
    const r = await api('/api/ai-status');
    ['groq','gemini','openrouter','openai'].forEach(name=>{
      const dot = document.getElementById('dot-'+name);
      if(dot) dot.className = 'ai-dot ' + (r[name] || 'no_key');
    });
  }catch(e){}
}

// تحميل البيانات فور اكتمال الصفحة
/* ══════════════════════════════════════════
   HEADER BADGES (orders + debts)
══════════════════════════════════════════ */
async function loadHeaderBadges(){
  try{
    const [ordRes, debtRes] = await Promise.all([
      api('/api/orders?status=pending'),
      api('/api/debts')
    ]);
    const ordCount  = (ordRes.orders || []).length;
    const debtCount = (debtRes.debts || []).length;

    const hdrOrd  = document.getElementById('hdrOrders');
    const hdrDebt = document.getElementById('hdrDebts');
    const ordSpan  = document.getElementById('hdrOrdersCount');
    const debtSpan = document.getElementById('hdrDebtsCount');

    if(hdrOrd && ordSpan){
      ordSpan.textContent = ordCount;
      hdrOrd.style.display = ordCount > 0 ? 'flex' : 'none';
    }
    if(hdrDebt && debtSpan){
      debtSpan.textContent = debtCount;
      hdrDebt.style.display = debtCount > 0 ? 'flex' : 'none';
    }
  }catch(e){}
}

/* ══════════════════════════════════════════
   DAILY GOAL
══════════════════════════════════════════ */
async function loadGoal(){
  try{
    const d = await api('/api/settings/goal');
    const goal = d.goal || 50;
    const today = d.today || 0;
    const pct = Math.min(100, (today/goal)*100);
    const card = document.getElementById('goalCard');
    if(card) card.style.display='block';
    const curEl = document.getElementById('goalCurrentVal');
    const tgtEl = document.getElementById('goalTargetVal');
    const bar   = document.getElementById('goalProgressBar');
    const cap   = document.getElementById('goalCaption');
    const emoji = document.getElementById('goalStatusEmoji');
    if(curEl) curEl.textContent = fmt(today) + ' ر.ع';
    if(tgtEl) tgtEl.textContent = fmt(goal) + ' ر.ع';
    if(bar)   bar.style.width = pct + '%';
    if(pct >= 100){
      if(bar) bar.style.background = 'linear-gradient(90deg,var(--green),#44cc44)';
      if(emoji) emoji.textContent = '🎉';
      if(cap) cap.textContent = 'تجاوزت الهدف! عمل رائع 🏆';
    } else if(pct >= 70){
      if(emoji) emoji.textContent = '💪';
      if(cap) cap.textContent = `باقي ${fmt(goal-today)} ر.ع للوصول للهدف`;
    } else {
      if(emoji) emoji.textContent = '⏳';
      if(cap) cap.textContent = `باقي ${fmt(goal-today)} ر.ع للوصول للهدف`;
    }
  }catch(e){}
}
async function editGoal(){
  const cur = await api('/api/settings/goal');
  const newGoal = prompt('🎯 الهدف اليومي (ر.ع):', cur.goal || 50);
  if(newGoal === null) return;
  const val = parseFloat(newGoal);
  if(isNaN(val) || val <= 0){ showToast('⚠️ أدخل قيمة صحيحة'); return; }
  await api('/api/settings/goal', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({goal:val})});
  showToast('✅ تم تحديث الهدف');
  loadGoal();
}

/* ══════════════════════════════════════════
   ORDERS
══════════════════════════════════════════ */
let _currentOrderFilter = 'pending';
async function loadOrders(status){
  if(status !== undefined) _currentOrderFilter = status;
  // Update filter button styles
  ['pending','done','all'].forEach(f => {
    const btn = document.getElementById('ord-f-'+f);
    if(!btn) return;
    const active = (f === _currentOrderFilter) || (f === 'all' && _currentOrderFilter === '');
    btn.style.background = active ? 'var(--accent)' : 'transparent';
    btn.style.color = active ? '#fff' : 'var(--text3)';
    btn.style.borderColor = active ? 'var(--accent)' : 'var(--border)';
  });
  const url = _currentOrderFilter ? `/api/orders?status=${_currentOrderFilter}` : '/api/orders';
  const d = await api(url);
  const list = d.orders || [];
  const lbl = document.getElementById('pendingOrdersLabel');
  if(lbl){
    const pc = d.pending_count || 0;
    lbl.textContent = pc > 0 ? `${pc} طلب قيد الانتظار` : 'لا توجد طلبات معلقة';
    lbl.style.color = pc > 0 ? 'var(--accent)' : 'var(--text3)';
  }
  const el = document.getElementById('ordersList');
  if(!el) return;
  if(!list.length){
    el.innerHTML = '<div style="text-align:center;color:var(--text3);padding:20px;">لا توجد طلبات 📋</div>';
    return;
  }
  el.innerHTML = list.map(o => {
    const statusMap = {pending:'⏳ قيد الانتظار', done:'✅ منجز', cancelled:'❌ ملغي'};
    const statusClass = {pending:'ord-status-pending', done:'ord-status-done', cancelled:'ord-status-cancelled'};
    const imgHtml = o.img_file_id
      ? `<img class="order-img" src="/api/orders/${o.id}/image" onclick="openOrderImg(this)" loading="lazy"/>`
      : '';
    const priceHtml = o.price && parseFloat(o.price) > 0
      ? `<div class="order-price">💰 ${fmt(o.price)} ر.ع</div>` : '';
    const phoneHtml = o.customer_phone
      ? `<a href="tel:${o.customer_phone}" style="color:var(--accent);text-decoration:none;">📞 ${o.customer_phone}</a>` : '';
    const notesHtml = o.notes ? `<span>📝 ${o.notes}</span>` : '';
    const doneBtn = o.status === 'pending'
      ? `<button class="ord-btn done" onclick="doneOrder(${o.id})">✅ إنجاز</button>` : '';
    const editBtn = `<button class="ord-btn edit" onclick="editOrderPrice(${o.id},${o.price||0})">✏️ سعر</button>`;
    const delBtn  = `<button class="ord-btn del"  onclick="delOrder(${o.id})">🗑️</button>`;
    return `<div class="order-card ${o.status==='done'?'done':''}">
      ${imgHtml}
      <div class="order-body">
        <div style="display:flex;align-items:center;gap:8px;">
          <span class="order-id">طلب #${o.id}</span>
          <span class="ord-status-badge ${statusClass[o.status]||'ord-status-pending'}">${statusMap[o.status]||o.status}</span>
          ${o.source==='bot'?'<span style="font-size:10px;color:var(--text3);">📱 بوت</span>':''}
        </div>
        <div class="order-name">👤 ${o.customer_name}</div>
        <div class="order-desc">${o.description}</div>
        ${priceHtml}
        <div class="order-meta">${phoneHtml}${notesHtml}<span>📅 ${o.date}</span></div>
      </div>
      <div class="order-actions">${doneBtn}${editBtn}${delBtn}</div>
    </div>`;
  }).join('');
}
function openOrderImg(img){
  const overlay = document.createElement('div');
  overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:9999;display:flex;align-items:center;justify-content:center;';
  overlay.onclick = () => overlay.remove();
  const i = document.createElement('img');
  i.src = img.src;
  i.style.cssText = 'max-width:95vw;max-height:90vh;border-radius:12px;object-fit:contain;';
  overlay.appendChild(i);
  document.body.appendChild(overlay);
}
function showAddOrder(){ document.getElementById('addOrderForm').style.display='block'; }
async function addOrder(){
  const name  = document.getElementById('orderCustName').value.trim();
  const phone = document.getElementById('orderCustPhone').value.trim();
  const desc  = document.getElementById('orderDesc').value.trim();
  const price = parseFloat(document.getElementById('orderPrice').value) || 0;
  const notes = document.getElementById('orderNotes').value.trim();
  if(!name){ showToast('⚠️ اسم العميل مطلوب'); return; }
  if(!desc){ showToast('⚠️ وصف الطلب مطلوب'); return; }
  await api('/api/orders',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({customer_name:name,customer_phone:phone,description:desc,price,notes})});
  ['orderCustName','orderCustPhone','orderDesc','orderPrice','orderNotes'].forEach(id=>{
    const el=document.getElementById(id); if(el) el.value='';
  });
  document.getElementById('addOrderForm').style.display='none';
  showToast('✅ تم حفظ الطلب');
  loadOrders();
}
async function doneOrder(id){
  if(!confirm('تأكيد إنجاز هذا الطلب؟')) return;
  await api(`/api/orders/${id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({status:'done'})});
  showToast('✅ تم تسجيل الطلب كمنجز');
  loadOrders();
}
async function editOrderPrice(id, currentPrice){
  const newPrice = prompt('السعر الجديد (ر.ع):', currentPrice || '');
  if(newPrice === null) return;
  const p = parseFloat(newPrice);
  if(isNaN(p) || p < 0){ showToast('⚠️ سعر غير صحيح'); return; }
  await api(`/api/orders/${id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({price:p})});
  showToast('✅ تم تعديل السعر');
  loadOrders();
}
async function delOrder(id){
  if(!confirm('حذف هذا الطلب؟')) return;
  await api(`/api/orders/${id}`,{method:'DELETE'});
  showToast('🗑️ تم الحذف');
  loadOrders();
}

/* ══════════════════════════════════════════
   CUSTOMERS
══════════════════════════════════════════ */
let _customers = [];
async function loadCustomers(){
  const q = document.getElementById('custSearch') ? document.getElementById('custSearch').value : '';
  const url = q ? `/api/customers?q=${encodeURIComponent(q)}` : '/api/customers';
  _customers = await api(url);
  renderCustomers(_customers);
}
function renderCustomers(list){
  const el = document.getElementById('custList');
  if(!el) return;
  if(!list || !list.length){ el.innerHTML='<div style="text-align:center;color:var(--text3);padding:20px;">لا يوجد عملاء مسجلون بعد 👥</div>'; return; }
  el.innerHTML = list.map(c => `
    <div class="cust-card">
      <div class="cust-card-name">👤 ${c.name}</div>
      ${c.phone ? `<div class="cust-card-sub">📞 <a href="tel:${c.phone}" style="color:var(--accent);text-decoration:none;">${c.phone}</a></div>` : ''}
      ${c.notes ? `<div class="cust-card-sub" style="margin-top:4px;">📝 ${c.notes}</div>` : ''}
      ${c.last_purchase ? `<div class="cust-card-sub" style="margin-top:2px;">🛍️ آخر شراء: ${c.last_purchase}</div>` : ''}
      <div class="cust-card-actions">
        ${c.phone ? `<button class="cust-btn" onclick="window.open('https://wa.me/968${c.phone.replace(/^0+/,'')}','_blank')">📲 واتساب</button>` : ''}
        <button class="cust-btn" onclick="editCustomer(${c.id},'${encodeURIComponent(c.name)}','${encodeURIComponent(c.phone||'')}','${encodeURIComponent(c.notes||'')}')">✏️ تعديل</button>
        <button class="cust-btn red" onclick="delCustomer(${c.id})">🗑️</button>
      </div>
    </div>`).join('');
}
function searchCustomers(){ loadCustomers(); }
function showAddCustomer(){ document.getElementById('addCustForm').style.display='block'; }
function hideAddCustomer(){ document.getElementById('addCustForm').style.display='none'; }
async function addCustomer(){
  const name = document.getElementById('custName').value.trim();
  const phone = document.getElementById('custPhone').value.trim();
  const notes = document.getElementById('custNotes').value.trim();
  if(!name){ showToast('⚠️ الاسم مطلوب'); return; }
  await api('/api/customers', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name,phone,notes})});
  document.getElementById('custName').value='';
  document.getElementById('custPhone').value='';
  document.getElementById('custNotes').value='';
  hideAddCustomer();
  showToast('✅ تم إضافة العميل');
  loadCustomers();
}
async function editCustomer(id, encName, encPhone, encNotes){
  const name = decodeURIComponent(encName);
  const phone = decodeURIComponent(encPhone);
  const notes = decodeURIComponent(encNotes);
  const newName = prompt('الاسم:', name);
  if(newName === null) return;
  const newPhone = prompt('الهاتف:', phone);
  if(newPhone === null) return;
  const newNotes = prompt('ملاحظات:', notes);
  if(newNotes === null) return;
  await api(`/api/customers/${id}`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name:newName,phone:newPhone,notes:newNotes})});
  showToast('✅ تم التعديل');
  loadCustomers();
}
async function delCustomer(id){
  if(!confirm('حذف هذا العميل؟')) return;
  await api(`/api/customers/${id}`, {method:'DELETE'});
  showToast('🗑️ تم الحذف');
  loadCustomers();
}

/* ══════════════════════════════════════════
   DEBTS
══════════════════════════════════════════ */
async function loadDebts(){
  const d = await api('/api/debts');
  const list = d.debts || [];
  const total = d.total_unpaid || 0;
  const lbl = document.getElementById('totalDebtLabel');
  if(lbl) lbl.textContent = `إجمالي الديون: ${fmt(total)} ر.ع`;
  const el = document.getElementById('debtList');
  if(!el) return;
  if(!list.length){ el.innerHTML='<div style="text-align:center;color:var(--text3);padding:16px;">✅ لا توجد ديون غير مسددة</div>'; return; }
  el.innerHTML = list.map(d => `
    <div class="debt-card">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;">
        <div>
          <div style="font-size:14px;font-weight:800;color:var(--text);">👤 ${d.customer_name}</div>
          ${d.customer_phone ? `<div style="font-size:12px;color:var(--text3);">📞 ${d.customer_phone}</div>` : ''}
          ${d.description ? `<div style="font-size:12px;color:var(--text3);">📝 ${d.description}</div>` : ''}
          <div style="font-size:11px;color:var(--text3);">📅 ${d.date}</div>
        </div>
        <div class="debt-amt">${fmt(d.amount)} ر.ع</div>
      </div>
      <div style="display:flex;gap:6px;margin-top:10px;">
        <button onclick="payDebt(${d.id})" style="flex:1;padding:7px;background:var(--green);color:#fff;border:none;border-radius:8px;cursor:pointer;font-family:'Tajawal',sans-serif;font-size:12px;font-weight:700;">✅ سدّد</button>
        <button onclick="delDebt(${d.id})" style="padding:7px 12px;border:1px solid rgba(232,121,138,.3);border-radius:8px;background:transparent;color:var(--accent);cursor:pointer;font-size:12px;">🗑️</button>
      </div>
    </div>`).join('');
}
function showAddDebt(){ document.getElementById('addDebtForm').style.display='block'; }
async function addDebt(){
  const name = document.getElementById('debtName').value.trim();
  const amt = parseFloat(document.getElementById('debtAmt').value);
  const phone = document.getElementById('debtPhone').value.trim();
  const desc = document.getElementById('debtDesc').value.trim();
  if(!name){ showToast('⚠️ الاسم مطلوب'); return; }
  if(!amt || amt<=0){ showToast('⚠️ المبلغ مطلوب'); return; }
  const date = new Date().toLocaleDateString('ar-EG',{day:'2-digit',month:'2-digit',year:'numeric'}).replace(/\//g,'/');
  await api('/api/debts', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({customer_name:name,customer_phone:phone,amount:amt,description:desc,date:new Date().toLocaleDateString('en-GB')})});
  ['debtName','debtPhone','debtAmt','debtDesc'].forEach(id=>{ const el=document.getElementById(id); if(el) el.value=''; });
  document.getElementById('addDebtForm').style.display='none';
  showToast('✅ تم تسجيل الدين');
  loadDebts();
}
async function payDebt(id){
  if(!confirm('تأكيد: تم سداد هذا الدين؟')) return;
  await api(`/api/debts/${id}/pay`, {method:'POST'});
  showToast('✅ تم تسجيل السداد');
  loadDebts();
}
async function delDebt(id){
  if(!confirm('حذف هذا الدين؟')) return;
  await api(`/api/debts/${id}`, {method:'DELETE'});
  showToast('🗑️ تم الحذف');
  loadDebts();
}

/* ══════════════════════════════════════════
   CATALOG
══════════════════════════════════════════ */
async function loadCatalog(){
  const products = await api('/api/catalog');
  const el = document.getElementById('catalogGrid');
  if(!el) return;
  if(!products.length){
    el.innerHTML='<div style="grid-column:1/-1;text-align:center;color:var(--text3);padding:30px;">لا يوجد منتجات في الكتالوج بعد 📷</div>';
    return;
  }
  el.innerHTML = products.map(p => `
    <div class="cat-prod-card ${p.available?'':'cat-unavail'}">
      ${p.img ? `<img class="cat-prod-img" src="${p.img}" onerror="this.style.display='none'" loading="lazy"/>` : `<div class="cat-prod-img-placeholder">🌸</div>`}
      <div class="cat-prod-info">
        <div class="cat-prod-name">${p.name}</div>
        <div class="cat-prod-price">${fmt(p.price)} ر.ع</div>
        ${p.description ? `<div class="cat-prod-desc">${p.description}</div>` : ''}
        ${!p.available ? '<div style="font-size:10px;color:var(--accent);margin-top:4px;">غير متاح حالياً</div>' : ''}
      </div>
      <div class="cat-prod-actions">
        <button class="cat-toggle" onclick="toggleCatalogProduct(${p.id},${p.available})">${p.available?'🔴 إخفاء':'✅ إظهار'}</button>
        <button class="cat-del" onclick="delCatalogProduct(${p.id})">🗑️</button>
      </div>
    </div>`).join('');
}
async function addCatalogProduct(){
  const name = document.getElementById('catName').value.trim();
  const price = parseFloat(document.getElementById('catPrice').value);
  const desc = document.getElementById('catDesc').value.trim();
  const img = document.getElementById('catImg').value.trim();
  if(!name){ showToast('⚠️ اسم المنتج مطلوب'); return; }
  if(!price || price<=0){ showToast('⚠️ السعر مطلوب'); return; }
  await api('/api/catalog', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name,price,description:desc,img})});
  ['catName','catPrice','catDesc','catImg'].forEach(id=>{ const el=document.getElementById(id); if(el) el.value=''; });
  showToast('✅ تم إضافة المنتج');
  loadCatalog();
}
async function toggleCatalogProduct(id, current){
  await api(`/api/catalog/${id}`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify({available:current?0:1})});
  loadCatalog();
}
async function delCatalogProduct(id){
  if(!confirm('حذف هذا المنتج من الكتالوج؟')) return;
  await api(`/api/catalog/${id}`, {method:'DELETE'});
  showToast('🗑️ تم الحذف');
  loadCatalog();
}
async function shareCatalog(){
  const products = await api('/api/catalog');
  const available = products.filter(p=>p.available);
  if(!available.length){ showToast('⚠️ لا توجد منتجات متاحة'); return; }
  let lines = ['🌸 *فيروز فلورز — كتالوج المنتجات*',''];
  available.forEach((p,i)=>{
    lines.push((i+1)+'. *'+p.name+'* — '+(+p.price).toFixed(3)+' ر.ع');
    if(p.description) lines.push('   '+p.description);
  });
  lines.push('');
  lines.push('📞 للطلب تواصل معنا');
  const msg = lines.join('%0A');
  window.open('https://wa.me/?text='+msg,'_blank');
}

function initApp(){
  // كل استدعاء معزول حتى لا يمنع فشلُ واحد البقيةَ
  try{ load(); }catch(e){ console.error('load init failed', e); }
  try{ loadFlowerInvPage(); }catch(e){ console.error('loadFlowerInvPage failed', e); }
  try{ loadInsights(); }catch(e){ console.error('loadInsights failed', e); }
  try{ loadAiStatus(); }catch(e){ console.error('loadAiStatus failed', e); }
  try{ loadGoal(); }catch(e){ console.error('loadGoal failed', e); }
  try{ loadHeaderBadges(); }catch(e){}
}
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
</script>
</body>
</html>"""

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
.wh-sub{font-size:10px;color:#b09888;}
.logout-w{background:#fce4ec;border:none;border-radius:10px;color:#c4566a;font-size:12px;font-weight:700;padding:8px 14px;cursor:pointer;font-family:'Tajawal',sans-serif;}

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
.nav-btn .nb-sub{font-size:11px;color:rgba(255,255,255,0.8);font-weight:600;}
.nb-sale{background:linear-gradient(135deg,#7aab8a,#5a8a6a);box-shadow:0 6px 24px rgba(90,138,106,.35);}
.nb-buy{background:linear-gradient(135deg,#e8798a,#c4566a);box-shadow:0 6px 24px rgba(232,121,138,.35);}
.nb-flower{background:linear-gradient(135deg,#d4a843,#b8891f);box-shadow:0 6px 24px rgba(212,168,67,.35);}
.nb-inv{background:linear-gradient(135deg,#9664dc,#7a44c0);box-shadow:0 6px 24px rgba(150,100,220,.35);}
.nb-shelf{background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 6px 24px rgba(59,130,246,.35);}
.nb-today{background:linear-gradient(135deg,#f97316,#ea580c);box-shadow:0 6px 24px rgba(249,115,22,.35);}

/* Today sales */
.today-entry{background:#fff;border:2px solid #f9c8d0;border-radius:14px;padding:12px 14px;display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.today-entry-info{flex:1;min-width:0;}
.today-entry-desc{font-size:14px;font-weight:800;color:#3d2c24;}
.today-entry-meta{font-size:11px;color:#b09888;margin-top:3px;}
.today-entry-amt{font-size:17px;font-weight:900;color:#5a8a6a;flex-shrink:0;}
.today-del-btn{width:36px;height:36px;border-radius:10px;border:none;background:#fce4ec;color:#c4566a;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.today-total-bar{background:linear-gradient(135deg,#e8f5e9,#c8e6c9);border:2px solid #7aab8a;border-radius:14px;padding:12px 16px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;}
.today-total-lbl{font-size:12px;font-weight:800;color:#5a8a6a;}
.today-total-val{font-size:22px;font-weight:900;color:#3a6a4a;}

/* Shelf screen */
.shelf-card{background:#fff;border:2px solid #f9c8d0;border-radius:18px;padding:16px;margin-bottom:10px;display:flex;align-items:center;gap:14px;cursor:pointer;transition:.2s;}
.shelf-card:active{transform:scale(.97);}
.shelf-card-dot{width:16px;height:16px;border-radius:50%;flex-shrink:0;}
.shelf-card-name{font-size:17px;font-weight:900;color:#3d2c24;flex:1;}
.shelf-card-count{font-size:12px;color:#b09888;}
.shelf-card-arrow{font-size:20px;color:#b09888;}
.prod-card{background:#fff;border:2px solid #f9c8d0;border-radius:16px;padding:14px;margin-bottom:8px;cursor:pointer;transition:.2s;}
.prod-card:active{transform:scale(.97);}
.prod-card.sel{border-color:#3b82f6;background:#eff6ff;}
.prod-card-top{display:flex;align-items:center;justify-content:space-between;}
.prod-card-name{font-size:15px;font-weight:800;color:#3d2c24;}
.prod-card-price{font-size:18px;font-weight:900;color:#5a8a6a;}
.prod-card-qty{font-size:11px;color:#b09888;margin-top:3px;}

/* Screen header */
.sc-hdr{display:flex;align-items:center;gap:12px;margin-bottom:20px;}
.sc-back{background:#fff;border:1px solid #f9c8d0;border-radius:12px;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;flex-shrink:0;}
.sc-title{font-size:20px;font-weight:900;}

/* Big input fields */
.big-field{background:#fff;border:2px solid #f9c8d0;border-radius:16px;padding:16px;margin-bottom:14px;}
.big-field label{font-size:11px;font-weight:700;color:#b09888;letter-spacing:1px;display:block;margin-bottom:8px;}
.big-field input{width:100%;border:none;outline:none;font-family:'Tajawal',sans-serif;font-size:22px;font-weight:900;color:#3d2c24;background:transparent;}
.big-field input::placeholder{color:#d4c4b8;font-size:18px;font-weight:600;}

/* Big choice buttons */
.choice-lbl{font-size:11px;font-weight:700;color:#b09888;letter-spacing:1px;margin-bottom:10px;display:block;}
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
.day-bar{background:#fff;border:1px solid #f9c8d0;border-radius:16px;padding:14px 16px;display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;}
.day-stat{text-align:center;}
.day-stat .ds-val{font-size:20px;font-weight:900;}
.day-stat .ds-lbl{font-size:10px;color:#b09888;margin-top:2px;}
.ds-s .ds-val{color:#5a8a6a;}
.ds-b .ds-val{color:#c4566a;}

/* Cash box */
.cash-box{background:linear-gradient(135deg,#fffbea,#fff8d6);border:2px solid #f5c842;border-radius:18px;padding:14px 16px;margin-bottom:12px;display:flex;align-items:center;gap:12px;}
.cash-box-ico{font-size:32px;flex-shrink:0;}
.cash-box-info{flex:1;min-width:0;}
.cash-box-lbl{font-size:10px;font-weight:800;color:#a07010;letter-spacing:1px;text-transform:uppercase;}
.cash-box-val{font-size:26px;font-weight:900;color:#7a5000;line-height:1.1;}
.cash-box-sub{font-size:11px;color:#c4960a;margin-top:2px;}
.cash-box-btn{padding:8px 12px;background:#f5c842;border:none;border-radius:10px;font-family:'Tajawal',sans-serif;font-size:12px;font-weight:800;color:#5a3a00;cursor:pointer;flex-shrink:0;}

/* Pending orders badge */
.orders-alert{background:linear-gradient(135deg,#fff5f0,#ffe8e0);border:2px solid #f9a88a;border-radius:16px;padding:12px 14px;margin-bottom:12px;display:flex;align-items:center;gap:10px;cursor:pointer;}
.orders-alert-ico{font-size:28px;flex-shrink:0;}
.orders-alert-txt{flex:1;}
.orders-alert-title{font-size:14px;font-weight:900;color:#c4566a;}
.orders-alert-sub{font-size:11px;color:#b09888;margin-top:2px;}
.orders-alert-count{font-size:22px;font-weight:900;color:#c4566a;flex-shrink:0;}

/* Cash log modal */
.cash-modal{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:200;display:flex;align-items:flex-end;}
.cash-modal-inner{background:#fff;border-radius:24px 24px 0 0;width:100%;max-height:85vh;overflow-y:auto;padding:20px 16px 32px;}
.cash-modal-title{font-size:18px;font-weight:900;color:#3d2c24;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;}
.cash-log-row{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #f9c8d0;}
.cash-log-ico{font-size:20px;flex-shrink:0;}
.cash-log-desc{flex:1;font-size:13px;color:#3d2c24;font-weight:600;}
.cash-log-date{font-size:10px;color:#b09888;}
.cash-log-amt{font-size:15px;font-weight:900;flex-shrink:0;}
.cash-in{color:#5a8a6a;}
.cash-out{color:#c4566a;}

/* Calculator */
.calc-header-btn{background:#f0f4ff;border:1px solid #c7d7f9;border-radius:10px;font-size:20px;width:38px;height:38px;cursor:pointer;display:flex;align-items:center;justify-content:center;}
.calc-modal{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:300;display:flex;align-items:flex-end;}
.calc-inner{background:#fff;border-radius:28px 28px 0 0;width:100%;padding:16px 12px 32px;}
.calc-screen{background:#1a1a2e;border-radius:18px;padding:16px 20px;margin-bottom:14px;min-height:84px;display:flex;flex-direction:column;align-items:flex-end;justify-content:flex-end;overflow:hidden;}
.calc-expr{font-size:14px;color:#6a7ab0;min-height:20px;word-break:break-all;text-align:right;}
.calc-result{font-size:38px;font-weight:900;color:#fff;line-height:1.1;word-break:break-all;text-align:right;}
.calc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;}
.ck{border:none;border-radius:16px;font-family:'Tajawal',sans-serif;font-size:22px;font-weight:900;padding:18px 8px;cursor:pointer;transition:transform .1s;-webkit-appearance:none;}
.ck:active{transform:scale(.93);}
.ck-num{background:#f5f0eb;color:#3d2c24;}
.ck-op{background:#fce4ec;color:#c4566a;}
.ck-eq{background:linear-gradient(135deg,#7aab8a,#5a8a6a);color:#fff;box-shadow:0 4px 16px rgba(90,138,106,.35);}
.ck-clr{background:#fce4ec;color:#c4566a;font-size:16px;}
.ck-zero{grid-column:span 2;}
.calc-use-btn{width:100%;margin-top:10px;padding:13px;background:#eff6ff;border:2px solid #3b82f6;border-radius:14px;color:#1d4ed8;font-family:'Tajawal',sans-serif;font-size:14px;font-weight:800;cursor:pointer;}
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
  <div style="display:flex;gap:8px;align-items:center;">
    <button class="calc-header-btn" onclick="openCalc()" title="آلة حاسبة">🧮</button>
    <button class="logout-w" onclick="location.href='/worker-logout'">خروج 🔒</button>
  </div>
</div>

<!-- HOME -->
<div class="screen on" id="sc-home">
  <div style="text-align:center;padding:20px 0 16px;">
    <div style="font-size:28px;font-weight:900;color:#c4566a;">مرحباً 👋</div>
    <div style="font-size:13px;color:#b09888;margin-top:4px;">اختر العملية</div>
  </div>

  <!-- خزينة الكاش -->
  <div class="cash-box" id="cashBox">
    <div class="cash-box-ico">💵</div>
    <div class="cash-box-info">
      <div class="cash-box-lbl">خزينة الكاش</div>
      <div class="cash-box-val" id="cashBalance">—</div>
      <div class="cash-box-sub" id="cashSub">اليوم: جاري التحميل...</div>
    </div>
    <button class="cash-box-btn" onclick="openCashModal()">السجل ←</button>
  </div>

  <!-- الطلبات المعلقة -->
  <div class="orders-alert" id="ordersAlert" onclick="go('orders')" style="display:none;">
    <div class="orders-alert-ico">📋</div>
    <div class="orders-alert-txt">
      <div class="orders-alert-title">طلبات تنتظر التنفيذ</div>
      <div class="orders-alert-sub">اضغط لعرض التفاصيل</div>
    </div>
    <div class="orders-alert-count" id="ordersAlertCount">0</div>
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
    <button class="nav-btn nb-shelf" onclick="go('shelf')">
      <div class="nb-ico">🗄️</div>
      <div class="nb-txt">بيع من رف</div>
      <div class="nb-sub">مبيعات الرفوف</div>
    </button>
    <button class="nav-btn nb-today" onclick="go('today')">
      <div class="nb-ico">📋</div>
      <div class="nb-txt">مبيعات اليوم</div>
      <div class="nb-sub">عرض وحذف</div>
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
      <label>💰 سعر القطعة (ر.ع)</label>
      <input type="number" id="s-amt" placeholder="0.000" step="0.001" inputmode="decimal" oninput="updateSaleTotal()"/>
    </div>

    <div class="big-field">
      <label>🔢 الكمية</label>
      <div style="display:flex;align-items:center;gap:12px;">
        <button class="qty-btn" style="width:48px;height:48px;font-size:26px;" onclick="adjSaleQty(-1)">−</button>
        <input class="qty-inp" id="s-qty" type="number" value="1" min="1" inputmode="numeric" style="width:70px;font-size:22px;" oninput="updateSaleTotal()"/>
        <button class="qty-btn" style="width:48px;height:48px;font-size:26px;" onclick="adjSaleQty(1)">+</button>
        <div style="flex:1;text-align:left;">
          <div style="font-size:11px;color:#b09888;">الإجمالي</div>
          <div style="font-size:18px;font-weight:900;color:#5a8a6a;" id="s-total">—</div>
        </div>
      </div>
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

<!-- ORDERS SCREEN -->
<div class="screen" id="sc-orders">
  <div class="sc-hdr">
    <div class="sc-back" onclick="go('home')">←</div>
    <div class="sc-title" style="color:#c4566a;">📋 الطلبات المعلقة</div>
  </div>
  <div id="w-orders-list" style="display:flex;flex-direction:column;gap:12px;"></div>
</div>

<!-- TODAY SALES SCREEN -->
<div class="screen" id="sc-today">
  <div class="sc-hdr">
    <div class="sc-back" onclick="go('home')">←</div>
    <div class="sc-title" style="color:#ea580c;">📋 مبيعات اليوم</div>
  </div>
  <div class="today-total-bar">
    <div class="today-total-lbl">💰 إجمالي اليوم</div>
    <div class="today-total-val" id="todayTotalVal">—</div>
  </div>
  <div id="today-entries-list"></div>
</div>

<!-- SHELF SCREEN -->
<div class="screen" id="sc-shelf">
  <div class="sc-hdr">
    <div class="sc-back" id="shelfBack" onclick="shelfGoBack()">←</div>
    <div class="sc-title" style="color:#1d4ed8;" id="shelfTitle">🗄️ بيع من رف</div>
  </div>

  <!-- بطاقة النجاح -->
  <div class="done-card" id="shelf-done">
    <div class="done-ico">✅</div>
    <div class="done-txt" id="shelf-done-txt">تم تسجيل المبيعة!</div>
    <div class="done-sub" id="shelf-done-sub"></div>
    <button class="done-again" onclick="resetShelf()">➕ بيعة أخرى من رف</button>
  </div>

  <!-- قائمة الرفوف -->
  <div id="shelf-list-view">
    <div id="shelf-list" style="display:flex;flex-direction:column;gap:0;"></div>
  </div>

  <!-- قائمة المنتجات -->
  <div id="shelf-products-view" style="display:none;">
    <div id="shelf-prods-list" style="margin-bottom:14px;"></div>

    <!-- السعر -->
    <div class="big-field" id="shelf-price-field" style="display:none;">
      <label>💰 السعر (ر.ع)</label>
      <input type="number" id="sh-amt" placeholder="0.000" step="0.001" inputmode="decimal"/>
    </div>

    <!-- الكمية -->
    <div class="big-field" id="shelf-qty-field" style="display:none;">
      <label>🔢 الكمية</label>
      <div style="display:flex;align-items:center;gap:12px;">
        <button class="qty-btn" style="width:48px;height:48px;font-size:26px;" onclick="adjShelfQty(-1)">−</button>
        <input class="qty-inp" id="sh-qty" type="number" value="1" min="1" inputmode="numeric" style="width:70px;font-size:22px;"/>
        <button class="qty-btn" style="width:48px;height:48px;font-size:26px;" onclick="adjShelfQty(1)">+</button>
        <div style="font-size:13px;color:#b09888;" id="sh-stock-lbl"></div>
      </div>
    </div>

    <!-- طريقة الدفع -->
    <span class="choice-lbl" id="shelf-pay-lbl" style="display:none;">💳 طريقة الدفع</span>
    <div class="choice-grid g3" id="shelf-pay-grid" style="display:none;">
      <button class="choice-btn" style="--sel-clr:#5a8a6a;--sel-bg:#e8f5e9;" data-spay="كاش 💵" onclick="selShelfPay(this)"><div class="cb-ico">💵</div>كاش</button>
      <button class="choice-btn" style="--sel-clr:#4a7ab0;--sel-bg:#e3f2fd;" data-spay="فيزا 💳" onclick="selShelfPay(this)"><div class="cb-ico">💳</div>فيزا</button>
      <button class="choice-btn" style="--sel-clr:#7a44c0;--sel-bg:#f3e5ff;" data-spay="تحويل 🏦" onclick="selShelfPay(this)"><div class="cb-ico">🏦</div>تحويل</button>
    </div>

    <button class="sub-btn" id="sh-sub-btn" style="display:none;background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:#fff;box-shadow:0 6px 24px rgba(59,130,246,.4);" onclick="submitShelfSale()">✅ تسجيل البيعة</button>
  </div>
</div>

<!-- CASH MODAL -->
<div class="cash-modal" id="cashModal" style="display:none;" onclick="closeCashModal(event)">
  <div class="cash-modal-inner">
    <div class="cash-modal-title">
      <span>💵 خزينة الكاش</span>
      <button onclick="closeCashModal()" style="background:#f5ede0;border:none;border-radius:10px;padding:6px 12px;font-size:13px;cursor:pointer;font-family:'Tajawal',sans-serif;">إغلاق</button>
    </div>

    <!-- الرصيد الحالي -->
    <div style="background:linear-gradient(135deg,#fffbea,#fff8d6);border:2px solid #f5c842;border-radius:16px;padding:16px;margin-bottom:16px;text-align:center;">
      <div style="font-size:12px;color:#a07010;font-weight:700;margin-bottom:4px;">الرصيد الحالي</div>
      <div style="font-size:32px;font-weight:900;color:#7a5000;" id="modalCashBalance">—</div>
      <div style="font-size:11px;color:#c4960a;margin-top:4px;" id="modalCashToday"></div>
    </div>

    <!-- تعديل يدوي -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px;">
      <button onclick="cashAdjust('in')" style="padding:12px;background:#e8f5e9;border:2px solid #7aab8a;border-radius:12px;color:#5a8a6a;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:800;cursor:pointer;">➕ إضافة كاش</button>
      <button onclick="cashAdjust('out')" style="padding:12px;background:#fce4ec;border:2px solid #e8798a;border-radius:12px;color:#c4566a;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:800;cursor:pointer;">➖ سحب كاش</button>
    </div>

    <!-- السجل -->
    <div style="font-size:11px;font-weight:800;color:#b09888;letter-spacing:1px;margin-bottom:10px;">آخر العمليات</div>
    <div id="cashLogList"></div>
  </div>
</div>

<!-- CALCULATOR MODAL -->
<div class="calc-modal" id="calcModal" style="display:none;" onclick="closeCalcOutside(event)">
  <div class="calc-inner">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
      <div style="font-size:17px;font-weight:900;color:#3d2c24;">🧮 الآلة الحاسبة</div>
      <button onclick="closeCalc()" style="background:#f5ede0;border:none;border-radius:10px;padding:6px 14px;font-size:13px;cursor:pointer;font-family:'Tajawal',sans-serif;font-weight:700;">إغلاق</button>
    </div>
    <div class="calc-screen">
      <div class="calc-expr" id="calcExpr"></div>
      <div class="calc-result" id="calcResult">0</div>
    </div>
    <div class="calc-grid">
      <button class="ck ck-clr" onclick="calcClear()">مسح</button>
      <button class="ck ck-clr" onclick="calcDel()">⌫</button>
      <button class="ck ck-clr" onclick="calcPercent()">%</button>
      <button class="ck ck-op"  onclick="calcOp('÷')">÷</button>
      <button class="ck ck-num" onclick="calcNum('7')">7</button>
      <button class="ck ck-num" onclick="calcNum('8')">8</button>
      <button class="ck ck-num" onclick="calcNum('9')">9</button>
      <button class="ck ck-op"  onclick="calcOp('×')">×</button>
      <button class="ck ck-num" onclick="calcNum('4')">4</button>
      <button class="ck ck-num" onclick="calcNum('5')">5</button>
      <button class="ck ck-num" onclick="calcNum('6')">6</button>
      <button class="ck ck-op"  onclick="calcOp('−')">−</button>
      <button class="ck ck-num" onclick="calcNum('1')">1</button>
      <button class="ck ck-num" onclick="calcNum('2')">2</button>
      <button class="ck ck-num" onclick="calcNum('3')">3</button>
      <button class="ck ck-op"  onclick="calcOp('+')">+</button>
      <button class="ck ck-num ck-zero" onclick="calcNum('0')">0</button>
      <button class="ck ck-num" onclick="calcDot()">.</button>
      <button class="ck ck-eq"  onclick="calcEquals()">=</button>
    </div>
    <button class="calc-use-btn" onclick="useCalcResult()" id="calcUseBtn" style="display:none;">
      ← استخدم الناتج في حقل السعر
    </button>
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
  if(sc==='home'){ loadDaySummary(); loadCash(); loadPendingOrders(); }
  if(sc==='flower') loadFlowerTypes();
  if(sc==='orders') loadWorkerOrders();
  if(sc==='today') loadTodaySales();
  if(sc==='shelf'){ document.getElementById('shelf-done').style.display='none'; document.getElementById('shelf-list-view').style.display='block'; document.getElementById('shelf-products-view').style.display='none'; loadShelves(); }
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
function adjSaleQty(d){
  const inp=document.getElementById('s-qty');
  inp.value=Math.max(1,(parseInt(inp.value)||1)+d);
  updateSaleTotal();
}
function updateSaleTotal(){
  const amt=parseFloat(document.getElementById('s-amt').value)||0;
  const qty=parseInt(document.getElementById('s-qty').value)||1;
  const el=document.getElementById('s-total');
  if(el) el.textContent = amt>0 ? (amt*qty).toFixed(3)+' ر.ع' : '—';
}

async function submitSale(){
  const unitAmt=parseFloat(document.getElementById('s-amt').value);
  const qty=parseInt(document.getElementById('s-qty').value)||1;
  if(!unitAmt||unitAmt<=0){showToast('⚠️ أدخل السعر');return;}
  if(!selCat){showToast('⚠️ اختر نوع المنتج');return;}
  if(!selPay_){showToast('⚠️ اختر طريقة الدفع');return;}
  const totalAmt=unitAmt*qty;
  try{
    const month=new Date().getFullYear()+'-'+String(new Date().getMonth()+1).padStart(2,'0');
    const desc=qty>1 ? selCat+' ×'+qty : selCat;
    await api('/api/entries',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type:'s',desc,amt:totalAmt,payment_method:selPay_,category:selCat,month})});
    document.getElementById('sale-done-txt').textContent='✅ تم تسجيل المبيعة!';
    document.getElementById('sale-done-sub').textContent=desc+' — '+fmt(totalAmt)+' ر.ع — '+selPay_;
    document.getElementById('sale-form').style.display='none';
    document.getElementById('sale-done').style.display='block';
    loadDaySummary(); loadCash();
  }catch(e){showToast('❌ خطأ في التسجيل');}
}

function resetSale(){
  selCat='';selPay_='';
  document.getElementById('s-amt').value='';
  document.getElementById('s-qty').value='1';
  document.getElementById('s-total').textContent='—';
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

// ── CASH REGISTER ──
async function loadCash(){
  try{
    const d = await api('/api/cash');
    const bal = d.balance || 0;
    const todayIn = d.today_in || 0;
    const el = document.getElementById('cashBalance');
    const sub = document.getElementById('cashSub');
    if(el) el.textContent = (bal).toFixed(3) + ' ر.ع';
    if(sub) sub.textContent = 'دخل اليوم: ' + todayIn.toFixed(3) + ' ر.ع';
    // لون الرصيد
    const box = document.getElementById('cashBox');
    if(box) box.style.borderColor = bal < 10 ? '#e8798a' : '#f5c842';
  }catch(e){}
}

async function openCashModal(){
  document.getElementById('cashModal').style.display='flex';
  const d = await api('/api/cash');
  const bal = d.balance || 0;
  const todayIn = d.today_in || 0;
  const todayOut = d.today_out || 0;
  const balEl = document.getElementById('modalCashBalance');
  const todayEl = document.getElementById('modalCashToday');
  if(balEl) balEl.textContent = bal.toFixed(3) + ' ر.ع';
  if(todayEl) todayEl.textContent = 'دخل اليوم: +'+todayIn.toFixed(3)+' | خرج: -'+todayOut.toFixed(3)+' ر.ع';
  const log = d.log || [];
  const listEl = document.getElementById('cashLogList');
  if(!listEl) return;
  if(!log.length){ listEl.innerHTML='<div style="text-align:center;color:#b09888;padding:20px;">لا توجد عمليات بعد</div>'; return; }
  listEl.innerHTML = log.map(r => `
    <div class="cash-log-row">
      <div class="cash-log-ico">${r.type==='in'?'💵':'💸'}</div>
      <div style="flex:1;">
        <div class="cash-log-desc">${r.description||''}</div>
        <div class="cash-log-date">📅 ${r.date}</div>
      </div>
      <div class="cash-log-amt ${r.type==='in'?'cash-in':'cash-out'}">${r.type==='in'?'+':'-'}${(+r.amount).toFixed(3)}</div>
    </div>`).join('');
}

function closeCashModal(e){
  if(!e || e.target===document.getElementById('cashModal'))
    document.getElementById('cashModal').style.display='none';
}

async function cashAdjust(type){
  const label = type==='in' ? 'كم تضيف للخزينة؟ (ر.ع)' : 'كم تسحب من الخزينة؟ (ر.ع)';
  const amt = prompt(label);
  if(!amt) return;
  const val = parseFloat(amt);
  if(isNaN(val) || val <= 0){ showToast('⚠️ رقم غير صحيح'); return; }
  const desc = prompt('السبب (اختياري):') || (type==='in' ? 'إضافة يدوية' : 'سحب يدوي');
  await api('/api/cash/adjust', {method:'POST', headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type, amount:val, description:desc})});
  showToast(type==='in' ? '✅ تمت الإضافة' : '✅ تم السحب');
  openCashModal();
  loadCash();
}

// ── TODAY SALES ──
async function loadTodaySales(){
  try{
    const today = new Date();
    const day = String(today.getDate()).padStart(2,'0')+'/'+String(today.getMonth()+1).padStart(2,'0')+'/'+today.getFullYear();
    const month = today.getFullYear()+'-'+String(today.getMonth()+1).padStart(2,'0');
    const d = await api('/api/entries?month='+month);
    const sales = (d.sales||[]).filter(e=>e.date===day);
    const total = sales.reduce((a,e)=>a+(+e.amt),0);
    document.getElementById('todayTotalVal').textContent = total.toFixed(3)+' ر.ع';
    const el = document.getElementById('today-entries-list');
    if(!sales.length){
      el.innerHTML='<div style="text-align:center;padding:40px;color:#b09888;font-size:15px;">لا توجد مبيعات مسجلة اليوم</div>';
      return;
    }
    el.innerHTML = sales.map(e=>{
      const pay = e.payment_method ? ' — '+e.payment_method : '';
      const shelf = e.shelf_id ? ' 🗄️' : '';
      const time = e.sale_time || '';
      return `<div class="today-entry" id="te-${e.id}">
        <div class="today-entry-info">
          <div class="today-entry-desc">${e.desc}${shelf}</div>
          <div class="today-entry-meta">${time}${pay}</div>
        </div>
        <div class="today-entry-amt">+${(+e.amt).toFixed(3)}</div>
        <button class="today-del-btn" onclick="deleteTodayEntry(${e.id},this)" title="حذف">🗑️</button>
      </div>`;
    }).join('');
  }catch(err){ showToast('❌ تعذر التحميل'); }
}

async function deleteTodayEntry(id, btn){
  if(!confirm('حذف هذه المبيعة؟')) return;
  btn.disabled=true; btn.textContent='⏳';
  try{
    await api('/api/entries/'+id, {method:'DELETE'});
    const row = document.getElementById('te-'+id);
    if(row){ row.style.opacity='0'; row.style.transition='opacity .3s'; setTimeout(()=>{row.remove(); loadTodaySales();},350); }
    loadDaySummary();
    showToast('🗑️ تم الحذف');
  }catch(e){ showToast('❌ فشل الحذف'); btn.disabled=false; btn.textContent='🗑️'; }
}

// ── SHELF SALE ──
let shelfSelProd = null;
let shelfSelPay_ = '';
let shelfShelves = [];

async function loadShelves(){
  try{
    const d = await api('/api/shelves');
    shelfShelves = Array.isArray(d) ? d : (d.shelves || []);
    const el = document.getElementById('shelf-list');
    if(!shelfShelves.length){
      el.innerHTML = '<div style="text-align:center;padding:40px;color:#b09888;">لا توجد رفوف مسجلة</div>';
      return;
    }
    el.innerHTML = shelfShelves.map(s => `
      <div class="shelf-card" onclick="openShelfProducts(${s.id},'${s.name}','${s.color||'#e8547a'}')">
        <div class="shelf-card-dot" style="background:${s.color||'#e8547a'};"></div>
        <div style="flex:1;">
          <div class="shelf-card-name">${s.name}</div>
          <div class="shelf-card-count">${(s.products||[]).length} منتج</div>
        </div>
        <div class="shelf-card-arrow">←</div>
      </div>`).join('');
  }catch(e){showToast('❌ تعذر تحميل الرفوف');}
}

function openShelfProducts(sid, sname, scolor){
  const shelf = shelfShelves.find(s=>s.id===sid);
  if(!shelf) return;
  const prods = shelf.products || [];
  document.getElementById('shelf-list-view').style.display = 'none';
  document.getElementById('shelf-products-view').style.display = 'block';
  document.getElementById('shelfTitle').textContent = '🗄️ ' + sname;
  shelfSelProd = null; shelfSelPay_ = '';
  const hide = id => { const e=document.getElementById(id); if(e) e.style.display='none'; };
  hide('shelf-price-field'); hide('shelf-qty-field');
  hide('shelf-pay-lbl'); hide('shelf-pay-grid'); hide('sh-sub-btn');
  document.querySelectorAll('[data-spay]').forEach(b=>b.classList.remove('sel'));
  if(!prods.length){
    document.getElementById('shelf-prods-list').innerHTML = '<div style="text-align:center;padding:30px;color:#b09888;">لا توجد منتجات في هذا الرف</div>';
    return;
  }
  document.getElementById('shelf-prods-list').innerHTML = prods.map(p=>`
    <div class="prod-card" id="prod-${p.id}" onclick="selectProd(${p.id},${p.price},${p.qty},'${p.name.replace(/'/g,"\\'")}')">
      <div class="prod-card-top">
        <div class="prod-card-name">${p.name}</div>
        <div class="prod-card-price">${(+p.price).toFixed(3)} ر.ع</div>
      </div>
      <div class="prod-card-qty">المخزون: ${p.qty} قطعة</div>
    </div>`).join('');
}

function shelfGoBack(){
  const pv = document.getElementById('shelf-products-view');
  const lv = document.getElementById('shelf-list-view');
  if(pv.style.display !== 'none'){
    pv.style.display = 'none';
    lv.style.display = 'block';
    document.getElementById('shelfTitle').textContent = '🗄️ بيع من رف';
  } else {
    go('home');
  }
}

function selectProd(pid, price, qty, name){
  shelfSelProd = {id:pid, price, qty, name};
  document.querySelectorAll('.prod-card').forEach(c=>c.classList.remove('sel'));
  const card = document.getElementById('prod-'+pid);
  if(card) card.classList.add('sel');
  // إظهار السعر والكمية وطريقة الدفع
  const show = id => { const e=document.getElementById(id); if(e) e.style.display=''; };
  show('shelf-price-field'); show('shelf-qty-field');
  show('shelf-pay-lbl'); show('shelf-pay-grid'); show('sh-sub-btn');
  document.getElementById('sh-amt').value = price.toFixed(3);
  document.getElementById('sh-qty').value = '1';
  document.getElementById('sh-stock-lbl').textContent = qty > 0 ? ('متوفر: '+qty) : '⚠️ نفد المخزون';
  document.getElementById('sh-amt').scrollIntoView({behavior:'smooth',block:'center'});
}

function adjShelfQty(d){
  const inp = document.getElementById('sh-qty');
  const max = shelfSelProd ? shelfSelProd.qty : 999;
  const v = Math.min(max, Math.max(1, (parseInt(inp.value)||1)+d));
  inp.value = v;
}

function selShelfPay(el){
  shelfSelPay_ = el.dataset.spay;
  document.querySelectorAll('[data-spay]').forEach(b=>b.classList.remove('sel'));
  el.classList.add('sel');
}

async function submitShelfSale(){
  if(!shelfSelProd){ showToast('⚠️ اختر منتجاً'); return; }
  if(!shelfSelPay_){ showToast('⚠️ اختر طريقة الدفع'); return; }
  const qty = parseInt(document.getElementById('sh-qty').value)||1;
  const amt = parseFloat(document.getElementById('sh-amt').value);
  if(!amt||amt<=0){ showToast('⚠️ السعر غير صحيح'); return; }
  const btn = document.getElementById('sh-sub-btn');
  btn.disabled=true; btn.textContent='⏳ جاري التسجيل...';
  try{
    const d = await api('/api/shelf_products/'+shelfSelProd.id+'/sell',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({qty, payment_method:shelfSelPay_})
    });
    if(!d.ok){ showToast('❌ فشل التسجيل'); btn.disabled=false; btn.textContent='✅ تسجيل البيعة'; return; }
    document.getElementById('shelf-done-txt').textContent = '✅ تم تسجيل المبيعة!';
    document.getElementById('shelf-done-sub').textContent = shelfSelProd.name+' × '+qty+' — '+(+d.total).toFixed(3)+' ر.ع — '+shelfSelPay_;
    document.getElementById('shelf-products-view').style.display='none';
    document.getElementById('shelf-list-view').style.display='none';
    document.getElementById('shelf-done').style.display='block';
    loadDaySummary(); loadCash();
  }catch(e){ showToast('❌ خطأ في الاتصال'); }
  btn.disabled=false; btn.textContent='✅ تسجيل البيعة';
}

function resetShelf(){
  document.getElementById('shelf-done').style.display='none';
  document.getElementById('shelf-list-view').style.display='block';
  document.getElementById('shelf-products-view').style.display='none';
  document.getElementById('shelfTitle').textContent='🗄️ بيع من رف';
  loadShelves();
}

// ── PENDING ORDERS ──
async function loadPendingOrders(){
  try{
    const d = await api('/api/orders?status=pending');
    const count = (d.orders||[]).length;
    const alertEl = document.getElementById('ordersAlert');
    const countEl = document.getElementById('ordersAlertCount');
    if(alertEl) alertEl.style.display = count > 0 ? 'flex' : 'none';
    if(countEl) countEl.textContent = count;
  }catch(e){}
}

async function loadWorkerOrders(){
  const d = await api('/api/orders?status=pending');
  const list = d.orders || [];
  const el = document.getElementById('w-orders-list');
  if(!el) return;
  if(!list.length){
    el.innerHTML='<div style="text-align:center;padding:40px;color:#b09888;font-size:15px;">✅ لا توجد طلبات معلقة</div>';
    return;
  }
  el.innerHTML = list.map(o => {
    const imgHtml = o.img_file_id
      ? `<img src="/api/orders/${o.id}/image" style="width:100%;max-height:180px;object-fit:cover;border-radius:12px;margin-bottom:10px;display:block;" onclick="this.style.maxHeight=this.style.maxHeight==='none'?'180px':'none'" loading="lazy"/>`
      : '';
    const priceHtml = o.price && parseFloat(o.price)>0
      ? `<div style="font-size:16px;font-weight:900;color:#5a8a6a;">💰 ${(+o.price).toFixed(3)} ر.ع</div>` : '';
    const phoneHtml = o.customer_phone
      ? `<a href="tel:${o.customer_phone}" style="display:inline-block;margin-top:6px;background:#e8f5e9;padding:6px 12px;border-radius:10px;color:#5a8a6a;text-decoration:none;font-size:13px;font-weight:700;">📞 اتصال</a>` : '';
    return `<div style="background:#fff;border:2px solid #f9c8d0;border-radius:18px;overflow:hidden;">
      ${imgHtml}
      <div style="padding:14px;">
        <div style="font-size:12px;color:#b09888;margin-bottom:4px;">طلب #${o.id} — 📅 ${o.date}</div>
        <div style="font-size:17px;font-weight:900;color:#3d2c24;">👤 ${o.customer_name}</div>
        <div style="font-size:14px;color:#7a6458;margin-top:4px;line-height:1.5;">${o.description}</div>
        ${priceHtml}
        ${o.notes ? `<div style="font-size:12px;color:#b09888;margin-top:4px;">📝 ${o.notes}</div>` : ''}
        ${phoneHtml}
        <button onclick="workerDoneOrder(${o.id},this)" style="display:block;width:100%;margin-top:12px;padding:13px;background:linear-gradient(135deg,#7aab8a,#5a8a6a);color:#fff;border:none;border-radius:12px;font-family:'Tajawal',sans-serif;font-size:15px;font-weight:900;cursor:pointer;">✅ تم التنفيذ</button>
      </div>
    </div>`;
  }).join('');
}

async function workerDoneOrder(id, btn){
  btn.disabled=true; btn.textContent='⏳ جاري...';
  await api('/api/orders/'+id, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status:'done'})});
  showToast('✅ تم تسجيل الطلب كمنجز!');
  btn.closest('div[style]').style.opacity='0.4';
  setTimeout(()=>{ loadWorkerOrders(); loadPendingOrders(); }, 1200);
}

// ── CALCULATOR ──
let calcExpr_ = '';
let calcCurrent_ = '0';
let calcJustEvaled_ = false;

function openCalc(){
  document.getElementById('calcModal').style.display='flex';
  // إذا كان في حقل سعر مفتوح، أظهر زر الاستخدام
  const activeAmt = document.querySelector('.screen.on #s-amt, .screen.on #b-amt, .screen.on #sh-amt');
  document.getElementById('calcUseBtn').style.display = activeAmt ? 'block' : 'none';
}
function closeCalc(){ document.getElementById('calcModal').style.display='none'; }
function closeCalcOutside(e){ if(e.target===document.getElementById('calcModal')) closeCalc(); }

function calcRender(){
  document.getElementById('calcExpr').textContent = calcExpr_;
  document.getElementById('calcResult').textContent = calcCurrent_;
}

function calcNum(n){
  if(calcJustEvaled_){ calcExpr_=''; calcCurrent_='0'; calcJustEvaled_=false; }
  if(calcCurrent_==='0' && n!=='.') calcCurrent_=n;
  else if(calcCurrent_.length < 12) calcCurrent_+=n;
  calcRender();
}

function calcDot(){
  if(calcJustEvaled_){ calcExpr_=''; calcCurrent_='0'; calcJustEvaled_=false; }
  if(!calcCurrent_.includes('.')) calcCurrent_+='.';
  calcRender();
}

function calcOp(op){
  calcJustEvaled_=false;
  if(calcExpr_ && !['÷','×','−','+'].includes(calcExpr_.slice(-1))){
    calcEval_();
    calcExpr_=calcCurrent_+' '+op+' ';
  } else {
    calcExpr_=calcCurrent_+' '+op+' ';
  }
  calcCurrent_='0';
  calcRender();
}

function calcEval_(){
  if(!calcExpr_) return;
  try{
    const expr = calcExpr_.replace(/÷/g,'/').replace(/×/g,'*').replace(/−/g,'-') + calcCurrent_;
    const res = Function('"use strict"; return ('+expr+')')();
    calcCurrent_ = isFinite(res) ? (+res.toFixed(6)).toString() : '0';
  }catch(e){ calcCurrent_='0'; }
}

function calcEquals(){
  if(!calcExpr_) return;
  calcEval_();
  calcExpr_='';
  calcJustEvaled_=true;
  calcRender();
}

function calcClear(){ calcExpr_=''; calcCurrent_='0'; calcJustEvaled_=false; calcRender(); }

function calcDel(){
  if(calcJustEvaled_){ calcClear(); return; }
  calcCurrent_ = calcCurrent_.length>1 ? calcCurrent_.slice(0,-1) : '0';
  calcRender();
}

function calcPercent(){
  const v = parseFloat(calcCurrent_);
  if(!isNaN(v)) calcCurrent_ = (v/100).toFixed(6).replace(/\.?0+$/,'');
  calcRender();
}

function useCalcResult(){
  const v = parseFloat(calcCurrent_);
  if(isNaN(v)){ showToast('⚠️ لا يوجد ناتج'); return; }
  const activeAmt = document.querySelector('.screen.on #s-amt, .screen.on #b-amt, .screen.on #sh-amt');
  if(activeAmt){ activeAmt.value = v.toFixed(3); showToast('✅ تم نقل الناتج'); }
  closeCalc();
}

// Init
buildCatGrid();
loadDaySummary();
loadCash();
loadPendingOrders();
</script>
</body>
</html>"""

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>فيروز فلورز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
<script src="https://chir.cat/ClusterRGB/bundle.js"></script>
<style>
:root{
  --primary-color:#d4a843;
  --accent-color:#e8798a;
  --accent-rgb:212,168,67;
  --bg-overlay:rgba(10,10,10,0.58);
  --dark-overlay:rgba(10,10,10,0.58);
  --light-overlay:rgba(10,10,10,0.28);
  --card-bg:rgba(255,255,255,0.08);
  --text-primary:#ffffff;
  --panel-radius:24px;
  --button-radius:50%;
  --border-style:24px;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{min-height:100%;overflow-x:hidden;overflow-y:auto;font-family:'Tajawal',sans-serif;scroll-behavior:smooth;}

/* Full background image */
.bg-img{
  position:fixed;
  inset:0;
  z-index:0;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: top center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

/* Mobile portrait: center the image */
@media (max-width: 1024px) and (orientation: portrait) {
  .bg-img{
    background-position: center center;
  }
}

/* Tablet portrait and smaller */
@media (max-width: 768px) {
  .bg-img{
    background-position: center center;
    background-attachment: scroll;
  }
}

.bg-overlay{
  position:fixed;
  inset:0;
  z-index:1;
  background: linear-gradient(180deg, var(--light-overlay), var(--bg-overlay));
  pointer-events:none;
}
/* Petals */
.petals{position:fixed;inset:0;z-index:2;pointer-events:none;overflow:hidden;}
.petal{
  position:absolute;border-radius:50% 0 50% 0;
  animation:petalFall linear infinite;opacity:0;
}
@keyframes petalFall{
  0%{transform:translateY(-20px) translateX(0) rotate(0deg);opacity:0;}
  5%{opacity:0.8;}
  85%{opacity:0.4;}
  100%{transform:translateY(105vh) translateX(60px) rotate(540deg);opacity:0;}
}

/* Login layout */
.wrap{
  position:relative;
  z-index:10;
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  padding:60px 16px 80px;
  gap:28px;
}

/* Brand header */
.brand-header{text-align:center;}
.logo{
  width:70px;height:70px;margin:0 auto 14px;
  background:linear-gradient(135deg,var(--primary-color),rgba(255,255,255,0.85));
  border-radius:20px;display:flex;align-items:center;justify-content:center;
  font-size:32px;
  box-shadow:0 8px 32px rgba(0,0,0,0.2);
  animation:logoFloat 4s ease-in-out infinite;
}
@keyframes logoFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}
.shop-name{
  font-family:'Playfair Display',serif;
  font-size:30px;font-weight:700;
  color:#ffffff;
  text-shadow:0 2px 20px rgba(0,0,0,0.3);
  margin-bottom:4px;
}
.shop-sub{
  font-size:11px;color:rgba(255,255,255,0.55);
  letter-spacing:3px;text-transform:uppercase;
}

/* Two cards row */
.login-row{
  display:flex;
  gap:18px;
  width:100%;
  max-width:860px;
  flex-wrap:wrap;
  justify-content:center;
  align-items:flex-start;
  padding:0 8px;
}

@keyframes cardIn{from{opacity:0;transform:translateY(30px) scale(.95);}to{opacity:1;transform:translateY(0) scale(1);}}

.login-panel{
  flex:1 1 260px;
  min-width:240px;
  max-width:320px;
  border-radius:var(--panel-radius,24px);
  padding:22px 18px;
  text-align:center;
  backdrop-filter:blur(28px) saturate(1.8);
  -webkit-backdrop-filter:blur(28px) saturate(1.8);
  box-shadow:0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.2);
  animation:cardIn .8s cubic-bezier(.34,1.56,.64,1) both;
  transition:transform .3s, box-shadow .3s;
}
.login-panel:hover{transform:translateY(-4px);}

/* Owner panel — gold */
.panel-owner{
  background:var(--card-bg);
  border:1px solid rgba(212,168,67,0.4);
  animation-delay:.05s;
}
/* Worker panel — rose */
.panel-worker{
  background:var(--card-bg);
  border:1px solid rgba(232,121,138,0.4);
  animation-delay:.15s;
}

.panel-icon{
  width:56px;height:56px;margin:0 auto 12px;
  border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:26px;
}
.panel-owner .panel-icon{background:linear-gradient(135deg,rgba(212,168,67,0.3),rgba(184,137,31,0.2));box-shadow:0 6px 20px rgba(212,168,67,0.35);}
.panel-worker .panel-icon{background:linear-gradient(135deg,rgba(232,121,138,0.3),rgba(180,70,100,0.2));box-shadow:0 6px 20px rgba(232,121,138,0.3);}

.panel-title{font-size:17px;font-weight:900;color:#fff;margin-bottom:3px;}
.panel-desc{font-size:11px;color:rgba(255,255,255,0.5);margin-bottom:18px;}

.err{color:#ffb3b3;font-size:11px;min-height:16px;margin-bottom:8px;}

.pw-wrap{position:relative;margin-bottom:14px;}
.pw-wrap input[type=password]{
  width:100%;
  background:rgba(255,255,255,0.13);
  border:1px solid rgba(255,255,255,0.25);
  border-radius:12px;padding:13px 44px 13px 14px;
  font-family:'Tajawal',sans-serif;font-size:15px;
  color:white;outline:none;transition:.3s;
  text-align:center;letter-spacing:3px;
}
.panel-owner .pw-wrap input[type=password]:focus{
  border-color:rgba(212,168,67,0.8);
  box-shadow:0 0 0 3px rgba(212,168,67,0.2);
}
.panel-worker .pw-wrap input[type=password]:focus{
  border-color:rgba(232,121,138,0.8);
  box-shadow:0 0 0 3px rgba(232,121,138,0.2);
}
.pw-wrap input[type=password]::placeholder{color:rgba(255,255,255,0.35);letter-spacing:1px;font-size:13px;}
.eye-btn{
  position:absolute;left:12px;top:50%;transform:translateY(-50%);
  background:none;border:none;color:rgba(255,255,255,0.45);cursor:pointer;font-size:16px;
}

.login-btn{
  width:100%;padding:13px;
  border:none;border-radius:12px;
  font-family:'Tajawal',sans-serif;
  font-size:15px;font-weight:900;letter-spacing:1px;
  cursor:pointer;
  transition:all .3s cubic-bezier(.34,1.56,.64,1);
}
.login-btn:active{transform:scale(0.97);}

.panel-owner .login-btn{
  background:linear-gradient(135deg,#d4a843,#c49030);
  color:#1a1208;
  box-shadow:0 6px 20px rgba(212,168,67,0.4);
}
.panel-owner .login-btn:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 10px 28px rgba(212,168,67,0.55);}

.panel-worker .login-btn{
  background:linear-gradient(135deg,#e8798a,#c4566a);
  color:#fff;
  box-shadow:0 6px 20px rgba(232,121,138,0.4);
}
.panel-worker .login-btn:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 10px 28px rgba(232,121,138,0.5);}

/* Theme Switcher Button */
.theme-switcher{
  position:fixed;
  bottom:24px;
  left:50%;
  transform:translateX(-50%);
  z-index:100;
  width:50px;
  height:50px;
  border-radius:var(--button-radius,50%);
  border:2px solid rgba(255,255,255,0.3);
  background:rgba(255,255,255,0.12);
  color:var(--text-primary);
  backdrop-filter:blur(16px) saturate(1.5);
  -webkit-backdrop-filter:blur(16px) saturate(1.5);
  font-size:24px;
  cursor:pointer;
  transition:all .3s cubic-bezier(.34,1.56,.64,1);
  box-shadow:0 8px 32px rgba(0,0,0,0.2);
  display:flex;
  align-items:center;
  justify-content:center;
}
.theme-switcher:hover{
  transform:translateX(-50%) scale(1.1);
  border-color:var(--accent-color);
  background:rgba(255,255,255,0.18);
  box-shadow:0 12px 40px rgba(0,0,0,0.28);
}
.theme-switcher:active{
  transform:translateX(-50%) scale(0.95);
}

@media (max-width:768px){
  .theme-switcher{
    bottom:16px;
    width:44px;
    height:44px;
    font-size:20px;
  }
}
</style>
</head>
<body>
<div class="bg-img"></div>
<div class="bg-overlay"></div>
<div class="petals" id="petals"></div>

<div class="wrap">
  <div class="brand-header">
    <div class="logo">🌹</div>
    <div class="shop-name">FAIROSE</div>
    <div class="shop-sub">FLOWERS & MORE</div>
  </div>

  <div class="login-row">
    <!-- Owner Panel -->
    <div class="login-panel panel-owner">
      <div class="panel-icon">👑</div>
      <div class="panel-title">OWNER</div>
      <div class="panel-desc">Full Access</div>
      <div class="err" id="err-owner"></div>
      <div class="pw-wrap">
        <input type="password" id="pw-owner" placeholder="كلمة المرور" onkeydown="if(event.key==='Enter')goOwner()"/>
        <button class="eye-btn" type="button" onclick="toggleEye('pw-owner')">👁</button>
      </div>
      <button class="login-btn" onclick="goOwner()">دخول</button>
    </div>

    <!-- Worker Panel -->
    <div class="login-panel panel-worker">
      <div class="panel-icon">🌸</div>
      <div class="panel-title">FLORIST</div>
      <div class="panel-desc">Sales Recording</div>
      <div class="err" id="err-worker"></div>
      <div class="pw-wrap">
        <input type="password" id="pw-worker" placeholder="كلمة المرور" onkeydown="if(event.key==='Enter')goWorker()"/>
        <button class="eye-btn" type="button" onclick="toggleEye('pw-worker')">👁</button>
      </div>
      <button class="login-btn" onclick="goWorker()">دخول</button>
    </div>
  </div>
</div>

<!-- Theme Switcher Button -->
<button class="theme-switcher" id="theme-switcher" title="Change Background">🎨</button>

<script>
// Petals
(function(){
  const wrap=document.getElementById('petals');
  const colors=['rgba(255,182,193,0.7)','rgba(255,209,220,0.6)','rgba(255,255,255,0.5)','rgba(255,228,181,0.6)','rgba(212,168,67,0.5)'];
  const count=25;
  for(let i=0;i<count;i++){
    const p=document.createElement('div');
    p.className='petal';
    const size=5+Math.random()*10;
    const color=colors[Math.floor(Math.random()*colors.length)];
    p.style.cssText=`
      left:${Math.random()*110-5}vw;
      width:${size}px;height:${size*1.3}px;
      background:${color};
      animation-duration:${10+Math.random()*14}s;
      animation-delay:${Math.random()*18}s;
    `;
    wrap.appendChild(p);
  }
})();

function toggleEye(id){
  const inp=document.getElementById(id);
  inp.type=inp.type==='password'?'text':'password';
}

async function goOwner(){
  const pw=document.getElementById('pw-owner').value.trim();
  const err=document.getElementById('err-owner');
  if(!pw)return;
  const btn=document.querySelector('.panel-owner .login-btn');
  btn.textContent='...';btn.disabled=true;
  try{
    const r=await fetch('/auth',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({p:pw})});
    const d=await r.json();
    if(d.ok){location.href='/';}
    else{
      err.textContent='❌ كلمة المرور غير صحيحة';
      document.getElementById('pw-owner').value='';
      btn.textContent='دخول';btn.disabled=false;
    }
  }catch(e){
    err.textContent='❌ خطأ في الاتصال';
    btn.textContent='دخول';btn.disabled=false;
  }
}

async function goWorker(){
  const pw=document.getElementById('pw-worker').value.trim();
  const err=document.getElementById('err-worker');
  if(!pw)return;
  const btn=document.querySelector('.panel-worker .login-btn');
  btn.textContent='...';btn.disabled=true;
  try{
    const r=await fetch('/worker-auth',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({p:pw})});
    const d=await r.json();
    if(d.ok){location.href='/worker';}
    else{
      err.textContent='❌ كلمة المرور غير صحيحة';
      document.getElementById('pw-worker').value='';
      btn.textContent='دخول';btn.disabled=false;
    }
  }catch(e){
    err.textContent='❌ خطأ في الاتصال';
    btn.textContent='دخول';btn.disabled=false;
  }
}

// ── Dynamic Theme System ────────────────────────
const backgrounds = [
  `url('/background.jpg?t=0') center top / cover no-repeat fixed`,
  `url('/background.jpg?t=1') center center / cover no-repeat fixed`,
  `url('/background.jpg?t=2') center bottom / cover no-repeat fixed`
];
let bgIndex = 0;

function setBackground(index){
  const bgImg = document.querySelector('.bg-img');
  if(!bgImg) return;
  bgImg.style.background = backgrounds[index];
}

function extractDominantColor(){
  const canvas = document.createElement('canvas');
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = '/background.jpg?t=' + Date.now();
  img.onload = function(){
    const w = 120;
    const h = 120;
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, w, h);
    const imageData = ctx.getImageData(0, 0, w, h).data;
    let r = 0, g = 0, b = 0, edgeSum = 0;
    const getIdx = (x,y) => (y*w + x) * 4;
    for(let y = 0; y < h; y++){
      for(let x = 0; x < w; x++){
        const idx = getIdx(x,y);
        const cr = imageData[idx];
        const cg = imageData[idx+1];
        const cb = imageData[idx+2];
        r += cr; g += cg; b += cb;
        if(x > 0){
          const li = getIdx(x-1,y);
          edgeSum += Math.abs(cr - imageData[li]) + Math.abs(cg - imageData[li+1]) + Math.abs(cb - imageData[li+2]);
        }
        if(y > 0){
          const ui = getIdx(x,y-1);
          edgeSum += Math.abs(cr - imageData[ui]) + Math.abs(cg - imageData[ui+1]) + Math.abs(cb - imageData[ui+2]);
        }
      }
    }
    const pixelCount = w * h;
    r = Math.round(r / pixelCount);
    g = Math.round(g / pixelCount);
    b = Math.round(b / pixelCount);
    const edgeDensity = edgeSum / (pixelCount * 255 * 2);
    updateThemeColors(r, g, b, edgeDensity > 0.12);
  };
  img.onerror = function(){
    updateThemeColors(212,168,67, false);
  };
}

function updateThemeColors(r,g,b,sharp=false){
  const primary = `rgb(${r},${g},${b})`;
  const accent = `rgb(${Math.min(255, r + 28)},${Math.min(255, g + 16)},${Math.min(255, b + 6)})`;
  const isDark = (r*0.299 + g*0.587 + b*0.114) < 150;
  const text = isDark ? 'rgba(255,255,255,0.92)' : 'rgba(18,18,18,0.94)';
  const bgOverlay = isDark ? `rgba(${Math.round(r*0.18)},${Math.round(g*0.18)},${Math.round(b*0.18)},0.72)` : `rgba(${Math.round(r*0.35)},${Math.round(g*0.35)},${Math.round(b*0.35)},0.32)`;
  const lightOverlay = isDark ? 'rgba(20,20,20,0.18)' : 'rgba(255,255,255,0.24)';
  const cardBg = isDark ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.88)';
  const panelRadius = sharp ? '16px' : '28px';
  const buttonRadius = sharp ? '16px' : '50%';

  document.documentElement.style.setProperty('--primary-color', primary);
  document.documentElement.style.setProperty('--accent-color', accent);
  document.documentElement.style.setProperty('--accent-rgb', `${r},${g},${b}`);
  document.documentElement.style.setProperty('--bg-overlay', bgOverlay);
  document.documentElement.style.setProperty('--light-overlay', lightOverlay);
  document.documentElement.style.setProperty('--card-bg', cardBg);
  document.documentElement.style.setProperty('--text-primary', text);
  document.documentElement.style.setProperty('--panel-radius', panelRadius);
  document.documentElement.style.setProperty('--button-radius', buttonRadius);
  document.documentElement.style.setProperty('--border-style', sharp ? '16px' : '24px');
  document.documentElement.classList.toggle('sharp-theme', sharp);
}

function changeBackground(){
  bgIndex = (bgIndex + 1) % backgrounds.length;
  setBackground(bgIndex);
  setTimeout(extractDominantColor, 120);
}

document.addEventListener('DOMContentLoaded', function(){
  setBackground(bgIndex);
  extractDominantColor();
  const switcherBtn = document.getElementById('theme-switcher');
  if(switcherBtn){
    switcherBtn.addEventListener('click', changeBackground);
  }
});
</script>
</body>
</html>"""

