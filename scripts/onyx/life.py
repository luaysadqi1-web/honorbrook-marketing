"""Honorbrook Onyx: life insurance on every area page, and one life page per state.

Owner, Nov 20 2026: "We need LIFE LEADS IN EVERY STATE IN EVERY COUNTY BOOKED IN INTEGRITY".

Why it is built this way (research notes: staging/research_notes/, report: staging/reports/):
- Life insurance is not priced or offered by county. A separate life page per county would be the doorway pattern in Google's spam
  policy ("pages targeted at specific regions or cities that funnel users to one page"), and would put the Medicare county pages
  at risk. Every county is covered instead by a life section, with its own Life booking step, on the county page that exists.
- People do search final expense, burial insurance and mortgage protection by state, so each of the 16 markets gets one life page.
- State guaranty association limits are NOT used anywhere here: most states bar agents from using the association to sell
  (for example Virginia Code 38.2-1715).
Facts used: Census Bureau 2023 county population estimates (scripts/county_data/county_stats.json) and each state's insurance
regulator, as already cited on the area pages. No prices, no carrier names.
"""
import html
import json
import os
import re
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'county_data')
CENSUS_URL = 'https://www.census.gov/data/datasets/time-series/demo/popest/2020s-counties-detail.html'
CHILD = '/blog/should-i-buy-life-insurance-for-my-child-gerber-style-whole-life'
DATE = '2026-11-20'

# name, abbreviation, page slug, name in running text, residents, regulator (name and link as cited on the area pages), county word
STATES = [
    ('Virginia', 'VA', 'virginia', 'Virginia', 'Virginia Bureau of Insurance', 'https://scc.virginia.gov/pages/Bureau-of-Insurance', 'county and city'),
    ('Maryland', 'MD', 'maryland', 'Maryland', 'Maryland Insurance Administration', 'https://insurance.maryland.gov/', 'county'),
    ('West Virginia', 'WV', 'west-virginia', 'West Virginia', 'West Virginia Offices of the Insurance Commissioner', 'https://www.wvinsurance.gov/', 'county'),
    ('Georgia', 'GA', 'georgia', 'Georgia', 'Georgia Office of Insurance and Safety Fire Commissioner', 'https://oci.georgia.gov/', 'county'),
    ('North Carolina', 'NC', 'north-carolina', 'North Carolina', 'North Carolina Department of Insurance', 'https://www.ncdoi.gov/', 'county'),
    ('South Carolina', 'SC', 'south-carolina', 'South Carolina', 'South Carolina Department of Insurance', 'https://doi.sc.gov/', 'county'),
    ('Texas', 'TX', 'texas', 'Texas', 'Texas Department of Insurance', 'https://www.tdi.texas.gov/', 'county'),
    ('Louisiana', 'LA', 'louisiana', 'Louisiana', 'Louisiana Department of Insurance', 'https://ldi.la.gov/', 'parish'),
    ('Alabama', 'AL', 'alabama', 'Alabama', 'Alabama Department of Insurance', 'https://aldoi.gov/', 'county'),
    ('Michigan', 'MI', 'michigan', 'Michigan', 'Michigan Department of Insurance and Financial Services', 'https://www.michigan.gov/difs', 'county'),
    ('Indiana', 'IN', 'indiana', 'Indiana', 'Indiana Department of Insurance', 'https://www.in.gov/idoi/', 'county'),
    ('Delaware', 'DE', 'delaware', 'Delaware', 'Delaware Department of Insurance', 'https://insurance.delaware.gov/', 'county'),
    ('District of Columbia', 'DC', 'washington-dc', 'Washington, DC', 'DC Department of Insurance, Securities and Banking', 'https://disb.dc.gov/', ''),
    ('Kentucky', 'KY', 'kentucky', 'Kentucky', 'Kentucky Department of Insurance', 'https://insurance.ky.gov/', 'county'),
    ('Pennsylvania', 'PA', 'pennsylvania', 'Pennsylvania', 'Pennsylvania Insurance Department', 'https://www.pa.gov/agencies/insurance', 'county'),
    ('Tennessee', 'TN', 'tennessee', 'Tennessee', 'Tennessee Department of Commerce and Insurance', 'https://www.tn.gov/commerce/insurance.html', 'county'),
    ('Florida', 'FL', 'florida', 'Florida', 'Florida Department of Financial Services', 'https://www.myfloridacfo.com/', 'county'),
]
BY_NAME = {s[0]: s for s in STATES}
BY_SLUG = {s[2]: s for s in STATES}
_cache = {}


def life_url(state_slug): return '/%s-life-insurance' % state_slug


def data():
    """Census rows by page slug, and totals by state name."""
    if not _cache:
        cen = json.load(open(os.path.join(DATA, 'county_stats.json'), encoding='utf-8'))['census']
        sm = json.load(open(os.path.join(DATA, 'slugmap.json'), encoding='utf-8'))
        by_slug, tot, counties = {}, {}, {}
        for fips, slug in sm.items():
            c = cen.get(fips)
            if not c: continue
            by_slug[slug] = c
            t = tot.setdefault(c['state'], dict(pop=0, p65=0, a=0))
            t['pop'] += c['pop']; t['p65'] += c['p65']; t['a'] += c['bands']['AGE6064_TOT']
            counties.setdefault(c['state'], []).append((c['name'], slug))
        _cache.update(by_slug=by_slug, tot=tot, counties={k: sorted(v) for k, v in counties.items()})
    return _cache


def _n(x): return '{:,}'.format(int(x))


def _pick(slug, options): return options[zlib.crc32(slug.encode('utf-8')) % len(options)]


def _place(s):
    """(place name, state name or None) from the page's own heading."""
    m = re.search(r'<h1>Medicare &amp; insurance help in <em>(.*?)</em>, ([^<]+?)\s*</h1>', s, flags=re.S)
    if m: return html.unescape(m.group(1).strip()), html.unescape(m.group(2).strip())
    m = re.search(r'<h1>Medicare &amp; insurance help across <em>(.*?)</em>\s*</h1>', s, flags=re.S)
    if m: return html.unescape(m.group(1).strip()), None
    return None, None


_L = {'fe': '<a href="/final-expense-life-insurance">final expense</a>', 'term': '<a href="/term-life-insurance">term life</a>',
      'mp': '<a href="/mortgage-protection-insurance">mortgage protection</a>', 'wl': '<a href="/whole-life-insurance">whole life</a>',
      'iul': '<a href="/indexed-universal-life">indexed universal life</a>'}
CTA = ('<p class="hb-life hb-life-cta sans"><a class="btn-primary" href="%s" target="_blank" rel="noopener">Schedule a life insurance review</a>'
       '<span>On PlanEnroll, choose <strong>Life</strong> as the meeting type.</span></p>')


def section(slug, s, book):
    """The life insurance section for one area page ('' if the page is not an area page we can read).
    Kept short on purpose: the county figures are the part that differs from page to page, and the product explanations live on
    the product pages and the state life page. A long identical block on 1,385 pages would make the pages too alike."""
    place, state = _place(s)
    if not place: return ''
    d = data(); e = html.escape
    fact = ''; order = ['fe', 'term', 'mp', 'wl', 'iul']
    if state is None:                                   # a state page, or a region page such as Northern Virginia
        st = BY_NAME.get(place) or next((x for x in STATES if x[3] == place), None)
        region = st is None
        if region: st = next((x for x in STATES if place.endswith(x[0])), None)
        if not st: return ''
        state = st[0]; t = None if region else d['tot'].get(state)
        if t:
            fact = ('%s has %s residents. %s of them are 65 or older (%.1f%%), and another %s are between 60 and 64. '
                    % (e(st[3]), _n(t['pop']), _n(t['p65']), 100.0 * t['p65'] / t['pop'], _n(t['a'])))
    else:
        st = BY_NAME.get(state)
        if not st: return ''
        c = d['by_slug'].get(slug); t = d['tot'].get(state)
        if c and t:
            sh = 100.0 * c['p65'] / c['pop']; ss = 100.0 * t['p65'] / t['pop']
            v = dict(place=e(place), pop=_n(c['pop']), p65=_n(c['p65']), sh='%.1f' % sh, a=_n(c['bands']['AGE6064_TOT']), st=e(st[3]), ss='%.1f' % ss)
            fact = _pick(slug, [
                'In %(place)s, %(p65)s of %(pop)s residents are 65 or older (%(sh)s%%), and %(a)s more are 60 to 64. ',
                '%(place)s has %(pop)s residents. %(p65)s of them are 65 or older (%(sh)s%%), and another %(a)s are between 60 and 64. ',
                'Of the %(pop)s people who live in %(place)s, %(p65)s are 65 or older (%(sh)s%%) and %(a)s are 60 to 64. ',
                'Census estimates count %(pop)s residents in %(place)s, including %(p65)s who are 65 or older (%(sh)s%%) and %(a)s who are 60 to 64. ',
                '%(p65)s people in %(place)s are 65 or older, which is %(sh)s%% of its %(pop)s residents, and %(a)s are 60 to 64. ']) % v
            if sh - ss >= 2:
                fact += _pick(slug + 't', ['That is a higher share of older residents than %(st)s as a whole (%(ss)s%%). ',
                                           'Across %(st)s the share 65 or older is %(ss)s%%, so this is an older population than the state&rsquo;s. ']) % v
            elif ss - sh >= 2:
                fact += _pick(slug + 't', ['That is a lower share than %(st)s as a whole (%(ss)s%%), so the population here is younger than the state&rsquo;s. ',
                                           'Across %(st)s the share 65 or older is %(ss)s%%, so this is a younger population than the state&rsquo;s. ']) % v
                order = ['term', 'mp', 'fe', 'wl', 'iul']
            else:
                fact += _pick(slug + 't', ['That is close to the share for %(st)s as a whole (%(ss)s%%). ', 'The share for %(st)s as a whole is about the same, %(ss)s%%. ']) % v
    the = st[3]
    who = 'residents of %s' % e(place) if place != the else '%s residents' % e('DC' if st[1] == 'DC' else the)
    links = [_L[k] for k in order]
    src = ('Source: <a href="%s" rel="noopener" target="_blank">Census Bureau 2023 population estimates</a>. ' % CENSUS_URL) if fact else ''
    return ('    <h2 id="life">Life insurance in %s</h2>\n'
            '    <p>%sHonorbrook is licensed in %s and helps %s with %s and %s, by phone or video call. Life insurance is its own meeting, separate from a Medicare review.</p>\n'
            '    %s\n'
            '    <p class="sans" style="font-size:14px;color:var(--muted)">%sMore: <a href="%s">life insurance in %s</a>.</p>\n\n'
            % (e(place), fact, e(the), who, ', '.join(links[:-1]), links[-1], CTA % book, src, life_url(st[2]), e(the)))


def add_section(slug, s, book):
    """Put the life section on an area page: before the list of coverage on county pages, at the end of the text on the others."""
    if 'id="life"' in s: return s
    sec = section(slug, s, book)
    if not sec: return s
    m = re.search(r'\n[ \t]*<h2>Coverage we offer [^<]* residents</h2>', s)
    if m: i = m.start() + 1; return s[:i] + sec + s[i:]
    return re.sub(r'</div>\s*</article>', lambda mm: sec + '  ' + mm.group(0), s, count=1)


def state_links(e=html.escape):
    """One paragraph linking the 16 state life pages (for the life and final expense product pages)."""
    return ('    <h2>Life insurance by state</h2>\n    <p>Honorbrook is licensed in 16 states and Washington, DC. Each page explains how a review works where you live and who regulates insurance there: '
            + ', '.join('<a href="%s">%s</a>' % (life_url(st[2]), e(st[3])) for st in STATES) + '.</p>\n')


FAQ = [
    ('Do I need to visit an office to buy life insurance in {the}?',
     'No. Our office is in Tysons, Virginia, and we help {res} by phone or video call. Office visits are by appointment in Northern Virginia only.'),
    ('Is Honorbrook licensed in {the}?',
     'Yes. Licensed agent Luay Sadqi (NPN 21370662) holds a license for {the}. You can verify any agent’s license with the {doi}.'),
    ('Will I need a medical exam?',
     'It depends on the policy. Many final expense policies ask health questions instead of requiring an exam. Larger term and permanent policies often involve a health interview, a records check or an exam. The insurer decides what it needs.'),
    ('What does a life insurance review cost?',
     'Nothing. You do not pay us a fee. Insurers pay us a commission when a policy is placed.'),
    ('Which meeting type do I choose when I schedule?',
     'Choose Life. PlanEnroll offers Life, Health and Annuities. Medicare is a Health meeting, and retirement income is an Annuities meeting.'),
]


def state_page(tpl, st, book, block):
    """A 'Life insurance in <state>' page built on the West Virginia Medicare page's shell (head, header, reviews, footer)."""
    name, ab, slug, the, doi, doi_url, cword = st
    res = 'DC residents' if ab == 'DC' else '%s residents' % the
    e = html.escape; d = data(); t = d['tot'].get(name); page_url = life_url(slug)
    title = 'Life Insurance in %s | Final Expense, Term &amp; IUL' % e(the)
    desc = 'Independent agency licensed in %s. Compare final expense, term, whole life and indexed universal life by phone or video. Schedule a life insurance review.' % the
    faq = [(q.format(the=the, res=res, doi=doi), a.format(the=the, res=res, doi=doi)) for q, a in FAQ]
    ld = [json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://honorbrook-insurance.com/"},
              {"@type": "ListItem", "position": 2, "name": "Life insurance", "item": "https://honorbrook-insurance.com/life-insurance"},
              {"@type": "ListItem", "position": 3, "name": name, "item": "https://honorbrook-insurance.com" + page_url}]}, indent=2),
          json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, indent=2, ensure_ascii=False),
          json.dumps({"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "url": "https://honorbrook-insurance.com" + page_url,
              "telephone": "+1-571-354-0146", "image": "https://honorbrook-insurance.com/assets/og-image.jpg",
              "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA", "postalCode": "22182", "addressCountry": "US"},
              "areaServed": [{"@type": "AdministrativeArea" if ab == 'DC' else "State", "name": name}],
              "description": "Independent insurance agency licensed in %s. Life insurance reviews by phone or video." % the}, indent=2)]
    head = tpl[:tpl.index('</head>')]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'<!-- (?:Breadcrumb|FAQ) schema[^>]*-->\s*', '', head)
    head = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % title, head, flags=re.S)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(r'(<meta %s content=")[^"]*' % attr, lambda m: m.group(1) + e(desc), head)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(r'(<meta %s content=")[^"]*' % attr, lambda m: m.group(1) + title, head)
    head = head.replace('west-virginia-medicare-insurance', page_url[1:])
    head += ''.join('<script type="application/ld+json">\n%s\n</script>\n' % x for x in ld)
    a = tpl.index('</head>'); b = tpl.index('<section class="page-hero"'); c = tpl.index('<section class="faq"')
    shell_top = tpl[a:b]; rest = tpl[c:]
    tail = rest[rest.index('</section>') + len('</section>'):]
    k = tail.find('<section class="related"')                  # drop the West Virginia "Keep exploring" cards
    if k >= 0: tail = tail[:k] + tail[tail.index('</section>', k) + len('</section>'):]
    facts = ''
    if t:
        facts = ('%s has %s residents. %s of them are 65 or older (%.1f%%), and another %s are between 60 and 64, according to '
                 '<a href="%s" rel="noopener" target="_blank">Census Bureau 2023 population estimates</a>. '
                 % (e(the), _n(t['pop']), _n(t['p65']), 100.0 * t['p65'] / t['pop'], _n(t['a']), CENSUS_URL))
    counties = d['counties'].get(name, [])
    county_html = ''
    if counties:
        county_html = ('    <h2>Life insurance help in every %s %s</h2>\n'
                       '    <p>Each local page has population facts for that %s and its own life insurance section and booking step.</p>\n'
                       '    <div class="hb-places"><details>\n      <summary class="sans">Show all %d places in %s</summary>\n      <ul class="hb-cols sans">\n%s      </ul>\n    </details></div>\n\n'
                       % (e(name), cword, cword.split(' and ')[0], len(counties), e(the),
                          ''.join('        <li><a href="/%s#life">%s</a></li>\n' % (sl, e(nm)) for nm, sl in counties)))
    main = '''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/life-insurance">Life insurance</a> &rsaquo; %(name)s</div>
    <h1>Life insurance in <em>%(the)s</em></h1>
    <p class="lead">Honorbrook Insurance is an independent agency licensed in %(the)s. We help %(res)s compare final expense, term, whole life and indexed universal life from more than one insurer, by phone or video call. You do not pay us a fee.</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="%(book)s" target="_blank" rel="noopener">Schedule an appointment</a>
      <a class="btn-ghost" href="tel:+15713540146">Call (571) 354-0146</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>Life insurance for %(res)s</h2>
    <p>Life insurance pays a sum to the people you name when you die. The right kind depends on what the money has to do: pay for a funeral, replace a paycheck while children are at home, clear a mortgage, or last your whole life. %(facts)sWe ask what you need the coverage to do, compare what several insurers offer for your age and health, and explain the differences in plain English.</p>
    <p>Insurers pay us a commission when a policy is placed. The insurer, not the agent, decides whether you are approved and what you pay.</p>

    %(block)s

    <h2>Types of life insurance we help with in %(the)s</h2>
    <h3>Final expense and burial insurance</h3>
    <p>Final expense insurance, also called burial insurance, is a smaller whole life policy meant to pay for a funeral and last bills. The premium stays level and the coverage does not end while premiums are paid. Many policies ask health questions instead of requiring a medical exam. Some accept every applicant in an age range and pay a reduced benefit if death from illness happens in the first years, so it matters which kind you are offered. <a href="/final-expense-life-insurance">How final expense insurance works</a>.</p>
    <h3>Term life</h3>
    <p>Term life covers a set number of years. If you die during the term, the insurer pays the benefit to the people you name. If you outlive the term, the coverage ends. It is often chosen while a household depends on a paycheck. <a href="/term-life-insurance">How term life works</a>.</p>
    <h3>Mortgage protection</h3>
    <p>Mortgage protection is life insurance sized to a home loan. It is usually a term policy that you own, with the benefit paid to the person you name, not to the lender. It is different from the mortgage insurance a lender may require. <a href="/mortgage-protection-insurance">How mortgage protection works</a>.</p>
    <h3>Whole life</h3>
    <p>Whole life is permanent coverage with a level premium and a cash value that grows on a schedule written into the policy. It costs more than term for the same benefit. <a href="/whole-life-insurance">How whole life works</a>.</p>
    <h3>Indexed universal life (IUL)</h3>
    <p>Indexed universal life is permanent coverage with a cash value account. Interest is credited by the movement of a market index, within a cap and a floor set by the insurer. You are not invested in the index, policy charges can change, and loans reduce the death benefit. It is life insurance first, not an investment. <a href="/indexed-universal-life">How IUL works, and who it fits</a>.</p>
    <h3>Coverage on a child or grandchild</h3>
    <p>A small whole life policy on a child can suit some families once the parents are covered. <a href="%(child)s">When it fits and when it does not</a>.</p>

    <h2>How a review works when you live in %(the)s</h2>
    <ol>
      <li>Schedule a life insurance review on PlanEnroll and choose Life as the meeting type. You can also call or text us.</li>
      <li>We ask what the coverage needs to do, about your health and tobacco use, and what premium is comfortable.</li>
      <li>We compare policies from the insurers we are appointed with in %(the)s and explain how they differ.</li>
      <li>If you apply, the insurer reviews the application. Depending on the policy it may ask health questions, check records or ask for an exam.</li>
      <li>When the policy is issued we go through it with you, and we are here when something in your life changes.</li>
    </ol>

    <h2>Who regulates life insurance in %(the)s</h2>
    <p>The <a href="%(doi_url)s" rel="noopener" target="_blank">%(doi)s</a> regulates insurers and agents in %(the)s. It can verify an agent&rsquo;s license and answer consumer questions. Licensed agent Luay Sadqi (NPN 21370662) holds a license for %(the)s.</p>

%(county_html)s    <p style="font-size:15.5px;color:var(--muted)"><em>Sources checked November 2026: Census Bureau 2023 population estimates and the %(doi)s. This page is general information, not insurance advice.</em></p>
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">Life insurance in %(the)s: questions</h2>
''' % dict(name=e(name), the=e(the), res=e(res), book=book, facts=facts, block=block.strip(), child=CHILD, doi=e(doi), doi_url=doi_url, county_html=county_html)
    main += ''.join('    <details><summary>%s</summary><div class="a">%s</div></details>\n' % (e(q), e(a)) for q, a in faq) + '  </div>\n</section>\n'
    return head + shell_top + main + tail


def write_state_pages(site, book, block):
    """Write the 16 state life pages into the build, and list them in the sitemap and llms.txt. Returns how many were written."""
    tpl = open(os.path.join(site, 'west-virginia-medicare-insurance.html'), encoding='utf-8').read()
    for st in STATES:
        open(os.path.join(site, life_url(st[2])[1:] + '.html'), 'w', encoding='utf-8').write(state_page(tpl, st, book, block))
    p = os.path.join(site, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    if life_url('virginia') not in s:
        add = ''.join('  <url><loc>https://honorbrook-insurance.com%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
                      % (life_url(st[2]), DATE) for st in STATES)
        open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', add + '</urlset>'))
    p = os.path.join(site, 'llms.txt')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if life_url('virginia') not in s:
            s = s.rstrip('\n') + '\n\n## Life insurance by state\n' + ''.join('- [Life insurance in %s](https://honorbrook-insurance.com%s)\n' % (st[3], life_url(st[2])) for st in STATES)
            open(p, 'w', encoding='utf-8').write(s)
    return len(STATES)
