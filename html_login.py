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

/* ── Approach animation (triggered by JS) ── */
.bg-img.approaching{
  animation:approachDoor 2.6s cubic-bezier(.15,.1,.25,1) forwards;
  transform-origin:50% 55%; /* center of the door */
}
@keyframes approachDoor{
  0%  {transform:scale(1);    filter:brightness(1)   blur(0px);}
  55% {transform:scale(1.6);  filter:brightness(1.08) blur(0px);}
  80% {transform:scale(2.3);  filter:brightness(1.4) blur(0px);}
  100%{transform:scale(3.2);  filter:brightness(2.2) blur(4px);}
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

/* ── Enter button ── */
#enterArea{
  position:fixed;bottom:100px;left:0;right:0;z-index:50;
  display:flex;flex-direction:column;align-items:center;gap:10px;
  pointer-events:none;opacity:0;
  transition:opacity .6s ease;
}
#enterArea.show{opacity:1;pointer-events:all;}
#enterBtn{
  padding:14px 36px;border-radius:50px;border:none;cursor:pointer;
  background:rgba(212,168,67,0.18);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
  border:1.5px solid rgba(212,168,67,0.55);
  color:#fff;font-family:'Tajawal',sans-serif;font-size:16px;font-weight:900;
  letter-spacing:1px;
  box-shadow:0 0 28px rgba(212,168,67,0.3);
  animation:enterPulse 2.2s ease-in-out infinite;
  touch-action:manipulation;-webkit-tap-highlight-color:transparent;
}
@keyframes enterPulse{
  0%,100%{box-shadow:0 0 22px rgba(212,168,67,.3),0 0 0 0 rgba(212,168,67,.25);}
  50%{box-shadow:0 0 36px rgba(212,168,67,.5),0 0 0 10px rgba(212,168,67,0);}
}
#enterHint{font-size:11px;color:rgba(255,255,255,.4);letter-spacing:2px;text-transform:uppercase;}

/* ── Flash overlay ── */
#flashEl{
  position:fixed;inset:0;z-index:200;
  background:#fff;opacity:0;pointer-events:none;
  transition:opacity .35s ease;
}
#flashEl.on{opacity:1;}

/* ── Sections screen ── */
#sectionsScreen{
  position:fixed;inset:0;z-index:150;
  background:linear-gradient(160deg,#0d1a18 0%,#0a1510 60%,#040d08 100%);
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  gap:24px;padding:32px 20px;
  opacity:0;pointer-events:none;
  transition:opacity .5s ease .1s;
}
#sectionsScreen.show{opacity:1;pointer-events:all;}
.sec-title{
  font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
  color:#d4a843;letter-spacing:1px;text-align:center;
  text-shadow:0 0 30px rgba(212,168,67,.4);
}
.sec-grid{
  display:grid;grid-template-columns:1fr 1fr;
  gap:12px;width:100%;max-width:360px;
}
.sec-card{
  border-radius:18px;padding:24px 14px;
  text-align:center;cursor:pointer;
  border:1px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.05);
  backdrop-filter:blur(12px);
  transition:transform .25s cubic-bezier(.34,1.56,.64,1),
             background .25s, border-color .25s;
  touch-action:manipulation;-webkit-tap-highlight-color:transparent;
}
.sec-card:active{transform:scale(.94);}
.sec-card:hover{transform:scale(1.04);background:rgba(255,255,255,.1);}
.sec-emoji{font-size:32px;display:block;margin-bottom:10px;}
.sec-label{font-size:14px;font-weight:900;color:#fff;}
.sec-sub{font-size:10px;color:rgba(255,255,255,.38);margin-top:3px;letter-spacing:1px;}
.sec-back{
  position:fixed;top:20px;right:20px;
  width:40px;height:40px;border-radius:50%;border:none;cursor:pointer;
  background:rgba(255,255,255,.08);backdrop-filter:blur(10px);
  color:rgba(255,255,255,.6);font-size:18px;
  display:flex;align-items:center;justify-content:center;
  transition:all .25s;touch-action:manipulation;
}
.sec-back:hover{background:rgba(255,255,255,.16);color:#fff;}

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
<div class="petals" id="petals"></div>


<!-- Enter button -->
<div id="enterArea">
  <button id="enterBtn" type="button">✨ ادخل المحل</button>
  <div id="enterHint">FAIROSE FLOWERS</div>
</div>

<!-- Flash overlay -->
<div id="flashEl"></div>

<!-- Sections screen (Phase 3 will replace with SVG) -->
<div id="sectionsScreen">
  <div class="sec-title">🌹 اختر قسماً</div>
  <div class="sec-grid" id="secGrid"></div>
  <button class="sec-back" onclick="backToShop()" title="رجوع">←</button>
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
  SECTIONS.forEach(s=>{
    const el=document.createElement('div');
    el.className='sec-card';
    el.style.borderColor=s.color.replace('.18','.45');
    el.style.background=s.color;
    el.innerHTML=`<span class="sec-emoji">${s.emoji}</span>
      <div class="sec-label">${s.label}</div>
      <div class="sec-sub">${s.sub}</div>`;
    el.addEventListener('click',()=>openSection(s));
    grid.appendChild(el);
  });
})();

// ── Animation sequence ──
function startEntry(){
  const seen=localStorage.getItem('fairose_entered');
  if(seen){showSections();return;}
  const bg=document.querySelector('.bg-img');
  const flash=document.getElementById('flashEl');
  document.getElementById('enterArea').classList.remove('show');
  bg.classList.add('approaching');
  setTimeout(()=>{flash.classList.add('on');},2300);
  setTimeout(()=>{
    showSections();
    setTimeout(()=>flash.classList.remove('on'),400);
  },2700);
  localStorage.setItem('fairose_entered','1');
}

function showSections(){
  document.getElementById('enterArea').classList.remove('show');
  document.getElementById('sectionsScreen').classList.add('show');
}

function backToShop(){
  document.getElementById('sectionsScreen').classList.remove('show');
  const bg=document.querySelector('.bg-img');
  bg.classList.remove('approaching');
  void bg.offsetWidth; // reflow
  setTimeout(()=>document.getElementById('enterArea').classList.add('show'),300);
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

