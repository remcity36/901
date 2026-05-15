/* LAB301 / OPERATIONS — shared chrome + palette controls */
(function(){
  // ── Clean URL: strip .html from address bar (GitHub Pages only, not file://)
  try {
    if (window.location.protocol !== 'file:' && window.location.pathname.endsWith('.html')) {
      var cleanPath = window.location.pathname.slice(0, -5);
      history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
    }
  } catch(e) {}
  const NAMES = {
    signal:"SIGNAL // 01", cyber:"CYBER // 02", acid:"ACID // 03",
    magenta:"PLASMA // 04", amber:"SODIUM // 05", ice:"ARCTIC // 06"
  };
  const root = document.documentElement;

  // ── pick up saved settings
  try {
    const p = localStorage.getItem('lab301.palette');
    const d = localStorage.getItem('lab301.density');
    const l = localStorage.getItem('lab301.lang');
    const bg = localStorage.getItem('lab301.bg');
    if (p && NAMES[p]) root.setAttribute('data-palette', p);
    if (d) root.setAttribute('data-density', d);
    if (l === 'en') root.setAttribute('lang', 'en');
    if (bg === 'grey') root.setAttribute('data-bg', 'grey');
  } catch(e){}

  // Translation dictionary for chrome + common UI strings
  const lang = root.getAttribute('lang') === 'en' ? 'en' : 'ru';
  const T = {
    ru: {
      home:'Главная', services:'Услуги', sites:'Сайты', ai:'AI-Ассистент', process:'Процесс', cases:'Архив', faq:'FAQ', contacts:'Контакты',
      live:'LAB301 / OPERATIONS LIVE', sys:'SYS · STABLE', uptime:'UPTIME · 99.98%', queue:'QUEUE · 03', tz:'MSK GMT+3',
      cta:'Заказать сайт', menuOpen:'Открыть меню', backHome:'LAB301 — на главную',
      fBrand:'LAB301 / OPS', fAbout:'Лаборатория, которая собирает сайты, AI‑агентов и&nbsp;автоматизации для роста&nbsp;бизнеса.',
      fNav:'Навигация', fSvc:'Сервисы', fLink:'Связь',
      fSvcSite:'Сайт под ключ', fSvcAi:'AI‑агент', fSvcAuto:'Автоматизация', fSvcPerf:'Performance',
      fLegal1:'WhatsApp принадлежит компании Meta, деятельность которой признана экстремистской и&nbsp;запрещена на&nbsp;территории РФ.',
      fLegal2:'Информация на&nbsp;сайте носит ознакомительный характер и&nbsp;не&nbsp;является публичной офертой в&nbsp;соответствии со&nbsp;ст.&nbsp;437 ГК&nbsp;РФ.',
      fCopy:'© LAB301 · 2026 · все&nbsp;права&nbsp;защищены', fBuild:'BUILD', fPalette:'PALETTE',
      fPowered:'Михалыч powered by AI · Built with',
      dPalette:'ПАЛИТРА', dDensity:'ПЛОТНОСТЬ', dCompact:'Compact', dComfort:'Comfortable', dSpacious:'Spacious',
      dLang:'Язык', dA11y:'Режим доступности'
    },
    en: {
      home:'Home', services:'Services', sites:'Sites', ai:'AI Assistant', process:'Process', cases:'Archive', faq:'FAQ', contacts:'Contacts',
      live:'LAB301 / OPERATIONS LIVE', sys:'SYS · STABLE', uptime:'UPTIME · 99.98%', queue:'QUEUE · 03', tz:'MSK GMT+3',
      cta:'Order a site', menuOpen:'Open menu', backHome:'LAB301 — home',
      fBrand:'LAB301 / OPS', fAbout:'A lab building websites, AI&nbsp;agents and automations that move business metrics.',
      fNav:'Navigation', fSvc:'Services', fLink:'Contact',
      fSvcSite:'Website turnkey', fSvcAi:'AI agent', fSvcAuto:'Automation', fSvcPerf:'Performance',
      fLegal1:'WhatsApp is owned by Meta, whose activities are recognized as extremist and prohibited in&nbsp;the&nbsp;Russian Federation.',
      fLegal2:'Information on&nbsp;the&nbsp;site is for reference only and does not constitute a&nbsp;public offer under Art.&nbsp;437 of&nbsp;the&nbsp;Civil Code of&nbsp;the&nbsp;Russian Federation.',
      fCopy:'© LAB301 · 2026 · all&nbsp;rights&nbsp;reserved', fBuild:'BUILD', fPalette:'PALETTE',
      fPowered:'Mikhalych powered by AI · Built with',
      dPalette:'PALETTE', dDensity:'DENSITY', dCompact:'Compact', dComfort:'Comfortable', dSpacious:'Spacious',
      dLang:'Language', dA11y:'Accessibility mode'
    }
  };
  const t = T[lang];

  // ── ribbon + nav + footer + dock chrome
  const palette = root.getAttribute('data-palette') || 'signal';
  const density = root.getAttribute('data-density') || 'comfortable';

  const pageId = document.body.dataset.page || '';
  const NAV = [
    { id:'home',     i:'00', label:t.home,     href:'index.html' },
    { id:'services', i:'01', label:t.services, href:'services.html' },
    { id:'sites',    i:'02', label:t.sites,    href:'sites.html' },
    { id:'ai',       i:'03', label:t.ai,       href:'ai-assistant.html' },
    { id:'process',  i:'04', label:t.process,  href:'process.html' },
    { id:'cases',    i:'05', label:t.cases,    href:'cases.html' },
    { id:'faq',      i:'06', label:t.faq,      href:'faq.html' },
    { id:'contacts', i:'07', label:t.contacts, href:'contacts.html' },
  ];

  const now = new Date();
  const dd = String(now.getDate()).padStart(2,'0');
  const mm = String(now.getMonth()+1).padStart(2,'0');
  const yy = String(now.getFullYear()).slice(2);

  const ribbon = `
    <div class="ribbon">
      <span class="live">${t.live}</span>
      <div class="ribbon-mid">
        <span>${t.sys}</span>
        <span>${t.uptime}</span>
        <span>${t.queue}</span>
        <span>${t.tz}</span>
      </div>
      <span class="mono">${dd}.${mm}.${yy}</span>
    </div>`;

  const navLinks = NAV.map(n =>
    `<li><a data-i="${n.i}" href="${n.href}"${n.id===pageId?' aria-current="page"':''}>${n.label}</a></li>`
  ).join('');

  const drawerLinks = NAV.map(n =>
    `<li><a data-i="${n.i}" href="${n.href}"${n.id===pageId?' aria-current="page"':''}>${n.label}</a></li>`
  ).join('');

  const nav = `
    <nav class="topnav">
      <a class="logo" href="index.html" aria-label="${t.backHome}">
        <img src="lab301-logo-mobile.png" alt="LAB301" class="logo-img" width="1200" height="630" />
        <span class="dim">AI automation &amp; digital studio</span>
      </a>
      <ul class="nav-links">${navLinks}</ul>
      <a class="nav-cta" href="https://t.me/Judgeopenclawbot" target="_blank">${t.cta} <span class="arrow">→</span></a>
      <div class="nav-mobile-controls">
        <button class="bg-toggle nav-bg-toggle" id="bgToggle" aria-label="Сменить фон" title="Тёмный / Чёрный фон">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13V1.5z" fill="currentColor"/></svg>
        </button>
        <button class="hamburger" id="hamburger" aria-label="${t.menuOpen}" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>
    <div class="mobile-drawer" id="mobileDrawer" aria-hidden="true">
      <ul class="drawer-links">${drawerLinks}</ul>
      <div class="drawer-cta">
        <a class="btn-primary" href="https://t.me/Judgeopenclawbot" target="_blank">Заказать сайт <span>→</span></a>
        <a class="btn-secondary" href="tel:+79996708772">+7 999 670 87 72</a>
        <a class="btn-secondary" href="mailto:lab.301@ya.ru">lab.301@ya.ru</a>
      </div>
    </div>
    <a class="fab-order" href="https://t.me/Judgeopenclawbot" target="_blank" aria-label="Заказать сайт">
      <span class="fab-text">Заказать сайт</span>
    </a>`;

  const footer = `
    <footer>
      <div class="container">
        <div class="f-grid">
          <div class="f-brand">
            <img src="guga.webp" alt="LAB301" class="f-logo-img" style="height:160px;" width="1200" height="630" />
            <p>${t.fAbout}</p>
            <div class="f-powered">
              <span>${t.fPowered}</span>
              <img src="image-151.webp" alt="Mikhalych AI" class="f-powered-img" width="1768" height="363" />
            </div>
            <div class="f-stack">OpenAI &middot; Anthropic &middot; Next.js &middot; Vercel &middot; Figma &middot; n8n</div>
          </div>
          <div class="f-col">
            <h5>${t.fNav}</h5>
            <ul>
              <li><a href="services.html">${t.services}</a></li>
              <li><a href="sites.html">${t.sites}</a></li>
              <li><a href="ai-assistant.html">${t.ai}</a></li>
              <li><a href="process.html">${t.process}</a></li>
              <li><a href="cases.html">${t.cases}</a></li>
              <li><a href="faq.html">${t.faq}</a></li>
            </ul>
          </div>
          <div class="f-col">
            <h5>${t.fSvc}</h5>
            <ul>
              <li><a href="sites.html">${t.fSvcSite}</a></li>
              <li><a href="ai-assistant.html">${t.fSvcAi}</a></li>
              <li><a href="services.html">${t.fSvcAuto}</a></li>
              <li><a href="services.html">${t.fSvcPerf}</a></li>
              <li><a href="services.html">Брендинг и&nbsp;дизайн</a></li>
              <li><a href="services.html">Сопровождение</a></li>
              <li><a href="services.html">Яндекс Бизнес</a></li>
              <li><a href="services.html">Аналитика и&nbsp;аудит</a></li>
            </ul>
          </div>
          <div class="f-col">
            <h5>${t.fLink}</h5>
            <ul>
              <li><a href="https://t.me/yuriybyg">Telegram</a></li>
              <li><a href="https://wa.me/79996708772">WhatsApp</a></li>
              <li><a href="tel:+79996708772">+7 999 670 87 72</a></li>
              <li><a href="mailto:lab.301@ya.ru">lab.301@ya.ru</a></li>
            </ul>
          </div>
        </div>
        <div class="f-legal">
          <p>${t.fLegal1}</p>
          <p>${t.fLegal2}</p>
        </div>
        <div class="f-bot">
          <span>${t.fCopy}</span>
          <span>Built for humans. <span style="color:var(--acc)">Optimized by AI.</span></span>
        </div>
      </div>
    </footer>`;


  // Batch all DOM reads first to prevent forced reflow (read-write-read-write pattern)
  const hasLayers = !!document.querySelector('.grid-bg');
  const hasNav    = !!document.querySelector('nav.topnav');
  const hasRibbon = !!document.querySelector('.ribbon');
  const hasFooter = !!document.querySelector('footer');
  const hasBgBtn  = !!document.querySelector('.bg-toggle:not(.nav-bg-toggle)');

  // Then batch all DOM writes
  if (!hasLayers && window.innerWidth > 768) {
    const layers = document.createElement('div');
    layers.innerHTML = '<div class="grid-bg"></div><div class="bloom"></div><div class="grain"></div>';
    document.body.prepend(...layers.children);
  }

  // mount chrome
  const mount = (where, html) => {
    const tmp = document.createElement('div');
    tmp.innerHTML = html.trim();
    where(tmp.firstElementChild);
  };
  if (!hasNav) {
    const tmp = document.createElement('div');
    tmp.innerHTML = nav.trim();
    document.body.prepend(...tmp.children);
  }
  if (!hasRibbon) mount(n => document.body.prepend(n), ribbon);
  if (!hasFooter)  mount(n => document.body.appendChild(n), footer);

  // ── Background toggle button (desktop floating)
  if (!hasBgBtn) {
    const btn = document.createElement('button');
    btn.className = 'bg-toggle';
    btn.setAttribute('aria-label', 'Сменить фон');
    btn.title = 'Тёмный / Чёрный фон';
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13V1.5z" fill="currentColor"/></svg>';
    document.body.appendChild(btn);
  }
  // shared toggle logic for all .bg-toggle buttons
  const bgToggleHandler = () => {
    const isGrey = root.getAttribute('data-bg') === 'grey';
    if (isGrey) { root.removeAttribute('data-bg'); }
    else { root.setAttribute('data-bg', 'grey'); }
    try { localStorage.setItem('lab301.bg', isGrey ? '' : 'grey'); } catch(e){}
  };
  document.querySelectorAll('.bg-toggle').forEach(b => b.addEventListener('click', bgToggleHandler));

  // ── reveal on scroll
  const io = new IntersectionObserver(es => {
    es.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // ── FAQ accordion
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', () => item.classList.toggle('open'));
  });

  // ── Hero swatch parallax (skip if reduced motion preferred)
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!prefersReduced) {
    document.querySelectorAll('.hero-title .swatch, .page-head .swatch').forEach(swatch => {
      document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - .5) * 8;
        const y = (e.clientY / window.innerHeight - .5) * 8;
        swatch.style.transform = `translate(${x}px, ${y}px)`;
      });
    });
  }

  // ── Hamburger / mobile drawer
  const hamburger = document.getElementById('hamburger');
  const drawer = document.getElementById('mobileDrawer');
  if (hamburger && drawer) {
    const toggleDrawer = (force) => {
      const isOpen = typeof force === 'boolean' ? force : !drawer.classList.contains('open');
      drawer.classList.toggle('open', isOpen);
      hamburger.classList.toggle('active', isOpen);
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      drawer.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    };
    hamburger.addEventListener('click', () => toggleDrawer());
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', () => toggleDrawer(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') toggleDrawer(false); });
  }

  // ── Language toggle (RU ↔ EN)
  const applyTranslations = (targetLang) => {
    document.querySelectorAll('[data-en]').forEach(el => {
      if (!el.hasAttribute('data-ru')) el.setAttribute('data-ru', el.innerHTML);
      el.innerHTML = targetLang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-ru');
    });
    document.querySelectorAll('[data-en-attr]').forEach(el => {
      const spec = el.getAttribute('data-en-attr');
      spec.split('|').forEach(pair => {
        const [attr, val] = pair.split(':');
        if (!el.hasAttribute('data-ru-' + attr)) el.setAttribute('data-ru-' + attr, el.getAttribute(attr) || '');
        el.setAttribute(attr, targetLang === 'en' ? val : el.getAttribute('data-ru-' + attr));
      });
    });
    document.documentElement.setAttribute('lang', targetLang);
    document.title = targetLang === 'en' && document.title.match(/[А-Яа-я]/) ? (document.querySelector('meta[name="title-en"]')?.content || document.title) : document.title;
  };
  applyTranslations(lang);


  // ── Pulsing green dot for ONLINE status indicators
  document.querySelectorAll('.sig, .v, .hero-coord > div').forEach(el => {
    if (el.textContent.includes('ONLINE')) {
      el.innerHTML = el.innerHTML.replace(/(?:<span[^>]*>)?●(?:<\/span>)?\s*/g, '<span class="online-dot"></span>');
    }
  });
})();
