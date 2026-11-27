"""VALife: the basics for veterans with a service-connected disability (for /veterans-life-insurance).
Facts only from the built page staging/site-onyx/veterans-life-insurance.html and scripts/onyx/data/patches/veterans.json,
each re-read on va.gov (VALife page, last updated October 13, 2026) on Nov 26, 2026. No premiums. Does not repeat the VGLI video.
"""
import video_life as K
P = K.P

VALIFE = 'https://www.va.gov/life-insurance/options-eligibility/valife/'
DATE = 'last updated Oct 13, 2026; checked Nov 26, 2026'
SRC = 'Source: va.gov, VALife (updated Oct 13, 2026; checked November 2026)'

VIDEO = dict(
    title='VALife: the basics for veterans with a service-connected disability',
    description=('VALife is whole life insurance from the VA for veterans with a service-connected disability rating. '
                 'Who can apply, how much coverage it offers, and when full coverage starts, with each fact from va.gov.'),
    poster=6.6,
    sources=[
        dict(fact='At age 80 or younger you are eligible for VALife with a VA service-connected disability rating, even a 0% rating.',
             url=VALIFE, date=DATE),
        dict(fact='There is no time limit to apply after getting your disability rating.', url=VALIFE, date=DATE),
        dict(fact='VALife offers up to $40,000 in whole life insurance coverage, in $10,000 increments.', url=VALIFE, date=DATE),
        dict(fact='You do not need to prove you are in good health.', url=VALIFE, date=DATE),
        dict(fact='Full coverage starts 2 years after you apply. If death happens during the 2-year wait, '
                  'VA pays the beneficiaries the premiums paid, plus interest.', url=VALIFE, date=DATE),
        dict(fact='Honorbrook is an independent agency, not part of the VA, and can show private options next to VALife.',
             url='https://honorbrook-insurance.com/veterans-life-insurance', date='page text, checked Nov 26, 2026'),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Life insurance', ['VALife: the basics', 'for veterans'], sub='With a service-connected disability', icon='shield'),
                [P('VALife: the basics for veterans with a service-connected disability.',
                   'V A Life: the basics, for veterans with a service-connected disability.'),
                 P('Who can apply, how much, and when coverage starts.')],
                pre=0.1, post=0.6),
        # 2. Who we are
        K.scene(K.fact_card('Who we are', 'Independent agency',
                            ['VA program facts here come from va.gov.', 'Checked November 2026.'],
                            head=['Not affiliated', 'with the VA'], at=[1, 1]),
                [P('Honorbrook is an independent agency, not affiliated with the VA.',
                   'Honorbrook is an independent agency, not affiliated with the V A.'),
                 P('VA facts here come from va.gov, checked November 2026.',
                   'V A facts here come from V A dot gov, checked November twenty twenty six.')]),
        # 3. Who can apply
        K.scene(K.fact_card('Who can apply', 'Age 80 or younger',
                            ['With a VA service-connected disability rating', 'Even a 0% rating'],
                            source=SRC, at=[2, 3]),
                [P('VALife is whole life insurance from the VA.', 'V A Life is whole life insurance from the V A.'),
                 P('You can apply at age 80 or younger,', 'You can apply at age eighty or younger,'),
                 P('with a service-connected disability rating.'),
                 P('Even a 0% rating.', 'Even a zero percent rating.')]),
        # 4. How much
        K.scene(K.fact_card('How much', 'Up to $40,000',
                            ['Whole life coverage', 'In $10,000 steps'], source=SRC),
                [P('VALife offers up to $40,000 of whole life coverage,',
                   'V A Life offers up to forty thousand dollars of whole life coverage,'),
                 P('in $10,000 steps.', 'in ten thousand dollar steps.')]),
        # 5. Health and timing to apply
        K.scene(K.checklist('Applying', 'Two things to know',
                            ['No need to prove good health', 'No time limit to apply after your rating'],
                            start=0, icons=['doc', 'calendar'], note=SRC),
                [P('You do not need to prove good health.'),
                 P('And there is no time limit to apply after you get your rating.')]),
        # 6. The 2-year wait
        K.scene(K.timeline('When it starts', 'The 2-year wait',
                           [('Apply', 'The 2-year wait begins'),
                            ('2 years', 'Full coverage starts')],
                           at=[0, 0], note='If death happens during the wait: premiums paid, plus interest. Source: va.gov, checked November 2026'),
                [P('Full coverage starts 2 years after you apply.', 'Full coverage starts two years after you apply.'),
                 P('If death happens during that wait, your beneficiaries get the premiums paid, plus interest.')]),
        # 7. Compare
        K.scene(K.checklist('Compare', 'See them side by side',
                            ['VALife from the VA', 'Private options next to VALife'],
                            start=0, mark_kind=None, icons=['shield', 'scale']),
                [P('Want to see how VALife fits?', 'Want to see how V A Life fits?'),
                 P('An independent agent can show private options next to VALife, so you can compare.',
                   'An independent agent can show private options next to V A Life, so you can compare.')]),
        K.end_scene(),
    ])
