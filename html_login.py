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

.err{color:rgba(220,80,80,0.9);font-size:11px;min-height:16px;margin-bottom:8px;}

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
  padding:18px 58px;border-radius:60px;
  background:rgba(255,255,255,0.06);
  backdrop-filter:blur(28px) saturate(1.5);
  -webkit-backdrop-filter:blur(28px) saturate(1.5);
  border:1px solid rgba(255,255,255,0.22);
  color:#f5f0eb;font-family:'Playfair Display',serif;font-style:italic;
  font-size:17px;font-weight:400;letter-spacing:3px;
  cursor:pointer;
  box-shadow:0 0 40px rgba(255,255,255,0.04), inset 0 1px 0 rgba(255,255,255,0.12);
  animation:enterBreath 3.8s ease-in-out infinite alternate;
  touch-action:manipulation;-webkit-tap-highlight-color:transparent;
  transition:background .3s, border-color .3s, box-shadow .3s, transform .3s;
}
#enterBtn:hover,#enterBtn:active{
  background:rgba(255,255,255,0.11);
  box-shadow:0 0 60px rgba(212,168,67,0.18);
}
#enterBtn:active{transform:scale(.96);}
@keyframes enterBreath{
  0%{transform:scale(1);opacity:.85;}
  100%{transform:scale(1.025);opacity:1;}
}
#enterHint{
  display:flex;align-items:center;justify-content:center;gap:14px;
  font-family:'Tajawal',sans-serif;
  font-size:11px;color:rgba(255,255,255,0.28);
  letter-spacing:5px;text-transform:uppercase;
}
#enterHint::before,#enterHint::after{
  content:"";display:block;width:28px;height:1px;
  background:rgba(255,255,255,0.18);
}

/* ── Warm flash overlay (golden-white, not clinical white) ── */
#flashEl{
  position:fixed;inset:0;z-index:200;
  background:radial-gradient(ellipse at 50% 54%,#fffcf2 0%,#fff8e6 45%,#fffaf0 100%);
  opacity:0;pointer-events:none;
  transition:opacity .5s cubic-bezier(.4,0,.2,1);
}
#flashEl.on{opacity:1;}

/* ── Sections screen — shop exterior photo ── */
#sectionsScreen{
  position:fixed;inset:0;z-index:150;
  background:url('/background.jpg') center center/cover no-repeat;
  opacity:0;pointer-events:none;
  transition:opacity .6s ease;
  overflow:hidden;
}
#sectionsScreen.show{opacity:1;pointer-events:all;}
.sec-overlay{
  position:absolute;inset:0;
  background:linear-gradient(
    180deg,
    rgba(0,0,0,0.52) 0%,
    rgba(15,8,4,0.08) 38%,
    rgba(40,20,8,0.22) 70%,
    rgba(0,0,0,0.65) 100%
  );
}
.sec-header{
  position:absolute;top:0;left:0;right:0;z-index:10;
  text-align:center;padding:14px 60px 12px;pointer-events:none;
  background:linear-gradient(to bottom,rgba(0,0,0,.72) 0%,transparent 100%);
}
.sec-eyebrow-txt{
  font-size:9px;color:rgba(212,168,67,0.55);
  letter-spacing:6px;text-transform:uppercase;margin-bottom:6px;
}
.sec-title-txt{
  font-family:'Playfair Display',serif;font-style:italic;font-size:24px;font-weight:700;
  color:#f0e6d0;letter-spacing:1px;
  text-shadow:0 2px 24px rgba(0,0,0,0.6), 0 0 40px rgba(212,168,67,0.3);
}
/* ── Zone pins ── */
.zone-pin{
  position:absolute;
  display:flex;flex-direction:column;align-items:center;
  cursor:pointer;
  transform:translate(-50%,-50%);
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.pin-ring{
  position:absolute;
  width:62px;height:62px;
  border-radius:50%;
  animation:pinPulse 2.8s ease-in-out infinite;
}
.pin-core{
  width:22px;height:22px;
  border-radius:50%;
  position:relative;z-index:2;
  transition:transform .35s cubic-bezier(.34,1.56,.64,1),box-shadow .35s ease;
}
.pin-label{
  margin-top:12px;
  background:rgba(8,4,2,0.62);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
  border:1px solid rgba(255,255,255,0.16);
  border-radius:22px;
  padding:7px 18px 6px;
  text-align:center;
  color:#fff;
  font-family:'Tajawal',sans-serif;
  font-size:13px;font-weight:700;letter-spacing:0.5px;
  white-space:nowrap;
  transition:background .3s,border-color .3s;
}
.pin-label span{
  display:block;
  font-family:sans-serif;
  font-size:8px;letter-spacing:3px;
  color:rgba(212,168,67,0.6);
  text-transform:uppercase;
  margin-top:2px;
}
@keyframes pinPulse{
  0%,100%{transform:scale(1);opacity:.55;}
  50%{transform:scale(1.5);opacity:.1;}
}
#zonePin0 .pin-core{background:#f472b6;box-shadow:0 0 18px rgba(244,114,182,.75);}
#zonePin0 .pin-ring{border:2px solid rgba(244,114,182,.65);}
#zonePin1 .pin-core{background:#34d399;box-shadow:0 0 18px rgba(52,211,153,.75);}
#zonePin1 .pin-ring{border:2px solid rgba(52,211,153,.6);}
#zonePin2 .pin-core{background:#a78bfa;box-shadow:0 0 18px rgba(167,139,250,.75);}
#zonePin2 .pin-ring{border:2px solid rgba(167,139,250,.6);}
#zonePin3 .pin-core{background:#fbbf24;box-shadow:0 0 18px rgba(251,191,36,.75);}
#zonePin3 .pin-ring{border:2px solid rgba(251,191,36,.6);}
#zonePin0{left:23%;top:38%;}
#zonePin1{left:22%;top:68%;}
#zonePin2{left:77%;top:35%;}
#zonePin3{left:78%;top:65%;}
.zone-pin.tapped .pin-ring{
  animation:none;
  transform:scale(2.2);opacity:0;
  transition:transform .45s ease,opacity .45s ease;
}
.zone-pin.tapped .pin-core{transform:scale(1.7);}
.zone-pin.tapped .pin-label{background:rgba(0,0,0,.78);border-color:rgba(255,255,255,.3);}
.sec-back{
  position:absolute;top:14px;right:16px;z-index:20;
  width:40px;height:40px;border-radius:50%;cursor:pointer;
  background:rgba(0,0,0,0.45);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  color:rgba(255,255,255,0.6);font-size:16px;
  display:flex;align-items:center;justify-content:center;
  border:1px solid rgba(255,255,255,0.12);
  transition:all .3s;touch-action:manipulation;
}
.sec-back:hover{color:#f0e6d0;border-color:rgba(212,168,67,0.35);}

/* ── Lock FAB ── */
#lockFab{
  position:fixed;bottom:28px;left:20px;z-index:999;
  width:52px;height:52px;border-radius:50%;
  background:rgba(4,8,16,0.72);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border:1.5px solid rgba(255,255,255,0.12);
  color:#fff;font-size:22px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 4px 20px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04);
  transition:transform .25s cubic-bezier(.34,1.56,.64,1),
             background .25s,border-color .25s,box-shadow .25s;
  touch-action:manipulation;
  -webkit-tap-highlight-color:transparent;
}
#lockFab:hover{
  border-color:rgba(212,168,67,0.4);
  box-shadow:0 4px 28px rgba(0,0,0,0.6), 0 0 20px rgba(212,168,67,0.12);
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
  background:rgba(4,6,10,0.96);
  backdrop-filter:blur(40px) saturate(1.8);
  -webkit-backdrop-filter:blur(40px) saturate(1.8);
  border-radius:24px 24px 0 0;
  border-top:1px solid rgba(255,255,255,0.07);
  padding:0 16px max(20px,env(safe-area-inset-bottom));
  transform:translateY(100%);
  transition:transform .38s cubic-bezier(.32,1.2,.6,1);
  box-shadow:0 -24px 80px rgba(0,0,0,0.7), 0 -1px 0 rgba(255,255,255,0.06);
}
#staffSheet.open{transform:translateY(0);}
.sheet-drag{
  width:38px;height:4px;border-radius:2px;
  background:rgba(255,255,255,0.16);
  margin:12px auto 16px;
}
.sheet-title{
  text-align:center;font-size:11px;font-weight:700;
  font-family:'Tajawal',sans-serif;
  color:rgba(255,255,255,0.35);letter-spacing:3px;
  text-transform:uppercase;margin-bottom:16px;
}
/* make panels more compact inside sheet */
#staffSheet .login-row{flex-wrap:nowrap;gap:10px;max-width:480px;margin:0 auto 8px;}
#staffSheet .login-panel{min-width:0;flex:1;padding:20px 14px;}
/* refined inputs inside sheet — boutique underline style */
#staffSheet .pw-wrap input[type=password]{
  background:rgba(255,255,255,0.04);
  border:none;
  border-bottom:1px solid rgba(255,255,255,0.14);
  border-radius:0;
  padding:10px 4px;
  font-size:14px;color:#f0e6d0;
  letter-spacing:2px;outline:none;
}
#staffSheet .pw-wrap input[type=password]:focus{
  box-shadow:none;
  border-bottom-color:rgba(212,168,67,0.6);
}
#staffSheet .eye-btn{left:4px;}
/* refined buttons inside sheet — restrained gold/rose */
#staffSheet .login-btn{
  font-size:14px;letter-spacing:2px;
  border:1px solid rgba(212,168,67,0.35);
}
#staffSheet .panel-owner .login-btn{
  background:linear-gradient(135deg,rgba(212,168,67,0.92),rgba(196,144,48,0.92));
  border-color:rgba(212,168,67,0.5);
}
#staffSheet .panel-worker .login-btn{
  background:linear-gradient(135deg,rgba(232,121,138,0.92),rgba(196,86,106,0.92));
  border-color:rgba(232,121,138,0.45);
}
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

<!-- Sections screen — shop exterior photo with zone pins -->
<div id="sectionsScreen">
  <div class="sec-overlay"></div>
  <div class="zone-pin" id="zonePin0"><div class="pin-ring"></div><div class="pin-core"></div><div class="pin-label">باقات<span>Bouquets</span></div></div>
  <div class="zone-pin" id="zonePin1"><div class="pin-ring"></div><div class="pin-core"></div><div class="pin-label">استاندات<span>Stands</span></div></div>
  <div class="zone-pin" id="zonePin2"><div class="pin-ring"></div><div class="pin-core"></div><div class="pin-label">مجسمات 3D<span>Sculptures</span></div></div>
  <div class="zone-pin" id="zonePin3"><div class="pin-ring"></div><div class="pin-core"></div><div class="pin-label">شرايط<span>Ribbons</span></div></div>
  <div class="sec-header">
    <div class="sec-eyebrow-txt">FAIROSE FLOWERS</div>
    <div class="sec-title-txt">اختر قسمك</div>
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

// ── Zone pin interactions ──
SECTIONS.forEach((s,i)=>{
  const pin=document.getElementById('zonePin'+i);
  if(!pin) return;
  pin.addEventListener('click',()=>{
    document.querySelectorAll('.zone-pin').forEach(z=>z.classList.remove('tapped'));
    pin.classList.add('tapped');
    setTimeout(()=>{ pin.classList.remove('tapped'); openSection(s); }, 380);
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
  document.querySelectorAll('.zone-pin').forEach(z=>z.classList.remove('tapped'));
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

