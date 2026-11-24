"""Footprint: 16 states + DC (17 markets). Georgia confirmed by the owner 2026-11-13 and again 2026-11-21 ("include georgia").
Florida added 2026-11-21: Florida approved the non-resident agent license on 2026-11-19 (Sircon confirmation 380057517, owner's Gmail).

Original 11: VA, MD, WV, GA, NC, SC, TX, LA, AL, MI, IN.   New in Nov 2026: DE, DC, KY, PA, TN.
apply(site_dir) rewrites the wording, state lists and schema on every page, patches the area finder, and writes a state page for
each new market. It only adds: no page is removed. Every fact on the new pages was checked against an official source in Nov 2026.
"""
import glob, html, json, os, re

ORIGINAL = [('Virginia', 'VA', 'virginia'), ('Maryland', 'MD', 'maryland'), ('West Virginia', 'WV', 'west-virginia'), ('Georgia', 'GA', 'georgia'),
            ('North Carolina', 'NC', 'north-carolina'), ('South Carolina', 'SC', 'south-carolina'), ('Texas', 'TX', 'texas'), ('Louisiana', 'LA', 'louisiana'),
            ('Alabama', 'AL', 'alabama'), ('Michigan', 'MI', 'michigan'), ('Indiana', 'IN', 'indiana')]

# name, abbr, page slug, short name used in running text, and verified facts (sources in comments)
NEW = [
    dict(name='Delaware', ab='DE', slug='delaware', the='Delaware', res='Delaware residents',
         # https://insurance.delaware.gov/divisions/dmab/
         ship='Delaware Medicare Assistance Bureau (DMAB)', ship_org='the Delaware Department of Insurance', ship_tel='1-800-336-9500',
         ship_url='https://insurance.delaware.gov/divisions/dmab/',
         doi='Delaware Department of Insurance', doi_url='https://insurance.delaware.gov/',
         # CMS marketplace map, plan year 2027: FFM
         exch='HealthCare.gov', exch_url='https://www.healthcare.gov/', exch_own=False,
         # KFF status of state Medicaid expansion decisions, Nov 2026
         expanded=True),
    dict(name='District of Columbia', ab='DC', slug='washington-dc', the='Washington, DC', res='DC residents',
         # https://dacl.dc.gov/service/health-insurance-counseling
         ship='DC State Health Insurance Assistance Program (SHIP)', ship_org='the DC Department of Aging and Community Living', ship_tel='(202) 727-8370',
         ship_url='https://dacl.dc.gov/service/health-insurance-counseling',
         doi='DC Department of Insurance, Securities and Banking', doi_url='https://disb.dc.gov/',
         exch='DC Health Link', exch_url='https://www.dchealthlink.com/', exch_own=True, expanded=True),
    dict(name='Kentucky', ab='KY', slug='kentucky', the='Kentucky', res='Kentucky residents',
         # https://www.chfs.ky.gov/agencies/dail/pages/ship.aspx
         ship='Kentucky State Health Insurance Assistance Program (SHIP)', ship_org='the Kentucky Department for Aging and Independent Living', ship_tel='1-877-293-7447',
         ship_url='https://www.chfs.ky.gov/agencies/dail/pages/ship.aspx',
         doi='Kentucky Department of Insurance', doi_url='https://insurance.ky.gov/',
         exch='kynect', exch_url='https://kynect.ky.gov/', exch_own=True, expanded=True),
    dict(name='Pennsylvania', ab='PA', slug='pennsylvania', the='Pennsylvania', res='Pennsylvania residents',
         # https://www.pa.gov/agencies/aging/aging-programs-and-services/pa-medi-medicare-counseling
         ship='Pennsylvania Medicare Education and Decision Insight (PA MEDI)', ship_org='the Pennsylvania Department of Aging', ship_tel='1-800-783-7067',
         ship_url='https://www.pa.gov/agencies/aging/aging-programs-and-services/pa-medi-medicare-counseling',
         doi='Pennsylvania Insurance Department', doi_url='https://www.pa.gov/agencies/insurance',
         exch='Pennie', exch_url='https://pennie.com/', exch_own=True, expanded=True),
    dict(name='Tennessee', ab='TN', slug='tennessee', the='Tennessee', res='Tennessee residents',
         # https://www.tn.gov/disability-and-aging/disability-aging-programs/tn-ship.html
         ship='Tennessee State Health Insurance Assistance Program (TN SHIP)', ship_org='the Tennessee Department of Disability and Aging', ship_tel='1-877-801-0044',
         ship_url='https://www.tn.gov/disability-and-aging/disability-aging-programs/tn-ship.html',
         doi='Tennessee Department of Commerce and Insurance', doi_url='https://www.tn.gov/commerce/insurance.html',
         exch='HealthCare.gov', exch_url='https://www.healthcare.gov/', exch_own=False, expanded=False),
    dict(name='Florida', ab='FL', slug='florida', the='Florida', res='Florida residents',
         # Florida's own SHIP site could not be reached from this Mac (IPv6 only), so the page names the program generically and
         # links to Medicare.gov's "talk to someone" page, which links SHIP help (checked Nov 21, 2026).
         ship=None, ship_org=None, ship_tel=None, ship_url='https://www.medicare.gov/talk-to-someone',
         # agent licensing: Florida Department of Financial Services (its Bureau of Licensing sends the license emails, myfloridacfo.com)
         doi='Florida Department of Financial Services', doi_url='https://www.myfloridacfo.com/',
         doi_role='licenses insurance agents in Florida. You can verify an agent&rsquo;s license with it.',
         # KFF State Health Insurance Marketplace Types, 2027: Federally Facilitated Marketplace
         exch='HealthCare.gov', exch_url='https://www.healthcare.gov/', exch_own=False,
         # KFF status of state action on the Medicaid expansion decision, as of November 2026: Not Adopted
         expanded=False),
]
NEW_NAMES = [s['name'] for s in NEW]
COUNT = '16 states and DC'
PROSE = ('Virginia, Maryland, West Virginia, Georgia, North Carolina, South Carolina, Texas, Louisiana, Alabama, Michigan, Indiana, '
         'Delaware, the District of Columbia, Kentucky, Pennsylvania, Tennessee, and Florida')
ABBR16 = 'VA, MD, NC, SC, GA, AL, LA, TX, MI, IN, WV, DE, DC, KY, PA, TN and FL'


def url(s): return '/%s-medicare-insurance' % s


def all16():
    """(name, abbr, state-page url, is_new) in display order."""
    return [(n, a, url(sl), False) for n, a, sl in ORIGINAL] + [(s['name'], s['ab'], url(s['slug']), True) for s in NEW]


FOOT_NEW = '<strong>Licensed in %s:</strong> ' % COUNT + ' · '.join('<a href="%s">%s</a>' % (u, n) for n, a, u, new in all16())
FOOT_RX = re.compile(r'<strong>Licensed in (?:11 states|14 states and DC|15 states and DC|16 states and DC):</strong>[^\n]*?>Indiana</a>(?:[^\n<]*?Tennessee(?:</a>)?)?'
                     r'(?: · <a href="/delaware-medicare-insurance">Delaware</a>[^\n]*?>Tennessee</a>(?: · <a href="/florida-medicare-insurance">Florida</a>)?)?')
_N11 = '|'.join(sorted([n for n, a, s in ORIGINAL], key=len, reverse=True))
LIST_RX = re.compile(r'(?:(?:%s)(?:, and |,? and |, | &amp; | & )){5,}(?:%s)' % (_N11, _N11) + r'(?:, Delaware, the District of Columbia, Kentucky, Pennsylvania,? and Tennessee)?')
JSON_LIST_RX = re.compile(r'\[\s*"Virginia",\s*"Maryland",\s*"(?:Georgia|West Virginia)"[^\]]*\]')
WV_OBJ = re.compile(r'(\{\s*"@type":\s*"State",\s*"name":\s*"West Virginia"\s*\})')
GA_OBJ_AFTER = re.compile(r'(\{\s*"@type":\s*"State",\s*"name":\s*"South Carolina"\s*\})(?!,\s*\{\s*"@type":\s*"State",\s*"name":\s*"Georgia")')
NEW_OBJS = ''.join(',\n    {"@type": "%s", "name": "%s"}' % ('AdministrativeArea' if s['name'] == 'District of Columbia' else 'State', s['name']) for s in NEW)
LI_COUNTY_WV = re.compile(r'([ \t]*)<li><a href="/west-virginia-medicare-insurance">West Virginia</a> (?:·|&middot;) <a href="/west-virginia-counties">county pages</a></li>(?!\n\s*<li><a href="/delaware)')
# new states that have county pages (built Nov 17, 2026) and how many; DC is one county-equivalent and uses its state page
COUNTY_N = {'DE': 3, 'KY': 120, 'PA': 67, 'TN': 95}
FOOT_COUNTY_RX = re.compile(r'(<strong>Medicare by county:</strong>[^\n]*?<a href="/west-virginia-counties">West Virginia</a>)(?! &middot; <a href="/delaware-counties")')
LI_DOI_WV = re.compile(r'([ \t]*)<li><strong><a href="/west-virginia-medicare-insurance">West Virginia</a>:</strong>[^\n]*</li>(?!\n\s*<li><strong><a href="/delaware)')
LI_DOI_SC = re.compile(r'([ \t]*)(<li><strong><a href="/south-carolina-medicare-insurance">South Carolina</a>:</strong>[^\n]*</li>)\n(?!\s*<li><strong><a href="/georgia)')
LI_STUB = re.compile(r'\n[ \t]*<li><strong>Delaware, District of Columbia, Kentucky, Pennsylvania, Tennessee:</strong>[^\n]*</li>')
GA_DOI = '<li><strong><a href="/georgia-medicare-insurance">Georgia</a>:</strong> <a href="https://oci.georgia.gov/" rel="noopener" target="_blank">Georgia Office of Insurance and Safety Fire Commissioner</a></li>'
WORDING = [
    ('Independent agency · Serving Virginia &amp; 10 more states', 'Independent agency · Licensed in 16 states + DC'),
    ('Independent agency &middot; Serving Virginia &amp; 10 more states', 'Independent agency &middot; Licensed in 16 states + DC'),
    ('Independent agency · Serving Virginia &amp; 13 more states plus DC', 'Independent agency · Licensed in 16 states + DC'),
    ('Serving Virginia &amp; 10 more states', 'Licensed in 16 states + DC'), ('Serving Virginia &amp; 13 more states plus DC', 'Licensed in 16 states + DC'),
    ('serving Virginia and 10 additional states', 'licensed in 16 states and Washington, DC'),
    ('Health, Medicare &amp; Life in 11 States', 'Medicare, Health, Life &amp; Annuities'),
    ('With Free Local Help in Each of Our 11 States', 'With Free Local Help by State'),
    ('licensed in these states and DC', 'licensed in the 16 states and DC below'),
    ('and a list of every 1,077 county and parish we cover.', 'and a list of the 1,362 counties and parishes we cover.'),
    ('the 11 states below', 'the 16 states and DC below'), ('the 14 states and DC below', 'the 16 states and DC below'),
    ('11 states in all', '16 states and DC in all'), ('all 11 states', 'all 16 states and DC'), ('across 11 states', 'across 16 states and DC'),
    (' and 10 other states', ', 15 other states and DC'), ('all 11 licensed states', 'all 16 licensed states and DC'), ('11 licensed states', '16 licensed states and DC'),
    ('in 11 states', 'in 16 states and DC'), ('11 states', '16 states and DC'), ('14 states and DC', '16 states and DC'),
    ('15 states and Washington, DC', '16 states and Washington, DC'), ('15 states and DC', '16 states and DC'), ('15 states + DC', '16 states + DC'),
    ('15 States + DC', '16 States + DC'), ('14 other states and DC', '15 other states and DC'),
]
stats = {}


def bump(k, n=1):
    if n: stats[k] = stats.get(k, 0) + n


def transform(path, s):
    s, n = FOOT_RX.subn(FOOT_NEW, s); bump('footer state block', n)
    # per-state lists in blog posts
    s, n = LI_COUNTY_WV.subn(lambda m: m.group(0) + ''.join(
        ('\n%s<li><a href="%s">%s</a> · <a href="/%s-counties">county pages</a></li>' % (m.group(1), url(x['slug']), x['name'], x['slug'])) if x['ab'] in COUNTY_N
        else ('\n%s<li><a href="%s">%s</a></li>' % (m.group(1), url(x['slug']), x['name'])) for x in NEW), s); bump('state list (county pages) extended', n)
    s, n = FOOT_COUNTY_RX.subn(lambda m: m.group(1) + ''.join(' &middot; <a href="/%s-counties">%s</a>' % (x['slug'], x['name']) for x in NEW if x['ab'] in COUNTY_N), s); bump('footer county directories extended', n)
    s, n = LI_STUB.subn('', s); bump('placeholder row removed', n)
    if '/south-carolina-medicare-insurance">South Carolina</a>:</strong>' in s and 'georgia-medicare-insurance">Georgia</a>:</strong>' not in s:
        s, n = LI_DOI_SC.subn(lambda m: m.group(1) + m.group(2) + '\n' + m.group(1) + GA_DOI + '\n', s); bump('georgia regulator row restored', n)
    s, n = LI_DOI_WV.subn(lambda m: m.group(0) + ''.join(
        '\n%s<li><strong><a href="%s">%s</a>:</strong> <a href="%s" rel="noopener" target="_blank">%s</a></li>' % (m.group(1), url(x['slug']), x['name'], x['doi_url'], x['doi']) for x in NEW), s)
    bump('state list (regulators) extended', n)
    # schema
    s, n = JSON_LIST_RX.subn(json.dumps([n_ for n_, a, u, new in all16()]), s); bump('schema state array', n)
    if '"name": "West Virginia"' in s or '"name":"West Virginia"' in s:
        if '"name": "Georgia"' not in s and '"name":"Georgia"' not in s and '"@type": "City"' not in s and re.search(r'"name":\s*"Alabama"', s):
            s, n = GA_OBJ_AFTER.subn(lambda m: m.group(1) + ',\n    {"@type": "State", "name": "Georgia"}', s, count=1); bump('schema georgia restored', n)
        if '"District of Columbia"' not in s and re.search(r'"name":\s*"Alabama"', s):
            s, n = WV_OBJ.subn(lambda m: m.group(1) + NEW_OBJS, s, count=1); bump('schema new markets added', n)
    # prose lists (idempotent)
    s = s.replace(PROSE, '\x00P\x00'); s, n = LIST_RX.subn('\x00P\x00', s); bump('prose state list', n); s = s.replace('\x00P\x00', PROSE)
    checklist = 'new-to-medicare-checklist' in path
    if not checklist:
        for a in ('VA, MD, NC, SC, GA, AL, LA, TX, MI, IN and WV', 'VA, MD, NC, SC, AL, LA, TX, MI, IN, WV, DE, DC, KY, PA and TN'):
            if a in s: s = s.replace(a, ABBR16); bump('abbreviation list')
    for a, b in WORDING:
        if a in s: bump('wording: ' + a, s.count(a)); s = s.replace(a, b)
    return s


FAQ = [
    ('Do you charge {res} for help?', 'No. Our help is free to you. Carriers pay us a commission when we place a policy, and your premium is the same whether you use an agent or enroll on your own.'),
    ('Do I need to visit an office?', 'No. Our office is in Tysons, Virginia, and we help {res} by phone or video call. Office visits are by appointment in Northern Virginia only.'),
    ('What plans can I get in {the}?', 'Plan availability varies by county and by carrier. We start with your ZIP code and compare only the plans offered at your address, from the carriers we are appointed with.'),
    ('Is Honorbrook licensed in {the}?', 'Yes. Licensed agent Luay Sadqi (NPN 21370662) holds a license for {the}. You can verify any agent’s license with the {doi}.'),
]


def state_page(tpl, st):
    """Build a state page for a new market from the West Virginia page's shell (head, header, reviews, footer)."""
    name, the, res, slug = st['name'], st['the'], st['res'], st['slug']
    e = html.escape
    title = '%s Medicare Agent | Part C, Medigap &amp; Part D | Honorbrook' % ('Washington DC' if st['ab'] == 'DC' else name)
    desc = 'Independent agency licensed in %s. Compare Medicare Advantage, Medigap and Part D plans. Free to you. Call (571) 354-0146.' % the
    faq = [(q.format(**st), a.format(**st)) for q, a in FAQ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, indent=2, ensure_ascii=False)
    crumb_ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://honorbrook-insurance.com/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": "https://honorbrook-insurance.com" + url(slug)}]}, indent=2)
    agency_ld = json.dumps({"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "url": "https://honorbrook-insurance.com" + url(slug),
        "telephone": "+1-571-354-0146", "image": "https://honorbrook-insurance.com/assets/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA", "postalCode": "22182", "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea" if st['ab'] == 'DC' else "State", "name": name}],
        "description": "Independent Medicare and insurance agency licensed in %s. Help by phone or video, free to the client." % the}, indent=2)
    head = tpl[:tpl.index('</head>')]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'<!-- (?:Breadcrumb|FAQ) schema[^>]*-->\s*', '', head)
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, head)
    head = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + title, head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + desc, head)
    head = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + 'Independent Medicare &amp; insurance help for %s. Free, no-pressure guidance by phone or video.' % res, head)
    head = head.replace('west-virginia-medicare-insurance', url(slug)[1:])
    head += ''.join('<script type="application/ld+json">\n%s\n</script>\n' % x for x in (crumb_ld, faq_ld, agency_ld))
    a = tpl.index('</head>'); b = tpl.index('<section class="page-hero"'); c = tpl.index('<section class="faq"')
    shell_top = tpl[a:b]
    rest = tpl[c:]
    d = rest.index('</section>') + len('</section>')          # end of the FAQ section
    tail = rest[d:]
    k = tail.find('<section class="related"')                  # drop the WV-specific "Keep exploring" cards
    if k >= 0:
        k2 = tail.index('</section>', k) + len('</section>'); tail = tail[:k] + tail[k2:]
    exch = ('%s runs its own health insurance Marketplace, <a href="%s" rel="noopener" target="_blank">%s</a>.' % (the, st['exch_url'], st['exch'])
            if st['exch_own'] else '%s uses the federal Marketplace, <a href="%s" rel="noopener" target="_blank">HealthCare.gov</a>.' % (the, st['exch_url']))
    medicaid = ('%s has adopted the Affordable Care Act Medicaid expansion' if st['expanded'] else '%s has not adopted the Affordable Care Act Medicaid expansion') % the
    if st.get('ship'):
        ship_html = ('<p>%s offers free, unbiased Medicare counseling through the <a href="%s" rel="noopener" target="_blank">%s</a>, run by %s. It does not sell insurance.</p>'
                     % (e(the), st['ship_url'], e(st['ship']), e(st['ship_org'])))
        src_html = 'the %s page, the CMS Marketplace map for plan year 2027, and KFF&rsquo;s status of state Medicaid expansion decisions' % e(st['ship'])
    else:
        ship_html = ('<p>%s has a State Health Insurance Assistance Program (SHIP) that gives free, unbiased Medicare counseling and does not sell insurance. '
                     '<a href="%s" rel="noopener" target="_blank">Medicare.gov</a> links to it.</p>' % (e(the), st['ship_url']))
        src_html = 'Medicare.gov, KFF&rsquo;s state marketplace types for 2027, and KFF&rsquo;s status of state Medicaid expansion decisions'
    main = f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; {e(name)}</div>
    <h1>Medicare &amp; insurance help across <em>{e(the)}</em></h1>
    <p class="lead">Honorbrook is an independent agency licensed in {e(the)}, helping residents compare and choose Medicare, health, and life coverage with free, no-pressure guidance, handled by phone or video.</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="tel:+15713540146">Call (571) 354-0146</a>
      <a class="btn-ghost" href="/#contact">Request a free comparison</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>Insurance help for {e(res)}</h2>
    <p>Whether you are <a href="/turning-65">turning 65</a>, already on Medicare and unsure your plan still fits, or shopping for health or life coverage for your family, Honorbrook is here to make it simple. We are an independent agency, which means we work for you and not for any single insurance company. Our job is to help you find the plan that matches your doctors, your prescriptions and your budget.</p>
    <p>Our help is free to you. Carriers pay us a commission when we place a policy, and your premium is the same whether you work with us or enroll on your own.</p>

    <h2>Coverage we help with in {e(the)}</h2>
    <ul>
      <li><a href="/medicare-advantage">Medicare Advantage</a>: all-in-one Part C plans.</li>
      <li><a href="/medicare-supplement-medigap">Medicare Supplement (Medigap)</a>: see any doctor who accepts Medicare.</li>
      <li><a href="/medicare-part-d">Part D drug plans</a>: we compare plans against your medication list.</li>
      <li><a href="/final-expense-life-insurance">Final expense</a> and <a href="/life-insurance">life insurance</a>.</li>
      <li><a href="/aca-health-insurance">ACA health plans (under 65)</a>, <a href="/ichra">ICHRA</a> and <a href="/group-health-insurance-shop">group coverage</a>.</li>
      <li><a href="/annuities">Annuities</a> and <a href="/retirement-rollover-annuity">retirement rollovers</a>.</li>
    </ul>
    <p>Products, carriers and rules differ by state. We will confirm what is available at your address before recommending anything.</p>

    <h2>Free Medicare counseling in {e(the)}, and how we fit in</h2>
    {ship_html}
    <p>Where Honorbrook adds value is the next step: comparing the specific Medicare Advantage, Medigap and Part D plans offered where you live, checking that your doctors and prescriptions are covered, and helping you enroll and stay on track year after year.</p>

    <div class="callout">
      <strong>Plan availability varies by county.</strong> The Medicare Advantage and drug plans offered at one address are not always offered at the next. We check what is available at your address first, so you only compare plans you can enroll in.
    </div>

    <div class="cta-strip">
      <h3>See your real options side by side</h3>
      <p class="sans">We check that your doctors and prescriptions are covered before you enroll.</p>
      <a class="btn-primary sans" href="/#contact">Get my plan comparison</a>
    </div>

    <h2>Under 65? Health insurance in {e(the)}</h2>
    <p>{exch} {medicaid}, according to KFF&rsquo;s state tracker (November 2026). Marketplace dates and savings rules change each year, so call us for what applies to you, or read our <a href="/aca-health-insurance">guide to ACA health insurance</a>.</p>

    <h2>Your state insurance regulator</h2>
    <p>The <a href="{st['doi_url']}" rel="noopener" target="_blank">{e(st['doi'])}</a> {st.get('doi_role') or 'regulates insurance in %s. It can verify an agent&rsquo;s license and answer consumer questions.' % e(the)}</p>

    <p style="font-size:15.5px;color:var(--muted)"><em>Sources checked November 2026: {src_html}. This page is general information, not insurance advice.</em></p>
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">{e(the)} FAQ</h2>
''' + ''.join('    <details><summary>%s</summary><div class="a">%s</div></details>\n' % (e(q), e(a)) for q, a in faq) + '''  </div>
</section>
'''
    page = head + shell_top + main + tail
    return page.replace('West Virginia Medicare Agent', '%s Medicare Agent' % the)


def patch_finder(js):
    def rep(a, b):
        nonlocal js
        assert a in js, a[:60]; js = js.replace(a, b, 1)
    rep("DE:'Delaware',DC:'District of Columbia',FL:'Florida',", "")
    rep("KY:'Kentucky',ME:'Maine'", "ME:'Maine'"); rep("PA:'Pennsylvania',RI:'Rhode Island'", "RI:'Rhode Island'"); rep("TN:'Tennessee',UT:'Utah'", "UT:'Utah'")
    rep("\n  function load() {", """
  /* Fallback by 3-digit ZIP prefix for ZIP codes missing from the county index (PO-box-only ZIPs), and for DC and Florida, which have no county pages. */
  var NEWST = {DE:['Delaware','delaware',[[197,199]]],DC:['District of Columbia','washington-dc',[[200,200],[202,205],[569,569]]],KY:['Kentucky','kentucky',[[400,427]]],PA:['Pennsylvania','pennsylvania',[[150,196]]],TN:['Tennessee','tennessee',[[370,385]]],FL:['Florida','florida',[[320,339],[341,342],[344,344],[346,347],[349,349]]],
    /* the original 11: fallback for ZIP codes missing from the county index (PO-box-only ZIPs) */
    AL:['Alabama','alabama',[[350,369]]],GA:['Georgia','georgia',[[300,319],[398,399]]],IN:['Indiana','indiana',[[460,479]]],LA:['Louisiana','louisiana',[[700,714]]],MD:['Maryland','maryland',[[206,219]]],MI:['Michigan','michigan',[[480,499]]],NC:['North Carolina','north-carolina',[[270,289]]],SC:['South Carolina','south-carolina',[[290,299]]],TX:['Texas','texas',[[750,799],[885,885]]],VA:['Virginia','virginia',[[201,201],[220,246]]],WV:['West Virginia','west-virginia',[[247,268]]]};
  function newStateByZip(z) { var p = parseInt(z.slice(0, 3), 10); for (var k in NEWST) { var r = NEWST[k][2]; for (var i = 0; i < r.length; i++) { if (p >= r[i][0] && p <= r[i][1]) return NEWST[k]; } } return null; }
  function newStateByQuery(q) { var n = norm(q), up = q.trim().toUpperCase(), five = {DC:1,FL:1}; if (n === 'washington dc' || n === 'dc' || n === 'washington, dc') return NEWST.DC; for (var k in five) { if (k === up || norm(NEWST[k][0]) === n) return NEWST[k]; } return null; }
  function newStateMsg(s) { return '<p class="fd-yes">Yes, we are licensed in ' + (s[0] === 'District of Columbia' ? 'the ' : '') + esc(s[0]) + ' and can help by phone or video, free to you. <a href="tel:+15713540146">Call (571) 354-0146</a> or <a href="/#contact">request a callback</a>.</p><ul class="fd-list"><li><a href="/' + s[1] + '-medicare-insurance"><strong>' + esc(s[0]) + '</strong> Medicare and insurance help</a></li></ul>'; }

  function load() {""")
    rep("if (ci === undefined) return { html: '<p class=\"fd-no\">We did not find ZIP ' + esc(q) + ' in the 11 states we serve.",
        "if (ci === undefined) { var nz = newStateByZip(q); if (nz) return { html: newStateMsg(nz), type: 'zip-new' }; }\n      if (ci === undefined) return { html: '<p class=\"fd-no\">We did not find ZIP ' + esc(q) + ' in the " + COUNT + " we serve.")
    rep("    var os = otherState(q);", "    var nsq = newStateByQuery(q);\n    if (nsq) return { html: newStateMsg(nsq), type: 'state-new' };\n    var os = otherState(q);")
    rep("Honorbrook is not licensed in ' + esc(os) + ' yet, so we cannot help with plans there. We serve Virginia, Maryland, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan, Indiana and West Virginia.",
        "Honorbrook is not licensed in ' + esc(os) + ' yet, so we cannot help with plans there. We serve Virginia, Maryland, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan, Indiana, West Virginia, Delaware, the District of Columbia, Kentucky, Pennsylvania, Tennessee and Florida.")
    rep("We serve 11 states: VA, MD, NC, SC, GA, AL, LA, TX, MI, IN and WV.", "We serve " + COUNT + ": " + ABBR16 + ".")
    rep("These matches are in the 11 states we serve:", "These matches are in the " + COUNT + " we serve:")
    return js


def apply(site):
    stats.clear()
    files = [f for f in glob.glob(os.path.join(site, '**', '*'), recursive=True)
             if os.path.isfile(f) and f.endswith(('.html', '.txt')) and '/assets/video' not in f]
    for f in files:
        s = open(f, encoding='utf-8', errors='ignore').read(); t = transform(f, s)
        if t != s: open(f, 'w', encoding='utf-8').write(t); bump('files changed')
    # new state pages
    tpl = open(os.path.join(site, 'west-virginia-medicare-insurance.html'), encoding='utf-8').read()
    for st in NEW:
        page = state_page(tpl, st)
        if st['ab'] in COUNTY_N:
            add = '    <p>See residents age 65 and older, Medicare Advantage enrollment and local hospitals for every %s county in our <a href="/%s-counties">%s county directory</a>.</p>\n' % (st['name'], st['slug'], st['name'])
            i = page.index('<div class="cta-strip">'); i = page.rindex('\n', 0, i) + 1
            page = page[:i] + add + page[i:]; bump('state pages linked to county directory')
        open(os.path.join(site, url(st['slug'])[1:] + '.html'), 'w', encoding='utf-8').write(page); bump('new state pages')
    # find-your-area table rows
    p = os.path.join(site, 'find-your-area.html'); s = open(p, encoding='utf-8').read()
    todo = [x for x in NEW if '/%s-medicare-insurance">Medicare' % x['slug'] not in s]
    if todo:
        rows = ''.join(
            ('          <tr><td><strong>%s</strong></td><td><a href="%s">Medicare</a></td><td>By phone or video</td><td><a href="/%s-counties">All %d counties</a></td></tr>\n' % (x['name'], url(x['slug']), x['slug'], COUNTY_N[x['ab']])) if x['ab'] in COUNTY_N
            else ('          <tr><td><strong>%s</strong></td><td><a href="%s">Medicare</a></td><td colspan="2">Help by phone or video: <a href="tel:+15713540146">(571) 354-0146</a></td></tr>\n' % (x['name'], url(x['slug']))) for x in todo)
        a = '        </tbody>\n      </table>'; assert a in s
        open(p, 'w', encoding='utf-8').write(s.replace(a, rows + a, 1)); bump('find-your-area rows', len(todo))
    # llms.txt
    p = os.path.join(site, 'llms.txt'); s = open(p, encoding='utf-8').read()
    wv = '- [West Virginia](https://honorbrook-insurance.com/west-virginia-medicare-insurance)'
    if wv in s:
        lines = s.split('\n'); k = lines.index(wv)
        for x in NEW:
            ln = '- [%s](https://honorbrook-insurance.com%s)' % (x['name'], url(x['slug']))
            if ln in lines: k = lines.index(ln)
            else: lines.insert(k + 1, ln); k += 1; bump('llms.txt links')
        open(p, 'w', encoding='utf-8').write('\n'.join(lines))
    # sitemap
    p = os.path.join(site, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    add = ''.join('  <url><loc>https://honorbrook-insurance.com%s</loc><lastmod>2026-11-21</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n' % url(x['slug'])
                  for x in NEW if 'honorbrook-insurance.com%s</loc>' % url(x['slug']) not in s)
    if add:
        s = s.replace('</urlset>', add + '</urlset>'); open(p, 'w', encoding='utf-8').write(s); bump('sitemap urls', add.count('<url>'))
    # area finder
    p = os.path.join(site, 'assets', 'find.js'); js = open(p, encoding='utf-8').read()
    if 'NEWST' not in js: open(p, 'w', encoding='utf-8').write(patch_finder(js)); bump('finder patched')
    return dict(stats)
