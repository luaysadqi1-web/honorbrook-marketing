import importlib.util,os
def _imp(n):
    sp=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),n+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
_m=_imp('posts_1'); cta=_m.cta; REL_M=_m.REL_M
POSTS=[
dict(slug="new-to-medicare-checklist-virginia-and-10-more-states",kind="med",
title="New to Medicare? Your Checklist, With Free Local Help in Each of Our 11 States",ttl="New to Medicare? Checklist for VA, MD, NC, SC, GA, AL, LA, TX, MI, IN, WV",short="New to Medicare Checklist",em="Checklist",
desc="New to Medicare or just moved to a new state? Follow this step-by-step checklist and find the free counseling program in VA, MD, NC, SC, GA, AL, LA, TX, MI, IN and WV.",
lead="Whether you just turned 65 or just moved, here is what to do, in what order, and where to get free local help.",
faqh="New to Medicare FAQ",
faqs=[("When should I sign up for Medicare if I am turning 65?","Your Initial Enrollment Period lasts seven months: the three months before your birthday month, your birthday month, and the three months after. Enrolling early helps your coverage start on time, and delaying without other qualifying coverage can lead to lifetime late penalties."),
("What if I am already on Medicare and move to a different state?","Moving to a new service area generally gives you a Special Enrollment Period to change your Medicare Advantage or Part D plan, because plans are tied to where you live. Original Medicare works nationwide, but a Medigap plan may need to be reviewed, and rules vary by state."),
("Is help available for free?","Yes. Every state has a State Health Insurance Assistance Program (SHIP) offering free, unbiased Medicare counseling, and independent agents like Honorbrook also help at no cost to you because carriers pay us, not you.")],
rel=REL_M,
body=f"""
Medicare is simple to describe and surprisingly hard to navigate the first time. There are deadlines, penalties for missing them, and several plan types that can look similar on paper. Add a move to a new state and the questions multiply. This checklist walks you through the steps in order, and includes the free counseling program for each state we serve. It is general information, not advice for your specific situation.

## Step 1: Find your enrollment window
Most people become eligible at 65. Your Initial Enrollment Period (IEP) is seven months long:
- The three months before your birthday month.
- Your birthday month.
- The three months after.

If you are already receiving Social Security benefits, you are usually enrolled in Parts A and B automatically around your 65th birthday. If not, you generally need to sign up yourself. People who qualify earlier because of a disability have different timing. Check your card and notices, and do not assume you are enrolled.

!callout **Still working at 65?** Whether you can delay Part B without a penalty depends on your employer's size and the type of coverage. Ask your benefits office before you decide. Our [Turning 65 guide](/turning-65) covers the common situations.

## Step 2: Understand the four parts
- **Part A** is hospital coverage, and most people pay no premium for it.
- **Part B** is medical coverage for doctors and outpatient care, with a monthly premium and cost-sharing.
- **Part C (Medicare Advantage)** is a private plan alternative that bundles A, B, and usually D.
- **Part D** is prescription drug coverage.

Our guide to [Medicare Parts A, B, C and D](/blog/medicare-parts-a-b-c-d-explained) explains each in plain English.

## Step 3: Choose your path
Most new enrollees pick one of two routes:
1. **Original Medicare + a Medigap plan + a Part D drug plan.** Higher monthly premiums, broad doctor choice, and predictable costs.
2. **A Medicare Advantage plan.** Often low premiums with extras like dental and vision, but with networks and copays.

Neither is automatically better. See [Advantage vs. Medigap](/blog/medicare-advantage-vs-medigap-2026). If you choose Medigap, your best chance for guaranteed acceptance is the six-month Medigap Open Enrollment Period that starts when you are 65 or older and enrolled in Part B.

## Step 4: Check your doctors and drugs before you enroll
Make a list of every doctor, hospital, pharmacy, and medication, with dosages. Check each against any plan you are considering. This single step prevents the most common new-enrollee regret.

{cta()}

## Step 5: Know the penalties and deadlines
Missing windows can be costly. Late enrollment penalties can apply to Part B and Part D and may last as long as you have the coverage. Medicare Advantage and Part D plans also have an Annual Enrollment Period each fall, from October 15 to December 7. Mark your calendar.

## Step 6: If you are moving to a new state
Original Medicare works across the country, but plans tied to a service area do not. If you move out of your plan's area, you generally have a Special Enrollment Period to choose a new Medicare Advantage or Part D plan. Medigap policies follow different rules, so check before you cancel anything, because insurers in many states can ask health questions when you apply for a new one. Read [when you can switch plans](/blog/when-can-you-switch-medicare-plans) for the windows.

## Free local help in each state we serve
Every state runs a State Health Insurance Assistance Program (SHIP) that offers free, unbiased Medicare counseling. These are the programs in the states Honorbrook serves:

| State | Free counseling program |
|---|---|
| Virginia | VICAP (Virginia Insurance Counseling and Assistance Program) |
| Maryland | Maryland SHIP |
| North Carolina | SHIIP (Seniors' Health Insurance Information Program) |
| South Carolina | I-CARE (Insurance Counseling Assistance and Referrals for Elders) |
| Georgia | GeorgiaCares |
| Alabama | Alabama SHIP |
| Louisiana | Louisiana SHIP |
| Texas | HICAP (Health Information, Counseling and Advocacy Program) |
| Michigan | MMAP (Michigan Medicare/Medicaid Assistance Program) |
| Indiana | Indiana SHIP |
| West Virginia | West Virginia SHIP |

Program names and contact details can change, so confirm through Medicare.gov or 1-800-MEDICARE. These programs are a good place to learn the basics. For help comparing the specific plans offered in your county, our state pages explain how we work: [Virginia](/virginia-medicare-insurance), [Maryland](/maryland-medicare-insurance), [North Carolina](/north-carolina-medicare-insurance), [South Carolina](/south-carolina-medicare-insurance), [Georgia](/georgia-medicare-insurance), [Alabama](/alabama-medicare-insurance), [Louisiana](/louisiana-medicare-insurance), [Texas](/texas-medicare-insurance), [Michigan](/michigan-medicare-insurance), [Indiana](/indiana-medicare-insurance) and [West Virginia](/west-virginia-medicare-insurance).

## Your one-page checklist
1. Write down your birthday and your enrollment window dates.
2. Confirm whether you are automatically enrolled in Parts A and B.
3. Decide whether to delay Part B based on your employer coverage.
4. List your doctors, hospitals, pharmacies, and medications.
5. Compare Original Medicare plus Medigap against Medicare Advantage in your county.
6. Add Part D if you choose Original Medicare.
7. Enroll before your window ends and keep confirmation records.
8. Set a reminder for October 15 each year to review your plan.

## How Honorbrook helps
We are an independent agency licensed in 11 states, appointed with many carriers, so we compare real plans at your address instead of promoting one company. Our help is free to you because carriers pay us, and by law your premium is the same whether you use an agent or enroll alone. Everything can be handled by phone, which is especially helpful if you are moving or live far from our Tysons, Virginia office.
"""),
]
