from config import *

STORE_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>فيروز فلورز</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --bg-primary: #0d1a18;
      --bg-card: #111f1d;
      --bg-card-hover: #162422;
      --bg-input: #0a1614;
      --bg-sheet: #0f1d1b;
      --gold: #c8914a;
      --gold-light: #e0a85e;
      --gold-dark: #a87238;
      --gold-gradient: linear-gradient(135deg, #c8914a 0%, #e0a85e 50%, #c8914a 100%);
      --text-white: #f5f0e8;
      --text-muted: #8a9e9b;
      --text-dark: #0d1a18;
      --border-subtle: rgba(200, 145, 74, 0.15);
      --border-gold: rgba(200, 145, 74, 0.5);
      --overlay: rgba(0, 0, 0, 0.65);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-pill: 50px;
      --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
      --shadow-gold: 0 2px 16px rgba(200, 145, 74, 0.2);
      --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    html {
      background: var(--bg-primary);
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Tajawal', sans-serif;
      background: var(--bg-primary);
      color: var(--text-white);
      min-height: 100vh;
      max-width: 430px;
      margin: 0 auto;
      position: relative;
      overflow-x: hidden;
    }

    /* ═══════════════════════════════
       HERO SECTION
    ═══════════════════════════════ */
    .hero {
      position: relative;
      width: 100%;
      height: 50vh;
      min-height: 280px;
      background-image: url('/background.jpg');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      overflow: hidden;
    }

    .hero::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        to bottom,
        rgba(13, 26, 24, 0.1) 0%,
        rgba(13, 26, 24, 0.3) 40%,
        rgba(13, 26, 24, 0.85) 75%,
        rgba(13, 26, 24, 1) 100%
      );
      z-index: 1;
    }

    .hero-content {
      position: relative;
      z-index: 2;
      text-align: center;
      padding: 0 24px 32px;
      width: 100%;
    }

    .hero-title {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2rem, 8vw, 2.8rem);
      font-weight: 700;
      color: var(--gold);
      letter-spacing: 0.02em;
      line-height: 1.2;
      text-shadow: 0 2px 20px rgba(200, 145, 74, 0.4);
      margin-bottom: 8px;
    }

    .hero-tagline {
      font-family: 'Tajawal', sans-serif;
      font-size: 1rem;
      font-weight: 300;
      color: rgba(245, 240, 232, 0.85);
      letter-spacing: 0.05em;
    }

    /* ═══════════════════════════════
       CATEGORY TABS
    ═══════════════════════════════ */
    .category-section {
      padding: 20px 0 12px;
      background: var(--bg-primary);
      position: sticky;
      top: 0;
      z-index: 10;
      border-bottom: 1px solid var(--border-subtle);
    }

    .category-scroll {
      display: flex;
      gap: 8px;
      padding: 0 16px;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      flex-direction: row-reverse;
    }

    .category-scroll::-webkit-scrollbar {
      display: none;
    }

    .cat-tab {
      flex-shrink: 0;
      padding: 8px 18px;
      border-radius: var(--radius-pill);
      font-family: 'Tajawal', sans-serif;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      border: 1.5px solid var(--gold);
      background: transparent;
      color: var(--gold);
      transition: var(--transition);
      white-space: nowrap;
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    }

    .cat-tab:active {
      transform: scale(0.96);
    }

    .cat-tab.active {
      background: var(--gold-gradient);
      color: var(--text-dark);
      font-weight: 700;
      border-color: transparent;
      box-shadow: var(--shadow-gold);
    }

    /* ═══════════════════════════════
       PRODUCTS GRID
    ═══════════════════════════════ */
    .products-section {
      padding: 16px;
    }

    .products-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    /* Product Card */
    .product-card {
      background: var(--bg-card);
      border-radius: var(--radius-md);
      overflow: hidden;
      box-shadow: var(--shadow-card);
      border: 1px solid var(--border-subtle);
      transition: var(--transition);
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
    }

    .product-card:active {
      transform: scale(0.98);
    }

    .card-image-wrap {
      position: relative;
      aspect-ratio: 1 / 1;
      overflow: hidden;
    }

    .card-image-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }

    .product-card:hover .card-image-wrap img {
      transform: scale(1.04);
    }

    .card-badge {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(13, 26, 24, 0.82);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      color: var(--gold);
      font-size: 0.65rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-gold);
      white-space: nowrap;
    }

    .card-body {
      padding: 10px 10px 12px;
    }

    .card-name {
      font-size: 0.825rem;
      font-weight: 700;
      color: var(--text-white);
      margin-bottom: 6px;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .card-price {
      font-family: 'Playfair Display', serif;
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--gold);
      margin-bottom: 10px;
      display: flex;
      align-items: baseline;
      gap: 3px;
    }

    .card-price .currency {
      font-family: 'Tajawal', sans-serif;
      font-size: 0.7rem;
      font-weight: 500;
      opacity: 0.8;
    }

    .card-btn {
      width: 100%;
      padding: 8px 0;
      background: var(--gold-gradient);
      color: var(--text-dark);
      font-family: 'Tajawal', sans-serif;
      font-size: 0.8rem;
      font-weight: 700;
      border: none;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: var(--transition);
      letter-spacing: 0.02em;
      -webkit-tap-highlight-color: transparent;
    }

    .card-btn:active {
      transform: scale(0.97);
      filter: brightness(0.9);
    }

    /* Skeleton Loading */
    .skeleton-card {
      background: var(--bg-card);
      border-radius: var(--radius-md);
      overflow: hidden;
      border: 1px solid var(--border-subtle);
    }

    .skeleton-img {
      aspect-ratio: 1 / 1;
      background: linear-gradient(90deg, #152220 25%, #1c302d 50%, #152220 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }

    .skeleton-body {
      padding: 10px;
    }

    .skeleton-line {
      height: 12px;
      border-radius: 6px;
      background: linear-gradient(90deg, #152220 25%, #1c302d 50%, #152220 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
      margin-bottom: 8px;
    }

    .skeleton-line.short { width: 60%; }
    .skeleton-line.btn { height: 30px; border-radius: var(--radius-sm); margin-bottom: 0; }

    @keyframes shimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }

    /* Empty State */
    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
    }

    .empty-state .empty-icon {
      font-size: 3rem;
      margin-bottom: 12px;
      display: block;
    }

    .empty-state p {
      font-size: 0.95rem;
      line-height: 1.6;
    }

    /* ═══════════════════════════════
       OVERLAY
    ═══════════════════════════════ */
    .overlay {
      position: fixed;
      inset: 0;
      background: var(--overlay);
      backdrop-filter: blur(3px);
      -webkit-backdrop-filter: blur(3px);
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: opacity var(--transition);
    }

    .overlay.visible {
      opacity: 1;
      pointer-events: all;
    }

    /* ═══════════════════════════════
       ORDER BOTTOM SHEET
    ═══════════════════════════════ */
    .order-sheet {
      position: fixed;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%) translateY(100%);
      width: 100%;
      max-width: 430px;
      background: var(--bg-sheet);
      border-radius: var(--radius-lg) var(--radius-lg) 0 0;
      z-index: 101;
      transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1);
      max-height: 92vh;
      overflow-y: auto;
      scrollbar-width: none;
      padding-bottom: calc(20px + env(safe-area-inset-bottom, 0px));
      border-top: 1px solid var(--border-gold);
    }

    .order-sheet::-webkit-scrollbar {
      display: none;
    }

    .order-sheet.open {
      transform: translateX(-50%) translateY(0);
    }

    .sheet-handle {
      width: 40px;
      height: 4px;
      background: var(--border-gold);
      border-radius: 2px;
      margin: 12px auto 0;
    }

    .sheet-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px 12px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .sheet-title {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 400;
    }

    .sheet-product-name {
      font-family: 'Playfair Display', serif;
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--gold);
      margin-top: 2px;
      max-width: 240px;
    }

    .sheet-close {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: rgba(200, 145, 74, 0.1);
      border: 1px solid var(--border-gold);
      color: var(--gold);
      font-size: 1.1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      flex-shrink: 0;
      transition: var(--transition);
      -webkit-tap-highlight-color: transparent;
    }

    .sheet-close:active {
      background: rgba(200, 145, 74, 0.2);
      transform: scale(0.93);
    }

    .sheet-form {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .form-label {
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-muted);
      letter-spacing: 0.03em;
    }

    .form-label .required {
      color: var(--gold);
      margin-right: 2px;
    }

    .form-input,
    .form-textarea {
      width: 100%;
      background: var(--bg-input);
      border: 1.5px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      color: var(--text-white);
      font-family: 'Tajawal', sans-serif;
      font-size: 0.95rem;
      padding: 11px 14px;
      outline: none;
      transition: border-color var(--transition), box-shadow var(--transition);
      -webkit-appearance: none;
    }

    .form-input::placeholder,
    .form-textarea::placeholder {
      color: var(--text-muted);
      opacity: 0.6;
    }

    .form-input:focus,
    .form-textarea:focus {
      border-color: var(--gold);
      box-shadow: 0 0 0 3px rgba(200, 145, 74, 0.12);
    }

    .form-textarea {
      resize: none;
      height: 80px;
      line-height: 1.5;
    }

    /* Delivery Toggle */
    .delivery-toggle {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .delivery-btn {
      padding: 10px 8px;
      border-radius: var(--radius-sm);
      border: 1.5px solid var(--border-gold);
      background: transparent;
      color: var(--text-muted);
      font-family: 'Tajawal', sans-serif;
      font-size: 0.875rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
      text-align: center;
      -webkit-tap-highlight-color: transparent;
    }

    .delivery-btn.active {
      background: rgba(200, 145, 74, 0.12);
      border-color: var(--gold);
      color: var(--gold);
    }

    .delivery-btn:active {
      transform: scale(0.97);
    }

    .address-group {
      overflow: hidden;
      max-height: 0;
      opacity: 0;
      transition: max-height 0.3s ease, opacity 0.3s ease;
    }

    .address-group.visible {
      max-height: 120px;
      opacity: 1;
    }

    .submit-btn {
      width: 100%;
      padding: 14px;
      background: var(--gold-gradient);
      color: var(--text-dark);
      font-family: 'Tajawal', sans-serif;
      font-size: 1rem;
      font-weight: 700;
      border: none;
      border-radius: var(--radius-md);
      cursor: pointer;
      letter-spacing: 0.02em;
      transition: var(--transition);
      box-shadow: var(--shadow-gold);
      -webkit-tap-highlight-color: transparent;
      margin-top: 4px;
    }

    .submit-btn:active {
      transform: scale(0.98);
      filter: brightness(0.92);
    }

    .submit-btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    /* ═══════════════════════════════
       SUCCESS TOAST
    ═══════════════════════════════ */
    .toast {
      position: fixed;
      top: calc(16px + env(safe-area-inset-top, 0px));
      left: 50%;
      transform: translateX(-50%) translateY(-120%);
      z-index: 200;
      background: #1a3d2b;
      border: 1px solid #2d6b47;
      color: #7edd9f;
      padding: 12px 20px;
      border-radius: var(--radius-pill);
      font-family: 'Tajawal', sans-serif;
      font-size: 0.9rem;
      font-weight: 600;
      white-space: nowrap;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
      transition: transform 0.4s cubic-bezier(0.32, 0.72, 0, 1);
      pointer-events: none;
    }

    .toast.show {
      transform: translateX(-50%) translateY(0);
    }

    /* ═══════════════════════════════
       FOOTER
    ═══════════════════════════════ */
    .footer {
      text-align: center;
      padding: 32px 20px calc(24px + env(safe-area-inset-bottom, 0px));
      border-top: 1px solid var(--border-subtle);
      margin-top: 24px;
    }

    .footer-text {
      font-size: 0.75rem;
      color: var(--text-muted);
      opacity: 0.6;
      font-family: 'Playfair Display', serif;
      letter-spacing: 0.05em;
    }

    .footer-admin {
      display: inline-block;
      margin-top: 8px;
      font-size: 0.7rem;
      color: transparent;
      text-decoration: none;
      opacity: 0.08;
      transition: opacity 0.2s;
      user-select: none;
    }

    .footer-admin:hover {
      opacity: 0.3;
    }

    /* ═══════════════════════════════
       UTILITIES
    ═══════════════════════════════ */
    .visually-hidden {
      position: absolute;
      width: 1px;
      height: 1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body>

  <!-- ═══ HERO ═══ -->
  <section class="hero" role="banner">
    <div class="hero-content">
      <h1 class="hero-title">فيروز فلورز</h1>
      <p class="hero-tagline">أجمل الورود لأجمل اللحظات</p>
    </div>
  </section>

  <!-- ═══ CATEGORY TABS ═══ -->
  <nav class="category-section" aria-label="تصفية المنتجات">
    <div class="category-scroll" role="tablist">
      <button class="cat-tab active" role="tab" aria-selected="true"  onclick="filterCategory('all')"       data-cat="all">الكل</button>
      <button class="cat-tab"        role="tab" aria-selected="false" onclick="filterCategory('باقات')"     data-cat="باقات">باقات</button>
      <button class="cat-tab"        role="tab" aria-selected="false" onclick="filterCategory('استاندات')"  data-cat="استاندات">استاندات</button>
      <button class="cat-tab"        role="tab" aria-selected="false" onclick="filterCategory('مجسمات')"    data-cat="مجسمات">مجسمات</button>
      <button class="cat-tab"        role="tab" aria-selected="false" onclick="filterCategory('شرايط')"     data-cat="شرايط">شرايط</button>
    </div>
  </nav>

  <!-- ═══ PRODUCTS ═══ -->
  <main class="products-section" id="products-section">
    <div class="products-grid" id="products-grid" aria-live="polite" aria-label="قائمة المنتجات">
      <!-- Populated by JS -->
    </div>
  </main>

  <!-- ═══ FOOTER ═══ -->
  <footer class="footer">
    <p class="footer-text">© فيروز فلورز</p>
    <a href="/admin" class="footer-admin" tabindex="-1" aria-hidden="true">🔐</a>
  </footer>

  <!-- ═══ OVERLAY ═══ -->
  <div class="overlay" id="overlay" onclick="closeSheet()" role="presentation"></div>

  <!-- ═══ ORDER BOTTOM SHEET ═══ -->
  <div class="order-sheet" id="orderSheet" role="dialog" aria-modal="true" aria-labelledby="sheetProductName">
    <div class="sheet-handle" role="presentation"></div>

    <div class="sheet-header">
      <div>
        <p class="sheet-title">طلب منتج</p>
        <p class="sheet-product-name" id="sheetProductName">—</p>
      </div>
      <button class="sheet-close" onclick="closeSheet()" aria-label="إغلاق">✕</button>
    </div>

    <form class="sheet-form" id="orderForm" onsubmit="submitOrder(event)" novalidate>

      <div class="form-group">
        <label class="form-label" for="customerName">
          <span class="required">*</span> الاسم
        </label>
        <input
          class="form-input"
          id="customerName"
          type="text"
          placeholder="اكتب اسمك الكريم"
          autocomplete="name"
          required
        >
      </div>

      <div class="form-group">
        <label class="form-label" for="customerPhone">
          <span class="required">*</span> رقم الهاتف
        </label>
        <input
          class="form-input"
          id="customerPhone"
          type="tel"
          dir="ltr"
          placeholder="+968 XXXX XXXX"
          autocomplete="tel"
          required
        >
      </div>

      <div class="form-group">
        <p class="form-label">نوع الاستلام</p>
        <div class="delivery-toggle">
          <button type="button" class="delivery-btn active" id="btnDelivery"  onclick="setDelivery('delivery')">🚗 توصيل</button>
          <button type="button" class="delivery-btn"        id="btnPickup"    onclick="setDelivery('pickup')">🏪 من المحل</button>
        </div>
      </div>

      <div class="address-group visible" id="addressGroup">
        <div class="form-group">
          <label class="form-label" for="addressField">العنوان</label>
          <textarea
            class="form-textarea"
            id="addressField"
            placeholder="المنطقة، الشارع، رقم المبنى..."
          ></textarea>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label" for="notesField">ملاحظات <span style="opacity:0.5;font-weight:400;">(اختياري)</span></label>
        <textarea
          class="form-textarea"
          id="notesField"
          placeholder="أي تفاصيل إضافية..."
        ></textarea>
      </div>

      <button type="submit" class="submit-btn" id="submitBtn">تأكيد الطلب 🌸</button>

    </form>
  </div>

  <!-- ═══ SUCCESS TOAST ═══ -->
  <div class="toast" id="successToast" role="alert" aria-live="assertive">
    ✅ تم استلام طلبك! سنتواصل معك قريباً
  </div>

  <script>
    // ══════════════════════════════════════════
    // STATE
    // ══════════════════════════════════════════
    let currentCategory = 'all';
    let selectedProduct = null;
    let deliveryType    = 'delivery';

    // ══════════════════════════════════════════
    // PRODUCTS
    // ══════════════════════════════════════════
    function showSkeletons() {
      const grid = document.getElementById('products-grid');
      grid.innerHTML = Array.from({ length: 4 }, () => `
        <div class="skeleton-card" aria-hidden="true">
          <div class="skeleton-img"></div>
          <div class="skeleton-body">
            <div class="skeleton-line"></div>
            <div class="skeleton-line short"></div>
            <div class="skeleton-line btn"></div>
          </div>
        </div>
      `).join('');
    }

    function renderProducts(products) {
      const grid = document.getElementById('products-grid');
      if (!products || products.length === 0) {
        grid.innerHTML = `
          <div class="empty-state">
            <span class="empty-icon">🌸</span>
            <p>لا توجد منتجات في هذه الفئة حالياً 🌸</p>
          </div>
        `;
        return;
      }
      grid.innerHTML = products.map(p => `
        <article class="product-card" onclick="openOrder(${JSON.stringify(p).replace(/"/g, '&quot;')})" role="button" tabindex="0" aria-label="${p.name}">
          <div class="card-image-wrap">
            <img
              src="${p.image || '/placeholder.jpg'}"
              alt="${p.name}"
              loading="lazy"
              onerror="this.src='/placeholder.jpg'"
            >
            ${p.category ? `<span class="card-badge">${p.category}</span>` : ''}
          </div>
          <div class="card-body">
            <p class="card-name">${p.name}</p>
            <div class="card-price">
              <span>${formatPrice(p.price)}</span>
              <span class="currency">ر.ع</span>
            </div>
            <button class="card-btn" onclick="event.stopPropagation(); openOrder(${JSON.stringify(p).replace(/"/g, '&quot;')})">
              اطلب الآن
            </button>
          </div>
        </article>
      `).join('');
    }

    function formatPrice(price) {
      if (price == null) return '—';
      const n = parseFloat(price);
      if (isNaN(n)) return price;
      return n.toFixed(3);
    }

    async function loadProducts(category = 'all') {
      showSkeletons();
      try {
        const url = '/api/store/products' + (category && category !== 'all' ? '?category=' + encodeURIComponent(category) : '');
        const res  = await fetch(url);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        renderProducts(Array.isArray(data) ? data : data.products || []);
      } catch (err) {
        console.error('Failed to load products:', err);
        const grid = document.getElementById('products-grid');
        grid.innerHTML = `
          <div class="empty-state">
            <span class="empty-icon">⚠️</span>
            <p>تعذّر تحميل المنتجات. يرجى المحاولة مجدداً.</p>
          </div>
        `;
      }
    }

    // ══════════════════════════════════════════
    // CATEGORY FILTER
    // ══════════════════════════════════════════
    function filterCategory(cat) {
      if (currentCategory === cat) return;
      currentCategory = cat;

      document.querySelectorAll('.cat-tab').forEach(btn => {
        const isActive = btn.dataset.cat === cat;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-selected', isActive);
      });

      loadProducts(cat);
    }

    // ══════════════════════════════════════════
    // BOTTOM SHEET
    // ══════════════════════════════════════════
    function openOrder(product) {
      selectedProduct = product;

      document.getElementById('sheetProductName').textContent = product.name || '—';
      document.getElementById('customerName').value   = '';
      document.getElementById('customerPhone').value  = '';
      document.getElementById('addressField').value   = '';
      document.getElementById('notesField').value     = '';

      // Reset delivery type
      setDelivery('delivery');

      document.getElementById('overlay').classList.add('visible');
      document.getElementById('orderSheet').classList.add('open');
      document.body.style.overflow = 'hidden';

      // Focus first field after animation
      setTimeout(() => document.getElementById('customerName').focus(), 360);
    }

    function closeSheet() {
      document.getElementById('overlay').classList.remove('visible');
      document.getElementById('orderSheet').classList.remove('open');
      document.body.style.overflow = '';
      selectedProduct = null;
    }

    // Keyboard: close on Escape
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeSheet();
    });

    // ══════════════════════════════════════════
    // DELIVERY TOGGLE
    // ══════════════════════════════════════════
    function setDelivery(type) {
      deliveryType = type;
      document.getElementById('btnDelivery').classList.toggle('active', type === 'delivery');
      document.getElementById('btnPickup').classList.toggle('active',   type === 'pickup');
      document.getElementById('addressGroup').classList.toggle('visible', type === 'delivery');
    }

    // ══════════════════════════════════════════
    // SUBMIT ORDER
    // ══════════════════════════════════════════
    async function submitOrder(event) {
      event.preventDefault();

      const name  = document.getElementById('customerName').value.trim();
      const phone = document.getElementById('customerPhone').value.trim();

      if (!name) {
        document.getElementById('customerName').focus();
        shakInput('customerName');
        return;
      }
      if (!phone) {
        document.getElementById('customerPhone').focus();
        shakInput('customerPhone');
        return;
      }

      const btn = document.getElementById('submitBtn');
      btn.disabled    = true;
      btn.textContent = 'جاري الإرسال...';

      const payload = {
        product_id:     selectedProduct?.id     || null,
        product_name:   selectedProduct?.name   || '',
        customer_name:  name,
        customer_phone: phone,
        delivery_type:  deliveryType,
        address:        deliveryType === 'delivery' ? document.getElementById('addressField').value.trim() : '',
        notes:          document.getElementById('notesField').value.trim(),
      };

      try {
        const res = await fetch('/api/store/order', {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify(payload),
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);

        closeSheet();
        showToast();
      } catch (err) {
        console.error('Order failed:', err);
        btn.disabled    = false;
        btn.textContent = 'تأكيد الطلب 🌸';
        showErrorToast();
      }
    }

    function shakInput(id) {
      const el = document.getElementById(id);
      el.style.borderColor = '#e05555';
      el.style.animation = 'none';
      requestAnimationFrame(() => {
        el.style.animation = 'shake 0.35s ease';
      });
      setTimeout(() => {
        el.style.borderColor = '';
        el.style.animation   = '';
      }, 800);
    }

    // ══════════════════════════════════════════
    // TOAST
    // ══════════════════════════════════════════
    let toastTimer = null;

    function showToast(message) {
      const toast = document.getElementById('successToast');
      if (message) toast.textContent = message;
      else toast.textContent = '✅ تم استلام طلبك! سنتواصل معك قريباً';
      toast.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove('show'), 4000);
    }

    function showErrorToast() {
      const toast = document.getElementById('successToast');
      toast.textContent = '❌ حدث خطأ. يرجى المحاولة مجدداً.';
      toast.style.background   = '#3d1a1a';
      toast.style.borderColor  = '#6b2d2d';
      toast.style.color        = '#dd7e7e';
      toast.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.remove('show');
        toast.style.background  = '';
        toast.style.borderColor = '';
        toast.style.color       = '';
      }, 4000);
    }

    // ══════════════════════════════════════════
    // SHAKE KEYFRAMES (injected once)
    // ══════════════════════════════════════════
    (function injectShakeAnim() {
      const style = document.createElement('style');
      style.textContent = `
        @keyframes shake {
          0%,100% { transform: translateX(0); }
          20%      { transform: translateX(-6px); }
          40%      { transform: translateX(6px); }
          60%      { transform: translateX(-4px); }
          80%      { transform: translateX(4px); }
        }
      `;
      document.head.appendChild(style);
    })();

    // ══════════════════════════════════════════
    // KEYBOARD: card accessible via Enter
    // ══════════════════════════════════════════
    document.getElementById('products-grid').addEventListener('keydown', e => {
      if (e.key === 'Enter' && e.target.classList.contains('product-card')) {
        e.target.click();
      }
    });

    // ══════════════════════════════════════════
    // INIT
    // ══════════════════════════════════════════
    loadProducts('all');
  </script>
</body>
</html>"""
