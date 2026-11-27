"""What is a fixed indexed annuity? The plain-English version.
For /blog/what-is-a-fixed-indexed-annuity-fia (and /annuities).
Facts only from those two built pages (staging/site-onyx, read Nov 27, 2026). The two tax lines were also confirmed on irs.gov
(Topic no. 410 and Publication 575). No prices, no rate examples, no company names.
"""
import video_life as K
P = K.P

BLOG = 'https://honorbrook-insurance.com/blog/what-is-a-fixed-indexed-annuity-fia'
PAGE = 'https://honorbrook-insurance.com/annuities'
D_BLOG = 'page dated Oct 12, 2026; read Nov 27, 2026'
D_PAGE = 'page updated June 2026; read Nov 27, 2026'
IRS_410 = 'https://www.irs.gov/taxtopics/tc410'
IRS_575 = 'https://www.irs.gov/publications/p575'

VIDEO = dict(
    title='What is a fixed indexed annuity? The plain-English version',
    description=('A fixed indexed annuity is a contract with an insurance company, not a market investment. Interest is linked to an index '
                 'and limited by caps, participation rates or spreads. Here is how the floor, surrender charges and taxes work, and who it may fit.'),
    poster=4.3,
    sources=[
        dict(fact='A fixed indexed annuity (FIA) is a deferred annuity issued by an insurance company. Interest is linked to a market index, '
                  'but the money is not invested in the market.', url=BLOG, date=D_BLOG),
        dict(fact='Crediting limits: a cap rate (the maximum interest for a period), a participation rate (the percentage of the index gain '
                  'that counts) and a spread (a percentage subtracted from the gain). They are set by the insurer and can change.',
             url=BLOG, date=D_BLOG),
        dict(fact='If the index falls, the credited interest is generally zero rather than negative. This is often called a floor.',
             url=BLOG, date=D_BLOG),
        dict(fact='FIAs are designed to be held for a period, commonly several years. Withdrawing more than the free-withdrawal amount '
                  'during the surrender period can bring a surrender charge. Not a place for emergency money.', url=BLOG, date=D_BLOG),
        dict(fact='Growth inside a non-qualified FIA is tax-deferred; gains are taxed as ordinary income when withdrawn.', url=BLOG, date=D_BLOG),
        dict(fact='Withdrawals before age 59½ can be subject to an additional 10% federal tax. Confirmed on irs.gov: pension or annuity '
                  'payments before age 59½ may be subject to an additional 10% tax on early distributions, with exceptions.',
             url=IRS_410, date='IRS Topic no. 410, page last reviewed Oct 16, 2026; read Nov 27, 2026'),
        dict(fact='The taxable part of an annuity distribution is treated as ordinary income (confirms the page line on taxable withdrawals).',
             url=IRS_575, date='IRS Publication 575 (2025); read Nov 27, 2026'),
        dict(fact='May fit someone near or in retirement who is comfortable leaving the money untouched for the surrender period. '
                  'Anyone who may need the money soon should be cautious.', url=BLOG, date=D_BLOG),
        dict(fact="Guarantees depend on the issuing company's claims-paying ability. Insurance and annuity products are not bank deposits "
                  'and are not FDIC-insured. A CD is FDIC-insured and has fixed terms; each has a different role.', url=BLOG, date=D_BLOG),
        dict(fact="Principal protection in an FIA is by contract terms, subject to the issuing company's claims-paying ability and to "
                  'surrender charges if you withdraw early.', url=PAGE, date=D_PAGE),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Annuities', ['What is a fixed', 'indexed annuity?'], sub='The plain-English version', icon='doc'),
                [P('What is a fixed indexed annuity?'),
                 P('Here is the plain-English version.')], pre=0.1, post=0.5),
        # 2. What it is
        K.scene(K.fact_card('The basics', 'An insurance contract',
                            ['A contract with an insurance company', 'Not a market investment'], head='It is', at=[0, 0]),
                [P('It is a contract with an insurance company, not a market investment.')], post=0.5),
        # 3. Index credits and their limits
        K.scene(K.checklist('How interest works', 'Linked to an index, with limits',
                            ['Caps', 'Participation rates', 'Spreads'],
                            at=[1, 1, 1], mark_kind=None, icons=['1', '2', '3'],
                            note='These limit the interest that is credited.'),
                [P('Interest is linked to a market index.'),
                 P('Caps, participation rates or spreads limit the interest that is credited.')], post=0.5),
        # 4. The floor
        K.scene(K.fact_card('In a down year', 'The floor',
                            ['If the index falls, credited interest is generally zero', 'Not negative'], at=[0, 0]),
                [P('If the index falls, credited interest is generally zero, not negative.'),
                 P('That is often called the floor.')], post=0.5),
        # 5. Surrender charges
        K.scene(K.fact_card('Access to your money', 'Surrender charges',
                            ['Built to be held for years', 'Withdraw more than the contract allows early, and they may apply'],
                            start=0),
                [P('It is built to be held for years.'),
                 P('Withdraw more than the contract allows early, and surrender charges may apply.')], post=0.5),
        # 6. Taxes
        K.scene(K.fact_card('Tax basics', 'Tax-deferred',
                            ['Withdrawals can be taxable', 'Before age 59½, an additional 10% federal tax can apply'],
                            source='Source: irs.gov, Topic no. 410 (reviewed Oct 16, 2026)', at=[0, 1]),
                [P('Growth is tax-deferred, but withdrawals can be taxable.'),
                 P('Before age 59½, an additional 10% federal tax can apply.',
                   'Before age fifty nine and a half, an additional ten percent federal tax can apply.')], post=0.5),
        # 7. Who it may and may not fit
        K.scene(K.checklist('Who it may fit', 'It depends on your timeline',
                            ['May fit: near or in retirement, money can stay untouched', 'Be cautious: you may need the money soon'],
                            start=0, mark_kind=['check', 'x'], icons=['person', 'clock']),
                [P('It may fit someone near or in retirement, whose money can stay untouched.'),
                 P('Be cautious if you may need the money soon.')], post=0.5),
        # 8. Limits
        K.scene(K.checklist('Keep in mind', 'Know the limits',
                            ["Guarantees depend on the insurer's claims-paying ability", 'Not a bank deposit. Not FDIC insured.',
                             'Not better than other savings, just a different role', 'General education, not tax advice'],
                            start=0, mark_kind=None, icons=['shield', 'lock', 'scale', 'chat']),
                [P("Guarantees depend on the insurer's claims-paying ability."),
                 P('Not a bank deposit. Not FDIC insured.', 'Not a bank deposit. Not F D I C insured.'),
                 P('Not better than other savings, just a different role.'),
                 P('General education, not tax advice.')], post=0.5),
        K.end_scene(),
    ])
