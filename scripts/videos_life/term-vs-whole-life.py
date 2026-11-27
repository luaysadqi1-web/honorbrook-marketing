"""Term or whole life: how to tell which fits. For /blog/term-vs-whole-life-insurance-which-fits-your-family.
Facts only from three built pages (staging/site-onyx, read Nov 27, 2026): the blog post, /term-life-insurance and
/whole-life-insurance. None of the facts used here carries a government link on those pages, so the pages are the source.
No prices, no rates, no company names.
"""
import video_life as K
P = K.P

BLOG = 'https://honorbrook-insurance.com/blog/term-vs-whole-life-insurance-which-fits-your-family'
TERM = 'https://honorbrook-insurance.com/term-life-insurance'
WHOLE = 'https://honorbrook-insurance.com/whole-life-insurance'
D_BLOG = 'page dated Sep 29, 2026; read Nov 27, 2026'
D_TERM = 'page updated August 2026; read Nov 27, 2026'
D_WHOLE = 'page updated November 2026; read Nov 27, 2026'

VIDEO = dict(
    title='Term or whole life: how to tell which fits',
    description=('Term life covers a set number of years. Whole life is permanent and builds cash value. '
                 'Here is what each is commonly used for, and three questions that help you tell which fits.'),
    poster=3.4,
    sources=[
        dict(fact='Term life pays a death benefit if you pass away during a set period, commonly 10, 20, or 30 years. '
                  'If the term ends and you are still living, the coverage ends.', url=BLOG, date=D_BLOG),
        dict(fact='Whole life is a type of permanent insurance. As long as premiums are paid, it is designed to stay in force '
                  'for your lifetime. Part of each premium builds cash value.', url=BLOG, date=D_BLOG),
        dict(fact='Term has no savings component. For the same death benefit, whole life costs more than term.', url=BLOG, date=D_BLOG),
        dict(fact='Paying off a mortgage or replacing income until the kids are grown are needs with an end date, which fits term. '
                  'Final expenses or supporting a lifelong dependent are needs that do not expire, which is where permanent coverage fits. '
                  'Many families use both.', url=BLOG, date=D_BLOG),
        dict(fact='Questions that help decide: how long the need lasts (time-limited or permanent), whether the premium fits your budget '
                  'for the long run, and any coverage you already have, including through work.', url=TERM, date=D_TERM),
        dict(fact="Whole life guarantees depend on the claims-paying ability of the insurance company.", url=WHOLE, date=D_WHOLE),
        dict(fact='Policy loans and withdrawals reduce the cash value and death benefit.', url=WHOLE, date=D_WHOLE),
        dict(fact='Policy availability, features and pricing vary by state, carrier and individual circumstances.', url=BLOG, date=D_BLOG),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Life insurance', ['Term or', 'whole life?'], sub='How to tell which fits', icon='scale'),
                [P('Term or whole life?'),
                 P('Here is how to tell which fits.')], pre=0.1, post=0.6),
        # 2. Term
        K.scene(K.fact_card('Term life', 'A set number of years',
                            ['Commonly 10, 20 or 30 years', 'If you outlive the term, coverage ends'], start=0),
                [P('Term life covers a set number of years, commonly 10, 20 or 30.',
                   'Term life covers a set number of years, commonly ten, twenty, or thirty.'),
                 P('If you outlive the term, coverage ends.')]),
        # 3. Whole life
        K.scene(K.fact_card('Whole life', 'Permanent coverage',
                            ['Designed to last your lifetime, as long as premiums are paid', 'It builds cash value'], start=0),
                [P('Whole life is permanent. It is designed to last your lifetime, as long as premiums are paid.'),
                 P('It also builds cash value.')]),
        # 4. Side by side (centerpiece)
        K.scene(K.two_column('Side by side', 'Term or whole life',
                             ('Term life', ['Covers a set number of years', 'Does not build cash value', 'Costs less for the same death benefit']),
                             ('Whole life', ['Designed to last your lifetime', 'Builds cash value', 'Costs more for the same death benefit']),
                             left_at=[0, 0, 2], right_at=[1, 1, 2]),
                [P('Term covers a set number of years and does not build cash value.'),
                 P('Whole life is permanent and builds cash value.'),
                 P('For the same death benefit, whole life costs more than term.')]),
        # 5. What each is commonly used for
        K.scene(K.two_column('Common uses', 'Match it to the need',
                             ('Term: needs with an end date', ['Paying off a mortgage', 'Income until the kids are grown']),
                             ('Whole life: needs that do not expire', ['Final expenses', 'A lifelong dependent']),
                             left_at=0, right_at=1, note='Many families use both.'),
                [P('Term fits needs with an end date, like a mortgage, or income until the kids are grown.'),
                 P('Whole life fits needs that do not expire, like final expenses or a lifelong dependent.'),
                 P('Many families use both.')]),
        # 6. Questions that help decide
        K.scene(K.checklist('How to tell', 'Ask three questions',
                            ['How long does the need last?', 'What fits your budget for the long run?', 'What coverage do you already have?'],
                            start=1, icons=['clock', 'scale', 'shield']),
                [P('Ask three questions.'),
                 P('How long does the need last?'),
                 P('What fits your budget for the long run?'),
                 P('And what coverage do you already have?')]),
        # 7. Caveats
        K.scene(K.checklist('Keep in mind', 'Two things to know',
                            ["Whole life guarantees depend on the insurer's claims-paying ability",
                             'Loans and withdrawals reduce the death benefit'],
                            start=0, mark_kind=None, icons=['shield', 'arrow'],
                            note='Features vary by state and company.'),
                [P("Whole life guarantees depend on the insurer's claims-paying ability."),
                 P('Loans and withdrawals reduce the death benefit.')]),
        K.end_scene(),
    ])
