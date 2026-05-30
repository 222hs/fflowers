from config import *

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>فيروز فلورز</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{height:100%;overflow:hidden;font-family:'Tajawal',sans-serif;}

/* Full background image */
.bg-img{
  position:fixed;inset:0;z-index:0;
  background:url('/background.jpg') center center/cover no-repeat;
  animation:kenBurns 22s ease-in-out infinite alternate;
}
@keyframes kenBurns{from{transform:scale(1);}to{transform:scale(1.07);}}

/* ── Cinematic approach — slow, deliberate, premium ── */
.bg-img.approaching{
  animation:cinematicPush 4.8s linear forwards;
  transform-origin:50% 55%;
}
@keyframes cinematicPush{
  /* Phase 1 — establishing: barely any movement, like standing and looking */
  0%   { transform:scale(1);    filter:brightness(1) saturate(1);
         animation-timing-function:cubic-bezier(.55,0,.8,.95); }
  /* Phase 2 — first steps: scene starts to grow */
  12%  { transform:scale(1.06); filter:brightness(1) saturate(1.02);
         animation-timing-function:cubic-bezier(.45,0,.65,.98); }
  /* Phase 3 — walking: confident pace building */
  28%  { transform:scale(1.20); filter:brightness(1.01) saturate(1.06);
         animation-timing-function:cubic-bezier(.38,0,.55,1); }
  46%  { transform:scale(1.48); filter:brightness(1.03) saturate(1.12);
         animation-timing-function:cubic-bezier(.32,0,.48,1); }
  /* Phase 4 — approaching door: scene fills the frame */
  62%  { transform:scale(1.86); filter:brightness(1.06) saturate(1.18);
         animation-timing-function:cubic-bezier(.25,0,.38,1); }
  /* Phase 5 — slowing at door: deliberate deceleration */
  74%  { transform:scale(2.22); filter:brightness(1.14) saturate(1.26);
         animation-timing-function:cubic-bezier(.18,0,.25,1); }
  83%  { transform:scale(2.52); filter:brightness(1.30) saturate(1.35) sepia(.05);
         animation-timing-function:cubic-bezier(.12,0,.18,1); }
  /* Phase 6 — at the door: warmth floods in */
  90%  { transform:scale(2.74); filter:brightness(1.60) saturate(1.45) sepia(.10); }
  95%  { transform:scale(2.92); filter:brightness(2.10) saturate(1.52) sepia(.08); }
  100% { transform:scale(3.18); filter:brightness(3.20) saturate(1.60) blur(4px); }
}

/* ── Cinematic vignette — lens edge darkening ── */
#vignette{
  position:fixed;inset:0;z-index:4;pointer-events:none;
  background:radial-gradient(ellipse 90% 82% at 50% 50%,transparent 42%,rgba(0,0,0,.72) 100%);
  opacity:0;transition:opacity 2s ease;
}
#vignette.show{opacity:1;}

/* ── Door warm-light bloom ── */
#doorGlow{
  position:fixed;inset:0;z-index:7;pointer-events:none;opacity:0;
}
#doorGlow.on{
  animation:doorBloom 1.9s cubic-bezier(.18,0,.28,1) forwards;
}
@keyframes doorBloom{
  0%  { opacity:0;
        background:radial-gradient(ellipse 10% 15% at 50% 54%,rgba(255,218,90,.9) 0%,transparent 100%); }
  12% { opacity:1;
        background:radial-gradient(ellipse 22% 32% at 50% 54%,rgba(255,215,80,1) 0%,rgba(255,195,55,.4) 55%,transparent 100%); }
  30% { opacity:1;
        background:
          radial-gradient(ellipse 6% 10% at 50% 54%,rgba(255,255,230,1) 0%,transparent 100%),
          radial-gradient(ellipse 42% 58% at 50% 54%,rgba(255,210,70,.98) 0%,rgba(255,180,40,.3) 58%,transparent 100%); }
  55% { opacity:1;
        background:
          radial-gradient(ellipse 9% 14% at 50% 54%,rgba(255,255,245,1) 0%,transparent 100%),
          radial-gradient(ellipse 72% 90% at 50% 54%,rgba(255,218,100,1) 0%,rgba(255,190,55,.5) 52%,transparent 88%); }
  78% { opacity:1;
        background:
          radial-gradient(ellipse 12% 18% at 50% 54%,rgba(255,255,255,1) 0%,transparent 100%),
          radial-gradient(ellipse 110% 130% at 50% 54%,rgba(255,228,130,1) 0%,rgba(255,205,80,.55) 48%,transparent 90%); }
  100%{ opacity:.65;
        background:radial-gradient(ellipse 165% 185% at 50% 54%,rgba(255,242,210,1) 0%,transparent 94%); }
}

/* Dark overlay */
.bg-overlay{
  position:fixed;inset:0;z-index:1;
  background:linear-gradient(
    to bottom,
    rgba(0,0,0,0.05) 0%,
    rgba(0,0,0,0.0) 40%,
    rgba(0,0,0,0.35) 100%
  );
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

/* Two cards row */
.login-row{
  display:flex;gap:14px;width:100%;max-width:700px;
  flex-wrap:wrap;justify-content:center;
}

@keyframes cardIn{from{opacity:0;transform:translateY(30px) scale(.95);}to{opacity:1;transform:translateY(0) scale(1);}}

.login-panel{
  flex:1;min-width:270px;max-width:320px;
  border-radius:24px;
  padding:30px 24px;
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
  background:rgba(255,255,255,0.10);
  border:1px solid rgba(212,168,67,0.4);
  animation-delay:.05s;
}
/* Worker panel — rose */
.panel-worker{
  background:rgba(255,255,255,0.08);
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

/* ── Enter button — minimal luxury ── */
#enterArea{
  position:fixed;bottom:88px;left:0;right:0;z-index:50;
  display:flex;flex-direction:column;align-items:center;gap:14px;
  pointer-events:none;opacity:0;
  transition:opacity .8s cubic-bezier(.4,0,.2,1);
}
#enterArea.show{opacity:1;pointer-events:all;}
#enterBtn{
  padding:17px 52px;border-radius:60px;
  background:rgba(255,255,255,.07);
  backdrop-filter:blur(28px) saturate(1.5);
  -webkit-backdrop-filter:blur(28px) saturate(1.5);
  border:1px solid rgba(255,255,255,.18);
  color:#fff;font-family:'Tajawal',sans-serif;
  font-size:15px;font-weight:700;letter-spacing:4px;
  cursor:pointer;
  box-shadow:0 8px 40px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.12);
  animation:enterBreath 3.5s ease-in-out infinite;
  touch-action:manipulation;-webkit-tap-highlight-color:transparent;
  transition:background .3s, border-color .3s, box-shadow .3s;
}
#enterBtn:active{transform:scale(.96);opacity:.85;}
@keyframes enterBreath{
  0%,100%{
    box-shadow:0 8px 40px rgba(0,0,0,.25),0 0 0 0 rgba(255,255,255,.06),inset 0 1px 0 rgba(255,255,255,.12);
    border-color:rgba(255,255,255,.18);
  }
  50%{
    box-shadow:0 8px 40px rgba(0,0,0,.25),0 0 0 12px rgba(255,255,255,0),inset 0 1px 0 rgba(255,255,255,.12);
    border-color:rgba(255,255,255,.32);
  }
}
#enterHint{font-size:9px;color:rgba(255,255,255,.22);letter-spacing:5px;text-transform:uppercase;}

/* ── Warm flash overlay (golden-white, not clinical white) ── */
#flashEl{
  position:fixed;inset:0;z-index:200;
  background:radial-gradient(ellipse at 50% 54%,#fffcf2 0%,#fff8e6 45%,#fffaf0 100%);
  opacity:0;pointer-events:none;
  transition:opacity .5s cubic-bezier(.4,0,.2,1);
}
#flashEl.on{opacity:1;}

/* ── Sections screen — shop interior ── */
#sectionsScreen{
  position:fixed;inset:0;z-index:150;
  background:#0b0805;
  opacity:0;pointer-events:none;
  transition:opacity .6s ease;
  overflow:hidden;
}
#sectionsScreen.show{opacity:1;pointer-events:all;}
#shopSvg{
  position:absolute;top:0;left:0;
  width:100%;height:auto;
}
.sec-header{
  position:absolute;top:0;left:0;right:0;z-index:10;
  text-align:center;padding:14px 60px 12px;pointer-events:none;
  background:linear-gradient(to bottom,rgba(11,8,5,.92) 0%,rgba(11,8,5,0) 100%);
}
.sec-eyebrow-txt{
  font-size:8px;color:rgba(255,255,255,.18);
  letter-spacing:5px;text-transform:uppercase;margin-bottom:5px;
}
.sec-title-txt{
  font-family:'Playfair Display',serif;font-size:21px;font-weight:700;
  color:#e2c06a;letter-spacing:1px;
  text-shadow:0 0 28px rgba(212,168,67,.45);
}
/* SVG zone interaction */
.svgZone{cursor:pointer;}
.svgZone .zo{opacity:0;transition:opacity .32s ease;}
.svgZone.tapped .zo{opacity:1;}
/* Idle breathing glow per zone */
#svgZone0{animation:bR 4s   ease-in-out       infinite;}
#svgZone1{animation:bT 4.3s ease-in-out  .7s  infinite;}
#svgZone2{animation:bP 3.9s ease-in-out  .3s  infinite;}
#svgZone3{animation:bG 4.5s ease-in-out  1.1s infinite;}
@keyframes bR{0%,100%{filter:brightness(1)   drop-shadow(0 0 8px rgba(224,80,110,.18));}50%{filter:brightness(1.08) drop-shadow(0 0 22px rgba(224,80,110,.6));}}
@keyframes bT{0%,100%{filter:brightness(1)   drop-shadow(0 0 8px rgba(52,211,153,.16));}50%{filter:brightness(1.08) drop-shadow(0 0 20px rgba(52,211,153,.55));}}
@keyframes bP{0%,100%{filter:brightness(1)   drop-shadow(0 0 8px rgba(147,51,234,.18));}50%{filter:brightness(1.08) drop-shadow(0 0 22px rgba(147,51,234,.6));}}
@keyframes bG{0%,100%{filter:brightness(1)   drop-shadow(0 0 8px rgba(212,168,67,.18));}50%{filter:brightness(1.08) drop-shadow(0 0 22px rgba(212,168,67,.6));}}
/* Tap burst */
#svgZone0.tapped{animation:none;filter:brightness(1.6) drop-shadow(0 0 36px rgba(224,80,110,.98));}
#svgZone1.tapped{animation:none;filter:brightness(1.6) drop-shadow(0 0 36px rgba(52,211,153,.98));}
#svgZone2.tapped{animation:none;filter:brightness(1.6) drop-shadow(0 0 36px rgba(147,51,234,.98));}
#svgZone3.tapped{animation:none;filter:brightness(1.6) drop-shadow(0 0 36px rgba(212,168,67,.98));}
.sec-back{
  position:absolute;top:14px;right:16px;z-index:20;
  width:36px;height:36px;border-radius:50%;border:none;cursor:pointer;
  background:rgba(255,255,255,.07);backdrop-filter:blur(12px);
  color:rgba(255,255,255,.5);font-size:15px;
  display:flex;align-items:center;justify-content:center;
  border:1px solid rgba(255,255,255,.1);
  transition:all .3s;touch-action:manipulation;
}
.sec-back:hover{background:rgba(255,255,255,.14);color:#fff;}

/* ── Lock FAB ── */
#lockFab{
  position:fixed;bottom:28px;left:20px;z-index:999;
  width:52px;height:52px;border-radius:50%;border:none;
  background:rgba(10,15,25,0.75);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border:1.5px solid rgba(255,255,255,0.18);
  color:#fff;font-size:22px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 6px 24px rgba(0,0,0,0.55);
  transition:transform .25s cubic-bezier(.34,1.56,.64,1),
             background .25s,border-color .25s;
  touch-action:manipulation;
  -webkit-tap-highlight-color:transparent;
}
#lockFab:hover{
  background:rgba(20,30,50,0.92);
  border-color:rgba(212,168,67,0.55);
  transform:scale(1.1);
}
#lockFab:active{transform:scale(0.93);}

/* ── Backdrop ── */
#staffBd{
  position:fixed;inset:0;z-index:1000;
  background:rgba(0,0,0,0.52);
  backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
  opacity:0;pointer-events:none;
  transition:opacity .28s;
}
#staffBd.open{opacity:1;pointer-events:all;}

/* ── Bottom Sheet ── */
#staffSheet{
  position:fixed;bottom:0;left:0;right:0;z-index:1001;
  background:rgba(8,14,24,0.97);
  backdrop-filter:blur(40px) saturate(1.8);
  -webkit-backdrop-filter:blur(40px) saturate(1.8);
  border-radius:24px 24px 0 0;
  border-top:1px solid rgba(255,255,255,0.09);
  padding:0 16px max(20px,env(safe-area-inset-bottom));
  transform:translateY(100%);
  transition:transform .38s cubic-bezier(.32,1.2,.6,1);
  box-shadow:0 -20px 60px rgba(0,0,0,0.6);
}
#staffSheet.open{transform:translateY(0);}
.sheet-drag{
  width:38px;height:4px;border-radius:2px;
  background:rgba(255,255,255,0.16);
  margin:12px auto 16px;
}
.sheet-title{
  text-align:center;font-size:13px;font-weight:700;
  color:rgba(255,255,255,0.45);letter-spacing:2px;
  text-transform:uppercase;margin-bottom:16px;
}
/* make panels more compact inside sheet */
#staffSheet .login-row{flex-wrap:nowrap;gap:10px;max-width:480px;margin:0 auto 8px;}
#staffSheet .login-panel{min-width:0;flex:1;padding:20px 14px;}
@media(max-width:380px){
  #staffSheet .login-row{flex-direction:column;}
}
</style>
</head>
<body>
<div class="bg-img"></div>
<div class="bg-overlay"></div>
<div id="vignette"></div>
<div id="doorGlow"></div>
<div class="petals" id="petals"></div>

<!-- Enter button -->
<div id="enterArea">
  <button id="enterBtn" type="button">ادخل المحل</button>
  <div id="enterHint">FAIROSE FLOWERS</div>
</div>

<!-- Flash overlay -->
<div id="flashEl"></div>

<!-- Sections screen — shop interior illustration -->
<div id="sectionsScreen">
  <svg id="shopSvg" viewBox="0 0 400 720" preserveAspectRatio="xMidYMin meet" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="wBg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#1c1408"/><stop offset="100%" stop-color="#0e0a05"/>
      </linearGradient>
      <linearGradient id="fBg" x1=".5" y1="0" x2=".5" y2="1">
        <stop offset="0%" stop-color="#231608"/><stop offset="100%" stop-color="#110a04"/>
      </linearGradient>
      <radialGradient id="sL" cx="27%" cy="4%" r="52%">
        <stop offset="0%" stop-color="rgba(255,228,148,.2)"/><stop offset="100%" stop-color="rgba(0,0,0,0)"/>
      </radialGradient>
      <radialGradient id="sR" cx="73%" cy="4%" r="52%">
        <stop offset="0%" stop-color="rgba(255,228,148,.2)"/><stop offset="100%" stop-color="rgba(0,0,0,0)"/>
      </radialGradient>
    </defs>
    <!-- ── Room ── -->
    <rect width="400" height="720" fill="#0b0805"/>
    <rect x="0" y="0" width="400" height="254" fill="url(#wBg)"/>
    <polygon points="0,254 400,254 400,720 0,720" fill="url(#fBg)"/>
    <rect x="0" y="248" width="400" height="8" fill="#1e1408"/>
    <!-- Ceiling lights + cones -->
    <rect x="0" y="0" width="400" height="720" fill="url(#sL)"/>
    <rect x="0" y="0" width="400" height="720" fill="url(#sR)"/>
    <rect x="86" y="0" width="34" height="6" fill="#241808" rx="1"/>
    <rect x="280" y="0" width="34" height="6" fill="#241808" rx="1"/>
    <circle cx="103" cy="4" r="5" fill="#fff8e0" opacity=".92"/>
    <circle cx="297" cy="4" r="5" fill="#fff8e0" opacity=".92"/>
    <polygon points="103,9 62,254 144,254" fill="rgba(255,216,130,.055)"/>
    <polygon points="297,9 256,254 338,254" fill="rgba(255,216,130,.055)"/>
    <!-- Floor perspective lines -->
    <line x1="0"   y1="720" x2="200" y2="254" stroke="#190e04" stroke-width="1.2"/>
    <line x1="133" y1="720" x2="200" y2="254" stroke="#190e04" stroke-width=".8"/>
    <line x1="267" y1="720" x2="200" y2="254" stroke="#190e04" stroke-width=".8"/>
    <line x1="400" y1="720" x2="200" y2="254" stroke="#190e04" stroke-width="1.2"/>
    <line x1="0"   y1="450" x2="400" y2="450" stroke="rgba(255,255,255,.022)" stroke-width="1"/>
    <line x1="0"   y1="580" x2="400" y2="580" stroke="rgba(255,255,255,.022)" stroke-width="1"/>
    <!-- Wall divider -->
    <line x1="200" y1="0"   x2="200" y2="252" stroke="rgba(255,255,255,.07)" stroke-width="1"/>
    <line x1="200" y1="262" x2="200" y2="720" stroke="rgba(255,255,255,.04)" stroke-width="1"/>

    <!-- ══════════════════════════════════ -->
    <!-- ZONE 0 — باقات  (back-left wall) -->
    <!-- ══════════════════════════════════ -->
    <g id="svgZone0" class="svgZone">
      <rect x="3"  y="16" width="193" height="233" fill="#150f07" rx="2"/>
      <rect x="3"  y="82" width="193" height="5"   fill="#2c1c0c" rx="1"/>
      <rect x="3"  y="158" width="193" height="5"  fill="#2c1c0c" rx="1"/>
      <rect x="3"  y="235" width="193" height="10" fill="#2c1c0c" rx="1"/>
      <rect x="3"  y="16" width="5"   height="233" fill="rgba(0,0,0,.32)" rx="2"/>
      <!-- Top shelf flowers -->
      <rect x="29" y="70"  width="3" height="16" fill="#3a5e30" rx="1"/>
      <circle cx="28" cy="57"  r="12" fill="#b43658"/>
      <circle cx="34" cy="49"  r="9"  fill="#d05870" opacity=".9"/>
      <circle cx="21" cy="52"  r="8"  fill="#c24468" opacity=".95"/>
      <circle cx="35" cy="43"  r="5"  fill="#e888a2" opacity=".8"/>
      <rect x="80" y="68"  width="3" height="18" fill="#3a5e30" rx="1"/>
      <circle cx="79" cy="53"  r="13" fill="#df5e7c"/>
      <circle cx="87" cy="44"  r="9"  fill="#f08aa6" opacity=".9"/>
      <circle cx="71" cy="47"  r="9"  fill="#cf4c6a" opacity=".95"/>
      <circle cx="88" cy="38"  r="6"  fill="#f0a0be" opacity=".8"/>
      <rect x="148" y="70" width="3" height="16" fill="#3a5e30" rx="1"/>
      <circle cx="147" cy="57" r="11" fill="#be4468"/>
      <circle cx="154" cy="49" r="8"  fill="#de6e8e" opacity=".9"/>
      <circle cx="140" cy="52" r="8"  fill="#ae3458" opacity=".95"/>
      <!-- Middle shelf flowers -->
      <rect x="26"  y="146" width="3" height="16" fill="#3a5e30" rx="1"/>
      <circle cx="25"  cy="133" r="11" fill="#cc4c6e"/>
      <circle cx="32"  cy="125" r="8"  fill="#e67898" opacity=".9"/>
      <circle cx="18"  cy="128" r="8"  fill="#bc3c5e" opacity=".95"/>
      <rect x="82"  y="145" width="3" height="17" fill="#3a5e30" rx="1"/>
      <circle cx="81"  cy="131" r="12" fill="#e06082"/>
      <circle cx="89"  cy="122" r="9"  fill="#f08eae" opacity=".9"/>
      <circle cx="73"  cy="125" r="8"  fill="#d05072" opacity=".9"/>
      <rect x="149" y="147" width="3" height="15" fill="#3a5e30" rx="1"/>
      <circle cx="148" cy="134" r="10" fill="#b84062"/>
      <circle cx="155" cy="127" r="7"  fill="#d87090" opacity=".9"/>
      <!-- Label -->
      <rect  x="3"  y="168" width="193" height="68" fill="rgba(0,0,0,.4)"/>
      <text  x="99" y="202" text-anchor="middle" fill="rgba(255,255,255,.88)" font-family="Tajawal,sans-serif" font-size="18" font-weight="700">باقات</text>
      <text  x="99" y="221" text-anchor="middle" fill="rgba(255,255,255,.25)" font-family="sans-serif" font-size="9" letter-spacing="3">BOUQUETS</text>
      <!-- Active overlay -->
      <rect x="3" y="16" width="193" height="233" fill="rgba(224,80,110,.13)" class="zo" rx="2"/>
    </g>

    <!-- ══════════════════════════════════════ -->
    <!-- ZONE 2 — مجسمات  (back-right wall)   -->
    <!-- ══════════════════════════════════════ -->
    <g id="svgZone2" class="svgZone">
      <rect x="204" y="16" width="193" height="233" fill="#150f07" rx="2"/>
      <rect x="204" y="82"  width="193" height="5"  fill="#2c1c0c" rx="1"/>
      <rect x="204" y="158" width="193" height="5"  fill="#2c1c0c" rx="1"/>
      <rect x="204" y="235" width="193" height="10" fill="#2c1c0c" rx="1"/>
      <rect x="392" y="16" width="5"   height="233" fill="rgba(0,0,0,.32)" rx="2"/>
      <!-- Top shelf: geometric sculptures -->
      <polygon points="258,26 278,76 238,76" fill="#7c3aed" opacity=".87"/>
      <polygon points="258,26 278,76 268,51" fill="#9c5aed" opacity=".52"/>
      <circle  cx="258" cy="24" r="6"  fill="#ddd6fe" opacity=".92"/>
      <circle  cx="258" cy="24" r="2.5" fill="#fff"   opacity=".95"/>
      <circle  cx="344" cy="50" r="18" fill="#6d28d9" opacity=".82"/>
      <circle  cx="357" cy="40" r="12" fill="#9c5aed" opacity=".88"/>
      <circle  cx="331" cy="42" r="11" fill="#7c3aed" opacity=".9"/>
      <circle  cx="354" cy="62" r="7"  fill="#a78bfa" opacity=".75"/>
      <circle  cx="325" cy="58" r="5"  fill="#c4b5fd" opacity=".8"/>
      <!-- Middle shelf: abstract floral sculptures -->
      <rect    x="230" y="116" width="32" height="40" fill="#3c2870" rx="2" opacity=".85"/>
      <ellipse cx="246" cy="116" rx="16" ry="6"  fill="#5c3890" opacity=".9"/>
      <polygon points="246,90 255,114 237,114" fill="#9333ea" opacity=".88"/>
      <polygon points="246,90 262,108 230,108" fill="#7c3aed" opacity=".58"/>
      <circle  cx="246" cy="87"  r="8"  fill="#e9d5ff" opacity=".95"/>
      <circle  cx="246" cy="79"  r="4"  fill="#fff"    opacity=".8"/>
      <rect    x="349" y="88"  width="20" height="62" fill="#4c1d95" rx="3" opacity=".88"/>
      <ellipse cx="359" cy="88"  rx="17" ry="6"  fill="#6d28d9" opacity=".9"/>
      <circle  cx="359" cy="78"  r="13" fill="#9333ea" opacity=".85"/>
      <circle  cx="359" cy="63"  r="8"  fill="#c4b5fd" opacity=".9"/>
      <circle  cx="359" cy="53"  r="4"  fill="#e9d5ff" opacity=".95"/>
      <!-- Label -->
      <rect  x="204" y="168" width="193" height="68" fill="rgba(0,0,0,.4)"/>
      <text  x="300" y="202" text-anchor="middle" fill="rgba(255,255,255,.88)" font-family="Tajawal,sans-serif" font-size="17" font-weight="700">مجسمات 3D</text>
      <text  x="300" y="221" text-anchor="middle" fill="rgba(255,255,255,.25)" font-family="sans-serif" font-size="9" letter-spacing="3">SCULPTURES</text>
      <rect x="204" y="16" width="193" height="233" fill="rgba(147,51,234,.12)" class="zo" rx="2"/>
    </g>

    <!-- ══════════════════════════════════════ -->
    <!-- ZONE 1 — استاندات  (floor left)       -->
    <!-- ══════════════════════════════════════ -->
    <g id="svgZone1" class="svgZone">
      <rect x="0" y="262" width="200" height="458" fill="rgba(0,0,0,0)"/>
      <!-- Stand 1 -->
      <ellipse cx="68"  cy="668" rx="30" ry="10" fill="#1c1208"/>
      <ellipse cx="68"  cy="664" rx="26" ry="8"  fill="#281a0c"/>
      <rect    x="63"   y="490" width="10" height="177" fill="#382412" rx="2"/>
      <ellipse cx="68"  cy="490" rx="36" ry="13" fill="#4c3418"/>
      <ellipse cx="68"  cy="483" rx="33" ry="11" fill="#5e4624"/>
      <circle  cx="56"  cy="462" r="16" fill="#4ade80" opacity=".88"/>
      <circle  cx="72"  cy="452" r="13" fill="#86efac" opacity=".84"/>
      <circle  cx="46"  cy="456" r="12" fill="#22c55e" opacity=".9"/>
      <circle  cx="80"  cy="463" r="10" fill="#6ee7b7" opacity=".8"/>
      <circle  cx="62"  cy="444" r="8"  fill="#bbf7d0" opacity=".85"/>
      <ellipse cx="40"  cy="480" rx="11" ry="5"  fill="#15803d" opacity=".6" transform="rotate(-28,40,480)"/>
      <ellipse cx="96"  cy="479" rx="11" ry="5"  fill="#15803d" opacity=".6" transform="rotate(28,96,479)"/>
      <!-- Stand 2 (slightly back, right) -->
      <ellipse cx="152" cy="646" rx="24" ry="8"  fill="#1c1208"/>
      <ellipse cx="152" cy="642" rx="20" ry="6"  fill="#281a0c"/>
      <rect    x="148"  y="500" width="8"  height="144" fill="#382412" rx="2"/>
      <ellipse cx="152" cy="500" rx="28" ry="10" fill="#4c3418"/>
      <ellipse cx="152" cy="494" rx="25" ry="9"  fill="#5e4624"/>
      <circle  cx="142" cy="474" r="13" fill="#34d399" opacity=".88"/>
      <circle  cx="156" cy="465" r="10" fill="#6ee7b7" opacity=".84"/>
      <circle  cx="134" cy="468" r="9"  fill="#10b981" opacity=".9"/>
      <circle  cx="163" cy="476" r="8"  fill="#a7f3d0" opacity=".8"/>
      <!-- Ambient teal -->
      <ellipse cx="100" cy="560" rx="90" ry="120" fill="rgba(52,211,153,.055)"/>
      <!-- Label -->
      <rect  x="14"  y="686" width="172" height="28" fill="rgba(0,0,0,.62)" rx="14"/>
      <text  x="100" y="704" text-anchor="middle" fill="rgba(255,255,255,.88)" font-family="Tajawal,sans-serif" font-size="15" font-weight="700">استاندات</text>
      <rect x="0" y="262" width="200" height="458" fill="rgba(52,211,153,.08)" class="zo"/>
    </g>

    <!-- ══════════════════════════════════════ -->
    <!-- ZONE 3 — شرايط  (floor right)         -->
    <!-- ══════════════════════════════════════ -->
    <g id="svgZone3" class="svgZone">
      <rect x="200" y="262" width="200" height="458" fill="rgba(0,0,0,0)"/>
      <!-- Ribbon rack frame -->
      <rect x="222" y="330" width="5"   height="318" fill="#382412" rx="2"/>
      <rect x="373" y="330" width="5"   height="318" fill="#382412" rx="2"/>
      <rect x="220" y="330" width="160" height="6"   fill="#4a3018" rx="2"/>
      <rect x="220" y="420" width="160" height="6"   fill="#4a3018" rx="2"/>
      <rect x="220" y="510" width="160" height="6"   fill="#4a3018" rx="2"/>
      <rect x="220" y="600" width="160" height="6"   fill="#4a3018" rx="2"/>
      <!-- Ribbon rolls — bar 1 (y≈333) -->
      <ellipse cx="248" cy="336" rx="16" ry="8"  fill="#d4a843"/><ellipse cx="248" cy="336" rx="10" ry="5" fill="#b88520"/><ellipse cx="248" cy="336" rx="4" ry="2" fill="#0b0805"/>
      <ellipse cx="285" cy="335" rx="14" ry="7"  fill="#e06888"/><ellipse cx="285" cy="335" rx="9"  ry="4" fill="#c4526a"/><ellipse cx="285" cy="335" rx="3" ry="2" fill="#0b0805"/>
      <ellipse cx="320" cy="334" rx="13" ry="7"  fill="#60a5fa"/><ellipse cx="320" cy="334" rx="8"  ry="4" fill="#3b82f6"/><ellipse cx="320" cy="334" rx="3" ry="2" fill="#0b0805"/>
      <ellipse cx="353" cy="334" rx="12" ry="6"  fill="#c084fc"/><ellipse cx="353" cy="334" rx="7"  ry="3" fill="#9333ea"/><ellipse cx="353" cy="334" rx="3" ry="2" fill="#0b0805"/>
      <!-- Hanging strands bar1→bar2 -->
      <path d="M245,340 Q241,383 247,420" stroke="#e8c040" stroke-width="1.5" fill="none" opacity=".52"/>
      <path d="M256,341 Q260,382 254,419" stroke="#c89820" stroke-width="1.5" fill="none" opacity=".52"/>
      <path d="M282,339 Q278,381 284,419" stroke="#e86880" stroke-width="1.5" fill="none" opacity=".52"/>
      <path d="M292,338 Q296,380 290,418" stroke="#c4526a" stroke-width="1.5" fill="none" opacity=".52"/>
      <path d="M318,337 Q314,380 320,418" stroke="#60a5fa" stroke-width="1.5" fill="none" opacity=".52"/>
      <!-- Ribbon rolls — bar 2 (y≈423) -->
      <ellipse cx="236" cy="426" rx="15" ry="7"  fill="#fbbf24"/><ellipse cx="236" cy="426" rx="9" ry="4"  fill="#d97706"/><ellipse cx="236" cy="426" rx="4" ry="2" fill="#0b0805"/>
      <ellipse cx="270" cy="425" rx="16" ry="7"  fill="#d4a843"/><ellipse cx="270" cy="425" rx="10" ry="4" fill="#b88520"/><ellipse cx="270" cy="425" rx="4" ry="2" fill="#0b0805"/>
      <ellipse cx="307" cy="424" rx="13" ry="7"  fill="#fb923c"/><ellipse cx="307" cy="424" rx="8"  ry="4" fill="#ea7218"/><ellipse cx="307" cy="424" rx="3" ry="2" fill="#0b0805"/>
      <ellipse cx="342" cy="424" rx="12" ry="6"  fill="#e06888"/><ellipse cx="342" cy="424" rx="7"  ry="3" fill="#c4526a"/><ellipse cx="342" cy="424" rx="3" ry="2" fill="#0b0805"/>
      <!-- Strands bar2→bar3 -->
      <path d="M233,430 Q229,472 235,510" stroke="#fbbf24" stroke-width="1.5" fill="none" opacity=".5"/>
      <path d="M268,429 Q272,471 266,509" stroke="#d4a843" stroke-width="1.5" fill="none" opacity=".5"/>
      <path d="M304,428 Q300,470 306,509" stroke="#fb923c" stroke-width="1.5" fill="none" opacity=".5"/>
      <!-- Ribbon rolls — bar 3 (y≈513) -->
      <ellipse cx="245" cy="516" rx="14" ry="7"  fill="#a78bfa"/><ellipse cx="245" cy="516" rx="8"  ry="4" fill="#7c3aed"/><ellipse cx="245" cy="516" rx="3" ry="2" fill="#0b0805"/>
      <ellipse cx="280" cy="515" rx="15" ry="7"  fill="#d4a843"/><ellipse cx="280" cy="515" rx="9"  ry="4" fill="#b88520"/><ellipse cx="280" cy="515" rx="4" ry="2" fill="#0b0805"/>
      <ellipse cx="315" cy="515" rx="13" ry="6"  fill="#f472b6"/><ellipse cx="315" cy="515" rx="7"  ry="3" fill="#ec4899"/><ellipse cx="315" cy="515" rx="3" ry="2" fill="#0b0805"/>
      <ellipse cx="348" cy="514" rx="12" ry="6"  fill="#60a5fa"/><ellipse cx="348" cy="514" rx="7"  ry="3" fill="#3b82f6"/><ellipse cx="348" cy="514" rx="3" ry="2" fill="#0b0805"/>
      <!-- Ambient gold glow -->
      <ellipse cx="300" cy="520" rx="95" ry="130" fill="rgba(212,168,67,.055)"/>
      <!-- Label -->
      <rect  x="214" y="686" width="172" height="28" fill="rgba(0,0,0,.62)" rx="14"/>
      <text  x="300" y="704" text-anchor="middle" fill="rgba(255,255,255,.88)" font-family="Tajawal,sans-serif" font-size="15" font-weight="700">شرايط</text>
      <rect x="200" y="262" width="200" height="458" fill="rgba(212,168,67,.08)" class="zo"/>
    </g>

  </svg>
  <div class="sec-header">
    <div class="sec-eyebrow-txt">FAIROSE FLOWERS</div>
    <div class="sec-title-txt">اختر قسماً</div>
  </div>
  <button class="sec-back" onclick="backToShop()">←</button>
</div>

<!-- Lock FAB -->
<button id="lockFab" type="button" aria-label="دخول الموظفين">🔐</button>

<!-- Backdrop -->
<div id="staffBd" onclick="closeSheet()"></div>

<!-- Staff Sheet -->
<div id="staffSheet">
  <div class="sheet-drag"></div>
  <div class="sheet-title">دخول فريق العمل</div>
  <div class="login-row">
    <!-- Owner -->
    <div class="login-panel panel-owner">
      <div class="panel-icon">👑</div>
      <div class="panel-title">المالك</div>
      <div class="panel-desc">صلاحيات كاملة</div>
      <div class="err" id="err-owner"></div>
      <div class="pw-wrap">
        <input type="password" id="pw-owner" placeholder="كلمة المرور" onkeydown="if(event.key==='Enter')goOwner()"/>
        <button class="eye-btn" type="button" onclick="toggleEye('pw-owner')">👁</button>
      </div>
      <button class="login-btn" onclick="goOwner()">دخول</button>
    </div>
    <!-- Worker -->
    <div class="login-panel panel-worker">
      <div class="panel-icon">🌸</div>
      <div class="panel-title">العامل</div>
      <div class="panel-desc">تسجيل المبيعات</div>
      <div class="err" id="err-worker"></div>
      <div class="pw-wrap">
        <input type="password" id="pw-worker" placeholder="كلمة المرور" onkeydown="if(event.key==='Enter')goWorker()"/>
        <button class="eye-btn" type="button" onclick="toggleEye('pw-worker')">👁</button>
      </div>
      <button class="login-btn" onclick="goWorker()">دخول</button>
    </div>
  </div>
</div>

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

// ── Sections config (add more here later) ──
const SECTIONS=[
  {id:'baqat',   label:'باقات',      sub:'Bouquets',    emoji:'💐', color:'rgba(249,168,212,.18)'},
  {id:'istandat',label:'استاندات',   sub:'Stands',      emoji:'🏺', color:'rgba(134,239,172,.18)'},
  {id:'mujasam', label:'مجسمات 3D',  sub:'Sculptures',  emoji:'🎨', color:'rgba(196,181,253,.18)'},
  {id:'sharayit',label:'شرايط',      sub:'Ribbons',     emoji:'🎀', color:'rgba(253,230,138,.18)'},
];

// ── SVG zone interactions ──
SECTIONS.forEach((s,i)=>{
  const zone=document.getElementById('svgZone'+i);
  if(!zone) return;
  zone.addEventListener('click',()=>{
    document.querySelectorAll('.svgZone').forEach(z=>z.classList.remove('tapped'));
    zone.classList.add('tapped');
    setTimeout(()=>{ zone.classList.remove('tapped'); openSection(s); }, 380);
  });
});

// ── Cinematic entry sequence ──
function startEntry(){
  const bg    = document.querySelector('.bg-img');
  const flash = document.getElementById('flashEl');
  const glow  = document.getElementById('doorGlow');
  const vig   = document.getElementById('vignette');

  document.getElementById('enterArea').classList.remove('show');
  bg.classList.add('approaching');

  // Vignette fades in — cinematic framing (1.4s)
  setTimeout(()=>{ vig.classList.add('show'); }, 1400);

  // Warm door light bloom at ~76% of walk (3.6s)
  setTimeout(()=>{ glow.classList.add('on'); }, 3600);

  // Warm golden flash just as entering (4.4s)
  setTimeout(()=>{ flash.classList.add('on'); }, 4400);

  // Sections appear (4.85s) — flash fades after
  setTimeout(()=>{
    showSections();
    setTimeout(()=>{
      flash.classList.remove('on');
      glow.classList.remove('on');
    }, 550);
  }, 4850);
}

function showSections(){
  document.getElementById('enterArea').classList.remove('show');
  document.getElementById('sectionsScreen').classList.add('show');
}

function backToShop(){
  document.getElementById('sectionsScreen').classList.remove('show');
  const bg  = document.querySelector('.bg-img');
  const vig = document.getElementById('vignette');
  document.getElementById('doorGlow').classList.remove('on');
  bg.classList.remove('approaching');
  vig.classList.remove('show');
  // Reset SVG zone tap states
  document.querySelectorAll('.svgZone').forEach(z=>z.classList.remove('tapped'));
  void bg.offsetWidth;
  setTimeout(()=>document.getElementById('enterArea').classList.add('show'), 400);
}

function openSection(s){
  // Phase 4 will open Google Drive catalog here
  alert('قريباً: كتالوج '+s.label+' 📸');
}

// Show enter button after 1.2s
setTimeout(()=>document.getElementById('enterArea').classList.add('show'),1200);
document.getElementById('enterBtn').addEventListener('click',startEntry);

// ── Sheet open/close ──
function openSheet(){
  document.getElementById('staffBd').classList.add('open');
  document.getElementById('staffSheet').classList.add('open');
}
function closeSheet(){
  document.getElementById('staffBd').classList.remove('open');
  document.getElementById('staffSheet').classList.remove('open');
}
document.getElementById('lockFab').addEventListener('click', openSheet);
document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeSheet(); });

// drag-down to close sheet
(function(){
  const sh=document.getElementById('staffSheet');
  let y0=0;
  sh.addEventListener('touchstart',e=>{y0=e.touches[0].clientY;},{passive:true});
  sh.addEventListener('touchend',e=>{
    if(e.changedTouches[0].clientY - y0 > 70) closeSheet();
  },{passive:true});
})();
</script>
</body>
</html>"""

