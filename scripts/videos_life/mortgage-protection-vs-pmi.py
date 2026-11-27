"""Mortgage protection vs. PMI: who each one protects. For /mortgage-protection-insurance.
Facts from scripts/onyx/data/patches/mortgage.json and the live page (CFPB, NAIC, va.gov). No prices.
"""
import video_life as K
P = K.P

CFPB_PMI = 'https://www.consumerfinance.gov/ask-cfpb/what-is-private-mortgage-insurance-en-122/'
CFPB_MI = 'https://www.consumerfinance.gov/ask-cfpb/what-is-mortgage-insurance-and-how-does-it-work-en-1953/'
VA_FEE = 'https://www.va.gov/housing-assistance/home-loans/funding-fee-and-closing-costs/'
NAIC = 'https://content.naic.org/article/consumer-insight-credit-insurance'

VIDEO = dict(
    title='Mortgage protection vs. PMI: who each one protects',
    description='PMI protects the lender if you stop paying. Mortgage protection is life insurance you own that pays the person you name. '
                'Here is how they compare, and what to check before you buy.',
    poster=4.6,
    sources=[
        dict(fact='PMI protects the lender, not you, if you stop making payments on your loan.', url=CFPB_PMI, date='reviewed Nov 9, 2026'),
        dict(fact='A lender may require PMI on a conventional loan when the down payment is less than 20 percent.', url=CFPB_PMI, date='reviewed Nov 9, 2026'),
        dict(fact='FHA mortgage insurance is required on all FHA loans.', url=CFPB_MI, date='reviewed Aug 28, 2026'),
        dict(fact='The VA guarantee takes the place of mortgage insurance and works in a similar way (protects the lender).', url=CFPB_MI, date='reviewed Aug 28, 2026'),
        dict(fact='Credit life insurance proceeds are paid directly to the creditor (the lender).', url=NAIC, date='modified Jan 16, 2024'),
        dict(fact='Mortgage protection is a term life policy you own; it pays the beneficiary you name; it is optional. '
                  'Compare what you owe, years left and coverage you already carry.',
             url='https://honorbrook-insurance.com/mortgage-protection-insurance', date='page text, checked 2026-11-25'),
    ],
    scenes=[
        K.scene(K.hook('For homeowners', ['Mortgage protection', 'vs. PMI'], sub='Who each one protects', icon='home'),
                [P('Mortgage protection and PMI sound alike.'),
                 P('Here is who each one protects.')], pre=0.1, post=0.6),
        K.scene(K.fact_card('Private mortgage insurance', 'The lender', ['If you stop making payments on the loan',
                                                                        'A lender may require it with under 20% down'],
                            head='PMI protects', source='Source: consumerfinance.gov, PMI (reviewed Nov 9, 2026)'),
                [P('PMI protects the lender if you stop making payments.'),
                 P('A lender may require it with less than 20 percent down.',
                   'A lender may require it with less than twenty percent down.')]),
        K.scene(K.checklist('FHA and VA loans', 'Their own versions',
                            ['FHA: mortgage insurance on all FHA loans', 'VA: VA backing takes its place',
                             'Both protect the lender, not you'],
                            start=1, mark_kind=None, icons=['doc', 'doc', 'shield'],
                            note='Source: consumerfinance.gov, mortgage insurance (reviewed Aug 28, 2026)'),
                [P('FHA and VA loans have their own versions.'),
                 P('FHA loans require mortgage insurance.'),
                 P('On VA loans, VA backing takes its place.'),
                 P('Like PMI, they protect the lender, not you.')]),
        K.scene(K.fact_card('Mortgage protection', 'Your family', ['Life insurance that you own',
                                                                  'Pays the person you name'],
                            head='It protects'),
                [P('Mortgage protection is different.'),
                 P('It is life insurance that you own.'),
                 P('It pays the person you name if you die during the term.')]),
        K.scene(K.two_column('Side by side', 'Who each one protects',
                             ('PMI', ['Protects the lender', 'A lender may require it', 'Does not pay your family']),
                             ('Mortgage protection', ['Protects your family', 'Optional: you choose it', 'Pays the person you name']),
                             left_mark='dot', right_mark='check'),
                [P('PMI protects the lender. A lender may require it.'),
                 P('Mortgage protection protects your family. It is optional.')]),
        K.scene(K.fact_card('Watch the name', 'Ask who gets paid', ['Credit life sold with a loan pays the lender',
                                                                   'A term policy you own pays your family'],
                            source='Source: content.naic.org, credit insurance (Jan 2024)'),
                [P('Watch the name. Ask who gets paid.'),
                 P('Credit life sold with a loan pays the lender.'),
                 P('A term policy you own pays your family.')]),
        K.scene(K.checklist('Before you buy', 'Check three numbers',
                            ['What you owe on the home', 'Years left on the loan', 'Life insurance you already have'],
                            start=1, icons=['home', 'clock', 'shield']),
                [P('Before you buy, check three numbers.'),
                 P('What you owe on the home.'),
                 P('The years left on the loan.'),
                 P('And the life insurance you already have.'),
                 P('If there is a gap, a term policy sized to the loan is one way to fill it.')]),
        K.end_scene(),
    ])
