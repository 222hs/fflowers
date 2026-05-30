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

/* ── Sections screen ── */
#sectionsScreen{
  position:fixed;inset:0;z-index:150;
  background:linear-gradient(170deg,#100e09 0%,#0d0b07 55%,#0a080c 100%);
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  gap:0;padding:32px 20px;
  opacity:0;pointer-events:none;
  transition:opacity .6s ease;
}
#sectionsScreen.show{opacity:1;pointer-events:all;}
.sec-eyebrow{
  font-size:9px;color:rgba(255,255,255,.22);
  letter-spacing:5px;text-transform:uppercase;
  margin-bottom:10px;
  opacity:0;transition:opacity .8s ease .15s;
}
#sectionsScreen.show .sec-eyebrow{opacity:1;}
.sec-title{
  font-family:'Playfair Display',serif;font-size:26px;font-weight:700;
  color:#e2c06a;letter-spacing:1px;text-align:center;
  text-shadow:0 0 50px rgba(212,168,67,.45);
  margin-bottom:32px;
  opacity:0;transform:translateY(-10px);
  transition:opacity .8s ease .05s, transform .9s cubic-bezier(.22,1,.36,1) .05s;
}
#sectionsScreen.show .sec-title{opacity:1;transform:none;}
.sec-grid{
  display:grid;grid-template-columns:1fr 1fr;
  gap:14px;width:100%;max-width:360px;
}
.sec-card{
  border-radius:20px;padding:26px 14px 22px;
  text-align:center;cursor:pointer;
  border:1px solid rgba(255,255,255,.08);
  background:rgba(255,255,255,.04);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  box-shadow:0 8px 32px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.07);
  will-change:transform;
  touch-action:manipulation;-webkit-tap-highlight-color:transparent;
  transition:transform .3s cubic-bezier(.34,1.4,.64,1),
             background .3s, border-color .3s, box-shadow .3s;
}
.sec-card:active{transform:scale(.93);}
.sec-card:hover{
  transform:scale(1.05) translateY(-3px);
  background:rgba(255,255,255,.09);
  box-shadow:0 16px 48px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.12);
}
.sec-emoji{font-size:34px;display:block;margin-bottom:12px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.4));}
.sec-label{font-size:14px;font-weight:900;color:#fff;letter-spacing:.5px;}
.sec-sub{font-size:9px;color:rgba(255,255,255,.30);margin-top:5px;letter-spacing:2px;text-transform:uppercase;}
.sec-back{
  position:fixed;top:20px;right:20px;
  width:38px;height:38px;border-radius:50%;border:none;cursor:pointer;
  background:rgba(255,255,255,.06);backdrop-filter:blur(12px);
  color:rgba(255,255,255,.5);font-size:16px;
  display:flex;align-items:center;justify-content:center;
  border:1px solid rgba(255,255,255,.08);
  transition:all .3s;touch-action:manipulation;
}
.sec-back:hover{background:rgba(255,255,255,.14);color:#fff;border-color:rgba(255,255,255,.18);}

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

<!-- Sections screen -->
<div id="sectionsScreen">
  <div class="sec-eyebrow">FAIROSE FLOWERS</div>
  <div class="sec-title">اختر قسماً</div>
  <div class="sec-grid" id="secGrid"></div>
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

// ── Build section grid ──
(function(){
  const grid=document.getElementById('secGrid');
  SECTIONS.forEach((s,i)=>{
    const el=document.createElement('div');
    el.className='sec-card';
    el.style.cssText+=`border-color:${s.color.replace('.18','.35')};background:${s.color};opacity:0;transform:translateY(32px) scale(0.92);`;
    el.innerHTML=`<span class="sec-emoji">${s.emoji}</span>
      <div class="sec-label">${s.label}</div>
      <div class="sec-sub">${s.sub}</div>`;
    el.addEventListener('click',()=>openSection(s));
    grid.appendChild(el);
  });
})();

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
  // Stagger card entrance
  document.querySelectorAll('.sec-card').forEach((c,i)=>{
    setTimeout(()=>{
      c.style.transition='opacity .55s ease, transform .65s cubic-bezier(.34,1.4,.64,1)';
      c.style.opacity='1';
      c.style.transform='none';
    }, 200 + i*110);
  });
}

function backToShop(){
  document.getElementById('sectionsScreen').classList.remove('show');
  const bg  = document.querySelector('.bg-img');
  const vig = document.getElementById('vignette');
  document.getElementById('doorGlow').classList.remove('on');
  bg.classList.remove('approaching');
  vig.classList.remove('show');
  // Reset cards for next entry
  document.querySelectorAll('.sec-card').forEach(c=>{
    c.style.transition='none';
    c.style.opacity='0';
    c.style.transform='translateY(32px) scale(0.92)';
  });
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

