# Functional public expense: source extraction and interpretation

## Files and reproduction

Run `python extract_functional_expense.py` in this folder. Requires PyMuPDF. The script reads the original supplied `Budget PDFs/2024-2025 Budget.pdf`, preserves source values, and writes:

- `latest_vintage_functional_expenses_2015_2024.csv`:10actual fiscal observations,2015–16 through2024–25; health,basic/advanced education,social services,other programs,total programs,debt servicing,pension recovery,and total expense. Latest source vintage and PDF pages accompany each row. July1population and calendar-year CPI inputs are separately labeled.
- `expense_accounting_components_2024_budget_actual.csv`:9source accounting categories from p3 with paired2024–25 budget/current actual/prior actual.
- `ministry_operating_expense_2024_budget_actual.csv`:26ministries from p7,distinct from functional expense.
- `functional_expense_source_manifest.json`:source SHA256,PDF title/author/date metadata,source pages and reconciliation results.
- Original text excerpts from pp3,6,7,8,13,14.

PDF identity is **2024–25 Final Results–Year-end Report**,Government of Alberta–Treasury Board and Finance,createdJune25,2025. Its filename “Budget” does not make its historical/current values forecasts. Fiscal observations endMarch31,2025. Source publication date follows the observation cutoff. Official landing URL is saved; original remote PDF URL was not verified. No protected existing repository files or completed Infrastructure Analysis artifacts were altered.

## What functional expense measures

Historical p14 reports **consolidated expense by function**,not ministry operating budgets. These functional allocations can include operating expenditure,capital grants,amortization/inventory-related expense,and other expenses assigned to programs. They are accounting expenditure inputs,not direct service outputs,real construction volume,staffed capacity,or proof of quality-of-life improvement.

2024–25 functional health is **29,560M** while Ministry of Health operating expense is **25,669M**; those cannot be swapped or added as separate spending. Functional basic/advanced education **17,197M** differs from Ministry Education operating9,288M plus Advanced Education operating6,608M(15,896M). Functional social services8,462M is not the operating expense of a single renamed social-services ministry. Functional and ministry classifications answer different questions.

Total program expense **71,337M** comprises health29,560 + education17,197 +social8,462 +other16,118. Total expense **74,149M** adds debt servicing3,215 and pension recovery−403. Pension recovery is an accounting reduction,not a negative service delivered. Do not stack program total on top of its component functions,or total expense on top of program total.

Capital investment generally adds assets to the balance sheet and is amortized over time; capital grants may already appear in expense. **Do not add the entire Capital Plan to these expenses**: that double-counts grants and mixes capital investment with annual expense. The quality-of-life report should distinguish service operating inputs,capital investment,and financial outcomes.

Debt servicing p14 includes the source's consolidated category,not exclusively taxpayer-supported direct debt. Latest p7 distinguishes taxpayer-supported versus self-supported financing,including local-authority loans and Agricultural Financial Services Corporation. Rising debt expense is not an identified dollar-for-dollar service cut,counterfactual spending opportunity,or household-interest burden. Any crowding-out claim needs fiscal-policy identification beyond this descriptive series.

## Source comparability and demographic adjustment

Latest p14 footnote a says **“Numbers are not strictly comparable due to numerous accounting policy changes over time.2019–20 and2021–22 expense by function have been re-classified following re-organizations and other adjustments.”** Using one latest historical vintage improves consistency but does not remove all accounting breaks. Retain this warning prominently.

Population is July1of the fiscal-start calendar year,rounded tothousands; annual Alberta CPI is calendar-year average growth,rounded to0.1percentage points. Inflation chaining should use2016–2024 rates for a2015-based index,not compound2015's own inflation twice. CPI-adjusted expense/resident is a broad allocation-intensity comparison,not a sector price/volume measure. It cannot adjust for aging,case complexity,enrolment,disease prevalence,disability eligibility,housing need,or local delivery.

Descriptive2018–19→2024–25 nominal/adjusted-per-resident changes,using these same inputs:

|Function|Nominal total growth|CPI-adjusted per-resident change|
|---|---:|---:|
|Health|+34.8%|−1.4%|
|Basic/advanced education|+15.8%|−15.3%|
|Social services|+44.2%|+5.4%|
|Other program expense|+35.8%|−0.7%|
|Total program expense|+30.9%|−4.3%|
|Debt servicing|+63.1%|+19.2%|
|Total expense|+31.7%|−3.7%|

These are **financial input descriptors**,not causal political effects or quality-of-life outcomes. Health's small1.4% decline is especially sensitive to fiscal alignment,prices,and accounting definitions. “Other programs” is broad and volatile; disasters/pandemic effects may matter. Avoid treating every expense movement as permanent service change.

## Source-table anomaly:2022–23 functional sum

Strict arithmetic audit found:

`25,486health +15,220education +7,222social +13,769other =61,697M`

but latest p14 reports total program expense **61,691M**,a **−6M residual** (about0.010%ofreportedprogram expense). Total expense nevertheless reconciles:

`61,691 +2,828debt −21pension recovery =64,498M`.

Four rounded-to-million components plus one rounded total could ordinarily disagree by about2M;6M exceeds ordinary rounding. The extractor **preserves all published values** and flags `program_reconciliation_status` as a source anomaly. Do not silently replace Other or Total to force a sum.2022–23 stacked functional composition charts would differ from the source program total unless an explicit residual/data-quality note is displayed.

Cross-vintage original-page checks support that this is a source-update issue rather than a parser mistake:

|Source vintage|2022–23 health|Education|Social|Other|Total program|Component sum−reported total|
|---|---:|---:|---:|---:|---:|---:|
|2022–23 PDF p13|25,486|15,220|7,222|13,743|61,671|0|
|2023–24 PDF p14|25,486|15,220|7,222|13,766|61,694|0|
|2024–25 PDF p14|25,486|15,220|7,222|13,769|61,691|+6|

The latest source changed Other and total in opposite directions. That does not establish which published entry is wrong;no source-backed repair is available locally. All other2015–16..2024–25 functional rows reconcile exactly. The anomaly does not affect the2018–19/2024–25 endpoint comparison,but it matters for a decade-wide stacked decomposition or modeling.

## Paired2024 budget/actual interpretation

The final-results report reproduces a budget-comparison column;an independent full original2024budget plan was not separately recovered locally. Call these **paired budget figures as reported in Final Results**,not independently verified original appropriations. Functional p14 has actuals only;do not invent functional health/education/social budget figures using ministry totals.

Source p3:total expense budget73,182M,actual74,149M;operating budget60,124M,actual62,025M;capital grants3,469→2,934M;disaster assistance0→1,932M;amortization/inventory/disposals4,564→4,446M;general debt1,856→1,779M;capital-plan debt1,533→1,436M;pension recovery−364→−403M;contingency2,000→0M. The contingency is budget authority/reserve,not missing delivered expenditure;disaster assistance's zero budget does not mean disasters had zero policy provision when reserves/contingency existed.

Ministry row sums versus source operating total have residuals budget0M,currentactual+1M,prioractual−1M,consistent ordinary rounding. Some displayed change columns differ by1M from subtracting displayed rounded values(e.g.Health budget24,648,current25,669,reportedchange1,020);preserve source-reported changes separately rather than treating rounding as a correction.

## Independent-review targets

Check latest p14original rendered cells for2022–23 anomaly;verify endpoint functions and total/pension reconciliation;verify functional versus ministry labels;review p14comparability footnote;ensure budget columns aren't fabricated for functions;ensure quality-of-life outcomes have independent outcome sources;avoid totals/component double-counting and causal debt-crowding-out claims.
