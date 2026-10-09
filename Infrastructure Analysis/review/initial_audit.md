# Independent initial audit

Reviewed 9 October 2026. Reviewer: independent agent. Scope: existing repository, not yet the new infrastructure findings. No existing tracked files changed.

## Critical risks

1. **Operating expenditure is not infrastructure investment.** The existing historical analysis explicitly excludes capital expenditure, and collapses Infrastructure and Transportation ministries into `Other`. These files can provide fiscal context but cannot substantiate infrastructure construction or capital growth. Capital investment, capital grants, amortization, maintenance/renewal, and ministry operating expenses need distinct definitions and sources. Adding operating and capital indiscriminately can double count capital grants and depreciation.
2. **Actuals, forecasts and budgets must remain distinct.** The existing historical operating README identifies 2024-25 as a budget, whereas the fiscal overview displays updated 2024-25 consolidated figures. These two series are neither contemporaneous nor the same concept. A budget PDF can contain actual prior years, current forecasts, and future estimates. The document year alone cannot determine a row's status. Three-year capital-plan envelopes are overlapping promises, not annual delivered spending; never sum adjacent envelopes.
3. **A documented political timeline error requires correction in the new analysis.** `Data/alberta_fiscal_overview.md` marks 2018-19 as NDP/UCP and Notley/Kenney. Alberta's fiscal year ends 31 March; Kenney took office 30 April 2019, after the 2018-19 fiscal year. Treat 2019-20 as the transition year. The NDP took office 24 May 2015; 2015-16 is also a transition year. Fiscal shading is descriptive, not a causal attribution. “Start of conservative rule” means the UCP return in 2019 for this decade, since the PC government governed before 2015.
4. **The requested decade needs an explicit date basis.** As of 9 October 2026, the most recent ten completed fiscal years are 2016-17 through 2025-26. The ongoing year 2026-27 is not completed. If actual source coverage ends earlier, show the actual-data window and missing coverage explicitly; do not silently present 2015-16 to 2024-25 as the latest completed decade. A supplemental 2015-16 baseline may be useful to represent the first NDP budget.
5. **Spending flows do not establish asset stocks or service capacity.** Capital investment can replace worn assets, buy land or equipment, and fund repairs rather than grow capacity. Nominal net book value is reduced by amortization and reflects historical prices; it is not physical infrastructure volume. Capacity and delivery claims need commissioned facilities, enrolment spaces, staffed beds, road kilometres, housing units or other relevant units, with dates and comparability caveats.

## Normalization and inference

- Existing notebook population and CPI dictionaries are hard-coded, with no retrieval date, raw series snapshot, status or revision vintage. Validate against the same current Statistics Canada vintage throughout the new analysis. Population estimates are revised.
- The existing notebook describes its CPI inputs as calendar-year annual averages but cites monthly table 18-10-0004-01. Annual values can be derived from monthly observations; show aggregation explicitly or use the annual table. Use the fiscal-start calendar year consistently and disclose the approximation, or construct fiscal-year averages.
- Real per-capita formula: `nominal millions * 1,000,000 * CPI_reference / CPI_year / population`. Population growth and inflation compound; nominal spending merely matching either comparator alone is insufficient to maintain real per-person spending.
- CPI measures household purchasing power, not school/road/hospital construction input costs. A CPI-adjusted capital measure is a household-price benchmark. Construction deflator sensitivity is preferable if a suitable comparable series exists.
- Provincial total population is not the correct demand denominator for every asset: K-12 should use students; health should consider age and staffed capacity; roads should consider travel and geography. Population is a transparent common benchmark, not a capacity-needs model.
- Pandemic interruptions, commodity prices, interest rates, federal contributions, accounting changes and projects approved before 2019 limit partisan attribution. No causal claim follows from before/after differences or shaded party periods alone.

## Existing report statements unsuitable for reuse

- “Real per-capita operating expenditure ... service intensity” overstates what dollars alone show: costs, service mix and quality can change.
- The existing description of the nominal/real graph says the 2024-25 real total is about $3.5 billion below an alternative nominal amount; at the reference year, nominal and real must be equal by definition.
- “Approximately 95% ... attributable” lacks a specified decomposition rule for compound interactions. If such language is reused, define a log decomposition or counterfactual denominator.
- “All other years use actual (audited) figures” needs row-level proof; extracting a prior-year column from a budget is not by itself an audit-status check.

## Acceptance checks for the developed report

1. One row per fiscal year and clearly defined measure; row-level original official URL, document page, status, units, transcription/extraction method and checksums where available.
2. Annual capital total reconciled to components and/or its printed total; restatements and bridges retained instead of overwritten silently.
3. No forward budgets displayed as completed delivery; no cumulative sums of overlapping multi-year plans.
4. At least nominal, population-adjusted and CPI-adjusted spending views; all chart units, fiscal years, reference prices, endpoints, status and baseline explicit. Avoid dual axes that imply arbitrary visual relationships.
5. Key percentage claims independently recomputed from clean data; missing observations do not become zero.
6. Political boundary accurately placed; transition-year and inherited-project caveats adjacent to interpretation.
7. Physical outcome claims tied to independently sourced completion/capacity evidence; announcement, funding, construction and opening statuses differentiated.
8. Actual source coverage and inability to establish “all changes” stated plainly. A source-bounded inventory can be complete for its stated sources without claiming exhaustive provincial asset change.
9. Reproducible pipeline and concise README explain execution, source snapshots, data cleaning, joins, missingness, validation and remaining limits.
