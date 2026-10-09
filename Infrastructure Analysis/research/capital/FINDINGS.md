# Capital spending source research

## Primary series and source identity

Use `latest_vintage_actual_series.csv`, reproducibly extracted with `extract_primary.py` from the supplied `Budget PDFs/2024-2025 Budget.pdf`. Despite its filename, PDF metadata identifies **2024–25 Final Results – Year-end Report**, author Government of Alberta – Treasury Board and Finance, created June 25, 2025. PDF page 14 (printed page 14), Historical Fiscal Summary 2013–14 to 2024–25, supplies a single-vintage **actual** Capital Plan series. PDF p13 supplies annual CPI inflation and July 1 population in thousands. Official publication landing URL provided in these documents is https://www.alberta.ca/government-and-ministry-annual-reports . Original online PDF URL is unverified: official network requests returned proxy 403, so local document identity and SHA256—not an invented URL—establish provenance.

2015–16 to 2024–25 actual Capital Plan spending, $million: **6,558; 6,578; 9,021; 6,057; 5,545; 6,896; 6,622; 5,633; 6,300; 7,243**.

The table's footnotes say numbers are not strictly comparable owing to accounting-policy changes. Capital Plan reflects capital grants and other support included in expense plus capital investment in government-owned assets excluded from expense; asset investment is depreciated over time. It is a spending flow, not the Ministry of Infrastructure operating expense, not total government expense, and not physical infrastructure capacity.

`local_manifest.json` supplies original local paths, hashes and candidate pages. `latest_history_page14.txt` and `latest_history_page13.txt` preserve source evidence. Fiscal and economic years differ: population is July 1 of the fiscal-start calendar year; CPI rate is calendar-year average-price growth. These provide a transparent approximate fiscal denominator/deflator, not a precisely aligned fiscal-year population average or construction-price index.

## Revisions and budget-vs-actual

Prefer primary same-vintage actuals for longitudinal charts. Contemporary total actuals differ: 2017–18 9,016 vs latest 9,021; 2018–19 6,180 vs latest 6,057; 2019–20 5,564 vs latest 5,545; 2022–23 5,644 vs latest 5,633. Do not replace old actuals with budget-column figures. PDF headings often show budget, current actual, prior actual, change from budget, change from prior actual.

Contemporaneous annual Budget/Actual totals ($million) for execution comparisons: 2015–16 7,863/6,558 (PDF p18); 2016–17 8,481/6,578 (p20); 2017–18 9,175/9,016 (p22); 2018–19 6,444/6,180 (p9); 2019–20 6,206/5,564 (p15); 2020–21 6,960/6,896 (p18); 2021–22 8,114/6,622 (p17); 2022–23 7,534/5,644 (p17); 2023–24 8,005/6,300 (p16 ministry table; p17 envelopes); 2024–25 8,299/7,243 (p17). The 2023–24 budget was corrected from a provisional transcription using the independently extracted current-year source table; the provisional value was not used in the main report or figures.

2017–18 spike partly reflects municipal transportation and other grants accelerated from future years (2017 report PDF p22; 2018–19 report p9). Its subsequent decline began in 2018–19, before UCP assumed government in spring 2019. Later source reports explain repeated underspending through project scheduling, planning, weather, procurement, COVID and supply chains. These facts preclude attributing all post-2019 changes to party control.

## Ministry attribution and secondary files

2018–19 Final Results PDF p2 and p9 explicitly changed attribution: Infrastructure reported capital construction managed for school boards/AHS; +$420m Infrastructure, –$134m Education, –$285m Health (rounded). The source says budget/prior actuals were not restated and ministry changes were not comparable. Climate Leadership Plan and flood spending also appeared separately in early years. **Do not equate ministry capital rows with stable functional sectors.**

`ministry_capital_verified_2019_2021.csv` gives 2019–20 through 2021–22 reported ministry detail only. Row sums differ from contemporary total by –$1m, $0m, $0m respectively, consistent with rounding. Early automated rows are quarantined in `ministry_capital_contemporaneous_2015_2021_DRAFT_DO_NOT_USE.csv`; malformed/split labels failed aggregate reconciliation and are unsuitable for analysis. Raw evidence remains available for manual repair.

`infrastructure_ministry_operating.csv` provides contemporaneous ministry operating expense, a separate measure subject to ministry reorganization. For example, 2022–23 Infrastructure operating expense 431 was restated as 447 in the following report; 2017–18 500 later became 490. It must not be treated as a definitive unadjusted like-for-like infrastructure-investment series.

Recent functional envelope detail and revised comparisons are in `actual_recent/`, extracted by the bounded subagent. Their FINDINGS explains reclassifications and rounding. Preserve original labels and use latest comparative vintages carefully.

## Asset stock caveat and coverage

Historical `net_capital_nonfinancial_assets_after_deferred_contributions_million` is book-value **capital plus other nonfinancial assets minus spent deferred capital contributions**, not strictly tangible infrastructure. Adoption of asset-retirement obligations restated 2021–22 opening values. Its nominal/per-capita growth cannot establish physical infrastructure adequacy or completed capacity. The latest report p11 describes about $61.7 billion capital assets; pp11–12 also describe other nonfinancial assets, including inventory, prepaid expenses and purchased intangibles. The p12 table aggregates capital and other nonfinancial assets rather than presenting a pure tangible-infrastructure inventory.

The ten-year window is complete for 2015–16 through 2024–25. No 2025–26 actual report is locally supplied. As of task date October 9, 2026, inability to check official sites means **publication status is unknown**; do not claim it has not been published or is still only a budget.
