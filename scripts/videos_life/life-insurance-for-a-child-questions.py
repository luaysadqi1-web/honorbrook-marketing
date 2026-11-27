"""Life insurance for a child: four questions before you buy.
For /blog/should-i-buy-life-insurance-for-my-child-gerber-style-whole-life.html.
Facts only from the built page text of that blog post and of /childrens-life-insurance (read 2026-11-26).
No company names, no prices. Does not repeat the child policy vs. child rider comparison (another video covers it).
"""
import video_life as K
P = K.P

BLOG = 'https://honorbrook-insurance.com/blog/should-i-buy-life-insurance-for-my-child-gerber-style-whole-life'
CHILD = 'https://honorbrook-insurance.com/childrens-life-insurance'
BLOG_D = 'page dated October 2026; page text read 2026-11-26'
CHILD_D = 'page updated November 2026; page text read 2026-11-26'

VIDEO = dict(
    title='Life insurance for a child: four questions before you buy',
    description=('Four questions for parents and grandparents before buying life insurance on a child: is the parents\' own coverage '
                 'in place, who owns and pays, can the child buy more coverage later, and what the cash value is and is not.'),
    poster=5.2,
    sources=[
        dict(fact='Parents should have their own coverage in place first. A child depends on your income far more than you depend on a policy on the child.',
             url=CHILD, date=CHILD_D),
        dict(fact='A parent or grandparent buys the policy on a child or grandchild. Premiums are paid for many years. '
                  'Ownership can usually be transferred to the child as an adult; ask how and when ownership transfers.',
             url=BLOG, date=BLOG_D + ' (also ' + CHILD + ', ' + CHILD_D + ')'),
        dict(fact='Many policies include the right to buy more coverage at set ages without health questions. Ask whether the policy includes it and what it costs. Terms vary, so check the policy.',
             url=CHILD, date=CHILD_D + ' (question list: ' + BLOG + ')'),
        dict(fact='Cash value builds slowly and is small in the early years; the owner can borrow against it. Policy loans can reduce the cash value and the death benefit.',
             url=CHILD, date=CHILD_D),
        dict(fact='A child\'s whole life policy is life insurance. It is not a college savings plan, and its cash value is not a savings account. If saving for education is the goal, compare dedicated options too.',
             url=CHILD, date=CHILD_D + ' (also ' + BLOG + ')'),
        dict(fact='We do not suggest that life insurance is better or worse than a 529 plan; each has different purposes, costs and tax treatment.',
             url=BLOG, date=BLOG_D),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Life insurance for a child', ['Four questions', 'before you buy'], sub='For parents and grandparents', icon='people'),
                [P('Life insurance for a child: 4 questions before you buy.',
                   'Life insurance for a child: four questions before you buy.'),
                 P('For parents and grandparents.')], pre=0.1, post=0.5),
        # 2. Question 1
        K.scene(K.fact_card('Question 1', 'Parents first',
                            ['A child depends on your income', 'Have your own coverage in place first'],
                            head='Are the parents covered?'),
                [P('Question 1. Are the parents covered?', 'Question one. Are the parents covered?'),
                 P('A child depends on your income.'),
                 P('So parents should have their own coverage in place first.')], post=0.5),
        # 3. Question 2
        K.scene(K.checklist('Question 2', 'Who owns it, and who pays?',
                            ['A parent or grandparent buys it', 'Premiums are paid for many years',
                             'Ask how ownership transfers later'],
                            start=1, mark_kind=None, icons=['person', 'calendar', 'doc']),
                [P('Question 2. Who owns the policy, and who pays?', 'Question two. Who owns the policy, and who pays?'),
                 P('A parent or grandparent buys it.'),
                 P('Premiums are paid for many years.'),
                 P('Ask how ownership transfers when the child is an adult.')], post=0.5),
        # 4. Question 3
        K.scene(K.fact_card('Question 3', 'More coverage later?',
                            ['Many policies include the right to buy more', 'At set ages, without health questions',
                             'Ask if it is included, and what it costs'],
                            source='Terms vary, so check the policy.', at=[1, 1, 2]),
                [P('Question 3. Can the child buy more coverage later?', 'Question three. Can the child buy more coverage later?'),
                 P('Many policies include the right to buy more at set ages, without health questions.'),
                 P('Ask if the policy includes it, and what it costs.')], post=0.5),
        # 5. Question 4
        K.scene(K.two_column('Question 4', 'What is the cash value?',
                             ('It is', ['Part of a whole life policy', 'Slow to build, small early on', 'Something the owner can borrow against']),
                             ('It is not', ['A college savings plan', 'A savings account']),
                             left_at=[0, 1, 2], right_at=[3, 3],
                             note='Policy loans can reduce the cash value and the death benefit.'),
                [P('Question 4. What is the cash value, and what is it not?', 'Question four. What is the cash value, and what is it not?'),
                 P('It builds slowly, and it is small in the early years.'),
                 P('The owner can borrow against it.'),
                 P('It is not a college savings plan or a savings account.')], post=0.5),
        # 6. Saving for education
        K.scene(K.fact_card('Saving for education', 'Compare both',
                            ['We do not say it is better or worse than a 529 plan', 'Different purposes, costs and tax treatment'],
                            start=1),
                [P('Saving for education? Compare dedicated options too.'),
                 P('We do not say life insurance is better or worse than a 529 plan.',
                   'We do not say life insurance is better or worse than a five twenty nine plan.'),
                 P('Each has different purposes, costs and tax treatment.')]),
        K.end_scene(),
    ])
