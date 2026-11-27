"""Leaving the military: your life insurance deadlines (for /veterans-life-insurance).
Facts only from scripts/onyx/data/patches/veterans.json (va.gov pages re-read Nov 24, 2026).
"""
import video_life as K
P = K.P

SRC = 'Source: va.gov, checked November 2026'

VIDEO = dict(
    title='Leaving the military: your life insurance deadlines',
    description=('The VA life insurance dates that count from the day you leave the military: 120 days for SGLI, '
                 '240 days for VGLI without proof of good health, and 1 year and 120 days to apply for VGLI.'),
    poster=5.6,
    sources=[
        dict(fact='SGLI coverage continues for 120 days after you leave the military.',
             url='https://www.va.gov/life-insurance/options-eligibility/sgli/', date='updated Nov 19, 2026; checked Nov 24, 2026'),
        dict(fact='Apply for VGLI within 240 days of leaving and you do not need to prove you are in good health.',
             url='https://www.va.gov/life-insurance/options-eligibility/vgli/', date='updated Oct 13, 2026; checked Nov 24, 2026'),
        dict(fact='After 240 days you can still apply for VGLI, with evidence of good health; the deadline to apply is 1 year and 120 days after you leave.',
             url='https://www.va.gov/life-insurance/options-eligibility/vgli/', date='updated Oct 13, 2026; checked Nov 24, 2026'),
        dict(fact='A spouse can convert FSGLI spouse coverage to a permanent individual policy, such as whole life, within 120 days of separation; child coverage cannot be converted.',
             url='https://www.va.gov/life-insurance/options-eligibility/fsgli/', date='updated Oct 14, 2026; checked Nov 24, 2026'),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Leaving the military', ['Your life insurance', 'deadlines'], sub='3 dates to know', icon='calendar'),
                [P('Leaving the military? Here are your life insurance deadlines.'),
                 P('3 dates to know, counted from the day you leave.', 'Three dates to know, counted from the day you leave.')],
                pre=0.1, post=0.6),
        # 2. Who we are
        K.scene(K.fact_card('Who we are', 'Independent agency',
                            ['VA program facts here come from va.gov.', 'Checked November 2026.'],
                            head=['Not affiliated', 'with the VA'], at=[1, 1]),
                [P('Honorbrook is an independent agency, not affiliated with the VA.',
                   'Honorbrook is an independent agency, not affiliated with the V A.'),
                 P('VA facts here come from va.gov, checked November 2026.',
                   'V A facts here come from V A dot gov, checked November twenty twenty six.')]),
        # 3. Timeline (centerpiece)
        K.scene(K.timeline('After you leave', 'Three VA dates',
                           [('120 days', 'SGLI coverage continues'),
                            ('240 days', 'Apply for VGLI with no proof of good health'),
                            ('1 yr+120 d', 'Last day to apply for VGLI')],
                           at=[0, 1, 3], note='Counted from the day you leave the military. ' + SRC),
                [P('Your SGLI coverage continues for 120 days after you leave.',
                   'Your S G L I coverage continues for one hundred twenty days after you leave.'),
                 P('Apply for VGLI within 240 days, with no need to prove good health.',
                   'Apply for V G L I within two hundred forty days, with no need to prove good health.'),
                 P('After that, you can still apply, with evidence of good health.'),
                 P('The deadline to apply for VGLI is 1 year and 120 days after you leave.',
                   'The deadline to apply for V G L I is one year and one hundred twenty days after you leave.')]),
        # 4. Spouse coverage
        K.scene(K.fact_card('Spouse coverage', '120 days',
                            ['A spouse can convert FSGLI spouse coverage',
                             'to a permanent individual policy, such as whole life.'],
                            source=SRC, start=1),
                [P('Spouse coverage under FSGLI has a 120-day date too.',
                   'Spouse coverage under F S G L I has a one hundred twenty day date too.'),
                 P('Within 120 days of your separation, your spouse can convert it',
                   'Within one hundred twenty days of your separation, your spouse can convert it'),
                 P('to a permanent individual policy, such as whole life.')]),
        # 5. Compare
        K.scene(K.checklist('A simple plan', 'Plan around your dates',
                            ['Mark day 120 and day 240', 'Compare private options next to VGLI'],
                            start=0, icons=['calendar', 'scale']),
                [P('Mark day 120 and day 240.', 'Mark day one hundred twenty, and day two hundred forty.'),
                 P('An independent agent can show private options next to VGLI, so you can compare.',
                   'An independent agent can show private options next to V G L I, so you can compare.')]),
        K.end_scene(),
    ])
