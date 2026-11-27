"""What is indexed universal life? The plain-English version.
For /blog/what-is-indexed-universal-life-iul-how-it-works-cost-risks and /indexed-universal-life.
Facts only from those two built pages (staging/site-onyx, read Nov 26, 2026). No prices, no rate examples, no company names.
"""
import video_life as K
P = K.P

BLOG = 'https://honorbrook-insurance.com/blog/what-is-indexed-universal-life-iul-how-it-works-cost-risks'
PAGE = 'https://honorbrook-insurance.com/indexed-universal-life'
D_BLOG = 'page dated Oct 12, 2026; read Nov 26, 2026'
D_PAGE = 'page updated November 2026; read Nov 26, 2026'

VIDEO = dict(
    title='What is indexed universal life? The plain-English version',
    description=('Indexed universal life (IUL) is permanent life insurance with a cash value. Interest credits are linked to an index, '
                 'but the money is not invested in the market. Here is how caps, participation rates, the floor, policy charges and lapse risk work.'),
    poster=4.3,
    sources=[
        dict(fact='IUL is permanent life insurance with a death benefit, paid while the policy is in force, and a cash value account.',
             url=BLOG, date=D_BLOG),
        dict(fact='The cash value earns interest credits linked to an index without being directly invested in it; '
                  'you do not own the stocks and do not receive their dividends.', url=PAGE, date=D_PAGE),
        dict(fact='Cap: the maximum interest credited in a period. Participation rate: the percentage of the index gain you receive. '
                  'Floor: the minimum credited, often zero (commonly 0%). The floor protects against index losses, not policy fees.',
             url=PAGE, date=D_PAGE),
        dict(fact='Caps and participation rates are not locked in; the insurer can change them within limits set in the policy.',
             url=PAGE, date=D_PAGE),
        dict(fact='Policy charges come out of the cash value, and the cost of insurance rises with age. '
                  'Surrender charges can apply if you cancel or take money out in the early years.', url=PAGE, date=D_PAGE),
        dict(fact='If the cash value is not enough to cover the cost of insurance and fees, the policy can lapse. '
                  'Loans and withdrawals reduce the death benefit and can cause a lapse.', url=PAGE, date=D_PAGE),
        dict(fact="Every guarantee in the policy, including the floor, depends on the claims-paying ability of the insurance company. "
                  'Illustrated values are projections, not promises.', url=PAGE, date=D_PAGE),
        dict(fact='IUL is not a substitute for tax-advantaged retirement accounts for most people. Consult a tax professional.',
             url=BLOG, date=D_BLOG),
        dict(fact='Background the page links: NAIC life insurance illustrations page and NAIC Life Insurance Buyer\'s Guide '
                  '(an illustration shows both guaranteed and non-guaranteed elements of the policy; '
                  'ask what part of the policy value is not guaranteed).',
             url='https://content.naic.org/insurance-topics/life-insurance-illustrations', date='linked from the page; no figure taken from it'),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Life insurance', ['What is indexed', 'universal life?'], sub='The plain-English version', icon='shield'),
                [P('What is indexed universal life?'),
                 P('Here is the plain-English version.')], pre=0.1, post=0.6),
        # 2. What it is
        K.scene(K.fact_card('The basics', 'Permanent life insurance',
                            ['A death benefit', 'A cash value account'],
                            head='IUL is', at=[1, 1]),
                [P('Indexed universal life, or IUL, is permanent life insurance.',
                   'Indexed universal life, or I U L, is permanent life insurance.'),
                 P('It has a death benefit and a cash value account.')]),
        # 3. Linked to an index, not invested
        K.scene(K.fact_card('The index part', 'Linked, not invested',
                            ['Interest credits are linked to an index', 'Your money is not invested in the market'], start=0),
                [P('The cash value earns interest credits linked to an index.'),
                 P('But your money is not invested in the market.')]),
        # 4. Cap, participation rate, floor
        K.scene(K.checklist('How credits work', 'Caps and rates limit credits',
                            ['Cap: the maximum credit in a period', 'Participation rate: your share of the gain',
                             'Floor: the minimum credit, often 0%'],
                            start=0, mark_kind=None,
                            note='Caps and participation rates can change, within policy limits.'),
                [P('A cap is the maximum credit in a period.'),
                 P('A participation rate is your share of the index gain.'),
                 P('A floor is the minimum credit, often 0 percent.', 'A floor is the minimum credit, often zero percent.'),
                 P('Caps and participation rates can change, within policy limits.')]),
        # 5. Charges
        K.scene(K.checklist('What it costs', 'Charges come out',
                            ['Policy charges reduce cash value', 'The floor does not stop charges', 'Surrender charges may apply'],
                            start=0, mark_kind=None, icons=['doc', 'arrow', 'x']),
                [P('Policy charges reduce the cash value.'),
                 P('The floor does not stop those charges.'),
                 P('Surrender charges may apply.')]),
        # 6. Lapse risk
        K.scene(K.fact_card('The risk', 'It can lapse',
                            ['Loans and withdrawals reduce the death benefit', 'They can also cause a lapse'],
                            head='If underfunded', start=1),
                [P('An IUL can lapse if it is underfunded.', 'An I U L can lapse if it is underfunded.'),
                 P('Loans and withdrawals reduce the death benefit,'),
                 P('and they can cause a lapse.')]),
        # 7. Limits
        K.scene(K.checklist('Keep in mind', 'Know the limits',
                            ["Guarantees depend on the insurer's claims-paying ability", 'Illustrations are projections, not promises',
                             'Not a substitute for a retirement plan', 'General education, not tax advice'],
                            start=0, mark_kind=None, icons=['shield', 'doc', 'scale', 'chat']),
                [P("Guarantees depend on the insurer's claims-paying ability."),
                 P('Illustrations are projections, not promises.'),
                 P('An IUL is not a substitute for a retirement plan.', 'An I U L is not a substitute for a retirement plan.'),
                 P('This is general education, not tax advice.')]),
        K.end_scene(),
    ])
