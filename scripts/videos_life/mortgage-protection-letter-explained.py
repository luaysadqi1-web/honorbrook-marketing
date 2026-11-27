"""That mortgage protection letter after closing: what it is. For /blog/mortgage-protection-letter-after-closing.
Facts only from the built page text (staging/site-onyx/blog/mortgage-protection-letter-after-closing.html); each one was
re-read on the primary source the page links (NAIC, CFPB, Tennessee Attorney General, Code of Virginia) on Nov 26, 2026.
No prices, no company names. Neutral tone: the letter may be an advertisement; it is never called anything else.
"""
import video_life as K
P = K.P

PAGE = 'https://honorbrook-insurance.com/blog/mortgage-protection-letter-after-closing'
VA_227 = 'https://law.lis.virginia.gov/vacode/title17.1/chapter2/section17.1-227/'
VA_208 = 'https://law.lis.virginia.gov/vacode/title17.1/chapter2/section17.1-208/'
TN_AG = 'https://www.tn.gov/attorneygeneral/news/2022/6/29/pr22-22.html'
NAIC_CREDIT = 'https://content.naic.org/article/consumer-insight-credit-insurance'
NAIC_LIFE = 'https://content.naic.org/insurance-topics/life-insurance'
CFPB_MI = 'https://www.consumerfinance.gov/ask-cfpb/what-is-mortgage-insurance-and-how-does-it-work-en-1953/'

VIDEO = dict(
    title='That mortgage protection letter after closing: what it is',
    description=('Why a mortgage protection letter can arrive after closing, why it may not be from your lender, '
                 'and 5 things to check before you reply. Mortgage protection is life insurance, and buying it is your choice.'),
    poster=4.0,
    sources=[
        dict(fact='Deeds and mortgages are recorded in local land records (Virginia example: recorded in the clerk of court\'s deed book).',
             url=VA_227, date='text as shown Nov 25, 2026; checked Nov 26, 2026'),
        dict(fact='Those records are generally open to the public (Virginia example: open to inspection in the office of the clerk by any person, with some exceptions).',
             url=VA_208, date='text as shown Nov 25, 2026; checked Nov 26, 2026'),
        dict(fact='Some mortgage information, such as the name of your lender and servicer, is public record, so a letter that shows your lender\'s name did not necessarily come from your lender.',
             url=TN_AG, date='June 29, 2022; checked Nov 26, 2026'),
        dict(fact='If credit insurance is optional, a lender cannot deny you credit for not buying it; the one exception named is PMI.',
             url=NAIC_CREDIT, date='Nov 1, 2008; checked Nov 26, 2026'),
        dict(fact='Mortgage insurance such as PMI protects the lender, not you, if you fall behind on your payments.',
             url=CFPB_MI, date='reviewed Aug 28, 2026; checked Nov 26, 2026'),
        dict(fact='Confirm the company or agent offering insurance is legitimate and licensed in your state, through your state insurance department.',
             url=NAIC_CREDIT, date='Nov 1, 2008; checked Nov 26, 2026'),
        dict(fact='Level term: the death benefit and premium are fixed for the term. Decreasing term: the death benefit goes down over time.',
             url=NAIC_LIFE, date='last updated Nov 14, 2025; checked Nov 26, 2026'),
        dict(fact='A letter like this may be an advertisement for life insurance; mortgage protection is life insurance and is optional; an advertisement does not need an answer; '
                  'count the life insurance you already have; ask for a second quote on level term for the same amount and years; a letter is not a reason to drop coverage you own.',
             url=PAGE, date='page dated November 2026; page text checked Nov 26, 2026'),
    ],
    scenes=[
        # 1. Hook: the title, word for word
        K.scene(K.hook('For new homeowners', ['That mortgage protection', 'letter after closing'], sub='What it is', icon='mail'),
                [P('That mortgage protection letter after closing:'),
                 P('here is what it is, and what to check before you reply.')], pre=0.1, post=0.6),
        # 2. Why it arrives
        K.scene(K.fact_card('Why it arrives', 'Public records',
                            ['Deeds and mortgages are recorded in local land records',
                             'Those records are generally open to the public'],
                            source='Example: Code of Virginia 17.1-227 and 17.1-208'),
                [P('A home purchase creates public records.'),
                 P('Deeds and mortgages are recorded in local land records.'),
                 P('Those records are generally open to the public.')]),
        # 3. Who sent it
        K.scene(K.fact_card('Who sent it', 'Maybe not your lender',
                            ["Your lender's name can be public record",
                             'The letter may be an advertisement for life insurance'],
                            source='Public record: Tennessee Attorney General, June 29, 2022', at=[0, 1]),
                [P("A letter that shows your lender's name did not necessarily come from your lender."),
                 P('It may be an advertisement for life insurance.')]),
        # 4. Optional, and not PMI
        K.scene(K.two_column('Two different things', 'Mortgage protection is optional',
                             ('Mortgage protection', ['Life insurance', 'Buying it is your choice']),
                             ('PMI', ['A lender may require it', 'Protects the lender, not you']),
                             left_mark='check', right_mark='dot',
                             note='Sources: NAIC, credit insurance (Nov 1, 2008). CFPB, mortgage insurance (reviewed Aug 28, 2026)'),
                [P('Mortgage protection is life insurance, and buying it is your choice.'),
                 P('PMI is different. A lender may require it, and it protects the lender.',
                   'P M I is different. A lender may require it, and it protects the lender.')]),
        # 5. The checklist: the centerpiece
        K.scene(K.checklist('Before you reply', 'Check 5 things',
                            ['Who sent it: agent and insurance company', 'Are both licensed in your state?',
                             'Level term or decreasing term?', 'The life insurance you already have',
                             'A second quote on level term'], start=1),
                [P('Before you reply, check 5 things.', 'Before you reply, check five things.'),
                 P('1. Find the names of the agent and the insurance company.',
                   'One. Find the names of the agent and the insurance company.'),
                 P('2. Confirm both are licensed with your state insurance department.',
                   'Two. Confirm both are licensed with your state insurance department.'),
                 P('3. Ask if it is level term or decreasing term.',
                   'Three. Ask if it is level term or decreasing term.'),
                 P('4. Count the life insurance you already have.',
                   'Four. Count the life insurance you already have.'),
                 P('5. Get a second quote on level term, and compare.',
                   'Five. Get a second quote on level term, and compare.')]),
        # 6. No pressure
        K.scene(K.fact_card('How to decide', 'In your own time',
                            ['An advertisement does not need an answer',
                             'A letter is not a reason to drop coverage you own'], at=[0, 1]),
                [P('An advertisement does not need an answer.'),
                 P('And a letter is not a reason to drop coverage you own.')]),
        K.end_scene(),
    ])
