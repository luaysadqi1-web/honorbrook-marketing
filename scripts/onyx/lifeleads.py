"""Honorbrook Onyx: life-lead page upgrades (Nov 24-25, 2026). Owner: "focus on generating final expense iul veteran life
insurance leads mortgage protection and kids accounts".

The page text changes live in scripts/onyx/data/patches/<group>.json as exact-text replacements on the final built HTML. Each
group was written by one agent and re-checked by an independent agent (every source re-fetched, owner rules, FAQ schema matching the
visible FAQ, HTML balance). Groups: final expense page and hidden-costs post; IUL, high-net-worth and whole life; veterans;
mortgage protection; children's page, single-premium annuities and the 5 kids posts.
apply() runs after seo.apply(), so the "old" text matches what those passes produced; the build stops if any "old" text is not
found exactly once (the page changed and the patch needs a fresh look).
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATCHES = os.path.join(HERE, 'data', 'patches')


def apply(out):
    done = {}
    for f in sorted(glob.glob(os.path.join(PATCHES, '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for pg in d['pages']:
            p = os.path.join(out, pg['page'])
            s = open(p, encoding='utf-8').read()
            for r in pg['replacements']:
                n = s.count(r['old']); want = r.get('count', 1)   # "count": the text is on the page that many times (visible FAQ plus FAQ schema)
                if n != want:
                    raise SystemExit('lifeleads: %s: expected the text %d time(s), found %d: %s' % (pg['page'], want, n, r['old'][:80]))
                s = s.replace(r['old'], r['new'])
            open(p, 'w', encoding='utf-8').write(s)
            done[pg['page']] = done.get(pg['page'], 0) + len(pg['replacements'])
    return done


# ---------------------------------------------------------------------------------------------------------------------
# Funnel pass (Nov 25, 2026): the path from a life page or post to a lead the owner can call and book.
# - Quote forms ask 1-3 qualifying questions per line, plus the best time to call. Options marked data-hot make the email
#   subject start with "HOT lead:" (assets/chat.js), so he knows whom to call first. No health details are asked.
# - The mortgage protection page gets a quote form (it had none).
# - Life and annuity forms end on /thank-you-life, which says which meeting type to pick on PlanEnroll.
# - Life and annuity posts: the Medicare enrollment banner becomes a booking line for the right meeting type; state names in
#   the "rules vary by state" list go to the state life pages; "/#contact" buttons go to the product page's quote form.
# - Tracking: every booking, text, call and lead event carries the line (final_expense, iul, veterans, mortgage, kids, life,
#   annuity); the duplicate book_call_click event is removed.
import re

BOOK = 'https://www.planenroll.com/?purl=Luay-Sadqi'
LINE = {'final-expense-life-insurance': 'final_expense', 'indexed-universal-life': 'iul', 'high-net-worth-life-insurance': 'iul', 'iul-policy-review': 'iul',
        'veterans-life-insurance': 'veterans', 'mortgage-protection-insurance': 'mortgage', 'childrens-life-insurance': 'kids',
        'life-insurance': 'life', 'term-life-insurance': 'life', 'whole-life-insurance': 'life', 'guaranteed-universal-life': 'life',
        'annuities': 'annuity', 'single-premium-annuities': 'annuity', 'retirement-rollover-annuity': 'annuity'}
HAS_FORM = ['final-expense-life-insurance', 'life-insurance', 'term-life-insurance', 'whole-life-insurance', 'indexed-universal-life', 'guaranteed-universal-life',
            'annuities', 'veterans-life-insurance', 'high-net-worth-life-insurance', 'childrens-life-insurance', 'single-premium-annuities', 'mortgage-protection-insurance',
            'iul-policy-review']
QUOTE_FOR = {'retirement-rollover-annuity': 'annuities'}   # pages without a form send to the closest one


def _sel(i, label, name, opts, blank=True):
    """One select field. opts: 'text' or ('text', True) for an option that marks the lead as hot.
    blank: the field starts on an empty "Choose one", so a question the visitor never touched is not sent as an answer
    (and can never mark the lead HOT). chat.js leaves empty answers out of the email and the lead record."""
    o = ('<option value="">Choose one</option>' if blank else '') + ''.join('<option%s>%s</option>' % (' data-hot' if isinstance(x, tuple) and x[1] else '', x[0] if isinstance(x, tuple) else x) for x in opts)
    return '<div><label for="qx-%s">%s</label>\n        <select id="qx-%s" name="%s">%s</select></div>' % (i, label, i, name, o)


def _rows(fields):
    out = []
    for k in range(0, len(fields), 2):
        pair = fields[k:k + 2]
        out.append('      <div class="row2">\n        ' + '\n        '.join(pair) + '\n      </div>' if len(pair) == 2 else '      ' + pair[0])
    return '\n'.join(out) + '\n'


BEST = lambda: _sel('best', 'Best time to call', 'Best time to call', ['Anytime', 'Morning', 'Afternoon', 'Evening'], blank=False)
EXTRA = {
    'final-expense-life-insurance': lambda: [
        _sel('who', 'Who is the coverage for?', 'Coverage for', ['Myself', 'My spouse', 'A parent or relative']),
        _sel('tob', 'Tobacco in the last 12 months?', 'Tobacco', ['No', 'Yes']),
        _sel('amt', 'Coverage amount in mind', 'Coverage amount', ['Not sure yet', ('$5,000', True), ('$10,000', True), ('$15,000', True), ('$20,000', True), ('$25,000 or more', True)]),
        BEST()],
    'indexed-universal-life': lambda: [
        _sel('need', 'What do you need?', 'Need', ['Compare options before buying', ('Review an IUL I already own', True), ('A retirement income question', True), 'Estate or business planning']),
        BEST()],
    'high-net-worth-life-insurance': lambda: [
        _sel('need', 'What do you need?', 'Need', ['Compare options before buying', ('Review a policy I already own', True), ('Estate or business planning', True), 'A retirement income question']),
        BEST()],
    'iul-policy-review': lambda: [
        _sel('need', 'What do you need?', 'Need', [('Review an IUL I already own', True), ('A retirement income question', True), 'Compare options before buying', 'Estate or business planning']),
        BEST()],
    'veterans-life-insurance': lambda: [
        _sel('sep', 'When did you leave the service?', 'Separation', [('Less than 120 days ago', True), ('120 to 240 days ago', True), '240 days to 1 year and 120 days ago', 'Longer ago', 'Other or not sure']),
        _sel('cov', 'Coverage you have now', 'Current coverage', ['VGLI', 'VALife', 'SGLI', 'S-DVI', 'None', 'Not sure']),
        BEST()],
    'mortgage-protection-insurance': lambda: [
        _sel('home', 'Where are you with the home?', 'Home status', [('Buying or closing soon', True), ('Closed in the last 12 months', True), ('Refinancing', True), 'Owned it longer than a year']),
        BEST()],
    'childrens-life-insurance': lambda: [
        _sel('who', 'Who is the coverage for?', 'Coverage for', ['My child', 'My grandchild', 'A child rider on my own policy', 'Not sure']),
        _sel('cage', 'Child&rsquo;s age', 'Child age', ['Under 1', '1 to 5', '6 to 12', '13 to 17']),
        BEST()],
}
DEFAULT_EXTRA = lambda: [BEST()]
WHO_NOTE = '      <p class="sub" style="margin-top:10px">If the coverage is for a parent or relative, that person takes part in the application and signs it.</p>\n'

READY = {'final_expense': 'the age of the person to be covered, tobacco use, the amount you have in mind and who it is for',
         'iul': 'your latest annual statement or illustration, if you own a policy now',
         'veterans': 'your VGLI or VALife letter, if you have one, and your separation date',
         'mortgage': 'the loan balance, the years left and your closing date',
         'kids': 'the child&rsquo;s age and who will own and pay for the policy',
         'life': 'your age, state, tobacco use and any coverage you have now',
         'annuity': 'a recent statement for the account you are thinking of using'}


def _mortgage_form(out):
    """A quote form on the mortgage protection page, cloned from the term life form."""
    p = os.path.join(out, 'mortgage-protection-insurance.html'); s = open(p, encoding='utf-8').read()
    if 'id="quote"' in s: return False
    t = open(os.path.join(out, 'term-life-insurance.html'), encoding='utf-8').read()
    a = t.index('<section id="quote"'); b = t.index('</section>', a) + len('</section>')
    blk = t[a:b]
    sub = re.search(r'name="_subject" value="([^"]*)"', blk).group(1); top = re.search(r'name="Topic" value="([^"]*)"', blk).group(1)
    blk = blk.replace(sub, 'Quote request: Mortgage protection insurance (Honorbrook website)', 1).replace('name="Topic" value="%s"' % top, 'name="Topic" value="Mortgage protection insurance"', 1)
    blk = re.sub(r'<h3>[^<]*</h3>', '<h3>Get a mortgage protection quote</h3>', blk, count=1)
    blk = re.sub(r'<p class="sub">[^<]*</p>', '<p class="sub">Tell us about the loan and we will compare coverage for it. We reply within one business day, by text if you prefer.</p>', blk, count=1)
    blk = re.sub(r'\b(id|for)="q\d+-', r'\1="qm-', blk)
    assert '<section class="faq">' in s
    s = s.replace('<section class="faq">', blk + '\n\n<section class="faq">', 1)
    hero = '<a class="btn-ghost" href="%s" target="_blank" rel="noopener">Get a quote</a>' % BOOK
    if hero in s: s = s.replace(hero, '<a class="btn-ghost" href="#quote">Get a quote</a>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return True


def _review_form(out):
    """A request form on the IUL policy review page, cloned from the IUL page's form."""
    p = os.path.join(out, 'iul-policy-review.html')
    if not os.path.exists(p): return False
    s = open(p, encoding='utf-8').read()
    if 'id="quote"' in s: return False
    t = open(os.path.join(out, 'indexed-universal-life.html'), encoding='utf-8').read()
    a = t.index('<section id="quote"'); b = t.index('</section>', a) + len('</section>')
    blk = t[a:b]
    sub = re.search(r'name="_subject" value="([^"]*)"', blk).group(1); top = re.search(r'name="Topic" value="([^"]*)"', blk).group(1)
    blk = blk.replace(sub, 'Quote request: IUL policy review (Honorbrook website)', 1).replace('name="Topic" value="%s"' % top, 'name="Topic" value="IUL policy review"', 1)
    blk = re.sub(r'<h3>[^<]*</h3>', '<h3>Ask for an IUL policy review</h3>', blk, count=1)
    blk = re.sub(r'<p class="sub">[^<]*</p>', '<p class="sub">Tell us how to reach you. We reply within one business day, by text if you prefer.</p>', blk, count=1)
    blk = re.sub(r'\b(id|for)="q\d+-', r'\1="qr-', blk)
    assert '<section class="faq">' in s
    open(p, 'w', encoding='utf-8').write(s.replace('<section class="faq">', blk + '\n\n<section class="faq">', 1))
    # the IUL page's "already own an IUL" button leads to the review page
    ip = os.path.join(out, 'indexed-universal-life.html'); t2 = re.sub(r'(<a[^>]*href=")#quote("[^>]*>[^<]*Already own an IUL[^<]*</a>)', r'\1/iul-policy-review\2', t, count=1)
    if t2 != t: open(ip, 'w', encoding='utf-8').write(t2)
    return True


def _forms(out):
    n = 0
    for slug in HAS_FORM:
        p = os.path.join(out, slug + '.html')
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        a = s.find('<section id="quote"')
        if a < 0: raise SystemExit('lifeleads: no quote form on ' + slug)
        b = s.index('</section>', a); blk = s[a:b]
        if 'data-line=' in blk: continue
        line = LINE[slug]
        fields = EXTRA.get(slug, DEFAULT_EXTRA)()
        extra = _rows(fields) + (WHO_NOTE if slug == 'final-expense-life-insurance' else '')
        if blk.count('<label class="consent">') != 1 or blk.count('<form action="https://formspree.io/f/') != 1: raise SystemExit('lifeleads: unexpected form markup on ' + slug)
        blk = blk.replace('<form action="https://formspree.io/f/', '<form data-line="%s" data-thanks="/thank-you-life?t=%s" action="https://formspree.io/f/' % (line, line), 1)
        blk = blk.replace('      <label class="consent">', extra + '      <label class="consent">', 1) if '      <label class="consent">' in blk else blk.replace('<label class="consent">', extra + '<label class="consent">', 1)
        if slug == 'childrens-life-insurance': blk = blk.replace('>Your age</label>', '>Your age (the person paying)</label>', 1)
        if slug == 'final-expense-life-insurance':   # the form is often filled in for a parent; ages below 50 are rare for this product
            blk = blk.replace('>Your age</label>', '>Age of the person to be covered</label>', 1)
            blk = blk.replace('<option>Under 40</option><option>40 to 49</option><option>50 to 59</option>', '<option>Under 50</option><option>50 to 59</option>', 1)
            if '<option>Under 50</option>' not in blk: raise SystemExit('lifeleads: final expense age options not found')
        s = s[:a] + blk + s[b:]
        open(p, 'w', encoding='utf-8').write(s); n += 1
    return n


def _thanks(out):
    """/thank-you-life: built from the thank-you page; names the meeting type and what to have ready."""
    t = open(os.path.join(out, 'thank-you.html'), encoding='utf-8').read()
    a = t.index('<section class="page-hero"'); b = t.index('<footer')
    ready = ''.join('      <li data-t="%s"><strong>%s:</strong> %s.</li>\n' % (k, {'final_expense': 'Final expense', 'iul': 'Indexed universal life', 'veterans': 'Veterans',
                    'mortgage': 'Mortgage protection', 'kids': 'Children&rsquo;s coverage', 'life': 'Life insurance', 'annuity': 'Annuities'}[k], v) for k, v in READY.items())
    main = '''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <h1>Thank <em>you</em></h1>
    <p class="lead">We received your request. Luay will call or text you within one business day.</p>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>Want a set time?</h2>
    <p>You can pick a time yourself. Booking opens Luay&rsquo;s page on PlanEnroll. When it asks what type of meeting you would like, choose <strong id="hbMeet">Life</strong>. The first open time is at least 24 hours ahead. To talk sooner, call or text. Our hours are Monday&ndash;Friday 8am&ndash;8pm ET and Saturday&ndash;Sunday 9am&ndash;2:30pm ET.</p>
    <p><a class="btn-primary" href="%s" target="_blank" rel="noopener">Schedule an appointment</a> &nbsp; <a class="btn-primary" href="tel:+13016158289">Call (301) 615-8289</a> &nbsp; <a class="btn-ghost" href="sms:+15713540146">Text (571) 354-0146</a></p>
    <h2>Have this ready</h2>
    <ul id="hbReady">
%s    </ul>
    <h2>While you wait</h2>
    <ul>
      <li><a href="/life-insurance">Life insurance options compared</a></li>
      <li><a href="/schedule-an-appointment">How scheduling works</a></li>
      <li><a href="/blog/">Read our guides</a></li>
    </ul>
  </div>
</article>

''' % (BOOK, ready)
    page = t[:a] + main + t[b:]
    # the life and annuity thank-you page carries the life disclaimer, not the Medicare one (Nov 25 review)
    lf = open(os.path.join(out, 'life-insurance.html'), encoding='utf-8').read()
    drx = re.compile(r'<div class="disclaimer">.*?</div>', re.S)
    life_disc = drx.search(lf[lf.index('<footer'):]).group(0)
    if 'MEDICARE' in life_disc or 'Medicare' in life_disc: raise SystemExit('lifeleads: life disclaimer not found')
    fi = page.index('<footer'); foot, k = drx.subn(lambda m: life_disc, page[fi:], count=1)
    if k != 1: raise SystemExit('lifeleads: thank-you footer disclaimer not found')
    page = page[:fi] + foot
    page = re.sub(r'<title>.*?</title>', '<title>Thank You | Honorbrook Insurance</title>', page, count=1, flags=re.S)
    page = page.replace('honorbrook-insurance.com/thank-you"', 'honorbrook-insurance.com/thank-you-life"')
    page = re.sub(r'<meta name="robots" content="index, follow">\s*', '', page)
    if 'noindex' not in page: raise SystemExit('lifeleads: thank-you-life must be noindex')
    page = re.sub(r'<body([^>]*)>', lambda m: '<body%s data-line="life">' % m.group(1), page, count=1)
    open(os.path.join(out, 'thank-you-life.html'), 'w', encoding='utf-8').write(page)


CHAT_PATCH = [
    # every extra form field reaches the lead connector, with the best time to call
    ("best:'',interests:fd0.getAll('Interests').join(', ')||fd0.get('Topic')||'',answers:fd0.get('Message')||'',",
     "best:fd0.get('Best time to call')||'',interests:fd0.getAll('Interests').join(', ')||fd0.get('Topic')||'',answers:hbAnswers(f,fd0),"),
    # life and annuity forms end on their own thank-you page
    ("else { location.href='/thank-you'; }", "else { location.href=f.getAttribute('data-thanks')||'/thank-you'; }"),
    # one booking event only (book_click in hb-nav.js); this listener doubled every count, so it is removed whole
    ("  document.addEventListener('click',function(e){\n    var a=e.target&&e.target.closest?e.target.closest('a[href*=\"planenroll.com\"]'):null;\n"
     "    if(a && typeof window.gtag==='function'){ try{ window.gtag('event','book_call_click',{page:location.pathname}); }catch(x){} }\n  },true);\n", ""),
    ("/* ---- Booking CTA: header button -> PlanEnroll, tracked as book_call_click ---- */",
     "/* ---- Booking CTA: header button -> PlanEnroll (clicks are counted as book_click in hb-nav.js) ---- */"),
    # a lead is counted when the form service accepts it (it was counted on every submit, even ones that failed); failures get their own event
    ("track(e.target.getAttribute('data-event')||'generate_lead',{form:(e.target.getAttribute('action')||'form')});",
     "if(!/formspree\\.io/.test(e.target.getAttribute('action')||'')){ track(e.target.getAttribute('data-event')||'generate_lead',{form:(e.target.getAttribute('action')||'form')}); }"),
    (".then(function(r){ if(r.ok){ if(f.hasAttribute('data-inline')){", ".then(function(r){ if(r.ok){ hbLead(f); if(f.hasAttribute('data-inline')){"),
    ("      .catch(function(){\n        if(btn){ btn.disabled=false; btn.textContent=label; }",
     "      .catch(function(){\n        try{ if(typeof window.gtag==='function'){ window.gtag('event','lead_error',{line:f.getAttribute('data-line')||'',page:location.pathname}); } }catch(x){}\n        if(btn){ btn.disabled=false; btn.textContent=label; }"),
    ("if(a){ track('phone_call_click',{phone:a.getAttribute('href').replace('tel:','')}); }",
     "if(a){ track('phone_call_click',{phone:a.getAttribute('href').replace('tel:',''),line:(document.body.getAttribute('data-line')||'')}); }"),
    ("    var btn=f.querySelector('button[type=submit]'), label=btn&&btn.textContent;",
     # the subject is rebuilt from the original on every submit, so a retry with a different answer is not left marked HOT
     "    var sj=f.querySelector('input[name=_subject]'); if(sj){ if(!sj.hasAttribute('data-base')){ sj.setAttribute('data-base',sj.value); } var sb=sj.getAttribute('data-base'); sj.value=f.querySelector('option[data-hot]:checked')?'HOT lead: '+sb.replace(/^Quote request: /,''):sb; }\n"
     "    var btn=f.querySelector('button[type=submit]'), label=btn&&btn.textContent;"),
    ("  function prep(){ document.querySelectorAll('form[action*=\"formspree.io\"]')",
     "  function hbLead(f){ try{ if(typeof window.gtag==='function'){ window.gtag('event',f.getAttribute('data-event')||'generate_lead',{form:f.getAttribute('action')||'form',line:f.getAttribute('data-line')||'',hot:!!f.querySelector('option[data-hot]:checked')}); } }catch(x){} }\n"
     "  function hbAnswers(f,fd){ var skip={Name:1,Phone:1,Email:1,ZIP:1,Consent:1,Topic:1,Interests:1,_subject:1,_gotcha:1,'Best time to call':1}, out=[]; fd.forEach(function(v,k){ if(!skip[k]&&v){ out.push(k+': '+v); } }); return out.join(' / '); }\n"
     "  function hbBody(f){ var d=new FormData(f); try{ if(d.has('Email')&&!d.get('Email')){ d['delete']('Email'); } }catch(x){} return d; }\n"
     "  function prep(){ document.querySelectorAll('form[action*=\"formspree.io\"]')"),
    ("var skip=/^\\/(thank-you|privacy-policy|terms|404|contact)$/.test(path);", "var skip=/^\\/(thank-you|thank-you-life|privacy-policy|terms|404|contact)$/.test(path);"),
]
CHAT_PATCH.append(
    # a copy of every lead goes to the second lead form, which emails the owner's Gmail. Not copied: newsletter sign-ups
    # (data-inline) and the reviews page's private feedback (data-nocopy). Sent once per form, so a retry after a failed
    # send does not email the same lead twice. An empty optional Email field is left out of both posts (hbBody).
    ("    fetch(f.action,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}})",
     "    if(!f.hasAttribute('data-inline')&&!f.hasAttribute('data-nocopy')&&!f._hbCopied){ f._hbCopied=true; try{ fetch('https://formspree.io/f/xljbopja',{method:'POST',body:hbBody(f),headers:{Accept:'application/json'},keepalive:true}).catch(function(){}); }catch(x){} }\n"
     "    fetch(f.action,{method:'POST',body:hbBody(f),headers:{Accept:'application/json'}})"))
CHAT_PATCH.append(
    # "Email me" needs an address: the visitor is asked for it before the form is sent (Nov 25 review)
    ("    if(!f.checkValidity()){",
     "    var how=f.querySelector('select[name=\"Contact preference\"]'), em=f.querySelector('input[name=\"Email\"]');\n"
     "    if(how&&em&&how.value==='Email me'&&!em.value.replace(/\\s/g,'')){ em.classList.add('hb-field-err'); msg(f,'Please add your email, or choose text or call.'); em.focus(); return; }\n"
     "    if(!f.checkValidity()){"))
CHAT_ADD = '''
/* ---- /thank-you-life: show the meeting type and the "have this ready" line for the form that was sent ---- */
(function(){
  if(!/^\\/thank-you-life/.test(location.pathname)) return;
  function go(){
    var t=(location.search.match(/[?&]t=([a-z_]+)/)||[])[1]||'', m=document.getElementById('hbMeet'), l=document.getElementById('hbReady');
    if(m&&t==='annuity'){ m.textContent='Annuities'; }
    if(l&&t){ var hit=l.querySelector('[data-t="'+t+'"]'); if(hit){ [].forEach.call(l.children,function(li){ if(li!==hit){ li.hidden=true; } }); } }
    if(t){ document.body.setAttribute('data-line',t); }
  }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',go); } else { go(); }
})();
'''


def _chat(out):
    p = os.path.join(out, 'assets', 'chat.js'); t = open(p, encoding='utf-8').read()
    for a, b in CHAT_PATCH:
        if t.count(a) != 1: raise SystemExit('lifeleads: chat.js text not found once: ' + a[:70])
        t = t.replace(a, b, 1)
    open(p, 'w', encoding='utf-8').write(t + CHAT_ADD)


LIFE_STATES_P = ('<p>Life insurance and annuity products, rates, riders and consumer protections differ by state, and a given product may not be available in every state. '
                 'Honorbrook is licensed in the 16 states and DC below; which products we can offer you depends on what carriers sell in your state. '
                 'Each state&rsquo;s insurance regulator can verify an agent&rsquo;s license and answer consumer questions.</p>')


def _posts(out, post_kind):
    n = {'banner': 0, 'states': 0, 'buttons': 0}
    banner = re.compile(r'<div class="aep-banner sans" id="aepBanner">.*?</div>', re.S)
    for f in glob.glob(os.path.join(out, 'blog', '*.html')):
        slug = os.path.basename(f)[:-5]
        if slug == 'index': continue
        page, kind = post_kind(slug)
        if page == 'aca-health-insurance':   # under-65 health posts: the button goes to the ACA page's own form
            s = open(f, encoding='utf-8').read()
            a, b = s.find('<article'), s.find('</article>')
            art, k = re.subn(r'(<a class="btn-primary sans" href=")/#contact(")', lambda m: m.group(1) + '/aca-health-insurance#quote' + m.group(2), s[a:b])
            if k: open(f, 'w', encoding='utf-8').write(s[:a] + art + s[b:]); n['buttons'] += k
            continue
        if kind not in ('Life', 'Annuities'): continue
        s = open(f, encoding='utf-8').read(); o = s
        what = 'life insurance' if kind == 'Life' else 'annuity'
        s, k = banner.subn('<div class="aep-banner sans"><strong>Want to talk through your %s options?</strong> Schedule a time and choose %s as the meeting type. '
                           '<a href="%s" target="_blank" rel="noopener">Schedule an appointment →</a></div>' % (what, kind, BOOK), s, count=1)
        n['banner'] += k
        i = s.find('<h2>Availability and rules vary by state</h2>')
        if kind == 'Life' and i >= 0:
            j = s.find('</ul>', i)
            if j > i and 'Life insurance and annuity products' not in s[i:j]:   # a life post that carries the health version of the paragraph
                blk, k = re.subn(r'<p>Health plans, premiums, enrollment rules and state programs differ by state.*?</p>', lambda m: LIFE_STATES_P, s[i:j], count=1, flags=re.S)
                if k: s = s[:i] + blk + s[j:]; j = s.find('</ul>', i)
            if j > i and 'Life insurance and annuity products' in s[i:j]:
                blk = re.sub(r'href="/([a-z-]+)-medicare-insurance"', lambda m: 'href="/%s-life-insurance"' % m.group(1) if os.path.exists(os.path.join(out, m.group(1) + '-life-insurance.html')) else m.group(0), s[i:j])
                if blk != s[i:j]: s = s[:i] + blk + s[j:]; n['states'] += 1
        if kind == 'Annuities' and i >= 0:   # the state life pages do not cover annuities, so the state names are plain text here
            j = s.find('</ul>', i)
            if j > i and 'Life insurance and annuity products' in s[i:j]:
                blk = re.sub(r'<a href="/[a-z-]+-medicare-insurance">([^<]+)</a>', r'\1', s[i:j])
                if blk != s[i:j]: s = s[:i] + blk + s[j:]; n['states'] += 1
        target = QUOTE_FOR.get(page, page)
        if target in HAS_FORM:
            a, b = s.find('<article'), s.find('</article>')
            art, k = re.subn(r'(<a class="btn-primary sans" href=")/#contact(")', lambda m: m.group(1) + '/%s#quote' % target + m.group(2), s[a:b])
            if k: s = s[:a] + art + s[b:]; n['buttons'] += k
            if target == 'life-insurance':   # the button opens the life insurance form, so it says so
                s = s.replace('href="/life-insurance#quote">Request my Retirement Income Review</a>', 'href="/life-insurance#quote">Request my life insurance review</a>')
                s = s.replace('<p class="sans">Request a no-obligation Retirement Income Review. ', '<p class="sans">Request a no-obligation life insurance review. ')
                s = s.replace('<h3>Want a second opinion before you move retirement money?</h3>', '<h3>Want a second opinion on your life insurance?</h3>')
        line = LINE.get(page)
        if line and 'data-line=' not in s[:s.find('>', s.find('<body')) + 1]:
            s = re.sub(r'<body([^>]*)>', lambda m: '<body%s data-line="%s">' % (m.group(1), line), s, count=1)
        if s != o: open(f, 'w', encoding='utf-8').write(s)
    return n


def _body_line(out):
    for slug, line in LINE.items():
        p = os.path.join(out, slug + '.html')
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        if 'data-line=' in s[:s.find('>', s.find('<body')) + 1]: continue
        open(p, 'w', encoding='utf-8').write(re.sub(r'<body([^>]*)>', lambda m: '<body%s data-line="%s">' % (m.group(1), line), s, count=1))
    for p in glob.glob(os.path.join(out, '*-life-insurance.html')):
        s = open(p, encoding='utf-8').read()
        if 'data-line=' in s[:s.find('>', s.find('<body')) + 1]: continue
        open(p, 'w', encoding='utf-8').write(re.sub(r'<body([^>]*)>', lambda m: '<body%s data-line="life">' % m.group(1), s, count=1))


def funnel(out, post_kind):
    made = _mortgage_form(out)
    _review_form(out)
    nf = _forms(out)
    _thanks(out)
    _chat(out)
    np_ = _posts(out, post_kind)
    # veterans page: no "free" wording (Virginia's military sales practices rule, 14VAC5-420, is strict about it)
    vp = os.path.join(out, 'veterans-life-insurance.html'); vs = open(vp, encoding='utf-8').read()
    open(vp, 'w', encoding='utf-8').write(vs.replace('<p>Free consultation · No obligation · No pressure</p>', '<p>No obligation · No pressure</p>', 1))
    _body_line(out)
    # reviews page: private feedback is not a lead (its own event, no Gmail lead copy)
    rp = os.path.join(out, 'reviews.html'); rs = open(rp, encoding='utf-8').read()
    fb = '<form class="fb-form sans" action="https://formspree.io/f/'
    if rs.count(fb) != 1: raise SystemExit('lifeleads: reviews feedback form not found')
    open(rp, 'w', encoding='utf-8').write(rs.replace(fb, '<form class="fb-form sans" data-event="feedback_submit" data-nocopy action="https://formspree.io/f/', 1))
    return {'mortgage form': made, 'forms upgraded': nf, 'posts': np_}


# ---------------------------------------------------------------------------------------------------------------------
# On-page forms (Nov 25, 2026): an on-page form wherever the page still sends
# visitors to the homepage form. Owner asked "is there anything else we should do to the site to ensure we are generating
# leads for all products". Measured on the build: 16 Medicare/health product pages, every county, town, state and ACA page,
# and the 17 state life pages had no form of their own; their "send a short form" links left the page.
# The form sits after the article (before the FAQ), so the article text that the repeated-text check measures is unchanged.
NEXT_PRODUCT = {
    'medicare-advantage': ('Medicare Advantage', 'medicare'), 'medicare-supplement-medigap': ('Medicare Supplement (Medigap)', 'medicare'),
    'medicare-part-d': ('Medicare Part D drug plans', 'medicare'), 'medicare-annual-enrollment-period': ('Medicare plan review', 'medicare'),
    'turning-65': ('Turning 65 / new to Medicare', 'medicare'), 'medicaid-dual-eligible': ('Medicare and Medicaid (dual eligible)', 'medicare'),
    'dental-vision-hearing-insurance': ('Dental, vision and hearing coverage', 'health'), 'hospital-indemnity-insurance': ('Hospital indemnity', 'health'),
    'cancer-critical-illness-insurance': ('Cancer and critical illness coverage', 'health'), 'short-term-home-care-insurance': ('Short-term and home care coverage', 'health'),
    'long-term-care-insurance': ('Long-term care insurance', 'health'), 'disability-insurance': ('Disability income insurance', 'health'),
    'aca-health-insurance': ('ACA health insurance', 'health'), 'self-employed-health-insurance': ('Self-employed health insurance', 'health'),
    'lost-health-coverage': ('Health coverage after losing a plan', 'health'), 'retirement-rollover-annuity': ('401(k) and IRA rollover', 'annuity'),
}
# headings that do not read well as "Ask about <name>" (and names with acronyms, which must not be lowercased)
HEADING = {'medicare-annual-enrollment-period': 'Ask for a Medicare plan review', 'turning-65': 'Ask about starting Medicare',
           'medicaid-dual-eligible': 'Ask about Medicare and Medicaid', 'aca-health-insurance': 'Ask about ACA health insurance',
           'retirement-rollover-annuity': 'Ask about a 401(k) or IRA rollover'}
HELP_OPTS = ['Medicare', 'Life insurance or final expense', 'Health insurance under 65', 'Annuities or retirement income', 'Something else']


def _form_shell(out):
    t = open(os.path.join(out, 'life-insurance.html'), encoding='utf-8').read()
    a = t.index('<section id="quote"'); b = t.index('</section>', a) + len('</section>')
    blk = t[a:b]
    # start from the plain form: drop the life questions the funnel pass added and the line attributes
    blk = re.sub(r'\s*<div class="row2">\s*<div><label for="qx-[^"]*".*?</div>\s*</div>', '', blk, flags=re.S)
    blk = re.sub(r'\s*<div><label for="qx-[^"]*".*?</select></div>', '', blk, flags=re.S)
    blk = re.sub(r' data-line="[^"]*" data-thanks="[^"]*"', '', blk)
    return blk


def _make_form(shell, subject, topic, h3, sub, line, thanks, extra, prefix):
    blk = shell
    blk = re.sub(r'(name="_subject" value=")[^"]*(")', lambda m: m.group(1) + 'Quote request: %s (Honorbrook website)' % subject + m.group(2), blk, count=1)
    blk = re.sub(r'(name="Topic" value=")[^"]*(")', lambda m: m.group(1) + topic + m.group(2), blk, count=1)
    blk = re.sub(r'<h3>[^<]*</h3>', '<h3>%s</h3>' % h3, blk, count=1)
    blk = re.sub(r'<p class="sub">[^<]*</p>', '<p class="sub">%s</p>' % sub, blk, count=1)
    blk = blk.replace('<form action="https://formspree.io/f/', '<form data-line="%s" data-thanks="%s" action="https://formspree.io/f/' % (line, thanks), 1)
    assert blk.count('      <label class="consent">') == 1
    blk = blk.replace('      <label class="consent">', _rows(extra) + '      <label class="consent">', 1)
    blk = re.sub(r'\b(id|for)="q[a-z0-9]*-', r'\1="%s-' % prefix, blk)   # one id prefix for the whole form
    # no age is preselected: finish_forms() starts the age field on an empty "Select" (Nov 25 review: a preselected
    # "60 to 69" or "Under 40" would be sent as an answer the visitor never gave)
    return blk


def _place(s, blk):
    if 'id="quote"' in s or '<section class="faq">' not in s: return s, False
    s = s.replace('<section class="faq">', blk + '\n\n<section class="faq">', 1)
    return s, True   # the page's "/#contact" links are pointed at this form by finish_forms()


def more_forms(out):
    shell = _form_shell(out)
    n = {'product': 0, 'area': 0, 'state life': 0}
    for slug, (name, line) in NEXT_PRODUCT.items():
        p = os.path.join(out, slug + '.html')
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        thanks = '/thank-you-life?t=annuity' if line == 'annuity' else '/thank-you'
        h3 = HEADING.get(slug) or 'Ask about %s' % (name if line == 'medicare' else name[0].lower() + name[1:])
        blk = _make_form(shell, name, name, h3, 'Tell us how to reach you. We reply within one business day, by text if you prefer.',
                         line, thanks, [BEST()], 'qn')
        s, ok = _place(s, blk)
        if ok: open(p, 'w', encoding='utf-8').write(s); n['product'] += 1
    import glob as _g
    for p in _g.glob(os.path.join(out, '*.html')):
        slug = os.path.basename(p)[:-5]
        area = slug.endswith(('-medicare-insurance', '-aca-health-insurance', '-medicare-advantage')) or slug == 'find-your-area'
        state_life = slug.endswith('-life-insurance') and os.path.exists(os.path.join(out, slug.replace('-life-insurance', '-medicare-insurance') + '.html'))
        if not (area or state_life): continue
        s = open(p, encoding='utf-8').read()
        if 'id="quote"' in s: continue
        m = re.search(r'<h1>(.*?)</h1>', s, re.S)
        place = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else slug
        if state_life:
            st = place.split(' in ')[-1].split(':')[0].strip() if ' in ' in place else slug
            blk = _make_form(shell, 'Life insurance in %s' % st, 'Life insurance (%s)' % st, 'Get a life insurance quote', 'Final expense, term or whole life. We reply within one business day, by text if you prefer.',
                             'life', '/thank-you-life?t=life', [_sel('need', 'What are you looking for?', 'Coverage type', ['Final expense', 'Term life', 'Whole life', 'Mortgage protection', 'Not sure yet']), BEST()], 'ql')
            kind = 'state life'
        else:
            # ACA state pages are for people under 65: their leads carry the health line; the question starts empty on every area form
            blk = _make_form(shell, place, place, 'Ask a question', 'Tell us how to reach you and what you need. We reply within one business day, by text if you prefer.',
                             'health' if slug.endswith('-aca-health-insurance') else 'area', '/thank-you', [_sel('help', 'What do you need help with?', 'Help with', HELP_OPTS), BEST()], 'qa')
            kind = 'area'
        s, ok = _place(s, blk)
        if ok: open(p, 'w', encoding='utf-8').write(s); n[kind] += 1
    return n


# Calculators and employer pages (Nov 25, 2026): the last public pages with no form of their own.
CALC_FORMS = {
    'medicare-cost-calculator': ('Medicare cost check', 'medicare', '/thank-you'),
    'life-insurance-calculator': ('Life insurance amount check', 'life', '/thank-you-life?t=life'),
    'retirement-calculator': ('Retirement income question', 'annuity', '/thank-you-life?t=annuity'),
    'aca-subsidy-calculator': ('ACA plan and savings check', 'health', '/thank-you'),
    'ichra-calculator': ('ICHRA for my business', 'group', '/thank-you'),
}
GROUP_FORMS = {'group-health-insurance-shop': 'Group health insurance (SHOP)', 'ichra': 'ICHRA', 'small-business-employee-benefits': 'Small business employee benefits'}
EMPLOYEES = ['Just me', '2 to 5', '6 to 19', '20 to 50', 'More than 50']
BIZ = lambda: '<div><label for="qx-biz">Business name</label>\n        <input id="qx-biz" type="text" name="Business" autocomplete="organization"></div>'


def _group(blk):
    """An employer form asks for the number of employees, not the visitor's age."""
    new, n = re.subn(r'<div><label for="([a-z0-9]+)-age">Your age</label>\s*<select id="\1-age" name="Age range">.*?</select></div>',
                     lambda m: '<div><label for="%s-emp">Number of employees</label>\n        <select id="%s-emp" name="Employees">%s</select></div>'
                     % (m.group(1), m.group(1), '<option value="">Select</option>' + ''.join('<option>%s</option>' % x for x in EMPLOYEES)), blk, count=1, flags=re.S)
    if n != 1: raise SystemExit('lifeleads: age field not found in the form shell')
    return new


def last_forms(out):
    shell = _form_shell(out); n = {'calculators': 0, 'employer': 0}
    sub = 'We reply within one business day, by text if you prefer.'
    for slug, (name, line, thanks) in CALC_FORMS.items():
        p = os.path.join(out, slug + '.html')
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        mark = '    <div class="prose">'
        if 'id="quote"' in s or s.count(mark) != 1: raise SystemExit('lifeleads: calculator layout changed: ' + slug)
        blk = _make_form(shell, name, name, 'Ask an agent to check your numbers',
                         'This sends only the contact details below, not what you typed in the calculator. ' + sub,
                         line, thanks, [BIZ(), BEST()] if line == 'group' else [BEST()], 'qc')
        if line == 'group': blk = _group(blk)
        s = s.replace(mark, blk + '\n' + mark, 1)
        open(p, 'w', encoding='utf-8').write(s); n['calculators'] += 1
    for slug, name in GROUP_FORMS.items():
        p = os.path.join(out, slug + '.html')
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        blk = _group(_make_form(shell, name, name, 'Ask about coverage for your team', 'Tell us about your business. ' + sub, 'group', '/thank-you', [BIZ(), BEST()], 'qg'))
        s, ok = _place(s, blk)
        if not ok: raise SystemExit('lifeleads: employer page layout changed: ' + slug)
        open(p, 'w', encoding='utf-8').write(s); n['employer'] += 1
    return n


# ---------------------------------------------------------------------------------------------------------------------
# Last pass over every page with a form (Nov 25, 2026, from the two pre-publish reviews). Runs after every form is placed.
# - The age field starts on an empty "Select", so an untouched field is not sent as "Under 40".
# - "Best way to reach you" offers "Email me", so the form has an optional Email field.
# - The three older health forms get a line for the lead events, like every other form.
# - Every "/#contact" link on a page with its own form goes to that form. Exception: the Medicare enrollment banner on a
#   page whose form is not a Medicare or area form keeps going to the general form (a Medicare visitor should not land in a
#   life, annuity or employer form).
# - <body data-line> is set from the form's line where the page has none, so booking, text and call clicks report a line.
OLD_HEALTH = ('accident-insurance', 'hsa-health-plans', 'private-health-insurance')
AEP_RX = re.compile(r'<div class="aep-banner sans" id="aepBanner">.*?</div>', re.S)


def finish_forms(out):
    n = {'pages': 0, 'email field': 0, 'age starts empty': 0, 'links to the form': 0, 'banner kept': 0, 'body line': 0}
    for p in glob.glob(os.path.join(out, '*.html')):
        s = open(p, encoding='utf-8').read()
        a = s.find('<section id="quote"')
        if a < 0: continue
        slug = os.path.basename(p)[:-5]; o = s
        b = s.index('</section>', a); blk = s[a:b]
        if blk.count('<form ') != 1: raise SystemExit('lifeleads: expected one form in the quote section: ' + slug)
        m = re.search(r'<form [^>]*data-line="([^"]*)"', blk)
        if not m:
            if slug not in OLD_HEALTH: raise SystemExit('lifeleads: form without a line: ' + slug)
            blk = blk.replace('<form action="https://formspree.io/f/', '<form data-line="health" data-thanks="/thank-you" action="https://formspree.io/f/', 1)
            m = re.search(r'<form [^>]*data-line="([^"]*)"', blk)
        line = m.group(1)
        if 'name="Age range"><option value="">' not in blk and 'name="Age range">' in blk:
            if blk.count('name="Age range">') != 1: raise SystemExit('lifeleads: age field: ' + slug)
            blk = blk.replace('name="Age range">', 'name="Age range"><option value="">Select</option>', 1); n['age starts empty'] += 1
        if '<option>Email me</option>' in blk and 'name="Email"' not in blk:
            blk, k = re.subn(r'(<select id="([a-z0-9]+)-how" name="Contact preference">.*?</select></div>\s*</div>)',
                             lambda x: x.group(1) + '\n      <label for="%s-email">Email (optional)</label>\n      <input id="%s-email" type="email" name="Email" autocomplete="email">' % (x.group(2), x.group(2)),
                             blk, count=1, flags=re.S)
            if k != 1: raise SystemExit('lifeleads: contact preference field not found: ' + slug)
            css = '.hb-quote input[type=tel],'
            if blk.count(css) != 1: raise SystemExit('lifeleads: form style not found: ' + slug)
            blk = blk.replace(css, css + '.hb-quote input[type=email],', 1); n['email field'] += 1
        if re.search(r'<select[^>]*>\s*<option[^>]*data-hot', blk): raise SystemExit('lifeleads: a HOT answer is the default on ' + slug)
        s = s[:a] + blk + s[b:]
        keep = None
        if line not in ('medicare', 'area'):
            bm = AEP_RX.search(s)
            if bm and 'href="/#contact"' in bm.group(0):
                keep = bm.group(0); s = s[:bm.start()] + '\x00AEP\x00' + s[bm.end():]; n['banner kept'] += 1
        n['links to the form'] += s.count('href="/#contact"')
        s = s.replace('href="/#contact"', 'href="#quote"')
        # buttons that point at the contact page do the same (annuities.html); the menu's own "Contact" link stays
        s, k = re.subn(r'href="/contact"(?=[^>]*>(?!Contact</a>))', 'href="#quote"', s); n['links to the form'] += k
        if keep: s = s.replace('\x00AEP\x00', keep, 1)
        bi = s.find('<body'); be = s.find('>', bi) + 1
        if bi < 0: raise SystemExit('lifeleads: form page without a body tag: ' + slug)
        if 'data-line=' not in s[bi:be]:
            s = s[:bi] + re.sub(r'<body([^>]*)>', lambda x: '<body%s data-line="%s">' % (x.group(1), line), s[bi:be], count=1) + s[be:]; n['body line'] += 1
        ids = re.findall(r'\bid="([^"]+)"', s)
        if len(ids) != len(set(ids)): raise SystemExit('lifeleads: duplicate id on %s: %s' % (slug, sorted(x for x in set(ids) if ids.count(x) > 1)[:5]))
        if s != o: open(p, 'w', encoding='utf-8').write(s)
        n['pages'] += 1
    return n
