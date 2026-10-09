# Second-loop independent audit: new composition, execution and demography panels

Reviewed9 October2026. Original PDFs opened independently withpdfplumber; values and calculations checked independently of the extractors. Reviewer edits confined toreview/.

## Correction to this review

A prior version of this memo incorrectly called1.4B the COVID/recovery addition. Direct reinspection confirms1.1B in PDFp16;1.4B on p18 is rounded year-over-year growth, not the recovery addition. The budget-comparator caveat remains valid.

## Material archive correction required

`research/demography/build_vintage_ledger.py` extracts CPI numeric tokens with a regex that discards parentheses. Original2018–19 Final Results PDFp14 gives calendar2009 CPI growth **(0.1)**, meaning **−0.1%**. The raw cross-vintage ledger stores+0.1. This affects an out-of-primary-window archive row, not2015–2024 headline results or summary. Correct token parsing to retain parenthetical negative sign and add a source-anchored regression check; do not silently drop genuine negative inflation. No need to recalculate the main financial series for this out-of-window issue.

## Capital panel findings

Actual filenames reviewed:

- `research/capital/budget_execution_original_vintage.csv`:10 fiscal rows.
- `research/capital/capital_composition_original_vintages.csv`:30 budget/current/prior observations.
- `research/capital/extract_execution_composition.py`:source list, page anchors, CAPITAL PLAN block matching and component aggregation.

All10 execution ratios, actual-minus-budget values, vintage differences and30 component reconciliation/share calculations pass independently. Original source anchors match internal report tables.2015–2017 PDF pages contain other cash-requirement tables on the same page; the extractor correctly isolates CAPITAL PLAN rows rather than cash adjustments. The2017–18 Climate Leadership Plan grants394M and investment25M are correctly included in component totals4017M and4999M, rather than lost or double counted.

### Latest grant/investment decomposition

Original2024–25 Final Results PDFp3:

| Component | Revised2023–24actualM |2024–25actualM | ChangeM |
|---|---:|---:|---:|
|Capital grants|2103|2934|+831|
|Capital investment|4197|4309|+112|
|Capital Plan|6300|7243|+943|

Arithmetic831+112=943. Grants account for88.123% of the net rebound; investment11.877%. This is a financing/accounting composition decomposition, **not a sector decomposition**, and does not show831M worth of completed municipal construction. Sector health/municipal attribution and grant/investment breakdown answer different questions; do not combine their percentages additively.

The2017–18 original report grants4017M versus2161M prior, an increase1856M; investment4999M versus4417M, an increase582M; total2438M. Grant growth accounts for76.13% of the original-vintage increase, but not all grants were the800M MSI advance. Original total9016M differs from latest9021M; source notes later5M operating-to-capital-grant reclassification. Clearly use original totals for original decomposition and latest totals for main historical panel.

### Execution interpretation constraints

Ratios compare **actual to budget as presented/restated in each final-results source**, not actual to a universally harmonized final authorization. Label the budget vintage explicitly.10 contemporaneous original-vintage actuals should not be replaced with later restated amounts while retaining their original denominators.

2020–21 source PDFp16 expressly states the Budget2020 Capital Plan was **revised substantially** and1.1B added in response toCOVID/recovery; it also identifies685M accelerated maintenance/renewal, with210M spilling into2021–22. Thus6896/6960=99.08% is correct against the budget table denominator, but cannot mean99% of the amended recovery capital plan delivered. A chart calling this “execution” must disclose original/table budget comparator and in-year plan revisions. Budget versus actual gaps are not cancellation, procurement inefficiency or unmet physical needs.

Unexplained revision2018–19 contemporaneous6180→latest6057 (−123M) remains a source-vintage bridge requirement.2022–23 contemporaneous5644→later5633 (−11M) also needs later source explanation. The archive correctly retains both instead of calling revisions expenditure changes. Existing2019–20−19M bridge is explained and verified.

## Demography panel findings

Inspected all7 distinct source table pages directly:2018–19p14,2019–20p12,2020–21p12,2021–22p12,2022–23p12,2023–24p13,2024–25p13. The archive has78 observations; no duplicate source/year keys.2015–2024 summary min/max/count/range and selected latest values independently pass. Annual CPI growth agrees across available vintages for the primary years.

The observed cross-vintage population ranges vary from1k to32k persons; calendar2022 has32k range across reports. This documents revision sensitivity **among accessible historical official report vintages**, not a probabilistic uncertainty interval or maximum possible future revision.2024 has one available report, so its0 range means no cross-vintage comparison, not certainty/no revision risk. Minimum and maximum endpoints from different vintages must not be mixed to claim a real demographic trajectory. Prefer latest internally consistent vintage, as the primary analysis does.

Archive source variable`source_report_calendar_endpoint` is an inferred table ending calendar year, not publication year or fiscal vintage. For example endpoint2024 source was publishedJune2025. Keep that distinction if labeling figures. Raw rows include years outside primary2015–2024 and the negative-CPI defect above; archive validation needs broader sign coverage than the primary decade alone.

## Integration recommendations

1. Add a short latest-year decomposition paragraph: “Of943M nominal Capital Plan increase,831M was capital grants and112M capital investment; transfers do not directly measure infrastructure completed.” Cite latestp3.
2. Show execution ratios with “budget as presented in contemporaneous final results” and annotate2020 altered recovery plan; never rank government competence from these ratios.
3. Keep revision bridges alongside budget panel so users understand6180/6057 and5644/5633 are source-status differences, not contradictory physical delivery.
4. Include a brief demographic revision warning citing source pages and the archived ledger; don't convert observed ranges into confidence intervals.
5. Correct negative2009 CPI in raw ledger before calling all archived source rows validated.

These additions deepen the report while retaining its grounded conclusion about resource inputs and selected physical delivery rather than complete capacity growth.
