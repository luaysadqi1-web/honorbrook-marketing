"""Own an IUL? Five questions for your annual review. For the page /iul-policy-review.
Facts: NAIC illustrations page and Model 582, NAIC Life Insurance Buyer's Guide, Virginia Form 30-A (see sources).
"""
import video_life as K
P = K.P

NAIC_PAGE = 'https://content.naic.org/insurance-topics/life-insurance-illustrations'
MODEL = 'https://content.naic.org/sites/default/files/model-law-582.pdf'
GUIDE = 'https://content.naic.org/sites/default/files/publication-lig-lp-consumer-life.pdf'
FORM = 'https://ris.dls.virginia.gov/uploads/14VAC5/forms/bd85f004265~1.pdf'
MODEL_DATE = 'NAIC Model 582, text dated April 2001 (model adopted 1995)'

VIDEO = dict(
    title='Own an IUL? Five questions for your annual review',
    description=('If you own an indexed universal life policy, you can ask the insurer for an in-force illustration. '
                 'This short video shows how to read it and five questions to check each year.'),
    poster=4.4,
    sources=[
        dict(fact='After the first policy anniversary, the policy owner may request updates on the policy, in the form of in-force illustrations.',
             url=NAIC_PAGE, date='Last updated 1/8/2026'),
        dict(fact='Upon the request of the policy owner, the insurer furnishes an in-force illustration (an illustration of a policy in force one year or more).',
             url=MODEL, date=MODEL_DATE),
        dict(fact='Guaranteed elements are shown before non-guaranteed elements; a zero is shown in the guaranteed column in a year with no guaranteed value.',
             url=MODEL, date=MODEL_DATE),
        dict(fact='Non-guaranteed values assume current non-guaranteed elements continue unchanged; the insurer can change the assumptions; results could be higher or lower.',
             url=MODEL, date=MODEL_DATE),
        dict(fact='Universal life lets you choose a flexible premium pattern as long as you pay enough to keep the policy in force.',
             url=GUIDE, date='Copyright 2026 NAIC'),
        dict(fact='The universal life annual report shows any outstanding loan, and amounts debited to the policy value by type (policy charges).',
             url=MODEL, date=MODEL_DATE),
        dict(fact='Surrender value is what is available after surrender charges, policy loans and loan interest.',
             url=MODEL, date=MODEL_DATE),
        dict(fact='A current cap or participation rate the policy does not guarantee is a non-guaranteed element, subject to change (owner-required IUL caveat).',
             url=MODEL, date=MODEL_DATE),
        dict(fact='Guarantees depend on the insurer (owner-required caveat; Form 30-A asks owners to compare the financial stability of the companies).',
             url=FORM, date='Form 30-A (eff. 4/07)'),
        dict(fact='A new policy has its own costs, and surrender charges may be deducted from the old one.', url=FORM, date='Form 30-A (eff. 4/07)'),
        dict(fact='A replacement may not be in your best interest, or it could be a good decision (suitable only some of the time).',
             url=FORM, date='Form 30-A (eff. 4/07)'),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Indexed universal life', ['Own an IUL?', 'Five questions', 'for your review'],
                       sub='Read the guaranteed column first', icon='doc'),
                [P('Own an IUL? Here are five questions for your annual review.',
                   'Own an I U L? Here are five questions for your annual review.')], pre=0.1, post=0.6),
        # 2. What an in-force illustration is
        K.scene(K.fact_card('Step one', 'In-force illustration',
                            ["The insurer's updated projection of your policy", 'After the first anniversary, you can ask'],
                            source='Source: NAIC, Life Insurance Illustrations (updated 1/8/2026)'),
                [P('Start by asking the insurer for an in-force illustration.'),
                 P("It is the insurer's updated projection of your policy."),
                 P('After the first policy anniversary, you can ask for one.')]),
        # 3. Guaranteed vs non-guaranteed
        K.scene(K.two_column('How to read it', 'Two kinds of columns',
                             ('Guaranteed', ['Shown first', 'Only what the policy guarantees', 'A zero means no guaranteed value']),
                             ('Non-guaranteed', ['Assumes current values continue', 'The insurer can change them', 'Results can be higher or lower']),
                             note='Source: NAIC Model 582 (April 2001)'),
                [P('The guaranteed column shows only what the policy guarantees.'),
                 P('The non-guaranteed column can change.')], post=1.7),   # holds the third right-hand row long enough to read
        # 4. Five questions: the centerpiece
        K.scene(K.checklist('Five questions', 'Check these each year',
                            ['Does the guaranteed column end, and when?', 'Is a loan balance growing?',
                             'Is your premium below what was illustrated?', 'When do surrender charges end?',
                             'What are the current cap and participation rate?'], start=0),
                [P('1. Does the guaranteed column end, and when?',
                   'One. Does the guaranteed column end, and when?'),
                 P('2. Is a loan balance growing?', 'Two. Is a loan balance growing?'),
                 P('3. Is your premium below what was illustrated?',
                   'Three. Is your premium below what was illustrated?'),
                 P('4. When do surrender charges end?', 'Four. When do surrender charges end?'),
                 P('5. What are the current cap and participation rate?',
                   'Five. What are the current cap and participation rate?')]),
        # 5. Required caveats
        K.scene(K.checklist('Good to know', 'Keep these in mind',
                            ['Caps and participation rates limit credits', 'Policy charges reduce cash value',
                             'Surrender charges may apply', 'Guarantees depend on claims-paying ability'],
                            start=0, mark_kind=None, icons=['scale', 'doc', 'lock', 'shield']),
                [P('Caps and participation rates limit index credits.'),
                 P('Policy charges reduce the cash value.'),
                 P('Surrender charges may apply.'),
                 P("Guarantees depend on the insurer's ability to pay claims.")], sfx=False),
        # 6. Replacement caution
        K.scene(K.fact_card('Before any change', 'Replacing a policy?',
                            ['A new policy has its own costs', 'The old one may deduct surrender charges',
                             'Replacing is suitable only some of the time'], start=0,
                            source='Source: Virginia Form 30-A, replacement notice (eff. 4/07)'),
                [P('A new policy has its own costs.'),
                 P('The old policy may deduct surrender charges.'),
                 P('Replacing a policy is suitable only some of the time.'),
                 P('This is general education, not tax advice.')]),
        # Standard end card, with the closing line split in two so the highlighted web address never runs into "or" on 9:16.
        K.scene(K.end(), [P(K.END_QUESTION),
                          P('Schedule a time at honorbrook-insurance.com,',
                            'Schedule a time at honorbrook insurance dot com,'),
                          P('or call (301) 615-8289.', 'or call three zero one, six one five, eight two eight nine.')],
                sfx=lambda ph: [(ph[1][0] + 0.55, 'ding')], pre=0.1, post=1.6),
    ])
