def cta(a=None):
    a=a or ("Get real numbers for your household","We compare plans and subsidies at your address — free, no pressure.","Get my free quote","/#contact"); return "!cta "+" | ".join(a)
REL_H=[("ACA Health Plans (Under 65)","Individual & family marketplace plans.","/aca-health-insurance"),("Lost Health Coverage","The 60-day special enrollment window.","/lost-health-coverage"),("Self-Employed Health Insurance","Options if you work for yourself.","/self-employed-health-insurance")]
NOTE="!callout **Rules change.** Subsidy amounts, enrollment dates, and eligibility rules for Marketplace coverage have changed in recent years and can change again. Treat this article as a guide to how things work, and confirm current figures before you decide."
POSTS=[
dict(slug="how-much-does-health-insurance-cost-without-a-job",kind="health",
title="How Much Does Health Insurance Cost Without a Job?",ttl="How Much Does Health Insurance Cost Without a Job?",short="Health Insurance Cost Without a Job",em="Cost",
desc="Wondering what health insurance costs without employer coverage? Learn what drives the price — age, location, plan tier, subsidies — and how to estimate yours.",
lead="There is no single number. Your price depends on a handful of factors, and the biggest one is often your income.",
faqh="Cost Without a Job FAQ",
faqs=[("Why is there no standard price for individual health insurance?","Premiums depend on your age, ZIP code, tobacco use, the plan tier you choose, and the insurers in your area. Subsidies based on income can also change what you actually pay."),
("Can I get help paying for health insurance if I lose my job?","Many people qualify for premium tax credits through the Marketplace based on their expected household income, and some qualify for Medicaid. Eligibility rules vary by state and can change."),
("Is COBRA cheaper than a Marketplace plan?","COBRA keeps your employer plan but you generally pay the full premium plus a fee. A Marketplace plan with a subsidy is often cheaper, but the network and benefits may differ.")],
rel=REL_H,
body=f"""
It is one of the most common questions people type after leaving a job: how much will health insurance cost me now? The honest answer is that it varies a lot, and the quickest way to a useful number is to understand what drives the price. This guide explains the main factors so you know what to expect before you run quotes.

{NOTE}

## The five things that set your premium
Individual health plans sold through the Marketplace are priced mostly on:
1. **Your age.** Older adults pay more, within limits set by law.
2. **Where you live.** Prices vary by state, county, and which insurers compete there.
3. **Tobacco use.** In most states insurers can charge more for tobacco users.
4. **Plan tier.** Bronze, Silver, Gold, and Platinum plans trade monthly premium against deductibles and copays. See our [Bronze vs. Silver vs. Gold guide](/blog/bronze-vs-silver-vs-gold-aca-plans).
5. **Household size.** Covering a family costs more than covering one person, though children are priced differently.

Notice that your health history is not on the list. ACA-compliant plans cannot charge you more because of pre-existing conditions.

## Income matters more than most people expect
Premium tax credits reduce the monthly price of Marketplace plans for many households. How much help you get depends on your expected household income, the cost of a benchmark plan in your area, and the rules in effect for that year. Two households with the same plan can pay very different amounts after subsidies. If your income dropped when you lost your job, you may qualify for more help than you expect, or even for Medicaid in some states.

## Your realistic options
- **COBRA.** You keep your old plan, but you typically pay the full premium plus an administrative fee. It can be expensive, but it may make sense if you are mid-treatment or near your deductible.
- **Marketplace plan.** Often the best value once subsidies are considered, with multiple tiers to choose from.
- **Medicaid.** Based on income and state rules.
- **A spouse's or partner's employer plan.** Losing coverage can open a window to join.
- **Short-term plans.** Cheaper but with limits and exclusions, so they are not a substitute for comprehensive coverage.

{cta()}

## The costs beyond the premium
The premium is only part of the bill. Compare these too:
- **Deductible.** What you pay before the plan starts sharing costs. See [deductible vs. out-of-pocket maximum](/blog/deductible-vs-out-of-pocket-maximum-explained).
- **Copays and coinsurance.** What you pay for visits and services.
- **Out-of-pocket maximum.** The most you could pay in a year for covered in-network care.
- **Drug coverage.** Tier structure and pharmacy network.
- **Provider network.** Whether your doctors are included.

A Bronze plan has a low premium but a high deductible. A Silver plan costs more each month but can include extra cost-sharing help if your income qualifies. A Gold plan costs more still but pays more when you use care.

## How to estimate your own price
1. Estimate your household income for the year, including any severance or unemployment benefits.
2. Count the people who need coverage.
3. Note your ZIP code and ages.
4. Compare a Bronze, a Silver, and a Gold plan, with subsidies applied.
5. Add up the premium, the deductible, and the out-of-pocket maximum for each.

The cheapest premium is rarely the cheapest year. If you expect to use care, a mid-tier plan can cost less overall.

## When you can enroll
If you lost coverage, you generally have a Special Enrollment Period of 60 days. If you did not, you usually enroll during Open Enrollment. Read about the [60-day window](/lost-health-coverage) and how to [choose between your options](/blog/lost-your-job-coverage-your-health-insurance-options).

## Common mistakes
- Picking the lowest premium without checking the deductible.
- Overestimating income and missing out on subsidies, or underestimating it and owing money later.
- Missing the enrollment deadline.
- Not checking whether doctors and drugs are covered.

## How we help
Honorbrook is an independent agency. We compare plans and subsidies at your address, explain the trade-offs, and help you enroll. Our help is free, because carriers pay us and your premium is the same either way.
"""),
dict(slug="aca-open-enrollment-deadline-can-i-sign-up-late",kind="health",
title="What Is the ACA Open Enrollment Deadline, and Can I Still Sign Up Late?",ttl="ACA Open Enrollment Deadline: Can I Sign Up Late?",short="ACA Open Enrollment Deadline",em="Deadline",
desc="Missed or unsure about the ACA open enrollment deadline? Learn how enrollment windows work, when you can sign up late, and what qualifies for a special enrollment.",
lead="Enrollment windows have been changing, so check current dates. Here is how the system works and your late-signup options.",
faqh="ACA Enrollment Deadline FAQ",
faqs=[("When is ACA open enrollment?","The federal Marketplace has typically opened November 1, with the end date set by federal rules that have changed in recent years. State-run marketplaces may set their own dates, so confirm the current dates for your state."),
("Can I sign up for ACA coverage after the deadline?","Usually only with a qualifying life event that opens a Special Enrollment Period, such as losing other coverage, moving, getting married, or having a baby."),
("What if I miss the deadline and have no qualifying event?","You may have to wait for the next open enrollment, though other options such as Medicaid, which enrolls year-round for those who qualify, may be available.")],
rel=REL_H,
body=f"""
Every year around the start of November, people begin searching for the health insurance enrollment deadline. The tricky part is that the exact dates have been changing, and they can differ between the federal Marketplace and state-run marketplaces. This guide explains how enrollment windows work and your options if you miss one, without relying on dates that may have changed.

{NOTE}

## How open enrollment works
Open Enrollment is the yearly window when anyone can sign up for or change a Marketplace health plan. Key points:
- Coverage chosen during the window starts on a set date, often January 1 if you enroll early enough.
- Enrolling later in the window can mean a later start date.
- The federal Marketplace has historically opened on November 1, with a closing date that has varied. Recent federal rules have changed the length of the window for some years.
- State-run marketplaces, including many in the states we serve, may use different dates.

Because of that, always confirm the current dates at HealthCare.gov or your state marketplace, or call us and we will check for your state.

## Why the deadline matters
Miss the window and, in most cases, you cannot buy Marketplace coverage until the next open enrollment, unless something qualifies you for a Special Enrollment Period. Going without coverage means you pay for medical care out of pocket, which can be costly even for routine events.

## Special Enrollment Periods: the exceptions
You may qualify to enroll outside open enrollment if you experience a qualifying life event, usually giving you about 60 days to act. Common examples:
- Losing other health coverage, such as through a job or a parent's plan. See [lost coverage options](/lost-health-coverage).
- Moving to a new area with different plan options.
- Getting married or divorced, depending on circumstances.
- Having or adopting a child.
- Changes in household income that make you newly eligible for certain help or for Medicaid.

You typically need to show documents proving the event. Failing to provide proof can end your coverage, so keep records.

!callout **Not a qualifying event:** simply deciding you want coverage after the deadline. If that is your situation, ask about Medicaid eligibility, which is not tied to open enrollment, and about other options.

{cta(("Not sure if you qualify to enroll now?","We'll check your dates and any special enrollment options for your state.","Check my enrollment options","/#contact"))}

## What about Medicaid?
Medicaid and the Children's Health Insurance Program accept applications throughout the year if you qualify. Eligibility depends on your state, income, and household. If your income is low, applying may be an option even after the open enrollment deadline. See how [Medicaid and ACA decisions work in Virginia](/blog/aca-or-medicaid-virginia-2026) as an example of how states differ.

## How to avoid missing the window
1. Put the enrollment dates on your calendar the moment you confirm them.
2. Update your income estimate before you apply.
3. Gather documents such as proof of income and household information.
4. Compare plans early, not on the last day, when websites are slow.
5. Confirm your plan selection and payment. Selecting a plan is not enough if the first premium is not paid.

## What if you are turning 65?
If you are approaching Medicare, you are in a different system with its own deadlines. Missing Medicare's enrollment windows can lead to penalties. Read our [Turning 65 guide](/turning-65).

## Choosing a plan once you enroll
Compare more than the premium. Look at the deductible, out-of-pocket maximum, drug coverage, and whether your doctors are in network. Our guide to [Bronze, Silver, and Gold plans](/blog/bronze-vs-silver-vs-gold-aca-plans) explains the tiers.

## How we help
Honorbrook is an independent agency licensed in multiple states. We confirm the dates for your state, compare plans, and help with enrollment. Our help is free, because carriers pay us and your premium is the same either way.
"""),
dict(slug="can-i-keep-my-aca-subsidy-if-my-income-changes",kind="health",
title="Can I Keep My ACA Subsidy If My Income Changes During the Year?",ttl="Can I Keep My ACA Subsidy If My Income Changes?",short="ACA Subsidy If Income Changes",em="Income Changes",
desc="Income changed mid-year? Learn how ACA premium tax credits are estimated, reconciled at tax time, and why updating your Marketplace application matters.",
lead="Your subsidy is based on an estimate. If reality turns out different, you settle up on your tax return, so updating early helps.",
faqh="ACA Subsidy & Income Changes FAQ",
faqs=[("Do I have to report income changes to the Marketplace?","You should report significant changes in household income or size so your advance premium tax credit can be adjusted. Doing so can reduce surprises at tax time."),
("What happens if I earned more than I estimated?","When you file your tax return, you reconcile the credits you received against what you were actually eligible for. Depending on the rules in effect, you may owe some or all of the excess back."),
("What if I earned less than I estimated?","You may be eligible for a larger credit, which can come as a refund or reduced tax when you reconcile, and you may qualify for more help during the year by updating your application.")],
rel=REL_H,
body=f"""
One of the biggest worries for people on Marketplace plans with subsidies is what happens if their income changes. Freelancers, commission earners, seasonal workers, and anyone who changes jobs mid-year all face it. The short version: your monthly subsidy is based on an estimate, and the true-up happens when you file taxes. Understanding that process helps you avoid unpleasant surprises.

{NOTE}

## How the subsidy is calculated
When you apply for a Marketplace plan, you estimate your household income for the coming year. Based on that estimate, your household size, and local plan prices, the Marketplace determines whether you qualify for a premium tax credit and how much. You can take the credit in advance, lowering your monthly premium, or claim it all at tax time.

The amount is not locked in. It is an estimate of what you should receive.

## What happens at tax time
When you file your tax return, you reconcile the advance credit you received with the credit you were actually entitled to based on your real income. The result can go in either direction:
- **If your actual income was higher than estimated,** you may have received too much credit and may need to repay some of it. Repayment rules depend on current law and have changed in recent years, so confirm the current rules.
- **If your actual income was lower,** you may qualify for a bigger credit and receive the difference as a refund or reduced tax.

!callout **Do not guess.** If your income is hard to predict, it can help to estimate carefully, update during the year, and talk to a tax professional about the reconciliation process.

## Why updating during the year helps
Reporting changes lets the Marketplace adjust your monthly credit closer to reality. That reduces the risk of a big repayment, or lets you capture more help sooner if your income dropped. You may want to update when:
- You change jobs or get a raise or bonus.
- You lose your job or work fewer hours.
- Your business income looks very different from your forecast.
- A household member joins or leaves.
- You start receiving unemployment, Social Security, or other income.

{cta(("Income uncertain? Let's build a realistic estimate","We help you model a conservative, realistic, and optimistic scenario so your subsidy fits your year.","Talk to a licensed agent","/#contact"))}

## Special situations
- **Self-employed.** Your income may vary month to month. Build your estimate from recent history and expected contracts. See [self-employed health insurance options](/blog/self-employed-health-insurance-aca-ichra-what-to-know).
- **Job loss.** If you lost your job, your estimate for the year should reflect wages before the loss, any severance, and unemployment benefits. Learn about [options after losing job coverage](/blog/lost-your-job-coverage-your-health-insurance-options).
- **Marriage or divorce.** Household size and filing status change the calculation.
- **Medicaid eligibility.** A significant drop in income may make you eligible for Medicaid in some states, which has its own rules.

## A practical approach to estimating
1. Start with what you earned last year and adjust for known changes.
2. Add expected bonuses, side income, and investment income.
3. Subtract only deductions that apply to the income calculation used by the Marketplace.
4. If your income is uncertain, consider planning for the middle of your range and update as the year unfolds.
5. Keep documentation of your income changes.

## Choosing a plan when income is uncertain
If repaying a subsidy would cause hardship, you can choose to take less of the credit in advance and claim the rest at tax time. This reduces the chance of owing but lowers your monthly savings. Talk through the trade-off with an advisor.

## How we help
Honorbrook is an independent agency. We help you compare plans, understand how subsidies work, and update your application when life changes. We do not provide tax advice, so involve a tax professional for the reconciliation process.
"""),
dict(slug="deductible-vs-out-of-pocket-maximum-explained",kind="health",
title="Deductible vs. Out-of-Pocket Maximum: A Plain-English Example",ttl="Deductible vs. Out-of-Pocket Maximum Explained",short="Deductible vs. Out-of-Pocket Max",em="Plain-English Example",
desc="Deductible vs. out-of-pocket maximum explained with a simple example. Learn what each term means, how copays and coinsurance fit, and how to compare plans.",
lead="Two terms that sound alike do very different jobs. Here is a worked example with made-up numbers to make it click.",
faqh="Deductible & Out-of-Pocket Max FAQ",
faqs=[("What is the difference between a deductible and an out-of-pocket maximum?","The deductible is what you pay before the plan starts sharing costs for many services. The out-of-pocket maximum is the most you pay in a year for covered in-network care, after which the plan pays 100 percent of covered services."),
("Do premiums count toward the out-of-pocket maximum?","No. Monthly premiums, out-of-network costs, and non-covered services generally do not count toward the out-of-pocket maximum."),
("Does every service count toward my deductible?","Not always. Some services, such as certain preventive care, may be covered without applying to the deductible, and some plans have copays that apply before the deductible is met.")],
rel=REL_H,
body=f"""
Few insurance terms cause more confusion than deductible and out-of-pocket maximum. They sound similar, they both involve what you pay, and plans mix them with copays and coinsurance. A quick example makes the difference clear. All numbers below are made up for illustration and are not real plan prices.

## The vocabulary, in one place
- **Premium.** What you pay each month to keep the plan active, whether or not you use care.
- **Deductible.** The amount you pay yourself for covered services before the plan begins to share the cost for many services.
- **Copay.** A flat fee for a specific service, such as a doctor visit.
- **Coinsurance.** Your percentage share of a covered cost after the deductible, for example 20 percent.
- **Out-of-pocket maximum.** The most you can pay in a plan year for covered, in-network care. After you hit it, the plan generally pays 100 percent of covered in-network services for the rest of the year.

## A worked example (hypothetical numbers)
Imagine a plan with a $3,000 deductible, 20 percent coinsurance, and a $7,000 out-of-pocket maximum. Suppose you have surgery with covered, in-network charges of $30,000.
1. **You pay the deductible first:** $3,000. Remaining bill: $27,000.
2. **Coinsurance applies to the rest:** 20 percent of $27,000 is $5,400.
3. **Add them up:** $3,000 plus $5,400 is $8,400, which is above the $7,000 maximum.
4. **The maximum caps your cost:** you pay $7,000 and the plan covers the rest.

If the bill had been $10,000 instead, you would pay $3,000 plus 20 percent of $7,000, which is $1,400, for a total of $4,400, below the maximum.

!callout **Key point:** the out-of-pocket maximum is your safety net in a bad year. The deductible is your starting cost in a typical year.

## What does and does not count
Generally:
- **Counts toward the maximum:** deductibles, copays, and coinsurance for covered in-network care.
- **Does not count:** monthly premiums, out-of-network costs beyond what the plan allows, and services the plan does not cover.

Plans differ, so read the summary of benefits and coverage for the exact rules. Some plans have separate deductibles for medical and prescriptions, or for individuals versus families.

{cta(("Want help comparing real plans?","We'll show premiums, deductibles, and out-of-pocket maximums side by side for your household.","Compare plans for free","/#contact"))}

## Why this matters when choosing a plan
Plan tiers trade premium against cost-sharing. A Bronze plan usually has the lowest premium and highest deductible. A Gold plan usually has a higher premium and lower deductible. Which is better depends on how much care you expect and how much risk you can absorb. Our [Bronze, Silver, and Gold guide](/blog/bronze-vs-silver-vs-gold-aca-plans) walks through the trade-offs.

## Family plans: embedded vs. aggregate
Family coverage can have an individual deductible and a family deductible. In an embedded structure, one person can meet the individual amount and trigger coverage for themselves. In an aggregate structure, the family deductible must be met first for anyone to get coverage. The details affect families with one high-cost member, so ask which applies.

## Tips for avoiding surprises
1. Always check that your doctors and hospitals are in network.
2. Know your deductible and maximum before scheduling non-urgent care.
3. Use preventive services, which many plans cover without cost-sharing.
4. Ask for estimates before procedures.
5. Keep track of what you have paid toward the deductible.
6. Consider an HSA if you have a qualifying high-deductible plan and want to save for these costs.

## Medicare uses these ideas too
Original Medicare has deductibles and coinsurance with no overall cap, while Medicare Advantage plans include an annual out-of-pocket maximum. If you are approaching 65, see the [Medicare Parts explained](/blog/medicare-parts-a-b-c-d-explained).

## How we help
Honorbrook is an independent agency. We explain the numbers on any plan in plain English and compare options at your address. Our help is free because carriers pay us and your premium is the same either way.
"""),
dict(slug="hmo-vs-ppo-vs-epo-which-health-plan-type-is-right",kind="health",
title="HMO vs. PPO vs. EPO: Which Health Plan Type Is Right for My Family?",ttl="HMO vs. PPO vs. EPO: Which Health Plan Is Right?",short="HMO vs. PPO vs. EPO",em="Family",
desc="HMO, PPO or EPO? Compare how each health plan type handles networks, referrals and out-of-network care, and which tends to fit your family's needs.",
lead="The letters describe how you access care. Choosing the wrong type can mean surprise bills or restricted choices.",
faqh="HMO vs. PPO vs. EPO FAQ",
faqs=[("What is the main difference between an HMO and a PPO?","HMOs generally require you to use a network and choose a primary care doctor who coordinates referrals, while PPOs offer more flexibility to see specialists and out-of-network providers, usually at a higher cost."),
("What is an EPO?","An EPO, or exclusive provider organization, typically does not cover out-of-network care except in emergencies, but often does not require referrals to see in-network specialists."),
("Which plan type is cheapest?","HMOs and EPOs often have lower premiums than PPOs, but pricing varies by insurer, county, and plan tier, so compare total costs and not only the premium.")],
rel=REL_H,
body=f"""
When you compare health plans, the plan type is as important as the price. HMO, PPO, and EPO describe the rules for which doctors you can see and whether you need a referral. For a family, the right choice can mean easy access to care or a string of frustrations. Here is a clear comparison, with a few questions to help you decide.

## HMO: Health Maintenance Organization
An HMO is generally built around a defined network of doctors and hospitals.
- You usually choose a primary care provider (PCP).
- You typically need a referral from your PCP to see a specialist.
- Care outside the network is generally not covered except in emergencies.
- Premiums and out-of-pocket costs are often lower.

HMOs tend to suit people who are comfortable with a defined network, like coordinated care, and want predictable costs.

## PPO: Preferred Provider Organization
A PPO gives you more freedom.
- You can usually see specialists without a referral.
- You can see out-of-network providers, though you pay more.
- You often pay higher premiums for that flexibility.
- You may have a separate, higher deductible for out-of-network care.

PPOs tend to suit people who want broad choice, see specialists often, or travel and need coverage in different areas.

## EPO: Exclusive Provider Organization
An EPO sits in between.
- It uses a network like an HMO, with no out-of-network coverage except emergencies.
- It usually does not require referrals to see in-network specialists.
- Premiums are often moderate.

EPOs can fit people who want fewer rules about referrals but are happy to stay in the network.

!callout **POS plans** (point of service) blend HMO and PPO features: you choose a PCP and need referrals, but you may have some out-of-network coverage. Ask which type you are looking at before you compare prices.

## Side-by-side summary
| What to compare | HMO | PPO | EPO |
|---|---|---|---|
| Referrals to see specialists | Usually required | Usually not required | Usually not required |
| Out-of-network coverage | Generally emergencies only | Yes, at higher cost | Generally emergencies only |
| Premium | Often lower | Often higher | Often in between |
| Flexibility | Lower | Higher | Medium |

## Questions that help families decide
1. **Which doctors do you want to keep?** Check each in the plan's directory.
2. **Does anyone need frequent specialist care?** A PPO or EPO avoids referral steps.
3. **Do you or your children live or study away from home?** Network coverage may not travel.
4. **How much do you value the lowest premium?** HMOs often win on cost.
5. **Do you have children's hospitals or specialists you want in network?**
6. **What happens in an emergency out of town?** Emergencies are generally covered, but ask how.

{cta(("Let's check your doctors against real networks","We'll look up your family's doctors and hospitals plan by plan so you pick with confidence.","Check my doctors","/#contact"))}

## The hidden cost of the wrong type
A low premium plan with a narrow network can cost more if your preferred doctors are out of network. Similarly, a PPO with a high premium may be more than you need if you rarely use care. Weigh premium, deductible, out-of-pocket maximum, and network together. Our guide to [deductibles and out-of-pocket maximums](/blog/deductible-vs-out-of-pocket-maximum-explained) explains the cost side.

## Plan type and metal tier are separate choices
Plan type (HMO, PPO, EPO) describes access. Metal tier (Bronze, Silver, Gold, Platinum) describes cost-sharing. You can find an HMO in any tier and a PPO in any tier, depending on what is available. See [Bronze vs. Silver vs. Gold](/blog/bronze-vs-silver-vs-gold-aca-plans).

## For small business owners
If you are comparing options for employees, plan type affects how satisfied your team is. See our guide to [small business health insurance options](/blog/small-business-health-insurance-group-plans-vs-shop-vs-ichra).

## How we help
Honorbrook is an independent agency. We compare plan types across multiple carriers, check your doctors and hospitals, and explain the trade-offs in plain English. Our help costs you nothing, because carriers pay us and your premium is the same either way.
"""),
]
