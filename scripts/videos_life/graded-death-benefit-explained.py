"""Final expense: level benefit or graded benefit? For /blog/graded-death-benefit-final-expense-explained.html.
Facts only from the built page text (staging/site-onyx/blog/graded-death-benefit-final-expense-explained.html, dated October 2026).
The page links no government source for these points, so the page itself is the source. No prices, no company names.
"""
import video_life as K
P = K.P

PAGE = 'https://honorbrook-insurance.com/blog/graded-death-benefit-final-expense-explained'
DATE = 'page dated October 2026; page text checked 2026-11-26'
VARY = 'A common pattern. Years and percentages differ by policy.'

VIDEO = dict(
    title='Final expense: level benefit or graded benefit?',
    description=('A level (immediate) benefit can pay the full benefit from day 1. A graded benefit has a waiting period, often the '
                 'first 2 or 3 years. Here is how each one works, why health answers decide, and 3 questions to ask before you apply.'),
    poster=4.5,
    sources=[
        dict(fact='If your health qualifies, a policy can pay the full benefit from day 1 (an immediate benefit).', url=PAGE, date=DATE),
        dict(fact='With a graded benefit the full benefit is not paid if death is from natural causes during an initial period, often the first 2 or 3 years.',
             url=PAGE, date=DATE),
        dict(fact='During that period the beneficiary typically receives a reduced amount: a return of premiums paid, often with some interest, or a percentage of the face amount.',
             url=PAGE, date=DATE),
        dict(fact='After the grading period the full face amount is paid. Many policies pay the full benefit from day 1 if death results from an accident. Years and percentages differ by policy.',
             url=PAGE, date=DATE),
        dict(fact='A graded benefit goes to people with health conditions that rule out an immediate benefit, to policies with no health questions, and to answers that place the applicant in a graded class.',
             url=PAGE, date=DATE),
        dict(fact='Questions to ask: how long is the grading period, what the beneficiary receives during it, and whether accidental death pays in full.',
             url=PAGE, date=DATE),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Final expense', ['Level benefit or', 'graded benefit?'], sub='What your family would receive', icon='scale'),
                [P('Final expense: level benefit or graded benefit?'),
                 P('Here is how each one works.')], pre=0.1, post=0.6),
        # 2. Level benefit
        K.scene(K.fact_card('Level benefit', 'From day 1',
                            ['Also called an immediate benefit', 'The full benefit, if your health qualifies'], at=[0, 1]),
                [P('A level benefit is also called an immediate benefit.'),
                 P('If your health qualifies, it can pay the full benefit from day 1.',
                   'If your health qualifies, it can pay the full benefit from day one.')], post=0.4),
        # 3. Graded benefit: the waiting period (timeline)
        K.scene(K.timeline('Graded benefit', 'A waiting period first',
                           [('Years 1-2', 'Sometimes 3. Natural causes: a reduced amount'),
                            ('After', 'The full face amount is paid')],
                           at=[0, 3], note=VARY),
                [P('A graded benefit has a waiting period, often the first 2 or 3 years.',
                   'A graded benefit has a waiting period, often the first two or three years.'),
                 P('If death is from natural causes in that time, the beneficiary receives a reduced amount.'),
                 P('Often that is the premiums paid, with some interest, or a percentage of the benefit.'),
                 P('After that period, the full face amount is paid.')], post=0.4),
        # 4. Side by side (centerpiece)
        K.scene(K.two_column('Side by side', 'Level or graded',
                             ('Level benefit', ['Full benefit from day 1', 'Your health has to qualify']),
                             ('Graded benefit', ['Reduced amount in the early years', 'Full benefit after that period',
                                                 'Accident: many pay from day 1']),
                             left_at=0, right_at=[1, 1, 2], left_mark='dot', right_mark='dot', note=VARY),
                [P('Level: the full benefit from day 1.', 'Level: the full benefit from day one.'),
                 P('Graded: a reduced amount early, then the full benefit.'),
                 P('Many policies pay accidental death in full from day 1.',
                   'Many policies pay accidental death in full from day one.')], post=0.4),
        # 5. Why health answers decide
        K.scene(K.checklist('Who gets a graded benefit', 'Health answers decide',
                            ['Health conditions that rule out a level benefit', 'Policies with no health questions',
                             'Answers that place you in a graded class'],
                            start=1, mark_kind=None, icons=['heart', 'doc', 'person'],
                            note='Be accurate on applications. Misstatements can lead to denied claims.'),
                [P('Your health answers decide which one is offered.'),
                 P('Some health conditions rule out a level benefit.'),
                 P('Policies with no health questions are typically graded.'),
                 P('Some answers place you in a graded class.')], post=0.4),
        # 6. Questions to ask
        K.scene(K.checklist('Before you apply', '3 questions to ask',
                            ['How long is the grading period?', 'What does my beneficiary receive in that time?',
                             'Does accidental death pay in full?'],
                            start=1, icons=['clock', 'people', 'shield']),
                [P('Before you apply, ask 3 questions.', 'Before you apply, ask three questions.'),
                 P('How long is the grading period?'),
                 P('What does my beneficiary receive in that time?'),
                 P('Does accidental death pay in full?')], post=0.4),
        K.end_scene(),
    ])
