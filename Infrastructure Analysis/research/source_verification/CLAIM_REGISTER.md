# Claim-to-source verification register

This register makes consequential claims in REPORT.md traceable to local official PDF pages. It is selective, not a claim that every sentence has been verified automatically. The links include exact extracted page text and original PDF pages. Locator anchors only detect a wrong page or changed extraction; arithmetic, definitions and interpretation still require source review.

For calculated spending comparisons, consult `data/baseline_comparisons.csv`, the executed notebook and independent Decimal checks in `tests/test_analysis.py`. Those calculations use F01 and F02; no physical-capacity conclusion follows from them.

## F01: Ten actual capital-plan observations

**Evidence type:** Financial input.

- [2024-2025 Budget.pdf, PDF p. 14](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=14) · [extracted page](pages/2024-2025%20Budget__pdf_page_14.txt)

**Interpretation limit:** Latest local vintage; historical accounting-policy changes remain.

[Supporting artifact](../../research/capital/latest_vintage_actual_series.csv)

## F02: July population and annual CPI inputs

**Evidence type:** Demographic / price input.

- [2024-2025 Budget.pdf, PDF p. 13](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=13) · [extracted page](pages/2024-2025%20Budget__pdf_page_13.txt)

**Interpretation limit:** Rounded demographic estimates; calendar timing and consumer prices do not measure construction volume.

[Supporting artifact](../../research/demography/demography_cpi_2015_2024.csv)

## F03: Capital grants and investment have different accounting treatment

**Evidence type:** Accounting definition.

- [2024-2025 Budget.pdf, PDF p. 16](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=16) · [extracted page](pages/2024-2025%20Budget__pdf_page_16.txt)

**Interpretation limit:** Grants fund assets outside provincial consolidation; do not add the full Capital Plan to expense.

## F04: Latest increase separates grants from investment

**Evidence type:** Financial decomposition.

- [2024-2025 Budget.pdf, PDF p. 3](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=3) · [extracted page](pages/2024-2025%20Budget__pdf_page_3.txt)

**Interpretation limit:** Grant growth is not automatically growth in provincially owned assets; neither component is physical capacity.

[Supporting artifact](../../research/capital/capital_composition_original_vintages.csv)

## F05: Municipal and health envelopes drive latest increase

**Evidence type:** Financial decomposition.

- [2024-2025 Budget.pdf, PDF p. 17](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=17) · [extracted page](pages/2024-2025%20Budget__pdf_page_17.txt)

**Interpretation limit:** Separate maintenance / self-finance; component rounding differs from total change by $1M.

[Supporting artifact](../../research/capital/actual_recent/recent_envelopes_all_vintages.csv)

## F06: Latest actual spending is below its budget

**Evidence type:** Budget execution.

- [2024-2025 Budget.pdf, PDF p. 17](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=17) · [extracted page](pages/2024-2025%20Budget__pdf_page_17.txt)

**Interpretation limit:** Undershoot is not proof of cancellation or permanent loss of funding.

[Supporting artifact](../../research/capital/budget_execution_original_vintage.csv)

## F07: Source pie has an inconsistent SUCH percentage

**Evidence type:** Source discrepancy.

- [2024-2025 Budget.pdf, PDF p. 16](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=16) · [extracted page](pages/2024-2025%20Budget__pdf_page_16.txt)
- [2024-2025 Budget.pdf, PDF p. 17](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=17) · [extracted page](pages/2024-2025%20Budget__pdf_page_17.txt)

**Interpretation limit:** 744/7243 is about 10.3%; the source percentage is not repeated as a valid share.

## F08: Source health-completion counts conflict internally

**Evidence type:** Source discrepancy.

- [2024-2025 Budget.pdf, PDF p. 15](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=15) · [extracted page](pages/2024-2025%20Budget__pdf_page_15.txt)
- [2024-2025 Budget.pdf, PDF p. 20](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=20) · [extracted page](pages/2024-2025%20Budget__pdf_page_20.txt)
- [2024-2025 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=23) · [extracted page](pages/2024-2025%20Budget__pdf_page_23.txt)

**Interpretation limit:** Use granular completed/in-progress and named-project evidence; retain the disagreement.

## F09: Historical nonfinancial row differs from gross balance-sheet amount

**Evidence type:** Accounting reconciliation.

- [2024-2025 Budget.pdf, PDF p. 12](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=12) · [extracted page](pages/2024-2025%20Budget__pdf_page_12.txt)
- [2024-2025 Budget.pdf, PDF p. 14](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=14) · [extracted page](pages/2024-2025%20Budget__pdf_page_14.txt)

**Interpretation limit:** Subtract spent deferred contributions; this is not a clean physical tangible-asset stock.

[Supporting artifact](../../review/stock_accounting_check.md)

## F10: Capital-asset investment is offset by amortization and other changes

**Evidence type:** Accounting reconciliation.

- [2024-2025 Budget.pdf, PDF p. 11](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=11) · [extracted page](pages/2024-2025%20Budget__pdf_page_11.txt)
- [2024-2025 Budget.pdf, PDF p. 3](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=3) · [extracted page](pages/2024-2025%20Budget__pdf_page_3.txt)

**Interpretation limit:** Book value is not physical capacity. The $4.309B plan flow is not reconciled to the rounded $3.9B asset narrative in this summary; no exact gap or cause is asserted.

[Supporting artifact](../../research/capital/INVESTMENT_TO_ASSET_ROLLFORWARD_GAP.md)

## F11: MSI grants were advanced into the pre-UCP spending peak

**Evidence type:** Timing / policy context.

- [2017 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2017%20Budget.pdf#page=23) · [extracted page](pages/2017%20Budget__pdf_page_23.txt)
- [2018-19 Budget.pdf, PDF p. 10](../../../Budget%20PDFs/2018-19%20Budget.pdf#page=10) · [extracted page](pages/2018-19%20Budget__pdf_page_10.txt)

**Interpretation limit:** Advanced cash transfers are not construction all delivered in that year.

## F12: 2019 capital-grant total was reclassified into operating expense

**Evidence type:** Accounting revision.

- [2020-21 Budget.pdf, PDF p. 2](../../../Budget%20PDFs/2020-21%20Budget.pdf#page=2) · [extracted page](pages/2020-21%20Budget__pdf_page_2.txt)

**Interpretation limit:** The reclassification is not an additional $19M infrastructure cut.

[Supporting artifact](../../research/capital/early_ucp_comparisons.md)

## F13: 2018 ministry attribution changed

**Evidence type:** Accounting revision.

- [2018-19 Budget.pdf, PDF p. 2](../../../Budget%20PDFs/2018-19%20Budget.pdf#page=2) · [extracted page](pages/2018-19%20Budget__pdf_page_2.txt)

**Interpretation limit:** A ministry row is not a stable functional-sector series.

## P01: 2024 school spaces mix new and modernized

**Evidence type:** Physical output.

- [2024-2025 Budget.pdf, PDF p. 20](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=20) · [extracted page](pages/2024-2025%20Budget__pdf_page_20.txt)

**Interpretation limit:** Completed gross/mixed spaces and the pipeline are distinct; neither is reconciled net seats.

## P02: 2021 school new spaces are separately reported

**Evidence type:** Physical output.

- [2021-22 Budget.pdf, PDF p. 20](../../../Budget%20PDFs/2021-22%20Budget.pdf#page=20) · [extracted page](pages/2021-22%20Budget__pdf_page_20.txt)

**Interpretation limit:** Gross new seats cannot be compared with a mixed new/modernized total.

## P03: 2018 supportive-living construction added reported spaces

**Evidence type:** Physical output.

- [2018-19 Budget.pdf, PDF p. 10](../../../Budget%20PDFs/2018-19%20Budget.pdf#page=10) · [extracted page](pages/2018-19%20Budget__pdf_page_10.txt)

**Interpretation limit:** Selected gross long-term-care additions do not reconcile provincial closures or staffing.

[Supporting artifact](../../research/physical/round2/explicit_capacity_observations.csv)

## P04: Grande Prairie hospital has separately completed phases

**Evidence type:** Project stage.

- [2020-21 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2020-21%20Budget.pdf#page=23) · [extracted page](pages/2020-21%20Budget__pdf_page_23.txt)
- [2021-22 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2021-22%20Budget.pdf#page=23) · [extracted page](pages/2021-22%20Budget__pdf_page_23.txt)

**Interpretation limit:** Do not count combined multiyear project funding twice or infer net provincial staffed beds.

[Supporting artifact](../../research/physical/health/health_project_evidence.csv)

## P05: Calgary cancer construction completion differs from anticipated opening

**Evidence type:** Project stage.

- [2022-2023 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2022-2023%20Budget.pdf#page=23) · [extracted page](pages/2022-2023%20Budget__pdf_page_23.txt)

**Interpretation limit:** The anticipated public-opening date in this source is not a verified actual opening date.

## P06: Misericordia emergency design volume is not observed throughput

**Evidence type:** Design capacity.

- [tbf-goa-2023-2024 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/tbf-goa-2023-2024%20Budget.pdf#page=23) · [extracted page](pages/tbf-goa-2023-2024%20Budget__pdf_page_23.txt)

**Interpretation limit:** Designed visits per year do not establish actual visits, waits or net beds.

## P07: High Prairie completed project introduced dialysis stations

**Evidence type:** Physical output.

- [2021-22 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2021-22%20Budget.pdf#page=23) · [extracted page](pages/2021-22%20Budget__pdf_page_23.txt)

**Interpretation limit:** Local gross delivery, not net provincial station growth or treatment volume.

## P08: Open recovery communities are distinct from planned beds

**Evidence type:** Operational stock / pipeline.

- [2024-2025 Budget.pdf, PDF p. 15](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=15) · [extracted page](pages/2024-2025%20Budget__pdf_page_15.txt)

**Interpretation limit:** Do not double-count Gunn; addiction treatment beds are not acute hospital beds.

## P09: Bow River westbound bridge expands by one lane

**Evidence type:** Physical output.

- [2024-2025 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=23) · [extracted page](pages/2024-2025%20Budget__pdf_page_23.txt)

**Interpretation limit:** Local corridor improvement does not supply provincial net lane kilometres.

## P10: Road-network stock unit labels differ across reports

**Evidence type:** Source comparability gap.

- [tbf-goa-2023-2024 Budget.pdf, PDF p. 20](../../../Budget%20PDFs/tbf-goa-2023-2024%20Budget.pdf#page=20) · [extracted page](pages/tbf-goa-2023-2024%20Budget__pdf_page_20.txt)
- [2024-2025 Budget.pdf, PDF p. 20](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=20) · [extracted page](pages/2024-2025%20Budget__pdf_page_20.txt)

**Interpretation limit:** No network-growth rate is derived from the inconsistent labels.

## P11: Springbank reservoir is flood protection

**Evidence type:** Project stage.

- [2024-2025 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=23) · [extracted page](pages/2024-2025%20Budget__pdf_page_23.txt)

**Interpretation limit:** Construction completion does not establish operational certification or drinking-water capacity.

## P12: Housing completions and pipeline are separately stated

**Evidence type:** Physical output / pipeline.

- [2024-2025 Budget.pdf, PDF p. 20](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=20) · [extracted page](pages/2024-2025%20Budget__pdf_page_20.txt)

**Interpretation limit:** Gross deliveries are not net housing stock after removals, ownership or eligibility changes.

## P13: Rural project basket includes transport and water

**Evidence type:** Financial support.

- [2024-2025 Budget.pdf, PDF p. 15](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=15) · [extracted page](pages/2024-2025%20Budget__pdf_page_15.txt)

**Interpretation limit:** Not 125 water projects or 125 completed projects.

## P14: MSI to LGFF program change is a narrow grant comparison

**Evidence type:** Financial support.

- [tbf-goa-2023-2024 Budget.pdf, PDF p. 16](../../../Budget%20PDFs/tbf-goa-2023-2024%20Budget.pdf#page=16) · [extracted page](pages/tbf-goa-2023-2024%20Budget__pdf_page_16.txt)
- [2024-2025 Budget.pdf, PDF p. 15](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=15) · [extracted page](pages/2024-2025%20Budget__pdf_page_15.txt)

**Interpretation limit:** Not all municipal funding or a measure of local asset delivery.

## P15: Broadband financial allocation is not connected households

**Evidence type:** Financial input.

- [2024-2025 Budget.pdf, PDF p. 17](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=17) · [extracted page](pages/2024-2025%20Budget__pdf_page_17.txt)

**Interpretation limit:** Verified connections and service quality are absent from this cited financial row.

## P16: Project completion definition changes over time

**Evidence type:** Source comparability gap.

- [2021-22 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2021-22%20Budget.pdf#page=23) · [extracted page](pages/2021-22%20Budget__pdf_page_23.txt)
- [2024-2025 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=23) · [extracted page](pages/2024-2025%20Budget__pdf_page_23.txt)

**Interpretation limit:** Reported completed-year series does not consistently measure operational opening.

## P17: Older school overview reports separate new and modernized spaces

**Evidence type:** Physical output.

- [2017 Budget.pdf, PDF p. 93](../../../Budget%20PDFs/2017%20Budget.pdf#page=93) · [extracted page](pages/2017%20Budget__pdf_page_93.txt)

**Interpretation limit:** Selected September 2017 context; not a reconciled net-seat series or political productivity ratio.

[Supporting artifact](../../research/physical/gaploop/additional_indicators.csv)

## P18: 2022 source reports gross continuing-care completions

**Evidence type:** Physical output.

- [2022-2023 Budget.pdf, PDF p. 15](../../../Budget%20PDFs/2022-2023%20Budget.pdf#page=15) · [extracted page](pages/2022-2023%20Budget__pdf_page_15.txt)

**Interpretation limit:** Broader care scope differs from earlier long-term-care figures; closures and staffing unknown.

## P19: Highway 19 source reports a specific twinned route segment

**Evidence type:** Physical output.

- [tbf-goa-2023-2024 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/tbf-goa-2023-2024%20Budget.pdf#page=23) · [extracted page](pages/tbf-goa-2023-2024%20Budget__pdf_page_23.txt)

**Interpretation limit:** Route kilometres, not lane kilometres or provincial net-network additions.

## P20: Red Deer Justice Centre has reported courtroom capacity

**Evidence type:** Design / facility capacity.

- [tbf-goa-2023-2024 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/tbf-goa-2023-2024%20Budget.pdf#page=23) · [extracted page](pages/tbf-goa-2023-2024%20Budget__pdf_page_23.txt)

**Interpretation limit:** Gross facility capacity; predecessor courtroom retirements unknown.

## P21: Conklin construction describes fifteen housing units

**Evidence type:** Physical output.

- [2024-2025 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2024-2025%20Budget.pdf#page=23) · [extracted page](pages/2024-2025%20Budget__pdf_page_23.txt)

**Interpretation limit:** Units are not buildings; no provincial net-stock or household-demand conclusion.

## P22: Northern Lights supply pipeline has a reported route length

**Evidence type:** Physical output.

- [2021-22 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2021-22%20Budget.pdf#page=23) · [extracted page](pages/2021-22%20Budget__pdf_page_23.txt)

**Interpretation limit:** Local supply-line length, not connected-household or production-capacity count.

## P23: Government data centres were consolidated

**Evidence type:** Digital infrastructure change.

- [2020-21 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2020-21%20Budget.pdf#page=23) · [extracted page](pages/2020-21%20Budget__pdf_page_23.txt)

**Interpretation limit:** Fewer centres do not mean lower digital service capacity; observed service outcomes unavailable.

## P24: Quest had operating evidence before its later completed-status listing

**Evidence type:** Source comparability gap.

- [2016-2017 Budget.pdf, PDF p. 17](../../../Budget%20PDFs/2016-2017%20Budget.pdf#page=17) · [extracted page](pages/2016-2017%20Budget__pdf_page_17.txt)
- [2021-22 Budget.pdf, PDF p. 23](../../../Budget%20PDFs/2021-22%20Budget.pdf#page=23) · [extracted page](pages/2021-22%20Budget__pdf_page_23.txt)

**Interpretation limit:** A completed-status list is not always a list of first completions during the fiscal year.

[Supporting artifact](../../research/physical/gaploop/completion_year_audit.md)

## F14: ARO adoption revised asset book values

**Evidence type:** Accounting policy change.

- [2022-2023 Budget.pdf, PDF p. 2](../../../Budget%20PDFs/2022-2023%20Budget.pdf#page=2) · [extracted page](pages/2022-2023%20Budget__pdf_page_2.txt)

**Interpretation limit:** Accounting value revision is not automatically a physical infrastructure addition.

## F15: P3 adoption revised opening book values without comparable restatement

**Evidence type:** Accounting policy change.

- [tbf-goa-2023-2024 Budget.pdf, PDF p. 2](../../../Budget%20PDFs/tbf-goa-2023-2024%20Budget.pdf#page=2) · [extracted page](pages/tbf-goa-2023-2024%20Budget__pdf_page_2.txt)

**Interpretation limit:** Accounting value revision is not automatically demolished infrastructure.

## P25: Lethbridge science replacement has an explicitly dated completion

**Evidence type:** Dated physical delivery.

- [2019-20 Budget.pdf, PDF p. 19](../../../Budget%20PDFs/2019-20%20Budget.pdf#page=19) · [extracted page](pages/2019-20%20Budget__pdf_page_19.txt)

**Interpretation limit:** Replacement does not quantify net student seats or capacity relative to enrolment.

