# Living standards: source-backed economic evidence and limits

The primary economic panel is the official **2024-25 Final Results Year-End Report**, PDF/printed page **13**, “Key Economic Indicators, 2013 to 2024”. The source file is misleadingly named `Budget PDFs/2024-2025 Budget.pdf`. A separate **2022-23 Final Results** panel, PDF/printed page **12**, preserves observations starting in 2011. It is explicitly a different vintage and is **not spliced** into the primary panel. The long ledger contains 144 observations across six metrics and two source panels, with exact source rows, units, dates, status and interpretation limits.

`extract_living_standards.py` reproduces economic CSVs directly from source PDFs using `pdftotext`. `verify_living_standards.py` independently uses `pypdf`, separately parses source values (including accounting negatives and wrapped rows), and verifies all 144 observations and estimated income endpoints. Original repository files and Infrastructure Analysis are read-only inputs. The existing population/CPI panel is reused read-only for earnings sensitivity.

## Supported findings

- Alberta's average weekly nominal earnings rose from **$1,148 in 2018 to $1,328 in 2024**, **15.7%**. Applying the rounded official calendar CPI chain produces a **3.7% decline in consumer-price-adjusted average weekly earnings**. From 2019, the equivalent decline is **3.3%**. These are average employee earnings, not median household disposable income or a living-standard index; employment mix and hours can affect the series.
- The unemployment rate was **6.5% in 2018**, **6.9% in 2019**, **5.8% in 2022**, and **7.0% in 2024**. Changes are percentage points, not population unemployment counts. Provincial total population is not the unemployment denominator.
- Employment expanded from **2.279 million in 2018 to 2.519 million in 2024**. Total jobs and total population alone do not establish an employment rate; that requires a consistently defined working-age population and labour-force coverage.
- The 2024 source reports **7.1% aggregate primary household income growth**, explicitly an **estimate** under the `a` footnote. It is not a final actual, per-person income, median income, disposable income or poverty rate. The separate 2022 endpoint income growth is also marked estimated.
- **47,827 housing starts in 2024** identify construction starts, not completed dwellings, rent burden, affordability, home ownership access, homelessness or net housing supply.

These observations describe economic conditions; they do not isolate UCP policy effects or infrastructure effects. Recession, commodity cycles, pandemic conditions, composition and migration are relevant confounders.

## Historical Canada comparator, strictly limited

The **2014-15 Annual Report**, PDF page **122** / printed page **116**, publishes an **unaudited Index of Economic Well-Being** for 2009–2013. Its 2013 Alberta value is **0.727**, versus **0.562 for Canada**, and Alberta ranks first among provinces. The source states: “The rating indicates Alberta’s and Canada’s position on an indexed scale derived from weighting four variables of economic well-being: consumption, wealth, equality and security.” Definitions/provider are on PDF page **133** / printed **127**: Centre for the Study of Living Standards; includes consumption, wealth, inequality/poverty intensity and risks.

`historical_wellbeing_comparator.csv` archives ten source values for Alberta/Canada with exact pages and limitations. It is **not a contemporary poverty rate**, not a 2019–2024 comparison, and cannot establish quality-of-life change during UCP rule. No Canada comparator is supplied by the selected latest economic table.

## Evidence gaps and network outcomes

No consistent post-2019 **poverty (Market Basket Measure), food insecurity, median/after-tax household income, rent burden or core housing need** series was recovered from the archived fiscal reports. Early references to eliminating poverty are policy goals or composite-index definitions, not observations of poverty rates. None have been substituted for missing outcomes.

The official annual-report index became reachable, but four specific linked 2024-25 resources returned **403**: whole-government report, Affordability and Utilities, Seniors/Community/Social Services, and Jobs/Economy/Trade. Each relevant resource was attempted once using the normal HTTPS proxy with TLS verification. URLs and results for the three ministry requests are in `linked_report_download_manifest.json`; the whole-government URL was obtained from the same index and returned 403. Successful index access does not establish successful PDF access. No guessed slugs or verification bypass was used.

There are **no 2025 living-standard observations** in the primary local panel. Exact annual/monthly CPI levels, post-2019 comparator outcomes, distributional measures and official source definitions beyond table labels remain necessary for a broader quality-of-life assessment. Financial allocations, housing starts and average wages cannot fill those evidence gaps.


## Material source-access update and current social evidence

Subsequent diagnosis showed a **client-dependent HTTP response**, rather than a general denial of these official PDFs: the three exact index-linked ministry URLs returned403 to Python urllib's default client, but **200 to curl -L --fail with ordinary TLS verification and the normal proxy**. The newly downloaded SCSS, Jobs/Economy/Trade and Affordability/Utilities reports, source hashes and successful responses are archived in `curl_linked_report_download_manifest.json`. Earlier failed-attempt manifests remain as an audit trail; the successful downloads supersede their resource-availability conclusion. No authentication or certificate verification was bypassed.

`current_social_outcomes_2021_2024.csv` and `extract_current_social_outcomes.py` archive SCSS housing and employment-service measures. Housing combined **new units plus additional rent-subsidy households** is2243/2325/2302/798 for2021-22 through2024-25 (PDFp38, printed36). The 2024-25 total decomposes to388 newly built units plus410 additional supported households; it is **not798 new physical housing units**. Definitions p67/printed65 include completed regenerated units and occupancy permits for capital projects; subsidies are incremental households at fiscalend minus fiscalstart. Comparable history is unavailable before2021-22. These program outputs are not population core-housing-need rates.

`childcare_income_access_2020_2025.csv` distinguishes AISH adjudication waits, actual licensed childcare capacity/growth, historical average fees and one **post-cutoff announced** fee. AISH median complete-application-to-medical-decision wait rose4.3→5.3weeks in2024-25, remaining below9.0week target (SCSS PDFp36/printed34); this does not measure waiting from initial application or income adequacy. Jobs/Economy/Trade PDFp65/printed63 reports average eligible licensed childcare fees $15/day inJanuary2024 under the federal-provincial agreement. The $326.25/month flat fee beginsApril1,2025 and is archived as announced/postcutoff, not2024-25delivery.

Jobs/Economy/Trade p66/printed64 reports142700 up-to-kindergarten licensed spaces byMarch31,2025 and14300 netnew in2024-25 (11% growth). Its all-licensed-space KPI p73/printed71 reports10% growth with **broader coverage including out-of-school care**, definedp79/printed77. Preserve the different populations; do not treat11% versus10% as conflicting or average them. Licensed capacity does not establish actual staffing, attendance, net household affordability or sufficiency relative to eligible children.

SCSS employment-service outcomes are selected former service clients employed three months later, not provincial employment rates or causal program effects. Its explanatory narrative p49/printed47 uses unemployment5.8% in2023 and7.1% in2024, whereas the primary Final Results economic table gives5.9% and7.0%. `unemployment_source_conflict.json` retains the conflict without overwriting the primary panel. No reconciled explanation is available locally.

The newer ministry reports add specific access and program-delivery outcomes but still do not establish provincial poverty, household food-insecurity prevalence or population-wide housing inadequacy. Those evidence gaps remain open.

## Direct poverty retrieval supersedes the earlier gap

Official Statistics Canada Table11-10-0135-01 is now retrieved successfully with curl and independently verified. [MBM poverty evidence](MBM_POVERTY.md) provides exact Alberta/Canada All-persons poverty rates, source metadata and quality flags. The **2018-base series covers2015–2023**, while the **2023-base series covers2020–2024**; they remain separate. No same-base2018–2024 comparison is available. Latest-base2024 poverty point estimates are11.0% for both Alberta andCanada; equality of rounded point estimates is not proof of equal underlying rates or a significance result. Household food-insecurity and population housing-need gaps remain unresolved.
