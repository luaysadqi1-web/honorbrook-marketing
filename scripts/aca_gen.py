#!/usr/bin/env python3
"""Build /{state}-aca-health-insurance.html for each of the 11 states from verified research JSON.

Input: scripts/aca_data/{state-slug}.json (copied from the research step). Null fields are omitted, never guessed.
Run from repo root: python3 scripts/aca_gen.py
"""
import json, os, re, sys, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = os.path.join(ROOT, 'site')
DATA = os.path.join(ROOT, 'scripts', 'aca_data')
BASE = g.BASE
esc = g.esc



KFF_URL = 'https://www.kff.org/elections/midterm-election-update-the-affordable-care-act-marketplaces/'
PTC = "The enhanced federal premium tax credits expired at the end of 2025 and have not been extended."
# Plain-English, page-ready statements. Every line below is traceable to a source the research step verified.
COPY = {
 'virginia': dict(exch='Virginia&rsquo;s Insurance Marketplace', exch_type='run by the state since November 2023',
    medicaid='Virginia has expanded Medicaid. Adults age 19 to 64 with income under 138% of the federal poverty level can qualify. Virginia has said work and community engagement requirements will apply to adults in Medicaid expansion starting January 2027.',
    state_help='Virginia Premium Savings is a new state program for 2027 plans for households with incomes between 138% and 250% of the federal poverty level. It is applied after the federal tax credit, and details are still being finalized.'),
 'maryland': dict(exch='Maryland Health Connection', exch_type='run by the state',
    medicaid='Maryland has expanded Medicaid. As of February 2026, a single adult with monthly income up to about $1,835 may qualify, and a household of four up to about $3,795.',
    state_help='The Maryland Premium Assistance Program gives eligible residents state help lowering monthly Marketplace premiums.'),
 'north-carolina': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='North Carolina has expanded Medicaid for adults age 19 to 64. NC Medicaid&rsquo;s 2025 limit was $1,800 a month for a single adult, and limits are updated each year. North Carolina has said most expansion adults will need to meet work requirements starting January 1, 2027, with exemptions.',
    state_help=None),
 'south-carolina': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='South Carolina has not expanded Medicaid. Parents and caretaker relatives can qualify at or below 62% of the federal poverty level, and the state lists no income limit for adults without children, who generally do not qualify.',
    state_help=None),
 'georgia': dict(exch='Georgia Access', exch_type='run by the state',
    medicaid='Georgia has not fully expanded Medicaid. Georgia Pathways to Coverage covers adults age 19 to 64 with income up to 100% of the federal poverty level who complete qualifying activities, such as 80 hours a month of work or similar activity. Rules are changing in 2027.',
    state_help='Georgia runs a state reinsurance program, launched in 2022 and authorized through December 31, 2026. The state has applied to extend it, and that application is under federal review.'),
 'michigan': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='Michigan has expanded Medicaid through the Healthy Michigan Plan for adults age 19 to 64. The state lists income at or below 133% of the federal poverty level, using the Modified Adjusted Gross Income method. Michigan has said work requirements begin January 1, 2027.',
    state_help=None),
 'west-virginia': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='West Virginia has expanded Medicaid. The state Department of Human Services describes low income as earning less than about $22,025 a year for one person or $45,540 for a family of four. West Virginia has said that starting January 1, 2027, many expansion adults age 19 to 64 must complete 80 hours a month of qualifying activities or earn at least $580 a month.',
    state_help=None),
 'louisiana': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='Louisiana has expanded Medicaid for adults age 19 to 64. The Louisiana Department of Health&rsquo;s 2026 table, effective March 1, 2026, lists monthly income up to $1,836 for one person and $3,142 for a household of three.',
    state_help=None),
 'texas': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='Texas has not expanded Medicaid. KFF lists Texas parents as qualifying only at about 15% of the federal poverty level for a parent in a family of three, and adults without children generally do not qualify. Some Texans with lower incomes fall into a coverage gap, which is why checking Marketplace subsidy eligibility matters.',
    state_help=None),
 'indiana': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='Indiana covers adults through the Healthy Indiana Plan (HIP), which the state describes as Medicaid for adults with income up to 138% of the federal poverty level, about $22,026 a year for one person in 2026. Indiana has said it will begin enforcing HIP work requirements on January 1, 2027.',
    state_help=None),
 'alabama': dict(exch='HealthCare.gov', exch_type='federal Marketplace',
    medicaid='Alabama has not expanded Medicaid. In 2026, parents and caretaker relatives qualify only with income up to about $240 a month for a family of one and $495 for a family of four, roughly 18% of the federal poverty level. Most adults without children do not qualify.',
    state_help=None),
}


def fdate(iso):
    if not iso:
        return None
    d = datetime.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def link(url, text):
    return f'<a href="{html.escape(url, quote=True)}" rel="noopener" target="_blank">{esc(text)}</a>' if url else esc(text)


def shell():
    t = open(os.path.join(SITE, 'aca-health-insurance.html')).read()
    a = t.index('<body>')
    b = t.index('<section class="page-hero"')
    hdr = t[a:b]
    hdr = re.sub(r'<div class="aep-banner.*?</div>\n', '@@BANNER@@\n', hdr, flags=re.S)
    return hdr, t[t.index('<footer>'):]


def build(sname, st, j, cen, pen, agg, slugmap, hdr, foot):
    slug = f"{st['slug']}-aca-health-insurance"
    canon = f'{BASE}/{slug}'
    hub = f"/{st['slug']}-medicare-insurance"
    C = COPY.get(st['slug'], {})
    ex = re.sub(r'&rsquo;', '\u2019', C.get('exch') or j.get('exchange_name') or 'the Health Insurance Marketplace')
    ex_url = j.get('exchange_url') or 'https://www.healthcare.gov/'
    s_, e_ = fdate(j.get('oe_start')), fdate(j.get('oe_end'))
    exch_type = C.get('exch_type') or ''
    banner = (f'<div class="aep-banner sans"><strong>{sname} ACA open enrollment: {s_} to {e_}.</strong> '
              f'<a href="/#contact">Get free help comparing plans &rarr;</a></div>') if s_ and e_ else \
             '<div class="aep-banner sans"><strong>ACA open enrollment begins November 1.</strong> <a href="/#contact">Get free help comparing plans &rarr;</a></div>'
    title = f"{sname} ACA Health Insurance 2027 | Honorbrook"
    desc = (f"{sname} ACA open enrollment for 2027: {s_} to {e_}. Compare plans and check your subsidy with an independent agency. (571) 354-0146."
            if s_ and e_ else f"{sname} ACA health insurance for 2027: compare plans and check your subsidy with an independent agency. (571) 354-0146.")
    desc = desc.replace(', 2026 to', ' to') if len(desc) > 160 else desc
    lead = (f"Open enrollment for 2027 ACA coverage in {sname} runs {s_} to {e_} on {esc(ex)}. "
            if s_ and e_ else f"Open enrollment for 2027 ACA coverage in {sname} begins November 1 on {esc(ex)}. ")
    lead += (f"Honorbrook Insurance is an independent agency licensed in {sname} that compares plans and checks your premium tax credit at no cost to you.")
    # table rows
    rows = [('Marketplace', f"{link(ex_url, ex)}" + (f" ({esc(exch_type)})" if exch_type else ''))]
    if s_ and e_:
        rows.append(('Open enrollment (2027 coverage)', f"{s_} to {e_}" + (f" &mdash; {link(j.get('oe_source_url'), 'source')}" if j.get('oe_source_url') else '')))
    me = j.get('medicaid_expanded')
    if me is not None:
        prog = 'full expansion' if me else ('Pathways work-requirement program, not a full expansion' if st['slug'] == 'georgia' else 'not expanded')
        rows.append(('Medicaid expansion', ('Yes' if me else ('Partial (Georgia Pathways, not a full expansion)' if st['slug'] == 'georgia' else 'No')) + (f" &mdash; {link(j.get('medicaid_url'), 'details')}" if j.get('medicaid_url') else '')))
    if C.get('state_help'):
        rows.append(('State help with premiums or costs', C['state_help'] + (f" ({link(j.get('state_subsidy_source_url'), 'source')})" if j.get('state_subsidy_source_url') else '')))
    rows.append(('Enhanced federal tax credits', PTC + f" ({link(KFF_URL, 'KFF, October 2026')})"))
    tbl = '\n'.join(f'          <tr><td>{a}</td><td>{b}</td></tr>' for a, b in rows)
    # medicaid section
    med = (C.get('medicaid') + ' Whether you qualify depends on your household and income, so we check Medicaid and Marketplace eligibility together before you pick a plan.') if C.get('medicaid') else ''
    # counties
    ag = agg[sname]; unit = 'parishes' if st['unit'] == 'parishes' else 'counties'
    items = []
    for k in ag['order'][:10]:
        items.append(f'      <li><a href="/{slugmap[k]}">{esc(g.display(cen[k]))}</a></li>')
    # faq
    qas = []
    if s_ and e_:
        qas.append((f"When is ACA open enrollment in {sname}?", f"Open enrollment for 2027 coverage in {sname} runs from {s_} to {e_}, according to {esc(ex)}. Dates can change, so confirm on the Marketplace site before you plan around them."))
    qas.append((f"Did the enhanced ACA tax credits end?", PTC + " Your subsidy depends on your income and the plans available where you live, so we check it for you."))
    qas.append((f"Can I get help choosing an ACA plan in {sname}?", f"Yes. We are an independent agency licensed in {sname}. We compare plans, check your premium tax credit and Medicaid eligibility, and help you enroll by phone or video. Our help is free to you."))
    qas.append(("What if I miss open enrollment?", "A qualifying life event, such as losing job-based coverage, moving or a change in household, can open a Special Enrollment Period. See our guide to <a href=\"/lost-health-coverage\">losing health coverage</a> or call us."))
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "ACA Health Insurance", "item": BASE + "/aca-health-insurance"},
            {"@type": "ListItem", "position": 3, "name": sname, "item": canon}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', html.unescape(a))}} for q, a in qas]},
        {"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance", "telephone": "+1-571-354-0146",
         "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA", "postalCode": "22182", "addressCountry": "US"},
         "areaServed": {"@type": "AdministrativeArea", "name": sname}, "url": canon},
    ]
    doi_n, doi_u = g.DOI[sname]
    res = [f'      <li>{link(ex_url, ex)}: the official {sname} Marketplace for 2027 coverage.</li>',
           '      <li><a href="https://www.healthcare.gov/" rel="noopener" target="_blank">HealthCare.gov</a>: federal Marketplace information.</li>']
    if j.get('medicaid_url'):
        res.append(f'      <li>{link(j["medicaid_url"], f"{sname} Medicaid")}: eligibility and how to apply.</li>')
    res.append(f'      <li>{link(doi_u, doi_n)}: {sname}&rsquo;s insurance regulator, including agent license lookup.</li>')
    guides = [('/blog/aca-open-enrollment-deadline-can-i-sign-up-late', 'ACA open enrollment deadline: can I sign up late?'),
              ('/blog/can-i-keep-my-aca-subsidy-if-my-income-changes', 'Can I keep my ACA subsidy if my income changes?'),
              ('/blog/bronze-vs-silver-vs-gold-aca-plans', 'Bronze vs. silver vs. gold ACA plans'),
              ('/blog/hmo-vs-ppo-vs-epo-which-health-plan-type-is-right', 'HMO vs. PPO vs. EPO'),
              ('/blog/deductible-vs-out-of-pocket-maximum-explained', 'Deductible vs. out-of-pocket maximum'),
              ('/blog/how-much-does-health-insurance-cost-without-a-job', 'How much does health insurance cost without a job?')]
    gl = '\n'.join(f'      <li><a href="{h_}">{esc(t_)}</a></li>' for h_, t_ in guides)
    body = f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/aca-health-insurance">ACA Health Insurance</a> &rsaquo; {sname}</div>
    <h1>ACA health insurance in <em>{sname}</em>: 2027 enrollment and help</h1>
    <p class="lead">{lead}</p>
    <p class="sans" style="font-size:14px;color:#aebbd0;letter-spacing:.3px;margin-top:4px">Independent agency &middot; Luay Sadqi, Licensed Agent, NPN 21370662</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="tel:+15713540146">&#128222; Call (571) 354-0146</a>
      <a class="btn-ghost" href="/#contact">Request a callback</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>{sname} ACA Marketplace at a glance</h2>
    <div class="table-wrap">
      <table class="compare">
        <thead>
          <tr><th>&nbsp;</th><th>{sname}</th></tr>
        </thead>
        <tbody>
{tbl}
        </tbody>
      </table>
    </div>
    <p class="sans" style="font-size:14px;color:var(--muted)">Facts verified from the sources linked above as of October 2026. Dates and rules can change; confirm on the official Marketplace site before you act.</p>

    <h2>Help with the cost of coverage in {sname}</h2>
    <p>Premium tax credits lower your monthly Marketplace premium based on your household income and the cost of local plans. The enhanced federal credits that applied through 2025 have expired, so many households pay more than before. To know your number, run it with your real income. Our <a href="/blog/can-i-keep-my-aca-subsidy-if-my-income-changes">subsidy guide</a> explains what happens if your income changes during the year.</p>
{f'    <h2>Medicaid in {sname}</h2>{chr(10)}    <p>{med}</p>' if med else ''}
    <h2>Plan choices and networks in {sname}</h2>
    <p>Marketplace plans come in bronze, silver, gold and platinum levels, and networks differ by insurer and by where you live. Compare the <a href="/blog/bronze-vs-silver-vs-gold-aca-plans">metal tiers</a>, check that your doctors and hospitals are in network, and look at the <a href="/blog/deductible-vs-out-of-pocket-maximum-explained">deductible and out-of-pocket maximum</a>, not just the premium.</p>

    <h2>Business owners and self-employed in {sname}</h2>
    <p>If you run a business, you may have better options than the individual Marketplace. See <a href="/ichra">ICHRA</a> (an employer allowance for employees&rsquo; individual plans), <a href="/group-health-insurance-shop">group health and SHOP</a>, and <a href="/self-employed-health-insurance">self-employed health insurance</a>.</p>

    <h2>ACA help by {unit[:-3] if unit == 'parishes' else 'county'} in {sname}</h2>
    <p>Marketplace plans and prices are set by area, so they can differ across {sname}. Here are the 10 largest {unit}. See all of them in our <a href="/{st['slug']}-counties">{sname} directory</a>.</p>
    <ul>
{chr(10).join(items)}
    </ul>

    <h2>Official {sname} resources</h2>
    <ul>
{chr(10).join(res)}
    </ul>

    <h2>Helpful guides</h2>
    <ul>
{gl}
    </ul>

    <div class="callout">
      <strong>Free to you.</strong> Carriers pay us when you enroll, and your premium is the same whether you use an agent or enroll yourself. We are an independent agency, not connected with the Marketplace or any government agency.
    </div>

    <div class="cta-strip">
      <h3>Let&rsquo;s check your {sname} options together</h3>
      <p class="sans">We run your income through the subsidy rules and compare plans for your doctors. No cost, no pressure.</p>
      <a class="btn-primary sans" href="/#contact">Get my plan comparison</a>
    </div>
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">{sname} ACA FAQ</h2>
{g.faq_html(qas)}
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
    <div class="kicker" style="text-align:center;margin-bottom:20px">More {sname} coverage</div>
    <div class="grid-3">
      <a class="rel-card" href="/aca-health-insurance"><h3>ACA health insurance</h3><p>How Marketplace plans and subsidies work nationwide.</p></a>
      <a class="rel-card" href="{hub}"><h3>{sname} Medicare</h3><p>Medicare help for {sname} residents, by phone or video.</p></a>
      <a class="rel-card" href="/{st['slug']}-counties"><h3>{sname} by {unit[:-3] if unit == 'parishes' else 'county'}</h3><p>Local numbers and free help in every {unit[:-3] if unit == 'parishes' else 'county'}.</p></a>
    </div>
  </div>
</section>

'''
    page = g.head(title, desc, canon, f"ACA health insurance help for {sname} residents, by phone or video.", ld) + hdr.replace('@@BANNER@@', banner) + body + foot
    return slug, page


def main():
    cen, pen, hosp = g.load(); agg = g.build_agg(cen, pen)
    slugmap = json.load(open(os.path.join(ROOT, 'scripts', 'county_data', 'slugmap.json')))
    hdr, foot = shell()
    made, urls, missing = 0, [], []
    for sname, st in g.STATES.items():
        p = os.path.join(DATA, f"{st['slug']}.json")
        if not os.path.exists(p):
            missing.append(sname); continue
        j = json.load(open(p))
        slug, page = build(sname, st, j, cen, pen, agg, slugmap, hdr, foot)
        open(os.path.join(SITE, slug + '.html'), 'w').write(page)
        urls.append(slug); made += 1
    print('pages', made, 'missing data for', missing)
    if urls:
        sm = open(os.path.join(SITE, 'sitemap.xml')).read()
        add = ''.join(f'  <url>\n    <loc>{BASE}/{u}</loc>\n    <lastmod>2026-10-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n' for u in urls if f'/{u}<' not in sm)
        if add:
            open(os.path.join(SITE, 'sitemap.xml'), 'w').write(sm.replace('</urlset>', add + '</urlset>'))


if __name__ == '__main__':
    main()
