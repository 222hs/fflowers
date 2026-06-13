from config import *

STORE_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>فيروز فلورز</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --bg:           #ffffff;
      --section-bg:   #f9f7f5;
      --card-bg:      #ffffff;
      --border:       #e8e2dc;
      --primary:      #c8596a;
      --primary-dark: #a83d52;
      --primary-light:#fdf0f2;
      --gold:         #c4963a;
      --text:         #1a1a1a;
      --text-sec:     #666666;
      --text-muted:   #999999;
      --green:        #4a7c59;
    }

    html {
      background: var(--bg);
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Cairo', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      max-width: 480px;
      margin: 0 auto;
      overflow-x: hidden;
      position: relative;
    }

    /* ─────────────────────────────────────────
       1. HEADER (fixed, 56px)
    ───────────────────────────────────────── */
    .site-header {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      max-width: 480px;
      height: 56px;
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      box-shadow: 0 1px 8px rgba(0,0,0,0.06);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 50;
    }

    .header-logo {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 16px;
      color: var(--text);
      text-decoration: none;
      user-select: none;
    }

    .header-logo .logo-emoji {
      font-size: 18px;
      line-height: 1;
    }

    .header-center {
      flex: 1;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .header-action-btn {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: none;
      border: none;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      position: relative;
      text-decoration: none;
      color: var(--text-sec);
    }

    .header-action-btn svg {
      width: 22px;
      height: 22px;
    }

    .cart-badge {
      position: absolute;
      top: 2px;
      right: 2px;
      background: var(--primary);
      color: white;
      font-size: 9px;
      font-weight: 700;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      display: none;
      align-items: center;
      justify-content: center;
      line-height: 1;
    }

    .cart-badge.visible {
      display: flex;
    }

    /* ─────────────────────────────────────────
       2. ANNOUNCEMENT BAR
    ───────────────────────────────────────── */
    .announce-bar {
      margin-top: 56px;
      height: 36px;
      background: var(--primary);
      color: white;
      text-align: center;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      letter-spacing: 0.2px;
    }

    /* ─────────────────────────────────────────
       3. HERO BANNER
    ───────────────────────────────────────── */
    .hero {
      position: relative;
      height: 220px;
      overflow: hidden;
      background: linear-gradient(135deg, #fff0f3 0%, #fce8d4 100%);
      background-image:
        url('/background.jpg'),
        linear-gradient(135deg, #fff0f3 0%, #fce8d4 100%);
      background-position: right center, center;
      background-size: 50% auto, cover;
      background-repeat: no-repeat, no-repeat;
      display: flex;
      align-items: center;
    }

    .hero-content {
      padding: 24px;
      max-width: 60%;
      position: relative;
      z-index: 2;
    }

    .hero-tag {
      display: inline-block;
      background: var(--primary);
      color: white;
      font-size: 10px;
      font-weight: 600;
      border-radius: 20px;
      padding: 3px 10px;
      margin-bottom: 8px;
    }

    .hero-heading {
      font-size: 22px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.3;
      white-space: pre-line;
    }

    .hero-cta {
      display: inline-block;
      margin-top: 12px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 8px;
      padding: 9px 20px;
      font-family: 'Cairo', sans-serif;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      -webkit-tap-highlight-color: transparent;
      transition: background 0.2s;
    }

    .hero-cta:hover,
    .hero-cta:active {
      background: var(--primary-dark);
    }

    /* ─────────────────────────────────────────
       4. OCCASION CATEGORIES
    ───────────────────────────────────────── */
    .occasions-section {
      background: var(--section-bg);
      padding: 16px;
    }

    .section-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 12px;
    }

    .occasions-scroll {
      display: flex;
      flex-direction: row;
      gap: 10px;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }

    .occasions-scroll::-webkit-scrollbar {
      display: none;
    }

    .occasion-card {
      flex-shrink: 0;
      width: 80px;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
    }

    .occasion-circle {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: white;
      border: 1.5px solid var(--border);
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .occasion-card:active .occasion-circle {
      border-color: var(--primary);
      box-shadow: 0 2px 8px rgba(200,89,106,0.15);
    }

    .occasion-label {
      font-size: 11px;
      font-weight: 600;
      color: #444;
      text-align: center;
      margin-top: 6px;
    }

    /* ─────────────────────────────────────────
       5. PRODUCTS SECTION
    ───────────────────────────────────────── */
    #productsSection {
      background: white;
      padding: 16px 16px 100px;
    }

    .cat-tabs-scroll {
      display: flex;
      flex-direction: row;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      margin-bottom: 16px;
    }

    .cat-tabs-scroll::-webkit-scrollbar {
      display: none;
    }

    .cat-pill {
      flex-shrink: 0;
      background: var(--section-bg);
      border: 1px solid var(--border);
      color: var(--text-sec);
      border-radius: 20px;
      padding: 7px 16px;
      font-family: 'Cairo', sans-serif;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.18s, color 0.18s, border-color 0.18s;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }

    .cat-pill.active {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
    }

    .products-section-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 14px;
    }

    .products-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    /* Product Card */
    .prod-card {
      background: white;
      border: 1px solid #f0ebe5;
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      -webkit-tap-highlight-color: transparent;
      display: flex;
      flex-direction: column;
    }

    .prod-card:active {
      transform: scale(0.98);
      box-shadow: 0 1px 6px rgba(0,0,0,0.10);
    }

    .card-img-wrap {
      position: relative;
      aspect-ratio: 1/1;
      overflow: hidden;
      background: linear-gradient(135deg, #fdf0f2, #fce8d4);
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
      font-size: 36px;
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .card-new-badge {
      position: absolute;
      top: 0;
      right: 0;
      background: var(--primary);
      color: white;
      font-size: 9px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 0 12px 0 8px;
    }

    .card-body {
      padding: 10px 12px 12px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }

    .card-name {
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      line-height: 1.35;
      margin-bottom: 4px;
    }

    .card-category {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .card-price-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      margin-top: auto;
    }

    .card-price {
      font-size: 16px;
      font-weight: 900;
      color: var(--primary);
      line-height: 1;
    }

    .card-price-on-request {
      font-size: 12px;
      font-weight: 400;
      color: var(--text-muted);
    }

    .card-order-btn {
      flex-shrink: 0;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 20px;
      padding: 5px 12px;
      font-family: 'Cairo', sans-serif;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      white-space: nowrap;
    }

    /* Skeleton */
    .skel-card {
      background: white;
      border: 1px solid #f0ebe5;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    .skel-img {
      aspect-ratio: 1/1;
      background: #ede8e3;
      position: relative;
      overflow: hidden;
    }

    .skel-body {
      padding: 10px 12px 12px;
    }

    .skel-line {
      height: 11px;
      border-radius: 6px;
      background: #ede8e3;
      margin-bottom: 8px;
      position: relative;
      overflow: hidden;
    }

    .skel-line.w70 { width: 70%; }
    .skel-line.w45 { width: 45%; }

    .skel-img::after,
    .skel-line::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(255,255,255,0.55) 50%,
        transparent 100%
      );
      background-size: 200% 100%;
      animation: shimmer 1.5s ease-in-out infinite;
    }

    @keyframes shimmer {
      0%   { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }

    /* Empty State */
    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 48px 20px;
    }

    .empty-icon {
      display: block;
      font-size: 40px;
      margin-bottom: 12px;
    }

    .empty-text {
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .empty-sub {
      font-size: 12px;
      color: #cccccc;
    }

    /* ─────────────────────────────────────────
       6. TRUST BADGES
    ───────────────────────────────────────── */
    .trust-section {
      background: var(--section-bg);
      padding: 20px 16px;
      display: flex;
      justify-content: space-around;
      align-items: flex-start;
    }

    .trust-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .trust-circle {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }

    .trust-label {
      font-size: 11px;
      color: var(--text-sec);
      text-align: center;
      font-weight: 600;
    }

    /* ─────────────────────────────────────────
       7. FLOATING WHATSAPP BUTTON
    ───────────────────────────────────────── */
    .wa-float {
      position: fixed;
      bottom: 84px;
      left: 16px;
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: #25D366;
      box-shadow: 0 4px 16px rgba(37,211,102,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      z-index: 49;
      -webkit-tap-highlight-color: transparent;
      transition: transform 0.15s;
    }

    .wa-float:active {
      transform: scale(0.93);
    }

    .wa-float svg {
      width: 28px;
      height: 28px;
    }

    /* ─────────────────────────────────────────
       8. SHEET OVERLAY
    ───────────────────────────────────────── */
    .sheet-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.5);
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
       8. ORDER BOTTOM SHEET
    ───────────────────────────────────────── */
    .order-sheet {
      position: fixed;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%) translateY(100%);
      width: 100%;
      max-width: 480px;
      background: white;
      border-top: 2px solid var(--primary);
      border-radius: 20px 20px 0 0;
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
      width: 36px;
      height: 4px;
      background: var(--border);
      border-radius: 2px;
      margin: 10px auto;
    }

    .sheet-top {
      position: relative;
      padding: 0 20px 4px;
    }

    .sheet-close {
      position: absolute;
      top: -4px;
      left: 20px;
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 22px;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      line-height: 1;
      padding: 4px;
    }

    .sheet-prod-name {
      font-size: 16px;
      font-weight: 700;
      color: var(--text);
      padding: 0 20px 4px;
    }

    .sheet-prod-price {
      font-size: 14px;
      font-weight: 900;
      color: var(--primary);
      padding: 0 20px 14px;
    }

    .sheet-divider {
      height: 1px;
      background: var(--border);
      opacity: 0.6;
    }

    .sheet-form {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .form-label {
      font-size: 12px;
      font-weight: 600;
      color: #444;
      display: block;
      margin-bottom: 6px;
    }

    .form-input,
    .form-textarea {
      width: 100%;
      background: var(--section-bg);
      border: 1.5px solid var(--border);
      border-radius: 10px;
      color: var(--text);
      padding: 12px 14px;
      font-family: 'Cairo', sans-serif;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s, background 0.2s;
      -webkit-appearance: none;
    }

    .form-input:focus,
    .form-textarea:focus {
      border-color: var(--primary);
      background: white;
    }

    .form-input::placeholder,
    .form-textarea::placeholder {
      color: var(--text-muted);
    }

    .form-textarea {
      resize: none;
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
      border: 1.5px solid var(--border);
      background: var(--section-bg);
      color: var(--text-sec);
      font-family: 'Cairo', sans-serif;
      font-size: 13px;
      font-weight: 500;
      padding: 10px;
      border-radius: 10px;
      cursor: pointer;
      text-align: center;
      transition: border-color 0.2s, background 0.2s, color 0.2s, font-weight 0.1s;
      -webkit-tap-highlight-color: transparent;
    }

    .dlv-btn.active {
      border-color: var(--primary);
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 700;
    }

    /* Address slide-down */
    .addr-wrap {
      overflow: hidden;
      max-height: 0;
      opacity: 0;
      transition: max-height 0.3s ease, opacity 0.25s ease;
    }

    .addr-wrap.show {
      max-height: 110px;
      opacity: 1;
    }

    .submit-btn {
      width: 100%;
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      color: white;
      border: none;
      border-radius: 12px;
      padding: 14px;
      font-family: 'Cairo', sans-serif;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: opacity 0.2s;
      -webkit-tap-highlight-color: transparent;
    }

    .submit-btn:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }

    .btn-spinner {
      width: 16px;
      height: 16px;
      border: 2px solid rgba(255,255,255,0.3);
      border-top-color: white;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      display: none;
    }

    .submit-btn.loading .btn-spinner { display: block; }
    .submit-btn.loading .btn-text    { opacity: 0.7; }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* ─────────────────────────────────────────
       9. SUCCESS STATE
    ───────────────────────────────────────── */
    .success-view {
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      text-align: center;
    }

    .success-view.show {
      display: flex;
    }

    .success-check {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: #e8f5ec;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: var(--green);
      margin-bottom: 0;
    }

    .success-title {
      font-size: 20px;
      font-weight: 700;
      color: var(--text);
      margin-top: 16px;
    }

    .success-sub {
      font-size: 13px;
      color: var(--text-sec);
      margin-top: 8px;
      line-height: 1.5;
    }

    .success-close-btn {
      margin-top: 24px;
      background: white;
      border: 1.5px solid var(--primary);
      color: var(--primary);
      font-family: 'Cairo', sans-serif;
      font-size: 14px;
      font-weight: 600;
      padding: 12px 32px;
      border-radius: 10px;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      transition: background 0.2s;
    }

    .success-close-btn:hover,
    .success-close-btn:active {
      background: var(--primary-light);
    }

    /* ─────────────────────────────────────────
       10. FOOTER
    ───────────────────────────────────────── */
    .site-footer {
      background: #1a1a1a;
      color: white;
      padding: 24px 16px;
      text-align: center;
    }

    .footer-logo {
      font-size: 16px;
      font-weight: 700;
      color: white;
      display: block;
    }

    .footer-tagline {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
      display: block;
    }

    .footer-divider {
      height: 1px;
      background: rgba(255,255,255,0.08);
      margin: 16px 0;
    }

    .footer-bottom {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      font-size: 11px;
      color: #555;
    }

    .footer-admin {
      opacity: 0.15;
      text-decoration: none;
      color: white;
      font-size: 13px;
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

  <!-- ══ 1. HEADER ══ -->
  <header class="site-header" role="banner">
    <a class="header-logo" href="#" aria-label="فيروز فلورز - الصفحة الرئيسية">
      <span class="logo-emoji">🌸</span>
      <span>فيروز فلورز</span>
    </a>

    <div class="header-center"></div>

    <div class="header-actions">
      <!-- WhatsApp -->
      <a class="header-action-btn" href="#" aria-label="واتساب" rel="noopener noreferrer">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" fill="#25D366"/>
          <path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.658 1.438 5.168L2 22l4.95-1.414A9.953 9.953 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18a7.95 7.95 0 01-4.073-1.117l-.292-.174-3.017.862.863-3.037-.19-.31A7.95 7.95 0 014 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8z" fill="#25D366"/>
        </svg>
      </a>
      <!-- Cart -->
      <button class="header-action-btn" id="cartBtn" aria-label="السلة">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <path d="M16 10a4 4 0 01-8 0"/>
        </svg>
        <span class="cart-badge" id="cartBadge" aria-live="polite">0</span>
      </button>
    </div>
  </header>

  <!-- ══ 2. ANNOUNCEMENT BAR ══ -->
  <div class="announce-bar" role="marquee" aria-label="إعلان">
    🚗 توصيل داخل المحافظة &nbsp;·&nbsp; اطلب الآن واستلم اليوم 🌸
  </div>

  <!-- ══ 3. HERO BANNER ══ -->
  <section class="hero" aria-label="قسم الترحيب">
    <div class="hero-content">
      <span class="hero-tag">جديد الموسم ✨</span>
      <h1 class="hero-heading">أجمل الباقات
لأجمل المناسبات</h1>
      <a class="hero-cta" href="#productsSection"
         onclick="document.getElementById('productsSection').scrollIntoView({behavior:'smooth'}); return false;">
        تصفح المنتجات
      </a>
    </div>
  </section>

  <!-- ══ 4. OCCASION CATEGORIES ══ -->
  <section class="occasions-section" aria-labelledby="occasionsTitle">
    <p class="section-title" id="occasionsTitle">تصفح حسب المناسبة</p>
    <div class="occasions-scroll" role="list">
      <div class="occasion-card" role="listitem" tabindex="0"
           onclick="filterCat('زواج')" onkeydown="if(event.key==='Enter')filterCat('زواج')" aria-label="زواج">
        <div class="occasion-circle">💍</div>
        <span class="occasion-label">زواج</span>
      </div>
      <div class="occasion-card" role="listitem" tabindex="0"
           onclick="filterCat('عيد ميلاد')" onkeydown="if(event.key==='Enter')filterCat('عيد ميلاد')" aria-label="عيد ميلاد">
        <div class="occasion-circle">🎂</div>
        <span class="occasion-label">عيد ميلاد</span>
      </div>
      <div class="occasion-card" role="listitem" tabindex="0"
           onclick="filterCat('تخرج')" onkeydown="if(event.key==='Enter')filterCat('تخرج')" aria-label="تخرج">
        <div class="occasion-circle">🎓</div>
        <span class="occasion-label">تخرج</span>
      </div>
      <div class="occasion-card" role="listitem" tabindex="0"
           onclick="filterCat('هدية')" onkeydown="if(event.key==='Enter')filterCat('هدية')" aria-label="هدية">
        <div class="occasion-circle">🌹</div>
        <span class="occasion-label">هدية</span>
      </div>
      <div class="occasion-card" role="listitem" tabindex="0"
           onclick="filterCat('افتتاح')" onkeydown="if(event.key==='Enter')filterCat('افتتاح')" aria-label="افتتاح">
        <div class="occasion-circle">🎉</div>
        <span class="occasion-label">افتتاح</span>
      </div>
      <div class="occasion-card" role="listitem" tabindex="0"
           onclick="filterCat('all')" onkeydown="if(event.key==='Enter')filterCat('all')" aria-label="تخص">
        <div class="occasion-circle">💐</div>
        <span class="occasion-label">تخص</span>
      </div>
    </div>
  </section>

  <!-- ══ 5. PRODUCTS SECTION ══ -->
  <main id="productsSection" aria-label="قسم المنتجات">

    <!-- Category tabs -->
    <div class="cat-tabs-scroll" role="tablist" aria-label="تصفية المنتجات">
      <button class="cat-pill active" data-cat="all"      role="tab" aria-selected="true"  onclick="filterCat('all')">الكل</button>
      <button class="cat-pill"        data-cat="باقات"    role="tab" aria-selected="false" onclick="filterCat('باقات')">💐 باقات</button>
      <button class="cat-pill"        data-cat="استاندات" role="tab" aria-selected="false" onclick="filterCat('استاندات')">🌹 استاندات</button>
      <button class="cat-pill"        data-cat="مجسمات"   role="tab" aria-selected="false" onclick="filterCat('مجسمات')">🌸 مجسمات</button>
      <button class="cat-pill"        data-cat="شرايط"    role="tab" aria-selected="false" onclick="filterCat('شرايط')">🎀 شرايط</button>
    </div>

    <p class="products-section-title">🌸 منتجاتنا</p>

    <div class="products-grid" id="productsGrid" aria-live="polite" aria-label="قائمة المنتجات">
      <!-- JS populated -->
    </div>
  </main>

  <!-- ══ 6. TRUST BADGES ══ -->
  <section class="trust-section" aria-label="مميزاتنا">
    <div class="trust-item">
      <div class="trust-circle">🚗</div>
      <span class="trust-label">توصيل سريع</span>
    </div>
    <div class="trust-item">
      <div class="trust-circle">🌸</div>
      <span class="trust-label">ورود طازجة</span>
    </div>
    <div class="trust-item">
      <div class="trust-circle">💬</div>
      <span class="trust-label">دعم فوري</span>
    </div>
  </section>

  <!-- ══ 10. FOOTER ══ -->
  <footer class="site-footer">
    <span class="footer-logo">🌸 فيروز فلورز</span>
    <span class="footer-tagline">أجمل الورود لأجمل اللحظات</span>
    <div class="footer-divider"></div>
    <div class="footer-bottom">
      <span>© 2025 فيروز فلورز</span>
      <a class="footer-admin" href="/admin" tabindex="-1" aria-hidden="true">🔐</a>
    </div>
  </footer>

  <!-- ══ 7. FLOATING WHATSAPP ══ -->
  <a class="wa-float" href="https://wa.me/96812345678" target="_blank" rel="noopener noreferrer" aria-label="تواصل عبر واتساب">
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" fill="white"/>
      <path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.658 1.438 5.168L2 22l4.95-1.414A9.953 9.953 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18a7.95 7.95 0 01-4.073-1.117l-.292-.174-3.017.862.863-3.037-.19-.31A7.95 7.95 0 014 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8z" fill="white"/>
    </svg>
  </a>

  <!-- ══ OVERLAY ══ -->
  <div class="sheet-overlay" id="sheetOverlay" onclick="closeOrderSheet()" aria-hidden="true"></div>

  <!-- ══ 8. ORDER BOTTOM SHEET ══ -->
  <div class="order-sheet" id="orderSheet" role="dialog" aria-modal="true" aria-label="نموذج الطلب">
    <div class="sheet-drag" aria-hidden="true"></div>

    <!-- Form content -->
    <div id="sheetFormContent">
      <div class="sheet-top">
        <button class="sheet-close" onclick="closeOrderSheet()" aria-label="إغلاق النافذة">✕</button>
      </div>

      <p class="sheet-prod-name" id="sheetName">—</p>
      <p class="sheet-prod-price" id="sheetPrice"></p>
      <div class="sheet-divider"></div>

      <form class="sheet-form" id="orderForm" onsubmit="return false;" novalidate>

        <div>
          <label class="form-label" for="f-name">الاسم *</label>
          <input class="form-input" id="f-name" type="text" autocomplete="name"
                 placeholder="اسمك الكريم" required>
        </div>

        <div>
          <label class="form-label" for="f-phone">رقم الهاتف *</label>
          <input class="form-input" id="f-phone" type="tel" dir="ltr" autocomplete="tel"
                 placeholder="9681XXXXXXX" required>
        </div>

        <div>
          <span class="form-label">طريقة الاستلام</span>
          <div class="delivery-row">
            <button type="button" class="dlv-btn active" id="dlvDelivery"
                    onclick="setDelivery('delivery')" aria-pressed="true">🚗&nbsp; توصيل</button>
            <button type="button" class="dlv-btn" id="dlvPickup"
                    onclick="setDelivery('pickup')" aria-pressed="false">🏪&nbsp; استلام من المحل</button>
          </div>
        </div>

        <div class="addr-wrap show" id="addrWrap">
          <label class="form-label" for="f-address">العنوان</label>
          <textarea class="form-textarea" id="f-address" rows="2"
                    placeholder="المنطقة، الشارع، رقم المنزل..."></textarea>
        </div>

        <div>
          <label class="form-label" for="f-notes">ملاحظات <span style="font-weight:400;color:var(--text-muted)">(اختياري)</span></label>
          <textarea class="form-textarea" id="f-notes" rows="2"
                    placeholder="أي تفاصيل إضافية..."></textarea>
        </div>

        <button type="button" class="submit-btn" id="submitBtn" onclick="submitOrder()">
          <span class="btn-spinner" id="btnSpinner" aria-hidden="true"></span>
          <span class="btn-text">تأكيد الطلب</span>
        </button>

      </form>
    </div>

    <!-- ══ 9. SUCCESS STATE ══ -->
    <div class="success-view" id="successView" aria-live="assertive">
      <div class="success-check" aria-hidden="true">✓</div>
      <h2 class="success-title">تم إرسال طلبك! 🌸</h2>
      <p class="success-sub">سنتواصل معك قريباً على رقم هاتفك</p>
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
      currentCategory = cat;
      document.querySelectorAll('.cat-pill').forEach(function(el) {
        var isActive = el.dataset.cat === cat;
        el.classList.toggle('active', isActive);
        el.setAttribute('aria-selected', String(isActive));
      });
      loadProducts(cat);
      // Scroll products into view on occasion tap
      var sec = document.getElementById('productsSection');
      if (sec) sec.scrollIntoView({ behavior: 'smooth' });
    }

    // ────────────────────────────────────────
    // LOAD PRODUCTS
    // ────────────────────────────────────────
    async function loadProducts(category) {
      renderSkeletons();
      try {
        var qs  = (!category || category === 'all') ? '' : '?category=' + encodeURIComponent(category);
        var res = await fetch('/api/store/products' + qs);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        var data = await res.json();
        var list = Array.isArray(data) ? data : (data.products || []);
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
      var g = document.getElementById('productsGrid');
      g.innerHTML = [0,1,2,3].map(function() {
        return '<div class="skel-card" aria-hidden="true">' +
          '<div class="skel-img"></div>' +
          '<div class="skel-body">' +
            '<div class="skel-line"></div>' +
            '<div class="skel-line w70"></div>' +
            '<div class="skel-line w45"></div>' +
          '</div>' +
        '</div>';
      }).join('');
    }

    function renderProducts(products) {
      var g = document.getElementById('productsGrid');
      if (!products.length) {
        g.innerHTML =
          '<div class="empty-state">' +
            '<span class="empty-icon">🌸</span>' +
            '<p class="empty-text">لا توجد منتجات في هذه الفئة</p>' +
            '<p class="empty-sub">تابعنا للجديد قريباً</p>' +
          '</div>';
        return;
      }
      g.innerHTML = products.map(function(p, idx) {
        var safe     = JSON.stringify(p).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        var priceStr = p.price ? formatPrice(p.price) + ' ر.ع' : null;
        var imgTag   = p.img
          ? '<img src="' + esc(p.img) + '" alt="' + esc(p.name) + '" loading="lazy"' +
            ' onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">'
          : '';
        var placeholderStyle = p.img ? 'display:none;' : '';
        var badge    = (idx < 2) ? '<span class="card-new-badge" aria-label="منتج جديد">جديد</span>' : '';
        var priceHtml = priceStr
          ? '<span class="card-price">' + esc(priceStr) + '</span>'
          : '<span class="card-price-on-request">السعر عند الطلب</span>';
        return '<article class="prod-card" role="button" tabindex="0"' +
          ' onclick="openOrderSheet(\'' + safe + '\')"' +
          ' onkeydown="if(event.key===\'Enter\')openOrderSheet(\'' + safe + '\')"' +
          ' aria-label="' + esc(p.name) + '">' +
          '<div class="card-img-wrap">' +
            imgTag +
            '<div class="card-img-placeholder" style="' + placeholderStyle + '" aria-hidden="true">🌸</div>' +
            badge +
          '</div>' +
          '<div class="card-body">' +
            '<p class="card-name">' + esc(p.name) + '</p>' +
            '<p class="card-category">' + esc(p.category || '') + '</p>' +
            '<div class="card-price-row">' +
              priceHtml +
              '<button class="card-order-btn" tabindex="-1" aria-hidden="true">اطلب</button>' +
            '</div>' +
          '</div>' +
        '</article>';
      }).join('');
    }

    function renderError() {
      document.getElementById('productsGrid').innerHTML =
        '<div class="empty-state">' +
          '<span class="empty-icon">🌸</span>' +
          '<p class="empty-text">تعذّر تحميل المنتجات</p>' +
          '<p class="empty-sub">يرجى المحاولة لاحقاً</p>' +
        '</div>';
    }

    function formatPrice(price) {
      var n = parseFloat(price);
      if (isNaN(n)) return String(price);
      return n.toFixed(3);
    }

    function esc(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g,  '&amp;')
        .replace(/</g,  '&lt;')
        .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;')
        .replace(/'/g,  '&#39;');
    }

    // ────────────────────────────────────────
    // ORDER SHEET — OPEN / CLOSE
    // ────────────────────────────────────────
    function openOrderSheet(productJson) {
      var product = (typeof productJson === 'string') ? JSON.parse(productJson) : productJson;
      selectedProduct = product;

      // Reset success state
      document.getElementById('sheetFormContent').style.display = '';
      document.getElementById('successView').classList.remove('show');

      // Populate
      document.getElementById('sheetName').textContent  = product.name || '—';
      var priceStr = product.price ? formatPrice(product.price) + ' ر.ع' : 'السعر عند الطلب';
      document.getElementById('sheetPrice').textContent = priceStr;

      // Reset form fields
      document.getElementById('f-name').value    = '';
      document.getElementById('f-phone').value   = '';
      document.getElementById('f-address').value = '';
      document.getElementById('f-notes').value   = '';
      setDelivery('delivery');
      resetSubmitBtn();

      document.getElementById('sheetOverlay').classList.add('open');
      document.getElementById('orderSheet').classList.add('open');
      document.body.style.overflow = 'hidden';

      setTimeout(function() {
        var fn = document.getElementById('f-name');
        if (fn) fn.focus();
      }, 380);
    }

    function closeOrderSheet() {
      document.getElementById('sheetOverlay').classList.remove('open');
      document.getElementById('orderSheet').classList.remove('open');
      document.body.style.overflow = '';
      selectedProduct = null;
    }

    // Escape key closes sheet
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeOrderSheet();
    });

    // ────────────────────────────────────────
    // DELIVERY TOGGLE
    // ────────────────────────────────────────
    function setDelivery(mode) {
      deliveryMode = mode;
      var dlvBtn    = document.getElementById('dlvDelivery');
      var pickupBtn = document.getElementById('dlvPickup');
      dlvBtn.classList.toggle('active',    mode === 'delivery');
      pickupBtn.classList.toggle('active', mode === 'pickup');
      dlvBtn.setAttribute('aria-pressed',    String(mode === 'delivery'));
      pickupBtn.setAttribute('aria-pressed', String(mode === 'pickup'));
      document.getElementById('addrWrap').classList.toggle('show', mode === 'delivery');
    }

    // ────────────────────────────────────────
    // SUBMIT ORDER
    // ────────────────────────────────────────
    async function submitOrder() {
      var name  = document.getElementById('f-name').value.trim();
      var phone = document.getElementById('f-phone').value.trim();

      if (!name) {
        shakeField('f-name');
        document.getElementById('f-name').focus();
        return;
      }
      if (!phone) {
        shakeField('f-phone');
        document.getElementById('f-phone').focus();
        return;
      }

      var btn = document.getElementById('submitBtn');
      btn.disabled = true;
      btn.classList.add('loading');

      var payload = {
        product_id:     selectedProduct ? (selectedProduct.id || null) : null,
        product_name:   selectedProduct ? (selectedProduct.name || '') : '',
        customer_name:  name,
        customer_phone: phone,
        delivery_type:  deliveryMode,
        address:        deliveryMode === 'delivery'
                          ? document.getElementById('f-address').value.trim()
                          : '',
        notes:          document.getElementById('f-notes').value.trim(),
      };

      try {
        var res = await fetch('/api/store/order', {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify(payload),
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);

        orderCount++;
        var badge = document.getElementById('cartBadge');
        badge.textContent = orderCount;
        badge.classList.add('visible');

        showSuccess();
      } catch (err) {
        console.error('submitOrder:', err);
        resetSubmitBtn();
        shakeField('submitBtn');
      }
    }

    function resetSubmitBtn() {
      var btn = document.getElementById('submitBtn');
      btn.disabled = false;
      btn.classList.remove('loading');
    }

    function shakeField(id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.style.borderColor = '#e05555';
      if (el.animate) {
        el.animate([
          { transform: 'translateX(0)' },
          { transform: 'translateX(-5px)' },
          { transform: 'translateX(5px)' },
          { transform: 'translateX(-3px)' },
          { transform: 'translateX(0)' },
        ], { duration: 280, easing: 'ease' });
      }
      setTimeout(function() { el.style.borderColor = ''; }, 900);
    }

    // ────────────────────────────────────────
    // SUCCESS STATE
    // ────────────────────────────────────────
    function showSuccess() {
      document.getElementById('sheetFormContent').style.display = 'none';
      document.getElementById('successView').classList.add('show');
      document.getElementById('orderSheet').scrollTop = 0;
    }

    // ────────────────────────────────────────
    // INIT
    // ────────────────────────────────────────
    loadProducts('all');
  </script>
</body>
</html>"""
