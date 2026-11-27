/* Honorbrook Onyx: phone and tablet menu. The button is in the page HTML; this opens the panel,
   turns the dropdown groups into tap-to-expand sections and adds the two contact buttons. */
/* Count every click that opens the PlanEnroll booking page, by page and by where the button sits, and every tap on the text number. */
document.addEventListener('click', function (e) {
  if (!e.target || !e.target.closest || typeof window.gtag !== 'function') return;
  /* text_click is counted in assets/chat.js (with transport_type beacon), so it is not sent twice */
  if (e.target.closest('a[href^="sms:"]')) return;
  var a = e.target.closest('a[href*="planenroll.com"]');
  if (!a) return;
  var place = a.closest('.hb-next') ? 'post next step' : a.closest('.hb-life') ? 'life block' : a.closest('.hb-book') ? 'product block' : a.closest('.cta-strip') ? 'page strip' : a.closest('.band') ? 'bottom band' : a.closest('.sticky-call') ? 'bottom bar' : a.closest('nav.menu') ? 'menu' : a.closest('header') ? 'header' :
    a.closest('.page-hero,.hx') ? 'hero' : a.closest('#funnel') ? 'funnel' : 'page';
  try { window.gtag('event', 'book_click', { page: location.pathname, place: place, line: document.body.getAttribute('data-line') || '' }); } catch (x) {}
}, true);

/* Cards lean toward the pointer and catch the light. Desktop pointers only; off when the visitor prefers reduced motion. */
(function () {
  if (!window.matchMedia || !matchMedia('(hover:hover) and (pointer:fine)').matches || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var SEL = '.card,.rel-card,.bundle-card,.calc-tile,.quote-card,.hb-book,.fe-box,.stat,.step,.cta-strip';
  var cur = null;
  function leave(el) {
    el.classList.remove('hb-tilting');
    el.style.transform = '';
    setTimeout(function () { if (cur !== el) el.style.transition = ''; }, 260);
  }
  document.addEventListener('pointermove', function (e) {
    var el = e.target && e.target.closest ? e.target.closest(SEL) : null;
    if (cur && cur !== el) { leave(cur); cur = null; }
    if (!el) return;
    if (cur !== el) {
      cur = el;
      if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
      if (!el.querySelector(':scope > .hb-glare')) { var g = document.createElement('i'); g.className = 'hb-glare'; g.setAttribute('aria-hidden', 'true'); el.appendChild(g); }
      el.style.transition = 'transform .16s ease-out';
      el.classList.add('hb-tilting');
    }
    var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
    var max = r.width > 560 ? 3 : 6;
    el.style.transform = 'perspective(1000px) rotateX(' + ((.5 - y) * max).toFixed(2) + 'deg) rotateY(' + ((x - .5) * max).toFixed(2) + 'deg) translateY(-4px)';
    el.style.setProperty('--gx', (x * 100).toFixed(1) + '%'); el.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
  }, { passive: true });
  document.addEventListener('pointerleave', function () { if (cur) { leave(cur); cur = null; } });
})();

(function () {
  var hdr = document.querySelector('header');
  var nav = hdr && hdr.querySelector('nav.menu');
  var btn = hdr && hdr.querySelector('.hb-burger');
  if (!nav || !btn) return;

  var cta = document.createElement('div');
  cta.className = 'hb-menu-cta';
  cta.innerHTML =
    '<a class="hb-mc-book" href="https://www.planenroll.com/?purl=Luay-Sadqi" target="_blank" rel="noopener">Schedule an appointment</a>' +
    '<a class="hb-mc-call" href="tel:+15713540146">Call</a>' +
    '<a class="hb-mc-how" href="/schedule-an-appointment">How scheduling works</a>';
  nav.appendChild(cta);

  /* one-line description under each top-level item (shown in the phone menu only) */
  var SUBS = { About: 'Who we are', Health: 'ACA, ICHRA, group and self-employed', Medicare: 'Advantage, Medigap and Part D',
               Life: 'Term, whole life and final expense', Retirement: 'Annuities and rollovers', Blog: 'Guides in plain English',
               Contact: 'Call or send a message' };
  var kids = nav.children;
  for (var k = 0; k < kids.length; k++) {
    var top = kids[k].tagName === 'A' ? kids[k] : (kids[k].classList.contains('has-dd') ? kids[k].firstElementChild : null);
    if (!top) continue;
    var label = (top.textContent || '').replace(/\s+/g, ' ').trim();
    if (!SUBS[label]) continue;
    var wrap = document.createElement('span'); wrap.className = 'hb-ml';
    var b = document.createElement('b'); b.textContent = label;
    var sm = document.createElement('small'); sm.textContent = SUBS[label];
    wrap.appendChild(b); wrap.appendChild(sm);
    top.textContent = ''; top.appendChild(wrap);
  }

  function isOpen() { return document.body.classList.contains('hb-menu-open'); }
  function fit() { nav.style.height = Math.max(260, window.innerHeight - hdr.getBoundingClientRect().bottom) + 'px'; }
  function set(open) {
    document.body.classList.toggle('hb-menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open) { fit(); nav.scrollTop = 0; }
    else {
      nav.style.height = '';
      var groups = nav.querySelectorAll('.has-dd.open');
      for (var i = 0; i < groups.length; i++) {
        groups[i].classList.remove('open');
        if (groups[i].firstElementChild) groups[i].firstElementChild.setAttribute('aria-expanded', 'false');
      }
    }
  }

  btn.addEventListener('click', function () { set(!isOpen()); });
  nav.addEventListener('click', function (e) {
    if (!isOpen()) return;
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var group = a.parentElement;
    if (group && group.classList.contains('has-dd') && a === group.firstElementChild) {
      e.preventDefault();
      var open = !group.classList.contains('open');
      group.classList.toggle('open', open);
      a.setAttribute('aria-expanded', open ? 'true' : 'false');
    } else {
      set(false);
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) { set(false); btn.focus(); }
  });
  window.addEventListener('resize', function () {
    if (!isOpen()) return;
    if (window.innerWidth > 1100) set(false); else fit();
  });
})();
