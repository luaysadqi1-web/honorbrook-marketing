/* Honorbrook "Find your area" search: ZIP, city, county or state. Loads its index only when first opened.
   No cookies, no third-party requests. Sends only the result type (never the typed text) to analytics. */
(function () {
  'use strict';
  var INDEX = null, LOADING = null;
  var OTHER = {AL:0,AK:'Alaska',AZ:'Arizona',AR:'Arkansas',CA:'California',CO:'Colorado',CT:'Connecticut',DE:'Delaware',DC:'District of Columbia',FL:'Florida',HI:'Hawaii',ID:'Idaho',IL:'Illinois',IA:'Iowa',KS:'Kansas',KY:'Kentucky',ME:'Maine',MA:'Massachusetts',MN:'Minnesota',MS:'Mississippi',MO:'Missouri',MT:'Montana',NE:'Nebraska',NV:'Nevada',NH:'New Hampshire',NJ:'New Jersey',NM:'New Mexico',NY:'New York',ND:'North Dakota',OH:'Ohio',OK:'Oklahoma',OR:'Oregon',PA:'Pennsylvania',RI:'Rhode Island',SD:'South Dakota',TN:'Tennessee',UT:'Utah',VT:'Vermont',WA:'Washington',WI:'Wisconsin',WY:'Wyoming'};

  function load() {
    if (INDEX) return Promise.resolve(INDEX);
    if (!LOADING) {
      LOADING = fetch('/assets/find-index.json').then(function (r) { return r.json(); }).then(function (j) { INDEX = j; return j; });
    }
    return LOADING;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function norm(s) { return s.toLowerCase().replace(/\bsaint\b/g, 'st').replace(/[.’']/g, '').replace(/\s+/g, ' ').trim(); }
  function track(type) { try { if (window.gtag) gtag('event', 'find_area_search', { result_type: type }); } catch (e) {} }

  function stateByQuery(q) {
    var n = norm(q);
    for (var i = 0; i < INDEX.s.length; i++) {
      var s = INDEX.s[i];
      if (norm(s[0]) === n || s[1].toLowerCase() === n) return s;
    }
    return null;
  }
  function otherState(q) {
    var n = norm(q), up = q.trim().toUpperCase();
    if (OTHER[up] && up !== 'AL') return OTHER[up];
    for (var k in OTHER) { if (OTHER[k] && norm(OTHER[k]) === n) return OTHER[k]; }
    return null;
  }
  function countyLine(c) { return '<a href="/' + c[2] + '"><strong>' + esc(c[0]) + '</strong>, ' + c[1] + '</a>'; }

  function search(q) {
    q = q.trim();
    var out = { html: '', type: 'none' };
    if (!q) return { html: '<p class="fd-hint">Type a ZIP code, city, county or state.</p>', type: 'empty' };
    var cta = '<p class="fd-yes">Yes, we can help here. We work by phone or video, free to you. <a href="tel:+15713540146">Call (571) 354-0146</a> or <a href="/#contact">request a callback</a>.</p>';
    if (/^\d{5}$/.test(q)) {
      var ci = INDEX.z[q];
      if (ci === undefined) return { html: '<p class="fd-no">We did not find ZIP ' + esc(q) + ' in the 11 states we serve. If you are moving to one of them, search by county or state, or <a href="tel:+15713540146">call (571) 354-0146</a>.</p>', type: 'zip-miss' };
      var c = INDEX.c[ci];
      return { html: cta + '<ul class="fd-list"><li>ZIP ' + esc(q) + ' is mostly in ' + countyLine(c) + '</li></ul>', type: 'zip' };
    }
    var st = stateByQuery(q);
    if (st) {
      var u = '/' + st[2];
      return { html: cta + '<ul class="fd-list"><li><a href="' + u + '-medicare-insurance"><strong>' + esc(st[0]) + '</strong> Medicare help</a></li><li><a href="' + u + '-aca-health-insurance">' + esc(st[0]) + ' ACA health insurance</a></li><li><a href="' + u + '-counties">All ' + esc(st[0]) + ' counties</a></li></ul>', type: 'state' };
    }
    var os = otherState(q);
    var osMsg = os ? '<p class="fd-no">Honorbrook is not licensed in ' + esc(os) + ' yet, so we cannot help with plans there. We serve Virginia, Maryland, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan, Indiana and West Virginia. <a href="tel:+15713540146">Call (571) 354-0146</a> with questions.</p>' : '';
    var n = norm(q), stFilter = null, m = n.match(/^(.*?)[, ]+([a-z]{2})$/);
    if (m) { for (var i = 0; i < INDEX.s.length; i++) { if (INDEX.s[i][1].toLowerCase() === m[2]) { stFilter = INDEX.s[i][1]; n = m[1].trim(); } } }
    n = n.replace(/\s+(county|parish)$/, '');
    var hits = [], seen = {};
    function add(score, html, key) { if (!seen[key]) { seen[key] = 1; hits.push([score, html]); } }
    INDEX.c.forEach(function (c, i) {
      if (stFilter && c[1] !== stFilter) return;
      var cn = norm(c[0]).replace(/\s+(county|parish)$/, '').replace(/^city of /, '');
      var s = cn === n ? 0 : cn.indexOf(n) === 0 ? 1 : cn.indexOf(n) > 0 ? 3 : -1;
      if (s >= 0) add(s, '<li>' + countyLine(c) + ' <span class="fd-tag">county</span></li>', 'c' + i);
    });
    INDEX.p.forEach(function (p) {
      var c = INDEX.c[p[1]];
      if (stFilter && c[1] !== stFilter) return;
      var pn = norm(p[0]);
      var s = pn === n ? 1 : pn.indexOf(n) === 0 ? 2 : pn.indexOf(n) > 0 ? 4 : -1;
      if (s >= 0) add(s, '<li><strong>' + esc(p[0]) + '</strong>, ' + c[1] + ' &mdash; in <a href="/' + c[2] + '">' + esc(c[0]) + '</a> <span class="fd-tag">city</span></li>', 'p' + p[0] + p[1]);
    });
    if (!hits.length && os) return { html: osMsg, type: 'other-state' };
    if (!hits.length) return { html: '<p class="fd-no">We did not find that. Try a ZIP code, a county or a state. We serve 11 states: VA, MD, NC, SC, GA, AL, LA, TX, MI, IN and WV.</p>', type: 'miss' };
    hits.sort(function (a, b) { return a[0] - b[0]; });
    var shown = hits.slice(0, 8).map(function (h) { return h[1]; }).join('');
    return { html: (os ? osMsg + '<p class="fd-hint">These matches are in the 11 states we serve:</p>' : '') + cta + '<ul class="fd-list">' + shown + '</ul>' + (hits.length > 8 ? '<p class="fd-hint">Showing 8 of ' + hits.length + ' matches. Add a state, like &ldquo;Franklin, VA&rdquo;, to narrow it.</p>' : ''), type: 'place' };
  }

  function build(root, inline) {
    root.innerHTML = '<label class="fd-label" for="fdInput">Enter your ZIP code, city, county or state</label>' +
      '<div class="fd-row"><input id="fdInput" class="fd-input" type="search" inputmode="search" autocomplete="off" placeholder="Example: 22182, Wake County, or Texas"><button type="button" class="fd-go">Search</button></div>' +
      '<div class="fd-out" aria-live="polite"></div>';
    var input = root.querySelector('.fd-input'), out = root.querySelector('.fd-out'), t;
    function run() { load().then(function () { var r = search(input.value); out.innerHTML = r.html; if (input.value.trim()) track(r.type); }); }
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(run, 160); });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); run(); } });
    root.querySelector('.fd-go').addEventListener('click', run);
    load();
    return input;
  }

  var dlg = null;
  function openDialog() {
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'findDlg'; dlg.className = 'fd-dlg';
      dlg.setAttribute('aria-labelledby', 'fdTitle');
      dlg.innerHTML = '<div class="fd-head"><h2 id="fdTitle">Can we help in your area?</h2><button type="button" class="fd-x" aria-label="Close">&times;</button></div><div class="fd-body"></div><p class="fd-foot"><a href="/find-your-area">Browse every state, county and city &rarr;</a></p>';
      document.body.appendChild(dlg);
      dlg.querySelector('.fd-x').addEventListener('click', function () { dlg.close(); });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      build(dlg.querySelector('.fd-body'));
    }
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    var i = dlg.querySelector('.fd-input'); if (i) i.focus();
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-find]');
    if (b) { e.preventDefault(); openDialog(); }
  });
  var inline = document.getElementById('findInline');
  if (inline) build(inline, true);
})();
