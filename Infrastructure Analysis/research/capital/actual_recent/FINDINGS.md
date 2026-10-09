# Recent actual Capital Plan evidence

The local files called `2022-2023 Budget.pdf`, `tbf-goa-2023-2024 Budget.pdf`, and `2024-2025 Budget.pdf` are Government of Alberta **Final Results / Year-end Reports**, published June 2023, June 2024, and June 2025 respectively. PDF page 1 establishes the title; PDF page 2 names Treasury Board and Finance and points readers to `www.alberta.ca/budget-documents.aspx`. Official publication landing page (printed in source): https://www.alberta.ca/budget-documents.aspx . Direct document URLs could not be recovered because requests to alberta.ca/open.alberta.ca returned proxy HTTP 403. Local hashes are recorded in `source_manifest.json`.

## Actual totals, CAD millions

| Fiscal year | Same-year report actual | Latest available comparative/history actual | Budget in same-year report | PDF evidence |
|---|---:|---:|---:|---|
|2022-23|5,644|5,633|7,534|2022-23 PDF p3,p17; 2023-24 PDF p17; 2024-25 PDF historical table p14|
|2023-24|6,300|6,300|8,005|2023-24 PDF p3,p17; 2024-25 PDF p17|
|2024-25|7,243|7,243|8,299|2024-25 PDF p3,p17|

For a comparable aggregate trend use 5,633, 6,300, 7,243. For reporting a **same-year budget delivery ratio**, preserve the contemporaneous numerator 5,644 for 2022-23 and clearly label its vintage. Do not blend the original budget with revised actual without explaining the mixed vintage.

Envelope tables and individual sector values are in `recent_envelopes_all_vintages.csv`; every row records fiscal year, source vintage, PDF page, and status. `recent_envelopes_latest_comparative.csv` selects the latest source available for each original label. This is not a fully harmonized taxonomy: renamed categories (e.g. Agriculture and Natural Resources versus Agriculture, Natural Resources, and Business Development; Sports and Recreation versus Arts, Sports and Recreation) require explicit mapping before charting. Total labels are normalized only; underlying source text is preserved.

## Reclassifications and checks

The 2022-23 core total changes from 4,905 to 4,893 in the 2023-24 comparative; fully consolidated changes from 5,644 to 5,633. Several values are revised: maintenance 1,175→1,166, health 501→500, service delivery 239→238. The source documents are authoritative; the report's note on restatements identifies reorganizations and accounting changes, but does not isolate the cause of each individual numerical revision.

The 2023-24 envelope total remains 6,300 but the 2024-25 comparative redistributes spending: municipal 1,523→1,580; roads 571→514; health 380→376; housing 105→103; service delivery 301→305. Reclassification therefore can create false category growth if older and newer vintages are used uncritically.

The sum of the 11 rounded current-year envelopes differs from the reported core total by -2m (2022-23), +1m (2023-24), and 0m (2024-25). PDF page 2 explicitly warns that tables may not add due to rounding. Core + SUCH reconciles exactly for these current-year tables.

Capital Plan is **capital grants/other capital support plus investment in government-owned assets**, including consolidated schools, universities, colleges and health entities (SUCH). SUCH self-financed investment is an added component, not an extra item to add after the fully consolidated total. Capital investment is not all an income-statement expense; do not compare this Capital Plan total directly with ministry operating expenses. Maintenance, renewal, replacement, and IT are present: spending is not a measurement of net new physical infrastructure or service capacity.

The 2023-24 report p2 states adoption of the P3 standard changed opening tangible capital net book value by -415m and opening P3 liabilities by -353m; prior-year comparatives were not restated for those existing contracts. This matters to asset-stock analyses even where spending totals are stable.

No 2025-26 Final Results PDF exists in the supplied local checkout. Network denial prevents establishing whether it has been published as of October 2026. Mark 2025-26 unavailable rather than assume it is an unclosed fiscal year or substitute a budget.
