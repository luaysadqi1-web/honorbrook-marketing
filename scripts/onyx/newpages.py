"""Honorbrook Onyx: new pages from research verified on Nov 24, 2026 (research, then an independent fact check of every source).

- ACA state pages for Delaware, Washington DC, Kentucky, Pennsylvania, Tennessee and Florida, built with the same generator as the
  first 11 (scripts/aca_gen.py build()), from scripts/onyx/data/aca/<state>.json. DC and Florida have no county pages, so their
  county section is left out.
- Medicare Advantage pages for West Virginia and Louisiana (the scorecard's first two product-by-state pages), from the CMS CY2027
  landscape file (Nov 2026 refresh) and the CMS MA penetration file (Sept 2026), in scripts/onyx/data/ma/<state>.json. Counts only:
  no premiums, no $0, no star ratings, no carrier names (owner rules).
Pages are written into the build before the page pass, so they get the same header, footer, booking blocks and phone handling.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
DATA = os.path.join(HERE, 'data')
BASE = 'https://honorbrook-insurance.com'
BOOK = 'https://www.planenroll.com/?purl=Luay-Sadqi'
ACA = ['delaware', 'washington-dc', 'kentucky', 'pennsylvania', 'tennessee', 'florida']
MA = ['west-virginia', 'louisiana']
DATE = '2026-11-25'
e = html.escape


GTAG = '<!-- Google tag (gtag.js) -->'
OPT_OUT = "<script>try{if(localStorage.getItem('hb_analytics')==='off')window['ga-disable-G-J5YG8E3PYC']=true}catch(e){}</script>"


def _name(j):
    return 'Washington, DC' if j['slug'] == 'washington-dc' else j['state']


def aca_pages(out):
    sys.path.insert(0, SCRIPTS)
    import county_gen as g
    import aca_gen as a
    import footprint
    cen, pen, hosp = g.load(); agg = g.build_agg(cen, pen)
    slugmap = json.load(open(os.path.join(SCRIPTS, 'county_data', 'slugmap.json')))
    hdr, foot = a.shell()
    made = []
    for slug in ACA:
        j = json.load(open(os.path.join(DATA, 'aca', slug + '.json')))
        sname = _name(j); c = j['copy']
        a.COPY[slug] = dict(exch=c['exch'], exch_type=c['exch_type'], medicaid=c['medicaid'], state_help=c.get('state_help'))
        st = dict(g.STATES.get(sname) or {'slug': slug, 'unit': 'counties'})
        if sname not in g.DOI:   # DC and Florida: the regulator that verifies agent licenses
            g.DOI[sname] = (('Florida Department of Financial Services', 'https://www.myfloridacfo.com/') if slug == 'florida' else (j['doi_name'], j['doi_url']))
        counties = sname in agg
        if not counties: agg[sname] = {'order': []}
        page_slug, page = a.build(sname, st, j, cen, pen, agg, slugmap, hdr, foot)
        page = page.replace('as of October 2026', 'as of November 2026')
        if not counties:
            page = re.sub(r'\n    <h2>ACA help by (?:county|parish) in [^<]*</h2>.*?</ul>\n', '\n', page, count=1, flags=re.S)
            page = re.sub(r'\s*<a class="rel-card" href="/%s-counties">.*?</a>' % re.escape(slug), '', page, count=1, flags=re.S)
        # Nov 25 review: these pages are written after footprint.apply(), from the raw shell, so they need the same pass
        # (16 states + DC header and footer, full county directory list), the analytics opt-out line, and two wording fixes.
        page = footprint.transform(os.path.join(out, page_slug + '.html'), page)
        for old in ('Licensed in 11 states', '10 more states', '10 additional states', '11 states'):
            if old in page: raise SystemExit('newpages: old footprint wording left on %s: %s' % (page_slug, old))
        if 'hb_analytics' not in page:
            if page.count(GTAG) != 1: raise SystemExit('newpages: Google tag comment not found on ' + page_slug)
            page = page.replace(GTAG, GTAG + '\n' + OPT_OUT, 1)
        if counties:
            ncty = len(re.findall(r'<li>', re.search(r'<h2>ACA help by (?:county|parish) in [^<]*</h2>.*?</ul>', page, re.S).group(0)))
            if ncty < 10:   # Delaware has three counties; the generator always says "the 10 largest"
                m = re.search(r'Here are the 10 largest (counties|parishes)\. See all of them in our (<a href="[^"]*">[^<]*</a>)\.', page)
                if not m: raise SystemExit('newpages: county sentence not found on ' + page_slug)
                page = page.replace(m.group(0), '%s has %d %s. Each has its own page in our %s.' % (sname, ncty, m.group(1), m.group(2)), 1)
        hc = '<li><a href="https://www.healthcare.gov/" rel="noopener" target="_blank">HealthCare.gov</a>:'
        if page.count(hc) == 2:   # federal-Marketplace states listed the same link twice
            page, k = re.subn(r'\n[ \t]*' + re.escape(hc) + r' federal Marketplace information\.</li>', '', page, count=1)
            if k != 1: raise SystemExit('newpages: duplicate HealthCare.gov line not found on ' + page_slug)
        open(os.path.join(out, page_slug + '.html'), 'w', encoding='utf-8').write(page)
        made.append((page_slug, sname))
    # national ACA page and each new state hub link the new pages
    p = os.path.join(out, 'aca-health-insurance.html'); s = open(p, encoding='utf-8').read()
    anchor = '<li><a href="/west-virginia-aca-health-insurance">West Virginia: 2027 enrollment, Medicaid and help</a></li>'
    if anchor in s and '/florida-aca-health-insurance"' not in s:
        s = s.replace(anchor, anchor + ''.join('\n      <li><a href="/%s">%s: 2027 enrollment, Medicaid and help</a></li>' % (ps, n) for ps, n in made), 1)
        open(p, 'w', encoding='utf-8').write(s)
    for ps, n in made:
        hub = os.path.join(out, ps.replace('-aca-health-insurance', '-medicare-insurance') + '.html')
        if not os.path.exists(hub): continue
        s = open(hub, encoding='utf-8').read()
        a_ = 'read our <a href="/aca-health-insurance">guide to ACA health insurance</a>.'
        if a_ in s and 'href="/%s"' % ps not in s:
            s = s.replace(a_, a_ + ' See <a href="/%s">2027 Marketplace dates, Medicaid rules and help in %s</a>.' % (ps, n), 1)
            open(hub, 'w', encoding='utf-8').write(s)
    return [ps for ps, n in made]


def _head(shell, title, desc, canon, ld):
    h = shell[:shell.index('</head>')]
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h, count=1, flags=re.S)
    for attr, name, val in (('name', 'description', desc), ('property', 'og:title', title), ('property', 'og:description', desc),
                            ('property', 'og:url', canon), ('name', 'twitter:title', title), ('name', 'twitter:description', desc)):
        h = re.sub(r'(<meta %s="%s" content=")[^"]*(")' % (attr, re.escape(name)), lambda m: m.group(1) + val + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + canon + m.group(2), h, count=1)
    h = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', h, flags=re.S)
    return h + ''.join('\n<script type="application/ld+json">\n%s\n</script>' % json.dumps(x, indent=2, ensure_ascii=False) for x in ld) + '\n'


def ma_page(out, slug):
    d = json.load(open(os.path.join(DATA, 'ma', slug + '.json')))
    name, unit = d['state'], d['county_unit']; units = 'parishes' if unit == 'parish' else 'counties'
    sw = d['statewide']; pr = d['page_ready']
    assert sw['total'] == sw['snp'] + sw['ma_pd'] + sw['ma_only'] and 'All special needs plans include drug coverage' in pr[1], slug
    hub = '/%s-medicare-insurance' % slug
    shell = open(os.path.join(out, slug + '-medicare-insurance.html'), encoding='utf-8').read()
    top = shell[shell.index('</head>'):shell.index('<section class="page-hero"')]
    foot = shell[shell.index('<footer'):]
    page_slug = slug + '-medicare-advantage'; canon = '%s/%s' % (BASE, page_slug)
    title = '%s Medicare Advantage Plans 2027 | Honorbrook' % name
    desc = ('For 2027, CMS lists %d Medicare Advantage plans in %s, %d to %d per %s. Compare the plans we offer by phone or video with an independent agent.'
            % (sw['total'], name, sw['total_per_county_min'], sw['total_per_county_max'], unit))
    rows = sorted(d['per_county'], key=lambda r: r['county'])
    trs = '\n'.join('          <tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%s%%</td></tr>'
                    % (('<a href="/%s">%s</a>' % (r['slug'], e(r['county'])) if r.get('slug_exists') else e(r['county'])),
                       r['total'], r['ma_pd'], r['snp'], ('%.1f' % r['penetration_pct']) if r.get('penetration_pct') is not None else '&ndash;') for r in rows)
    periods = '\n'.join('      <li><strong>%s.</strong> %s</li>' % (e(p['name']), e(p['page_copy'])) for p in d['periods'] if p.get('page_copy'))
    ship, doi = d['ship'], d['doi']
    ship_short = ship.get('short_name') or ship['name']
    faq = [
        ('How many Medicare Advantage plans are in %s for 2027?' % name, '%s %s' % (pr[0], pr[3])),
        ('Do all Medicare Advantage plans include drug coverage?',
         'No. Of the %d Medicare Advantage plans CMS lists in %s for 2027, %d are special needs plans, and all of those include drug coverage. Of the other %d, %d include drug coverage and %d do not.'
         % (sw['total'], name, sw['snp'], sw['total'] - sw['snp'], sw['ma_pd'], sw['ma_only'])),
        ('Who can join a special needs plan?', pr[2]),
        ('When can I join or switch a Medicare Advantage plan?', 'Most people can first join when they turn 65, during a 7-month window. Each year from October 15 to December 7 you can join, switch or drop a plan, and the change starts January 1. If you are already in a Medicare Advantage plan, you can switch plans or go back to Original Medicare from January 1 to March 31.'),
        ('Does it cost anything to use Honorbrook?', 'No. Carriers pay us when you enroll, and your premium is the same whether you use an agent or enroll on your own. We do not offer every plan available in your area.'),
    ]
    faq_html = '\n'.join('    <details><summary>%s</summary><div class="a">%s</div></details>' % (e(q), e(a)) for q, a in faq)
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": BASE + hub},
            {"@type": "ListItem", "position": 3, "name": "Medicare Advantage", "item": canon}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "telephone": "+1-571-354-0146", "url": canon,
         "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA",
                     "postalCode": "22182", "addressCountry": "US"}, "areaServed": {"@type": "State", "name": name}},
    ]
    src = [('CMS CY2027 Medicare Advantage and Prescription Drug Plan Landscape, November 2026 data refresh', 'https://www.cms.gov/medicare/coverage/prescription-drug-coverage'),
           ('CMS Medicare Advantage State/County Penetration, September 2026', 'https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/ma-state/county-penetration'),
           ('Medicare.gov: joining a plan', 'https://www.medicare.gov/basics/get-started-with-medicare/get-more-coverage/joining-a-plan'),
           ('Medicare.gov: special needs plans', 'https://www.medicare.gov/health-drug-plans/health-plans/your-health-plan-options/SNP')]
    src_html = '\n'.join('      <li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (u, e(t)) for t, u in src)
    change = '/blog/when-can-i-change-my-medicare-plan-in-%s' % slug
    body = '''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="%(hub)s">%(name)s</a> &rsaquo; Medicare Advantage</div>
    <h1>Medicare Advantage in <em>%(name)s</em>: 2027 plans by %(unit)s</h1>
    <p class="lead">%(pr0)s Honorbrook is an independent agency licensed in %(name)s. We compare the plans we offer in your %(unit)s, check your doctors and prescriptions, and help you enroll by phone or video.</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="%(book)s" target="_blank" rel="noopener">Schedule an appointment</a>
      <a class="btn-ghost" href="tel:+15713540146">Call (571) 354-0146</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>%(name)s Medicare Advantage at a glance</h2>
    <div class="table-wrap">
      <table class="compare">
        <thead><tr><th>&nbsp;</th><th>%(name)s, 2027</th></tr></thead>
        <tbody>
          <tr><td>Medicare Advantage plans listed by CMS</td><td>%(total)d</td></tr>
          <tr><td>With drug coverage (not special needs)</td><td>%(ma_pd)d</td></tr>
          <tr><td>Without drug coverage</td><td>%(ma_only)d</td></tr>
          <tr><td>Special needs plans (all include drug coverage)</td><td>%(snp)d</td></tr>
          <tr><td>Plans per %(unit)s</td><td>%(mn)d to %(mx)d</td></tr>
          <tr><td>Companies offering plans</td><td>%(orgs)d</td></tr>
          <tr><td>People with Medicare in a Medicare Advantage plan (Sept 2026)</td><td>%(pen).1f%%</td></tr>
        </tbody>
      </table>
    </div>
    <p>%(pr1)s %(pr2)s</p>
    <p>%(pr3)s %(pr4)s</p>
    <p>%(pr5)s</p>
    <p class="sans" style="font-size:14px;color:var(--muted)">%(pr6)s Plan lists can change as contracts are finalized; confirm on Medicare.gov before you enroll.</p>

    <div class="hb-book">
      <h3>Schedule a Medicare Advantage review</h3>
      <p>Booking opens Luay&rsquo;s page on PlanEnroll. Create your profile there and ask for your meeting. Having these ready makes the first conversation useful:</p>
      <ul><li>Your Medicare card, or the dates your Part A and Part B start.</li><li>The doctors and hospitals you want to keep.</li><li>A list of your prescriptions and the pharmacy you use.</li><li>Whether you have Medicaid or get help paying Medicare costs.</li></ul>
      <p class="hb-book-type">When PlanEnroll asks what type of meeting you would like, choose <strong>Health</strong>. You may be asked to complete a short Scope of Appointment form first. It does not obligate you to enroll. The first open time is at least 24 hours ahead. To talk sooner, call <a href="tel:+15713540146">(571) 354-0146</a>.</p>
      <div class="hb-book-cta sans"><a class="btn-primary" href="%(book)s" target="_blank" rel="noopener">Schedule an appointment</a><a class="hb-book-how" href="/schedule-an-appointment">How scheduling works</a></div>
    </div>

    <h2>Medicare Advantage plans by %(unit)s in %(name)s</h2>
    <p>Plans are offered by %(unit)s, so the choices where you live can differ from the next %(unit)s over. Counts include special needs plans. Select a %(unit)s for Medicare facts and help where you live.</p>
    <div class="table-wrap">
      <table class="compare">
        <thead><tr><th>%(Unit)s</th><th>Plans</th><th>With drug coverage (not special needs)</th><th>Special needs</th><th>In Medicare Advantage</th></tr></thead>
        <tbody>
%(trs)s
        </tbody>
      </table>
    </div>

    <h2>When you can join or switch</h2>
    <ul>
%(periods)s
    </ul>
    <p>See <a href="%(change)s">when you can change Medicare plans in %(name)s</a> for special enrollment periods and the Medigap rules that apply.</p>

    <h2>How we help you choose</h2>
    <p>The number of plans matters less than whether a plan fits you. We check that your doctors and hospitals are in the plan&rsquo;s network, look up each of your prescriptions, and compare the total yearly cost of the plans we offer, not only the premium. If you have both Medicare and Medicaid, we check whether a special needs plan fits. See <a href="/medicare-advantage">how Medicare Advantage works</a> and <a href="/medicare-supplement-medigap">Medicare Supplement</a>, the main alternative.</p>

    <h2>Free counseling and your state regulator</h2>
    <p>%(name)s&rsquo;s State Health Insurance Assistance Program, <a href="%(ship_url)s" rel="noopener" target="_blank">%(ship_short)s</a>, gives free, unbiased Medicare counseling and does not sell insurance. The <a href="%(doi_url)s" rel="noopener" target="_blank">%(doi_name)s</a> regulates insurance in %(name)s and can verify an agent&rsquo;s license.</p>

    <h2>Sources</h2>
    <ul>
%(src)s
    </ul>
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">%(name)s Medicare Advantage FAQ</h2>
%(faq)s
  </div>
</section>

<div class="band">
  <div class="wrap">
    <h2>One honest call can make all the difference.</h2>
    <p>Free consultation &middot; No obligation &middot; No pressure</p>
    <a class="phone" href="tel:+15713540146">(571) 354-0146</a>
  </div>
</div>

<section class="related">
  <div class="wrap">
    <div class="kicker" style="text-align:center;margin-bottom:20px">More %(name)s coverage</div>
    <div class="grid-3">
      <a class="rel-card" href="%(hub)s"><h3>%(name)s Medicare</h3><p>Medicare help for %(name)s residents, by phone or video.</p></a>
      <a class="rel-card" href="/%(slug)s-counties"><h3>%(name)s by %(unit)s</h3><p>Medicare facts for every %(unit)s.</p></a>
      <a class="rel-card" href="/%(slug)s-life-insurance"><h3>%(name)s life insurance</h3><p>Final expense, term and whole life in %(name)s.</p></a>
    </div>
  </div>
</section>

''' % dict(hub=hub, name=e(name), unit=unit, Unit=unit.capitalize(), book=BOOK, pr0=e(pr[0]), pr1=e(pr[1]), pr2=e(pr[2]), pr3=e(pr[3]), pr4=e(pr[4]),
           pr5=e(pr[5]), pr6=e(pr[6]), total=sw['total'], ma_pd=sw['ma_pd'], ma_only=sw['ma_only'], snp=sw['snp'], mn=sw['total_per_county_min'],
           mx=sw['total_per_county_max'], orgs=sw['orgs'], pen=sw['penetration_pct'], trs=trs, periods=periods, change=change,
           ship_url=ship['url'], ship_short=e(ship_short), doi_url=doi['url'], doi_name=e(doi['name']), src=src_html, faq=faq_html, slug=slug)
    page = _head(shell, title, desc, canon, ld) + top + body + foot
    open(os.path.join(out, page_slug + '.html'), 'w', encoding='utf-8').write(page)
    return page_slug, name, units


def ma_pages(out):
    made = []
    for slug in MA:
        page_slug, name, units = ma_page(out, slug)
        made.append(page_slug)
        # the state hub lists it under the coverage we offer; every county or parish page lists it to read next
        hub = os.path.join(out, slug + '-medicare-insurance.html'); s = open(hub, encoding='utf-8').read()
        a = '<li><a href="/medicare-advantage">Medicare Advantage</a>'
        i = s.find(a)
        if i >= 0 and 'href="/%s"' % page_slug not in s:
            j = s.index('</li>', i) + len('</li>')
            s = s[:j] + '\n      <li><a href="/%s">Medicare Advantage in %s</a> — 2027 plan counts for every %s, from CMS.</li>' % (page_slug, name, 'county' if units == 'counties' else 'parish') + s[j:]
            open(hub, 'w', encoding='utf-8').write(s)
    # national Medicare Advantage page: by-state links
    p = os.path.join(out, 'medicare-advantage.html'); s = open(p, encoding='utf-8').read()
    if '/west-virginia-medicare-advantage"' not in s and '<div class="cta-strip">' in s:
        line = '<p>Medicare Advantage by state: %s.</p>\n    ' % ', '.join('<a href="/%s-medicare-advantage">%s</a>' % (x, x.replace('-', ' ').title()) for x in MA)
        s = s.replace('<div class="cta-strip">', line + '<div class="cta-strip">', 1)
        open(p, 'w', encoding='utf-8').write(s)
    return made


def county_links(out):
    """After the page pass: each WV county and LA parish page lists its state's Medicare Advantage page under its reading list."""
    import glob
    rx = re.compile(r'(<h2>(?:Read next|Plain-English Medicare answers|Medicare guides for [^<]*)</h2>\s*<ul>)')
    n = 0
    for slug, ab in (('west-virginia', 'wv'), ('louisiana', 'la')):
        name = slug.replace('-', ' ').title()
        for f in glob.glob(os.path.join(out, '*-%s-medicare-insurance.html' % ab)):
            s = open(f, encoding='utf-8').read()
            if '/%s-medicare-advantage"' % slug in s: continue
            t = rx.sub(lambda m: m.group(1) + '\n      <li><a href="/%s-medicare-advantage">Medicare Advantage plans in %s for 2027</a></li>' % (slug, name), s, count=1)
            if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
    return n


def sitemap(out, pages):
    p = os.path.join(out, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    add = ''.join('  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n' % (BASE, x, DATE)
                  for x in pages if '/%s</loc>' % x not in s)
    open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', add + '</urlset>'))
    lp = os.path.join(out, 'llms.txt')
    if os.path.exists(lp):
        t = open(lp, encoding='utf-8').read()
        if '## Medicare Advantage by state' not in t:
            t = t.rstrip('\n') + '\n\n## Medicare Advantage by state\n' + ''.join('- [%s Medicare Advantage plans 2027](%s/%s-medicare-advantage)\n' % (x.replace('-', ' ').title(), BASE, x) for x in MA)
            open(lp, 'w', encoding='utf-8').write(t)


# ---------------------------------------------------------------------------------------------------------------------
# Content pieces (Nov 25, 2026): written by one agent, re-checked by another against each source, stored as JSON in
# scripts/onyx/data/content/. kind "page" is a top-level page; kind "post" is a blog post (card on the blog index).
CONTENT = os.path.join(DATA, 'content')
MONTH = 'November 2026'
AUTHOR = {"@type": "Person", "@id": BASE + "/#luay-sadqi", "name": "Luay Sadqi", "jobTitle": "Founder & Designated Responsible Licensed Producer",
          "url": BASE + "/about", "identifier": "NPN 21370662", "worksFor": {"@id": BASE + "/#organization"}}
BAND = '''<div class="band">
  <div class="wrap">
    <h2>One honest call can make all the difference.</h2>
    <p>No obligation &middot; No pressure</p>
    <a class="phone" href="tel:+15713540146">(571) 354-0146</a>
  </div>
</div>
'''


def _faq_html(name, faq):
    return ('<section class="faq">\n  <div class="wrap" style="max-width:880px">\n    <div class="kicker">Common questions</div>\n'
            '    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">%s FAQ</h2>\n' % e(name)
            + '\n'.join('    <details><summary>%s</summary><div class="a">%s</div></details>' % (e(x['q']), e(x['a'])) for x in faq)
            + '\n  </div>\n</section>\n')


def _related(rel):
    return ('<section class="related">\n  <div class="wrap">\n    <div class="kicker" style="text-align:center;margin-bottom:20px">Keep exploring</div>\n    <div class="grid-3">\n'
            + '\n'.join('      <a class="rel-card" href="%s"><h3>%s</h3><p>%s</p></a>' % (x['href'], e(x['title']), e(x['text'])) for x in rel)
            + '\n    </div>\n  </div>\n</section>\n')


def _states_block(out):
    """The life version of the 'rules vary by state' block the other life posts carry (copied from one of them)."""
    s = open(os.path.join(out, 'blog', 'what-is-indexed-universal-life-iul-how-it-works-cost-risks.html'), encoding='utf-8').read()
    i = s.index('<h2>Availability and rules vary by state</h2>'); j = s.index('</ul>', i) + len('</ul>')
    return '    ' + s[i:j] + '\n'


def content_pages(out):
    made = []
    for f in sorted(glob_json(CONTENT)):
        c = json.load(open(f, encoding='utf-8'))
        slug, kind = c['slug'], c['kind']
        canon = '%s/%s' % (BASE, slug)
        for x in c['related']:
            if not os.path.exists(os.path.join(out, x['href'].lstrip('/').split('#')[0] + '.html')): raise SystemExit('newpages: related link missing: ' + x['href'])
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": x['q'], "acceptedAnswer": {"@type": "Answer", "text": x['a']}} for x in c['faq']]}
        if kind == 'post':
            shell = open(os.path.join(out, 'blog', 'graded-death-benefit-final-expense-explained.html'), encoding='utf-8').read()
            crumb = [("Home", BASE + "/"), ("Blog", BASE + "/blog/"), (c['breadcrumb'], canon)]
            ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumb)]},
                  {"@context": "https://schema.org", "@type": "BlogPosting", "headline": html.unescape(re.sub(r'<[^>]+>', '', c['h1_html'])), "description": html.unescape(c['description']),
                   "datePublished": DATE, "dateModified": DATE, "author": AUTHOR, "publisher": {"@type": "Organization", "name": "Honorbrook Insurance"},
                   "mainEntityOfPage": {"@type": "WebPage", "@id": canon}}, faq_ld]
            hero = ('<section class="page-hero" id="maincontent" role="main">\n  <div class="wrap">\n    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; %s</div>\n'
                    '    <h1>%s</h1>\n    <p class="lead">%s</p>\n    <p class="byline sans">By Luay Sadqi, Licensed Agent (NPN 21370662) · %s</p>\n  </div>\n</section>\n\n'
                    % (e(c['breadcrumb']), c['h1_html'], c['lead'], MONTH))
            article = '<article class="article">\n  <div class="wrap prose">\n%s\n\n%s  </div>\n</article>\n' % (c['article_html'].strip(), _states_block(out))
        else:
            shell = open(os.path.join(out, 'indexed-universal-life.html'), encoding='utf-8').read()
            crumb = [("Home", BASE + "/"), ("Life Insurance", BASE + "/life-insurance"), (c['breadcrumb'], canon)]
            ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumb)]}, faq_ld,
                  {"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "telephone": "+1-571-354-0146", "url": canon,
                   "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA", "postalCode": "22182", "addressCountry": "US"}}]
            hero = ('<section class="page-hero" id="maincontent" role="main">\n  <div class="wrap">\n    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/life-insurance">Life Insurance</a> &rsaquo; %s</div>\n'
                    '    <h1>%s</h1>\n    <p class="lead">%s</p>\n    <p class="sans" style="font-size:14px;color:#aebbd0;letter-spacing:.3px;margin-top:4px">Reviewed by Luay Sadqi, Licensed Agent &middot; NPN 21370662 &middot; Updated %s</p>\n'
                    '    <div class="hero-ctas sans">\n      <a class="btn-primary" href="%s" target="_blank" rel="noopener">Schedule an appointment</a>\n      <a class="btn-ghost" href="tel:+15713540146">Call (571) 354-0146</a>\n    </div>\n  </div>\n</section>\n\n'
                    % (e(c['breadcrumb']), c['h1_html'], c['lead'], MONTH, BOOK))
            article = '<article class="article">\n  <div class="wrap prose">\n%s\n  </div>\n</article>\n' % c['article_html'].strip()
        top = shell[shell.index('</head>'):shell.index('<section class="page-hero"')]
        if kind == 'page' and c.get('banner'):   # the shell page's banner is about that page; use this page's own line
            top = re.sub(r'<div class="aep-banner[^>]*>.*?</div>', lambda m: '<div class="aep-banner sans">%s</div>' % c['banner'], top, count=1, flags=re.S)
        foot = shell[shell.index('<footer'):]
        page = _head(shell, c['title'], c['description'], canon, ld) + top + hero + article + '\n' + _faq_html(c['breadcrumb'], c['faq']) + '\n' + BAND + '\n' + _related(c['related']) + '\n' + foot
        dest = os.path.join(out, slug + '.html')
        open(dest, 'w', encoding='utf-8').write(page)
        made.append((slug, kind, c))
    # blog index: a card for each new post, first in the list
    posts = [(s_, c) for s_, k, c in made if k == 'post']
    if posts:
        p = os.path.join(out, 'blog', 'index.html'); s = open(p, encoding='utf-8').read()
        i = s.index('<a class="rel-card" href="/blog/')
        cards = ''.join('<a class="rel-card" href="/%s">\n        <h3>%s</h3>\n        <p class="sans" style="font-size:13px;color:var(--gold-d);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px">%s</p>\n        <p>%s</p>\n      </a>\n      '
                        % (s_, re.sub(r'<[^>]+>', '', c['h1_html']), MONTH, c['description']) for s_, c in posts if 'href="/%s"' % s_ not in s)
        open(p, 'w', encoding='utf-8').write(s[:i] + cards + s[i:])
    return [s_ for s_, k, c in made]


def glob_json(folder):
    import glob
    return glob.glob(os.path.join(folder, '*.json'))


def content_sitemap(out, slugs):
    p = os.path.join(out, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    add = ''.join('  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>\n' % (BASE, x, DATE, '0.6' if x.startswith('blog/') else '0.8')
                  for x in slugs if '/%s</loc>' % x not in s)
    open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', add + '</urlset>'))
