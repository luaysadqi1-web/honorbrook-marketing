/* Honorbrook homepage (Onyx): coverage funnel UI + page motion. Needs hb-funnel-core.js (window.HB). */
(function () {
  var root = document.getElementById('funnel'); if (!root || !window.HB) return;
  var S, RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var STAGES = [
    { l: "I'm turning 65 or on Medicare", d: 'Medicare Advantage, dental and vision, hospital plans, Medigap', ic: 'advantage', t: ['advantage', 'dvh', 'hospital', 'cancer', 'medigap', 'partd'] },
    { l: 'I need health insurance, under 65', d: 'Individual, family, self-employed or lost coverage', ic: 'health', t: ['health', 'hospital', 'cancer', 'disability'] },
    { l: 'I want to protect my family', d: 'Life insurance, final expense and mortgage protection', ic: 'life', t: ['life', 'final', 'mortgage', 'cancer', 'disability'] },
    { l: "I'm planning for retirement", d: 'Annuities, rollovers, long-term care', ic: 'annuity', t: ['annuity', 'life', 'final', 'ltc', 'homecare'] },
    { l: 'I own a business', d: 'Group health, ICHRA and employee benefits', ic: 'biz', t: ['biz', 'health', 'disability'] }
  ];
  function reset() { S = { stage: null, queue: [], cur: 0, ans: {}, sel: [], skipped: false, pw: 0 }; }
  function phase(n) { return '<div class="fx-phase">' + ['Situation', 'Coverage', 'Contact'].map(function (l, i) { return '<div class="' + (i === n ? 'on' : i < n ? 'dn' : '') + '"><i></i><span>0' + (i + 1) + '</span> ' + l + '</div>'; }).join('') + '</div>'; }
  function note() { return '<p class="fx-fn">' + HB.FINE + '</p>'; }
  function scroll() { var y = root.getBoundingClientRect().top; if (y < 0 || y > 220) root.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' }); }
  function stage() {
    reset();
    root.innerHTML = phase(0) + '<h2>What brings you here today?</h2><p class="fx-sub">Choose the one that fits best. It takes about two minutes.</p><div class="fx-stack">' + STAGES.map(function (s, i) { return '<button class="fx-card" data-i="' + i + '"><span class="fx-ic">' + HB.icon[s.ic] + '</span><span class="fx-tx"><b>' + s.l + '</b><small>' + s.d + '</small></span><span class="fx-go">' + HB.icon.arrow + '</span></button>'; }).join('') + '</div><button class="fx-skip" id="fxnf">Not sure? Just have someone call me.</button>' + note();
    root.querySelectorAll('.fx-card').forEach(function (b) { b.onclick = function () { b.classList.add('on'); root.querySelector('.fx-stack').classList.add('lock'); setTimeout(function () { S.stage = STAGES[+b.dataset.i]; HB.track('funnel_stage', { stage: S.stage.l }); products(); }, RM ? 0 : 220); }; });
    root.querySelector('#fxnf').onclick = function () { S.queue = ['general']; S.ans.general = {}; S.skipped = true; contact(); };
  }
  function products() {
    var ps = S.stage.t.map(HB.byId);
    root.innerHTML = phase(0) + '<div class="fx-top"><button class="fx-back">' + HB.icon.back + 'Back</button></div><h2>What would you like help with?</h2><p class="fx-sub">Pick one or more. We review them together on one call.</p><div class="fx-stack">' + ps.map(function (p) { var on = S.sel.indexOf(p.id) > -1; return '<button class="fx-card' + (on ? ' on' : '') + '" data-id="' + p.id + '" aria-pressed="' + on + '"><span class="fx-ic">' + HB.icon[p.icon] + '</span><span class="fx-tx"><b>' + p.label + '</b><small>' + p.desc + '</small></span><span class="fx-bx">' + HB.icon.check + '</span></button>'; }).join('') + '</div><button class="fx-cta" id="fxc1" ' + (S.sel.length ? '' : 'disabled') + '><span>Continue' + (S.sel.length ? ' with ' + S.sel.length : '') + '</span>' + HB.icon.arrow + '</button>' + note();
    root.querySelectorAll('.fx-card').forEach(function (b) { b.onclick = function () { var k = S.sel.indexOf(b.dataset.id); if (k > -1) S.sel.splice(k, 1); else S.sel.push(b.dataset.id); products(); }; });
    root.querySelector('.fx-back').onclick = stage;
    root.querySelector('#fxc1').onclick = function () { if (!S.sel.length) return; S.queue = S.sel.slice(); S.ans = {}; S.queue.forEach(function (id) { S.ans[id] = {}; }); S.cur = 0; S.skipped = false; S.pw = 0; HB.track('funnel_products', { products: S.queue.join(',') }); ask(); scroll(); };
  }
  function cp() { var id = S.queue[S.cur]; return { p: HB.byId(id), a: S.ans[id] }; }
  function goBack() {
    var c = cp(); if (HB.back(c.p, c.a)) return ask();
    if (S.cur > 0) { S.cur--; var c2 = cp(); HB.back(c2.p, c2.a); return ask(); }
    products();
  }
  function ask() {
    var c = cp(), q = HB.nextQ(c.p, c.a);
    if (!q) { if (S.cur < S.queue.length - 1) { S.cur++; return ask(); } return contact(); }
    var g = HB.prog(c.p, c.a), nw = Math.round((g.n - 1) / (g.total - 1) * 100);
    root.innerHTML = phase(1) + '<div class="fx-top"><button class="fx-back">' + HB.icon.back + 'Back</button><span class="fx-count">' + c.p.label + (S.queue.length > 1 ? ' · ' + (S.cur + 1) + ' of ' + S.queue.length : '') + ' · ' + g.n + '/' + (g.total - 1) + '</span></div><div class="fx-bar"><i style="width:' + nw + '%;--from:' + S.pw + '%"></i></div><h2>' + q.q + '</h2>' + (q.multi ? '<p class="fx-hint">Choose all that apply.</p>' : '') + '<div class="fx-stack">' + q.o.map(function (o) { return '<button class="fx-opt" data-v="' + HB.esc(o) + '"><span>' + o + '</span><span class="fx-tick">' + HB.icon.check + '</span></button>'; }).join('') + '</div>' + (q.multi ? '<button class="fx-cta" id="fxmc"><span>Continue</span>' + HB.icon.arrow + '</button>' : '') + '<button class="fx-skip" id="fxsk">Skip the rest. Just call me.</button>' + note();
    S.pw = nw;
    root.querySelectorAll('.fx-opt').forEach(function (b) { b.onclick = function () { if (q.multi) { b.classList.toggle('on'); } else { b.classList.add('on'); root.querySelector('.fx-stack').classList.add('lock'); setTimeout(function () { HB.set(c.p, c.a, q.id, b.dataset.v); ask(); }, RM ? 0 : 240); } }; });
    var mc = root.querySelector('#fxmc'); if (mc) mc.onclick = function () { var v = [].map.call(root.querySelectorAll('.fx-opt.on'), function (x) { return x.dataset.v; }); HB.set(c.p, c.a, q.id, v.join(', ') || 'No preference'); ask(); };
    root.querySelector('.fx-back').onclick = goBack;
    root.querySelector('#fxsk').onclick = function () { S.skipped = true; contact(); };
  }
  function contact() {
    root.innerHTML = phase(2) + '<div class="fx-top"><button class="fx-back">' + HB.icon.back + 'Back</button></div><h2>Where should we reach you?</h2><p class="fx-sub">A licensed Honorbrook agent will call within one business day. We do not sell your data.</p>' + HB.contactHTML('Send my request');
    root.querySelector('.fx-back').onclick = function () { if (S.skipped || S.queue[0] === 'general') { S.skipped = false; stage(); } else { S.cur = S.queue.length - 1; var c = cp(); HB.back(c.p, c.a); ask(); } };
    HB.bindContact(root.querySelector('form'), function () { return { products: S.queue, answers: S.ans, source: 'homepage-funnel' }; }, done);
    scroll();
  }
  function done() {
    root.innerHTML = '<div class="fx-done"><div class="fx-big" id="fxchk">' + HB.icon.check + '</div><h2>Thank you. We have your request.</h2><p>A licensed Honorbrook agent will call you within one business day. Want to get started now? Schedule your appointment online, or call us.</p><a class="fx-callbig" href="https://www.planenroll.com/?purl=Luay-Sadqi" target="_blank" rel="noopener">Schedule an appointment</a><p class="fx-meet">' + HB.esc(HB.meetHint(S.queue)) + '</p><a class="fx-how" href="/schedule-an-appointment">How scheduling works</a><br><a class="fx-callbig" href="tel:' + HB.TEL + '">' + HB.icon.phone + HB.PHONE + '</a>' + (S.queue[0] === 'general' ? '' : '<p class="fx-more">While you wait, here is more about what you chose:</p>' + HB.doneLinks(S.queue, S.ans)) + '</div>';
    scroll(); burst(document.getElementById('fxchk'));
  }
  function burst(host) {
    if (RM || !host) return; var cols = ['#ffffff', '#dfe2e7', '#aab0ba', '#7d838e', '#f4f5f7'];
    for (var i = 0; i < 30; i++) {
      var p = document.createElement('i'); p.className = 'fx-cf'; var a = Math.random() * Math.PI * 2, d = 80 + Math.random() * 130;
      p.style.setProperty('--x', Math.cos(a) * d + 'px'); p.style.setProperty('--y', (Math.sin(a) * d - 34) + 'px'); p.style.setProperty('--r', (Math.random() * 600 - 300) + 'deg');
      p.style.background = cols[i % cols.length]; p.style.animationDelay = (Math.random() * .14) + 's'; host.appendChild(p);
    }
    setTimeout(function () { [].forEach.call(host.querySelectorAll('.fx-cf'), function (x) { x.remove(); }); }, 1700);
  }
  stage(); HB.track('funnel_view');
  new MutationObserver(function () { root.classList.remove('swap'); void root.offsetWidth; root.classList.add('swap'); }).observe(root, { childList: true });

  /* ---- page motion ---- */
  document.documentElement.classList.add('js');
  var card = root.parentNode;
  card.addEventListener('pointermove', function (e) { var r = card.getBoundingClientRect(); card.style.setProperty('--mx', (e.clientX - r.left) + 'px'); card.style.setProperty('--my', (e.clientY - r.top) + 'px'); });
  var els = [].slice.call(document.querySelectorAll('body.home h2.section-title,body.home p.section-sub,body.home .card,body.home .bundle-card,body.home .step,body.home .quote-card,body.home .ab-grid>*,body.home .mk-copy,body.home .calc-tile,body.home .fe-box'));
  els.forEach(function (e, i) { e.classList.add('ox-rv'); e.style.setProperty('--d', ((i % 4) * 80) + 'ms'); });
  function countUp(box) {
    [].forEach.call(box.querySelectorAll('[data-count]'), function (b) {
      var to = parseFloat(b.dataset.count), dec = +(b.dataset.dec || 0), suf = b.dataset.suf || '', t0 = null, dur = 1500;
      if (RM) { b.textContent = to.toFixed(dec) + suf; return; }
      function f(t) { if (!t0) t0 = t; var k = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - k, 3); b.textContent = (to * e).toFixed(dec) + suf; if (k < 1) requestAnimationFrame(f); else b.textContent = to.toFixed(dec) + suf; }
      requestAnimationFrame(f);
    });
  }
  var hc = document.getElementById('hbcard'), hx = document.querySelector('.hx');
  /* idle float needs registered custom properties so the angles animate smoothly */
  if (hc && !RM && window.CSS && CSS.registerProperty) hc.classList.add('float');
  if (hc && hx && !RM && matchMedia('(hover:hover)').matches) {
    hx.addEventListener('pointermove', function (e) {
      hc.classList.add('live');
      var r = hc.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      var cx = Math.max(-1, Math.min(2, x)), cy = Math.max(-1, Math.min(2, y));
      hc.style.setProperty('--ry', ((cx - .5) * 14 - 4).toFixed(2) + 'deg'); hc.style.setProperty('--rx', ((.5 - cy) * 10 + 3).toFixed(2) + 'deg');
      hc.style.setProperty('--sx', (30 + cx * 40) + '%'); hc.style.setProperty('--sy', (20 + cy * 40) + '%');
    });
    hx.addEventListener('pointerleave', function () { ['--rx', '--ry', '--sx', '--sy'].forEach(function (k) { hc.style.removeProperty(k); }); hc.classList.remove('live'); });
  }
  var mt = document.querySelector('.hx-metrics'), map = document.querySelector('.mk-map');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .1 });
    els.forEach(function (e) { io.observe(e); });
    if (map) io.observe(map);
    if (mt) { var so = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { countUp(x.target); so.unobserve(x.target); } }); }, { threshold: .4 }); so.observe(mt); }
  } else { els.forEach(function (e) { e.classList.add('in'); }); if (map) map.classList.add('in'); }
  /* guarantee: nothing stays hidden if the observer never fires */
  setTimeout(function () { [].forEach.call(document.querySelectorAll('.ox-rv:not(.in)'), function (e) { var r = e.getBoundingClientRect(); if (r.top < window.innerHeight * 1.5) e.classList.add('in'); }); }, 2600);
})();
