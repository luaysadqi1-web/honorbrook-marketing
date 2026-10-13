import importlib.util
def _imp(n):
    import os; sp=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),n+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
_w=_imp('posts_2'); cta=_w.cta; REL_W=_w.REL_W; CAV=_w.CAV
POSTS=[
dict(slug="iul-vs-term-life-plus-investing-for-high-earners",kind="life",
title="IUL vs. Term Life Plus Investing: Which Is Better for High Earners?",ttl="IUL vs. Term Life Plus Investing for High Earners",short="IUL vs. Term + Invest",em="Better",
desc="Is indexed universal life better than buying term and investing the difference? Compare costs, flexibility, taxes and risks for high earners.",
lead="There is no universal winner. The answer depends on your goals, your discipline, and what else you have already maxed out.",
faqh="IUL vs. Term + Invest FAQ",
faqs=[("What does 'buy term and invest the difference' mean?","It means buying low-cost term life insurance for protection and putting the money you would have spent on a more expensive permanent policy into separate investments or retirement accounts."),
("Is IUL ever the better choice for high earners?","It can be for people who need permanent coverage, such as for estate planning or business needs, have maxed out other tax-advantaged accounts, and can fund the policy consistently. It is not automatically better."),
("What are the main risks of IUL compared with term plus investing?","IUL has policy charges, caps that limit upside, non-guaranteed elements, and lapse risk if underfunded. Term plus investing has market risk and requires discipline to actually invest the difference.")],
rel=REL_W,
body=f"""
Few debates in personal finance are as heated as this one. Should a high earner buy an indexed universal life (IUL) policy, or buy cheap term insurance and invest the savings elsewhere? Both camps are loud, and many of the loudest are selling something. Here is a balanced look at how the two approaches compare, so you can ask better questions of any advisor.

{CAV}

## What each approach actually is
- **Term life** pays a death benefit if you die during a set period, such as 10, 20, or 30 years. It has no cash value and is usually the cheapest way to buy a large amount of coverage.
- **IUL** is permanent life insurance with a death benefit and a cash value account whose credits are linked to an index, subject to caps and other limits. It costs much more per dollar of coverage because it is designed to last a lifetime and build cash value. Read the basics in [what IUL is and how it works](/blog/what-is-indexed-universal-life-iul-how-it-works-cost-risks).
- **Term plus investing** means buying term for protection and putting the savings into 401(k)s, IRAs, brokerage accounts, or other investments.

## Where term plus investing tends to win
- **Cost of protection.** For a family that needs a large death benefit during working years, term is usually far cheaper.
- **Transparency.** The cost is simple, and investments can be low-fee and easy to understand.
- **Liquidity.** Taxable and retirement accounts can be accessed without policy rules, though taxes and penalties may apply.
- **Upside.** Direct investments are not limited by caps, though they also carry the full risk of loss.

## Where IUL may have an edge
- **Permanent coverage.** If you need coverage that will not expire, for example for estate liquidity or a lifelong dependent, term eventually runs out.
- **Tax features.** Life insurance death benefits are generally income-tax-free to beneficiaries, and cash value grows tax-deferred inside the policy. Policy loans can be a way to access value, with caveats.
- **Downside floor on credits.** The index credit has a floor, often zero, which can reduce exposure to market losses on the cash value account, though policy charges continue regardless.
- **Forced savings.** For some people, a required premium is a discipline tool.

## The honest costs of IUL
IUL charges include the cost of insurance, administrative fees, and rider costs, and these generally rise as you age. If the cash value does not grow as illustrated, the policy can require more premium or lapse. Caps and participation rates can change. Illustrations rely on assumptions, so ask to see conservative and guaranteed scenarios. This is the single most important step before buying.

!callout **The fair test:** compare an IUL against term plus a real investing plan using the same dollars and conservative assumptions for both. If the IUL only wins under optimistic assumptions, treat that as a warning.

{cta()}

## Questions that help you decide
1. **Do you need coverage for life, or for a period?** If your need ends when kids are grown and debts are paid, term usually fits.
2. **Have you used your tax-advantaged accounts?** 401(k), IRA, HSA, and similar accounts often come first for most people.
3. **How disciplined are you?** If you would not actually invest the difference, that changes the comparison.
4. **Do you have estate or business planning needs?** Permanent coverage may play a role.
5. **How comfortable are you with complexity?** IUL has many moving parts.

## A hybrid approach
Many people use both: term to cover large temporary needs, and a smaller permanent policy for lifelong needs. This can balance cost and permanence. A tax professional and a licensed agent can help you size each piece.

## Related reading
If you are still comparing basics, read [term vs. whole life](/blog/term-vs-whole-life-insurance-which-fits-your-family). To size coverage, see how much [life insurance you need](/blog/how-much-life-insurance-do-you-need).

## How we help
Honorbrook is an independent agency. We can quote term, whole life, and IUL from multiple carriers and tell you honestly when a simpler option fits better. We do not give tax or investment advice, and we never promise returns.
"""),
dict(slug="fixed-indexed-annuity-vs-cd-vs-bond-where-does-an-fia-fit",kind="life",
title="Fixed Indexed Annuity vs. CD vs. Bond: Where Does an FIA Fit?",ttl="Fixed Indexed Annuity vs. CD vs. Bond",short="FIA vs. CD vs. Bond",em="FIA",
desc="How does a fixed indexed annuity compare with a CD or a bond? Learn the differences in safety, access, taxes and growth potential.",
lead="They can all be called conservative, but they work very differently. Here is how to compare them honestly.",
faqh="FIA vs. CD vs. Bond FAQ",
faqs=[("Is a fixed indexed annuity safer than a CD?","They are different kinds of safety. CDs are generally FDIC-insured up to applicable limits, while annuity guarantees depend on the insurer's claims-paying ability and state guaranty protections, which vary."),
("Do bonds and FIAs have the same risks?","No. Bonds can lose value when interest rates rise or if the issuer defaults, while an FIA's credited interest is subject to its crediting limits and its value can be reduced by withdrawals and fees."),
("Which one has better tax treatment?","CD interest and bond interest are generally taxable each year, while FIA growth is generally tax-deferred until withdrawn. Taxes depend on your situation, so consult a professional.")],
rel=REL_W,
body=f"""
When people near retirement want to protect money from market swings, the same three choices come up: a certificate of deposit (CD), a bond, or a fixed indexed annuity (FIA). They are sometimes lumped together as "conservative," but they have different safety nets, costs, and tradeoffs. Understanding those differences helps you pick what fits, or decide to use more than one.

{CAV}

## The three products in plain English
- **CD.** You deposit money with a bank for a fixed term and earn a stated interest rate. Early withdrawal usually costs a penalty.
- **Bond.** You lend money to a government or company, which pays interest and returns principal at maturity. You can hold individual bonds or bond funds, and prices can move before maturity.
- **FIA.** You deposit money with an insurance company. Interest credits are linked to an index, subject to caps, participation rates, or spreads, with a floor that is often zero. Learn more in [what an FIA is](/blog/what-is-a-fixed-indexed-annuity-fia).

## How safety differs
- **CDs** are generally backed by FDIC insurance up to the applicable limit per depositor, per bank, per ownership category. That is a federal guarantee, not a company promise.
- **Bonds** are backed by the issuer. U.S. Treasury bonds are backed by the federal government, while corporate and municipal bonds carry credit risk.
- **FIAs** are backed by the claims-paying ability of the insurer. They are not FDIC-insured. State guaranty associations provide limited protection if an insurer fails, and limits vary by state.

Safety is not one thing. Ask who stands behind the promise and what happens if they cannot keep it.

## How access to your money differs
- **CDs:** liquid at maturity, penalties for early withdrawal.
- **Bonds:** can be sold before maturity at market price, which may be above or below what you paid.
- **FIAs:** commonly have a surrender period, often several years, with surrender charges for withdrawals above the free-withdrawal amount. Withdrawals before 59½ can also face an extra tax.

## How growth differs
- **CD:** a known rate for the term.
- **Bond:** interest payments plus the possibility of price changes.
- **FIA:** potential interest linked to an index, limited by crediting rules, with protection against negative index credits. The credited amount is often less than the index's gain, and index dividends are generally not included.

!callout **No product wins everywhere.** A CD's strength is certainty and FDIC insurance. A bond's strength is income and liquidity. An FIA's strength is a floor on credits with some growth potential and, with optional riders, lifetime income features. Each has a cost.

{cta()}

## Taxes
- **CD and bond interest** is generally taxed as ordinary income in the year earned, with some bond types exempt from certain taxes.
- **FIA growth** is generally tax-deferred until you take money out, then taxed as ordinary income. See [how annuities are taxed](/blog/how-are-annuities-taxed).
- Inside an IRA, all three follow IRA tax rules, and an annuity does not add extra tax deferral.

## When each may fit
- **CD:** short-term savings, emergency reserves, or when FDIC insurance is a priority.
- **Bond:** income needs, diversification, or a defined time horizon.
- **FIA:** money you will not need for several years, where you value a floor on credits and are comfortable with caps and surrender charges.

## A way to compare
Ask the same questions of each:
1. Who guarantees it and how strong are they?
2. What can I earn, and what is the realistic range?
3. What does it cost to get my money early?
4. How is it taxed?
5. What happens to it when I die?

Then build a simple table of your own with a bank CD quote, a bond or bond fund yield, and an FIA's cap, participation, and surrender schedule.

## Mixing instead of choosing
Many retirees use a combination: a cash reserve for near-term needs, bonds for income, and a portion in an annuity for protected growth or guaranteed income. The right mix depends on your age, other income, and comfort with risk.

## How we help
We are an independent agency and we explain annuity features from multiple carriers. We cannot give tax or investment advice, and we encourage you to compare with bank and brokerage options before deciding.
"""),
dict(slug="how-much-life-insurance-do-high-income-earners-need",kind="life",
title="How Much Life Insurance Do High-Income Earners Need?",ttl="How Much Life Insurance Do High Earners Need?",short="Life Insurance for High Earners",em="High-Income Earners",
desc="High income doesn't mean the rule-of-thumb multiples work. Learn a needs-based method for sizing life insurance, plus estate and business factors.",
lead="Rules of thumb break down at higher incomes. A needs-based approach gives a more honest number.",
faqh="High-Earner Life Insurance FAQ",
faqs=[("Is there a simple multiple of income for life insurance?","Rules of thumb like 10 times income are only starting points. A needs analysis based on debts, income replacement, future costs, and existing assets is more accurate."),
("Do high earners need permanent life insurance?","Not always. Permanent coverage can fit estate planning, business, or lifelong needs, but many families rely mainly on term during working years."),
("Should I include my spouse's income in the calculation?","Yes. Consider both incomes, who relies on whom, childcare and household costs, and how much each partner contributes beyond a paycheck.")],
rel=REL_W,
body=f"""
When income rises, the usual advice, "buy ten times your salary," starts to sound inadequate or even absurd. A high earner may have a mortgage, college goals, a business, investments, and complicated taxes. Sizing life insurance for that picture takes more thought than a multiple. Here is a practical way to approach it.

{CAV}

## Why rules of thumb fall short
Multiples of income treat everyone the same. But two people earning the same salary can have very different needs. One has young children, a large mortgage, and few savings. The other has grown kids, no debts, and a large investment portfolio. The first needs much more coverage. A needs-based analysis fits the real situation instead.

## A needs-based method
Think in four buckets:
1. **Debts and final costs.** Mortgage, loans, credit cards, funeral costs, and legal expenses.
2. **Income replacement.** How many years would your family need support, and how much per year after accounting for other income?
3. **Future goals.** College funding, a spouse's retirement, and care for a dependent with special needs.
4. **Business and estate needs.** Buy-sell agreements, key-person coverage, and estate liquidity.

Then subtract what your family already has: savings, investments, existing life insurance (including any group coverage that may end if you change jobs), and a surviving spouse's income.

## Income replacement, step by step
- Estimate the annual amount your family would need to maintain their lifestyle.
- Subtract your surviving partner's income and any benefits.
- Multiply the gap by the number of years of support you want to provide, then consider whether a lump sum invested could reasonably produce that income.

This is where an advisor can help you choose conservative assumptions about returns and inflation.

!callout **Do not count on employer coverage alone.** Group life insurance through work often stops when you leave the job, and its amount is usually a multiple of salary that may be smaller than your need.

{cta()}

## Special considerations for high earners
- **Business owners.** Coverage can fund buy-sell agreements or protect the business from losing a key person.
- **Estate planning.** Larger estates may face estate taxes or need liquidity so heirs do not have to sell assets quickly. An attorney can advise on structures such as trusts.
- **Stay-at-home partners.** Replacing childcare, household management, and other contributions is a real cost.
- **Variable compensation.** Bonuses, equity, and commissions make income less predictable, so plan around stable levels and review often.
- **Health and age.** The earlier you buy, the cheaper it generally is, and health changes can limit options.

## Term, permanent, or both
Term insurance can provide large amounts at lower cost during the years your family depends on your income. Permanent insurance such as whole life or [IUL](/blog/what-is-indexed-universal-life-iul-how-it-works-cost-risks) may serve lifelong needs. Many families use a mix. Compare the two approaches in [IUL vs. term plus investing](/blog/iul-vs-term-life-plus-investing-for-high-earners).

## Underwriting at higher amounts
Large policies usually involve more underwriting, such as medical exams and financial documentation. Apply earlier than you think you need to, and be accurate on applications. Insurers look at how much coverage is reasonable relative to your income and net worth.

## Review regularly
Your needs change with a new child, a bigger mortgage, a business sale, or a divorce. Review coverage every few years and after major life events. See the basic framework in [how much life insurance you need](/blog/how-much-life-insurance-do-you-need).

## How we help
Honorbrook is an independent agency. We help size coverage and quote term, whole life, and IUL from multiple carriers. We do not give tax or legal advice, so involve your CPA and attorney in estate and business planning.
"""),
dict(slug="is-cash-value-life-insurance-a-good-retirement-supplement",kind="life",
title="Is Cash Value Life Insurance a Good Retirement Supplement? What Agents Don't Always Say",ttl="Is Cash Value Life Insurance a Good Retirement Supplement?",short="Cash Value Life for Retirement",em="Retirement Supplement",
desc="Can cash value life insurance supplement retirement? Learn how it works, the costs and limits, and honest questions to ask before relying on it.",
lead="It can play a role for some people, but it is not a replacement for a retirement plan, and the sales pitch skips important details.",
faqh="Cash Value Life Insurance for Retirement FAQ",
faqs=[("Can I use life insurance cash value for retirement income?","Some people access cash value through withdrawals and policy loans, but this reduces the death benefit and can cause the policy to lapse if mismanaged, so it requires careful planning."),
("Is cash value life insurance better than a 401(k)?","They serve different purposes. Retirement accounts are designed for retirement savings with their own tax benefits and employer matches, and most people consider them first."),
("What are the downsides of using life insurance for retirement?","Higher costs, surrender charges early on, complexity, loans that accrue interest, and the risk of lapse if the policy is underfunded.")],
rel=REL_W,
body=f"""
You may have heard that permanent life insurance can double as a retirement account: pay premiums for years, build cash value, then borrow against it tax-free in retirement. Parts of that are true. Other parts leave out costs and risks. This guide covers both sides so you can judge whether it belongs in your plan.

{CAV}

## What cash value is
Permanent policies such as whole life and universal life have a cash value account in addition to the death benefit. Part of your premium goes to insurance costs, and part builds cash value, which can earn dividends or interest depending on the policy type. In an [indexed universal life policy](/blog/what-is-indexed-universal-life-iul-how-it-works-cost-risks), credits are linked to an index within caps and floors.

## How people use it in retirement
- **Withdrawals.** You can generally withdraw up to your basis (the premiums you paid) without income tax in many policies, though this reduces cash value and death benefit.
- **Policy loans.** You can borrow against cash value. Loans are not generally treated as income when the policy stays in force, but interest accrues and unpaid loans reduce the death benefit.
- **Surrender.** Cancel the policy and receive the surrender value, possibly with taxable gain.

Read more about loans in [policy loans and taxes](/blog/life-insurance-policy-loan-does-it-avoid-taxes).

## The upsides
- Growth inside the policy is tax-deferred.
- Death benefit generally passes income-tax-free to beneficiaries.
- No contribution limits like those on retirement accounts, though funding limits tied to tax rules apply.
- Access to value without the early-withdrawal rules that apply to retirement accounts.
- Permanent coverage that does not expire.

## What agents don't always say
1. **Costs are real.** Insurance charges, administrative fees, and surrender charges reduce growth, especially in early years. Cash value may be low in the first years.
2. **Illustrations are not guarantees.** Projected values depend on assumptions about future credits or dividends.
3. **Loans can backfire.** If a policy with a large loan lapses, the gain can become taxable and the coverage disappears.
4. **Overfunding triggers rules.** A policy funded too heavily can become a modified endowment contract, which changes tax treatment of loans and withdrawals.
5. **It is a long-term commitment.** Policies often take many years to work as intended.
6. **Other accounts usually come first.** Employer matches, 401(k)s, IRAs, and HSAs offer valuable benefits that life insurance does not.

!callout **The honest framing:** cash value life insurance is better thought of as insurance with a savings feature, not as a high-performing investment.

{cta()}

## Who it might suit
- People with permanent insurance needs who also want a savings component.
- High earners who have maxed out other tax-advantaged accounts.
- Business owners or families with estate planning goals.
- Buyers who can fund the policy for decades and understand the costs.

## Who may be better off elsewhere
- Anyone who has not used employer matches and retirement accounts.
- People who may need to stop paying premiums in a few years.
- Those who mainly want inexpensive protection. See [term vs. whole life](/blog/term-vs-whole-life-insurance-which-fits-your-family).
- Savers who need simple, flexible access to funds.

## Questions to ask
- What is the cash value in years 1, 5, 10, and 20 under guaranteed and non-guaranteed assumptions?
- What are all the charges, and which can change?
- How much premium keeps the policy in force if returns are lower than illustrated?
- What happens if I take a loan and cannot repay it?
- How does this compare with simply investing the same money?

## How we help
We are an independent agency and we show cash value policies from multiple carriers with conservative as well as optimistic illustrations. We do not give tax or investment advice, so ask your tax professional how it fits your plan.
"""),
dict(slug="life-insurance-policy-loan-does-it-avoid-taxes",kind="life",
title="What Is a Life Insurance Policy Loan, and Does It Really Avoid Taxes?",ttl="Life Insurance Policy Loans: Do They Avoid Taxes?",short="Life Insurance Policy Loans",em="Avoid Taxes",
desc="Policy loans can give access to cash value, but 'tax-free' comes with conditions. Learn how loans work, how interest accrues, and what can trigger taxes.",
lead="Loans are generally not taxed as income while the policy stays in force. The word 'while' is doing a lot of work.",
faqh="Policy Loan FAQ",
faqs=[("Are life insurance policy loans taxable?","Generally a loan is not treated as taxable income if the policy stays in force and is not a modified endowment contract, but unpaid loans plus interest can create a taxable event if the policy lapses or is surrendered."),
("Do I have to repay a life insurance loan?","There is typically no required repayment schedule, but interest accrues, and unpaid loans reduce the death benefit and cash value and can cause the policy to lapse."),
("What is a modified endowment contract?","A policy funded beyond certain tax-law limits is treated as a modified endowment contract, and loans and withdrawals from it are generally taxed differently and may face a penalty before age 59½.")],
rel=REL_W,
body=f"""
Policy loans are central to many sales pitches for cash value life insurance. The idea is simple: borrow from your policy instead of withdrawing, and avoid income tax. The reality is more nuanced. Loans can be useful, but only if you understand the conditions and the risks.

{CAV}

## How a policy loan works
When your permanent policy has built up cash value, the insurer may let you borrow against it. You are not usually withdrawing your own money. Instead, the insurer lends you money, using your cash value as collateral. Key features:
- No credit check is typically required.
- There is generally no fixed repayment schedule.
- Interest accrues on the loan at a rate set by the policy.
- Part of your cash value may continue to earn credits, but the amount securing the loan may earn differently depending on the policy design.

## Why loans are generally not taxed as income
Because it is technically a loan and not a distribution, the proceeds are generally not treated as taxable income at the time you receive them, provided the policy remains in force and is not a modified endowment contract. That is the basis for the "tax-free retirement income" pitch. But the conditions matter.

## What can trigger taxes
1. **The policy lapses with a loan outstanding.** If the policy ends and there are loans larger than your basis in the contract, the excess can become taxable income, often without any cash in hand to pay the tax.
2. **The policy is a modified endowment contract (MEC).** If you fund a policy faster than tax-law limits allow, it is classified as a MEC. Loans and withdrawals from a MEC are generally taxed on a gains-first basis and may face an additional 10 percent tax before age 59½.
3. **You surrender the policy** with loans outstanding and gain in the contract.

!callout **The big risk:** loans plus accrued interest can grow faster than the cash value supporting them. If the policy collapses late in life, you may face a tax bill and no coverage.

## Other costs and trade-offs
- **Interest.** Loan interest can be fixed or variable and often compounds against you.
- **Reduced death benefit.** Unpaid loans are subtracted from the death benefit paid to beneficiaries.
- **Complex interactions.** Some policies have loan features that credit differently on borrowed amounts, so the net cost depends on the design.
- **Impact on guarantees.** A heavily loaded policy may require more premium to stay in force.

{cta()}

## Loan vs. withdrawal
A withdrawal permanently reduces cash value and may reduce the death benefit. Withdrawals up to basis are generally tax-free in non-MEC policies, while amounts above basis are taxable. A loan leaves the cash value in place as collateral but creates a debt. The better choice depends on your policy and plan, which is why you should ask the insurer to model both.

## How to use loans carefully
1. **Ask for an in-force illustration** showing the effect of the loan at your age under conservative assumptions.
2. **Keep the policy well funded** so it can support loans.
3. **Avoid taking loans that approach the full cash value.**
4. **Monitor annually.** Review statements for loan balance, interest, and lapse risk.
5. **Know your options** if the policy weakens, such as repaying part of the loan or adding premium.
6. **Talk to a tax professional** before taking large loans.

## Alternatives to consider
Depending on your goals, alternatives may include drawing from taxable or retirement accounts in a planned order, a home equity line, or a fixed annuity income stream. Compare after-tax cost and risk. See also [is cash value life insurance a good retirement supplement](/blog/is-cash-value-life-insurance-a-good-retirement-supplement).

## How we help
Honorbrook is an independent agency. We explain how policy loans work for the policies we offer and encourage you to review projections with your tax advisor. We do not provide tax advice.
"""),
dict(slug="what-happens-to-a-fixed-indexed-annuity-when-you-die",kind="life",
title="What Happens to a Fixed Indexed Annuity When You Die? Beneficiaries and Probate Explained",ttl="What Happens to an FIA When You Die?",short="FIA at Death",em="Die",
desc="What happens to a fixed indexed annuity at death? Learn how beneficiaries are paid, how probate and taxes work, and the options for spouses.",
lead="Usually the named beneficiary receives the value and skips probate, but taxes, timing and contract terms matter.",
faqh="FIA at Death FAQ",
faqs=[("Does a fixed indexed annuity go through probate?","If a beneficiary is named and living, the proceeds generally pass directly to that person without probate. If there is no named beneficiary, the annuity may become part of the estate and go through probate."),
("Do beneficiaries pay taxes on an inherited annuity?","Beneficiaries generally owe ordinary income tax on the gain, not the original investment in a non-qualified annuity, and qualified annuities are generally fully taxable. Rules depend on the account type and the beneficiary."),
("Can a spouse keep the annuity after the owner dies?","Many contracts allow a spouse to continue the contract as the new owner, which can preserve tax deferral. Terms vary by contract, so check the specifics.")],
rel=REL_W,
body=f"""
People buy annuities for many reasons, but not many think about what happens when they die. The answer affects your family, your taxes, and whether the annuity does what you intended. Here is how the common scenarios work. Contracts differ, so the specifics of yours always control.

{CAV}

## The basics: who gets the money
Every annuity should have a named beneficiary on file. At the owner's death, in most cases:
- **The beneficiary receives the contract's death benefit,** which for many fixed indexed annuities is the accumulation value (sometimes with adjustments), not necessarily a rider's income base.
- **Surrender charges are typically waived** at death under many contracts, but check.
- **The money is generally paid directly to the beneficiary,** outside the will, so it often avoids probate.

## When probate becomes an issue
If no beneficiary is named, or all named beneficiaries have died, the annuity may be paid to the estate, which usually means probate. That can add time, cost, and public exposure. Reviewing your beneficiary designations periodically is one of the simplest and most valuable steps you can take. Also keep contingent beneficiaries on file.

!callout **Annuity beneficiary forms override your will.** If your will says one thing and the annuity form says another, the form generally controls. Update both after life events such as marriage, divorce, or the birth of a child.

## How beneficiaries are taxed
- **Non-qualified annuity (after-tax money).** The beneficiary generally owes ordinary income tax on the gain above the original investment. There is typically no step-up in basis for annuity gains, unlike some other assets.
- **Qualified annuity (IRA or other retirement money).** Distributions are generally fully taxable, and required distribution rules apply to inherited retirement accounts, which can include a limited payout window for many non-spouse beneficiaries.

Because rules change, confirm the current treatment with a tax professional. See also [how annuities are taxed](/blog/how-are-annuities-taxed).

## Payout options for beneficiaries
Contracts often offer choices such as:
- **Lump sum.** All at once, with the full taxable gain recognized in that year.
- **Payments over a period.** Spreading the income, and the tax, over several years.
- **Life income.** Converting to lifetime payments, if available.
- **Continuation by a spouse.** Some contracts let a surviving spouse become the new owner and keep deferral.

Timing rules may apply, so beneficiaries should act promptly and not simply cash out without understanding the tax effect.

{cta()}

## What about income riders?
If your annuity has a guaranteed lifetime income rider, understand that the rider's income base is generally a calculation for determining income, not a separate pot of money. At death, beneficiaries typically receive the contract value, not the income base. If this matters to your plan, ask exactly what the beneficiary receives under your contract, and whether any remaining payments continue.

## Joint ownership and spousal rights
Contracts may be owned jointly or by one spouse. State property laws can affect what a spouse is entitled to, particularly in community property states. Consider legal advice if the annuity is a large part of your estate.

## Steps to take now
1. **Confirm your beneficiaries** with the insurer in writing.
2. **Name contingent beneficiaries.**
3. **Tell your family** where the annuity is held and who to call.
4. **Keep contract copies** and the insurer's contact information with your estate documents.
5. **Review after major life events.**
6. **Talk to an estate attorney** about the best ownership and beneficiary structure for your situation.

## Related reading
If you are still evaluating annuities, start with [what an FIA is](/blog/what-is-a-fixed-indexed-annuity-fia) and [single-premium annuities](/blog/what-is-a-single-premium-annuity-who-is-it-for).

## How we help
Honorbrook is an independent agency. We explain the death-benefit features of annuities from multiple carriers. We do not give legal or tax advice, so involve your estate attorney and tax professional.
"""),
]
