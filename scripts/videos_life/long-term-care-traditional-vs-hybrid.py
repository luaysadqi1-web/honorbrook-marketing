"""Long-term care insurance: traditional or hybrid?
For /blog/traditional-vs-hybrid-long-term-care-insurance-which-fits and /long-term-care-insurance.
Facts only from those two built pages (staging/site-onyx, read Nov 27, 2026). The pages link no outside primary source,
so nothing about Medicare or health insurance is stated here. No prices, no company names.
"""
import video_life as K
P = K.P

BLOG = 'https://honorbrook-insurance.com/blog/traditional-vs-hybrid-long-term-care-insurance-which-fits'
PAGE = 'https://honorbrook-insurance.com/long-term-care-insurance'
D_BLOG = 'page dated September 2026; read Nov 27, 2026'
D_PAGE = 'page updated September 2026; read Nov 27, 2026'

VIDEO = dict(
    title='Long-term care insurance: traditional or hybrid?',
    description=('Traditional long-term care insurance is pure care coverage. A hybrid pairs care benefits with life insurance or an annuity. '
                 'Here is how the two types differ on premiums, on what happens if you do not need care, and the questions to ask.'),
    poster=4.6,
    sources=[
        dict(fact='Long-term care is help with activities of daily living, such as bathing, dressing and eating. '
                  'It can happen at home, in assisted living or in a nursing facility.', url=PAGE, date=D_PAGE),
        dict(fact="A traditional policy is pure long-term care coverage. If you meet the policy's benefit triggers, it pays toward covered care.",
             url=BLOG, date=D_BLOG),
        dict(fact='Traditional premiums are not guaranteed (premiums can rise). Insurers can request rate increases for a group of policyholders, subject to state approval. '
                  'If you do not need care, the premiums paid generally are not returned.', url=BLOG, date=D_BLOG),
        dict(fact='Traditional policies generally buy more care coverage per premium dollar.', url=BLOG, date=D_BLOG),
        dict(fact='A hybrid combines long-term care benefits with a life insurance policy or annuity. If care is not needed, '
                  'some or all of the value passes to beneficiaries as a death benefit.', url=BLOG, date=D_BLOG),
        dict(fact='Hybrid premiums are often guaranteed; hybrids have a higher upfront cost (often a larger lump sum or larger payments over a shorter period).',
             url=BLOG, date=D_BLOG),
        dict(fact='Questions that decide it: How important is premium certainty? Is maximum care coverage the priority? Does leaving something to heirs matter?',
             url=BLOG, date=D_BLOG),
        dict(fact='Benefits, benefit triggers, underwriting and premium guarantees vary by state, carrier and individual circumstances (page disclaimer). '
                  "Guarantees depend on the insurer's claims-paying ability (standard caveat required for this video).",
             url=BLOG, date=D_BLOG),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Long-term care insurance', ['Traditional', 'or hybrid?'], sub='How the two types differ', icon='scale'),
                [P('Long-term care insurance: traditional or hybrid?'),
                 P('Here is how the two types differ.')], pre=0.1, post=0.6),
        # 2. What long-term care is
        K.scene(K.fact_card('Long-term care', 'Help with daily living',
                            ['Such as bathing, dressing or eating', 'At home, in assisted living or in a nursing facility'], start=0),
                [P('Long-term care is help with daily living, such as bathing, dressing or eating.'),
                 P('It can happen at home, in assisted living or in a nursing facility.')]),
        # 3. Traditional
        K.scene(K.fact_card('Traditional', 'Pure care coverage',
                            ['Pays toward covered care', "If you meet the policy's benefit triggers"], start=1, at=[1, 1]),
                [P('A traditional policy is pure long-term care coverage.'),
                 P("It pays toward covered care if you meet the policy's benefit triggers.")]),
        # 4. Hybrid
        K.scene(K.fact_card('Hybrid', 'Care plus life insurance',
                            ['Or care benefits with an annuity'], start=0),
                [P('A hybrid combines care benefits with life insurance or an annuity.')]),
        # 5. Side by side (centerpiece)
        K.scene(K.two_column('Side by side', 'Traditional or hybrid',
                             ('Traditional', ['Premiums can rise', 'Generally nothing returned if care is not needed',
                                              'Generally more care coverage per premium dollar']),
                             ('Hybrid', ['Premiums are often guaranteed', 'A death benefit if care is not needed',
                                         'A higher upfront cost']),
                             left_at=[0, 1, 2], right_at=[3, 4, 5]),
                [P('Traditional: premiums can rise.'),
                 P('Generally nothing returned if care is not needed.'),
                 P('Generally more care coverage per premium dollar.'),
                 P('Hybrid: premiums are often guaranteed.'),
                 P('A death benefit if care is not needed.'),
                 P('And a higher upfront cost.')]),
        # 6. Questions to ask
        K.scene(K.checklist('Questions to ask', 'What matters to you?',
                            ['How important is premium certainty?', 'Is maximum care coverage the priority?',
                             'Does leaving something to heirs matter?'],
                            start=0, mark_kind=None, icons=['lock', 'shield', 'people']),
                [P('How important is premium certainty?'),
                 P('Is maximum care coverage the priority?'),
                 P('Does leaving something to heirs matter?')]),
        # 7. Caveats
        K.scene(K.checklist('Keep in mind', 'Read the policy',
                            ['Benefits and eligibility depend on the policy', 'Traditional premiums are not guaranteed',
                             "Guarantees depend on the insurer's claims-paying ability"],
                            start=0, mark_kind=None, icons=['doc', 'arrow', 'shield']),
                [P('Benefits and eligibility depend on the policy.'),
                 P('Traditional premiums are not guaranteed.'),
                 P("Guarantees depend on the insurer's claims-paying ability.")]),
        K.end_scene(),
    ])
