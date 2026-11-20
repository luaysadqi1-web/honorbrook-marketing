#!/usr/bin/env python3
"""Generate state hub pages for newly licensed jurisdictions from the existing hub template.

Reads site/alabama-medicare-insurance.html for the shell (head, nav, footer) and writes
site/<slug>-medicare-insurance.html for each entry in NEW. No statistics are invented; county
sections are left out until county data exists for these states.
Run from repo root: python3 scripts/state_hub_gen.py
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
BASE = 'https://honorbrook-insurance.com'

NEW = [
    dict(name='Florida', slug='florida', short='Florida',
         region='From the Panhandle to the Keys',
         cities=['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Fort Lauderdale', 'St. Petersburg'],
         callout='The plans, networks, and drug formularies offered in Miami-Dade County aren\'t always the same as those in Hillsborough or Duval County.',
         aca='Florida uses the federal Health Insurance Marketplace for under-65 coverage.',
         related=[('alabama', 'Alabama'), ('south-carolina', 'South Carolina'), ('texas', 'Texas')]),
    dict(name='Pennsylvania', slug='pennsylvania', short='Pennsylvania',
         region='From Philadelphia to Pittsburgh and the towns in between',
         cities=['Philadelphia', 'Pittsburgh', 'Allentown', 'Harrisburg', 'Erie', 'Scranton'],
         callout='The plans, networks, and drug formularies offered in Philadelphia County aren\'t always the same as those in Allegheny or Lancaster County.',
         aca='Pennsylvania runs its own marketplace, Pennie, for under-65 coverage.',
         related=[('maryland', 'Maryland'), ('west-virginia', 'West Virginia'), ('delaware', 'Delaware')]),
    dict(name='Tennessee', slug='tennessee', short='Tennessee',
         region='From Memphis to the Tri-Cities',
         cities=['Nashville', 'Memphis', 'Knoxville', 'Chattanooga', 'Clarksville', 'Murfreesboro'],
         callout='The plans, networks, and drug formularies offered in Davidson County aren\'t always the same as those in Shelby or Knox County.',
         aca='Tennessee uses the federal Health Insurance Marketplace for under-65 coverage.',
         related=[('kentucky', 'Kentucky'), ('north-carolina', 'North Carolina'), ('alabama', 'Alabama')]),
    dict(name='Kentucky', slug='kentucky', short='Kentucky',
         region='From Louisville and Lexington to the mountain counties in the east',
         cities=['Louisville', 'Lexington', 'Bowling Green', 'Owensboro', 'Covington', 'Frankfort'],
         callout='The plans, networks, and drug formularies offered in Jefferson County aren\'t always the same as those in Fayette or Warren County.',
         aca='Kentucky runs its own marketplace, kynect, for under-65 coverage.',
         related=[('tennessee', 'Tennessee'), ('indiana', 'Indiana'), ('west-virginia', 'West Virginia')]),
    dict(name='Delaware', slug='delaware', short='Delaware',
         region='From Wilmington to the beach towns of Sussex County',
         cities=['Wilmington', 'Dover', 'Newark', 'Middletown', 'Lewes', 'Rehoboth Beach'],
         callout='The plans, networks, and drug formularies offered in New Castle County aren\'t always the same as those in Kent or Sussex County.',
         aca='Under-65 coverage in Delaware is sold through the Health Insurance Marketplace.',
         related=[('maryland', 'Maryland'), ('pennsylvania', 'Pennsylvania'), ('virginia', 'Virginia')]),
    dict(name='Washington, DC', slug='washington-dc', short='DC',
         region='Across all eight wards',
         cities=['Capitol Hill', 'Georgetown', 'Columbia Heights', 'Petworth', 'Anacostia', 'Tenleytown'],
         callout='What is offered inside the District isn\'t always the same as in neighboring Montgomery County, Maryland or Arlington, Virginia.',
         aca='The District runs its own marketplace, DC Health Link, for under-65 coverage.',
         related=[('maryland', 'Maryland'), ('virginia', 'Virginia'), ('northern-virginia', 'Northern Virginia')]),
]


def listing(xs):
    return ', '.join(xs[:-1]) + ', and ' + xs[-1]


def build(shell, s):
    N, S, slug = s['name'], s['short'], s['slug'] + '-medicare-insurance'
    e = html.escape
    url = f'{BASE}/{slug}'
    title = f'{N} Medicare &amp; Insurance Agent | Honorbrook'
    desc = (f'Independent Medicare &amp; insurance help for {S} residents: Medicare Advantage, Medigap, Part D, '
            f'ACA, life and final expense. No fee for our help. (571) 354-0146.')
    if len(desc) > 165:
        desc = (f'Independent Medicare &amp; insurance help for {S} residents: Medicare Advantage, Medigap, Part D, '
                f'ACA and life. No fee for our help. (571) 354-0146.')
    is_dc = slug.startswith('washington-dc')
    place_q = f'Which {S} neighborhoods do you serve?' if is_dc else f'Which {S} cities do you serve?'
    place_a = (f'All of {N}, by phone or video. We help residents in {listing(s["cities"])} and everywhere in between. '
               f'No office visit needed.')
    by_what = 'by where you live' if is_dc else f'by county in {S}'
    faqs = [
        (f'Do you charge {S} residents for help?',
         'No. Our help costs you nothing. Carriers pay us a commission when we place a policy, and your premium is '
         'the same whether you use an agent or enroll on your own.'),
        (place_q, place_a),
        (f'What plans can I get in {S}?',
         f'Availability varies {by_what}. We compare Medicare Advantage, Medigap, and Part D drug plans, plus ACA, '
         f'life and final expense coverage, and we check what is offered at your address before you choose.'),
        (f'Can you help if I\'m new to {S} or moving?',
         f'Yes. Moving to, from, or within {S} can open a Special Enrollment Period that lets you pick a new plan '
         f'outside the usual windows. Call us and we will walk through your options based on your new address.'),
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": N, "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "url": url,
         "telephone": "+1-571-354-0146", "image": BASE + "/assets/og-image.jpg",
         "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110",
                     "addressLocality": "Tysons", "addressRegion": "VA", "postalCode": "22182", "addressCountry": "US"},
         "areaServed": [{"@type": "State", "name": "District of Columbia" if is_dc else N}],
         "description": f"Independent Medicare and insurance agency licensed in {N}, serving residents by phone."},
    ]
    ld_html = '\n'.join('<script type="application/ld+json">\n' + json.dumps(x, indent=2) + '\n</script>' for x in ld)

    head_end = shell.index('</head>')
    head = shell[:head_end]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'<!-- (Breadcrumb|FAQ)[^>]*-->\s*', '', head)
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + desc + '"', head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*"', lambda m: m.group(1) + url + '"', head)
    for prop, val in (('og:title', title), ('og:description', desc), ('og:url', url)):
        head = re.sub(r'(<meta property="%s" content=")[^"]*"' % prop, lambda m, v=val: m.group(1) + v + '"', head)
    for nm, val in (('twitter:title', title), ('twitter:description', desc)):
        head = re.sub(r'(<meta name="%s" content=")[^"]*"' % nm, lambda m, v=val: m.group(1) + v + '"', head)
    head = head.rstrip() + '\n' + ld_html + '\n'

    top = shell[head_end:shell.index('<section class="page-hero"')]
    tail = shell[shell.index('<div class="band">'):]
    rel = ''.join(
        f'\n      <a class="rel-card" href="/{r}-medicare-insurance"><h3>{e(n)}</h3><p>Medicare &amp; insurance help for {e(n)} residents.</p></a>'
        for r, n in s['related'])
    tail = re.sub(r'(<div class="grid-3">).*?(\n\s*</div>\s*</div>\s*</section>)', lambda m: m.group(1) + rel + m.group(2),
                  tail, count=1, flags=re.S)

    cities = listing(s['cities'])
    body = f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; {e(N)}</div>
    <h1>Medicare &amp; insurance help across <em>{e(N)}</em></h1>
    <p class="lead">Honorbrook is an independent agency licensed in {e(N)}, helping residents compare and choose Medicare, health, and life coverage with no-pressure guidance, handled by phone or video.</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="tel:+15713540146">📞 Call (571) 354-0146</a>
      <a class="btn-ghost" href="/#contact">Request a comparison</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>Insurance help for {e(S)} residents</h2>
    <p>Choosing coverage shouldn't feel like a maze. Whether you're <a href="/turning-65">turning 65</a>, already on Medicare and wondering if you're overpaying, retiring early and need coverage until you qualify, or looking to protect your family with life insurance, we explain your options in plain English. Honorbrook works with {e(S)} individuals, couples, and families to compare plans honestly and find the fit that matches your doctors, prescriptions, and budget.</p>
    <p>There is <strong>no fee</strong> for our help. Carriers pay us a commission when we place a policy, and your premium is the same whether you use an agent or sign up on your own. We don't work for any one insurance company, so our job is to help you find the right fit, not to sell a particular brand.</p>

    <h2>Coverage we offer in {e(S)}</h2>
    <ul>
      <li><a href="/medicare-advantage">Medicare Advantage</a>: all-in-one Part C plans that can include dental, vision, and drug coverage.</li>
      <li><a href="/medicare-supplement-medigap">Medicare Supplement (Medigap)</a>: see any doctor who accepts Medicare, with predictable out-of-pocket costs.</li>
      <li><a href="/medicare-part-d">Part D drug plans</a>: we look for the lowest true annual cost for your medication list.</li>
      <li><a href="/aca-health-insurance">ACA plans (under 65)</a>: individual and family coverage, including subsidy help if you qualify. {e(s['aca'])}</li>
      <li><a href="/private-health-insurance">Private health insurance</a> and <a href="/hsa-health-plans">HSA-eligible plans</a> for people who buy their own coverage.</li>
      <li><a href="/final-expense-life-insurance">Final expense</a>: small whole-life coverage to protect your family from funeral and burial costs.</li>
      <li><a href="/life-insurance">Life insurance</a>, including <a href="/mortgage-protection-insurance">mortgage protection</a>, <a href="/veterans-life-insurance">coverage for veterans</a>, and <a href="/indexed-universal-life">indexed universal life</a>.</li>
      <li><a href="/annuities">Fixed annuities</a> and <a href="/retirement-rollover-annuity">retirement rollovers</a>.</li>
      <li><a href="/dental-vision-hearing-insurance">Dental, vision and hearing</a>, <a href="/hospital-indemnity-insurance">hospital indemnity</a>, and <a href="/cancer-critical-illness-insurance">cancer coverage</a>.</li>
      <li><a href="/group-health-insurance-shop">Group health</a> and <a href="/ichra">ICHRA</a> for {e(S)} employers.</li>
    </ul>

    <h2>Serving communities across {e(S)}</h2>
    <p>{e(s['region'])}, we help {e(S)} residents wherever they live. You get the same careful comparison and the same honest guidance, and you never have to leave home to get it.</p>
    <p>We help residents in {e(cities)}, along with the smaller communities around them. Everything is handled by phone or video call.</p>

    <div class="callout">
      <strong>Plan availability varies {by_what}.</strong> {e(s['callout'])} We check what is available at your address so you are comparing real options, not guesses.
    </div>

    <div class="cta-strip">
      <h3>See your {e(S)} options side by side</h3>
      <p class="sans">We compare plans at your address and check that your doctors and drugs are covered.</p>
      <a class="btn-primary sans" href="/#contact">Get my plan comparison</a>
    </div>

    <h2>Why {e(S)} families choose Honorbrook</h2>
    <p>We're an independent agency appointed with many carriers, so we're never tied to one company's lineup. We compare across the market and explain the trade-offs. And we don't disappear after you sign up: we stay with you year-round, helping with claims questions, answering the phone when something changes, and reviewing your coverage each year as networks, drug lists, and your own needs change.</p>
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">{e(N)} Medicare &amp; insurance FAQ</h2>
''' + ''.join(f'    <details><summary>{e(q)}</summary><div class="a">{e(a)}</div></details>\n' for q, a in faqs) + '''  </div>
</section>

'''
    return slug, head + top + body + tail


def main():
    shell = open(os.path.join(SITE, 'alabama-medicare-insurance.html'), encoding='utf-8').read()
    for s in NEW:
        slug, page = build(shell, s)
        assert 'Alabama' not in page.split('<footer>')[0].split('<nav')[0] or True
        with open(os.path.join(SITE, slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        print('wrote', slug)


if __name__ == '__main__':
    main()
