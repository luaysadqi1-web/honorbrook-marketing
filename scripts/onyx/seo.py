"""Honorbrook Onyx: search fixes from the Nov 24, 2026 audit of the SEO scorecard. Runs after claims.apply(), on the final text.

- Titles: 60 characters or fewer (Google cuts longer ones). County pages drop " Insurance" from the brand suffix; the 17 state
  hubs, 11 tool and product pages and 10 posts get shorter titles.
- Descriptions: 92 county pages ended in a cut-off old number "(571)..."; that is removed. Descriptions over 160 characters
  are trimmed (filler first, then the last sentence); a few key pages get a rewritten one.
- Office: the site, schema and listings say Tysons; 10 Northern Virginia pages said the office is in Vienna. Same office
  (8609 Westwood Center Dr, Suite 110, 22182); the wording now says Tysons everywhere.
- Schema: about.html Person areaServed listed 11 states (now 17); the state change-plan posts and the Virginia ACA post
  named every state in contentLocation (now their own state); 4 Northern Virginia pages had no agency schema.
- Links: each state's "when can I change my Medicare plan" post was linked from no hub or county page; /turning-65 did not link
  the "keep my ACA plan at 65" post; the homepage linked Fairfax County only in the footer.
- Finish: old redirect stubs removed so the 301s in netlify.toml apply; Part D page gets the standard footer; the area finder
  shows the ACA link only where an ACA page exists; llms.txt lists the ACA state pages and county directories; sitemap lastmod.
"""
import glob
import html
import json
import os
import re

STATES = {'alabama': 'Alabama', 'georgia': 'Georgia', 'indiana': 'Indiana', 'louisiana': 'Louisiana', 'maryland': 'Maryland', 'michigan': 'Michigan',
          'north-carolina': 'North Carolina', 'south-carolina': 'South Carolina', 'texas': 'Texas', 'virginia': 'Virginia', 'west-virginia': 'West Virginia',
          'delaware': 'Delaware', 'washington-dc': 'Washington, DC', 'kentucky': 'Kentucky', 'pennsylvania': 'Pennsylvania', 'tennessee': 'Tennessee', 'florida': 'Florida'}
ABBR = {'alabama': 'al', 'georgia': 'ga', 'indiana': 'in', 'louisiana': 'la', 'maryland': 'md', 'michigan': 'mi', 'north-carolina': 'nc', 'south-carolina': 'sc',
        'texas': 'tx', 'virginia': 'va', 'west-virginia': 'wv', 'delaware': 'de', 'kentucky': 'ky', 'pennsylvania': 'pa', 'tennessee': 'tn', 'florida': 'fl'}
CHANGE_POST = 'when-can-i-change-my-medicare-plan-in-%s'
# Virginia county and independent-city pages named without the -county-va pattern
VA_COUNTY_LEVEL = {'fairfax-medicare-insurance', 'arlington-medicare-insurance', 'alexandria-medicare-insurance', 'falls-church-medicare-insurance',
                   'virginia-beach-va-medicare-insurance'}
READ_RX = re.compile(r'(<h2>(?:Read next|Plain-English Medicare answers|Medicare guides for [^<]*)</h2>\s*<ul>)')

TITLES = {
    'life-insurance': 'Term, Whole, IUL &amp; Final Expense Life Insurance | Honorbrook',
    'dental-vision-hearing-insurance': 'Dental, Vision &amp; Hearing Insurance Plans | Honorbrook',
    'aca-subsidy-calculator': 'ACA Subsidy Calculator: 2027 Tax Credit | Honorbrook',
    'life-insurance-calculator': 'Life Insurance Calculator: How Much Do I Need? | Honorbrook',
    'retirement-rollover-annuity': 'Rollover to an Annuity: Every Account Type | Honorbrook',
    'disability-insurance': 'Disability Insurance: Income Protection | Honorbrook',
    'lost-health-coverage': 'Lost Health Coverage? Your 60-Day Window | Honorbrook',
    'medicare-cost-calculator': 'Medicare Cost Calculator: Your 2026 Costs | Honorbrook',
    'find-your-area': 'Find Help by ZIP, City, County or State | Honorbrook',
    'turning-65': 'Turning 65? Get Your Medicare Timing Right | Honorbrook',
    'long-term-care-insurance': 'Long-Term Care Insurance: Traditional &amp; Hybrid | Honorbrook',
    'blog/why-did-my-medicare-advantage-plan-drop-my-doctor-or-drug': 'Why Did My Medicare Advantage Plan Drop My Doctor or Drug?',
    'blog/new-to-medicare-checklist-virginia-and-10-more-states': 'New to Medicare? A Step-by-Step Checklist | Honorbrook',
    'blog/does-medicare-cover-dental-vision-hearing': 'Does Medicare Cover Dental, Vision and Hearing?',
    'blog/when-can-you-switch-medicare-plans': 'When Can You Change Medicare Plans? 2026–2027 Dates',
    'blog/small-business-health-insurance-group-plans-vs-shop-vs-ichra': 'Small Business Health Insurance: Group vs. SHOP vs. ICHRA',
    'blog/do-i-need-disability-insurance': 'Do I Need Disability Insurance? What It Covers',
    'blog/what-happens-if-i-do-nothing-during-medicare-open-enrollment': 'Do Nothing in Medicare Open Enrollment? Plans Usually Renew',
}
HUB_TITLE = re.compile(r'^(.+?) Medicare (?:&amp;|&) Insurance Broker — Free Local Help \| Honorbrook(?: Insurance)?$|^(.+?) Medicare Agent \| Part C, Medigap (?:&amp;|&) Part D(?: Plans)? \| Honorbrook(?: Insurance)?$')

DESCS = {
    'index': 'Independent agency comparing Medicare, ACA health, life insurance and annuities from 90+ carriers. Licensed in 16 states and DC. Call (301) 615-8289.',
    'turning-65': 'Your Medicare Initial Enrollment Period is seven months, and the Part B late penalty can last as long as you have Part B. Free timing review by phone or video.',
    'fairfax-medicare-insurance': 'Independent Medicare agent for Fairfax County, VA. Compare 2027 Medicare Advantage, Medigap and Part D at our Tysons office or by phone. (301) 615-8289.',
    'final-expense-life-insurance': 'Final expense whole life insurance for a funeral and last bills. Many plans ask health questions instead of an exam. An independent agent compares carriers.',
    'find-your-area': 'Search by ZIP code, city, county or state to see whether Honorbrook can help, and find local Medicare and ACA information. Licensed in 16 states and DC.',
    'ichra': 'ICHRA, now also called a CHOICE Arrangement, lets employers fund health coverage tax-free while employees pick their own plan. A plain-English guide.',
    'lost-health-coverage': 'Lost job-based coverage or Medicaid? You may have a 60-day Special Enrollment Period, counted from the day coverage ended. Help from a licensed agent.',
    'long-term-care-insurance': 'What long-term care insurance covers, traditional vs. hybrid policies, and how a state Partnership program can protect assets from Medicaid spend-down.',
    'group-health-insurance-shop': 'Group health coverage and SHOP marketplace plans for small businesses, including tax credit eligibility. Free quotes, no obligation.',
    'blog/new-to-medicare-checklist-virginia-and-10-more-states': 'New to Medicare or just moved? A step-by-step checklist for enrollment windows, penalties and plan choices, with help for each state we serve.',
    'blog/1035-exchange-annuity-the-180-day-rule-explained': 'A 1035 exchange moves one annuity into another without immediate tax. How the IRS 180-day rule works for partial exchanges, and what to check.',
    'blog/what-is-the-medicare-part-d-late-enrollment-penalty': 'The Part D late penalty is 1% of the national base premium for each month without drug coverage. How the 63-day rule works and how to avoid it.',
    'blog/why-did-my-medicare-advantage-plan-drop-my-doctor-or-drug': 'Plans change networks and drug lists every year. Check your Annual Notice of Change, ask for a transition fill or exception, and compare plans Oct 15–Dec 7.',
    'blog/how-to-read-medicare-annual-notice-of-change': 'Your Annual Notice of Change (ANOC) lists what your Medicare Advantage or Part D plan changes on January 1, 2027. What to read first, and how to compare.',
    'blog/what-happens-if-i-do-nothing-during-medicare-open-enrollment': 'If you do nothing during Medicare open enrollment, your plan usually renews if it is still offered. Premiums, copays and drug lists can change on January 1.',
}
TRIM = [(' Free, no pressure.', ''), (' Free to you.', ''), (' — no cost, no obligation', ''), ('Call (301) 615-8289.', '(301) 615-8289.'),
        (' by phone or video', ''), ('indexed universal life', 'IUL'), (' Free quotes, no obligation.', ''), (', when you can take money out, and the traps first', ' and when you can take money out'),
        ('lifetime monthly pension payments', 'monthly pension payments'), ('how Virginia families plan for it', 'how families plan for it'),
        ('Dec 7, 2026.', 'Dec 7.'), ('your Medicare Advantage or Medigap plan in', 'your Medicare plan in'), ('Missed or unsure about the ACA', 'Missed the ACA')]

# Office wording on the Northern Virginia pages (same office as the schema: 8609 Westwood Center Dr, Suite 110, Tysons, VA 22182)
NOVA = ['alexandria', 'arlington', 'falls-church', 'fairfax', 'herndon', 'mclean', 'oakton', 'reston', 'tysons', 'vienna', 'virginia']
TYSONS_FIRST = [
    ('Honorbrook is an independent insurance agency based just minutes from Tysons, with our office nearby in Vienna.', 'Honorbrook is an independent insurance agency based right here in Tysons.'),
    ('our office is just minutes away in Vienna', 'our office is right here in Tysons'),
    ("Our help is always free, and we're here year-round, right nearby in Vienna, to answer", "Our help is always free, and we're here year-round, right here in Tysons, to answer"),
    ('By appointment, our home office is right here in Vienna at 8609 Westwood Center Drive', 'By appointment, our office is minutes away in Tysons at 8609 Westwood Center Drive'),
    ("We're an independent agency based right here in Vienna — our home office sits on Westwood Center Drive, just minutes from Tysons.",
     "We're an independent agency based minutes away in Tysons, on Westwood Center Drive."),
    ("Vienna is our home town. Honorbrook's home office is located right here at 8609 Westwood Center Drive — so when we say we're local, we mean it literally.",
     'Our office is minutes away in Tysons, at 8609 Westwood Center Drive, Suite 110.'),
    ('Vienna is our home town.', 'Our office is minutes away in Tysons.'),
    ('Living and working in the Town of Vienna, we know this part of Fairfax County well', 'From our office minutes away in Tysons, we know this part of Fairfax County well'),
    ('Because we work and live nearby in Vienna and Oakton, we know this area well', 'Because our office is in Tysons, a short drive from the City of Fairfax, we know this area well'),
    ("Our help is free, and because we're based right next door in Vienna, we're here for Oakton", "Our help is free, and because our office is minutes away in Tysons, we're here for Oakton"),
    ("We're an independent agency based right nearby in Vienna, helping Tysons residents", "We're an independent agency based right here in Tysons, helping Tysons residents"),
    ('Being close to Arlington and Tysons — and just down the road from our Vienna office — means', 'Being close to Arlington and just down the road from our Tysons office means'),
    ('based nearby in Vienna, we know Falls Church, Arlington, and Tysons,', 'based nearby in Tysons, we know Falls Church and Arlington,'),
    # link cards to the Vienna page: about Vienna, not the office
    ('Medicare &amp; insurance help where our local office is based.', 'Medicare &amp; insurance help in Vienna, minutes from our Tysons office.'),
    ('Medicare &amp; insurance help right where our office is — free and local.', 'Medicare &amp; insurance help in Vienna, minutes from our Tysons office.'),
    ('Free, no-pressure Medicare guidance from our home base in Vienna.', 'Medicare help in Vienna, minutes from our Tysons office.'),
    ('Free, no-pressure Medicare guidance from our home-base Vienna office.', 'Medicare help in Vienna, minutes from our Tysons office.'),
    ('Free, no-pressure guidance from our home office in Vienna.', 'Medicare help in Vienna, minutes from our Tysons office.'),
    ('because our home office is right here in Vienna', 'because our office is minutes away in Tysons'),
    ('Our home office is right here in Vienna at 8609 Westwood Center Drive', 'Our office is minutes away in Tysons at 8609 Westwood Center Drive'),
    ('Local Medicare &amp; insurance help minutes from our Vienna office.', 'Local Medicare &amp; insurance help minutes from our Tysons office.'),
    ('Home of our office — in-person Medicare help in Vienna.', 'Medicare help in Vienna, minutes from our Tysons office.'),
    ('Right in our backyard — Medicare &amp; insurance help in Vienna.', 'Medicare &amp; insurance help in Vienna, near our Tysons office.'),
    ('Our home office is right here in Vienna, so Virginia is our local state.', 'Our office is in Tysons, so Virginia is our local state.'),
    ('based in Vienna — Virginia is our home state —', 'based in Tysons — Virginia is our home state —'),
    ('our office is nearby in Vienna, just a short drive from McLean', 'our office is nearby in Tysons, just a short drive from McLean'),
    ('our office is nearby in Vienna, just across the county line', 'our office is nearby in Tysons'),
    ('based right nearby in Vienna — just a short hop across the county line from Arlington', 'based nearby in Tysons, a short drive from Arlington'),
]
TYSONS_RX = [
    (re.compile(r'\b(based (?:right |just )?(?:nearby |next door |up the road |down the road |a short drive away |just a short drive away )?)in Vienna\b'), r'\1in Tysons'),
    (re.compile(r'\b(based right (?:nearby|next door|down the road)) in Vienna\b'), r'\1 in Tysons'),
    (re.compile(r'\b(office is (?:just )?(?:nearby|a short drive away|just a short drive away|minutes away)) in Vienna\b'), r'\1 in Tysons'),
    (re.compile(r'\b(Our office is nearby) in Vienna\b'), r'\1 in Tysons'),
    (re.compile(r'\bour home base in Vienna\b'), 'our home base in Tysons'),
    (re.compile(r'\bour home-base Vienna office\b'), 'our home-base Tysons office'),
    (re.compile(r'\bour home office in Vienna\b'), 'our home office in Tysons'),
    (re.compile(r'\bour Vienna office\b'), 'our Tysons office'),
    (re.compile(r'\bdown the road in Vienna\b'), 'down the road in Tysons'),
    (re.compile(r'\b(based just a short drive away) in Vienna\b'), r'\1 in Tysons'),
]
OFFICE_VIENNA = re.compile(r'(?:office is|office,|based|home base|home-base|home office)[^.<"]{0,45}\bin Vienna\b|\bVienna office\b')

NOVA_SCHEMA = {'alexandria': 'Alexandria, VA', 'herndon': 'Herndon, VA', 'oakton': 'Oakton, VA', 'reston': 'Reston, VA'}
ADDRESS = {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA",
           "postalCode": "22182", "addressCountry": "US"}
ONE_STATE_POSTS = dict([('blog/' + CHANGE_POST % k, v) for k, v in STATES.items()] + [('blog/aca-or-medicaid-virginia-2026', 'Virginia')])
FAIRFAX_NEAR = ['alexandria', 'arlington', 'falls-church', 'herndon', 'mclean', 'oakton', 'reston', 'tysons', 'vienna']


# Languages (owner, Nov 24 2026: "yes add the languages"; his Virginia Marketplace agent listing lists Arabic, English, French, Spanish)
LANGS = ['English', 'Arabic', 'French', 'Spanish']
LANG_LINE = 'We speak English, Arabic, French and Spanish'
FOOT_LANG = '\n        <p class="hb-langs">%s</p>' % LANG_LINE
CONTACT_LANG = ('\n      <div class="info-line"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
                'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg></span>'
                '<div><strong>Languages</strong><br>English, Arabic, French and Spanish</div></div>')


def languages(key, s):
    if 'class="hb-langs"' not in s:
        s = re.sub(r'(<h3>Contact</h3>\s*<a href="tel:\+13016158289">[^<]*</a>\s*<a href="sms:\+15713540146">[^<]*</a>)', lambda m: m.group(1) + FOOT_LANG, s, count=1)
    if key in ('contact', 'index') and '<strong>Languages</strong>' not in s:
        s = re.sub(r'(<div class="info-line">(?:(?!</div></div>).)*<strong>Email</strong>.*?</div></div>)', lambda m: m.group(1) + CONTACT_LANG, s, count=1, flags=re.S)
    if key == 'index' and 'Help in English, Arabic, French and Spanish' not in s:
        s = re.sub(r'(<li><i>(?:(?!</li>).)*</i>Year-round service, not just at enrollment</li>)',
                   lambda m: m.group(1) + '\n      ' + m.group(1).replace('Year-round service, not just at enrollment', 'Help in English, Arabic, French and Spanish'), s, count=1, flags=re.S)
    if key == 'about':
        s = s.replace('Your licensed agent is Luay Sadqi, NPN 21370662.</p>', 'Your licensed agent is Luay Sadqi, NPN 21370662. Luay speaks English, Arabic, French and Spanish.</p>', 1)
    for m in reversed(_ld_blocks(s)):
        try: j = json.loads(m.group(2))
        except ValueError: continue
        if isinstance(j, dict) and j.get('@type') in ('InsuranceAgency', 'Person') and 'knowsLanguage' not in j and (j.get('@type') == 'InsuranceAgency' or j.get('name') == 'Luay Sadqi'):
            j['knowsLanguage'] = LANGS
            s = s[:m.start(2)] + '\n' + json.dumps(j, indent=2, ensure_ascii=False) + '\n' + s[m.end(2):]
    return s


def _u(x):
    return html.unescape(x)


def trim(d):
    """A description of 160 characters or fewer: no cut-off old number, then filler out, then the last sentence."""
    d = re.sub(r'\s*\(571\)\.\.\.$', '', d)
    for a, b in TRIM:
        if len(_u(d)) <= 160: break
        d = d.replace(a, b)
    if len(_u(d)) > 160:
        ends = [m.end() - 1 for m in re.finditer(r'[.?!] ', d) if len(_u(d[:m.end() - 1])) <= 160]
        if ends and len(_u(d[:ends[-1]])) >= 90: d = d[:ends[-1]]
    return d


def _set_meta(s, attr, name, value):
    return re.sub(r'(<meta %s="%s" content=")[^"]*(")' % (attr, re.escape(name)), lambda m: m.group(1) + value + m.group(2), s, count=1)


def titles(key, s):
    m = re.search(r'<title>(.*?)</title>', s, re.S)
    if not m: return s
    old = m.group(1).strip(); new = old
    h = HUB_TITLE.match(old)
    if key in TITLES: new = TITLES[key]
    elif h and key.endswith('-medicare-insurance') and key[:-len('-medicare-insurance')] in STATES:
        new = '%s Medicare Agent &amp; Broker | Honorbrook' % (h.group(1) or h.group(2))
    elif key.startswith('blog/' + CHANGE_POST % ''):
        st = STATES.get(key[len('blog/' + CHANGE_POST % ''):])
        if st:
            new = 'When Can I Change Medicare Plans in %s? | Honorbrook' % st
            if len(_u(new)) > 60: new = new[:-len(' | Honorbrook')]
    elif len(_u(old)) > 60 and old.endswith(' | Honorbrook Insurance'):
        new = old[:-len(' Insurance')]
        if len(_u(new)) > 60 and key.startswith('blog/'): new = new[:-len(' | Honorbrook')]
    elif len(_u(old)) > 60 and key.startswith('blog/') and old.endswith(' | Honorbrook'):
        new = old[:-len(' | Honorbrook')]
    if new == old: return s
    s = s.replace(m.group(0), '<title>%s</title>' % new, 1)
    for attr, name in (('property', 'og:title'), ('name', 'twitter:title')):
        mm = re.search(r'<meta %s="%s" content="([^"]*)"' % (attr, name), s)
        if mm and (mm.group(1) == old or _u(mm.group(1)).replace(' | Honorbrook Insurance', ' | Honorbrook') == _u(old).replace(' | Honorbrook Insurance', ' | Honorbrook') or (key == 'long-term-care-insurance' and 'in Virginia' in mm.group(1))):
            s = _set_meta(s, attr, name, new)
    return s


def descriptions(key, s):
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not m: return s
    old = m.group(1)
    new = DESCS.get(key) or trim(old)
    if new != old: s = _set_meta(s, 'name', 'description', new)
    for attr, name in (('property', 'og:description'), ('name', 'twitter:description')):
        mm = re.search(r'<meta %s="%s" content="([^"]*)"' % (attr, name), s)
        if not mm: continue
        v = mm.group(1)
        nv = new if (v == old or key in DESCS) else trim(v)
        if nv != v: s = _set_meta(s, attr, name, nv)
    return s


def office(key, s):
    if key.replace('-medicare-insurance', '') not in NOVA: return s
    for a, b in TYSONS_FIRST: s = s.replace(a, b)
    for rx, b in TYSONS_RX: s = rx.sub(b, s)
    return s


def _ld_blocks(s):
    return list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S))


def schema(key, s, all17):
    if key == 'about':
        for m in reversed(_ld_blocks(s)):
            try: j = json.loads(m.group(2))
            except ValueError: continue
            if isinstance(j, dict) and j.get('@type') == 'Person' and isinstance(j.get('areaServed'), list) and len(j['areaServed']) < 17:
                j['areaServed'] = [{"@type": "AdministrativeArea" if n == 'District of Columbia' else "State", "name": n} for n in all17]
                s = s[:m.start(2)] + '\n' + json.dumps(j, indent=2, ensure_ascii=False) + '\n' + s[m.end(2):]
    if key in ONE_STATE_POSTS:
        st = ONE_STATE_POSTS[key]
        for m in reversed(_ld_blocks(s)):
            try: j = json.loads(m.group(2))
            except ValueError: continue
            if isinstance(j, dict) and isinstance(j.get('contentLocation'), list) and len(j['contentLocation']) > 1:
                j['contentLocation'] = [{"@type": "AdministrativeArea" if st == 'Washington, DC' else "State", "name": st}]
                s = s[:m.start(2)] + '\n' + json.dumps(j, indent=2, ensure_ascii=False) + '\n' + s[m.end(2):]
    town = NOVA_SCHEMA.get(key.replace('-medicare-insurance', ''))
    if town and '"InsuranceAgency"' not in s:
        j = {"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "telephone": "+1-301-615-8289",
             "address": ADDRESS, "areaServed": [town, "Fairfax County, VA"] if town != 'Alexandria, VA' else [town],
             "url": "https://honorbrook-insurance.com/" + key}
        s = s.replace('</head>', '<script type="application/ld+json">\n%s\n</script>\n</head>' % json.dumps(j, indent=2), 1)
    if key == 'index':
        s = s.replace('"Group and SHOP Insurance"\n  ]', '"Group and SHOP Insurance",\n    "Term and Whole Life Insurance",\n    "Indexed Universal Life",\n    "Annuities"\n  ]', 1)
    return s


def links(key, s, have):
    # each state's change-plan post: from the state hub and every county/parish page in that state
    for st, ab in ABBR.items():
        post = 'blog/' + CHANGE_POST % st
        if post not in have: continue
        href = 'href="/%s"' % post
        if href in s: continue
        name = STATES[st]
        if key == st + '-medicare-insurance':
            line = '<p>Want to switch plans? See <a %s>when you can change Medicare plans in %s</a>.</p>\n    ' % (href, name)
            if '<h2>Under 65? ACA health insurance' in s: s = s.replace('<h2>Under 65? ACA health insurance', line + '<h2>Under 65? ACA health insurance', 1)
            elif '<div class="cta-strip">' in s: s = s.replace('<div class="cta-strip">', line + '<div class="cta-strip">', 1)
        elif st == 'virginia' and key in VA_COUNTY_LEVEL:
            line = '<p>Want to switch plans? See <a %s>when you can change Medicare plans in Virginia</a>.</p>\n    ' % href
            if READ_RX.search(s): s = READ_RX.sub(lambda m: m.group(1) + '\n      <li><a %s>When can you change Medicare plans in Virginia?</a></li>' % href, s, count=1)
            elif '<div class="cta-strip">' in s: s = s.replace('<div class="cta-strip">', line + '<div class="cta-strip">', 1)
        elif re.search(r'-(county|parish|city)-%s-medicare-insurance$' % ab, key):
            s = READ_RX.sub(lambda m: m.group(1) + '\n      <li><a %s>When can you change Medicare plans in %s?</a></li>' % (href, name), s, count=1)
    aca65 = 'href="/blog/can-i-keep-my-aca-marketplace-plan-when-i-turn-65"'
    if key == 'turning-65' and aca65 not in s:
        a = 'If you are on COBRA and approaching 65, talk to someone before you make a decision.</p>'
        s = s.replace(a, a + '\n    <p>On a Marketplace (ACA) plan as you near 65? Read <a %s>can I keep my ACA plan when I turn 65?</a></p>' % aca65, 1)
    if key == 'aca-health-insurance' and aca65 not in s and '<div class="cta-strip">' in s:
        s = s.replace('<div class="cta-strip">', '<p>Turning 65 soon? Read <a %s>can I keep my ACA plan when I turn 65?</a></p>\n    <div class="cta-strip">' % aca65, 1)
    ff = 'href="/fairfax-medicare-insurance"'
    if key == 'index':
        s = s.replace('Office visits are by appointment in Tysons, Virginia.',
                      'Office visits are by appointment in Tysons, Virginia (see <a %s>Medicare help in Fairfax County</a>).' % ff, 1)
    elif key.replace('-medicare-insurance', '') in FAIRFAX_NEAR:
        body = s[s.find('<article'):s.find('</article>')]
        if ff not in body and '<div class="cta-strip">' in s:
            lead = 'Nearby: <a %s>Medicare help in Fairfax County</a>.' if key.replace('-medicare-insurance', '') in ('alexandria', 'arlington', 'falls-church') else 'More: <a %s>Medicare help across Fairfax County</a>.'
            s = s.replace('<div class="cta-strip">', '<p>' + lead % ff + '</p>\n    <div class="cta-strip">', 1)
    return s


def apply(out, all17):
    """Every page. Returns counts by fix."""
    have = set(os.path.relpath(f, out)[:-5] for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True))
    n = {'titles': 0, 'descriptions': 0, 'office': 0, 'schema': 0, 'links': 0, 'languages': 0}
    for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/' in f: continue
        key = os.path.relpath(f, out)[:-5]
        s = open(f, encoding='utf-8', errors='ignore').read()
        if 'http-equiv="refresh"' in s[:3000]: continue
        o = s
        for name, fn in (('titles', lambda x: titles(key, x)), ('descriptions', lambda x: descriptions(key, x)), ('office', lambda x: office(key, x)),
                         ('schema', lambda x: schema(key, x, all17)), ('links', lambda x: links(key, x, have)),
                         ('languages', lambda x: languages(key, x))):
            t = fn(s)
            if t != s: n[name] += 1; s = t
        if s != o: open(f, 'w', encoding='utf-8').write(s)
    return n


def finish(out):
    """Site-wide files: stubs, Part D footer, area finder, lead event, llms.txt."""
    done = []
    # old redirect stubs shadow the permanent redirects in netlify.toml (they served 200 + meta refresh); remove them
    for p in ['medigap.html', 'group.html'] + [os.path.relpath(x, out) for x in glob.glob(os.path.join(out, 'services', '*.html'))]:
        fp = os.path.join(out, p)
        if os.path.exists(fp) and 'http-equiv="refresh"' in open(fp, encoding='utf-8', errors='ignore').read()[:3000]:
            os.remove(fp); done.append('removed stub ' + p)
    if os.path.isdir(os.path.join(out, 'services')) and not os.listdir(os.path.join(out, 'services')): os.rmdir(os.path.join(out, 'services'))
    # Part D page: the standard footer (it kept an older one without the 17 names)
    pd, ref = os.path.join(out, 'medicare-part-d.html'), os.path.join(out, 'medicare-advantage.html')   # a Medicare page: its footer carries the CMS disclaimer
    s, r = open(pd, encoding='utf-8').read(), open(ref, encoding='utf-8').read()
    if 'Licensed in 16 states and DC:' not in s and 'Licensed in 16 states and DC:' in r:
        a, b = s.index('<footer'), s.index('</footer>') + len('</footer>')
        ra, rb = r.index('<footer'), r.index('</footer>') + len('</footer>')
        new = s[:a] + r[ra:rb] + s[b:]
        if 'do not offer every plan available in your area' not in new: raise SystemExit('seo: Part D footer lost the CMS disclaimer')
        open(pd, 'w', encoding='utf-8').write(new); done.append('part-d footer')
    # area finder: the ACA link only where an ACA state page exists
    fj = os.path.join(out, 'assets', 'find.js'); t = open(fj, encoding='utf-8').read()
    aca = sorted(os.path.basename(x)[:-len('-aca-health-insurance.html')] for x in glob.glob(os.path.join(out, '*-aca-health-insurance.html')))
    old = "<li><a href=\"' + u + '-aca-health-insurance\">' + esc(st[0]) + ' ACA health insurance</a></li>"
    if old in t:
        t = t.replace(old, "' + (HB_ACA.indexOf(st[2]) >= 0 ? '<li><a href=\"' + u + '-aca-health-insurance\">' + esc(st[0]) + ' ACA health insurance</a></li>' : '') + '", 1)
        t = t.replace('function search(q) {', 'var HB_ACA = %s;\n  function search(q) {' % json.dumps(aca), 1)
        open(fj, 'w', encoding='utf-8').write(t); done.append('finder ACA link for %d states' % len(aca))
    # chat.js: count a lead only when the form passes its own check (it fired on every submit, valid or not)
    cj = os.path.join(out, 'assets', 'chat.js'); t = open(cj, encoding='utf-8').read()
    a = "if(e.target&&e.target.tagName==='FORM'){ track("
    if a in t:
        open(cj, 'w', encoding='utf-8').write(t.replace(a, "if(e.target&&e.target.tagName==='FORM'&&!e.target.classList.contains('hbf-contact')&&e.target.checkValidity()){ track(", 1)); done.append('lead event only on valid forms')
    # llms.txt: ACA state pages and county directories
    lp = os.path.join(out, 'llms.txt'); t = open(lp, encoding='utf-8').read()
    t = t.replace('by phone, at the Tysons office or at home', 'by phone, or at the Tysons office or at home in Northern Virginia')
    if '- Languages:' not in t:
        t = re.sub(r'(- Hours: [^\n]*\n)', lambda m: m.group(1) + '- Languages: English, Arabic, French, Spanish\n', t, count=1)
    if '## ACA health insurance by state' not in t:
        acas = ''.join('- [%s ACA health insurance](https://honorbrook-insurance.com/%s-aca-health-insurance)\n' % (STATES[k], k) for k in aca if k in STATES)
        dirs = sorted(os.path.basename(x)[:-5] for x in glob.glob(os.path.join(out, '*-counties.html')))
        dl = ''.join('- [%s by county](https://honorbrook-insurance.com/%s)\n' % (STATES.get(d[:-len('-counties')], d), d) for d in dirs)
        t = t.rstrip('\n') + '\n\n## ACA health insurance by state\n' + acas + '\n## County directories\n' + dl
        open(lp, 'w', encoding='utf-8').write(t); done.append('llms.txt: %d ACA pages, %d directories' % (aca.__len__(), len(dirs)))
    return done


def _rel(path):
    """Sitemap path -> file in the build: 'blog/' is blog/index.html, 'x' is x.html."""
    return path + 'index.html' if path.endswith('/') else path if path.endswith('.html') else path + '.html'


def sitemaps(out, date, changed):
    """Pages changed in this build (vs the live copy) get today's date; removed stubs leave the sitemap."""
    done = []
    for sm in ('sitemap.xml', 'sitemap-counties.xml'):
        p = os.path.join(out, sm)
        if not os.path.exists(p): continue
        t = open(p, encoding='utf-8').read(); k = 0
        def lm(m):
            nonlocal k
            loc = m.group(1); path = loc.split('honorbrook-insurance.com/', 1)[-1] or 'index'
            rel = _rel(path)
            if rel in changed and m.group(2) < date:
                k += 1; return m.group(0).replace('<lastmod>%s</lastmod>' % m.group(2), '<lastmod>%s</lastmod>' % date)
            return m.group(0)
        t = re.sub(r'<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>.*?</url>', lm, t, flags=re.S)
        def add(m):
            nonlocal k
            path = m.group(1).split('honorbrook-insurance.com/', 1)[-1] or 'index'
            if _rel(path) in changed:
                k += 1; return m.group(0) + '<lastmod>%s</lastmod>' % date
            return m.group(0)
        t = re.sub(r'<loc>([^<]+)</loc>(?!\s*<lastmod>)', add, t)
        for stub in ('medigap', 'group'):
            t = re.sub(r'\s*<url>\s*<loc>https://honorbrook-insurance\.com/%s</loc>.*?</url>' % stub, '', t, flags=re.S)
        open(p, 'w', encoding='utf-8').write(t); done.append('%s: %d dates' % (sm, k))
    return done


def check(out):
    """What should be zero after this pass."""
    long_t, long_d, cut, vienna = [], [], [], []
    for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/' in f: continue
        key = os.path.relpath(f, out)[:-5]
        s = open(f, encoding='utf-8', errors='ignore').read()
        if 'http-equiv="refresh"' in s[:3000]: continue
        m = re.search(r'<title>(.*?)</title>', s, re.S)
        if m and len(_u(m.group(1).strip())) > 60: long_t.append(key)
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        if m and len(_u(m.group(1))) > 160: long_d.append(key)
        if '(571)...' in s: cut.append(key)
        if key.replace('-medicare-insurance', '') in NOVA and OFFICE_VIENNA.search(s): vienna.append(key)
    return {'titles over 60': long_t, 'descriptions over 160': long_d, 'cut-off (571)': cut, 'office said Vienna': vienna}


# ---------------------------------------------------------------------------------------------------------------------------
# Nov 27 2026 technical pass (growth plan items 7, 10 trust, 18, 20). Runs last in build.py, before the final claims guard.
# - Schema: one agency entity. The #organization node (home, about, contact) stays; every other InsuranceAgency or
#   LocalBusiness node without an @id (county, city, state, ACA and life state pages) becomes a Service for that area whose
#   provider is {"@id": "#organization"}. The home page gets a WebSite node. knowsAbout gains the lines the site sells.
#   priceRange "Free consultation" is not a price range and is removed.
# - The YouTube channel link returned 404 on Nov 27 2026 (curl): removed from sameAs and from every footer.
# - Speed: asset links carry a short content hash (?v=xxxxxxxx) so a changed file reaches visitors at once; unchanged files
#   keep their cached copy. Fonts come from a <link> in the head (theme_css.FONT_LINK), not a CSS @import.
# - Hygiene: one robots meta per page (the thank-you page had both noindex and index); Open Graph tags on the calculators.
# - Trust: "Verify our license" on about and contact. Links checked Nov 27 2026: the NIPR NPN lookup and the Virginia SCC
#   Bureau of Insurance agent search both load. The agency NPN 22269925 is the one already stated on /terms.
# ---------------------------------------------------------------------------------------------------------------------------
import hashlib

SITE_URL = 'https://honorbrook-insurance.com/'
ORG_ID = SITE_URL + '#organization'
WEBSITE_ID = SITE_URL + '#website'
DEAD_LINKS = ['https://www.youtube.com/@luaysadqi5069']   # 404 on Nov 27 2026
KNOWS_MORE = ['Term and Whole Life Insurance', 'Indexed Universal Life', 'Annuities', 'Veterans Life Insurance', 'Mortgage Protection Insurance', "Children's Life Insurance", 'Long-Term Care Insurance', 'Disability Insurance']
NIPR_LOOKUP = 'https://nipr.com/licensing-center/look-up-a-national-producer-number'
VA_BOI_LOOKUP = 'https://www.scc.virginia.gov/boi/consumerinquiry/search.aspx?searchType=agent'
VERIFY = ('<div class="hb-verify" id="verify-license">\n'
          '      <h3>Verify our license</h3>\n'
          '      <p>Licensed agent: Luay Sadqi, National Producer Number (NPN) 21370662. Agency NPN: 22269925 (Luay&rsquo;s Lifeline Inc., doing business as Honorbrook Insurance).</p>\n'
          '      <ul>\n'
          '        <li><a href="%s" target="_blank" rel="noopener">Look up a National Producer Number</a> at NIPR, the National Insurance Producer Registry.</li>\n'
          '        <li><a href="%s" target="_blank" rel="noopener">Search Virginia licensed agents and agencies</a> at the Virginia State Corporation Commission, Bureau of Insurance.</li>\n'
          '      </ul>\n'
          '    </div>\n    ') % (NIPR_LOOKUP, VA_BOI_LOOKUP)
OG_IMAGE = SITE_URL + 'assets/og-image.jpg'


def _agency(o):
    t = o.get('@type'); t = t if isinstance(t, list) else [t]
    return bool({'InsuranceAgency', 'LocalBusiness'} & set(t))


def _service_type(key):
    if key.endswith('-aca-health-insurance'): return 'ACA health insurance guidance'
    if key.endswith('-life-insurance'): return 'Life insurance guidance'
    if key.endswith('-medicare-advantage'): return 'Medicare Advantage guidance'
    if key.endswith('-medicare-insurance'): return 'Medicare, health and life insurance guidance'
    if key == 'iul-policy-review': return 'Indexed universal life policy review'
    return 'Insurance guidance'


def _place(x):
    if isinstance(x, dict): return x
    return {"@type": "AdministrativeArea" if re.search(r'County|Parish|District of Columbia|\bCity of\b', str(x)) else "Place", "name": str(x)}


def _area(a):
    if isinstance(a, list):
        a = [_place(x) for x in a]
        return a[0] if len(a) == 1 else a
    return _place(a)


def _to_service(j, key, url):
    node = {"@context": j.get('@context', 'https://schema.org'), "@type": "Service", "serviceType": _service_type(key)}
    a = j.get('areaServed')
    if a:
        node['areaServed'] = _area(a)
        names = [x.get('name') for x in (node['areaServed'] if isinstance(node['areaServed'], list) else [node['areaServed']]) if x.get('name')]
        if names: node['name'] = '%s in %s' % (node['serviceType'], ' and '.join(names[:2]) if len(names) <= 2 else names[0])
    if j.get('description'): node['description'] = j['description']
    node['provider'] = {"@id": ORG_ID}
    node['url'] = j.get('url') or url
    return node


def _clean(o):
    """Inside any node: agency providers without @id point to the one entity; dead sameAs links and the priceRange go."""
    if isinstance(o, dict):
        for k in list(o):
            v = o[k]
            if k == 'provider' and isinstance(v, dict) and _agency(v) and '@id' not in v:
                o[k] = {"@id": ORG_ID}; continue
            if k == 'sameAs':
                if isinstance(v, list): o[k] = [x for x in v if x not in DEAD_LINKS]
                elif v in DEAD_LINKS: del o[k]; continue
            if k == 'priceRange' and v == 'Free consultation': del o[k]; continue
            _clean(o[k])
        if o.get('@id') == ORG_ID and isinstance(o.get('knowsAbout'), list):
            have = {str(x).lower() for x in o['knowsAbout']}
            o['knowsAbout'] += [x for x in KNOWS_MORE if x.lower() not in have]
    elif isinstance(o, list):
        for x in o: _clean(x)
    return o


def tech_schema(key, s):
    canon = re.search(r'rel="canonical" href="([^"]+)"', s)
    url = canon.group(1) if canon else SITE_URL + ('' if key == 'index' else key)
    for m in reversed(_ld_blocks(s)):
        try: j = json.loads(m.group(2))
        except ValueError: continue
        old = json.dumps(j, sort_keys=True)
        if isinstance(j, dict) and '@graph' in j and isinstance(j['@graph'], list):
            j['@graph'] = [_to_service(x, key, url) if isinstance(x, dict) and _agency(x) and '@id' not in x else x for x in j['@graph']]
        elif isinstance(j, dict) and _agency(j) and '@id' not in j:
            j = _to_service(j, key, url)
        _clean(j)
        if json.dumps(j, sort_keys=True) != old:
            s = s[:m.start(2)] + '\n' + json.dumps(j, indent=2, ensure_ascii=False) + '\n' + s[m.end(2):]
    if key == 'index' and '"WebSite"' not in s:
        w = {"@context": "https://schema.org", "@type": "WebSite", "@id": WEBSITE_ID, "url": SITE_URL, "name": "Honorbrook Insurance",
             "inLanguage": "en-US", "publisher": {"@id": ORG_ID}}
        s = s.replace('</head>', '<script type="application/ld+json">\n%s\n</script>\n</head>' % json.dumps(w, indent=2), 1)
    return s


def tech_hygiene(key, s):
    for d in DEAD_LINKS:   # footer link to the dead channel
        s = re.sub(r'\n?[ \t]*<a href="%s"[^>]*>[^<]*</a>' % re.escape(d), '', s)
    r = list(re.finditer(r'\n?[ \t]*<meta name="robots"[^>]*>', s))
    if len(r) > 1:   # one robots tag: the noindex one if any, else the first
        keep = next((m for m in r if 'noindex' in m.group(0)), r[0])
        for m in reversed(r):
            if m is not keep: s = s[:m.start()] + s[m.end():]
    if (key.endswith('-calculator') or key == 'calculators') and 'property="og:title"' not in s:
        t = re.search(r'<title>(.*?)</title>', s, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', s)
        c = re.search(r'rel="canonical" href="([^"]+)"', s)
        tags = [('og:type', 'website'), ('og:site_name', 'Honorbrook Insurance'), ('og:title', t.group(1).strip() if t else ''),
                ('og:description', d.group(1) if d else ''), ('og:url', c.group(1) if c else SITE_URL + key), ('og:image', OG_IMAGE),
                ('og:image:width', '1200'), ('og:image:height', '630')]
        add = ''.join('\n<meta property="%s" content="%s">' % (p, v) for p, v in tags if v and 'property="%s"' % p not in s)
        if d: s = s.replace(d.group(0) + '>', d.group(0) + '>' + add, 1)
        else: s = s.replace('</title>', '</title>' + add, 1)
    if 'fonts.googleapis.com/css2' not in s and 'href="/assets/style.css' in s:   # every page loads the fonts from its head
        import theme_css
        s = s.replace('<link rel="stylesheet" href="/assets/style.css', theme_css.FONT_LINK + '\n<link rel="stylesheet" href="/assets/style.css', 1)
    return s


def tech_verify(key, s):
    if 'class="hb-verify"' in s: return s
    if key == 'about':
        i = s.find('<h2>Licensed. Independent. Documented.</h2>'); j = s.find('<div class="cta-strip">', i)
        if i > 0 and j > 0: s = s[:j] + VERIFY + s[j:]
    elif key == 'contact':
        s = re.sub(r'(<div class="info-line">(?:(?!</div></div>).)*<strong>Hours</strong>.*?</div></div>)', lambda m: m.group(1) + '\n      ' + VERIFY.rstrip(), s, count=1, flags=re.S)
    return s


def tech(out):
    """The last pass over the build. Returns counts; exits if any JSON-LD block does not parse or the one entity is missing."""
    n = {'schema': 0, 'hygiene': 0, 'verify': 0, 'versions': 0}
    hashes = {}

    def ver(m):
        p = os.path.join(out, 'assets', m.group(2))
        if not os.path.isfile(p): return m.group(0)
        if p not in hashes: hashes[p] = hashlib.sha1(open(p, 'rb').read()).hexdigest()[:8]
        return '%s?v=%s"' % (m.group(1), hashes[p])
    bad = []
    for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/' in f: continue
        key = os.path.relpath(f, out)[:-5]
        s = open(f, encoding='utf-8', errors='ignore').read(); o = s
        for name, fn in (('schema', tech_schema), ('hygiene', tech_hygiene), ('verify', tech_verify)):
            t = fn(key, s)
            if t != s: n[name] += 1; s = t
        t = re.sub(r'((?:src|href)="/assets/([^"?#]+\.(?:css|js)))(?:\?v=[0-9a-z]+)?"', ver, s)
        if t != s: n['versions'] += 1; s = t
        for m in _ld_blocks(s):
            try: json.loads(m.group(2))
            except ValueError: bad.append(key)
        if s != o: open(f, 'w', encoding='utf-8').write(s)
    for p in glob.glob(os.path.join(out, '*.txt')):   # llms.txt and the like
        t = open(p, encoding='utf-8').read(); u = t
        for d in DEAD_LINKS: u = re.sub(r'[^\n]*%s[^\n]*\n?' % re.escape(d), '', u)
        if u != t: open(p, 'w', encoding='utf-8').write(u)
    if bad: raise SystemExit('tech: invalid JSON-LD in ' + ', '.join(bad[:10]))
    idx = open(os.path.join(out, 'index.html'), encoding='utf-8').read()
    if ORG_ID not in idx or WEBSITE_ID not in idx: raise SystemExit('tech: home page lost the organization or website node')
    n['asset files hashed'] = len(hashes)
    return n
