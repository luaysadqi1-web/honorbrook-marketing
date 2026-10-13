import importlib.util,os
def _imp(n):
    sp=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),n+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
_m=_imp('posts_1'); cta=_m.cta; REL_M=_m.REL_M
NATL=[
dict(slug="medicare-advantage-open-enrollment-period-january-to-march",kind="med",
title="Medicare Advantage Open Enrollment (Jan 1 – Mar 31): Can I Switch Plans?",ttl="Medicare Advantage Open Enrollment, Jan 1 – Mar 31",short="Medicare Advantage Open Enrollment",em="Switch Plans",
desc="Missed AEP? The Medicare Advantage Open Enrollment Period (Jan 1 – Mar 31) lets you switch once. See who qualifies, what you can change, and what you can't.",
lead="If you are in a Medicare Advantage plan and January brought surprises, you get one more chance to fix it.",
faqh="Medicare Advantage Open Enrollment FAQ",
faqs=[("When is the Medicare Advantage Open Enrollment Period?","It runs from January 1 through March 31 each year for people already enrolled in a Medicare Advantage plan."),
("Can I switch from Original Medicare to Medicare Advantage during this period?","No. The Medicare Advantage Open Enrollment Period is for people who are already in a Medicare Advantage plan. It generally does not let you move from Original Medicare into Advantage."),
("How many changes can I make?","One. You can switch to another Medicare Advantage plan or drop your plan and return to Original Medicare, and you can add a stand-alone Part D plan if you return to Original Medicare.")],
rel=REL_M,
body=f"""
Many people find out in January that something changed: a doctor left the network, a drug moved to a higher tier, or the copays are not what they expected. If you are in a Medicare Advantage plan, you may not be stuck for the year. The Medicare Advantage Open Enrollment Period, often called MA-OEP, gives you one more chance to make a change. Here is exactly how it works.

## The short answer
If you are already enrolled in a [Medicare Advantage plan](/medicare-advantage), you can make one change between January 1 and March 31. That is true in every state. You can switch to a different Advantage plan, or drop your plan and return to Original Medicare.

## Who qualifies
- People enrolled in a Medicare Advantage plan (including HMO, PPO, and most special needs plans, subject to their own rules).
- It applies to people who joined the plan during AEP or earlier.

## Who does not
- People on Original Medicare who want to move into Medicare Advantage. This window does not let you do that.
- People who want to change a stand-alone Part D plan, unless they are in an Advantage plan and dropping back to Original Medicare.
- Anyone who already used a change during the window.

!callout **One change only.** Make sure the new plan covers your doctors and drugs before you switch, because you generally cannot undo the change during the same window.

## What you can do during MA-OEP
1. **Switch to a different Medicare Advantage plan.** If you want drug coverage, choose a plan that includes it.
2. **Drop your Advantage plan and return to Original Medicare.** You can add a stand-alone [Part D plan](/medicare-part-d) at the same time if you want drug coverage.

## When changes take effect
Changes made during the window generally take effect the first day of the month after the plan receives your request. Keep your old coverage until the new coverage is confirmed.

## The Medigap catch if you return to Original Medicare
If you leave Advantage for Original Medicare, you may want a [Medigap plan](/medicare-supplement-medigap). Outside certain protected situations, insurers in many states can ask health questions and may decline or charge more. Read [when you can change your Medigap plan](/blog/when-can-i-change-my-medigap-plan-birthday-rule-and-underwriting) before you cancel anything.

{cta()}

## How to decide if it is worth switching
- Is your doctor still in network? Check the plan's directory by name.
- Is each of your drugs covered, and at what tier?
- Did the copays or the out-of-pocket maximum change?
- Is the problem fixable by switching to a different Advantage plan, or do you really want Original Medicare?
- Do you travel or spend part of the year in another state?

If the answer to most of these is "it is fine," do nothing. Switching only helps if the new plan fits better.

## Compare with other windows
- **Annual Enrollment Period (Oct 15 – Dec 7):** you can change almost any plan type for the following January 1.
- **Special Enrollment Periods:** triggered by events like moving, losing coverage, or your plan ending.
- **Initial Enrollment Period:** around your 65th birthday.

See [when you can switch plans](/blog/when-can-you-switch-medicare-plans) for the full list.

## A short checklist for January and February
1. Review your plan documents and recent bills.
2. List doctors, hospitals, and medications.
3. Check them against two or three alternatives.
4. Confirm the effective date and how you will get your new card.
5. Do not cancel anything until the new plan confirms your enrollment.

## How we help
We are an independent agency, so we compare Advantage plans and Original Medicare options across carriers and check your doctors and drugs first. Our help is free because carriers pay us, and your premium is the same either way.
"""),
dict(slug="when-can-i-change-my-medigap-plan-birthday-rule-and-underwriting",kind="med",
title="When Can I Change My Medigap Plan? Birthday Rules, Guaranteed Issue and Underwriting",ttl="When Can I Change My Medigap Plan?",short="Change Your Medigap Plan",em="Medigap",
desc="Medigap has no annual switching deadline, but you may face health questions. Learn guaranteed-issue rights, birthday rules and how to switch safely.",
lead="There is no October deadline for Medigap, but there is something else to know first: underwriting.",
faqh="Changing Medigap FAQ",
faqs=[("Is there an open enrollment period for Medigap?","There is a six-month Medigap Open Enrollment Period that starts when you are 65 or older and enrolled in Part B. Outside it, and outside certain guaranteed-issue situations, an insurer in many states can ask health questions."),
("What is the Medigap birthday rule?","Some states give people a short window each year around their birthday to switch to another Medigap plan, often with equal or lesser benefits, without health questions. Which states have it, and the details, vary and have been changing."),
("Can I keep my Medigap plan if I change Part D plans?","Yes. Medigap and Part D are separate. Changing your Part D plan does not affect your Medigap policy.")],
rel=REL_M,
body=f"""
People are often surprised to learn that [Medicare Supplement (Medigap)](/medicare-supplement-medigap) does not work like Medicare Advantage or Part D. There is no annual enrollment deadline. You can generally apply for a new Medigap plan any time of year. The catch is that, outside protected situations, the insurer may be allowed to ask about your health and can decline you or charge more. This guide explains the rules.

## The basics: Medigap is year-round, but not guaranteed
Medigap policies are sold by private insurers and standardized by plan letter. You can apply to change carriers or plans at any time. Whether you will be accepted at the best rate depends on which protections apply to you.

## Protection 1: your Medigap Open Enrollment Period
This is a one-time, six-month window that begins when you are 65 or older and enrolled in Medicare Part B. During it, insurers generally cannot deny you coverage or charge more because of your health. After it ends, you are usually subject to underwriting unless another protection applies.

## Protection 2: federal guaranteed-issue rights
Federal law gives guaranteed access to certain Medigap plans in specific situations, typically with a 63-day window. Examples include:
- Your Medicare Advantage plan leaves your area or stops operating.
- You move out of your plan's service area.
- You joined Medicare Advantage when you first became eligible and leave within a trial period, generally the first year.
- Your employer or union coverage that supplemented Medicare ends.
- Your Medigap insurer goes bankrupt or ends your coverage through no fault of your own.

Timing and details matter, so check your situation before you cancel any coverage.

## Protection 3: state rules and birthday rules
Some states offer additional protections. A few give a short yearly window around your birthday during which you may switch to another Medigap plan, often of equal or lesser benefits, without health questions. Details differ by state: how long the window lasts, which plans you can move to, and whether you can change insurers or only stay with your current insurer or its affiliates. These rules have been changing, so confirm the current rule with your state's Department of Insurance. See our state guides, for example [Virginia](/blog/when-can-i-change-my-medicare-plan-in-virginia) and [Maryland](/blog/when-can-i-change-my-medicare-plan-in-maryland).

!callout **Never cancel before you are approved.** Apply for the new plan first, wait for approval in writing, and only then end your old plan, so you do not end up without coverage.

{cta()}

## Why people change Medigap plans
- **A lower premium.** Medigap premiums for the same plan letter can differ a lot between carriers, and increases over time vary.
- **Better service** or a different rating method.
- **Changing needs,** such as moving from a richer plan to one with more cost-sharing.
- **A move** to a new state or area.

## What underwriting looks like
When underwriting applies, the insurer may ask about your medical history, medications, and recent treatments. They can accept you, decline you, or in some cases offer a higher rate. Answer honestly because incorrect answers can cause problems later.

## The Advantage-to-Medigap situation
If you are leaving a Medicare Advantage plan and want Medigap, check your protections first. Outside the trial period and other protected situations, insurers in many states can underwrite. See [Medicare Advantage Open Enrollment](/blog/medicare-advantage-open-enrollment-period-january-to-march) and [switching from Advantage back to Original Medicare](/blog/switch-from-medicare-advantage-back-to-original-medicare).

## Rating methods affect your future premium
Medigap premiums are priced in different ways: community-rated, issue-age, or attained-age. A plan that looks cheap at the start may become more expensive over time under attained-age pricing. When comparing, ask how the rate is determined and how the carrier has handled increases.

## How to switch safely
1. Compare plans of the same letter across carriers at your ZIP code.
2. Check whether you have a guaranteed-issue right or a state birthday window.
3. If underwriting applies, apply before you cancel and wait for approval.
4. Confirm the effective date so there is no gap.
5. Keep your confirmation letters.

## How we help
We are an independent agency and we compare Medigap plans from multiple carriers. We will tell you honestly whether you have a protected window or whether underwriting applies. Our help is free because carriers pay us and your premium is the same either way.
"""),
]
S={
'virginia':dict(n='Virginia',dept='the Virginia Bureau of Insurance',ship='VICAP (Virginia Insurance Counseling and Assistance Program)',metros='Northern Virginia, Richmond, Hampton Roads, Roanoke and the Shenandoah Valley',
 med="Virginia is one of the states reported in 2026 to have a Medigap birthday-style rule. One 2026 source describes it as taking effect in July 2025 and allowing a switch to the same Medigap plan with a different insurer, but the window length is not clearly stated across sources. Because the details have been changing, confirm the current rule with the Virginia Bureau of Insurance, and do not cancel your current plan until a new one is approved.",
 loc="Virginia's plan choices can look very different from Northern Virginia, where there are many providers and health systems, to the rural Southwest and Southside, where networks can be narrower. If you live near the D.C. area you may use providers across state lines, so check whether your doctors in Maryland or D.C. are in network. Plan availability varies by county and independent city in Virginia, so always compare options at your exact address.",
 slug='virginia',x='- **"I live in Northern Virginia but see doctors in D.C. or Maryland."** Confirm those providers are in the network of the plan you pick, because networks do not always cross state lines.'),
'maryland':dict(n='Maryland',dept='the Maryland Insurance Administration',ship='Maryland SHIP (State Health Insurance Assistance Program)',metros='Baltimore, Montgomery and Prince George\'s counties, Howard County, Annapolis and the Eastern Shore',
 med="Maryland is reported in 2026 sources as having a Medigap birthday rule. Reports describe a short window of about 30 days following your birthday to switch to a plan with equal or lesser benefits without health questions, though sources differ by a day or so and do not agree on which insurers you may choose. Confirm the current window and carrier rules with the Maryland Insurance Administration before relying on it, and note that missing the window generally returns you to underwriting.",
 loc="Maryland residents often receive care in several places, such as Baltimore, the D.C. suburbs, or across the Delaware and Virginia lines, so network coverage matters. People near the Eastern Shore and western Maryland can have fewer in-network options than those in the central corridor. Plan availability varies by county, so compare options at your address and confirm that the hospitals you actually use are included.",
 slug='maryland',x='- **"I commute across the Maryland line."** If your doctors are in D.C. or Virginia, confirm they are in network before you switch.'),
'north-carolina':dict(n='North Carolina',dept='the North Carolina Department of Insurance',ship='SHIIP (Seniors\' Health Insurance Information Program)',metros='Charlotte, the Triangle (Raleigh, Durham, Chapel Hill), Greensboro, Asheville and the coast',
 med="In the recent 2026 sources we reviewed, North Carolina was not listed as having a Medigap birthday rule. That generally means that outside your Medigap Open Enrollment Period and the federal guaranteed-issue situations, an insurer may ask health questions when you apply for a different plan. State rules can change, so confirm with the North Carolina Department of Insurance before you decide, and do not cancel your current plan until a new one is approved.",
 loc="North Carolina has large metro areas and many smaller communities, from the Triangle and Charlotte to the mountains and the coast, and networks vary widely between them. Retirees who split time between the coast and the mountains or move between counties should check whether plan networks extend to both. Plan availability varies by county, so compare options at the address where you actually live.",
 slug='north-carolina',x='- **"I live part of the year on the coast or in the mountains."** Ask how the plan covers care away from your home county.'),
'south-carolina':dict(n='South Carolina',dept='the South Carolina Department of Insurance',ship='I-CARE (Insurance Counseling Assistance and Referrals for Elders)',metros='Charleston, Columbia, Greenville, Myrtle Beach and Hilton Head',
 med="In the recent 2026 sources we reviewed, South Carolina was not listed as having a Medigap birthday rule. That generally means that outside your Medigap Open Enrollment Period and federal guaranteed-issue situations, an insurer may ask health questions when you apply to change plans. Rules can change, so confirm with the South Carolina Department of Insurance, and do not end your current plan until a new one is approved.",
 loc="South Carolina draws many retirees to the coast and to growing inland metros, and many people split time between South Carolina and another state. If you are a part-year resident, check how each plan handles care outside its service area. Plan availability varies by county, so compare options at your primary address and confirm that the hospitals you use are in network.",
 slug='south-carolina',x='- **"I split time between South Carolina and another state."** Ask how the plan covers care outside its service area before you rely on it.'),
'georgia':dict(n='Georgia',dept='the Georgia Office of Insurance and Safety Fire Commissioner',ship='GeorgiaCares',metros='Atlanta, Savannah, Augusta, Columbus and Macon',
 med="In the recent 2026 sources we reviewed, Georgia was not listed as having a Medigap birthday rule. That generally means that outside your Medigap Open Enrollment Period and federal guaranteed-issue situations, an insurer may ask health questions when you apply to change plans. Rules can change, so confirm with the Georgia insurance commissioner's office, and do not cancel your current plan until a new one is approved.",
 loc="Georgia has a large Atlanta metro area with many health systems, and smaller communities and rural counties where networks can be narrower. Where you live inside the state can change which Medicare Advantage plans are offered, so compare options at your exact address. If you use specialists in Atlanta but live elsewhere, check that those doctors are in network.",
 slug='georgia',x='- **"I live outside Atlanta but see specialists there."** Check whether those specialists and hospitals are in your plan\'s network.'),
'alabama':dict(n='Alabama',dept='the Alabama Department of Insurance',ship='Alabama SHIP (State Health Insurance Assistance Program)',metros='Birmingham, Huntsville, Montgomery, Mobile and Tuscaloosa',
 med="In the recent 2026 sources we reviewed, Alabama was not listed as having a Medigap birthday rule. That generally means that outside your Medigap Open Enrollment Period and federal guaranteed-issue situations, an insurer may ask health questions when you apply to change plans. Rules can change, so confirm with the Alabama Department of Insurance, and do not cancel your current plan until a new one is approved.",
 loc="Alabama's larger cities such as Birmingham and Huntsville have more health systems and plan choices than many rural counties, where networks can be narrower and travel to specialists longer. If you rely on a specialist in a larger city, confirm that provider is in your plan's network. Plan availability varies by county, so compare options at your exact address.",
 slug='alabama',x='- **"The specialist I need is hours away."** Check network coverage for travel to larger cities before you choose a plan.'),
'louisiana':dict(n='Louisiana',dept='the Louisiana Department of Insurance',ship='Louisiana SHIP (State Health Insurance Assistance Program)',metros='New Orleans, Baton Rouge, Lafayette, Shreveport and Lake Charles',
 med="Louisiana is reported in 2026 sources as having a Medigap birthday rule. Reports describe a window of about 63 days following your birthday to switch to a plan with equal or lesser benefits without health questions, with the choice generally limited to your current insurer or its affiliate, though one guide describes a different window, so the details vary by source. Confirm the current window and rules with the Louisiana Department of Insurance before relying on it.",
 loc="Louisiana is organized into parishes, not counties, and Medicare plan availability is set by service area, so it can differ from one parish to the next. Residents in the New Orleans and Baton Rouge areas may have more plan choices than those in smaller parishes. Check that the hospitals and doctors you use, including those you reach after storms or travel, are in your plan's network.",
 slug='louisiana',x='- **"My parish has fewer plan options."** Plan availability is set by service area, so compare plans at your exact address and ask about nearby parishes\' hospitals.'),
'texas':dict(n='Texas',dept='the Texas Department of Insurance',ship='HICAP (Health Information, Counseling and Advocacy Program)',metros='Houston, Dallas–Fort Worth, Austin, San Antonio, El Paso and the Rio Grande Valley',
 med="In the recent 2026 sources we reviewed, Texas was not listed as having a Medigap birthday rule. That generally means that outside your Medigap Open Enrollment Period and federal guaranteed-issue situations, an insurer may ask health questions when you apply to change plans. Rules can change, so confirm with the Texas Department of Insurance, and do not cancel your current plan until a new one is approved.",
 loc="Texas is huge, and plan availability varies a great deal by county, from big metros like Houston and Dallas–Fort Worth to rural West Texas. Distances to specialists can be long, so network details matter. If you split your time between two cities or live near a county line, compare options for the exact address that your plan will use.",
 slug='texas',x='- **"I live near a county line."** Plan service areas follow counties, so confirm the plan is offered where you actually live.'),
'michigan':dict(n='Michigan',dept='the Michigan Department of Insurance and Financial Services (DIFS)',ship='MMAP (Michigan Medicare/Medicaid Assistance Program)',metros='Detroit, Grand Rapids, Lansing, Ann Arbor, Flint and the Upper Peninsula',
 med="In the recent 2026 sources we reviewed, Michigan was not listed as having a Medigap birthday rule, though one source notes that similar legislation has been considered. That generally means that outside your Medigap Open Enrollment Period and federal guaranteed-issue situations, an insurer may ask health questions when you apply to change plans. Rules can change, so confirm with DIFS, and do not cancel your current plan until a new one is approved.",
 loc="Michigan has a big difference between the Detroit, Ann Arbor, and Grand Rapids health systems and the northern Lower Peninsula and Upper Peninsula, where networks are smaller and travel for specialty care can be long. Many Michiganders also spend winters elsewhere, so ask how a plan covers care outside its service area. Plan availability varies by county, so compare options at your exact address.",
 slug='michigan',x='- **"I winter in another state."** Ask how the plan covers care outside Michigan, and whether it limits non-emergency care away from home.'),
'indiana':dict(n='Indiana',dept='the Indiana Department of Insurance',ship='Indiana SHIP (State Health Insurance Assistance Program)',metros='Indianapolis, Fort Wayne, Evansville, South Bend and Bloomington',
 med="Indiana is reported in 2026 sources as having a Medigap birthday-style rule, described as effective January 1, 2026, allowing a switch to the same plan type with a different insurer, though another source describes a window of about 30 to 60 days around your birthday. Because the details differ by source, confirm the exact window and rules with the Indiana Department of Insurance, and do not cancel your current plan until a new one is approved.",
 loc="Indiana's plan choices differ between the Indianapolis area, with several large health systems, and smaller cities and rural counties where there are fewer in-network options. If you use hospitals across a county line or in a neighboring state, confirm they are in your plan's network. Plan availability varies by county, so compare options at your exact address.",
 slug='indiana',x='- **"I use a hospital across the state line."** Confirm it is in network for the plan you choose.'),
'west-virginia':dict(n='West Virginia',dept='the West Virginia Offices of the Insurance Commissioner',ship='West Virginia SHIP (State Health Insurance Assistance Program)',metros='Charleston, Huntington, Morgantown, Wheeling and the Eastern Panhandle',
 med="West Virginia is listed in one 2026 source among states with some form of Medigap birthday rule, but the window, plan limits, and carrier rules were not stated, so we cannot give you exact terms. Confirm the current rule with the West Virginia Offices of the Insurance Commissioner before relying on it, and do not cancel your current plan until a new one is approved.",
 loc="West Virginia's terrain and small communities can mean longer trips to specialists and fewer in-network providers than in more urban states, and people in the Eastern Panhandle may use providers in neighboring Virginia or Maryland. Plan availability varies by county, so compare options at your exact address and check that the hospitals and clinics you use are in network.",
 slug='west-virginia',x='- **"My local hospital has limited specialists."** Check whether the plan covers specialists in neighboring Virginia, Maryland, Ohio, or Pennsylvania if you use them.'),
}
def state_post(k,d):
    n=d['n']
    body=f"""
If you live in {n} and you have been searching for how and when to change your Medicare Advantage or Medigap plan, you have probably found confusing answers, because the rules depend on which type of plan you have. Here is a clear {n}-specific guide that separates the two, with the federal windows that apply everywhere and what to check for {n} in particular.

## The quick answer for {n}
- **Medicare Advantage:** you can generally change during the Annual Enrollment Period (October 15 to December 7), during the Medicare Advantage Open Enrollment Period (January 1 to March 31) if you are already in an Advantage plan, or during a Special Enrollment Period if you qualify. These windows are set by Medicare, so they are the same in {n} as in every state.
- **Medigap:** there is no annual deadline, but whether you can switch without health questions depends on protections that include some state rules. See below for what we found for {n}.

## Medicare Advantage changes in {n}
1. **Annual Enrollment Period (Oct 15 – Dec 7).** Change plans for the following January 1. See our [Annual Enrollment guide](/medicare-annual-enrollment-period).
2. **Medicare Advantage Open Enrollment (Jan 1 – Mar 31).** If you are already in an Advantage plan, you get one change. Read the [full guide](/blog/medicare-advantage-open-enrollment-period-january-to-march).
3. **Special Enrollment Periods.** Triggered by moving to a new area, losing other coverage, your plan ending, or qualifying for Extra Help or Medicaid, among others. See [when you can switch plans](/blog/when-can-you-switch-medicare-plans).

## Medigap changes in {n}
{d['med']}

Regardless of state, you generally have protection in your six-month Medigap Open Enrollment Period and in certain federal guaranteed-issue situations. Our national guide, [when can I change my Medigap plan](/blog/when-can-i-change-my-medigap-plan-birthday-rule-and-underwriting), explains each one.

!callout **Apply first, cancel second.** Whatever the rule in {n}, wait for written approval of your new plan before ending the old one so you never have a gap.

{cta()}

## What to think about in {n}
{d['loc']} We serve people in and around {d['metros']}, and we handle everything by phone.

## Free help in {n}
{n}'s State Health Insurance Assistance Program is {d['ship']}, which offers free, unbiased Medicare counseling. For questions about Medigap rules and consumer protections, you can also contact {d['dept']}. Program names and contact details can change, so confirm through Medicare.gov or 1-800-MEDICARE.

## Common situations people ask about
- **"My doctor left my plan's network."** You may qualify for a Special Enrollment Period in some cases, and you can compare plans at the next window. See [what to do when a plan drops your doctor](/blog/why-did-my-medicare-advantage-plan-drop-my-doctor).
- **"My premium or drug costs went up."** Review your [Annual Notice of Change](/blog/how-to-read-medicare-annual-notice-of-change) and compare during the next open window.
- **"I moved within {n}."** A move to a different county can change which plans you can choose, and may open a Special Enrollment Period.
- **"I want to move from Advantage back to Original Medicare."** Check your Medigap options before you cancel. Read [leaving Medicare Advantage](/blog/switch-from-medicare-advantage-back-to-original-medicare).
- **"I have both Medicare and Medicaid."** You may have more frequent change opportunities. See [Medicaid and dual-eligible options](/medicaid-dual-eligible).
{d['x']}

## A checklist before you change anything in {n}
1. Identify which window you are in (AEP, MA-OEP, SEP, or Medigap rules).
2. List your doctors, hospitals, pharmacies, and medications.
3. Check each against the plan you are considering at your {n} address.
4. If it is Medigap, find out whether underwriting applies and apply before you cancel.
5. Confirm the effective date in writing.

## How Honorbrook helps {n} residents
We are an independent agency licensed in {n} and 10 other states. We compare plans offered at your address across many carriers, check your doctors and drugs, and explain the trade-offs plainly. Our help is free because carriers pay us, and your premium is the same whether you use an agent or enroll yourself. See our [{n} Medicare page](/{d['slug']}-medicare-insurance) for more about how we work in your state.
"""
    return dict(slug=f"when-can-i-change-my-medicare-plan-in-{d['slug']}",kind="med",
     title=f"When Can I Change My Medicare Advantage or Medigap Plan in {n}?",ttl=f"Change Your Medicare Plan in {n}: AEP, OEP and Medigap",short=f"Change Medicare Plan in {n}",em="Change",
     desc=f"When can you change your Medicare Advantage or Medigap plan in {n}? AEP, Open Enrollment, special periods, and {n}'s Medigap switching rules.",
     lead=f"The Medicare windows are federal, but Medigap switching rules vary by state. Here is what applies in {n}.",
     faqh=f"Changing Medicare Plans in {n} FAQ",
     faqs=[(f"When can I change my Medicare Advantage plan in {n}?",f"You can generally change during the Annual Enrollment Period (October 15 to December 7), during the Medicare Advantage Open Enrollment Period (January 1 to March 31) if you are already in an Advantage plan, or during a Special Enrollment Period if you qualify. These windows are the same in {n} as in every state."),
           (f"Can I change my Medigap plan any time in {n}?",f"You can generally apply any time of year, but whether you can switch without health questions depends on protections such as your Medigap Open Enrollment Period, federal guaranteed-issue rights, and any state rule. Confirm current {n} rules with {d['dept']}."),
           (f"Where can I get free Medicare help in {n}?",f"{n}'s State Health Insurance Assistance Program, {d['ship']}, offers free, unbiased counseling, and an independent agent like Honorbrook can compare plans available at your address at no cost to you.")],
     rel=[(f"{n} Medicare Help","How Honorbrook helps in your state.",f"/{d['slug']}-medicare-insurance"),("Annual Enrollment (AEP)","Dates, deadlines and what you can change.","/medicare-annual-enrollment-period"),("Medicare Supplement (Medigap)","Plan G, Plan N and more.","/medicare-supplement-medigap")],
     body=body)
POSTS=NATL+[state_post(k,d) for k,d in S.items()]
