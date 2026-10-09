# Demographic and CPI evidence-gap review: additional validation loop

## New evidence archived

`build_vintage_ledger.py` now reproduces `population_cpi_cross_vintage_ledger.csv` and `cross_vintage_revision_summary.csv` from seven existing official Final Results reports, with source filenames and exact PDF page numbers. Covers final-results vintages 2018-19 through 2024-25. These are local source observations; no remote retrieval or new population observations are claimed. Cover inspection independently verifies that the misleading `Budget.pdf` filenames identify **year-end Final Results**, not forecast budgets.

**Every overlapping annual CPI growth rate for 2015–2024 agrees across all available report vintages.** In particular, 2021 remains 3.2%, 2022 remains 6.4%, 2023 remains 3.3%, and 2024 is 2.9% in its sole local report. Thus available official-report evidence does not support explaining the notebook's materially different implied CPI growth rates as ordinary revisions in these published annual growth rates. The notebook may be using another timing or index concept, but it does not archive evidence establishing that interpretation. It should not supply inflation inputs to the infrastructure analysis.

By contrast, population histories visibly change across vintages:

| July year | Minimum across local vintages | Maximum | Range, persons | Latest local vintage |
|---|---:|---:|---:|---:|
| 2015 | 4,144,000 | 4,150,000 | 6,000 | 4,150,000 |
| 2018 | 4,293,000 | 4,307,000 | 14,000 | 4,293,000 |
| 2019 | 4,355,000 | 4,371,000 | 16,000 | 4,355,000 |
| 2022 | 4,511,000 | 4,543,000 | 32,000 | 4,511,000 |
| 2023 | 4,685,000 | 4,695,000 | 10,000 | 4,685,000 |
| 2024 | 4,889,000 | 4,889,000 | not measurable: one report | 4,889,000 |

The ranges are **between observed local report vintages**, not confidence intervals or total revision bounds. No claim is made about future revisions or unseen vintages. Multiple-thousand differences exceed the ±500-person rounding convention; therefore rounding and vintage uncertainty must remain separate.

## Calculations that improve inference

With source spending, CPI and the latest 2024 population held fixed, replacing only the 2018 baseline population by its largest observed historical-vintage value shifts the CPI-adjusted change from **−12.5891% to −12.3040%**. Doing the corresponding isolated replacement for 2019 shifts **−1.3955% to −1.0332%**. These are transparent **mixed-vintage sensitivity scenarios**, not recommended re-estimates: they isolate one observed historical population revision without representing a consistent new population series. Neither observed-baseline scenario reverses direction, although this does not bound revisions in the 2024 endpoint.

For 2022, the observed 32,000-person historical range similarly moves the 2022-to-2024 recovery from **+11.6133% to +12.4050%**, holding other inputs fixed. This is materially larger than deterministic rounded-input uncertainty and demonstrates why the report should avoid decimal precision in headline claims.

The rounded CPI chain is independently corroborated but fiscal timing remains untested. Seven annual reports repeatedly reporting the same **calendar-year** growth rates cannot validate an April–March CPI average. Nor can seven July-population histories establish a fiscal-average quarterly denominator. Treat this as a distinct missing-data requirement, not another source-vintage error.

The pre-UCP 2018 comparison requires only **5.0030% cumulative hypothetical appropriate-price inflation** to produce zero price-adjusted per-resident growth; observed consumer inflation is 20.1257%. The meaningful unresolved issue is choosing and recovering a compatible construction-price series, not further numerical refinement of the rounded CPI arithmetic. For the small 2019 comparison, fiscal timing and choice of deflator can materially affect whether “roughly unchanged” is the best characterization; preserve that caution.

## Material qualifications recommended for the report

1. Keep **same-vintage population** for the main series and explicitly label the figures as demographic estimates rounded to thousands. Existing report text already does this.
2. Treat rounded-input bounds as arithmetic only. They omit demographic revision uncertainty; the new ledger supplies observed evidence of such revisions.
3. Retain **calendar-year CPI sensitivity**, rather than construction purchasing power or real infrastructure volume. The observed agreement across vintages strengthens the chosen annual rates but does not correct fiscal alignment or sector mismatch.
4. Use one-decimal headline changes and rounded money/population. Fine decimal outputs belong in reproducibility files.
5. Retain the **2019 baseline timing caveat** and prioritize the last full pre-UCP 2018-19 baseline. No additional spending, staffing or capacity conclusions follow from this demographic audit.
6. Avoid saying 2024 population uncertainty is zero: only one local vintage provides that year. Absence of an observed revision is not evidence of exactness.

No blocking error was found in the integrated analysis. New ledger evidence improves why the report prefers one report vintage and limits rounding bounds. The original tracked repository files and root-owned analysis scripts were not changed.
