import importlib.util
def _imp(n):
    import os; sp=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),n+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
_h=_imp('posts_3'); cta=_h.cta; REL_H=_h.REL_H; NOTE=_h.NOTE
REL_B=[("Group Health & SHOP","Small-business health plans.","/group-health-insurance-shop"),("ICHRA","Employer-funded individual coverage.","/ichra"),("Small-Business Benefits","Plans for owners and teams.","/small-business-employee-benefits")]
POSTS=[
dict(slug="do-my-kids-need-their-own-health-insurance-family-glitch",kind="health",
title="Do I Need Health Insurance for My Kids If I'm on a Spouse's Plan? The Family Glitch Explained",ttl="Kids on a Spouse's Plan: The Family Glitch Explained",short="Kids on a Spouse's Plan",em="Family Glitch",
desc="Can your kids get Marketplace subsidies if a spouse's job plan is too expensive for the family? Learn how the family glitch worked and what changed.",
lead="Yes, children need coverage, and where they get it depends on what the job plan costs for the whole family, not just the employee.",
faqh="Kids & Spouse's Plan FAQ",
faqs=[("Do my children need their own health insurance policy?","Children need health coverage, but it can come from a parent's employer plan, a Marketplace plan, Medicaid, or CHIP. They do not need a separate policy if they are covered under a plan that includes them."),
("What was the family glitch?","Before federal rules changed, affordability of employer coverage was judged only by the employee-only premium, which could leave families unable to get Marketplace subsidies even when adding family members made the job plan very expensive. Rules since 2023 look at the cost of family coverage for family members."),
("Can my kids qualify for Medicaid or CHIP if I have a job plan?","Possibly. Eligibility depends on your state and household income, and children can sometimes qualify even when parents have employer coverage. Check your state's rules.")],
rel=REL_H,
body=f"""
Many families have one spouse with job-based insurance and a long-running assumption that everyone should be on it. Then the paycheck deductions for adding the kids turn out to be huge, and the question appears: do we have other options? The answer has changed in recent years. Here is how it works in plain English, with the usual note that subsidy and eligibility rules can change.

{NOTE}

## First, do kids need their own policy?
Children need coverage, but not necessarily their own separate policy. The common sources are:
- **A parent's employer plan,** adding children as dependents.
- **A Marketplace plan** for the child alone or for the whole family.
- **Medicaid or CHIP,** depending on state and household income.
- **A plan through the other parent,** if parents live apart and a court order applies.

Dependents can generally stay on a parent's plan until age 26 under federal rules, whether or not they live at home or are students.

## What the family glitch was
Marketplace premium tax credits are available only if you are not offered "affordable" employer coverage. Under the old approach, affordability was measured by the cost of the employee-only plan. If that was under the affordability threshold, the whole family was treated as having affordable coverage, even if adding a spouse and children made the premium far higher than the threshold. The result was that family members could be shut out of subsidies. People called this the family glitch.

## What changed
A federal rule that took effect for 2023 changed the test for family members. Now, affordability for a spouse and children is generally measured by the cost of the family plan, not just the employee-only plan. That means family members in households where the job's family coverage is expensive may now qualify for Marketplace subsidies, while the employee may still be treated as having affordable coverage under the employee-only test. Because rules and thresholds change, confirm the current numbers each year.

!callout **Practical effect:** a household might keep the employee on the job plan and put the spouse and children on a subsidized Marketplace plan, if the family-plan cost is too high under the current test and income qualifies.

{cta()}

## How to compare your options
1. **Get the family cost from HR.** Ask for the employee-only premium and the premium for employee plus spouse and children, plus the plan's deductible and network.
2. **Estimate your household income** for the year.
3. **Price Marketplace plans** for the people you are considering moving, with subsidies applied. Our guide to [what health insurance costs without a job](/blog/how-much-does-health-insurance-cost-without-a-job) explains the pricing factors.
4. **Compare total yearly cost,** not just premiums. See [deductibles and out-of-pocket maximums](/blog/deductible-vs-out-of-pocket-maximum-explained).
5. **Check networks** for the pediatrician and hospital your kids use. See [HMO vs. PPO vs. EPO](/blog/hmo-vs-ppo-vs-epo-which-health-plan-type-is-right).

## Things that can complicate it
- **Mixed coverage.** Splitting a family across plans can mean separate deductibles and out-of-pocket maximums.
- **Enrollment timing.** You usually need Open Enrollment or a qualifying life event to change coverage. If your employer plan has a waiting period or an open enrollment window, plan around it.
- **Income swings.** A subsidy is based on an estimate, and mistakes can mean repayment. Read [how income changes affect your subsidy](/blog/can-i-keep-my-aca-subsidy-if-my-income-changes).
- **Medicaid and CHIP.** Children can qualify at higher income levels than adults in many states, so check even if you earn a good salary.
- **Waiving the job plan.** You may need to decline employer coverage for the family in writing, and that choice may limit when you can rejoin.

## A simple example (hypothetical)
Imagine a job plan that costs a modest amount for the employee alone, but a much higher amount to add a spouse and two children, with a high deductible. The family's household income is within the range that earns Marketplace subsidies. A subsidized Silver plan for the spouse and kids could cost less than adding them to the job plan and might have lower cost-sharing. Run the numbers for your own household because every case differs.

## When the job plan is still the better value
The employer plan may win if your employer pays a large share of family premiums, the network fits your doctors, or the Marketplace plans in your area have narrow networks. Employer contributions are a valuable benefit that you do not get on the Marketplace, so compare carefully.

## How we help
Honorbrook is an independent agency. We compare your employer's cost against Marketplace and Medicaid options for your family and explain the trade-offs. Our help is free because carriers pay us and your premium is the same either way.
"""),
dict(slug="how-small-businesses-offer-health-insurance-with-2-to-10-employees",kind="health",
title="How Do Small Businesses Offer Health Insurance With Just 2 to 10 Employees?",ttl="Health Insurance for a Business With 2 to 10 Employees",short="Health Insurance for 2-10 Employees",em="2 to 10 Employees",
desc="Offering health insurance with 2 to 10 employees? Compare group plans, SHOP, ICHRA and QSEHRA, plus participation and contribution rules.",
lead="You have more options than most owners realize, and the right one depends on your budget, your team, and how much risk you want.",
faqh="Small Business Health Insurance FAQ",
faqs=[("Can a business with only two employees offer group health insurance?","In many states a group generally needs at least one or two common-law employees besides the owner or owner's spouse, though rules vary by state and insurer, so check with an agent."),
("What if my employees do not want to join the group plan?","Group plans often have participation and employer-contribution requirements. If too few eligible employees enroll, the insurer may decline or delay the group, so planning ahead helps."),
("Is an ICHRA a good fit for a very small business?","Often yes, because you set a monthly allowance and employees choose individual plans, which avoids participation minimums. It is different from group coverage, so compare both.")],
rel=REL_B,
body=f"""
Offering health insurance can help you attract and keep good people, but when you have only a handful of employees the options and rules can feel confusing. The good news is that very small businesses have several workable paths. This guide explains each in plain English, with the key rules that usually decide which one fits.

## Option 1: Traditional small-group health plan
This is the classic employer plan. You pick a plan (or a few), the employer pays part of the premium, and employees pay the rest. Common features:
- **Eligibility.** Most states require at least one or two employees who are not the owner or owner's spouse. Rules differ, so ask before you assume you qualify.
- **Participation.** Insurers often require a minimum share of eligible employees to enroll, unless they have other coverage.
- **Employer contribution.** Insurers commonly require the employer to pay a minimum share of employee-only premium.
- **Rating.** Premiums are set using the group's demographics, location, and plan choice, and generally cannot be based on health status.

This option works well when you want a traditional plan that employees understand.

## Option 2: SHOP Marketplace coverage
The Small Business Health Options Program (SHOP) is a Marketplace for small employers, and in some states you can enroll year-round. Availability and structure differ by state. Read more in [group plans vs. SHOP vs. ICHRA](/blog/small-business-health-insurance-group-plans-vs-shop-vs-ichra). SHOP may also connect to the [Small Business Health Care Tax Credit](/blog/the-small-business-health-care-tax-credit-do-you-qualify) if you qualify.

## Option 3: ICHRA
An individual coverage health reimbursement arrangement lets you give employees a monthly allowance to buy their own individual plans. Key points:
- You set the allowance and can vary it by employee class within IRS rules.
- Employees choose plans that fit their families and doctors.
- There are generally no group participation minimums.
- It can make budgeting predictable.

Learn more in our [ICHRA guide for small businesses](/blog/what-is-an-ichra-guide-for-small-businesses) and the [5-step setup guide](/blog/how-to-set-up-an-ichra-in-5-steps).

## Option 4: QSEHRA
A qualified small employer HRA is designed for employers with fewer than 50 full-time equivalent employees that do not offer group coverage. The employer reimburses employees tax-free for qualifying medical costs up to a yearly limit set by the IRS. It is simpler than ICHRA in some ways and more limited in others, so compare them if you qualify.

!callout **Owner-only businesses** (no employees other than the owner and spouse) generally cannot buy a standard small-group plan. They typically look at individual coverage, and self-employed health options. See [self-employed health insurance](/blog/self-employed-health-insurance-aca-ichra-what-to-know).

{cta(("Not sure which structure fits your team?","We'll compare group, SHOP, and ICHRA costs for your employees and location — free.","Get my free business benefits review","/#contact"))}

## How to decide
Ask yourself five questions:
1. **Budget:** How much can you contribute each month, and do you want that number to be fixed?
2. **Team:** Do employees live in the same area, and are their health needs similar?
3. **Simplicity:** Do you want one plan everyone shares or flexibility for each person?
4. **Participation:** Would some employees decline because they have a spouse's plan?
5. **Growth:** Do you expect to add staff soon?

If you want a single shared plan and employees mostly want it, small-group often fits. If your team is spread out or has varied needs, ICHRA's flexibility can be attractive.

## Compliance basics
- Most employers with fewer than 50 full-time equivalent employees are not required by federal law to offer coverage, but state rules and tax benefits vary.
- Employer contributions are generally deductible business expenses; consult your accountant.
- Notice, nondiscrimination, and reporting rules differ by structure.
- Employee classification matters, including part-time workers and owners.

## Steps to get started
1. List your employees, their ages, and ZIP codes.
2. Decide the monthly amount you can afford.
3. Ask an agent to price group, SHOP, and ICHRA options.
4. Check participation and contribution rules for the group option.
5. Choose, communicate the benefit clearly, and set enrollment dates.

## Common mistakes
- Assuming the cheapest premium is the best value for your team.
- Forgetting that group plans can require a minimum participation level.
- Ignoring tax credits you may qualify for.
- Starting too late before a desired coverage date.

## How we help
We are an independent agency and we compare small-group, SHOP, ICHRA, and QSEHRA options from multiple carriers. We explain the rules, but your accountant or attorney should confirm tax and compliance details. Our help costs you nothing because carriers pay us.
"""),
dict(slug="can-i-deduct-health-insurance-premiums-if-self-employed",kind="health",
title="Can I Deduct Health Insurance Premiums If I'm Self-Employed?",ttl="Can Self-Employed People Deduct Health Insurance?",short="Self-Employed Premium Deduction",em="Deduct",
desc="Self-employed? Learn how the health insurance deduction generally works, who qualifies, the net-profit limit, and how it interacts with ACA subsidies.",
lead="Often yes, and it is taken on your personal return, not as a business expense. A few rules decide whether you qualify.",
faqh="Self-Employed Health Deduction FAQ",
faqs=[("Is the self-employed health insurance deduction an itemized deduction?","It is generally an adjustment to income taken on your personal tax return, so you can usually claim it without itemizing, subject to eligibility rules."),
("Is there a limit on the deduction?","Generally the deduction cannot exceed your net profit from the business, and you generally cannot claim it for months when you were eligible for subsidized coverage through an employer or a spouse's employer."),
("Does this affect my ACA premium tax credit?","It can. The deduction and the premium tax credit can interact, so work with a tax professional to calculate them correctly.")],
rel=[("Self-Employed Health Insurance","Options for solo owners.","/self-employed-health-insurance"),("ACA Health Plans","Marketplace plans and subsidies.","/aca-health-insurance"),("ICHRA","Employer-funded individual coverage.","/ichra")],
body=f"""
If you work for yourself, you pay for health insurance from your own pocket instead of through a company plan. The tax code gives many self-employed people a break on those premiums, but the rules have conditions. This guide explains the basics in plain English. It is general information, not tax advice, so confirm details with a tax professional.

## What the deduction is
The self-employed health insurance deduction lets eligible people deduct premiums they pay for medical insurance for themselves, a spouse, and dependents. It is generally claimed as an adjustment to income on your personal return, not as a business expense on Schedule C. Because it is an adjustment, it can lower your adjusted gross income, which can affect other tax calculations.

## Who generally qualifies
- Sole proprietors, partners, and certain S-corporation owners who meet the rules.
- People with a trade or business that earns a net profit.
- Those whose plan is established under the business or, in some cases, personally and linked to the business according to IRS rules.

Rules for S-corporation shareholders are more specific, including how premiums are reported on the owner's wages, so those owners should work with a professional.

## What premiums may be included
Depending on circumstances, deductible premiums can include:
- Medical, dental, and qualified vision insurance.
- Medicare premiums, including Part B, Part D, and Medigap or Advantage premiums.
- Certain qualified long-term care premiums, subject to age-based limits.

Coverage for yourself, your spouse, and your dependents, including children under 27 at the end of the year, can qualify.

## The key limits
1. **Net profit limit.** The deduction generally cannot exceed your net earnings from the business. If your business has a loss, you may not be able to deduct.
2. **Other coverage.** You generally cannot deduct premiums for any month when you were eligible to participate in a subsidized plan through your own or your spouse's employer.
3. **The business must be real.** The deduction connects to a trade or business that earns income.

!callout **Interaction with subsidies:** if you take Marketplace premium tax credits, the amount of the deduction and the credit depend on each other, which creates a circular calculation. Use a tax professional or software that handles it correctly.

{cta(("Want plans priced before tax season?","We'll compare ACA, Medicare, and ICHRA options for your income and give you the premium figures your accountant needs.","Get my free quote","/#contact"))}

## How it helps in practice
Suppose a self-employed person pays a monthly premium and has enough net profit. The deduction reduces taxable income by the qualifying premiums, which can reduce both income tax and, in some cases, other tax calculations. Because it is an adjustment to income, you do not need to itemize to benefit. The savings depend on your tax bracket, so a precise number requires your actual return.

## Records to keep
- Premium statements or invoices for each month.
- Proof of who was covered.
- Records showing months you were or were not eligible for employer coverage.
- Form 1095-A if you had Marketplace coverage.
- Your business income and expense records.

## Ways to organize your coverage
- **Individual Marketplace plan.** Many self-employed people use ACA plans, sometimes with subsidies. See [self-employed health insurance options](/blog/self-employed-health-insurance-aca-ichra-what-to-know).
- **Spouse's employer plan.** If eligible, it may limit your deduction.
- **ICHRA from your own corporation.** If you have W-2 employees, an ICHRA may be possible. Details are technical.
- **Medicare.** If you are 65 or older, Medicare premiums may be deductible too. See [Medicare Parts explained](/blog/medicare-parts-a-b-c-d-explained).

## Common mistakes
- Claiming the deduction in a month you could have joined a spouse's employer plan.
- Ignoring the net-profit limit.
- Forgetting that the deduction and the premium tax credit interact.
- Not keeping premium records.
- Treating it as a Schedule C expense when it is an adjustment on the personal return.

## Planning tip
Because the deduction depends on your annual profit, a big drop in income can change both the deduction and your subsidy. If your income is variable, check your estimates mid-year. Our guide on [subsidies and changing income](/blog/can-i-keep-my-aca-subsidy-if-my-income-changes) walks through the process.

## How we help
Honorbrook is an independent agency. We compare health plans for self-employed people and explain how premiums and subsidies work. We do not provide tax advice, so your CPA should confirm your deduction. Our help is free because carriers pay us.
"""),
dict(slug="what-is-a-health-sharing-plan-is-it-real-insurance",kind="health",
title="What Is a Health Sharing Plan, and Is It Real Insurance?",ttl="Health Sharing Plans: Is It Real Insurance?",short="Health Sharing Plans",em="Real Insurance",
desc="Health sharing ministries aren't insurance. Learn how they work, what they typically exclude, and the risks to weigh against ACA and other coverage.",
lead="Health sharing plans are not insurance. That difference matters most on the day you have a big claim.",
faqh="Health Sharing Plan FAQ",
faqs=[("Is a health sharing plan the same as health insurance?","No. Health sharing arrangements are generally not insurance, are not regulated the same way, and typically do not guarantee that your medical bills will be paid."),
("Do health sharing plans cover pre-existing conditions?","Many limit or exclude pre-existing conditions, at least for a period, which is a major difference from ACA-compliant plans that cannot deny coverage for them."),
("Does a health sharing plan satisfy ACA requirements?","There is no federal individual mandate penalty now, but sharing plans generally do not count as ACA minimum essential coverage, and some states have their own rules, so check before relying on one.")],
rel=REL_H,
body=f"""
When health insurance premiums look steep, health sharing plans can look like a bargain. They advertise lower monthly amounts and a community feel. But they work very differently from insurance, and people are sometimes surprised by what that means. This guide explains the differences so you can compare with eyes open.

## How health sharing works
In a health sharing arrangement, members pay a monthly contribution into a pool. When a member has an eligible medical expense, other members' contributions are directed to help pay it, according to the program's guidelines. Many are organized as faith-based nonprofits and ask members to follow certain lifestyle or belief statements.

The key words are "guidelines" and "sharing." The program describes what it will consider for sharing. It is not a contract promising payment in the way an insurance policy is.

## Why it is not insurance
Differences usually include:
- **No guarantee of payment.** Most programs state that sharing is voluntary and that they do not promise to pay bills.
- **Limited regulation.** Insurance companies are regulated by state insurance departments, with rules on solvency, claims handling, and consumer protections. Health sharing programs are generally not regulated as insurance, though some states have specific laws about them.
- **No ACA consumer protections.** Rules requiring coverage of essential health benefits, limits on out-of-pocket costs, and protection for pre-existing conditions generally do not apply.
- **No premium tax credits.** Subsidies are for Marketplace plans, not sharing arrangements.

!callout **Ask this question:** "If my bills are not shared, what can I do?" With insurance, you have appeal rights and state regulators. With sharing programs, your recourse may be limited to the program's own process.

## What sharing plans often exclude or limit
Always read the guidelines, but common limits include:
- Pre-existing conditions, sometimes for a waiting period or permanently.
- Certain services such as some mental health care, maternity, or preventive care.
- Care related to behaviors the program does not support.
- Charges above what the program deems reasonable.
- Annual or lifetime sharing limits.

Requirements such as negotiating bills or submitting through the program's process can also affect how much is shared.

## What it can cost compared with insurance
Monthly amounts can be lower than comparable ACA premiums, particularly for people who do not qualify for subsidies. But the comparison is not apples to apples. Lower monthly cost can come with more financial risk after a major illness or accident. If you qualify for premium tax credits, an ACA plan may cost less than you think. See [what health insurance costs without a job](/blog/how-much-does-health-insurance-cost-without-a-job).

{cta(("Compare before you decide","We'll show you real ACA prices with subsidies for your household so you can compare against a sharing plan fairly.","Get my free comparison","/#contact"))}

## Who sometimes considers sharing plans
- Healthy people who do not qualify for subsidies and want lower monthly costs.
- Individuals who value a faith-based community model.
- People willing to accept the financial risk of non-guaranteed payment.

## Who should be cautious
- Anyone with ongoing health needs or pre-existing conditions.
- Families expecting a baby or planning major care.
- People who cannot afford a large unpaid medical bill.
- Anyone who would be unable to enroll in an ACA plan outside open enrollment if the sharing plan fails them.

## Other lower-cost alternatives to compare
1. **ACA Bronze plan** with a high deductible. See [Bronze, Silver, and Gold plans](/blog/bronze-vs-silver-vs-gold-aca-plans).
2. **Catastrophic plan,** for those who qualify.
3. **Medicaid or CHIP,** if you meet income rules.
4. **ICHRA,** if your employer offers it.
5. **Short-term plans,** which have their own limits. See [short-term health insurance](/blog/short-term-health-insurance-when-it-works-and-when-it-doesnt).

## Questions to ask any sharing program
- Is there any guarantee of payment?
- How do you treat pre-existing conditions?
- What are the annual and lifetime limits?
- What happens if I have a large claim?
- How do I appeal a denied request?
- How is the program regulated in my state?

## How we help
Honorbrook is an independent insurance agency. We sell regulated insurance, not sharing plans, and we are happy to show you how ACA coverage compares at your income and address. Our help is free because carriers pay us.
"""),
dict(slug="short-term-health-insurance-when-it-works-and-when-it-doesnt",kind="health",
title="Short-Term Health Insurance: When It Works and When It Doesn't",ttl="Short-Term Health Insurance: When It Works",short="Short-Term Health Insurance",em="When It Works",
desc="Short-term health insurance can bridge a gap but isn't ACA coverage. Learn what it excludes, how it differs by state, and safer alternatives.",
lead="It can be a reasonable bridge in specific situations, but it is not a substitute for a major medical plan.",
faqh="Short-Term Health Insurance FAQ",
faqs=[("Does short-term health insurance cover pre-existing conditions?","Generally no. Short-term plans commonly use medical underwriting and exclude pre-existing conditions, and may deny coverage based on health history."),
("Is short-term insurance allowed in every state?","No. Some states restrict or ban short-term plans, and others limit how long they can last. Availability and duration vary by state and have changed over time."),
("Can I use short-term insurance as a long-term solution?","It is not designed for that. Plans are temporary, may not cover essential benefits, and may not be renewable, so they are a poor substitute for comprehensive coverage.")],
rel=REL_H,
body=f"""
Short-term health insurance gets a lot of attention because the monthly premium is often lower than a Marketplace plan. For some people in specific circumstances, it can be a sensible stopgap. For many others, it is a trap that looks like coverage until the first big claim. Here is how to tell the difference.

## What short-term health insurance is
Short-term medical plans are temporary policies meant to bridge gaps in coverage, for example between jobs or while waiting for another plan to start. They are not ACA-compliant plans. That means they do not have to follow the ACA's rules, and they differ from Marketplace plans in important ways.

## How it differs from an ACA plan
- **Medical underwriting.** Insurers can ask health questions and deny applicants or exclude conditions.
- **Pre-existing conditions.** Typically excluded.
- **Essential health benefits.** Not required. Many plans exclude maternity, mental health, substance use treatment, or prescription drugs, or have low caps on them.
- **Benefit limits.** Annual or per-condition maximums may apply.
- **Out-of-pocket maximums.** May be high or may not exist in the same way.
- **Duration.** Limited terms; renewal rules vary.
- **No subsidies.** Premium tax credits only apply to Marketplace plans.
- **Not minimum essential coverage.** It may not count if a rule requires qualifying coverage.

## State rules vary a lot
Some states ban or tightly limit short-term plans, others allow them with shorter terms, and federal rules about maximum duration have changed several times. Because of that, whether a plan is available or how long it can last depends on your state. Check current rules for where you live.

!callout **Read the exclusions first.** Before buying, ask for the brochure and read the section on what is not covered. The exclusions tell you more than the benefits summary.

{cta(("Gap in coverage? Check your better options first","You may qualify for a Special Enrollment Period or Medicaid. We'll check before you buy a stopgap.","Check my options","/#contact"))}

## When short-term insurance can make sense
- You expect to have another plan within a few months, such as a new job's coverage that starts after a waiting period.
- You missed Open Enrollment, have no qualifying event, and you are generally healthy.
- You want catastrophic-style protection for a short period and understand the limits.

Even in these cases, compare alternatives. If you lost coverage, you may have a 60-day window to enroll in a Marketplace plan. See [your options after losing job coverage](/blog/lost-your-job-coverage-your-health-insurance-options). COBRA may also make sense if you are mid-treatment.

## When it does not make sense
- You have ongoing health conditions or take regular medications.
- You are planning a pregnancy.
- You need mental health or substance use care.
- You expect to use care frequently.
- You qualify for substantial ACA subsidies or Medicaid.
- You might need the coverage for longer than the term.

## How to compare it with other options
1. **ACA plan with subsidies.** The premium may be lower than you think. Read [what health insurance costs](/blog/how-much-does-health-insurance-cost-without-a-job).
2. **Catastrophic or Bronze plan.** Lower premiums with higher deductibles but protections intact. See [Bronze vs. Silver vs. Gold](/blog/bronze-vs-silver-vs-gold-aca-plans).
3. **Medicaid or CHIP.** Free or low cost for those who qualify.
4. **COBRA.** Keeps your old plan at full price.
5. **A spouse's or parent's plan.**

## Questions to ask before buying
- Does it exclude pre-existing conditions, and how does it define them?
- What is the maximum benefit per year and per condition?
- Are prescriptions, mental health, and maternity covered?
- What is the network, and what happens out of network?
- What are the term and renewal rules in my state?
- Does it count as qualifying coverage for any purpose I care about?

## Warning signs
- Marketing that calls it "full coverage" or "just like ACA."
- Pressure to buy quickly.
- Unclear exclusions.
- A seller who cannot explain the claim process.

## How we help
Honorbrook is an independent agency. We will tell you honestly whether an ACA plan, Medicaid, COBRA, or another option fits better than a stopgap. Our help is free because carriers pay us.
"""),
]
