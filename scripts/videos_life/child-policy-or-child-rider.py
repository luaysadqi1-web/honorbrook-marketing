"""Children's life insurance: a child policy or a child rider? For /childrens-life-insurance.
Facts come only from the built page staging/site-onyx/childrens-life-insurance.html (dateModified 2026-11-24,
after the kids-pr3 edits). No prices, no company names."""
import video_life as K
P = K.P

URL = 'https://honorbrook-insurance.com/childrens-life-insurance'
DATE = 'Updated November 2026 (dateModified 2026-11-24)'

VIDEO = dict(
    title="Children's life insurance: a child policy or a child rider?",
    description=("Two ways to cover a child: a small whole life policy on the child, or a child rider on a parent's term policy. "
                 "A plain side-by-side look for parents and grandparents."),
    poster=3.0,
    sources=[
        dict(fact="Children's life insurance is usually a small whole life policy that a parent or grandparent buys on a child or grandchild; the child can keep it as an adult.", url=URL, date=DATE),
        dict(fact='Locks in insurability: as long as premiums are paid, coverage stays in force even if health conditions appear later.', url=URL, date=DATE),
        dict(fact='Whole life builds cash value slowly; in the early years it is small.', url=URL, date=DATE),
        dict(fact="A child rider on a parent's term policy covers all your children and usually can be converted to the child's own permanent policy later.", url=URL, date=DATE),
        dict(fact='Product availability, benefits, riders, ownership rules and eligibility vary by state, carrier and individual circumstances (page disclaimer).', url=URL, date=DATE),
        dict(fact='For families whose goal is simply protection during childhood, a rider is often enough.', url=URL, date=DATE),
        dict(fact='Parents should have their own coverage in place first. A child depends on your income far more than you depend on a policy on the child.', url=URL, date=DATE),
        dict(fact="A child's whole life policy is life insurance, not a college savings plan; cash value grows slowly in the first decade; if saving for education is the goal, compare dedicated options too.", url=URL, date=DATE),
    ],
    scenes=[
        K.scene(K.hook("Children's life insurance", ['A child policy', 'or a child rider?'], sub='Two ways to cover a child', icon='people'),
                [P("Two ways to cover a child with life insurance, side by side.")], pre=0.1, post=0.6),
        K.scene(K.checklist('Way 1', 'A policy on the child',
                            ['Usually a small whole life policy', 'Bought by a parent or grandparent', 'The child can keep it as an adult'],
                            start=0, icons=['1', 'people', 'person']),
                [P("The first way is usually a small whole life policy on the child."),
                 P("A parent or grandparent buys it."),
                 P("The child can keep it as an adult.")]),
        K.scene(K.checklist('What it does', 'What a child policy does',
                            ['Locks in insurability', 'Stays in force while premiums are paid', 'Builds cash value slowly'],
                            at=[0, 1, 3], icons=['lock', 'shield', 'clock']),
                [P("It locks in insurability."),
                 P("Coverage stays in force while premiums are paid,"),
                 P("even if health conditions appear later."),
                 P("It builds cash value slowly.")],
                ),
        K.scene(K.checklist('Way 2', "A rider on a parent's policy",
                            ["Can be added to a parent's term policy", 'One rider covers all your children', 'Can usually be converted later'],
                            at=[0, 1, 2], icons=['2', 'doc', 'arrow'],
                            note='Riders and rules vary by state and carrier.'),
                [P("The second way is a child rider on a parent's term policy."),
                 P("If you buy term life, you may be able to add one for all your children."),
                 P("It usually can be converted to the child's own policy later.")],
                ),
        K.scene(K.two_column('Side by side', 'Policy or rider?',
                             ('Child policy', ['Permanent whole life', 'The child can keep it', 'Cash value builds slowly']),
                             ('Child rider', ["Part of a parent's term policy", 'Protection during childhood', 'Often enough for that goal']),
                             left_mark='check', right_mark='check'),
                [P("A child policy is permanent. The child can keep it."),
                 P("A rider is often enough when the goal is simply protection during childhood.")]),
        K.scene(K.fact_card('Parents first', 'Cover yourself first',
                            ['A child depends on your income', 'Your own coverage comes first'], start=0),
                [P("A child depends on your income far more than you depend on a policy on the child."),
                 P("So parents should have their own coverage in place first.")]),
        K.scene(K.fact_card('College savings', 'Insurance, not savings',
                            ['Not a college savings plan', 'Cash value grows slowly at first', 'Saving for school? Compare options too'], start=0),
                [P("A child's whole life policy is not a college savings plan."),
                 P("Its cash value grows slowly in the first decade."),
                 P("If saving for education is the goal, compare dedicated options too.")]),
        K.end_scene(),
    ])
