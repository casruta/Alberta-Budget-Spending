# Improvement loop: budget execution, grants and revisions

## Reproducible additions

Run `extract_execution_composition.py` after the primary extractor. It reads the capital-plan section of each fiscal summary; explicitly includes Climate Leadership Plan capital grants/investment separately reported in 2017–18; checks components against the total within $1M; preserves budget, actual and prior-actual columns; and writes:

- `budget_execution_original_vintage.csv`: ten fiscal years, source-report budget comparisons, contemporary actuals, latest-vintage actuals, execution percentages and revision differences.
- `capital_composition_original_vintages.csv`: thirty rows, grant and investment amounts for the budget/current/prior columns in each report. `observation_fiscal_year` identifies the year measured, while `source_vintage` and legacy `fiscal_year` identify the reporting year. Never join prior-actual rows on the reporting year.
- `adjacent_vintage_revision_ledger.csv`: nine previous-year comparisons to their first revised annual-report vintage, with changes separately for total/grants/investment.
- `execution_composition_source_manifest.json`: ten source hashes, exact fiscal-summary PDF pages, PDF titles/authors.
- `.composition_summary_page*.txt`: preserved source page text.

A dash inside an otherwise present five-cell accounting row is the source nil convention and may be represented as zero. An absent source row or missing observation is retained as missing (`None`), never imputed as zero.

Use the source **budget column as published in each final-results report**, which can reflect accounting/presentation restatements. This is not independently reconstructed original appropriation authority or the last forecast. Use contemporary actual with its paired budget; do not substitute latest revised actual into original-vintage execution ratios without reconstructing budget comparability.

## Annual execution panel

| Fiscal year | Budget $M | Contemporary actual $M | Actual minus budget $M | Execution |
|---|---:|---:|---:|---:|
| 2015–16 | 7,863 | 6,558 | −1,305 | 83.4% |
| 2016–17 | 8,481 | 6,578 | −1,903 | 77.6% |
| 2017–18 | 9,175 | 9,016 | −159 | 98.3% |
| 2018–19 | 6,444 | 6,180 | −264 | 95.9% |
| 2019–20 | 6,206 | 5,564 | −642 | 89.7% |
| 2020–21 | 6,960 | 6,896 | −64 | 99.1% |
| 2021–22 | 8,114 | 6,622 | −1,492 | 81.6% |
| 2022–23 | 7,534 | 5,644 | −1,890 | 74.9% |
| 2023–24 | 8,005 | 6,300 | −1,705 | 78.7% |
| 2024–25 | 8,299 | 7,243 | −1,056 | 87.3% |

This corroborates repeated cash-flow revisions before and after April 2019. The lowest reported execution is 2022–23, 74.9%; the last year improved to87.3%, but remained below the annual budget. These are descriptive comparisons, not procurement efficiency scores or causal political rankings. Annual shortfalls must not be summed and labeled infrastructure backlog: postponed spending can appear in later budgets and actuals.

**2020–21 aggregate near-budget spending masks a materially altered project mix.** Source PDF p16 says the Capital Plan was revised substantially with $1.1B COVID/recovery support added. p18 lists $627M municipal stimulus grants, $475M accelerated maintenance/renewal, $46M health equipment and $15M strategic projects (rounded components), offset by $329M reduced SUCH self-financed investment, $419M federal project re-profiling and other timing shifts. Thus99.1% total execution does not establish delivery of the original project schedule.

Other source mechanisms:2016–17 p20 notes weather/Wood Buffalo wildfire/federal eligibility/partner delays and reduced costs;2018–19 p9 removes a budgeted$391M cash-flow adjustment as intended;2022–23 p17 notes LRT delays, health site/servicing agreements, capital planning, material/equipment delays;2023–24 p17 describes health scheduling, roads/tender delays and municipal/water projects. Latest2024–25 details are in `early_ucp_comparisons.md`.

## Composition explains the latest rebound

Latest PDF p3 same-vintage2023–24→2024–25:

- Capital grants2,103→2,934M: **+$831M**.
- Capital investment4,197→4,309M: **+$112M**.
- Total6,300→7,243M: **+$943M**, exactly reconciled.

Therefore capital grants account for **88.1% of the latest net spending increase**, versus11.9% for capital investment. Grants' share of total spending rose33.4%→40.5%. This does **not** mean grants lack infrastructure value: they can fund municipal and partner assets. It does explain why financial spending growth cannot be equated one-for-one with increased provincially consolidated asset value.

Longer composition ratios may be shown only as **original report-vintage descriptors** with an accounting warning; they are not a fully harmonized grant/asset-investment panel. The2017–18 spike included4,017M capital grants when the separately reported394M Climate Leadership Plan grants are included. Omitting that separate row would understate capital transfers and fail total reconciliation.

## Adjacent-vintage revisions and unresolved causes

- **2017–18 +$5M**:9,016→9,021 total in next report.2018–19 p2 explicitly corrects$5M Service Alberta operating expense into capital grants. Displayed component revisions are grants+4M and investment+1M, consistent rounded values.
- **2018–19 −$123M**:6,180→6,057. Grant amount1,952M unchanged; investment4,228→4,105M. This exact specific correction is not explained in the accessible2019–20 narrative. **Do not claim the−$123M is explained by the contemporaneous2018–19 Infrastructure/Education/Health attribution transfer**, which primarily reallocates construction among ministries. The correction must remain an unresolved comparability limitation.
- **2019–20 −$19M**:5,564→5,545.2020–21 p2 explicitly moves$19M capital grants into operating expense across Education,Infrastructure,Service Alberta,Transportation; total expense/debt unchanged. Displayed grants decrease1,696→1,678M(−18M), investment remains3,868M, component/total difference$1M is rounding.
- **2022–23 −$11M**:5,644→5,633. Grants1,536→1,525M(−11M);investment4,108M unchanged.2023–24 p2 records ministry-organization and accounting-standard changes, but does not isolate this grant correction. Exact cause remains unresolved.
- Other adjacent aggregate totals unchanged, which does not guarantee unchanged ministry attribution or stock-accounting definitions.

Stock effects can occur without a capital-plan flow revision.2022–23 p2 says adoption of Asset Retirement Obligations restated2021–22 tangible capital assets **+$692M** and amortization+$29M, while the capital-plan flow6,622M is unchanged.2023–24 p2 says adoption of P3 accounting decreased opening tangible-capital net book value **$415M** and P3 liabilities$353M without restating prior comparatives. These are accounting changes, not automatically buildings added/demolished. The report's general structural-break warning should be retained.

## Targets for independent review

1. Check all ten fiscal-summary page capital sections and5-column interpretation directly against the PDFs.
2. Verify2017–18 separately reported CLP grants394 and investment25 are included in current actual composition.
3. Verify2023–24 budget8,005M (not7,537M), actual6,300M, variance−1,705M.
4. Check latest grants831+investment112=total943 and grant-growth contribution88.1%.
5. Review2020–21 p16/p18 to ensure near-budget execution is not described as an unchanged project program.
6. Ensure2018–19−123M and2022–23−11M revisions are not assigned invented causes.
7. Check the report does not convert cumulative under-budget amounts into a service need/backlog or sum budget and actuals as separate expenditures.
