CTA_M=("Not sure which Medicare option fits you?","We'll compare what's available at your address and check your doctors and drugs — free, no pressure.","Get my free plan review","/#contact")
def cta(a=None):
    a=a or CTA_M; return "!cta "+" | ".join(a)
REL_M=[("Medicare Annual Enrollment (AEP)","Dates, deadlines, and what you can change.","/medicare-annual-enrollment-period"),("Medicare Advantage Plans","Compare all-in-one Part C plans side by side.","/medicare-advantage"),("Medicare Supplement (Medigap)","See any doctor who accepts Medicare, with predictable costs.","/medicare-supplement-medigap")]
POSTS=[
dict(slug="can-i-change-my-medicare-plan-after-december-7",kind="med",
title="Can I Change My Medicare Plan After December 7? Your Options",ttl="Can I Change My Medicare Plan After December 7?",short="Change Medicare After Dec 7",em="Options",
desc="Missed the Dec 7 Medicare deadline? Learn which windows still let you change plans — Open Enrollment, Special Enrollment Periods and more.",
lead="Short answer: sometimes. The Annual Enrollment Period ends December 7, but other doors may still be open depending on your situation.",
faqh="Changing Medicare After Dec 7 FAQ",
faqs=[("Can I change Medicare plans in January?","If you are in a Medicare Advantage plan, you can generally make one change between January 1 and March 31 during the Medicare Advantage Open Enrollment Period. If you have Original Medicare with a stand-alone drug plan, this window usually does not let you switch drug plans."),
("What if I miss Medicare open enrollment completely?","Your current coverage generally continues into the new year, but it may change in price, network, or drug list. You may still qualify for a Special Enrollment Period if you move, lose coverage, or meet another qualifying condition."),
("Can I switch Medigap plans after December 7?","Medigap plans do not have a fixed annual window the way Advantage and drug plans do, but outside certain guaranteed-issue situations the insurer may use medical underwriting in most states, so it is best to check before dropping any coverage.")],
rel=REL_M,
body=f"""
If you are reading this after the Annual Enrollment Period (AEP) closed on December 7, you are probably worried that you are stuck with a plan that is wrong for 2027. Sometimes you are, and sometimes you are not. The honest answer depends on what type of Medicare coverage you have and what changed in your life. Here are the windows that can still open after December 7.

## First, a quick refresher on AEP
The Annual Enrollment Period runs every year from October 15 to December 7. During AEP anyone with Medicare can join, drop, or switch a Medicare Advantage plan or a Part D drug plan, and changes take effect on January 1. You can read more on our [Annual Enrollment page](/medicare-annual-enrollment-period). After AEP closes, most people are locked into their choices for the rest of the year unless another window applies.

## Window 1: Medicare Advantage Open Enrollment (Jan 1 – Mar 31)
If you are already enrolled in a [Medicare Advantage plan](/medicare-advantage), you get one more chance. Between January 1 and March 31 you can:
- Switch to a different Medicare Advantage plan, or
- Drop your Advantage plan and return to Original Medicare (and add a stand-alone [Part D plan](/medicare-part-d) if you want drug coverage).

You only get one change during this window, and it does not let you move from Original Medicare into Advantage. If you suspect your plan changed in ways you do not like, this is the window to know about.

!callout **Know the limit:** this window is for people who are already in a Medicare Advantage plan. If you have Original Medicare plus a drug plan, it generally does not apply to you.

## Window 2: Special Enrollment Periods (SEPs)
A Special Enrollment Period lets you change coverage outside the normal calendar when something qualifying happens. Common triggers include:
- You move to a new ZIP code or county that is outside your plan's service area, or you move into or out of a facility.
- You lose other coverage, such as employer coverage that was working with Medicare.
- Your plan leaves Medicare or stops serving your area.
- You qualify for Extra Help or you have both Medicare and Medicaid, which can create more frequent change opportunities.
- Your plan has a high Medicare quality rating, which in some cases lets you move into it once during the year.

SEP rules are specific, and the length of the window varies. If you think one applies, do not guess. Call before you change anything so your current coverage is not cancelled by mistake.

{cta()}

## Window 3: Your Medigap rights
[Medicare Supplement (Medigap)](/medicare-supplement-medigap) works differently. There is no annual deadline to buy or change a Medigap plan, but outside your six-month Medigap Open Enrollment Period (which starts when you are 65 and enrolled in Part B) and a few guaranteed-issue situations, insurers in most states can ask health questions and may decline or charge more based on your answers. A few states have more generous rules. Because of that, never cancel a Medigap plan until a replacement has been approved.

## What if none of these windows apply?
You may need to wait until next October 15. In the meantime, there are still practical steps that can protect you:
1. **Check your plan documents.** Compare the Annual Notice of Change to what your doctors and drugs actually require.
2. **Ask about exceptions.** If a drug you need is not covered, you can ask your plan for a formulary exception. If a doctor is out of network, ask about continuity-of-care options.
3. **Review costs again.** Know your deductible, copays, and annual out-of-pocket maximum so you can budget before a surprise.
4. **Set a reminder.** Put October 15 on your calendar so you can start comparing early.

## How to decide whether to change
Do not change plans just because you can. Switching only helps if the new plan fits your doctors, prescriptions, travel habits, and budget. A quick comparison takes a few minutes and avoids a second mistake. Before you switch, confirm your preferred doctors are in the new plan's network, your medications are on its drug list at a cost you can afford, and the plan serves your ZIP code year-round.

## Where Honorbrook fits in
We are an independent agency appointed with many carriers, so we can compare plans available at your address rather than push one company's plan. Our help is free to you: carriers pay us, and by law your premium is the same whether you use an agent or enroll alone. We handle this by phone across the states we serve, and we will tell you plainly if waiting for the next window is the better choice.
"""),
dict(slug="what-happens-if-i-do-nothing-during-medicare-open-enrollment",kind="med",
title="What Happens If I Do Nothing During Medicare Open Enrollment?",ttl="What Happens If I Do Nothing During Medicare Open Enrollment?",short="Doing Nothing at Medicare Enrollment",em="Nothing",
desc="Skipping Medicare open enrollment? See what usually happens to your plan, premiums, doctors and drugs if you make no changes, and when doing nothing is fine.",
lead="For many people the plan simply renews. But renewing is not the same as staying the same, and that is where costs creep in.",
faqh="Doing Nothing During Open Enrollment FAQ",
faqs=[("Will my Medicare coverage automatically continue if I do nothing?","In most cases yes. Original Medicare, Medigap, Medicare Advantage, and Part D plans generally renew for the next year if you take no action, though the plan's price, network, and benefits can change."),
("Can my Medicare Advantage plan change my doctors or drugs?","Yes. Plans can update networks and drug lists each year. That is why reviewing your Annual Notice of Change matters even if you plan to stay put."),
("What if my plan ends at the end of the year?","If your plan stops operating in your area, you generally get a Special Enrollment Period to choose a new plan, and you will receive a notice from the plan. Do not ignore it.")],
rel=REL_M,
body=f"""
Every fall, millions of people with Medicare get letters, calls, and ads telling them to act. If you are tired of the noise and tempted to ignore it all, you are not alone. The good news is that your coverage usually does not simply vanish. The risk is different: your plan can quietly change, and you only find out when you use it. Here is what normally happens when you do nothing during open enrollment.

## In most cases, your plan renews
Medicare plans are written to continue year to year. If you stay silent during the Annual Enrollment Period (October 15 – December 7), then:
- **Original Medicare** continues as is. Parts A and B do not need to be renewed.
- **Medigap (Medicare Supplement)** continues as long as you keep paying the premium.
- **Medicare Advantage** continues in the same plan, if the plan is still offered in your area.
- **Part D drug coverage** continues in the same plan, if the plan is still offered.

That is the baseline. The problem is what is allowed to change underneath.

## What can change when you do nothing
Plans reset their rules every January 1. Even if you keep the same plan name, any of the following might be different:
- **Premiums.** Your monthly premium can go up or down. This includes the Medigap premium, which typically rises with age or over time.
- **Deductibles and copays.** The cost of a primary care visit, a specialist, or a hospital stay can change.
- **Out-of-pocket maximum.** Advantage plans set a yearly cap on covered medical spending, and it can move.
- **Provider network.** A hospital or your doctor's group may leave the network.
- **Drug list (formulary).** A drug can move to a higher cost tier, require prior authorization, or be removed.
- **Extra benefits.** Dental, vision, hearing, and over-the-counter allowances can shrink or grow.

!callout **Your Annual Notice of Change (ANOC)** is the document that lists these changes. Plans are required to send it before open enrollment begins. If you have not opened it, find it before you decide to do nothing.

## When doing nothing is perfectly fine
Staying put makes sense when all of these are true:
1. Your doctors and hospital are still in network.
2. Every medication you take is still covered at a cost you accept.
3. Your total expected costs, premium plus copays plus drug costs, did not rise much.
4. You are happy with how the plan has worked for you this year.

If that sounds like you, a quick confirmation is all you need. It still takes only a few minutes to verify.

{cta(("Want a second set of eyes on your renewal?","Send us your plan letter or call and we will tell you in plain English whether staying makes sense.","Get my free plan review","/#contact"))}

## When doing nothing can cost you
The riskiest situations are:
- **You take expensive or specialty medications.** One tier change can add hundreds over a year.
- **Your doctor or hospital changed networks.** You may discover it only at the appointment.
- **Your premium or copays climbed.** A small monthly increase adds up across twelve months.
- **Your needs changed.** A new diagnosis, a planned surgery, or a move can make last year's plan a poor fit.

## If you miss the deadline and regret it
Missing the December 7 cutoff does not always lock you out. If you have a Medicare Advantage plan, you may be able to make one change between January 1 and March 31. Some life events also trigger a Special Enrollment Period. Read our guide on [when you can switch plans](/blog/when-can-you-switch-medicare-plans) for the full list.

## A simple 10-minute review
You do not need to become a Medicare expert. Do this once a year:
1. Open the Annual Notice of Change and read the summary page.
2. List your doctors and prescriptions.
3. Check each against the new year's network and drug list.
4. Compare the total cost to one other plan type, for example the [Medigap versus Advantage choice](/blog/medicare-advantage-vs-medigap-2026).

## How we help
We are an independent agency, which means we can compare many carriers instead of defending one. We check doctors and drugs against each plan and tell you whether staying put is smart. Our help costs you nothing: carriers pay us, and by law your premium is the same either way. Call or request a review and we will do the homework.
"""),
dict(slug="how-to-read-medicare-annual-notice-of-change",kind="med",
title="How Do I Read My Medicare Annual Notice of Change (ANOC)?",ttl="How to Read Your Medicare Annual Notice of Change",short="Read Your Medicare ANOC",em="Annual Notice of Change",
desc="Your Medicare Annual Notice of Change (ANOC) explains what changes next year. Here's what to check — premiums, drugs, doctors and benefits — in plain English.",
lead="That thick envelope from your plan is not junk mail. It tells you exactly how your coverage is about to change.",
faqh="Annual Notice of Change FAQ",
faqs=[("What is the Medicare Annual Notice of Change?","It is a document your Medicare Advantage or Part D plan sends each fall that summarizes changes to next year's costs, coverage, and rules. It is usually sent with the Evidence of Coverage."),
("When should I get my ANOC?","Plans are generally required to send it ahead of open enrollment, which begins October 15. If you have not received one, contact your plan or check your member portal."),
("What if I do not like the changes in my ANOC?","You can use the Annual Enrollment Period (October 15 – December 7) to switch plans for the next year. Compare alternatives before you decide.")],
rel=REL_M,
body=f"""
Each fall your Medicare Advantage or Part D plan mails a document called the Annual Notice of Change, or ANOC. It is easy to toss because it is long and written in insurance language. But it is the single most useful piece of mail you will get about your coverage, because it tells you what is different on January 1. Here is how to read it in about fifteen minutes.

## What the ANOC is and what it is not
The ANOC lists changes your plan is making for next year to costs, benefits, networks, and drug coverage. It usually arrives with another document, the Evidence of Coverage (EOC), which explains the plan's full rules. The ANOC is the short version of "what is changing." It does not replace the EOC, and it is not a bill.

Not every plan type sends one. Original Medicare does not, because Original Medicare's rules are set at the federal level. Medigap plans send a different kind of renewal notice. Advantage and Part D plans send the ANOC.

## Step 1: Go straight to the summary of changes
Most ANOCs start with a summary table. Look for these rows first:
- **Monthly premium.** Compare the new number to what you pay now.
- **Annual deductible.** The amount you pay before the plan begins sharing costs.
- **Maximum out-of-pocket (MOOP).** The yearly cap on covered medical spending for an Advantage plan.
- **Copays and coinsurance.** Primary care, specialist, emergency room, hospital stay, and lab tests.

If the increases are small, great. If several rows moved up, ask what you are getting in return.

## Step 2: Check your doctors and hospital
The ANOC may not list each doctor, so go to the plan's provider directory and search for yours by name. Also check:
1. Your primary care doctor.
2. Specialists you see regularly.
3. The hospital you would use.
4. Any pharmacy you rely on.

!callout **Why this matters:** networks change every year. A doctor leaving a plan's network is one of the most common surprises, and it does not always show up as a bold headline.

## Step 3: Check your prescriptions
This is where the biggest dollar differences hide. In the drug section look at:
- Whether each of your medications is still on the plan's formulary.
- Which cost tier it sits in. A move to a higher tier means higher copays.
- Whether new rules like prior authorization, step therapy, or quantity limits were added.
- The pharmacy network and whether your pharmacy is preferred or standard.

Write down every drug and strength, then check each one. If any drug changed, estimate the annual difference.

{cta(("We'll run your medication list for you","Send us your drug list and doctors and we will check them against every plan available at your address.","Check my doctors and drugs","/#contact"))}

## Step 4: Look at extra benefits
Dental, vision, hearing, over-the-counter allowances, fitness memberships, and transportation can change or disappear. If you chose the plan for a certain benefit, confirm it is still included and at the same level. See what Advantage plans typically add in [our guide to Medicare dental, vision and hearing](/blog/does-medicare-cover-dental-vision-and-hearing).

## Step 5: Compare against one alternative
Do not judge the changes in a vacuum. Compare the plan's total expected cost against at least one other option:
- A different [Medicare Advantage plan](/medicare-advantage) in your county.
- Original Medicare with a [Medigap plan](/medicare-supplement-medigap) and a stand-alone [Part D plan](/medicare-part-d).

A plan that looked cheap last year may not be the best value now, and the reverse can also be true.

## Red flags to watch for
- Your drug or your pharmacy moved to a higher cost level.
- A specialist or hospital you rely on is gone from the network.
- The maximum out-of-pocket amount increased noticeably.
- A benefit you use was cut or capped.
- The notice says the plan is leaving your area or ending.

If you see a plan ending notice, you generally get a Special Enrollment Period to pick a new plan, so do not ignore it.

## What to do next
If everything checks out, you can keep your plan and be done. If something looks off, you have until December 7 to switch for the next year. Putting it off to the last week is risky, because you may need time to compare plans and confirm your doctors.

## How Honorbrook helps
We read the ANOC with you, check doctors and drugs, and compare other options. We are an independent agency, so we are not tied to a single plan. Our help is free, because carriers pay us and your premium is the same either way.
"""),
dict(slug="why-did-my-medicare-advantage-plan-drop-my-doctor",kind="med",
title="Why Did My Medicare Advantage Plan Drop My Doctor? What to Do Now",ttl="Medicare Advantage Plan Dropped My Doctor: What to Do",short="Plan Dropped My Doctor",em="Drop My Doctor",
desc="Your Medicare Advantage plan dropped your doctor or a medication? Learn why it happens, what rights you have, and the steps to keep your care.",
lead="Doctors and drugs leave plans every year. Here is why it happens and the practical steps you can take right away.",
faqh="Dropped Doctor or Drug FAQ",
faqs=[("Why would a Medicare Advantage plan drop a doctor?","Contracts between plans and provider groups are renegotiated regularly. If they cannot agree on payment or terms, the provider can leave the network, or the plan can end the contract."),
("Can I keep seeing my doctor if they leave my plan's network?","Usually the visit will not be covered as in-network, and out-of-network care can cost much more or be denied under certain plan types. Ask your plan about continuity-of-care options and compare other plans before the next enrollment window."),
("What if my drug was removed from the plan's drug list?","You can ask your plan for a formulary exception with a supporting statement from your prescriber. You can also compare other plans during the next enrollment window or a Special Enrollment Period if you qualify.")],
rel=REL_M,
body=f"""
You went to schedule an appointment, and the office says they no longer take your plan. Or the pharmacy tells you your medication is suddenly not covered. It is frustrating and sometimes frightening, especially when you chose the plan with that doctor or drug in mind. This guide explains why it happens and what you can do.

## Why do doctors leave Medicare Advantage networks?
A [Medicare Advantage plan](/medicare-advantage) is run by a private insurer that contracts with doctors, hospitals, and medical groups to form a network. Those contracts are not permanent. Reasons a provider can leave include:
- A payment disagreement between the plan and the provider group.
- A merger or change of ownership at the hospital or medical group.
- The provider deciding to stop accepting that plan because of paperwork or reimbursement.
- The plan reorganizing its network to cut costs or focus on a different service area.

None of this means you did something wrong, and none of it is hidden. It simply happens, often in the fall for the following year.

## Why do drugs leave the formulary?
Each plan has a drug list, called a formulary, that it can change. A medication can be moved to a higher cost tier, restricted by prior authorization, or removed entirely. Plans update formularies for the new year and sometimes mid-year when generics appear or manufacturers change pricing. The drug is still available, but the plan may not help pay for it as before.

!callout **The best protection is checking early.** Review your plan's Annual Notice of Change each fall and search for your doctors and drugs before December 7. See our step-by-step guide on [how to read your ANOC](/blog/how-to-read-medicare-annual-notice-of-change).

## What to do right now if your doctor is out of network
1. **Call the plan and the doctor's office.** Confirm the facts. Sometimes a listing is out of date.
2. **Ask about continuity of care.** Some plans allow a transition period for ongoing treatment such as chemotherapy or recovery after surgery.
3. **Understand your plan type.** HMO plans generally do not cover out-of-network care except in emergencies, while PPO plans may cover some out-of-network visits at a higher cost.
4. **Look for timing options.** Depending on the circumstances, you may qualify for a Special Enrollment Period, or you may need to wait for the next window. Our guide on [when you can switch plans](/blog/when-can-you-switch-medicare-plans) explains the options.

{cta(("Need to find a plan that keeps your doctor?","We will check your doctors and drugs against every plan available at your address before you switch.","Check my doctors","/#contact"))}

## What to do right now if a drug is no longer covered
- **Ask for a formulary exception.** Have your doctor submit a statement explaining why you need that drug rather than an alternative.
- **Ask whether a covered alternative exists.** Your prescriber may be able to switch you to a similar medication on the formulary.
- **Check pharmacy options.** A preferred pharmacy in the plan's network can lower the price.
- **Look at manufacturer assistance and discount programs.** These do not replace insurance, but they can reduce what you pay at the counter. Ask your pharmacist.
- **Review your Part D options.** See [what Part D plans cost](/blog/what-does-medicare-part-d-actually-cost) and how to lower the total.

## How to avoid this next year
A few habits make a big difference:
- **Verify before you enroll,** not after. Search each doctor and drug in the plan's directory for the exact plan you are joining.
- **Do not rely on last year's memory.** Re-check every fall.
- **Compare plan types.** If keeping your doctor matters more than saving on the monthly premium, [Original Medicare with Medigap](/medicare-supplement-medigap) lets you see any doctor who accepts Medicare nationwide.
- **Keep a list.** Names of doctors, hospitals, pharmacies, and medications, with dosages, so you can verify them quickly.

## When to consider changing plans
If a key doctor or drug is gone, the plan may no longer fit your life. But do not switch in a panic. First confirm that the new plan includes everything you need, that the premium and copays make sense, and that you understand the timing of any change. Switching without checking can lead to a second problem.

## How we help
Honorbrook is an independent agency. We look up your doctors and drugs plan by plan, explain the trade-offs between Advantage and Medigap, and tell you what window you are in. There is no charge for our help, because carriers pay us and your premium is the same either way.
"""),
dict(slug="switch-from-medicare-advantage-back-to-original-medicare",kind="med",
title="Should I Switch From Medicare Advantage Back to Original Medicare?",ttl="Switch From Medicare Advantage to Original Medicare?",short="Advantage Back to Original Medicare",em="Original Medicare",
desc="Thinking of leaving Medicare Advantage for Original Medicare? Learn the enrollment windows, the Medigap catch, and how to decide before you drop anything.",
lead="You can leave an Advantage plan, but getting a Medigap plan afterward is the part that trips people up.",
faqh="Leaving Medicare Advantage FAQ",
faqs=[("When can I switch from Medicare Advantage to Original Medicare?","Generally during the Annual Enrollment Period (October 15 – December 7) or the Medicare Advantage Open Enrollment Period (January 1 – March 31), and during certain Special Enrollment Periods."),
("Can I get a Medigap plan if I leave Medicare Advantage?","Outside of specific guaranteed-issue rights, insurers in most states can use medical underwriting, which means they may decline you or charge more depending on your health. Some states have additional protections."),
("Do I need a separate Part D plan if I return to Original Medicare?","If you want prescription drug coverage, yes. Original Medicare does not include it, so you would add a stand-alone Part D plan, and enrolling late can carry a penalty.")],
rel=REL_M,
body=f"""
Many people choose a [Medicare Advantage plan](/medicare-advantage) because the low premium and extra benefits look attractive, and for a lot of them it works well. But health changes, doctors leave networks, and travel habits shift. If you have started to wonder whether Original Medicare would suit you better, you are asking a reasonable question. The key is to understand the catch before you drop your plan.

## The first question: why do you want to switch?
The right move depends on the reason. People usually consider leaving Advantage because of:
- Limited provider networks or referrals they find frustrating.
- Higher-than-expected copays or approvals for care.
- A need to see specialists outside the plan's area.
- Spending long periods in another state.
- A health change that makes predictable costs more valuable.

If your reason is one of those, Original Medicare with a [Medigap plan](/medicare-supplement-medigap) may fit better. If it is only a single problem, a different Advantage plan could solve it without a big change.

## When can you leave Medicare Advantage?
There are three common windows:
1. **Annual Enrollment Period (Oct 15 – Dec 7).** You can drop your Advantage plan and return to Original Medicare, effective January 1.
2. **Medicare Advantage Open Enrollment Period (Jan 1 – Mar 31).** You can leave your plan and go back to Original Medicare once.
3. **Special Enrollment Periods.** Triggers include moving out of the plan's area, losing coverage, or your plan ending.

!callout **Do not cancel first.** Make sure your replacement coverage is set up before your Advantage plan ends, so there is no gap in your coverage.

## What changes when you return to Original Medicare
Original Medicare means Parts A and B, administered by the federal government. Compared with an Advantage plan:
- **Doctor choice is broader.** You can see any provider in the U.S. who accepts Medicare.
- **No network or referral rules.** You generally do not need approval to see a specialist.
- **No annual out-of-pocket cap by default.** Parts A and B carry deductibles and 20 percent coinsurance for many Part B services unless a Medigap plan covers them.
- **No drug coverage.** You would add a stand-alone [Part D plan](/medicare-part-d).
- **Extras usually go away.** Dental, vision, hearing, and fitness benefits included in your Advantage plan are not part of Original Medicare.

## The Medigap catch
This is the part people miss. Medigap (Medicare Supplement) plans fill the gaps in Original Medicare, such as deductibles and coinsurance. Most Medigap sales are subject to medical underwriting unless you are in a guaranteed-issue situation. That means:
- If you are not in a protected window, an insurer in most states can ask health questions and may decline you or charge more.
- If you first joined Medicare Advantage when you turned 65 and leave within the first year, you may have a trial right that guarantees Medigap access.
- A few states have continuous or annual guaranteed-issue rules that are more generous.

Because Medigap rules vary by state and by your circumstances, check your options before you leave your Advantage plan. A rushed switch without Medigap leaves you with Original Medicare's 20 percent coinsurance and no cap.

{cta(("Find out if you can get Medigap before you leave","We will check your state's rules and your options before you cancel anything.","Check my Medigap options","/#contact"))}

## Cost comparison: think in total, not monthly
An Advantage plan may have a low or $0 premium, but you pay copays when you use care. A Medigap plan has a higher monthly premium but little out-of-pocket cost when you use care. Compare:
- Your premium for each choice (plus the Part B premium, which everyone pays).
- Your drug plan premium and drug costs.
- Your likely use of care in a typical year and in a bad year.
- The most you could pay in a worst-case year.

Our guide on [Medicare Advantage vs. Medigap](/blog/medicare-advantage-vs-medigap-2026) walks through the comparison in more detail.

## A safe sequence if you decide to switch
1. Confirm your enrollment window.
2. Apply for a Medigap plan and wait for approval.
3. Enroll in a stand-alone Part D plan if you need drug coverage.
4. Only then confirm the end date of your Advantage plan.
5. Keep your confirmation letters.

## How we help
We are an independent agency and we can compare Medigap and Advantage options from many carriers, check your state's rules, and tell you honestly which path makes sense. Our help is free because carriers pay us, and your premium is the same either way.
"""),
dict(slug="medicare-parts-a-b-c-d-explained",kind="med",
title="Medicare Part A, B, C and D Explained: What Each Part Covers",ttl="Medicare Parts A, B, C and D Explained",short="Medicare Parts A, B, C, D",em="Explained",
desc="Medicare Parts A, B, C and D in plain English: what each part covers, what it costs in general terms, and how they fit together.",
lead="Four letters, one confusing system. Here is what each part does and how people usually put them together.",
faqh="Medicare Parts FAQ",
faqs=[("What is the difference between Medicare Part A and Part B?","Part A generally covers inpatient hospital stays, skilled nursing facility care, hospice, and some home health. Part B generally covers doctor visits, outpatient care, preventive services, and medical equipment."),
("Is Medicare Part C the same as Medicare Advantage?","Yes. Part C is another name for Medicare Advantage, which bundles Parts A and B (and usually Part D) through a private insurance company approved by Medicare."),
("Do I need Part D if I do not take many medications?","Even if you take few medications now, going without drug coverage can lead to a late enrollment penalty later if you enroll after your initial window. Talk to an agent before skipping it.")],
rel=REL_M,
body=f"""
The first time you read about Medicare, the letters can feel like alphabet soup. Part A, Part B, Part C, Part D, plus Medigap on top. The structure is actually simple once you see it. Parts A and B are Original Medicare. Part C is a different way to get A and B. Part D is drug coverage. Here is what each does.

## Part A: hospital insurance
Medicare Part A generally helps pay for:
- Inpatient care in a hospital.
- Skilled nursing facility care after a qualifying hospital stay.
- Hospice care.
- Some home health care.

Most people do not pay a monthly premium for Part A if they or a spouse paid Medicare taxes for enough years. Part A does have a deductible for each benefit period and cost-sharing for longer stays.

## Part B: medical insurance
Medicare Part B generally helps pay for:
- Doctor visits and specialist services.
- Outpatient care and many diagnostic tests.
- Preventive services such as screenings and vaccines.
- Durable medical equipment such as walkers.

Part B has a monthly premium, an annual deductible, and typically 20 percent coinsurance for many covered services. There is no cap on what you could pay in a year unless you have other coverage. Higher-income beneficiaries pay a higher Part B premium, known as an income-related adjustment.

!callout **Parts A and B together are Original Medicare.** It is run by the federal government, you can see any doctor or hospital in the U.S. that accepts Medicare, and it does not include routine dental, vision, hearing aids, or prescription drug coverage.

## Part C: Medicare Advantage
Part C is also called [Medicare Advantage](/medicare-advantage). Instead of Original Medicare, you get your Part A and Part B benefits through a private insurance company approved by Medicare. These plans:
- Must cover everything Original Medicare covers (with the exception of hospice, which Original Medicare still handles).
- Usually include prescription drug coverage.
- Often include extra benefits like dental, vision, hearing, or fitness memberships.
- Use networks such as HMOs or PPOs.
- Include an annual out-of-pocket maximum.

You still pay your Part B premium, and the plan may charge its own premium, which is often low or $0.

## Part D: prescription drug coverage
[Part D](/medicare-part-d) plans are sold by private insurers and help pay for prescription drugs. You can add one to Original Medicare, or it may be built into a Medicare Advantage plan. Each Part D plan has its own formulary (drug list), pharmacy network, premium, deductible, and cost-sharing. If you do not join when first eligible and have no other creditable drug coverage, you may owe a lifetime late enrollment penalty. Read [what Part D actually costs](/blog/what-does-medicare-part-d-actually-cost) for how the pieces add up.

## Where does Medigap fit?
[Medicare Supplement (Medigap)](/medicare-supplement-medigap) is separate insurance that works alongside Original Medicare. It helps pay deductibles and coinsurance that Original Medicare leaves to you. You cannot use Medigap with a Medicare Advantage plan. People who choose Medigap generally also add a Part D plan.

{cta(("Not sure which combination fits you?","We'll walk through your doctors, drugs, and budget and show you the real options.","Get my free plan review","/#contact"))}

## The two common ways to put it together
1. **Original Medicare + Medigap + Part D.** Higher monthly premiums, broad doctor choice, and predictable costs when you use care.
2. **Medicare Advantage (Part C), usually with Part D built in.** Often low premiums and extras, but you use a network and pay copays.

Neither is automatically better. See [Advantage vs. Medigap](/blog/medicare-advantage-vs-medigap-2026) for a closer comparison.

## When do you enroll?
Your Initial Enrollment Period lasts seven months, around your 65th birthday. After that, there are specific windows each year. If you are approaching 65, see our [Turning 65 guide](/turning-65). Delaying Part B or Part D without other qualifying coverage can lead to penalties, so timing matters.

## Plain-English summary
- **Part A:** hospital.
- **Part B:** doctor and outpatient care.
- **Part C:** a private-plan alternative that bundles A, B, and usually D.
- **Part D:** prescription drugs.
- **Medigap:** optional add-on for Original Medicare.

## How we help
Honorbrook is an independent agency and we compare the real plans available at your address. Our help is free to you, because carriers pay us and your premium is the same either way. We can walk you through your options by phone.
"""),
dict(slug="does-medicare-cover-dental-vision-and-hearing",kind="med",
title="Does Medicare Cover Dental, Vision and Hearing?",ttl="Does Medicare Cover Dental, Vision and Hearing?",short="Medicare Dental, Vision, Hearing",em="Dental, Vision and Hearing",
desc="Does Medicare cover dental, vision and hearing? Learn what Original Medicare covers, what Advantage plans add, and other ways to cover those costs.",
lead="Original Medicare mostly does not cover routine teeth, eyes, and ears. Here is what is covered and how people fill the gap.",
faqh="Medicare Dental, Vision & Hearing FAQ",
faqs=[("Does Original Medicare cover routine dental care?","Generally no. Original Medicare does not cover most routine dental care such as cleanings, fillings, or dentures, with limited exceptions when dental care is part of a covered medical procedure."),
("Does Medicare cover eyeglasses or hearing aids?","Original Medicare does not usually cover routine eye exams, eyeglasses, or hearing aids, with limited exceptions such as eyeglasses after cataract surgery. Some Medicare Advantage plans include allowances."),
("Are dental, vision and hearing benefits the same on every Advantage plan?","No. Benefits, limits, and networks vary by plan and by county, so check the specifics for any plan you are considering.")],
rel=[("Dental, Vision & Hearing Insurance","Stand-alone coverage you can add.","/dental-vision-hearing-insurance"),("Medicare Advantage Plans","Many include extra benefits.","/medicare-advantage"),("Medicare Supplement (Medigap)","Fills Original Medicare gaps.","/medicare-supplement-medigap")],
body=f"""
Teeth, eyes, and ears are the three things most people ask about when they first look at Medicare. The surprise is that Original Medicare mostly leaves them out. That does not mean you have no options. Here is what is covered, what is not, and how people handle the gap.

## What Original Medicare covers
Original Medicare means Parts A and B. For these three areas, coverage is limited:
- **Dental.** Generally not covered for routine care like cleanings, fillings, extractions, root canals, or dentures. There are narrow exceptions, such as dental services needed as part of certain covered hospital procedures.
- **Vision.** Routine eye exams, eyeglasses, and contact lenses are generally not covered. There are exceptions, for example eyeglasses or contacts after cataract surgery, and some screenings for people at higher risk of eye disease.
- **Hearing.** Routine hearing exams and hearing aids are generally not covered, although diagnostic hearing and balance exams ordered by a doctor may be.

!callout **Rules and exceptions change,** so confirm details for any procedure with Medicare or your plan before you schedule it.

## What Medicare Advantage often adds
Many [Medicare Advantage plans](/medicare-advantage) include extra benefits beyond Original Medicare. Depending on the plan, these may include:
- Preventive and basic dental such as exams and cleanings, and sometimes fillings or dentures.
- Routine eye exams with an allowance toward eyeglasses or contacts.
- Hearing exams and an allowance toward hearing aids.
- Over-the-counter allowances and fitness memberships.

Benefits vary a lot. Some plans have low annual dollar limits, waiting periods, or networks that include only certain dentists, so a headline benefit might not match what you actually need. Always check the plan's specific details and confirm that your providers are in network.

## Your options for coverage
1. **Pick an Advantage plan with the benefits you use.** If you need dental work, look at annual limits and network dentists before enrolling.
2. **Add stand-alone dental, vision, and hearing insurance.** If you have Original Medicare with a Medigap plan, you can still buy separate [dental, vision and hearing coverage](/dental-vision-hearing-insurance). Compare waiting periods, annual maximums, and networks.
3. **Use discount plans or local programs.** These are not insurance, but they can lower out-of-pocket costs.
4. **Check other sources.** Some people qualify for help through Medicaid or other programs depending on the state and income. Read about [Medicaid and dual-eligible options](/medicaid-dual-eligible).
5. **Pay out of pocket for routine care.** Some people choose to save for these costs rather than buy coverage.

{cta(("Compare plans by the benefits you actually use","Tell us what matters most — teeth, glasses, hearing aids — and we'll compare real plans at your address.","Get my free comparison","/#contact"))}

## How to decide
A useful way to think about it is to list what you expect to use in the next year:
- Do you have upcoming dental work such as crowns or dentures?
- Do you wear glasses or contacts, and when did you last update them?
- Have you noticed hearing changes, and would you consider hearing aids?
- Do your preferred dentist, optometrist, and audiologist take the plan?

Then compare total yearly cost: plan premium, copays, and what you would pay out of pocket for dental or hearing beyond the plan limits. A plan with a generous dental benefit but a restrictive network might cost you more than a plan with a smaller benefit that includes your dentist.

## Common mistakes
- Assuming a benefit is unlimited because it is listed.
- Skipping the dentist's name check in the plan directory.
- Forgetting waiting periods for major dental work.
- Comparing only the monthly premium and ignoring the extras.
- Buying stand-alone coverage that duplicates what your plan already provides.

## When to review
Benefits can change every year, so review your Annual Notice of Change each fall. If you rely on a particular benefit, [read the ANOC carefully](/blog/how-to-read-medicare-annual-notice-of-change) and compare alternatives before the December 7 deadline.

## How Honorbrook helps
We are an independent agency. We compare Medicare Advantage plans and stand-alone dental, vision, and hearing options from many carriers and match them to what you actually use. Our help costs you nothing, because carriers pay us and your premium is the same whether or not you use an agent.
"""),
dict(slug="medigap-plan-g-vs-plan-n-2027",kind="med",
title="Medigap Plan G vs. Plan N in 2027: Which Costs Less for You?",ttl="Medigap Plan G vs. Plan N for 2027",short="Plan G vs. Plan N (2027)",em="Costs Less",
desc="Comparing Medigap Plan G and Plan N for 2027? See the differences in copays, Part B excess charges and how to decide which one saves you more.",
lead="Plan G has a higher premium and fewer surprises. Plan N costs less each month but asks for small copays. Which wins depends on how you use care.",
faqh="Plan G vs. Plan N FAQ",
faqs=[("What is the main difference between Medigap Plan G and Plan N?","Plan G covers nearly all Medicare cost-sharing except the Part B deductible, while Plan N usually has a lower premium but may have copays for office visits and emergency room visits, and does not cover Part B excess charges."),
("Which Medigap plan is cheaper, G or N?","Plan N is usually cheaper per month, but pricing varies by carrier, age, ZIP code, and tobacco use, and the cheaper premium can be offset by copays and excess charges if you use a lot of care."),
("Can I switch from Plan G to Plan N later?","You can apply, but outside certain guaranteed-issue situations the insurer may require health underwriting in most states, so switching may not be easy.")],
rel=[("Medicare Supplement (Medigap)","Compare plans and carriers.","/medicare-supplement-medigap"),("Plan G vs. Plan N guide","Our earlier side-by-side breakdown.","/blog/medigap-plan-g-vs-plan-n"),("Advantage vs. Medigap","Which type of plan suits you?","/blog/medicare-advantage-vs-medigap-2026")]
,body=f"""
If you have decided on Original Medicare with a [Medicare Supplement (Medigap) plan](/medicare-supplement-medigap), the next question is often which letter to choose. For new enrollees, Plan G and Plan N are the two most commonly compared. Both are strong plans. The real question is how much risk you are comfortable with in exchange for a lower monthly premium. This guide explains the differences without quoting prices, because prices change by carrier, age, and ZIP code.

## What Medigap plans are standardized
Medigap plans are standardized by letter, so a Plan G sold by one company covers the same benefits as a Plan G sold by another, in most states. The difference is the premium, the carrier's service, and how the company raises rates over time. That is why comparing carriers within a plan letter matters just as much as comparing letters.

## What Plan G covers
Plan G pays for most of the costs Original Medicare leaves to you, including:
- Part A coinsurance and hospital costs.
- Part A deductible.
- Part B coinsurance or copayment.
- Part B excess charges (when a doctor charges above the Medicare-approved amount, where allowed).
- Skilled nursing facility coinsurance.
- Foreign travel emergency care, subject to limits.

You pay the Part B deductible once per year. After that, Plan G generally leaves you with few out-of-pocket costs for Medicare-covered care.

## What Plan N covers
Plan N covers much the same list but with a few differences:
- **Office visit copay.** You may pay up to a set copay for some doctor visits.
- **Emergency room copay.** A copay may apply if you are not admitted.
- **No Part B excess charge coverage.** If a provider charges more than the Medicare-approved amount, you may owe the difference.
- You also pay the Part B deductible.

Plan N premiums are generally lower, which is its appeal.

!callout **Excess charges are rare in some areas and more common in others.** Ask your doctors whether they accept Medicare assignment. If they do, excess charges are not an issue.

## A framework for deciding
Think about three things:
1. **How often do you use care?** If you visit doctors frequently, copays on Plan N add up. If you visit rarely, the lower premium may win.
2. **How much surprise can you absorb?** Plan G is predictable. With Plan N, a bad year can cost more than expected.
3. **Which doctors do you see?** If your providers accept assignment, the excess-charge risk drops.

A simple comparison is to take the premium difference between G and N, multiply by twelve, then compare it to the copays you would pay in a typical year and in a heavy-use year. If the annual premium savings is larger than your expected copays, Plan N may save you money. If you expect many visits, Plan G may break even or win.

{cta(("See real Plan G and Plan N quotes side by side","We'll compare carriers at your ZIP code and show the true annual cost for each plan.","Get my free Medigap comparison","/#contact"))}

## Why the cheapest premium can be misleading
Medigap premiums are not just about the starting price. Carriers use different rating methods:
- **Attained-age:** the premium rises as you get older.
- **Issue-age:** the premium is based on the age you were when you bought the plan, and does not rise because of age (it can still rise with inflation).
- **Community-rated:** the same premium for everyone regardless of age.

A plan that looks cheapest at 65 may become expensive later. Ask how a carrier has handled rate increases historically, and compare more than one.

## Other points to consider
- **High-deductible Plan G.** Some carriers offer a high-deductible version of Plan G with a much lower premium and a larger annual deductible. It can make sense for healthy people who want catastrophic protection.
- **Household discounts.** Some carriers discount for spouses at the same address.
- **Timing.** Your best chance for guaranteed acceptance is during your six-month Medigap Open Enrollment Period. Outside it, health questions may apply.
- **Drug coverage.** Medigap does not include drug coverage, so you need a separate [Part D plan](/medicare-part-d).

## Bottom line
Choose Plan G if you want the most predictable costs and are willing to pay a bit more each month. Choose Plan N if you use care moderately, your doctors accept assignment, and you want a lower premium. If you want to see how the two compare to an Advantage plan, read [Advantage vs. Medigap](/blog/medicare-advantage-vs-medigap-2026). For a shorter breakdown, see our earlier [Plan G vs. Plan N guide](/blog/medigap-plan-g-vs-plan-n).

## How we help
We are an independent agency, so we compare Plan G and Plan N across many carriers and show the actual price at your ZIP code and age. Our help costs you nothing because carriers pay us and your premium is the same either way.
"""),
]
