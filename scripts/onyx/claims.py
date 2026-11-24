"""Honorbrook Onyx: rewrite claims the owner's content rules do not allow (Nov 24, 2026).

Rules (owner, CLAUDE.md): verified facts only; no invented prices, statistics or carrier claims; no "$0", "free plan",
superlatives, guarantees or urgency. The audit of Nov 24 found these still live, mostly in copy older than the Onyx build:
"$2/day" (8 places), a sample monthly rates table with carrier names, an unsourced funeral cost range, "$300-$450 per day",
"lowest true annual cost" (33), "never overpay", "smartest companion", "no cost, ever", "Most popular" and similar.
Each is rewritten to a plain description of what we do, or removed. Runs after phone.apply(), on the final text.
guard() fails the build if any of the old wording comes back.
"""
import glob
import os
import re

BOOK = 'https://www.planenroll.com/?purl=Luay-Sadqi'

# every page: (old, new)
ALL = [
    # Part D wording ("lowest" is a superlative we cannot show for every visitor)
    ('— we find the lowest true annual cost for your exact medication list.', '— we compare the total yearly cost for your medication list.'),
    ('— we find the lowest true annual cost for your medication list.', '— we compare the total yearly cost for your medication list.'),
    ('— we find the lowest true annual cost for your medications.', '— we compare the total yearly cost for your medications.'),
    ('— we find the lowest true cost for your medications.', '— we compare the total yearly cost for your medications.'),
    ('— the lowest true annual cost for your medication list.', '— the total yearly cost for your medication list, compared.'),
    ('We find the lowest true annual cost for your exact medication list.', 'We compare the total yearly cost for your medication list.'),
    ('Find the lowest true annual cost for your exact medication list.', 'Compare the total yearly cost for your medication list.'),
    ('Find your lowest true annual prescription cost.', 'Compare the total yearly cost of your prescriptions.'),
    ('Find your lowest true annual drug cost across every Part D plan — free help.', 'Compare the total yearly drug cost across the Part D plans we offer in your area, with free help.'),
    ('We run your exact medication list through every Part D plan to find the lowest true annual cost — premium, deductible and copays combined.',
     'We run your medication list through the Part D plans we offer in your area and compare the total yearly cost: premium, deductible and copays combined.'),
    ('We run your exact medication list through every available plan to find the lowest true annual cost — premium, deductible, and copays combined.',
     'We run your medication list through the plans we offer in your area and compare the total yearly cost: premium, deductible and copays combined.'),
    # Medigap
    ('Compare Medicare Supplement plans across a dozen carriers so you never overpay for identical coverage.',
     'Compare Medicare Supplement prices across carriers. Plans with the same letter have the same benefits.'),
    ('We compare Plan G and Plan N rates across a dozen carriers so you never overpay for identical coverage.',
     'Plans with the same letter have the same benefits, so we compare Plan G and Plan N prices across carriers for you.'),
    ("We compare Plan G, Plan N, and more across a dozen carriers — so you never overpay for coverage that's identical by law.",
     'Plans with the same letter have the same benefits by law, so we compare Plan G, Plan N and more across carriers for you.'),
    ('Plan G vs. Plan N: the two most popular choices', 'Plan G vs. Plan N: two common choices'),
    # hospital indemnity
    ("Cash for each day you're admitted — the smartest companion to Medicare Advantage.",
     "Cash for each day you're admitted, to help with the hospital copays many Medicare Advantage plans charge."),
    ("It pays YOU a fixed cash benefit for each day you're admitted — the smartest companion to a Medicare Advantage plan.",
     "It pays you a set cash benefit for each day you're admitted, which you can put toward the hospital copays many Medicare Advantage plans charge."),
    ('Instead of a single deductible, Advantage plans often charge a per-day copay for the first several days of an inpatient stay, commonly in the range of $300–$450 per day before that copay tops out.',
     'Instead of a single deductible, many Advantage plans charge a per-day copay for the first several days of an inpatient stay. Your plan&rsquo;s Evidence of Coverage lists the amount.'),
    # final expense price lines on product cards
    ('Protect your family from funeral costs starting around $2/day.', 'Whole life coverage to help pay for a funeral and final bills.'),
    ('Whole-life burial insurance from around $2/day — no medical exam, locked premiums, paid to your family tax-free.',
     'Whole life insurance to help pay for a funeral and final bills. Many plans ask health questions instead of an exam.'),
    # other
    ('— no pressure, no cost, ever.', '— no pressure and no cost to you.'),
    ('<strong>Free, no-pressure quotes from many carriers.</strong> Find your best rate — ', '<strong>Free, no-pressure quotes from many carriers.</strong> Call '),
    ('<span class="hint">Funeral and burial often run $8,000&ndash;$12,000</span>', '<span class="hint">Funeral, burial and final bills</span>'),
    ('href="/#contact">Free Plan Review</a>', 'href="/#contact">Plan Review</a>'),
    # licensing: only the 16 states and DC (two pages said "and beyond")
    (', and Florida, and beyond —', ', and Florida —'),
    # "compare every plan" contradicts the CMS disclaimer on the same pages ("We do not offer every plan available in your area")
    ('we compare them all and recommend', 'we compare the plans we offer and recommend'),
    ('a local guide who shops the whole market for you.', 'a local guide who compares carriers for you.'),
    ('We compare every option side by side and explain the tradeoffs', 'We compare your options side by side and explain the tradeoffs'),
    # term life superlatives
    ('<p>The most protection per dollar you can buy.</p>', '<p>Coverage for a set number of years, usually for less than permanent coverage.</p>'),
    ('<p>The most protection per dollar — and how to pick the right length.</p>', '<p>Coverage for a set number of years, and how to pick the right length.</p>'),
    ('<p>The other half of income protection — the most coverage per dollar.</p>', '<p>The other half of income protection: coverage for a set number of years.</p>'),
    ('This is the most expensive mistake we see,', 'This is a costly mistake we see often,'),
    # local presence is Northern Virginia only; elsewhere we work by phone or video
    ('Local, independent help for Alabama residents from 90+ carriers — always free.', 'Independent help for Alabama residents from 90+ carriers, always free.'),
    ('Independent local help for Alabama residents — compare plans at your exact address.', 'Independent help for Alabama residents: compare plans at your exact address.'),
    ('Free local guidance for Maryland residents', 'Free guidance for Maryland residents'),
    ('Local-style help for North Carolina residents', 'Independent help for North Carolina residents'),
    ('Local-feel help for South Carolina residents', 'Independent help for South Carolina residents'),
    ('with no-pressure local guidance.', 'with no-pressure guidance by phone or video.'),
    ('Plan networks and local help for Lake County, Indiana residents.', 'Plan networks and help for Lake County, Indiana residents.'),
    ('<h3>Get free, local Georgia help</h3>', '<h3>Get free Georgia help by phone or video</h3>'),
    ("We'll confirm your dates and find the best coverage available at your new address.", "We'll confirm your dates and compare the coverage available at your new address."),
]

# page: [(old, new)]; each old must be found (the build stops if a page changed and a rule no longer matches)
PAGE = {
    'medicare-part-d.html': [
        ('Medicare Part D: Find Your Lowest Cost', 'Medicare Part D: Compare Total Drug Costs'),
        ('<h1>Medicare Part D: find your <em>lowest</em> true drug cost</h1>', '<h1>Medicare Part D: compare your <em>total</em> drug cost</h1>'),
        ("The cheapest Part D plan isn't the one with the lowest premium — it's the one that costs you the least once <strong>your</strong> specific medications are factored in. We run your exact drug list through every available plan to find your true lowest annual cost: premium, deductible, and copays combined.",
         'The Part D plan with the lowest premium is not always the one that costs you least once <strong>your</strong> medications are factored in. We run your drug list through the Part D plans we offer in your area and compare the total yearly cost: premium, deductible and copays combined.'),
        ('We compare every Part D plan against your exact prescriptions and show your lowest total cost. Free.', 'We compare the Part D plans we offer against your prescriptions and show the total yearly cost of each. Free.'),
        ("We'll help you avoid the penalty and pick the lowest-cost option that keeps you covered.", "We'll help you avoid the penalty and compare options that keep you covered."),
        ("The cheapest plan isn't the one with the lowest premium — it's the one with the lowest total annual cost once your specific drugs, the deductible, and copays are included. We enter your exact medication list and compare every available plan to find your true lowest cost.",
         'The plan with the lowest premium is not always the one with the lowest total yearly cost once your drugs, the deductible and copays are included. We enter your medication list and compare the total yearly cost of the plans we offer in your area.'),
        ("We run a free review each fall so you're never quietly overpaying.", 'We offer a free review each fall so you can compare.'),
        ('we compare the full slate of Part D plans available to you rather than steering you to one carrier', 'we compare Part D plans from several carriers rather than steering you to one'),
    ],
    'medicare-supplement-medigap.html': [
        ('Compare Medigap Plan G &amp; Plan N across a dozen carriers — free, no-pressure help.', 'Compare Medigap Plan G &amp; Plan N prices across carriers, with free, no-pressure help.'),
        ('<h3>Compare Medigap rates across a dozen carriers</h3>', '<h3>Compare Medigap prices across carriers</h3>'),
        ('Same coverage, different prices — we find you the lowest one.', 'Same coverage, different prices. We compare them for you.'),
        ('That means shopping carriers can save you hundreds per year for identical coverage — which is exactly what we do for you.', 'That is why comparing carriers matters, and it is what we do for you.'),
        ('So shopping carriers can save you hundreds of dollars a year for the exact same benefits.', 'So comparing carriers can lower what you pay for the same benefits.'),
        ('Shopping carriers can save you hundreds per year for identical coverage, which is exactly what we do for you.', 'That is why comparing carriers matters, and it is what we do for you.'),
        ('appointed with many top Medigap carriers, so we shop the whole market for you instead of pushing one company', 'appointed with many Medigap carriers, so we compare them for you instead of pushing one company'),
        ('Both are excellent plans.', 'Both are common choices.'),
        ('which we also compare for you to find your lowest total cost.', 'which we also compare for you on total yearly cost.'),
    ],
    'hospital-indemnity-insurance.html': [
        ('<h1>Hospital indemnity: cash that <em>wipes out</em> hospital copays</h1>', '<h1>Hospital indemnity: cash for <em>each day</em> you&rsquo;re admitted</h1>'),
        ('<li><strong>The monthly premium is affordable.</strong> Because the benefit is fixed and predictable, these plans typically cost just a few dollars a month for meaningful protection.</li>',
         '<li><strong>The benefit is set in advance.</strong> You know the daily amount the policy pays before you buy it.</li>'),
        ('the indemnity plan hands you cash to wipe out the daily hospital copays that Advantage plans leave on your plate.', 'the indemnity plan pays you cash that can help with the daily hospital copays many Advantage plans charge.'),
        ("a small monthly premium can neutralize a four-figure hospital bill. It's also a smart pick for anyone who simply wants", 'it can help pay the hospital copays your plan charges. It can also suit anyone who wants'),
        ("That adds up fast. A short, unplanned admission can leave you owing well over a thousand dollars out of pocket — and that's on top of any other care you receive.", 'Those copays can add up over a hospital stay, on top of any other care you receive.'),
        ('<h3>Turn a surprise hospital bill into a non-event</h3>', '<h3>See how hospital indemnity fits your plan</h3>'),
        ("We'll show you how a small monthly premium can cover the copays your plan leaves behind — for free.", "We'll show you how a hospital indemnity plan can help with the copays your plan leaves behind, for free."),
    ],
    'medicaid-dual-eligible.html': [
        ('comparing every D-SNP available in your county', 'comparing the D-SNPs we offer in your county'),
        ('often with dental, vision, hearing, transportation, and grocery or over-the-counter benefits at no added premium.', 'often with extra benefits such as dental, vision, hearing, transportation, and grocery or over-the-counter allowances, depending on the plan.'),
        ('and an over-the-counter benefit, typically at no additional premium beyond what you already pay.', 'and an over-the-counter benefit, depending on the plan.'),
        ('and an over-the-counter or grocery benefit — typically at no additional premium.', 'and an over-the-counter or grocery benefit, depending on the plan.'),
    ],
    'final-expense-life-insurance.html': [
        ('<strong>No medical exam — just a few health questions.</strong>', '<strong>Many plans ask health questions instead of a medical exam.</strong>'),
        ("<li><strong>No medical exam</strong> — just a few health questions, no needles, no doctor's visit.</li>", "<li><strong>Health questions instead of an exam</strong> on many plans: no needles, no doctor's visit.</li>"),
        ('<li><strong>Most conditions accepted</strong> for ages 45–85, including common issues like diabetes, high blood pressure, and heart conditions.</li>',
         '<li><strong>Options for many health histories</strong>, ages 45–85, including common conditions like diabetes, high blood pressure and heart conditions.</li>'),
        ('exist for more serious conditions, so coverage is available even when other policies have turned you down.</li>', 'exist for more serious conditions. They usually have a waiting period before the full benefit applies.</li>'),
        ('<li><strong>Locked premiums</strong> that never increase — your rate is set the day your policy begins and stays there for life.</li>', '<li><strong>Level premiums</strong>: on a whole life final expense policy, the premium is set when the policy starts and stays level.</li>'),
        ("<li><strong>Coverage that never expires</strong> as long as premiums are paid, so it's always there when your family needs it.</li>", '<li><strong>Coverage for life</strong>, as long as premiums are paid.</li>'),
        ('see your options and lock in a rate.', 'see your options.'),
    ],
    'turning-65.html': [
        ('Turning 65 is the one insurance deadline that never forgives you. Your Initial Enrollment Period runs seven months, the Part B late-enrollment penalty is permanent, and working past 65 changes the math entirely.',
         'Your Initial Enrollment Period runs seven months, the Part B late enrollment penalty can last as long as you have Part B, and working past 65 changes the math.'),
        ('and some of the penalties are permanent.', 'and some penalties last as long as you have the coverage.'),
        ('The most expensive mistakes we see are timing mistakes, and they are all avoidable with a conversation months earlier.', 'Many of the costly mistakes we see are timing mistakes, and a conversation months earlier can help avoid them.'),
    ],
    'medicare-annual-enrollment-period.html': [
        ('against every plan available in your county — free', 'against the plans we offer in your county — free'),
        ('run them against every plan available in your county, and show you', 'run them against the plans we offer in your county, and show you'),
        ('That sounds convenient, but it is the single most expensive mistake in Medicare, because plans change', 'That sounds convenient, but it can cost you, because plans change'),
        ('<h2>The most expensive mistake: doing nothing</h2>', '<h2>The common mistake: doing nothing</h2>'),
        ('Your plan generally renews automatically — which is the most expensive mistake in Medicare.', 'Your plan generally renews automatically, even if it no longer fits.'),
        ("It's the only chance most people have to fix a plan that isn't working — and the deadline is firm.", "For most people it's the main yearly chance to change a plan that isn't working, and it ends December 7."),
    ],
    'blog/medicare-101-what-every-family-should-know.html': [
        ('Medicare is one of the few decisions where the wrong choice can quietly cost you thousands a year for the rest of your life.', 'Medicare is a decision where the wrong choice can cost you money year after year.'),
    ],
    'life-insurance.html': [
        ('— the most affordable option and the right answer for most families.', '— usually less expensive than permanent coverage for the same death benefit.'),
    ],
    'term-life-insurance.html': [
        ('<strong>The most coverage per dollar you can buy.</strong>', '<strong>Coverage for the years your family depends on you.</strong>'),
        ('The most protection per dollar. Compare 10, 20 &amp; 30-year term quotes — no-exam options available.', 'Coverage for the years your family depends on you. Compare 10, 20 &amp; 30-year term quotes, with no-exam options.'),
    ],
    'medicare-advantage.html': [
        ('compare every plan the <em>honest</em> way', 'compare your options the <em>honest</em> way'),
        ('The difference is that we compare every option for you', 'The difference is that we compare your options for you'),
        ('All-in-one Medicare plans from Aetna, Humana, UnitedHealthcare, Wellcare and more — that can include', 'All-in-one Medicare plans that can include'),
        ('Compare Medicare Advantage plans from Aetna, Humana, UnitedHealthcare and more. plan options that can include dental, vision and drug coverage. Free help.',
         'Compare Medicare Advantage plans that can include dental, vision and drug coverage, with free help from an independent agent.'),
    ],
    'about.html': [('I compare every plan available in your area', 'I compare the plans I offer in your area')],
    'maryland-medicare-insurance.html': [('since the carriers pay us and your premium never changes.', 'since the carriers pay us, and your premium is the same whether you use us or enroll on your own.')],
    'guaranteed-universal-life.html': [
        ('Guaranteed Universal Life (GUL) — Permanent Coverage, Lowest Cost', 'Guaranteed Universal Life (GUL) Insurance | Honorbrook'),
        ('at the lowest possible cost?', 'at a lower cost than whole life?'),
        ('A locked-in permanent death benefit for far less than whole life.', 'A locked-in permanent death benefit, usually for less than whole life.'),
    ],
    'childrens-life-insurance.html': [('covers all your children for a few dollars a month.', 'covers all your children for a small added premium.')],
    'blog/new-to-medicare-checklist-virginia-and-10-more-states.html': [
        ('and includes the free counseling program for each state we serve.', 'and links to Medicare help for each state we serve.'),
        ('"headline": "New to Medicare? Your Checklist, With Free Local Help by State"', '"headline": "New to Medicare? A Step-by-Step Checklist"'),
        ('"description": "New to Medicare or just moved to a new state? Follow this step-by-step checklist and find the free counseling program in VA, MD, NC, SC, GA, AL, LA, TX, MI, IN and WV."',
         '"description": "New to Medicare or just moved? A step-by-step checklist for enrollment windows, penalties and plan choices, with help for each state we serve."'),
    ],
    'index.html': [('explains every option in plain English', 'explains your options in plain English')],
    'schedule-an-appointment.html': [('at our office in Tysons or at your home.', 'at our office in Tysons or at your home (office and home visits are in Northern Virginia).')],
}
# the Part D "donut hole" answer: the coverage gap ended in 2025 (Part D redesign; the site's own posts say so)
DONUT = [
    (re.compile(r'"name":"What is the Part D coverage gap or donut hole\?","acceptedAnswer":\{"@type":"Answer","text":"[^"]*"'),
     '"name":"Is there still a Part D donut hole?","acceptedAnswer":{"@type":"Answer","text":"No. Starting in 2025, Part D no longer has a coverage gap, and there is a yearly cap on what you pay out of pocket for covered drugs. We include that in the total yearly cost we show you."'),
    (re.compile(r'<details><summary>What is the coverage gap or "donut hole"\?</summary><div class="a">.*?</div></details>', re.S),
     '<details><summary>Is there still a "donut hole"?</summary><div class="a">No. Starting in 2025, Part D no longer has a coverage gap, and there is a yearly cap on what you pay out of pocket for covered drugs. We include that in the total yearly cost we show you.</div></details>'),
]

FE_OLD = re.compile(r'<h2 class="section-title">Protect your family from funeral costs — starting around \$2/day</h2>.*?</div>\s*<div class="fe-box">.*?</div>\s*</div>\s*</section>', re.S)
FE_NEW = '''<h2 class="section-title">Help your family with funeral costs and final bills</h2>
      <p>Final expense insurance is a smaller whole life policy meant to pay for a funeral and last bills, so they do not fall on the people you leave behind.</p>
      <ul>
        <li>Many plans ask health questions instead of a medical exam</li>
        <li>Options for many health histories, ages 45&ndash;85</li>
        <li>Level premiums that are set when the policy starts</li>
        <li>Coverage for life, as long as premiums are paid</li>
        <li>The benefit is paid to the beneficiary you name</li>
      </ul>
      <a class="btn-primary sans" href="#contact" style="margin-top:8px">Get My Free Quote</a>
    </div>
    <div class="fe-box">
      <h3>Schedule your final expense review</h3>
      <p class="note">Have these ready and the first conversation is useful:</p>
      <div class="row"><span>The date of birth and state of the person the policy is for</span></div>
      <div class="row"><span>Whether they have used tobacco in the last 12 months</span></div>
      <div class="row"><span>A list of current medications</span></div>
      <div class="row"><span>Who the beneficiary will be</span></div>
      <a class="btn-primary sans" href="%s" target="_blank" rel="noopener" style="margin-top:18px">Schedule an appointment</a>
      <p class="note">On PlanEnroll, choose <strong>Life</strong> as the meeting type.</p>
    </div>
  </div>
</section>''' % BOOK

HOME = [
    ('Medicare has more moving parts than ever — and choosing wrong can cost you thousands. We compare every option side by side and check that your doctors, hospitals, and prescriptions are covered before you enroll.',
     'Medicare has a lot of moving parts. We compare your options side by side and check that your doctors, hospitals and prescriptions are covered before you enroll.'),
    ('<span class="badge">Most popular</span>', '<span class="badge">All-in-one</span>'),
    ('<span class="badge gold">Maximum freedom</span>', '<span class="badge gold">Any Medicare doctor</span>'),
    ('All-in-one plans from Aetna, Humana, UnitedHealthcare, Wellcare and more — that can include dental, vision, hearing, and drug coverage built in.',
     'All-in-one plans that can include dental, vision, hearing and drug coverage built in.'),
    ('Even good Medicare plans leave you exposed to hospital copays, cancer treatment costs, and dental bills. These affordable add-ons cap the costs that catch most retirees off guard.',
     'Medicare plans can leave hospital copays, cancer treatment costs and dental bills for you to pay. These add-on policies pay cash or cover care your plan leaves out.'),
    ('Medicare Advantage plans often charge $300–$450 per day for hospital stays. A hospital indemnity plan pays you cash for each day admitted — wiping out those copays for a few dollars a month. The smartest companion to any Advantage plan.',
     'Many Medicare Advantage plans charge a daily copay for the first days of a hospital stay. A hospital indemnity plan pays you a set cash amount for each day you are admitted, which you can put toward those copays.'),
    ('A lump-sum cash benefit paid directly to you on diagnosis — use it for treatment, travel, bills, or anything else. A serious diagnosis can drain a lifetime of savings — this is how you face it without that fear.',
     'A lump-sum cash benefit paid to you on diagnosis, to use for treatment, travel, bills or anything else.'),
    ('Original Medicare covers none of these. Affordable DVH plans from Mutual of Omaha, Aetna, and ManhattanLife cover cleanings, dentures, glasses, and hearing aids — the bills seniors actually face.',
     'Original Medicare does not cover most dental care, eye exams for glasses or hearing aids. A dental, vision and hearing plan can help with cleanings, dentures, glasses and hearing aids.'),
    ('Medicare only pays for limited recovery care. Short-term care and home health care plans protect your savings — and your independence — if you need help recovering at home.',
     'Medicare pays for limited recovery care. Short-term care and home health care plans can pay a benefit if you need help recovering at home.'),
    ('SHOP-certified small-business group health plans — and we\'ll check if you qualify for the small business tax credit.',
     'Small-business group health plans, including SHOP, and we\'ll check if you qualify for the small business tax credit.'),
    ('Have both Medicare and Medicaid? D-SNP plans add dental, vision, hearing &amp; transportation at no extra premium. We check Extra Help too.',
     'Have both Medicare and Medicaid? Many D-SNP plans include extra benefits such as dental, vision and transportation. We check Extra Help too.'),
    ("Turn retirement savings into guaranteed, predictable income you can't outlive — fixed and fixed-indexed options.",
     'Fixed and fixed-indexed annuities, including options that pay income for life. Guarantees depend on the issuing insurer&rsquo;s claims-paying ability.'),
    ('Appointed with leading national carriers', 'Appointed with many national carriers'),
    ('Almost always, yes. Simplified-issue policies ask a few health questions but require no exam, and guaranteed-issue options exist for serious conditions. Because we work with many carriers, we match your specific health history to the carrier most likely to approve you at the best rate.',
     'Often, yes. Simplified-issue policies ask a few health questions but require no exam, and guaranteed-issue options exist for serious conditions. Because we work with many carriers, we match your health history with carriers whose underwriting fits it.'),
    ("Plans change every single year — premiums, drug lists, doctor networks, and benefits all shift. The plan that was perfect two years ago may be costing you money today. We run a free annual review each fall so you're never stuck overpaying.",
     'Plans can change every year: premiums, drug lists, doctor networks and benefits. A plan that fit two years ago may not fit as well now. We offer a free review each fall so you can compare.'),
]

# Old wording that must not come back. (pattern, where) where 'all' = every page.
BANNED = [r'\$2/day', r'\$2 a day', r'Sample monthly rates', r'lowest true', r'never overpay', r'smartest companion', r'\$300[–-]\$450',
          r'no cost, ever', r'Find your best rate', r'\$8,000(?:–|&ndash;)\$12,000', r'never carry that burden', r'Free Plan Review',
          r'choosing wrong can cost', r'Most popular', r'true lowest', r'lowest</em> true', r'Find Your Lowest', r'never quietly overpaying', r'and beyond —',
          r'find the best coverage', r'most protection per dollar', r'most coverage per dollar', r'wipes? out', r'few dollars a month', r'compare every plan',
          r'(?<!offer )every plan available in your (?:area|county)', r'single most expensive mistake', r'never forgives', r'no (?:added|additional) premium',
          r'a dozen carriers', r'top Medigap', r'whole market', r'hundreds (?:of dollars )?(?:per|a) year', r'compare them all', r'coverage gap or']


def _sub_count(s, a, b):
    n = s.count(a)
    return s.replace(a, b), n


def apply(out):
    """Rewrite the claims in every page. Returns {rule: hits} so the build can show what changed."""
    hits = {}
    for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/video' in f: continue
        s = open(f, encoding='utf-8', errors='ignore').read(); o = s
        for a, b in ALL:
            s, n = _sub_count(s, a, b)
            if n: hits[a[:60]] = hits.get(a[:60], 0) + n
        rel = os.path.relpath(f, out)
        for a, b in PAGE.get(rel, []):
            s, n = _sub_count(s, a, b)
            if not n: raise SystemExit('claims: %s: text not found: %s' % (rel, a[:70]))
            hits[rel + ': ' + a[:40]] = n
        if rel == 'medicare-part-d.html':
            for rx, b in DONUT:
                s, n = rx.subn(lambda m, b=b: b, s)
                if n != 1: raise SystemExit('claims: Part D donut hole answer not found')
        if os.path.relpath(f, out) == 'index.html':
            s, n = FE_OLD.subn(lambda m: FE_NEW, s)
            if n != 1: raise SystemExit('claims: homepage final expense section not found')
            hits['homepage final expense section'] = n
            for a, b in HOME:
                s, n = _sub_count(s, a, b)
                if not n: raise SystemExit('claims: homepage text not found: ' + a[:70])
                hits[a[:60]] = n
        if s != o: open(f, 'w', encoding='utf-8').write(s)
    return hits


def guard(out):
    """Files that still show any banned wording (empty list = clean)."""
    rx = re.compile('|'.join(BANNED))
    bad = []
    for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/video' in f: continue
        s = open(f, encoding='utf-8', errors='ignore').read()
        m = rx.search(s)
        if m: bad.append('%s (%s)' % (os.path.relpath(f, out), m.group(0)))
    return bad
