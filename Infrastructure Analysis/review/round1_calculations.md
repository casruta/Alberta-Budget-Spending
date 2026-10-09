# Independent review, round 1: source and calculations

Reviewed 9 October 2026. Evidence: directly opened original PDFs with pdfplumber, manually transcribed page 13 demographic inputs and page 14 capital rows of the June 2025 **2024–25 Final Results Year-End Report**, then computed using standard Python independently of `scripts/analyze.py`. The misleading local filename `2024-2025 Budget.pdf` does not identify the document type. Independent assertions are retained in `review/independent_calculation_check.py`.

## Result: arithmetic passes; interpretative caveats required

All ten annual capital amounts, July 1 populations and calendar CPI growth rates match the source. Independently recomputed all ten CPI-adjusted per-resident values; tested three principal baselines and four weighted period averages. All comparisons match to numerical precision.

| Baseline → 2024–25 | Nominal capital | Population | Chained consumer prices | CPI-adjusted per resident |
|---|---:|---:|---:|---:|
| 2015–16 | +10.4453% | +17.8072% | +26.3516% | −25.8016% |
| 2018–19 | +19.5807% | +13.8831% | +20.1257% | −12.5891% |
| 2019–20 | +30.6222% | +12.2618% | +18.0017% | −1.3955% |

The CPI chain correctly excludes the growth rate for the baseline calendar year. For 2018→2024 it compounds 2019–2024 rates. CPI inflation is not a sum of annual percentage changes. The deterministic bounds in `analyze.py` correctly apply ±0.05 percentage points to one-decimal CPI growth, ±500 residents to population rounded to thousands, and ±0.5 million dollars to capital rounded to millions. These are quantization bounds, not statistical confidence intervals; exact original prices, revisions and construction costs remain outside them.

Population weighting passes: `sum(real annual dollars)/sum(annual residents)`, equivalently a population-weighted mean of annual per-person values. Results: pre-UCP $2,066.948; UCP $1,532.123; pre-UCP excluding 2017–18 $1,881.875; recent three years $1,399.598. The descriptive UCP/pre-UCP ratio is −25.8751%, or −18.5853% versus the spike-excluded comparison. These unequal windows are not a matched policy comparison, and total multi-year dollars are not comparable without duration adjustment.

## Required interpretation corrections / warnings

**High severity: source explicitly warns about comparability.** Historical table p14 footnote a states: “Numbers are not strictly comparable due to numerous accounting policy changes over time.” Same-report vintage reduces accidental splicing but does not eliminate this official warning. Preserve this near the main result. The footnote specifically reclassifies 2019–20 and 2021–22 expense by function; do not imply those function reclassifications necessarily changed the Capital Plan total. Footnote b defines Capital Plan as capital grants and other support already in expense, plus government-owned capital investment outside expense. Consequently do not add total capital to total expense as a new total.

**High severity: grants reflect funding timing, not municipal construction timing.** `2017 Budget.pdf` is actually the **2017–18 Annual Report**. PDF p23 / printed p21 identifies $1,648 million Municipal Sustainability Initiative grants, **including $800 million reprofiled from future years**. PDF p11 / printed p9 states municipal funding was moved forward to increase flexibility. Excluding the whole 2017–18 observation is an outlier sensitivity, not an accounting correction: ordinary spending is removed too, and the shifted future-year amounts are not restored to their originally intended years. Do not call the exclusion a grant-timing-adjusted series or assign the entire $2.443 billion increase to the $800 million item. Capital grants rose $1.856 billion in that report's original presentation, and capital investment also changed.

**Medium severity: classify updated actuals, not audited amounts by implication.** June 2025 final-results tables label these amounts Actual; the yearly infrastructure appendix is not itself a financial audit opinion. Prefer “official reported actuals” unless the capital measure is reconciled to the audited financial statement schedules.

**Medium severity: source population is report vintage.** 2024 is 4.889 million in this report, not the original notebook's 4.909 million. Do not combine with original hard-coded dictionary. July 1 fiscal-start calendar population and annual CPI do not exactly align with April–March cash flows. The reported precision is limited; round headline percentages to one decimal and amounts appropriately.

**Medium severity: pandemic and inherited contracts.** The UCP window spans COVID, the oil shock, construction timing and high inflation. Six annual observations do not isolate a government effect. Opening a facility during one administration does not establish who initiated, funded or built its full project; establish project milestones separately.

## Restatement checks

- 2024–25 source p2: 2023–24 Actual and 2024–25 Budget/Actual reclassified to revised government structure and health changes; 2023–24 Alberta Enterprise Corporation revenue/expense reclassification $5.85 million. The p17 sector pair is therefore valid for same-vintage sector changes, not automatically comparable to older envelope labels.
- 2024–25 source p14 footnote d: 2021–22 opening balance restated for Asset Retirement Obligations; financial-instrument standards from 2022–23 add unrealized remeasurement effects to net assets outside surplus/deficit. This limits interpretation of balance-sheet trends.
- 2018–19 Final Results p2: 2017–18 Service Alberta operating expense reclassified to capital grants $5 million. Its p3 updates 2017–18 Capital Plan to $9,021 million versus $9,016 million in the original 2017–18 report. Latest vintage appropriately uses $9,021.
- 2018–19 Final Results p2: $420 million capital investment moved to Infrastructure for assets managed on behalf of school boards and AHS; corresponding Education −$134 million and Health −$285 million, rounding difference. Ministry totals are affected by administrative transfer rather than capacity.
- Original 2018–19 final report p3 Capital Plan total is $6,180 million, whereas latest historical table is $6,057 million. The latest series is consistently applied, but the exact bridge requires later restatement evidence; do not explain the full difference without a source.

## Recommendation

Proceed with the verified descriptive results using 2018–19 as last full pre-UCP baseline and showing 2015–16 and 2019–20 alongside it. The decrease from 2019–20 is much smaller, making baseline disclosure essential. Maintain the last-completed-decade coverage gap and distinguish capacity evidence, grant flows, maintenance, net book values and announced budgets throughout the report.
