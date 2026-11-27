"""Final expense insurance or a prepaid funeral plan? For /blog/final-expense-vs-burial-insurance-vs-prepaid-funeral-plan.
Facts only from the built page (staging/site-onyx, read Nov 27, 2026). The two Funeral Rule points were confirmed on
consumer.ftc.gov (The FTC Funeral Rule, read Nov 27, 2026). No prices, no company names.
"""
import video_life as K
P = K.P

BLOG = 'https://honorbrook-insurance.com/blog/final-expense-vs-burial-insurance-vs-prepaid-funeral-plan'
D_BLOG = 'page dated October 2026; read Nov 27, 2026'
FTC = 'https://consumer.ftc.gov/articles/ftc-funeral-rule'
D_FTC = 'page shows July 2012; read Nov 27, 2026'

VIDEO = dict(
    title='Final expense insurance or a prepaid funeral plan?',
    description=('Final expense insurance, also sold as burial insurance, is a small whole life policy that pays the beneficiary you name. '
                 'A prepaid funeral plan is a contract with a funeral home. Here is who gets the money with each one, and what to ask before you sign.'),
    poster=3.6,
    sources=[
        dict(fact='Final expense insurance is a small whole life insurance policy; the insurer pays a death benefit to your named beneficiary.',
             url=BLOG, date=D_BLOG),
        dict(fact='"Burial insurance" is in many cases the same product as final expense insurance, sold under a different name.',
             url=BLOG, date=D_BLOG),
        dict(fact='A prepaid funeral plan is a contract with a funeral home; you select services and merchandise ahead of time and pay in advance.',
             url=BLOG, date=D_BLOG),
        dict(fact='Side by side: insurance pays your named beneficiary, for any purpose, and is not tied to a location. '
                  'A prepaid plan pays the funeral home, for listed items, and is often tied to one provider.', url=BLOG, date=D_BLOG),
        dict(fact='If you move or the funeral home closes, you may need to transfer or cancel a prepaid plan. Whether you can cancel and what you '
                  'receive back depends on state law and the contract. Ask: is it portable if I move, and where is the money held?',
             url=BLOG, date=D_BLOG),
        dict(fact='Federal rules require funeral homes to give you itemized price lists, and you generally can choose only the items you want.',
             url=BLOG, date=D_BLOG),
        dict(fact='FTC Funeral Rule, confirmed: "Get a written, itemized price list when you visit a funeral home" and '
                  '"Buy only the funeral arrangements you want."', url=FTC, date=D_FTC),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Planning ahead', ['Final expense insurance', 'or a prepaid funeral plan?'], sub='Who gets the money', icon='scale'),
                [P('Final expense insurance, or a prepaid funeral plan?'),
                 P('Here is who gets the money with each one.')], pre=0.1, post=0.6),
        # 2. Final expense / burial insurance
        K.scene(K.fact_card('Final expense insurance', 'A small whole life policy',
                            ['Burial insurance: often the same product', 'It pays the beneficiary you name']),
                [P('Final expense insurance is a small whole life policy.'),
                 P('Burial insurance is often the same product, under a different name.'),
                 P('It pays the beneficiary you name.')]),
        # 3. Prepaid plan
        K.scene(K.fact_card('Prepaid funeral plan', 'A contract with a funeral home',
                            ['You choose services ahead of time', 'You pay in advance'], at=[1, 1]),
                [P('A prepaid funeral plan is a contract with a funeral home.'),
                 P('You choose services ahead of time, and pay in advance.')]),
        # 4. Comparison (centerpiece)
        K.scene(K.two_column('Side by side', 'Who gets the money',
                             ('Final expense insurance', ['Pays your named beneficiary', 'For any purpose', 'Not tied to a location']),
                             ('Prepaid funeral plan', ['Pays the funeral home', 'For the items listed', 'Often tied to one provider']),
                             left_at=[0, 1, 2], right_at=[3, 3, 4]),
                [P('Final expense insurance pays your named beneficiary.'),
                 P('The money can be used for any purpose.'),
                 P('It is not tied to a location.'),
                 P('A prepaid plan pays the funeral home, for the items listed.'),
                 P('It is often tied to one provider.')]),
        # 5. If you move or change your mind
        K.scene(K.checklist('If you move or change your mind', 'Ask before you sign',
                            ['Is the plan portable if I move?', 'Can I cancel, and what do I get back?', 'Where is the money held?'],
                            start=1, mark_kind=None, icons=['home', 'doc', 'lock'],
                            note='Refund rules depend on state law and the contract.'),
                [P('If you move, a prepaid plan may need to be transferred or canceled.'),
                 P('Before you sign, ask: is the plan portable if I move?'),
                 P('Can I cancel, and what do I get back?'),
                 P('Where is the money held?')]),
        # 6. Funeral Rule
        K.scene(K.fact_card('Your rights', 'Itemized price list',
                            ['Federal rules require funeral homes to give you one', 'You can generally choose only the items you want'],
                            source='Source: ftc.gov, The FTC Funeral Rule', at=[0, 1]),
                [P('Federal rules require funeral homes to give you an itemized price list.'),
                 P('You can generally choose only the items you want.')]),
        K.end_scene(),
    ])
