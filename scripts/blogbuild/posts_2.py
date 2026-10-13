def cta(a=None):
    a=a or ("Want a second opinion before you move retirement money?","Request a no-obligation Retirement Income Review. We explain your options in plain English — no pressure, no promises of returns.","Request my Retirement Income Review","/#contact"); return "!cta "+" | ".join(a)
REL_W=[("Annuities","Fixed, indexed, and single-premium options explained.","/annuities"),("Indexed Universal Life","Permanent coverage with cash value potential.","/indexed-universal-life"),("Life Insurance","Term and permanent protection for your family.","/life-insurance")]
CAV="!callout **Important:** this article is educational, not personalized advice. Annuities and life insurance guarantees depend on the issuing company's claims-paying ability, can carry surrender charges and fees, and are not bank products or investments. Speak with a licensed professional and your tax advisor before moving money."
POSTS=[
dict(slug="what-to-do-with-your-401k-when-you-retire-or-leave-a-job",kind="life",
title="What Should I Do With My 401(k) When I Retire or Leave a Job?",ttl="What to Do With Your 401(k) at Retirement or Job Change",short="What to Do With Your 401(k)",em="401(k)",
desc="Retiring or changing jobs? Learn the four options for your 401(k), the tax traps to avoid, and questions to ask before you roll money anywhere.",
lead="You generally have four choices. Each has trade-offs, and one of them can trigger taxes and penalties if handled badly.",
faqh="401(k) at Retirement FAQ",
faqs=[("Do I have to move my 401(k) when I leave my job?","Not always. Many plans let you leave the money where it is, though some require smaller balances to be moved. Check with your plan administrator."),
("What is the difference between a direct and indirect rollover?","In a direct rollover the money moves from one account to another without you touching it. In an indirect rollover you receive a check, and mandatory tax withholding and a 60-day deadline can create problems, so a direct rollover is usually simpler."),
("Can I withdraw from my 401(k) before 59½ without a penalty?","Sometimes. There are exceptions, such as separation from service at 55 or later from that employer's plan, but many early withdrawals face a 10 percent additional tax plus income tax. Confirm your situation with a tax professional.")],
rel=REL_W,
body=f"""
Leaving a job, or leaving work altogether, often leaves people holding a 401(k) and wondering what to do with it. It may be the largest account you own, and a rushed decision can cost you in taxes, fees, or flexibility. This guide lays out your options in plain English. It is not personalized advice, and your tax advisor should weigh in before you act.

{CAV}

## Option 1: Leave it in your old employer's plan
Many plans allow former employees to keep their balance in place. Reasons to consider this:
- You like the investment choices or low fees.
- You want time to decide without pressure.
- The plan offers features that are hard to replicate elsewhere.

Reasons to be careful: you can no longer contribute, you may have fewer services, and a small balance may be forced out. Keep track of old accounts so they do not get lost.

## Option 2: Roll it into your new employer's plan
If you have a new job, your new plan may accept rollovers. This keeps everything in one place and can simplify required distributions later. Check the new plan's investment options, fees, and whether it accepts rollovers at all.

## Option 3: Roll it into an IRA
A rollover to an IRA gives you wider investment choices and consolidation. It also means you are responsible for managing the account. Fees and services vary across providers. A direct rollover keeps the money tax-deferred, but if it is handled as a check made out to you, the plan may withhold 20 percent for taxes and you must deposit the full amount within 60 days or risk taxes and penalties.

## Option 4: Cash it out
You can take the money, but it is generally taxable as ordinary income, and if you are under 59½ you may owe an additional 10 percent tax unless an exception applies. A large withdrawal can also push you into a higher tax bracket and may raise your Medicare premiums later through income-related adjustments. For most people this is the most expensive option.

## Where annuities can fit in
Some people use part of a rollover to buy an [annuity](/annuities) for guaranteed income, or to add a layer of protection from market swings. An annuity is not a replacement for a plan, and it is not right for everyone. Key points to understand:
- Annuities can have surrender charges if you withdraw too early.
- Fees, riders, and caps vary widely by contract.
- Guarantees depend on the issuing insurer's financial strength.
- Inside an IRA, an annuity does not add extra tax deferral because the IRA is already tax-deferred.

We cover the last point in more detail in [IRA rollover into an annuity: what to ask first](/blog/ira-rollover-into-an-annuity-what-to-ask-first).

{cta()}

## Special rules worth knowing
- **Rule of 55.** If you leave your employer in or after the year you turn 55, you may be able to take penalty-free withdrawals from that employer's 401(k). This usually does not apply to IRAs.
- **Employer stock.** If your 401(k) holds company stock with large gains, special tax treatment may apply. Ask a tax professional before rolling it over.
- **Roth balances.** Roth 401(k) money has different tax rules and should be rolled to a Roth account.
- **Required distributions.** Traditional 401(k) and IRA balances are subject to required minimum distributions later in life. The starting age depends on your birth year.

## Questions to ask before you decide
1. What are the total fees in each choice?
2. What investment options or guarantees does each give me?
3. Do I need access to this money before 59½?
4. How will this affect my taxes this year and in retirement?
5. Is the person recommending it paid by commission, by fee, or both?

## A simple process
1. Gather your statements and plan rules.
2. Decide how much income you will need and when.
3. Compare the four options on cost, flexibility, and protection.
4. Talk to a tax professional about the tax effect.
5. Use a direct transfer if you move the money.

## How we help
Honorbrook is an independent insurance agency. We help people understand whether an annuity or life insurance product has a place in their retirement picture, and we explain the costs and trade-offs. We do not provide investment or tax advice, and you are never obligated to buy anything.
"""),
dict(slug="what-is-a-single-premium-annuity-who-is-it-for",kind="life",
title="What Is a Single-Premium Annuity, and Who Is It Actually For?",ttl="What Is a Single-Premium Annuity?",short="Single-Premium Annuity",em="Single-Premium Annuity",
desc="A single-premium annuity turns a lump sum into guaranteed income or growth. Learn how SPIAs and deferred annuities work, who they suit, and the risks.",
lead="One lump sum in, a stream of payments or tax-deferred growth out. Here is how it works and when it makes sense.",
faqh="Single-Premium Annuity FAQ",
faqs=[("What is a single-premium annuity?","It is an annuity you fund with one lump-sum payment. It can be an immediate annuity that begins paying income right away, or a deferred annuity that grows for a period before payments start."),
("Can I get my money back from a single-premium annuity?","It depends on the contract. Immediate annuities are generally irrevocable once income begins, while deferred annuities often allow limited withdrawals but may charge a surrender fee for early access."),
("Is a single-premium annuity safe?","Guarantees depend on the claims-paying ability of the issuing insurance company. Annuities are not FDIC-insured, and state guaranty associations offer limited protection that varies by state.")],
rel=REL_W,
body=f"""
If you have a lump sum from the sale of a business, an inheritance, a pension payout, or a retirement account, you may hear about single-premium annuities. The name sounds technical, but the idea is simple: you pay one premium and the insurance company agrees, under the contract terms, to pay you income or credit growth. Whether that is a good deal depends on your goals and the specific contract.

{CAV}

## The two main types
Single-premium annuities generally come in two forms:
- **Single-premium immediate annuity (SPIA).** You pay a lump sum and income payments begin soon after, often within a year. Payments can last for life, for a set period, or for the lives of two people.
- **Single-premium deferred annuity.** You pay a lump sum and it grows tax-deferred for a period before you take income or withdrawals. These can be fixed, indexed, or variable (variable annuities are securities and require additional licensing, so we focus here on fixed and indexed types).

## How a SPIA works
You hand the insurer a lump sum, choose a payout structure, and the insurer calculates your payments based on your age, the amount, interest rates, and the option you choose. Common options include:
- Life only: the highest payment, but payments stop at death.
- Life with period certain: payments continue to a beneficiary for a set number of years if you die early.
- Joint and survivor: payments continue for a spouse after the first death.
- Period certain only: payments for a fixed number of years.

Once income begins, a SPIA is typically irreversible. That is the trade-off for the guarantee.

## Who a single-premium annuity may suit
- Someone who wants guaranteed income to cover essential expenses that Social Security and a pension do not meet.
- A retiree who worries about outliving savings and wants a floor of income.
- Someone with a lump sum who wants predictability and is comfortable giving up some flexibility.
- A person who wants to reduce the stress of market swings on a portion of their savings.

## Who it may not suit
- People who may need the full lump sum for emergencies.
- Those who want to leave the full amount to heirs and do not want a payout structure that ends at death.
- Anyone who has not yet built an emergency fund or paid off high-interest debt.
- Buyers who have not compared several carriers and structures.

{cta()}

## Costs and risks to understand
1. **Liquidity.** Immediate annuities are generally not reversible. Deferred annuities often have surrender charges for early withdrawals.
2. **Inflation.** Fixed payments lose purchasing power over time unless you choose an increasing option, which starts lower.
3. **Insurer strength.** Guarantees rely on the company paying. Compare financial strength ratings and understand your state's guaranty association limits.
4. **Taxes.** Rules depend on whether the money is from a qualified account such as an IRA or from after-tax savings. See [how annuities are taxed](/blog/how-are-annuities-taxed).
5. **Opportunity cost.** Money in an annuity is not available for other uses.

## Questions to ask before buying
- What exactly is guaranteed, and for how long?
- What happens if I die early?
- What are the surrender charges and free-withdrawal terms?
- How does this compare to other options such as CDs, bonds, or leaving money invested?
- How is the person recommending it compensated?

## Comparing with a fixed indexed annuity
A [fixed indexed annuity](/blog/what-is-a-fixed-indexed-annuity-fia) is a deferred annuity with growth tied to an index, subject to caps or other limits. It generally aims for protection from market losses with limited upside, whereas a SPIA focuses on income. Both have trade-offs and the right choice depends on your goals.

## How we help
We are an independent agency and we can explain the structures from multiple carriers. We do not provide tax or investment advice, and nothing here is a recommendation for your situation. Request a review if you want to talk through whether an annuity belongs in your plan at all.
"""),
dict(slug="what-is-a-fixed-indexed-annuity-fia",kind="life",
title="What Is a Fixed Indexed Annuity (FIA)? Caps, Participation and Surrender Charges",ttl="What Is a Fixed Indexed Annuity (FIA)?",short="Fixed Indexed Annuity (FIA)",em="Fixed Indexed Annuity",
desc="A fixed indexed annuity credits interest linked to an index with downside protection. Learn how caps, participation rates, spreads and surrender charges work.",
lead="An FIA is not the stock market and it is not a CD. Here is how the crediting rules work and what to question before you buy.",
faqh="Fixed Indexed Annuity FAQ",
faqs=[("Does a fixed indexed annuity lose money when the market falls?","Interest credited is typically linked to an index and cannot go below the contract floor, often zero, in a down year. But fees, rider charges, and withdrawals can reduce your value, and surrender charges can apply."),
("Do I get the full return of the index?","Usually not. Caps, participation rates, and spreads limit how much of an index's gain is credited, and most indexes exclude dividends."),
("Can I take money out of an FIA?","Most contracts allow a limited annual free withdrawal. Withdrawals above that during the surrender period typically incur a surrender charge, and withdrawals before 59½ may face a tax penalty.")],
rel=REL_W,
body=f"""
A fixed indexed annuity, or FIA, is a deferred annuity issued by an insurance company. Your interest is linked to the performance of a market index such as the S&P 500, but your money is not invested in the market. In exchange for giving up some upside, the contract limits losses according to its terms. That sounds attractive, so it deserves careful reading of how the pieces work.

{CAV}

## The basic idea
You deposit money with the insurer. Each contract year, the insurer measures the change in the chosen index and credits interest using a formula. If the index falls, the credited interest is generally zero rather than negative. This is often called a floor. The trade-off is that the credited gain is limited by one or more crediting limits.

## The three limits that matter
- **Cap rate.** The maximum interest you can earn for a period. For illustration only, imagine a hypothetical cap of 5 percent. If the index rose 12 percent, you would be credited 5 percent. If the index fell 10 percent, you would be credited zero.
- **Participation rate.** The percentage of the index gain that counts. With a hypothetical 60 percent participation rate and an index gain of 10 percent, you would be credited 6 percent.
- **Spread (or margin).** A percentage subtracted from the index gain before crediting.

These numbers are set by the insurer and can change, often annually, on non-guaranteed portions. Always ask which are guaranteed for the life of the contract and which can be adjusted.

!callout **Index does not mean dividends.** Most indexes used in annuities are price indexes that exclude dividends, so the credited return will generally differ from what a total-return investment would earn.

## Surrender charges and liquidity
FIAs are designed to be held for a period, commonly several years. If you withdraw more than the free-withdrawal amount during the surrender period, a surrender charge can apply, often declining each year. Withdrawals before age 59½ can also be subject to an additional 10 percent federal tax. This is a long-term product, not a place for emergency money.

## Riders and fees
Some FIAs offer optional income riders that promise a guaranteed lifetime income amount, sometimes with a rider fee. Pay attention to:
- How the rider's income base grows, and that it may differ from the account value.
- The annual rider charge.
- When income can begin and how payments are calculated.
- Whether the rider can be changed or removed.

The income base is often not a cash value you can withdraw, and confusing the two is a common misunderstanding.

{cta()}

## Who an FIA may fit
- Someone near or in retirement who wants some growth potential without direct market losses.
- Savers who are comfortable leaving the money untouched for the surrender period.
- Buyers who value contractual guarantees and understand the limits on upside.

## Who should be cautious
- Anyone who may need the money soon.
- People who expect to capture most of the stock market's gains.
- Buyers who have not read the cap, participation, and spread terms and the surrender schedule.
- Anyone being pressured to move money quickly.

## Tax basics
Growth inside a non-qualified FIA is tax-deferred, but gains are taxed as ordinary income when withdrawn. Qualified money such as an IRA is generally fully taxable on distribution. Read [how annuities are taxed](/blog/how-are-annuities-taxed) and consult your tax professional.

## How an FIA compares
An FIA generally sits between a savings-type product and market investments in risk and reward. It differs from a [single-premium immediate annuity](/blog/what-is-a-single-premium-annuity-who-is-it-for), which focuses on income, and from a CD, which is FDIC-insured and has fixed terms. Each has a different role.

## Questions to ask
1. Which crediting limits are guaranteed and for how long?
2. What is the surrender schedule and free-withdrawal rule?
3. What fees or rider charges apply?
4. What is the insurer's financial strength?
5. How is the recommending agent paid?

## How we help
We are an independent agency. We explain how FIAs from multiple carriers work, in plain English, and we do not promise returns. Request a review if you want a second set of eyes on an illustration before you decide.
"""),
dict(slug="turning-65-with-a-401k-medicare-and-retirement-savings",kind="med",
title="Turning 65 With a 401(k): What to Do About Medicare and Your Savings",ttl="Turning 65 With a 401(k): Medicare and Retirement Savings",short="Turning 65 With a 401(k)",em="401(k)",
desc="Turning 65 and still working or holding a 401(k)? Learn how it affects Medicare timing, HSA contributions, and Medicare premiums from retirement income.",
lead="Your 401(k) and Medicare decisions affect each other more than most people realize. Timing is everything.",
faqh="Turning 65 and 401(k) FAQ",
faqs=[("Do I have to sign up for Medicare at 65 if I still work?","Not always. If you have coverage through a current employer, whether you can delay Part B without a penalty depends on the size of the employer and the type of coverage. Confirm with your benefits office before deciding."),
("Does my 401(k) income affect my Medicare premiums?","It can. Higher income can trigger income-related adjustments to Part B and Part D premiums, based on tax returns from a couple of years earlier."),
("Can I keep contributing to an HSA after 65?","Once you are enrolled in any part of Medicare, you generally cannot contribute to an HSA. Part A coverage can start retroactively, so timing needs care.")],
rel=[("Turning 65 Guide","What to do and when.","/turning-65"),("Annuities","Guaranteed income options for retirement.","/annuities"),("Medicare Annual Enrollment","Dates and rules each fall.","/medicare-annual-enrollment-period")],
body=f"""
Turning 65 is a double milestone for many people. It is the age Medicare eligibility begins, and it is often when retirement planning gets serious. If you have a 401(k) or other retirement savings, your Medicare timing and your money decisions can affect each other. This guide covers the main connections in plain English. It is general information, not tax or financial advice.

## Do you need to sign up for Medicare at 65?
It depends on whether you are still working and what coverage you have.
- **If you are retired or have no employer coverage,** you should generally enroll during your Initial Enrollment Period, a seven-month window around your 65th birthday. Missing it can lead to lifetime late penalties for Part B and Part D.
- **If you still work for an employer with 20 or more employees and have group health coverage through that job,** you may be able to delay Part B without a penalty and enroll later during a Special Enrollment Period.
- **If your employer is small or your coverage is not through current employment,** different rules can apply. Check with your benefits office and Medicare before delaying.

Our [Turning 65 guide](/turning-65) walks through the enrollment windows.

## The HSA catch
Many people with a high-deductible health plan contribute to a Health Savings Account (HSA). Once you enroll in any part of Medicare, you generally cannot contribute to an HSA. Part A can also begin up to six months back when you apply after 65, which can create an unexpected tax problem if you contributed during that period. If you plan to keep contributing, talk to your benefits administrator or tax professional about timing.

## How retirement income affects Medicare premiums
Medicare Part B and Part D premiums can be higher for people with higher income. These income-related adjustments are based on your modified adjusted gross income from a tax return filed a couple of years earlier. Things that can increase it include:
- Large withdrawals from traditional 401(k) or IRA accounts.
- Roth conversions.
- Selling a business or property with large gains.
- Taking a lump-sum pension or rollover distribution that is taxable.

!callout **The takeaway:** a big taxable withdrawal in one year can raise your Medicare premiums two years later. If your income is about to change, ask a tax professional how to time it.

{cta(("Planning around Medicare and retirement income?","We'll coordinate your Medicare enrollment timing and show you retirement income options side by side.","Request my Retirement Income Review","/#contact"))}

## What to do with the 401(k) when you retire
You generally have four options: leave it, roll it to a new employer plan, roll it to an IRA, or take the cash. Read [what to do with your 401(k) when you retire or leave a job](/blog/what-to-do-with-your-401k-when-you-retire-or-leave-a-job) for the full list. At 65 there is one more consideration: required minimum distributions begin later in retirement, so how you structure withdrawals now affects your future taxes and Medicare premiums.

## Where guaranteed income can fit
Some people build a base of income that does not depend on the market, using Social Security, a pension, and in some cases an [annuity](/annuities). Which mix fits depends on your spending needs, health, and how you feel about risk. We can explain how these products work, but a tax professional should weigh in before you move money.

## A simple 65-year-old's checklist
1. Confirm whether you are still covered by an employer plan and how it coordinates with Medicare.
2. Mark your Initial Enrollment Period dates.
3. Decide how to handle your HSA before enrolling.
4. List your doctors and medications so you can compare plans.
5. Estimate your retirement income and how it will be taxed.
6. Review your life insurance and beneficiary designations.

## Medicare plan choices
Once you enroll, you will choose between Original Medicare with a [Medigap plan](/medicare-supplement-medigap) and a [Medicare Advantage plan](/medicare-advantage), plus drug coverage if needed. Our guide on [Advantage vs. Medigap](/blog/medicare-advantage-vs-medigap-2026) helps you think through the choice.

## How we help
Honorbrook is an independent agency. We help with Medicare enrollment timing and explain insurance-based retirement options from multiple carriers. We do not provide tax or investment advice, and our help is free to you because carriers pay us.
"""),
dict(slug="what-is-indexed-universal-life-iul-how-it-works-cost-risks",kind="life",
title="What Is Indexed Universal Life (IUL)? How It Works, What It Costs, and the Risks",ttl="What Is Indexed Universal Life (IUL)?",short="Indexed Universal Life (IUL)",em="Indexed Universal Life",
desc="Indexed universal life (IUL) pairs a death benefit with cash value tied to an index. Learn how it works, what it costs, and the risks to understand first.",
lead="IUL is permanent life insurance with flexible premiums and an index-linked cash value. The marketing is rosy, so here is the full picture.",
faqh="Indexed Universal Life FAQ",
faqs=[("What is indexed universal life insurance?","It is permanent life insurance with a death benefit and a cash value account whose credited interest is linked to an index, subject to caps, participation rates, and a floor. You also pay policy charges."),
("Can an IUL policy lapse?","Yes. If the cash value is not enough to cover the cost of insurance and fees, the policy can lapse, which may cause taxes and loss of coverage. Premium funding and policy loans affect this risk."),
("Is IUL a good retirement strategy?","It can serve some people with long-term needs, but illustrations are not guarantees. Costs, caps, and loans matter, and it is not a substitute for tax-advantaged retirement accounts for most people.")],
rel=[("Indexed Universal Life","Our IUL overview.","/indexed-universal-life"),("Life Insurance","Compare term and permanent options.","/life-insurance"),("Term vs. Whole Life","Which fits your family?","/blog/term-vs-whole-life-insurance-which-fits-your-family")],
body=f"""
Indexed universal life, or IUL, is one of the most heavily marketed life insurance products, especially to higher earners. It can be useful in the right situation, but it is also easy to misunderstand. This guide explains how it works, what it costs, and what can go wrong, so you can ask better questions.

{CAV}

## What IUL is
An IUL is a type of permanent life insurance. It has two main parts:
- **A death benefit** paid to your beneficiaries when you die, as long as the policy is in force.
- **A cash value account** that earns interest credits linked to an index, such as the S&P 500, without being directly invested in it.

You pay premiums, which the insurer uses to cover the cost of insurance and policy fees, with the rest going to cash value. Premiums are flexible within limits.

## How the interest credits work
Like a fixed indexed annuity, an IUL credits interest using a formula tied to an index. Key terms:
- **Cap.** The maximum interest credited in a period.
- **Participation rate.** The share of the index's gain that counts.
- **Floor.** The minimum credited, often zero, in a down year.
- **Spread.** A percentage deducted from the gain.

Insurers can change some of these limits over time. Policy illustrations show hypothetical scenarios, not guaranteed results, so always ask which numbers are guaranteed and which are not.

## What it costs
IUL policies carry several charges:
- **Cost of insurance,** which generally rises as you age.
- **Administrative and premium charges.**
- **Rider charges** for options you add.
- **Surrender charges** if you cancel early.

Because costs rise with age, a policy that looks fine early can strain later if the cash value does not grow as illustrated.

!callout **Illustrations are not promises.** Ask for the guaranteed column, a conservative-rate illustration, and a version that shows what happens if credits are lower than the sales example.

{cta()}

## Who may consider IUL
- Higher earners who have maxed out other tax-advantaged options and want permanent coverage.
- People with long-term needs such as estate planning, business succession, or lifelong dependents.
- Buyers who understand the costs and can fund the policy consistently.

## Who may be better served by something else
- People who mainly need affordable protection for a set period. [Term life](/blog/term-vs-whole-life-insurance-which-fits-your-family) is often much cheaper for pure protection.
- Those who cannot commit to funding a policy for many years.
- Savers who have not used tax-advantaged retirement accounts such as 401(k)s and IRAs.

## Policy loans and withdrawals
Policies can allow you to borrow against cash value. Generally, loans are not taxed as income if the policy remains in force and is not a modified endowment contract, but loans accrue interest and reduce the death benefit. If the policy lapses with an outstanding loan, the gain can become taxable. Overfunding a policy can also trigger modified endowment contract rules, which change the tax treatment. These details are why you should consult a tax professional.

## Key risks
1. Policy lapse if funding is too low.
2. Non-guaranteed elements changing.
3. Surrender charges early on.
4. Loans reducing benefits.
5. Complexity that makes comparison difficult.

## Questions to ask before buying
- What are the guaranteed and non-guaranteed elements?
- What is the total annual cost in years 1, 10, and 20?
- How much premium keeps the policy in force under conservative assumptions?
- How will loans affect the policy?
- How does this compare with term insurance plus separate savings?
- How is the agent compensated?

## How we help
We are an independent agency. We compare IUL, term, and whole life from multiple carriers and tell you honestly if a simpler option fits better. We do not provide tax advice, and we never promise returns.
"""),
dict(slug="how-are-annuities-taxed",kind="life",
title="How Are Annuities Taxed? Rollovers, Withdrawals and Required Distributions",ttl="How Are Annuities Taxed?",short="How Annuities Are Taxed",em="Taxed",
desc="Annuity taxes depend on whether the money is qualified or non-qualified. Learn how withdrawals, payments, penalties and RMDs are generally taxed.",
lead="The tax rules differ depending on where the money came from. Knowing which bucket you are in comes first.",
faqh="Annuity Taxes FAQ",
faqs=[("Are annuity withdrawals taxed as income?","Gains are generally taxed as ordinary income when withdrawn. For non-qualified annuities, earnings are typically treated as coming out first, and for qualified annuities, withdrawals are generally fully taxable."),
("Is there a penalty for taking annuity money out early?","Withdrawals of taxable amounts before age 59½ may face an additional 10 percent federal tax, with exceptions, and the contract may also have surrender charges."),
("Do annuities have required minimum distributions?","Annuities held inside traditional IRAs or other qualified plans are subject to required minimum distribution rules. Non-qualified annuities generally are not, though contract rules may apply.")],
rel=REL_W,
body=f"""
Tax treatment is one of the most misunderstood parts of annuities. The tax-deferral feature is often promoted, but the full picture depends on whether your annuity is bought with pre-tax or after-tax dollars, how you take money out, and your age. This guide covers the general rules. Tax law changes and individual situations differ, so confirm details with a qualified tax professional.

{CAV}

## Start with the bucket: qualified or non-qualified
- **Qualified annuity.** Funded with pre-tax money inside a retirement account, such as a traditional IRA. Because you did not pay tax on the contributions, distributions are generally fully taxable as ordinary income.
- **Non-qualified annuity.** Funded with after-tax money. You get your original principal back without tax, and only the earnings are taxed.

Roth accounts follow Roth rules, which are different.

## Tax deferral explained
In both types, earnings inside the annuity are generally not taxed each year. You owe tax when you take money out. That tax deferral is a real feature, but remember that in a qualified account such as an IRA, tax deferral already exists. An annuity inside an IRA does not add extra tax deferral. People who buy one usually do so for other features such as guarantees or income, not for tax reasons.

## How withdrawals are taxed
For a non-qualified deferred annuity, withdrawals are generally treated as coming from earnings first, then principal. This is often called last-in, first-out treatment. That means early withdrawals are taxable until the gain has been taken out. For qualified annuities, the whole withdrawal is generally taxable.

## How annuitized payments are taxed
When you convert an annuity into a stream of income payments, a portion of each payment may be treated as a return of your original investment and tax-free, while the rest is taxable. This is based on an exclusion ratio for non-qualified contracts. In a qualified annuity, the entire payment is generally taxable.

!callout **Ask a tax professional** how a large annuity withdrawal could affect your bracket, your Medicare premiums, and the taxation of Social Security benefits in the same year.

{cta()}

## The early withdrawal tax
Taxable withdrawals before age 59½ may face an additional 10 percent federal tax, with exceptions such as disability or certain structured payments. This is separate from any surrender charge the insurer applies under the contract, so both costs can apply at once.

## Required minimum distributions
If an annuity is held in a traditional IRA or other qualified plan, required minimum distributions generally apply once you reach the applicable age, which depends on your birth year. Non-qualified annuities generally do not have the same required distributions, though contracts and beneficiary rules may impose their own timelines.

## Death benefits and beneficiaries
When an annuity owner dies, beneficiaries may owe income tax on the gain in a non-qualified annuity. They do not typically get a step-up in basis the way they might with stocks or real estate. Beneficiary options, including spousal continuation and payout timing, vary by contract, so review them carefully.

## 1035 exchanges
A Section 1035 exchange allows you to move from one annuity or life insurance policy to another annuity without triggering immediate tax if done correctly. This can be useful, but surrender charges and new terms may apply. Do not cash out one contract before completing an exchange.

## Common mistakes
1. Buying an annuity inside an IRA for tax deferral alone.
2. Forgetting that gains are taxed as ordinary income.
3. Ignoring surrender charges and the 10 percent additional tax.
4. Taking a large withdrawal in a single year without considering tax brackets and Medicare premiums.
5. Cashing out instead of exchanging.

## Learn the product first
If you are new to annuities, start with our explainers on [single-premium annuities](/blog/what-is-a-single-premium-annuity-who-is-it-for) and [fixed indexed annuities](/blog/what-is-a-fixed-indexed-annuity-fia).

## How we help
We are an independent agency. We explain product features from multiple carriers but we do not give tax advice. Your CPA or tax attorney should confirm how any product affects your return.
"""),
dict(slug="ira-rollover-into-an-annuity-what-to-ask-first",kind="life",
title="IRA or 401(k) Rollover Into an Annuity: What to Ask Before You Move Money",ttl="Rolling an IRA or 401(k) Into an Annuity",short="Rollover Into an Annuity",em="Rollover",
desc="Thinking of rolling an IRA or 401(k) into an annuity? Learn how it works, what it does and doesn't change, and the questions to ask before moving money.",
lead="Moving retirement money into an annuity is a big, often irreversible step. These are the questions that protect you.",
faqh="Annuity Rollover FAQ",
faqs=[("Can I roll my 401(k) into an annuity?","Often yes, typically by first rolling it to an IRA and then purchasing an annuity within the IRA, or sometimes directly from a plan that allows it. Rules depend on the plan and the product."),
("Does an annuity in an IRA give extra tax benefits?","No. An IRA already defers taxes, so an annuity inside it does not add further tax deferral. The reasons to use one are the contract features such as guarantees or income."),
("Can I undo an annuity rollover?","Many contracts have a short free-look period, often 10 to 30 days depending on state, but after that, surrender charges and tax consequences can make reversing it costly.")],
rel=REL_W,
body=f"""
Rolling an IRA or 401(k) into an annuity is one of the largest financial decisions a retiree or near-retiree can make. Done well, it can provide guaranteed income or protection. Done poorly, it can lock money in a product that does not fit, with fees and surrender charges you did not expect. Before you transfer a dollar, here is what to know and what to ask.

{CAV}

## How the mechanics work
There are two common paths:
1. **Direct from a 401(k).** Some plans allow in-plan annuity options or direct transfers to an insurer. This is not available everywhere.
2. **Through an IRA.** You first roll the 401(k) to an IRA via a direct, trustee-to-trustee transfer, then buy an annuity inside the IRA. This is a qualified annuity.

In both cases the money should move directly between institutions. Taking a check yourself can trigger withholding and a 60-day deadline.

## What an annuity changes, and what it does not
- **It does not add tax deferral.** The IRA is already tax-deferred.
- **It does not remove required distributions.** Required minimum distributions generally still apply to qualified annuities.
- **It can add guarantees.** Depending on the contract, this could include lifetime income, protection against loss of principal, or a death benefit.
- **It adds contract costs and restrictions.** Surrender charges, rider fees, and caps may apply.

!callout **The real question is not "annuity or no annuity."** It is "what job do I want this money to do, and is this contract the best tool for that job?"

## What job is the money supposed to do?
People usually have one of three goals for rollover money:
- **Income:** a reliable paycheck for life, to cover essential expenses.
- **Protection:** limit exposure to market losses on money you will need soon.
- **Growth with limits:** modest, protected growth while preparing for retirement.

If you are not sure which goal applies, slow down. A product that serves one goal poorly may be a mismatch for another.

{cta()}

## Questions to ask about the annuity
1. What is guaranteed, what is not, and for how long?
2. What are all the fees, including rider charges and any annual contract fees?
3. What is the surrender schedule, and what is the free-withdrawal amount?
4. How does the income rider work, and is the income base different from the cash value?
5. What is the insurer's financial strength rating?
6. What happens to the money when I die?
7. What is the free-look period?

## Questions to ask about the alternative
- What would happen if I left the money where it is?
- What are the fees and options in my current plan?
- Could I do part of the rollover instead of all of it?
- How would this affect my taxes, my Medicare premiums, and my Social Security taxation?

## Questions to ask the person selling it
- How are you paid on this sale, and does it differ across products?
- What products did you compare, and why did you choose this one?
- Can I see the contract, not just the brochure?
- Can I take it home and review it with my tax advisor?

A trustworthy professional welcomes these questions and does not pressure you to act quickly.

## Warning signs
- Pressure to move money immediately.
- Promises of high, guaranteed returns with no downside.
- Vague answers about fees or surrender charges.
- Discouragement from consulting a tax professional or family member.
- Claims that the annuity gives you tax advantages in an IRA beyond what the IRA already provides.

## Consider a partial rollover
You do not have to move everything. Some people dedicate a portion of savings to guaranteed income and keep the rest invested or accessible. Because annuity decisions are hard to reverse, starting smaller and leaving flexibility can be wise.

## Related reading
Start with [what to do with your 401(k)](/blog/what-to-do-with-your-401k-when-you-retire-or-leave-a-job), then learn how [annuities are taxed](/blog/how-are-annuities-taxed) and how a [fixed indexed annuity](/blog/what-is-a-fixed-indexed-annuity-fia) works.

## How we help
Honorbrook is an independent insurance agency. We explain annuity options from multiple carriers, show you the costs and trade-offs, and encourage you to review everything with your tax professional. We do not provide investment or tax advice.
"""),
]
