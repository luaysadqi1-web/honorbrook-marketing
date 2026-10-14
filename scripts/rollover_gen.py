#!/usr/bin/env python3
"""Generates the annuity-rollover pillar page and the account-type posts.

Output:
  site/retirement-rollover-annuity.html            (pillar)
  site/blog/<slug>.html                            (9 account-type posts)

Head, header, state block, band and footer are copied from an existing post so they stay in sync with the site.
Every rule stated here was read on irs.gov (or Rev. Proc. 2011-38 / IRB 2024-33) on 2026-10-13; see ANNUITY-ROLLOVER-STRATEGY.md.
Anything not confirmed there is phrased as a question to ask, never as a fact. Idempotent: rerun to regenerate.
Registration (blog index, sitemap, llms.txt) is done by scripts/rollover_register.py.
"""
import re, os, json, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = os.path.join(ROOT, 'site')
TEMPLATE = os.path.join(SITE, 'blog', 'ira-rollover-into-an-annuity-what-to-ask-first.html')
BASE = 'https://honorbrook-insurance.com'
DATE = '2026-10-13'
BYLINE = 'By Luay Sadqi, Licensed Agent (NPN 21370662) · October 2026'

S = {  # IRS and primary sources: key -> (url, label)
    'roll': ('https://www.irs.gov/retirement-plans/plan-participant-employee/rollovers-of-retirement-plan-and-ira-distributions', 'IRS: Rollovers of retirement plan and IRA distributions'),
    'chart': ('https://www.irs.gov/pub/irs-tege/rollover_chart.pdf', 'IRS rollover chart (PDF)'),
    'tc413': ('https://www.irs.gov/taxtopics/tc413', 'IRS Topic 413: Rollovers from retirement plans'),
    'simple': ('https://www.irs.gov/retirement-plans/simple-ira-withdrawal-and-transfer-rules', 'IRS: SIMPLE IRA withdrawal and transfer rules'),
    'rmd': ('https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-required-minimum-distributions-rmds', 'IRS: Retirement topics, required minimum distributions'),
    'early': ('https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-exceptions-to-tax-on-early-distributions', 'IRS: Exceptions to tax on early distributions'),
    'tc558': ('https://www.irs.gov/taxtopics/tc558', 'IRS Topic 558: Additional tax on early distributions from retirement plans other than IRAs'),
    'bene': ('https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-beneficiary', 'IRS: Retirement topics, beneficiary'),
    'p571': ('https://www.irs.gov/publications/p571', 'IRS Publication 571: Tax-sheltered annuity plans (403(b) plans)'),
    'faq403': ('https://www.irs.gov/retirement-plans/retirement-plans-faqs-regarding-403b-tax-sheltered-annuity-plans', 'IRS: FAQs regarding 403(b) plans'),
    'c457': ('https://www.irs.gov/retirement-plans/comparison-of-tax-exempt-457b-plans-and-governmental-457b-plans', 'IRS: Comparison of tax-exempt 457(b) plans and governmental 457(b) plans'),
    'snap457': ('https://www.irs.gov/retirement-plans/issue-snapshot-457b-plan-of-tax-exempt-entity-tax-consequences-of-noncompliance', 'IRS: Issue snapshot, 457(b) plan of a tax-exempt entity'),
    'rp1138': ('https://www.irs.gov/pub/irs-drop/rp-11-38.pdf', 'IRS Rev. Proc. 2011-38 (partial annuity exchanges)'),
    'irb': ('https://www.irs.gov/irb/2024-33_IRB', 'IRS Internal Revenue Bulletin 2024-33 (final QLAC regulations)'),
}

IMPORTANT = ('<div class="callout">\n  <strong>Important:</strong> this article is educational, not personalized advice. Annuity guarantees depend on the '
             "issuing company's claims-paying ability, and annuities can carry surrender charges and fees. They are not bank products or "
             'investments. Speak with a licensed professional and your tax advisor before moving money.\n</div>')
CTA = ('<div class="cta-strip">\n  <h3>%s</h3>\n  <p class="sans">Request a no-obligation Retirement Income Review. We explain your options in plain English, with no pressure '
       'and no promises of returns.</p>\n  <a class="btn-primary sans" href="/#contact">Request my Retirement Income Review</a>\n</div>')
CLOSE_NOTE = ('<p style="font-size:15.5px;color:var(--muted)"><em>This article is general information and is not tax, legal, investment or financial '
              "advice. Annuity guarantees depend on the issuing company&rsquo;s claims-paying ability, and surrender charges and fees may apply. "
              'A licensed agent can help with your situation.</em></p>')


def link(key, text=None):
    u, l = S[key]
    return '<a href="%s" rel="noopener" target="_blank">%s</a>' % (u, text or l)


def sources(keys):
    return '<h2>Where to check these rules</h2>\n<p>Every rule on this page comes from the IRS. Read the source for your situation:</p>\n<ul>\n%s\n</ul>' % \
        '\n'.join('  <li>%s</li>' % link(k) for k in keys)


def table(head, rows):
    return ('<div class="table-wrap">\n  <table class="compare">\n    <thead><tr>%s</tr></thead>\n    <tbody>\n%s\n    </tbody>\n  </table>\n</div>' %
            (''.join('<th>%s</th>' % h for h in head),
             '\n'.join('      <tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows)))


def ul(items):
    return '<ul>\n%s\n</ul>' % '\n'.join('  <li>%s</li>' % i for i in items)


def plain(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s))).strip()


T = open(TEMPLATE, encoding='utf-8').read()
HEAD_TOP = T[:T.index('<title>')]
BODY_TOP = T[T.index('</head>'):T.index('<section class="page-hero"')]
BAND = T[T.index('<div class="band">'):T.index('<section class="related">')]
FOOT = T[T.index('<footer>'):]
STATES = T[T.index('<h2>Availability and rules vary by state</h2>'):]
STATES = STATES[:STATES.index('</ul>') + len('</ul>')]
LDJSON = json.loads(re.findall(r'<script type="application/ld\+json">\s*(\{\s*"@context": "https://schema.org",\s*"@type": "BlogPosting".*?)</script>', T, re.S)[0])


def render(p, pillar=False):
    url = BASE + p['path']
    title = p['title']
    desc = p['desc']
    bc = [('Home', BASE + '/')]
    bc += [(n, BASE + h) for n, h in p['crumbs']]
    bc.append((p['crumb'], url))
    bc_json = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(bc)]}
    art = dict(LDJSON)
    art.update({'@type': 'Article' if pillar else 'BlogPosting', 'headline': plain(p['h1']), 'description': desc,
                'datePublished': DATE, 'dateModified': DATE, 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}})
    faq_json = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in p['faq']]}
    esc = lambda s: s.replace('"', '&quot;')
    crumbs_html = ' &rsaquo; '.join('<a href="%s">%s</a>' % (h, n) for n, h in [('Home', '/')] + p['crumbs']) + ' &rsaquo; ' + p['crumb']
    head = (HEAD_TOP +
            '<title>%s</title>\n<meta name="description" content="%s">\n<link rel="icon" type="image/png" href="/favicon-64.png">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="canonical" href="%s">\n<meta name="theme-color" content="#142339">\n'
            '<meta name="robots" content="index, follow, max-image-preview:large">\n\n'
            '<meta property="og:site_name" content="Honorbrook Insurance">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n<meta property="og:type" content="article">\n<meta property="og:locale" content="en_US">\n'
            '<meta property="og:image" content="https://honorbrook-insurance.com/assets/og-image.jpg">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
            '<meta name="twitter:image" content="https://honorbrook-insurance.com/assets/og-image.jpg">\n\n<link rel="stylesheet" href="/assets/style.css">\n\n'
            % (title, esc(desc), url, esc(title), esc(desc), url, esc(title), esc(desc)))
    head += ''.join('<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(j, indent=2, ensure_ascii=False) for j in (bc_json, art, faq_json))
    hero = ('<section class="page-hero" id="maincontent" role="main">\n  <div class="wrap">\n    <div class="breadcrumb">%s</div>\n    <h1>%s</h1>\n'
            '    <p class="lead">%s</p>\n    <p class="byline sans">%s</p>\n  </div>\n</section>\n\n' % (crumbs_html, p['h1'], p['lead'], BYLINE))
    body = '\n'.join(p['body'])
    article = ('<article class="article">\n  <div class="wrap prose">\n%s\n\n    %s\n    %s\n  </div>\n</article>\n\n' % (body, STATES, CLOSE_NOTE))
    faq = ('<section class="faq">\n  <div class="wrap" style="max-width:880px">\n    <div class="kicker">Common questions</div>\n'
           '    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">%s</h2>\n%s\n'
           '    <p class="sans" style="margin-top:20px;font-style:italic">This article is general information, not insurance, tax, investment, or legal advice, '
           'and a licensed agent will help you weigh your specific situation.</p>\n  </div>\n</section>\n\n'
           % (p['faq_title'], '\n'.join('    <details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in p['faq'])))
    related = ('<section class="related">\n  <div class="wrap">\n    <div class="kicker" style="text-align:center;margin-bottom:20px">Keep exploring</div>\n    <div class="grid-3">\n%s\n'
               '    </div>\n  </div>\n</section>\n\n' % '\n'.join('      <a class="rel-card" href="%s"><h3>%s</h3><p>%s</p></a>' % r for r in p['related']))
    return head + BODY_TOP + hero + article + faq + BAND + related + FOOT


A = lambda h, t: '<a href="%s">%s</a>' % (h, t)
PILLAR = '/retirement-rollover-annuity'
B = '/blog/'
SL = {
    '403b': 'can-i-roll-my-403b-into-an-annuity',
    '457b': '457b-rollover-to-an-annuity-governmental-vs-non-governmental',
    'simple': 'simple-ira-and-sep-ira-rollover-to-an-annuity-the-two-year-rule',
    'pension': 'pension-lump-sum-or-monthly-payments-and-rolling-into-an-annuity',
    'inherited': 'inherited-ira-and-annuities-spouse-vs-non-spouse-rollover-rules',
    'x1035': '1035-exchange-annuity-the-180-day-rule-explained',
    'qlac': 'qlac-longevity-annuity-and-required-minimum-distributions',
    'roth': 'roth-ira-and-roth-401k-rollover-to-an-annuity',
    'age55': 'age-55-rule-what-you-lose-rolling-a-401k-into-an-ira-annuity',
}
EXIST = {
    'ira': (B + 'ira-rollover-into-an-annuity-what-to-ask-first', 'Rollover into an annuity: what to ask first'),
    '401k': (B + 'what-to-do-with-your-401k-when-you-retire-or-leave-a-job', 'What to do with your 401(k)'),
    'tsp': (B + 'can-i-roll-over-my-tsp-to-an-ira-or-401k', 'Rolling over your TSP'),
    'tax': (B + 'how-are-annuities-taxed', 'How annuities are taxed'),
    'fia': (B + 'what-is-a-fixed-indexed-annuity-fia', 'What a fixed indexed annuity is'),
    'spia': (B + 'what-is-a-single-premium-annuity-who-is-it-for', 'Single-premium annuities'),
}
REL = {  # rel-card tuples (href, title, blurb)
    'pillar': (PILLAR, 'Every rollover account', 'Which retirement accounts can fund an annuity, and the trap for each.'),
    'annuities': ('/annuities', 'Annuities', 'Fixed, indexed, and single-premium options explained.'),
    'tax': (EXIST['tax'][0], 'How annuities are taxed', 'What is taxed, when, and how the rules differ by account.'),
    'ira': (EXIST['ira'][0], 'Rollover into an annuity', 'The questions to ask before you move money.'),
    '401k': (EXIST['401k'][0], 'Your 401(k) options', 'Leave it, move it, roll it, or cash out.'),
    'fia': (EXIST['fia'][0], 'Fixed indexed annuities', 'How crediting, caps and surrender charges work.'),
    'spia': (EXIST['spia'][0], 'Single-premium annuities', 'Turning a lump sum into income.'),
}
for k, s in SL.items():
    REL[k] = (B + s, '', '')

pages = []

# ---------------------------------------------------------------- pillar
pages.append(dict(
    path=PILLAR, crumbs=[('Annuities', '/annuities')], crumb='Retirement Rollovers', pillar=True,
    title='Retirement Rollover to an Annuity: Every Account Type | Honorbrook',
    desc='Which retirement accounts can fund an annuity? IRA, 401(k), 403(b), 457(b), SIMPLE, SEP, pension and inherited IRA, with the IRS rule and the trap for each.',
    h1='Rolling Retirement Money Into an <em>Annuity</em>: Every Account Type, What Is Allowed and the Traps',
    lead=('Most retirement accounts can be moved into an annuity, usually by rolling them to an IRA first, but not all of them, and each type has its own trap. '
          'A non-governmental 457(b) cannot be rolled over at all, a SIMPLE IRA is locked for two years, and a check made out to you from a plan triggers 20% withholding.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>Which accounts can fund an annuity?</h2>',
        '    <p>An annuity is bought with money that is already in an IRA or a plan, or with money from another annuity. The question is whether the account you have can legally move there without tax. This table is based on the ' + link('chart', 'IRS rollover chart') + ' and the IRS pages linked below it.</p>',
        '    ' + table(['Account', 'Can it move to an IRA or annuity?', 'The main trap', 'Guide'], [
            ['Traditional IRA', 'Yes, by direct transfer or rollover', 'A rollover you receive yourself counts against a one-per-12-months limit across all your IRAs. Direct transfers do not.', A(EXIST['ira'][0], 'Read')],
            ['Roth IRA', 'Only to another Roth IRA', 'It cannot move to a traditional IRA or a plan.', A(REL['roth'][0], 'Read')],
            ['SEP IRA', 'Yes', 'It counts toward the same one-per-12-months limit.', A(REL['simple'][0], 'Read')],
            ['SIMPLE IRA', 'Only to another SIMPLE IRA for your first two years in the plan; after that, yes', 'Breaking the two-year rule means income tax plus a 25% additional tax if you are under 59&frac12;.', A(REL['simple'][0], 'Read')],
            ['401(k) at a former employer', 'Yes, to an IRA or another plan', 'A check payable to you has 20% withheld. Required minimum distributions cannot be rolled.', A(EXIST['401k'][0], 'Read')],
            ['401(k) at a current employer', 'Only if the plan lets you take a distribution while you work', 'The plan document decides, not the IRS.', A(REL['age55'][0], 'Read')],
            ['403(b)', 'Yes, generally to a traditional IRA', 'Hardship payments and lifetime installment payments cannot be rolled.', A(REL['403b'][0], 'Read')],
            ['Governmental 457(b)', 'Yes', 'The plan&rsquo;s exemption from the 10% additional tax does not carry into an IRA.', A(REL['457b'][0], 'Read')],
            ['Non-governmental 457(b) or 457(f)', '<strong>No</strong>', 'An attempted rollover is treated as an excess contribution and is subject to an excise tax.', A(REL['457b'][0], 'Read')],
            ['Pension (defined benefit) lump sum', 'Yes, if the plan offers a lump sum', 'Monthly lifetime payments cannot be rolled, and the election may be impossible to undo.', A(REL['pension'][0], 'Read')],
            ['Inherited IRA', 'Depends on whether you are the spouse', 'Spouses and other heirs have different options and deadlines.', A(REL['inherited'][0], 'Read')],
            ['An existing annuity', 'Not a rollover: a 1035 exchange', 'It must move insurer to insurer, and partial exchanges have a 180-day rule.', A(REL['x1035'][0], 'Read')],
        ]),
        '    <p>Federal employees with a TSP should start with our guide to ' + A(EXIST['tsp'][0], 'rolling over the TSP') + '.</p>',
        '    <h2>Rules that apply to every rollover</h2>',
        '    ' + ul([
            '<strong>Direct is safer than a check.</strong> Ask the plan or IRA to send the money straight to the new institution. A plan distribution paid to you is subject to mandatory 20% withholding even if you plan to roll it over, and to roll over the full amount you must replace the withheld money from other funds (' + link('tc413', 'IRS Topic 413') + ').',
            '<strong>The 60-day clock.</strong> If you receive the money yourself, you generally have 60 days to deposit it in another plan or IRA. The IRS can waive the deadline in some cases where circumstances were beyond your control (' + link('roll') + ').',
            '<strong>One IRA rollover per 12 months.</strong> The limit applies across all your IRAs together, including SEP, SIMPLE, traditional and Roth. It does not apply to trustee-to-trustee transfers, Roth conversions, or rollovers between a plan and an IRA.',
            '<strong>Required minimum distributions cannot be rolled over.</strong> The IRS lists age 73 as the starting age on its current page, and your own date depends on your birth year, so confirm yours (' + link('rmd', 'IRS: required minimum distributions') + ').',
            '<strong>Report it.</strong> A rollover is not taxable when done correctly, but it is reportable on your federal tax return.',
        ]),
        '    <h2>What an annuity changes, and what it does not</h2>',
        '    <p>An IRA already defers taxes, so an annuity inside an IRA does not add tax deferral. What an annuity adds is a contract: possible income guarantees, protection features, or a way to turn savings into payments. What it costs is liquidity: many contracts carry surrender charges if you withdraw early, and the guarantees depend on the issuing company&rsquo;s claims-paying ability. Read ' + A(EXIST['tax'][0], 'how annuities are taxed') + ' and ' + A(EXIST['ira'][0], 'what to ask before you roll over') + ' first.</p>',
        '    <p>If you want to compare product types, start with ' + A('/annuities', 'our annuities overview') + ', ' + A(EXIST['fia'][0], 'fixed indexed annuities') + ' and ' + A(EXIST['spia'][0], 'single-premium annuities') + '.</p>',
        '    <h2>Which situation sounds like yours?</h2>',
        '    ' + ul([
            '<strong>You just left a job and have an old 401(k):</strong> ' + A(EXIST['401k'][0], 'your 401(k) options') + '.',
            '<strong>You work for a school, hospital or nonprofit:</strong> ' + A(REL['403b'][0], '403(b)') + ' or ' + A(REL['457b'][0], '457(b)') + '.',
            '<strong>You own a small business:</strong> ' + A(REL['simple'][0], 'SEP and SIMPLE IRAs') + '.',
            '<strong>You were offered a pension buyout:</strong> ' + A(REL['pension'][0], 'lump sum or monthly') + '.',
            '<strong>You are 55 to 59&frac12; and may need cash:</strong> ' + A(REL['age55'][0], 'the age 55 rule') + '.',
            '<strong>You are approaching required withdrawals:</strong> ' + A(REL['qlac'][0], 'QLACs and RMDs') + '.',
            '<strong>You already own an annuity:</strong> ' + A(REL['x1035'][0], 'the 1035 exchange') + '.',
            '<strong>You inherited an IRA:</strong> ' + A(REL['inherited'][0], 'spouse and non-spouse rules') + '.',
            '<strong>You have Roth money:</strong> ' + A(REL['roth'][0], 'Roth rollover rules') + '.',
        ]),
        '    ' + CTA % 'Want a second opinion before you move retirement money?',
        '    <h2>Questions to ask before any rollover</h2>',
        '    ' + ul([
            'Is this a direct rollover, and will the money go straight to the new institution?',
            'What surrender charges apply, for how long, and what can I take out each year without a charge?',
            'What are all the fees, including rider fees, and who is paid a commission?',
            'What will I give up by leaving my current account, such as plan features, exceptions to the 10% additional tax, or a lower-cost option?',
            'Does the contract&rsquo;s start date or payout schedule fit when I will actually need the money?',
            'Who is the issuing company, and what is its financial strength rating from independent agencies?',
            'What does my tax professional say about the tax result?',
        ]),
        '    <h2>Take your time</h2>',
        '    <p>A reputable carrier gives you a free-look period after you receive the contract, during which you can cancel and get your money back under the contract terms and state law. Use it to read the entire contract and share it with your tax professional. If anyone says an offer disappears unless you sign today, that is a reason to slow down.</p>',
        '    ' + sources(['chart', 'roll', 'tc413', 'simple', 'rmd', 'c457', 'rp1138']),
    ],
    faq_title='Retirement Rollover FAQ',
    faq=[
        ('Which retirement accounts can be rolled into an annuity?',
         'Traditional, SEP and (after two years) SIMPLE IRAs, 401(k)s, 403(b)s, governmental 457(b)s and pension lump sums can generally be rolled to an IRA, which can then hold an annuity. A non-governmental 457(b) cannot be rolled over, and a Roth IRA can move only to another Roth IRA.'),
        ('Is rolling a 401(k) into an annuity taxable?',
         'A direct rollover to a traditional IRA is generally not taxable when done correctly. A distribution paid to you can have 20% withheld, and money you do not deposit within 60 days is generally taxable. Moving pre-tax money to a Roth IRA is taxable as income.'),
        ('Does an annuity in an IRA give extra tax benefits?',
         'No. The IRA already defers tax, so the reason to use an annuity is its contract features, such as income options, not extra tax deferral.'),
        ('Is a 1035 exchange the same as a rollover?',
         'No. A 1035 exchange moves one annuity into another and must go directly between insurers. A rollover moves money between retirement accounts.'),
    ],
    related=[REL['annuities'], REL['ira'], REL['tax']],
))

# ---------------------------------------------------------------- 403(b)
pages.append(dict(
    path=B + SL['403b'], crumbs=[('Blog', '/blog/')], crumb='403(b) to an Annuity',
    title='Can I Roll My 403(b) Into an Annuity? | Honorbrook',
    desc='A 403(b) can generally be rolled to an IRA tax-free and then used to buy an annuity. See what cannot be rolled, when you can take money out, and the traps first.',
    h1='Can I Roll My <em>403(b)</em> Into an Annuity? Rules, Taxes and Traps',
    lead=('Usually yes. A 403(b) distribution can generally be rolled tax-free to a traditional IRA, and an annuity can then be bought inside that IRA, but only if your plan lets you take the money out '
          'and the payment is an eligible rollover distribution. Hardship payments, required minimum distributions and lifetime installment payments cannot be rolled.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>When can you take money out of a 403(b)?</h2>',
        '    <p>Under IRS Publication 571, payments from a 403(b) generally cannot begin until you reach age 59&frac12;, leave your employer, die or become disabled, or, for your own contributions, face a financial hardship, plus a few special cases added in recent years (' + link('p571', 'Pub. 571') + '). So a teacher or nurse who is still working usually cannot roll over an active 403(b) unless the plan allows it. The plan document decides, so ask your plan administrator.</p>',
        '    <h2>What can and cannot be rolled over</h2>',
        '    ' + ul([
            '<strong>Can be rolled:</strong> all or part of an eligible distribution to a traditional IRA or another non-Roth eligible plan, tax-free.',
            '<strong>Roth IRA:</strong> a distribution can be converted to a Roth IRA by direct rollover, but the converted amount is generally included in that year&rsquo;s taxable income.',
            '<strong>Cannot be rolled tax-free:</strong> required minimum distributions, payments that are a series of substantially equal payments over your life, the joint lives of you and a beneficiary, or 10 years or more, hardship distributions, and corrective distributions of excess contributions.',
        ]),
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>Withholding.</strong> A taxable eligible rollover distribution paid to you from an employer plan is subject to mandatory withholding, generally 20%, even if you intend to roll it over (' + link('tc413', 'IRS Topic 413') + '). Ask for a direct rollover instead.',
            '<strong>The age 55 exception.</strong> The IRS lists an exception to the 10% additional tax for leaving your employer in or after the year you turn 55 for qualified plans but not for IRAs (' + link('early', 'IRS exceptions table') + '). If you are between 55 and 59&frac12; and may need cash, ask your tax professional whether your 403(b) qualifies before you roll it to an IRA.',
            '<strong>Contract exchanges are different.</strong> A 403(b) can be held in annuity contracts, and the IRS has separate rules for exchanging one 403(b) contract for another inside the plan (' + link('faq403', 'IRS 403(b) FAQs') + '). If your 403(b) is already an annuity, ask the current issuer about surrender charges before you move it.',
            '<strong>Loans and after-tax money.</strong> A loan treated as a distribution cannot be rolled over. If any of your balance is after-tax money, ask the plan how it can be rolled.',
        ]),
        '    <h2>What the annuity changes</h2>',
        '    <p>Once the money is in a traditional IRA, it follows IRA rules, including required minimum distributions, whether it sits in an annuity or not. The 403(b) did not need an annuity to defer tax, so the question is whether you want the contract features and can accept the surrender charges. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + ' and ' + A(EXIST['ira'][0], 'what to ask before you move money') + '.</p>',
        '    ' + CTA % 'Rolling over a 403(b)? Get a second opinion first.',
        '    <h2>Questions to ask your 403(b) plan</h2>',
        '    ' + ul([
            'Am I eligible to take a distribution now, and under which event?',
            'Can the plan send a direct rollover to an IRA, and what paperwork does the receiving company need?',
            'Are any of my contracts annuities with surrender charges, and what is the schedule?',
            'Do I have a loan outstanding, or any after-tax money?',
            'What happens to the money if I leave it in the plan instead?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>Compare with ' + A(REL['457b'][0], 'a 457(b)') + ' and ' + A(REL['age55'][0], 'the age 55 rule') + ', and see ' + A(EXIST['tax'][0], 'how annuities are taxed') + '.</p>',
        '    ' + sources(['p571', 'faq403', 'roll', 'tc413', 'early']),
    ],
    faq_title='403(b) Rollover FAQ',
    faq=[
        ('Can I roll a 403(b) into an annuity while I still work?',
         'Only if your plan permits a distribution. The IRS lists age 59&frac12;, leaving your employer, death, disability and hardship among the events that can allow payments. Check your plan document.'),
        ('Is a 403(b) rollover to an annuity taxable?',
         'A direct rollover to a traditional IRA is generally not taxable when done correctly. Converting the money to a Roth IRA is generally taxable as income in the year of the distribution.'),
        ('My 403(b) is already an annuity. Can I still move it?',
         'Often yes, but ask the current issuer about surrender charges and about how contract exchanges within a 403(b) differ from a rollover to an IRA.'),
    ],
    related=[REL['pillar'], REL['457b'], REL['tax']],
))

# ---------------------------------------------------------------- 457(b)
pages.append(dict(
    path=B + SL['457b'], crumbs=[('Blog', '/blog/')], crumb='457(b) to an Annuity',
    title='457(b) Rollover to an Annuity: Which Plans Qualify | Honorbrook',
    desc='A governmental 457(b) can be rolled to an IRA, but a non-governmental 457(b) cannot be rolled at all. Learn how to tell which you have and what changes after a rollover.',
    h1='<em>457(b)</em> Rollover to an Annuity: Governmental vs. Non-Governmental Plans',
    lead=('It depends on who your employer is. A governmental 457(b), offered by a state or local government, can generally be rolled to an IRA and then used to buy an annuity. '
          'A 457(b) from a tax-exempt employer, such as a nonprofit, cannot be rolled over at all, and an attempted rollover creates an excise-tax problem.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>The two kinds of 457(b)</h2>',
        '    ' + table(['', 'Governmental 457(b)', 'Tax-exempt employer 457(b)'], [
            ['Who offers it', 'State and local governments', 'Nonprofits and other tax-exempt employers'],
            ['Rollover to a 401(k), 403(b), governmental 457(b) or IRA', 'Yes', '<strong>No</strong>'],
            ['If you try anyway', 'Not applicable', 'Treated as an excess contribution, subject to an excise tax'],
        ]),
        '    <p>Source: ' + link('c457', 'IRS comparison of 457(b) plans') + ' and the ' + link('snap457', 'IRS issue snapshot') + '. The IRS says the same for 457(f) plans.</p>',
        '    <h2>How to tell which one you have</h2>',
        '    <p>Ask your plan administrator or HR department in writing: &ldquo;Is this a governmental 457(b) plan?&rdquo; The summary plan description usually states the employer type. Do not guess, because the cost of guessing wrong is a tax problem, not just a delay.</p>',
        '    <h2>The traps with a governmental 457(b)</h2>',
        '    ' + ul([
            '<strong>You can lose the early-withdrawal advantage.</strong> The IRS says distributions from a governmental 457(b) are generally not subject to the 10% additional tax on early distributions, except for amounts that were rolled into the plan from other plans or IRAs (' + link('tc558', 'IRS Topic 558') + '). Money rolled into an IRA is IRA money, and IRA withdrawals before age 59&frac12; are subject to the 10% additional tax unless an exception applies.',
            '<strong>Withholding.</strong> A taxable eligible rollover distribution paid to you from an employer plan is subject to mandatory withholding, generally 20% (' + link('tc413', 'IRS Topic 413') + '). Use a direct rollover.',
            '<strong>Hardship payments.</strong> Payments for an unforeseeable emergency are hardship distributions, which cannot be rolled over (' + link('roll') + ').',
            '<strong>Required minimum distributions.</strong> These cannot be rolled over either.',
        ]),
        '    <h2>Where an annuity fits</h2>',
        '    <p>An annuity is bought inside an IRA after the rollover. The IRA already defers tax, so the case for an annuity rests on its contract features, not on extra tax deferral. A younger retiree who may need to withdraw before 59&frac12; should weigh two costs together: the loss of the 457(b) exception and any surrender charge on the annuity. Ask your tax professional to run the numbers before you decide. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + '.</p>',
        '    ' + CTA % 'Not sure which kind of 457(b) you have?',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'Is my plan governmental or tax-exempt?',
            'If governmental, can the plan send a direct rollover to an IRA?',
            'How much of my balance came from other plans or IRAs, since that part is treated differently?',
            'Do I expect to need money before 59&frac12;, and what would it cost from an IRA annuity?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>Compare with ' + A(REL['403b'][0], 'a 403(b)') + ', and read ' + A(REL['age55'][0], 'the age 55 rule') + ' and ' + A(EXIST['tax'][0], 'how annuities are taxed') + '.</p>',
        '    ' + sources(['c457', 'snap457', 'tc558', 'tc413', 'roll']),
    ],
    faq_title='457(b) Rollover FAQ',
    faq=[
        ('Can I roll a nonprofit 457(b) into an IRA?',
         'No. The IRS says distributions from a 457(b) maintained by a tax-exempt entity cannot be rolled over, and an attempted rollover is treated as an excess contribution subject to an excise tax.'),
        ('Is a 457(f) plan the same as a 457(b)?',
         'No. They are different arrangements, but the IRS says distributions from 457(f) plans cannot be rolled over either.'),
        ('Will I owe the 10% additional tax after rolling a governmental 457(b) into an IRA annuity?',
         'Not on the rollover itself. But early withdrawals from an IRA before age 59&frac12; are generally subject to the 10% additional tax unless an exception applies, which is a difference from the 457(b).'),
    ],
    related=[REL['pillar'], REL['403b'], REL['age55']],
))

# ---------------------------------------------------------------- SIMPLE / SEP
pages.append(dict(
    path=B + SL['simple'], crumbs=[('Blog', '/blog/')], crumb='SIMPLE and SEP to an Annuity',
    title='SIMPLE and SEP IRA Rollover to an Annuity | Honorbrook',
    desc='A SEP IRA moves like any IRA, but a SIMPLE IRA has a two-year lock on transfers and a 25% additional tax if you break it. See the IRS rules before you move money.',
    h1='SIMPLE IRA and SEP IRA <em>Rollover</em> to an Annuity: The Two-Year Rule',
    lead=('A SEP IRA can generally move into an IRA annuity like any other IRA. A SIMPLE IRA can too, but only after two years from when you first participated in your employer&rsquo;s SIMPLE plan; '
          'before that, the money can go only to another SIMPLE IRA, and breaking the rule can mean income tax plus a 25% additional tax.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>The rules in one table</h2>',
        '    ' + table(['', 'SEP IRA', 'SIMPLE IRA'], [
            ['Roll to a traditional IRA', 'Yes', 'Only after the two-year period'],
            ['Roll to an employer plan (401(k), 403(b), governmental 457(b))', 'Yes', 'Only after the two-year period'],
            ['Roll to a Roth IRA', 'Yes, the untaxed amount is included in income', 'After two years, and the untaxed amount is included in income'],
            ['First two years in the plan', 'No special lock', 'Only another SIMPLE IRA'],
        ]),
        '    <p>Source: the ' + link('chart', 'IRS rollover chart') + ' and ' + link('simple', 'IRS SIMPLE IRA transfer rules') + '.</p>',
        '    <h2>How the two-year clock works</h2>',
        '    <p>The IRS counts two years from the date you first participated in your employer&rsquo;s SIMPLE IRA plan. During that period, a transfer to anything other than another SIMPLE IRA is treated as a withdrawal: you include the amount in income and pay an additional 25% tax, unless you are at least 59&frac12; at the time of the transfer or qualify for another exception. Note the nuance: being over 59&frac12; avoids the 25% additional tax, but the amount is still included in your income.</p>',
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>10% becomes 25%.</strong> Withdrawals from a SIMPLE IRA before 59&frac12; normally face a 10% additional tax, which rises to 25% within two years of first participating.',
            '<strong>One rollover per 12 months.</strong> The limit applies across all your IRAs together, including SEP and SIMPLE. It does not apply to trustee-to-trustee transfers, so ask for a direct transfer (' + link('roll') + ').',
            '<strong>Do not take a check.</strong> A check payable to you can start the 60-day clock and count as your one rollover for the year.',
            '<strong>Ownership paperwork.</strong> Keep the SIMPLE IRA statements that show your first participation date. Ask your plan sponsor or the custodian for it in writing.',
        ]),
        '    <h2>Where an annuity fits</h2>',
        '    <p>After a valid rollover, the money is in a traditional IRA and follows IRA rules. Buying an annuity inside it does not add tax deferral, and it can add surrender charges. For a business owner who still contributes to a SEP or SIMPLE plan, an annuity is one of several ways to hold the rolled money, not a replacement for the plan. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + '.</p>',
        '    ' + CTA % 'Own a small business? Check the timeline before you move.',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'What was the date I first participated in the SIMPLE IRA plan?',
            'Can this be done as a trustee-to-trustee transfer?',
            'Have I done another IRA-to-IRA rollover in the last 12 months?',
            'Will the annuity sit in a traditional IRA or a Roth IRA, and what is the tax result of that choice?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(REL['roth'][0], 'Roth rollovers') + ', ' + A(REL['age55'][0], 'the age 55 rule') + ' and ' + A(EXIST['tax'][0], 'how annuities are taxed') + '.</p>',
        '    ' + sources(['simple', 'chart', 'roll', 'early']),
    ],
    faq_title='SIMPLE and SEP Rollover FAQ',
    faq=[
        ('Can I move a SIMPLE IRA into an annuity in my first two years?',
         'Not without tax. During the first two years, the IRS says a transfer can go only to another SIMPLE IRA. Otherwise it is treated as a withdrawal and an additional 25% tax can apply.'),
        ('Does the one-rollover-per-year rule apply to a direct transfer?',
         'No. The IRS says the one-per-12-months limit does not apply to trustee-to-trustee transfers between IRAs.'),
        ('If I am over 59&frac12;, does the two-year rule still matter?',
         'Partly. The 25% additional tax does not apply if you are at least 59&frac12;, but a transfer made in violation of the two-year rule is still treated as a withdrawal included in your income.'),
    ],
    related=[REL['pillar'], REL['roth'], REL['tax']],
))

# ---------------------------------------------------------------- pension
pages.append(dict(
    path=B + SL['pension'], crumbs=[('Blog', '/blog/')], crumb='Pension Lump Sum',
    title='Pension Lump Sum vs Monthly: Rolling Into an Annuity | Honorbrook',
    desc='Offered a pension lump sum? Learn what can be rolled over, what cannot, and the questions to ask before trading lifetime monthly pension payments for an annuity.',
    h1='Pension <em>Lump Sum</em> or Monthly Payments? Rolling It Into an Annuity',
    lead=('If your pension plan offers a lump sum, that lump sum can generally be rolled over to an IRA, and an annuity can then be bought inside the IRA. Monthly lifetime payments cannot be rolled over, '
          'and the choice is a plan election that may be hard or impossible to undo. Ask the plan for the numbers before you decide.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>What can be rolled over</h2>',
        '    <p>The IRS rollover chart treats defined benefit pension plans as qualified plans, so an eligible lump-sum distribution can be rolled to a traditional IRA (' + link('chart', 'IRS rollover chart') + '). But a distribution that is one of a series of substantially equal payments, such as a monthly pension for life, is not an eligible rollover distribution, and neither is a required minimum distribution (' + link('roll') + '). In plain terms: you can roll a lump sum, but you cannot roll monthly pension checks.</p>',
        '    <h2>Two paths side by side</h2>',
        '    ' + table(['', 'Keep the monthly pension', 'Take the lump sum and roll it'], [
            ['What you receive', 'Monthly payments set by the plan formula and the survivor option you choose', 'A lump sum you control and can turn into income with a product you choose'],
            ['Can you change your mind?', 'Elections are usually final once payments start; ask the plan', 'A completed direct rollover cannot be undone; an annuity has a free-look period, then surrender charges'],
            ['Taxes', 'Monthly payments are generally taxed as income when received', 'A direct rollover to a traditional IRA is generally not taxed until withdrawn'],
            ['If you die first', 'Depends on the survivor option you elected', 'Depends on your beneficiary designation and the contract'],
        ]),
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>Withholding.</strong> A taxable lump sum paid to you is subject to mandatory withholding, generally 20%, and you must replace it from other funds to roll over the full amount (' + link('tc413', 'IRS Topic 413') + '). Choose a direct rollover.',
            '<strong>An irreversible choice.</strong> Once payments begin or the money is rolled, you may not be able to go back. Ask in writing whether the election can be changed and until when.',
            '<strong>Comparing unlike things.</strong> A pension&rsquo;s monthly amount and an annuity&rsquo;s payout are not the same kind of promise. Ask for the plan&rsquo;s lump-sum figure and the monthly figure side by side, and for an annuity quote with all fees and surrender charges stated.',
            '<strong>Someone else&rsquo;s sales pitch.</strong> Be cautious of anyone who says you will &ldquo;get more&rdquo; without showing the comparison on paper.',
        ]),
        '    <h2>Where an annuity fits</h2>',
        '    <p>Some retirees use an annuity inside the IRA to rebuild a stream of payments after taking a lump sum. Whether that is better than the pension depends on the survivor benefit, the interest-rate environment, the carrier and your health, and an annuity&rsquo;s guarantees depend on the issuing company&rsquo;s claims-paying ability. See ' + A(EXIST['spia'][0], 'single-premium annuities') + ' and ' + A(REL['pillar'][0], 'every rollover account at a glance') + '.</p>',
        '    ' + CTA % 'Weighing a pension buyout? Get the comparison on paper.',
        '    <h2>Questions to ask the pension plan</h2>',
        '    ' + ul([
            'What is the lump-sum amount, and how is it calculated? Does it change with the date I elect?',
            'What is the monthly amount, with and without a survivor benefit?',
            'Does my spouse have to consent to a lump sum?',
            'Can the lump sum be sent as a direct rollover, and by what date must I elect?',
            'Can I change my election after I make it?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(EXIST['401k'][0], 'your 401(k) options') + ', ' + A(EXIST['tsp'][0], 'rolling over a TSP') + ' and ' + A(EXIST['tax'][0], 'how annuities are taxed') + '.</p>',
        '    ' + sources(['chart', 'roll', 'tc413']),
    ],
    faq_title='Pension Lump Sum FAQ',
    faq=[
        ('Can I roll my pension into an annuity?',
         'If the plan offers a lump sum, that lump sum can generally be rolled to an IRA, which can then buy an annuity. Monthly lifetime pension payments cannot be rolled over.'),
        ('Will taxes be withheld on a pension lump sum?',
         'If it is paid to you, mandatory withholding of generally 20% applies. A direct rollover to an IRA avoids the withholding.'),
        ('Can I change my mind after choosing monthly payments?',
         'Usually not once payments begin, but the rules are set by your plan, so ask in writing before you elect.'),
    ],
    related=[REL['pillar'], REL['spia'], REL['401k']],
))

# ---------------------------------------------------------------- inherited IRA
pages.append(dict(
    path=B + SL['inherited'], crumbs=[('Blog', '/blog/')], crumb='Inherited IRA and Annuities',
    title='Inherited IRA and Annuities: Spouse vs Non-Spouse | Honorbrook',
    desc='A spouse can roll an inherited IRA into their own IRA. Other heirs follow different payout rules, including the 10-year rule. Check the IRS options before an annuity.',
    h1='<em>Inherited IRA</em> and Annuities: Spouse vs. Non-Spouse Rollover Rules',
    lead=('A surviving spouse who inherits an IRA has the most options, including rolling it into their own IRA. Other beneficiaries generally must follow payout rules such as the 10-year rule, and a mistaken '
          'transfer can end the favorable treatment. Before any money goes into an annuity, confirm what kind of beneficiary you are.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>What the IRS says your options depend on</h2>',
        '    <p>The IRS says the rules depend on your relationship to the account owner, whether the owner died before or after their required beginning date (the first date they had to take required distributions), and, for deaths after 2019, on whether you are an eligible designated beneficiary (' + link('bene', 'IRS: beneficiary') + ').</p>',
        '    ' + ul([
            '<strong>Surviving spouse:</strong> the IRS lists keeping it as an inherited account, taking distributions over your own life expectancy, and rolling the account into your own IRA, among the options, depending on timing. Whether a spouse is the sole beneficiary is determined by September 30 of the year after death.',
            '<strong>Eligible designated beneficiaries</strong> (a minor child of the owner, a disabled or chronically ill person, or someone not more than 10 years younger than the owner) can generally take distributions over a life-expectancy period.',
            '<strong>Other individual beneficiaries</strong> generally follow the 10-year rule.',
            '<strong>Any beneficiary</strong> of an IRA can generally take a lump sum at any time, and taxable distributions are included in income.',
        ]),
        '    <h2>Non-spouse transfers</h2>',
        '    <p>The IRS lists rolling the account into your own IRA as an option for a spouse, but not for other beneficiaries. For employer-plan money, such as a 403(b), the IRS says a non-spouse beneficiary can make a direct rollover only into an inherited IRA set up to receive the distribution, which stays an inherited account with the required distribution rules still applying (' + link('p571', 'IRS Pub. 571') + ').</p>',
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>Taking a check.</strong> A distribution paid to a non-spouse beneficiary is generally taxable income, not a rollover.',
            '<strong>Losing the &ldquo;inherited&rdquo; label.</strong> The account must stay titled as an inherited account unless you are a spouse electing to treat it as your own.',
            '<strong>A payout schedule that does not fit.</strong> If you have to take money out on a set schedule and the annuity charges for early withdrawals, ask for the surrender rules in writing before you buy.',
            '<strong>Inherited Roth IRAs.</strong> The IRS says beneficiaries of Roth IRAs are generally subject to required distribution rules too.',
        ]),
        '    <h2>Where an annuity fits</h2>',
        '    <p>Some carriers offer annuities that can be held in an inherited IRA. Availability, payout choices and whether a contract can meet the required distribution schedule vary by carrier and state, so ask for the answer in writing before moving anything. An annuity does not change the payout deadlines, and its guarantees depend on the issuing company&rsquo;s claims-paying ability. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + '.</p>',
        '    ' + CTA % 'Inherited an IRA? Talk it through before you transfer it.',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'Am I the spouse, a minor child, disabled or chronically ill, or someone else?',
            'When did the owner die, and had they already reached their required beginning date?',
            'Will the transfer be trustee-to-trustee into an account titled as inherited?',
            'Does the annuity&rsquo;s payout and surrender schedule fit the required withdrawals?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(REL['roth'][0], 'Roth rollovers') + ', ' + A(REL['qlac'][0], 'QLACs and required minimum distributions') + ' and ' + A(EXIST['tax'][0], 'how annuities are taxed') + '.</p>',
        '    ' + sources(['bene', 'p571', 'rmd']),
    ],
    faq_title='Inherited IRA FAQ',
    faq=[
        ('Can a non-spouse roll an inherited IRA into their own IRA?',
         'The IRS lists rolling the account into your own IRA as an option for a spouse, not for other beneficiaries. A non-spouse generally moves inherited money only by direct transfer into an account that stays titled as inherited.'),
        ('What is the 10-year rule?',
         'Most individual beneficiaries who are not eligible designated beneficiaries generally have 10 years from the owner&rsquo;s death to withdraw the full balance. The timing details depend on the facts, so confirm with a tax professional.'),
        ('Can I buy an annuity with an inherited IRA?',
         'Some carriers allow it, but availability varies. The annuity cannot change the required withdrawal timeline.'),
    ],
    related=[REL['pillar'], REL['roth'], REL['qlac']],
))

# ---------------------------------------------------------------- 1035
pages.append(dict(
    path=B + SL['x1035'], crumbs=[('Blog', '/blog/')], crumb='1035 Exchange',
    title='1035 Exchange for an Annuity: The 180-Day Rule | Honorbrook',
    desc='A 1035 exchange moves one annuity into another without immediate tax, but it must go insurer to insurer. Learn the IRS 180-day rule for partial exchanges and the traps.',
    h1='<em>1035 Exchange</em> for Annuities: What It Is and the 180-Day Rule',
    lead=('A 1035 exchange lets you swap one annuity contract for another without recognizing gain or loss at that moment, but it is not an IRA rollover: the money must move directly between insurers. '
          'If you move only part of a contract, IRS Rev. Proc. 2011-38 generally treats it as tax-free only if nothing is withdrawn from either contract for 180 days.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>What the rule says</h2>',
        '    ' + ul([
            '<strong>Contract for contract.</strong> Section 1035(a)(3) provides that no gain or loss is recognized on the exchange of one annuity contract for another, when the same person or persons are the obligee under the new contract as under the old one.',
            '<strong>Cash you receive is taxed.</strong> If you also receive money or other property, gain is recognized up to that amount.',
            '<strong>Do not take the check.</strong> The IRS cites a ruling treating a check you receive and then endorse to a second company as a distribution, not a tax-free exchange.',
            '<strong>Basis carries over.</strong> In a partial exchange, the cost basis of the original contract is allocated ratably between the original and the new contract.',
        ]),
        '    <p>Source: ' + link('rp1138') + ', which covers exchanges of annuity contracts. It does not address exchanges involving life insurance or annuities held inside IRAs, so ask the carriers which rules apply to your contract.</p>',
        '    <h2>The 180-day rule for partial exchanges</h2>',
        '    <p>For transfers completed on or after October 24, 2011, a direct transfer of part of an annuity&rsquo;s cash value to a second annuity is treated as a tax-free exchange if no amount, other than annuity payments over 10 years or more or over one or more lives, is received under either contract during the 180 days starting on the transfer date. The revenue procedure replaced an earlier 12-month period, and it removed the earlier requirement to show a qualifying life event. If a transfer fails the test, the IRS looks at the facts and circumstances.</p>',
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>A new surrender period.</strong> A new contract can start a new surrender schedule. Ask for it in writing.',
            '<strong>What you give up.</strong> Ask which benefits, riders or crediting terms in the old contract will not carry over.',
            '<strong>Withdrawing too soon.</strong> In a partial exchange, taking a withdrawal in the first 180 days can change the tax treatment.',
            '<strong>Replacement rules.</strong> State insurance departments regulate replacing one policy or annuity with another. Ask for any disclosure forms, and compare the old and new contracts side by side.',
        ]),
        '    <h2>Where it fits with rollovers</h2>',
        '    <p>A 1035 exchange and a rollover solve different problems. A rollover moves money between retirement accounts. A 1035 exchange swaps one annuity for another. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + ' and ' + A(EXIST['tax'][0], 'how annuities are taxed') + '. Annuity guarantees depend on the issuing company&rsquo;s claims-paying ability, so check the new carrier as well.</p>',
        '    ' + CTA % 'Thinking about replacing an annuity? Compare before you sign.',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'Is this a full or a partial exchange?',
            'What surrender charge applies to the old contract, and what new schedule starts on the new one?',
            'Which features, riders or rates do I lose?',
            'Will I need to withdraw anything in the next 180 days?',
            'Is the transfer going directly between the two insurers?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(EXIST['fia'][0], 'fixed indexed annuities') + ', ' + A(EXIST['spia'][0], 'single-premium annuities') + ' and ' + A(EXIST['ira'][0], 'what to ask before you move money') + '.</p>',
        '    ' + sources(['rp1138']),
    ],
    faq_title='1035 Exchange FAQ',
    faq=[
        ('Is a 1035 exchange taxable?',
         'A properly completed exchange of one annuity contract for another is generally not taxed at the time of the exchange, but cash or other property you receive can be taxed.'),
        ('Can I do a partial 1035 exchange?',
         'Yes. Under Rev. Proc. 2011-38, a direct transfer of part of an annuity to a second contract is generally treated as tax-free if nothing is withdrawn from either contract for 180 days.'),
        ('Is a 1035 exchange the same as a rollover?',
         'No. A 1035 exchange swaps one annuity contract for another and must go directly between insurers. A rollover moves money between retirement plans and IRAs.'),
    ],
    related=[REL['pillar'], REL['fia'], REL['tax']],
))

# ---------------------------------------------------------------- QLAC
pages.append(dict(
    path=B + SL['qlac'], crumbs=[('Blog', '/blog/')], crumb='QLAC and RMDs',
    title='QLAC Longevity Annuity and RMDs Explained | Honorbrook',
    desc='A qualifying longevity annuity contract (QLAC) can start payments as late as age 85, and its value is excluded from RMD calculations. Learn the IRS limits and trade-offs.',
    h1='<em>QLAC</em>: How a Longevity Annuity Affects Your Required Minimum Distributions',
    lead=('A QLAC, or qualifying longevity annuity contract, is a deferred income annuity bought with IRA or plan money. While payments are deferred, its value is excluded from the balance used to figure required '
          'minimum distributions, and payments must start no later than the first day of the month after your 85th birthday. The premium limit is $200,000, adjusted for inflation.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>What the IRS requires</h2>',
        '    ' + ul([
            '<strong>Start date.</strong> Payments must begin no later than the first day of the month after your 85th birthday.',
            '<strong>Premium limit.</strong> The final regulations removed the old 25%-of-balance limit and raised the dollar limit from $125,000 to $200,000, adjusted for inflation. The adjusted figure changes, so confirm the current-year number.',
            '<strong>No cash-out feature.</strong> The contract cannot make available a commutation benefit, cash surrender value, or similar feature before payments begin.',
            '<strong>RMD effect.</strong> While it qualifies, the QLAC&rsquo;s value is excluded from the account balance used to calculate required minimum distributions.',
        ]),
        '    <p>Source: ' + link('irb') + '.</p>',
        '    <h2>How it connects to required withdrawals</h2>',
        '    <p>The IRS current page says you generally must start withdrawals from an IRA or employer plan at age 73, and a required minimum distribution cannot be rolled over (' + link('rmd', 'IRS: required minimum distributions') + '). The starting age depends on your birth year, so confirm yours. A QLAC lowers the balance the RMD formula uses, which can lower the required amount in the years before the QLAC pays. It does not remove RMDs on the rest of the account, and the QLAC&rsquo;s payments are taxable when they arrive.</p>',
        '    <h2>The trade-offs</h2>',
        '    ' + ul([
            '<strong>The money is committed.</strong> Because the contract cannot offer cash surrender value, you cannot get the premium back as cash if circumstances change.',
            '<strong>If you die before payments start.</strong> Whether anything is paid to a beneficiary depends on the contract. Ask about a return-of-premium feature and what it costs.',
            '<strong>Inflation.</strong> A fixed payment starting at 85 buys less than the same payment would today. Ask whether the contract has an inflation adjustment and how it affects the starting amount.',
            '<strong>The carrier.</strong> Payments depend on the issuing company&rsquo;s claims-paying ability for decades.',
        ]),
        '    <h2>Where it fits with a rollover</h2>',
        '    <p>A QLAC is bought with money in an IRA or an employer plan, so a rollover to an IRA is often the first step if the plan does not offer one. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + ' and ' + A(EXIST['spia'][0], 'single-premium annuities') + ' for how income annuities differ.</p>',
        '    ' + CTA % 'Curious whether a longevity annuity fits your plan?',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'What premium am I considering, and does it respect the current dollar limit?',
            'What start age would I choose, and what is the income at each age?',
            'Is there a death benefit, and what does it cost?',
            'Is there an inflation adjustment?',
            'What will my RMD be with and without the QLAC? (Ask for the calculation in writing.)',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(REL['inherited'][0], 'inherited IRA rules') + ', ' + A(EXIST['tax'][0], 'how annuities are taxed') + ' and ' + A(REL['age55'][0], 'the age 55 rule') + '.</p>',
        '    ' + sources(['irb', 'rmd', 'roll']),
    ],
    faq_title='QLAC FAQ',
    faq=[
        ('How much can I put in a QLAC?',
         'The final regulations set the limit at $200,000, adjusted for inflation, and removed the old 25%-of-balance limit. Confirm the current-year figure before buying.'),
        ('Does a QLAC reduce required minimum distributions?',
         'It can lower them while payments are deferred, because the QLAC&rsquo;s value is excluded from the balance used to calculate RMDs. RMDs on the rest of the account still apply.'),
        ('Can a QLAC start before 85?',
         'Yes. The rule is that payments must begin no later than the first day of the month after your 85th birthday.'),
    ],
    related=[REL['pillar'], REL['spia'], REL['inherited']],
))

# ---------------------------------------------------------------- Roth
pages.append(dict(
    path=B + SL['roth'], crumbs=[('Blog', '/blog/')], crumb='Roth Rollover to an Annuity',
    title='Roth IRA and Roth 401(k) Rollover to an Annuity | Honorbrook',
    desc='A designated Roth 401(k) can roll to a Roth IRA, but a Roth IRA cannot roll back to a traditional IRA or a plan. See the IRS chart and the tax trap on pre-tax money.',
    h1='<em>Roth</em> IRA and Roth 401(k) Rollover to an Annuity: What to Know',
    lead=('Roth money stays Roth: a Roth 401(k) or other designated Roth account can generally roll to a Roth IRA, and a Roth IRA can move only to another Roth IRA. Moving pre-tax money '
          'into a Roth IRA is a conversion that is generally taxable as income that year. An annuity bought inside a Roth IRA follows Roth IRA rules.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>What the IRS chart allows</h2>',
        '    ' + table(['Roll from', 'To a Roth IRA', 'To a traditional IRA or plan'], [
            ['Roth IRA', 'Yes (one rollover per 12 months)', 'No'],
            ['Designated Roth 401(k), 403(b) or 457(b)', 'Yes', 'No'],
            ['Traditional IRA, SEP IRA', 'Yes, the untaxed amount is included in income', 'Not applicable'],
            ['Pre-tax 401(k), 403(b) or governmental 457(b)', 'Yes, the untaxed amount is included in income', 'Yes'],
            ['SIMPLE IRA', 'Only after two years, and the untaxed amount is included in income', 'Only after two years'],
        ]),
        '    <p>Source: the ' + link('chart', 'IRS rollover chart') + ' and ' + link('simple', 'IRS SIMPLE IRA rules') + '.</p>',
        '    <h2>The conversion trap</h2>',
        '    <p>Moving pre-tax money to a Roth IRA is taxable as income in the year of the transaction, other than qualified Roth distributions and amounts already taxed (' + link('roll') + '). If you pay the tax out of the converted money, less lands in the Roth. A conversion also adds to your income for that year, which can affect other income-based costs, so ask your tax professional to model it before you convert.</p>',
        '    <h2>Required withdrawals</h2>',
        '    <p>The IRS says you are not required to take withdrawals from a Roth IRA, or from a designated Roth account in a 401(k) or 403(b), while the account owner is alive. Beneficiaries of Roth accounts are subject to required distribution rules (' + link('rmd', 'IRS: required minimum distributions') + ').</p>',
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>Nontaxable amounts.</strong> The IRS chart notes that any nontaxable amounts distributed from a designated Roth account must be rolled over by a direct trustee-to-trustee transfer.',
            '<strong>A Roth IRA cannot go backward.</strong> It cannot roll into a traditional IRA or an employer plan.',
            '<strong>Timing rules.</strong> Roth accounts have a separate waiting period for tax-free earnings. Ask your tax professional how it applies to your accounts before you rely on a withdrawal being tax-free.',
        ]),
        '    <h2>Where an annuity fits</h2>',
        '    <p>An annuity inside a Roth IRA does not add tax benefits beyond the Roth treatment already there, and it can add surrender charges and fees. The reasons to consider one are the contract features, and its guarantees depend on the issuing company&rsquo;s claims-paying ability. Because Roth money has no required lifetime withdrawals, a Roth IRA annuity should be evaluated for how long you can leave the money untouched. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + '.</p>',
        '    ' + CTA % 'Weighing a Roth conversion and an annuity?',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'Is this money Roth or pre-tax, and how do I know?',
            'If it is pre-tax, what would the conversion tax be, and where would I pay it from?',
            'Is the transfer direct, trustee to trustee?',
            'How long can I leave this money untouched, given surrender charges?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(REL['simple'][0], 'SEP and SIMPLE rollovers') + ', ' + A(REL['inherited'][0], 'inherited IRA rules') + ' and ' + A(EXIST['tax'][0], 'how annuities are taxed') + '.</p>',
        '    ' + sources(['chart', 'roll', 'rmd', 'simple']),
    ],
    faq_title='Roth Rollover FAQ',
    faq=[
        ('Can I roll a Roth IRA into a traditional IRA?',
         'No. The IRS rollover chart shows a Roth IRA can roll only to another Roth IRA.'),
        ('Is moving a 401(k) to a Roth IRA taxable?',
         'Pre-tax money moved to a Roth IRA is generally included in income that year. A designated Roth 401(k) rolled to a Roth IRA is a different case, because it is already Roth money.'),
        ('Does a Roth IRA have required minimum distributions?',
         'Not for the owner while alive, according to the IRS. Beneficiaries of Roth accounts are subject to required distribution rules.'),
    ],
    related=[REL['pillar'], REL['simple'], REL['tax']],
))

# ---------------------------------------------------------------- age 55
pages.append(dict(
    path=B + SL['age55'], crumbs=[('Blog', '/blog/')], crumb='Age 55 Rule',
    title='Age 55 Rule: Rolling a 401(k) Into an IRA Annuity | Honorbrook',
    desc='Leave a job at 55 or later and you may withdraw from that 401(k) without the 10% additional tax. Roll it to an IRA and that exception does not follow. Check first.',
    h1='The <em>Age 55</em> Rule: What You Can Lose Rolling a 401(k) Into an IRA Annuity',
    lead=('If you leave your job in or after the year you turn 55, withdrawals from that employer&rsquo;s 401(k) may avoid the 10% additional tax on early distributions. The IRS exceptions table shows that exception '
          'for qualified plans but not for IRAs, so rolling the money to an IRA, including an IRA annuity, can give it up. Check your timeline before you roll.'),
    body=[
        '    ' + IMPORTANT,
        '    <h2>What the IRS table shows</h2>',
        '    ' + table(['Where the money sits', 'Leave the employer at 55 or later', 'Age 59&frac12; or older'], [
            ['Employer 401(k) or similar qualified plan', 'Exception applies', 'Exception applies'],
            ['IRA, SEP or SIMPLE IRA, including an IRA annuity', '<strong>Exception does not apply</strong>', 'Exception applies'],
        ]),
        '    <p>The separation-from-service exception covers an employee who leaves their employer during or after the year they reach 55 (50 for certain public safety employees in governmental plans). Source: ' + link('early', 'IRS exceptions table') + ' and ' + link('tc558', 'IRS Topic 558') + '.</p>',
        '    <h2>Why this matters for a rollover</h2>',
        '    <p>Say you leave your job at 56 and roll the 401(k) into an IRA annuity. At 57, you need money. A 401(k) withdrawal could have avoided the 10% additional tax, but an IRA withdrawal at 57 would face it unless another exception applies. The annuity can add a second cost if you take more than the contract allows without a surrender charge. The exception only affects the 10% additional tax, and withdrawals are still taxed as income.</p>',
        '    <h2>The traps</h2>',
        '    ' + ul([
            '<strong>The exception does not follow the money.</strong> Once the money is in an IRA, the table shows no age-55 exception for it.',
            '<strong>Stacking costs.</strong> A pre-59&frac12; withdrawal from an IRA annuity can mean income tax, the 10% additional tax and a surrender charge at the same time.',
            '<strong>Your plan type.</strong> The IRS table lists the exception for qualified plans. Ask your tax professional whether your specific plan, such as a 403(b), qualifies.',
            '<strong>Governmental 457(b).</strong> These plans generally are not subject to the 10% additional tax at all, which is a separate advantage that also does not follow into an IRA (' + link('tc558') + ').',
        ]),
        '    <h2>Ways people handle it</h2>',
        '    <p>Some people roll only part of the plan to an IRA annuity and leave a bridge amount in the plan for the years before 59&frac12;. Whether your plan lets you keep money there after you leave, and how withdrawals work, is in the plan document, so ask your plan administrator. See ' + A(REL['pillar'][0], 'every rollover account at a glance') + '.</p>',
        '    ' + CTA % 'Between 55 and 59&frac12;? Check the timeline before you roll.',
        '    <h2>Questions to ask</h2>',
        '    ' + ul([
            'In what year did or will I leave this employer?',
            'Does my plan allow me to keep money there and take withdrawals after I leave?',
            'Do I expect to need money before 59&frac12;?',
            'What surrender charge would apply to a withdrawal from the annuity, and what free withdrawal amount is allowed?',
        ]),
        '    <h2>Related reading</h2>',
        '    <p>See ' + A(EXIST['401k'][0], 'your 401(k) options') + ', ' + A(REL['457b'][0], '457(b) rollovers') + ' and ' + A(REL['403b'][0], '403(b) rollovers') + '.</p>',
        '    ' + sources(['early', 'tc558', 'roll']),
    ],
    faq_title='Age 55 Rule FAQ',
    faq=[
        ('Does the age 55 rule apply to IRAs?',
         'No. The IRS exceptions table shows the separation-from-service exception for qualified plans but not for IRAs.'),
        ('Does the rule apply to a 403(b)?',
         'The IRS table lists the exception for qualified plans. Ask your tax professional whether your specific 403(b) qualifies before you roll it.'),
        ('Does leaving at 55 mean the withdrawals are tax-free?',
         'No. The exception removes the 10% additional tax, but withdrawals are still taxed as income.'),
    ],
    related=[REL['pillar'], REL['401k'], REL['457b']],
))

# fill in related titles/blurbs for sibling pages
TITLES = {B + SL['403b']: ('403(b) rollovers', 'Can a 403(b) go into an annuity?'),
          B + SL['457b']: ('457(b) rollovers', 'Governmental vs. non-governmental plans.'),
          B + SL['simple']: ('SEP and SIMPLE rollovers', 'The two-year rule explained.'),
          B + SL['pension']: ('Pension lump sum', 'What can be rolled and what cannot.'),
          B + SL['inherited']: ('Inherited IRAs', 'Spouse and non-spouse options.'),
          B + SL['x1035']: ('The 1035 exchange', 'Swap one annuity for another, and the 180-day rule.'),
          B + SL['qlac']: ('QLACs and RMDs', 'A longevity annuity and required withdrawals.'),
          B + SL['roth']: ('Roth rollovers', 'What can and cannot move.'),
          B + SL['age55']: ('The age 55 rule', 'What an IRA rollover can cost you.')}
for p in pages:
    p['related'] = [(h, TITLES[h][0] if h in TITLES and not t else t, TITLES[h][1] if h in TITLES and not b else b) for h, t, b in p['related']]


def main():
    for p in pages:
        out = os.path.join(SITE, p['path'].lstrip('/') + '.html')
        open(out, 'w', encoding='utf-8').write(render(p, pillar=p.get('pillar', False)))
        print('wrote', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    main()
