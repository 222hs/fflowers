from config import *

STORE_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>فيروز فلورز</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --bg:        #0c0c0c;
      --surface:   #141414;
      --surface2:  #1a1a1a;
      --border:    rgba(212,175,55,0.15);
      --border-b:  rgba(212,175,55,0.4);
      --gold:      #d4af37;
      --gold-l:    #f0d060;
      --text:      #f5f0e8;
      --muted:     #8a8070;
      --dim:       #4a4540;
    }

    html {
      background: var(--bg);
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Tajawal', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      max-width: 480px;
      margin: 0 auto;
      overflow-x: hidden;
      position: relative;
    }

    /* ─────────────────────────────────────────
       1. TOP NAV
    ───────────────────────────────────────── */
    .topnav {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      max-width: 480px;
      height: 60px;
      background: #0c0c0c;
      border-bottom: 1px solid rgba(212,175,55,0.2);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 18px;
      z-index: 50;
    }

    .nav-bag {
      position: relative;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      background: none;
      border: none;
      color: var(--muted);
    }

    .nav-bag svg {
      width: 22px;
      height: 22px;
      stroke: var(--muted);
      fill: none;
      stroke-width: 1.6;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .bag-count {
      position: absolute;
      top: 2px;
      left: 2px;
      background: var(--gold);
      color: #0c0c0c;
      font-family: 'Tajawal', sans-serif;
      font-size: 9px;
      font-weight: 700;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      line-height: 1;
    }

    .nav-logo {
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 20px;
      color: var(--gold);
      letter-spacing: 0.01em;
      user-select: none;
    }

    .nav-ig {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      text-decoration: none;
      -webkit-tap-highlight-color: transparent;
      transition: color 0.2s;
    }

    .nav-ig:hover { color: var(--gold); }

    .nav-ig svg {
      width: 20px;
      height: 20px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.6;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    /* ─────────────────────────────────────────
       2. HERO
    ───────────────────────────────────────── */
    .hero {
      position: relative;
      width: 100%;
      height: 100svh;
      background-image: url('/background.jpg');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      display: flex;
      align-items: flex-end;
      overflow: hidden;
    }

    .hero::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        to bottom,
        rgba(12,12,12,0.3) 0%,
        rgba(12,12,12,0.0) 40%,
        rgba(12,12,12,0.85) 80%,
        rgba(12,12,12,1) 100%
      );
      z-index: 1;
    }

    .hero-content {
      position: relative;
      z-index: 2;
      padding: 28px;
      width: 100%;
    }

    .hero-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: 'Tajawal', sans-serif;
      font-size: 11px;
      font-weight: 500;
      color: var(--gold);
      border: 1px solid var(--gold);
      border-radius: 50px;
      padding: 4px 12px;
      margin-bottom: 14px;
      letter-spacing: 0.5px;
    }

    .hero-heading {
      font-family: 'Playfair Display', serif;
      font-size: 36px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.2;
      white-space: pre-line;
      margin-bottom: 8px;
    }

    .hero-sub {
      font-family: 'Tajawal', sans-serif;
      font-size: 13px;
      color: var(--muted);
      margin-top: 8px;
      letter-spacing: 0.3px;
    }

    .hero-cta {
      display: inline-block;
      margin-top: 16px;
      border: 1px solid var(--gold);
      color: var(--gold);
      background: transparent;
      padding: 10px 24px;
      border-radius: 4px;
      font-family: 'Tajawal', sans-serif;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.2s, color 0.2s;
      -webkit-tap-highlight-color: transparent;
    }

    .hero-cta:hover,
    .hero-cta:active {
      background: rgba(212,175,55,0.1);
    }

    /* ─────────────────────────────────────────
       3. CATEGORY FILTER BAR
    ───────────────────────────────────────── */
    .filter-bar {
      position: sticky;
      top: 60px;
      z-index: 40;
      background: #0c0c0c;
      border-bottom: 1px solid rgba(212,175,55,0.12);
      height: 48px;
      display: flex;
      align-items: center;
      padding: 0 16px;
    }

    .filter-scroll {
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      width: 100%;
      padding-bottom: 0;
    }

    .filter-scroll::-webkit-scrollbar {
      display: none;
    }

    .filter-pill {
      flex-shrink: 0;
      border: 1px solid rgba(212,175,55,0.25);
      color: var(--muted);
      background: transparent;
      border-radius: 4px;
      padding: 5px 14px;
      font-family: 'Tajawal', sans-serif;
      font-size: 12px;
      font-weight: 400;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.2s, color 0.2s, border-color 0.2s;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }

    .filter-pill.active {
      background: var(--gold);
      color: #0c0c0c;
      font-weight: 700;
      border-color: transparent;
    }

    .filter-pill:not(.active):hover {
      border-color: rgba(212,175,55,0.5);
      color: var(--text);
    }

    /* ─────────────────────────────────────────
       4. PRODUCTS SECTION
    ───────────────────────────────────────── */
    #productsSection {
      padding: 20px 16px 100px;
    }

    .section-label {
      text-align: center;
      font-family: 'Tajawal', sans-serif;
      font-size: 11px;
      letter-spacing: 3px;
      color: var(--dim);
      margin-bottom: 18px;
      user-select: none;
    }

    .products-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    /* Product Card */
    .prod-card {
      background: var(--surface);
      border: 1px solid rgba(212,175,55,0.12);
      border-radius: 2px;
      overflow: hidden;
      cursor: pointer;
      transition: border-color 0.3s, transform 0.2s;
      -webkit-tap-highlight-color: transparent;
      display: flex;
      flex-direction: column;
    }

    .prod-card:hover {
      border-color: rgba(212,175,55,0.5);
      transform: translateY(-2px);
    }

    .prod-card:active {
      transform: translateY(0px) scale(0.985);
    }

    .card-img-wrap {
      position: relative;
      aspect-ratio: 3/4;
      overflow: hidden;
      background: linear-gradient(135deg, #1a1512, #2a1f15);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .card-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .card-img-placeholder {
      font-size: 40px;
      line-height: 1;
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      color: rgba(212,175,55,0.25);
    }

    .card-badge {
      position: absolute;
      top: 10px;
      right: 10px;
      font-size: 10px;
      background: rgba(12,12,12,0.8);
      color: var(--gold);
      border: 1px solid rgba(212,175,55,0.4);
      padding: 3px 8px;
      border-radius: 2px;
      letter-spacing: 1px;
      text-transform: uppercase;
      font-family: 'Tajawal', sans-serif;
      font-weight: 500;
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
    }

    .card-body {
      padding: 12px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }

    .card-name {
      font-family: 'Playfair Display', serif;
      font-size: 14px;
      font-weight: 400;
      color: var(--text);
      line-height: 1.3;
      margin-bottom: 6px;
    }

    .card-price {
      font-family: 'Playfair Display', serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--gold);
      margin-bottom: 0;
    }

    .card-order {
      display: block;
      margin-top: 8px;
      font-family: 'Tajawal', sans-serif;
      font-size: 11px;
      color: var(--muted);
      letter-spacing: 1px;
      text-decoration: none;
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
      text-align: right;
      width: 100%;
    }

    /* Skeleton */
    .skel-card {
      background: var(--surface);
      border: 1px solid rgba(212,175,55,0.08);
      border-radius: 2px;
      overflow: hidden;
    }

    .skel-img {
      aspect-ratio: 3/4;
      background: #1a1a1a;
      position: relative;
      overflow: hidden;
    }

    .skel-body {
      padding: 12px;
    }

    .skel-line {
      height: 12px;
      border-radius: 2px;
      background: #1a1a1a;
      margin-bottom: 8px;
      position: relative;
      overflow: hidden;
    }

    .skel-line.w60 { width: 60%; }
    .skel-line.w40 { width: 40%; }

    .skel-img::after,
    .skel-line::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(212,175,55,0.06) 50%,
        transparent 100%
      );
      background-size: 200% 100%;
      animation: shimmer 1.6s ease-in-out infinite;
    }

    @keyframes shimmer {
      0%   { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }

    /* Empty State */
    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
    }

    .empty-icon {
      display: block;
      font-size: 32px;
      margin-bottom: 12px;
      opacity: 0.4;
    }

    .empty-text {
      font-family: 'Tajawal', sans-serif;
      font-size: 14px;
      color: var(--dim);
    }

    /* ─────────────────────────────────────────
       5. BOTTOM SHEET OVERLAY
    ───────────────────────────────────────── */
    .sheet-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.85);
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }

    .sheet-overlay.open {
      opacity: 1;
      pointer-events: all;
    }

    /* ─────────────────────────────────────────
       5. ORDER BOTTOM SHEET
    ───────────────────────────────────────── */
    .order-sheet {
      position: fixed;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%) translateY(100%);
      width: 100%;
      max-width: 480px;
      background: var(--surface);
      border-top: 1px solid rgba(212,175,55,0.3);
      border-radius: 16px 16px 0 0;
      z-index: 101;
      max-height: 92vh;
      overflow-y: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      padding-bottom: env(safe-area-inset-bottom, 0px);
      transition: transform 0.38s cubic-bezier(0.32,0.72,0,1);
    }

    .order-sheet::-webkit-scrollbar { display: none; }

    .order-sheet.open {
      transform: translateX(-50%) translateY(0);
    }

    .sheet-drag {
      width: 40px;
      height: 3px;
      background: rgba(212,175,55,0.35);
      border-radius: 2px;
      margin: 12px auto 0;
    }

    .sheet-top {
      position: relative;
      padding: 16px 20px 0;
      margin-bottom: 4px;
    }

    .sheet-close {
      position: absolute;
      top: 12px;
      left: 20px;
      background: none;
      border: none;
      color: var(--dim);
      font-size: 18px;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      line-height: 1;
      padding: 4px;
    }

    .sheet-close:hover { color: var(--muted); }

    .sheet-prod-name {
      font-family: 'Playfair Display', serif;
      font-size: 16px;
      font-weight: 600;
      color: var(--gold);
      padding: 0 20px;
      margin-bottom: 4px;
    }

    .sheet-prod-price {
      font-family: 'Tajawal', sans-serif;
      font-size: 13px;
      color: var(--muted);
      padding: 0 20px;
      margin-bottom: 16px;
    }

    .sheet-divider {
      height: 1px;
      background: rgba(212,175,55,0.1);
    }

    .sheet-form {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .form-label {
      font-family: 'Tajawal', sans-serif;
      font-size: 11px;
      color: var(--muted);
      display: block;
      margin-bottom: 6px;
      letter-spacing: 0.5px;
    }

    .form-input,
    .form-textarea {
      width: 100%;
      background: #0c0c0c;
      border: 1px solid rgba(212,175,55,0.2);
      border-radius: 2px;
      color: var(--text);
      padding: 12px 14px;
      font-family: 'Tajawal', sans-serif;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
      -webkit-appearance: none;
    }

    .form-input:focus,
    .form-textarea:focus {
      border-color: var(--gold);
    }

    .form-input::placeholder,
    .form-textarea::placeholder {
      color: var(--dim);
      opacity: 0.9;
    }

    .form-textarea {
      resize: none;
      rows: 2;
      height: 72px;
      line-height: 1.5;
    }

    /* Delivery toggle */
    .delivery-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .dlv-btn {
      border: 1px solid rgba(212,175,55,0.2);
      background: transparent;
      color: var(--muted);
      font-family: 'Tajawal', sans-serif;
      font-size: 13px;
      font-weight: 500;
      padding: 10px;
      border-radius: 2px;
      cursor: pointer;
      text-align: center;
      transition: border-color 0.2s, background 0.2s, color 0.2s;
      -webkit-tap-highlight-color: transparent;
    }

    .dlv-btn.active {
      border-color: var(--gold);
      background: rgba(212,175,55,0.08);
      color: var(--gold);
    }

    /* Address slide-down */
    .addr-wrap {
      overflow: hidden;
      max-height: 0;
      opacity: 0;
      transition: max-height 0.3s ease, opacity 0.25s ease;
    }

    .addr-wrap.show {
      max-height: 100px;
      opacity: 1;
    }

    .submit-btn {
      width: 100%;
      background: var(--gold);
      color: #0c0c0c;
      border: none;
      border-radius: 2px;
      padding: 14px;
      font-family: 'Tajawal', sans-serif;
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 0.5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: opacity 0.2s, filter 0.2s;
      -webkit-tap-highlight-color: transparent;
    }

    .submit-btn:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }

    .submit-btn:not(:disabled):active {
      filter: brightness(0.9);
    }

    .btn-spinner {
      width: 16px;
      height: 16px;
      border: 2px solid rgba(0,0,0,0.25);
      border-top-color: #0c0c0c;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      display: none;
    }

    .submit-btn.loading .btn-spinner { display: block; }
    .submit-btn.loading .btn-text { opacity: 0.7; }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* ─────────────────────────────────────────
       6. SUCCESS STATE (replaces sheet content)
    ───────────────────────────────────────── */
    .success-view {
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 48px 32px;
      text-align: center;
    }

    .success-view.show {
      display: flex;
    }

    .success-check {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: 2px solid var(--gold);
      background: rgba(212,175,55,0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: var(--gold);
      margin-bottom: 20px;
    }

    .success-title {
      font-family: 'Playfair Display', serif;
      font-size: 22px;
      color: var(--gold);
      margin-bottom: 10px;
    }

    .success-sub {
      font-family: 'Tajawal', sans-serif;
      font-size: 13px;
      color: var(--muted);
      line-height: 1.6;
      margin-bottom: 28px;
    }

    .success-close-btn {
      border: 1px solid var(--gold);
      background: transparent;
      color: var(--gold);
      font-family: 'Tajawal', sans-serif;
      font-size: 14px;
      font-weight: 500;
      padding: 12px 32px;
      border-radius: 2px;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      transition: background 0.2s;
    }

    .success-close-btn:hover {
      background: rgba(212,175,55,0.08);
    }

    /* ─────────────────────────────────────────
       7. FOOTER
    ───────────────────────────────────────── */
    .footer {
      padding: 40px 20px 20px;
      text-align: center;
      position: relative;
    }

    .footer-logo {
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 14px;
      color: var(--dim);
      display: block;
      margin-bottom: 6px;
    }

    .footer-en {
      font-family: 'Tajawal', sans-serif;
      font-size: 10px;
      color: #2a2520;
      display: block;
    }

    .footer-admin {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      opacity: 0.05;
      text-decoration: none;
      font-size: 14px;
      color: var(--text);
    }

    /* ─────────────────────────────────────────
       REDUCED MOTION
    ───────────────────────────────────────── */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body>

  <!-- ══ 1. TOP NAV ══ -->
  <nav class="topnav" role="navigation" aria-label="شريط التنقل">
    <button class="nav-bag" id="bagBtn" aria-label="السلة">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
        <line x1="3" y1="6" x2="21" y2="6"/>
        <path d="M16 10a4 4 0 01-8 0"/>
      </svg>
      <span class="bag-count" id="bagCount" aria-live="polite">0</span>
    </button>

    <span class="nav-logo" aria-label="فيروز فلورز">فيروز فلورز</span>

    <a class="nav-ig" href="#" aria-label="انستغرام" rel="noopener noreferrer">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
        <path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/>
        <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>
      </svg>
    </a>
  </nav>

  <!-- ══ 2. HERO ══ -->
  <section class="hero" role="banner" aria-label="قسم الترحيب">
    <div class="hero-content">
      <div class="hero-pill">🌸 محل ورد عُماني</div>
      <h1 class="hero-heading">أجمل الورود
لأجمل اللحظات</h1>
      <p class="hero-sub">باقات · استاندات · مجسمات · شرايط</p>
      <a class="hero-cta" href="#productsSection" onclick="document.getElementById('productsSection').scrollIntoView({behavior:'smooth'}); return false;">
        تصفح المنتجات ↓
      </a>
    </div>
  </section>

  <!-- ══ 3. CATEGORY FILTER BAR ══ -->
  <div class="filter-bar" role="navigation" aria-label="تصفية الفئات">
    <div class="filter-scroll" id="filterScroll">
      <button class="filter-pill active" data-cat="all"       onclick="filterCat('all')">الكل</button>
      <button class="filter-pill"        data-cat="باقات"     onclick="filterCat('باقات')">💐 باقات</button>
      <button class="filter-pill"        data-cat="استاندات"  onclick="filterCat('استاندات')">🌹 استاندات</button>
      <button class="filter-pill"        data-cat="مجسمات"    onclick="filterCat('مجسمات')">🌸 مجسمات</button>
      <button class="filter-pill"        data-cat="شرايط"     onclick="filterCat('شرايط')">🎀 شرايط</button>
    </div>
  </div>

  <!-- ══ 4. PRODUCTS SECTION ══ -->
  <main id="productsSection">
    <div class="section-label" aria-hidden="true">— المنتجات —</div>
    <div class="products-grid" id="productsGrid" aria-live="polite" aria-label="المنتجات">
      <!-- JS populated -->
    </div>
  </main>

  <!-- ══ 7. FOOTER ══ -->
  <footer class="footer">
    <span class="footer-logo">فيروز فلورز</span>
    <span class="footer-en">Fairuz Flowers &amp; More</span>
    <a class="footer-admin" href="/admin" tabindex="-1" aria-hidden="true">🔐</a>
  </footer>

  <!-- ══ OVERLAY ══ -->
  <div class="sheet-overlay" id="sheetOverlay" onclick="closeOrderSheet()"></div>

  <!-- ══ 5. ORDER BOTTOM SHEET ══ -->
  <div class="order-sheet" id="orderSheet" role="dialog" aria-modal="true" aria-label="نموذج الطلب">
    <div class="sheet-drag"></div>

    <!-- Normal form content -->
    <div id="sheetFormContent">
      <div class="sheet-top">
        <button class="sheet-close" onclick="closeOrderSheet()" aria-label="إغلاق">✕</button>
      </div>
      <p class="sheet-prod-name" id="sheetName">—</p>
      <p class="sheet-prod-price" id="sheetPrice"></p>
      <div class="sheet-divider"></div>

      <form class="sheet-form" id="orderForm" onsubmit="return false;" novalidate>

        <div>
          <label class="form-label" for="f-name">الاسم الكريم *</label>
          <input class="form-input" id="f-name" type="text" autocomplete="name" placeholder="اسمك الكريم" required>
        </div>

        <div>
          <label class="form-label" for="f-phone">رقم الهاتف *</label>
          <input class="form-input" id="f-phone" type="tel" dir="ltr" autocomplete="tel" placeholder="+968 9XXX XXXX" required>
        </div>

        <div>
          <span class="form-label">طريقة الاستلام</span>
          <div class="delivery-row">
            <button type="button" class="dlv-btn active" id="dlvDelivery" onclick="setDelivery('delivery')">🚗&nbsp; توصيل</button>
            <button type="button" class="dlv-btn"        id="dlvPickup"   onclick="setDelivery('pickup')">🏪&nbsp; استلام من المحل</button>
          </div>
        </div>

        <div class="addr-wrap show" id="addrWrap">
          <label class="form-label" for="f-address">العنوان</label>
          <textarea class="form-textarea" id="f-address" placeholder="المنطقة، الشارع، رقم المنزل..." rows="2"></textarea>
        </div>

        <div>
          <label class="form-label" for="f-notes">ملاحظات إضافية <span style="opacity:0.5">(اختياري)</span></label>
          <textarea class="form-textarea" id="f-notes" placeholder="أي تفاصيل إضافية..." rows="2"></textarea>
        </div>

        <button type="button" class="submit-btn" id="submitBtn" onclick="submitOrder()">
          <span class="btn-spinner" id="btnSpinner"></span>
          <span class="btn-text">تأكيد الطلب</span>
        </button>

      </form>
    </div>

    <!-- 6. Success State -->
    <div class="success-view" id="successView">
      <div class="success-check">✓</div>
      <h2 class="success-title">شكراً لك! 🌸</h2>
      <p class="success-sub">تم استلام طلبك وسنتواصل معك قريباً</p>
      <button class="success-close-btn" onclick="closeOrderSheet()">متابعة التصفح</button>
    </div>
  </div>

  <script>
    // ────────────────────────────────────────
    // STATE
    // ────────────────────────────────────────
    let currentCategory = 'all';
    let selectedProduct = null;
    let deliveryMode    = 'delivery';
    let orderCount      = 0;

    // ────────────────────────────────────────
    // CATEGORY FILTER
    // ────────────────────────────────────────
    function filterCat(cat) {
      if (currentCategory === cat) return;
      currentCategory = cat;
      document.querySelectorAll('.filter-pill').forEach(el => {
        const isActive = el.dataset.cat === cat;
        el.classList.toggle('active', isActive);
        el.setAttribute('aria-pressed', String(isActive));
      });
      loadProducts(cat);
    }

    // ────────────────────────────────────────
    // LOAD PRODUCTS
    // ────────────────────────────────────────
    async function loadProducts(category) {
      renderSkeletons();
      try {
        const qs  = (!category || category === 'all') ? '' : '?category=' + encodeURIComponent(category);
        const res = await fetch('/api/store/products' + qs);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        const list = Array.isArray(data) ? data : (data.products || []);
        renderProducts(list);
      } catch (err) {
        console.error('loadProducts:', err);
        renderError();
      }
    }

    // ────────────────────────────────────────
    // RENDER HELPERS
    // ────────────────────────────────────────
    function renderSkeletons() {
      const g = document.getElementById('productsGrid');
      g.innerHTML = [0,1,2,3].map(() => `
        <div class="skel-card" aria-hidden="true">
          <div class="skel-img"></div>
          <div class="skel-body">
            <div class="skel-line"></div>
            <div class="skel-line w60"></div>
            <div class="skel-line w40"></div>
          </div>
        </div>
      `).join('');
    }

    function renderProducts(products) {
      const g = document.getElementById('productsGrid');
      if (!products.length) {
        g.innerHTML = `
          <div class="empty-state">
            <span class="empty-icon">🌸</span>
            <p class="empty-text">لا توجد منتجات في هذه الفئة</p>
          </div>`;
        return;
      }
      g.innerHTML = products.map(p => {
        const safe    = JSON.stringify(p).replace(/'/g, "\\'");
        const priceStr = p.price ? formatPrice(p.price) + ' ر.ع' : 'السعر عند الطلب';
        const imgTag  = p.img
          ? `<img src="${esc(p.img)}" alt="${esc(p.name)}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`
          : '';
        const placeholderStyle = p.img ? 'display:none;' : '';
        const badge   = p.category ? `<span class="card-badge">${esc(p.category)}</span>` : '';
        return `
          <article class="prod-card" role="button" tabindex="0"
            onclick="openOrderSheet(${safe})"
            onkeydown="if(event.key==='Enter')openOrderSheet(${safe})"
            aria-label="${esc(p.name)}">
            <div class="card-img-wrap">
              ${imgTag}
              <div class="card-img-placeholder" style="${placeholderStyle}" aria-hidden="true">🌸</div>
              ${badge}
            </div>
            <div class="card-body">
              <p class="card-name">${esc(p.name)}</p>
              <p class="card-price">${priceStr}</p>
              <span class="card-order" aria-hidden="true">اطلب الآن →</span>
            </div>
          </article>`;
      }).join('');
    }

    function renderError() {
      document.getElementById('productsGrid').innerHTML = `
        <div class="empty-state">
          <span class="empty-icon" style="opacity:0.3">⚠️</span>
          <p class="empty-text">تعذّر تحميل المنتجات، يرجى المحاولة لاحقاً</p>
        </div>`;
    }

    function formatPrice(price) {
      const n = parseFloat(price);
      if (isNaN(n)) return price;
      return n.toFixed(3);
    }

    function esc(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    // ────────────────────────────────────────
    // ORDER SHEET OPEN / CLOSE
    // ────────────────────────────────────────
    function openOrderSheet(product) {
      selectedProduct = product;

      // Reset success state
      document.getElementById('sheetFormContent').style.display = '';
      document.getElementById('successView').classList.remove('show');

      // Populate product info
      document.getElementById('sheetName').textContent  = product.name  || '—';
      const priceStr = product.price ? formatPrice(product.price) + ' ر.ع' : 'السعر عند الطلب';
      document.getElementById('sheetPrice').textContent = priceStr;

      // Reset form
      document.getElementById('f-name').value    = '';
      document.getElementById('f-phone').value   = '';
      document.getElementById('f-address').value = '';
      document.getElementById('f-notes').value   = '';
      setDelivery('delivery');
      resetSubmitBtn();

      document.getElementById('sheetOverlay').classList.add('open');
      document.getElementById('orderSheet').classList.add('open');
      document.body.style.overflow = 'hidden';

      setTimeout(() => document.getElementById('f-name').focus(), 380);
    }

    function closeOrderSheet() {
      document.getElementById('sheetOverlay').classList.remove('open');
      document.getElementById('orderSheet').classList.remove('open');
      document.body.style.overflow = '';
      selectedProduct = null;
    }

    // Escape key
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeOrderSheet();
    });

    // ────────────────────────────────────────
    // DELIVERY TOGGLE
    // ────────────────────────────────────────
    function setDelivery(mode) {
      deliveryMode = mode;
      document.getElementById('dlvDelivery').classList.toggle('active', mode === 'delivery');
      document.getElementById('dlvPickup').classList.toggle('active',   mode === 'pickup');
      document.getElementById('addrWrap').classList.toggle('show', mode === 'delivery');
    }

    // ────────────────────────────────────────
    // SUBMIT ORDER
    // ────────────────────────────────────────
    async function submitOrder() {
      const name  = document.getElementById('f-name').value.trim();
      const phone = document.getElementById('f-phone').value.trim();

      if (!name) {
        pulse('f-name');
        document.getElementById('f-name').focus();
        return;
      }
      if (!phone) {
        pulse('f-phone');
        document.getElementById('f-phone').focus();
        return;
      }

      const btn = document.getElementById('submitBtn');
      btn.disabled = true;
      btn.classList.add('loading');

      const payload = {
        product_id:     selectedProduct?.id     || null,
        product_name:   selectedProduct?.name   || '',
        customer_name:  name,
        customer_phone: phone,
        delivery_type:  deliveryMode,
        address:        deliveryMode === 'delivery' ? document.getElementById('f-address').value.trim() : '',
        notes:          document.getElementById('f-notes').value.trim(),
      };

      try {
        const res = await fetch('/api/store/order', {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify(payload),
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);

        showSuccess();
        orderCount++;
        document.getElementById('bagCount').textContent = orderCount;
      } catch (err) {
        console.error('submitOrder:', err);
        resetSubmitBtn();
        pulse('submitBtn');
      }
    }

    function resetSubmitBtn() {
      const btn = document.getElementById('submitBtn');
      btn.disabled = false;
      btn.classList.remove('loading');
    }

    function pulse(id) {
      const el = document.getElementById(id);
      if (!el) return;
      el.style.transition = 'border-color 0.2s';
      el.style.borderColor = 'rgba(220,80,80,0.8)';
      el.animate
        ? el.animate([
            {transform: 'translateX(0)'},
            {transform: 'translateX(-5px)'},
            {transform: 'translateX(5px)'},
            {transform: 'translateX(-3px)'},
            {transform: 'translateX(0)'},
          ], { duration: 300, easing: 'ease' })
        : null;
      setTimeout(() => { el.style.borderColor = ''; }, 900);
    }

    // ────────────────────────────────────────
    // SUCCESS STATE
    // ────────────────────────────────────────
    function showSuccess() {
      document.getElementById('sheetFormContent').style.display = 'none';
      document.getElementById('successView').classList.add('show');
      // Scroll sheet to top
      document.getElementById('orderSheet').scrollTop = 0;
    }

    // ────────────────────────────────────────
    // INIT
    // ────────────────────────────────────────
    loadProducts('all');
  </script>
</body>
</html>"""
