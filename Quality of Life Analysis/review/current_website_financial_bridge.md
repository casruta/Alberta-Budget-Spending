# Current government website corroboration: all 80 financial cells

**All 80 functional expense cells match exactly** across the original supplied Final Results PDF (physical p. 14), the freshly downloaded full Government of Alberta Annual Report (physical p. 14 / printed p. 12), and the primary functional-expense ledger. The comparison covers ten fiscal years, 2015–16 through 2024–25, and eight measures: health, basic/advanced education, social services, other programs, total programs, debt servicing, pension provisions/recovery, and total expense.

[current_website_functional_all80_comparison.csv](current_website_functional_all80_comparison.csv) records every source/ledger value, difference and match flag. Both differences are zero for every cell. [The JSON receipt](current_website_financial_bridge.json) preserves document identities and hashes.

## Provenance

The fresh annual report contains 152 pages; the archived Final Results excerpt contains 24. They are different documents, so different hashes are expected:

- Archived `Budget PDFs/2024-2025 Budget.pdf`, titled “2024-25 Final Results – Year-end Report”: SHA256 `a1a5d7638d96995845885ac43c556249bff2341f0d875d0f38027944df17c87f`.
- Fresh `research/source_verification/downloads/goa-annual-report-2024-2025.pdf`, titled “Annual Report – Government of Alberta 2024-2025”: SHA256 `9928eabc408f5f6a4770f0d62dc8da42d654e6dd34e3932299265355492de477`.

The fresh hash matches the successful HTTP 200 receipt in [download_manifest.json](../research/source_verification/download_manifest.json), checked October 9, 2026 at 03:44:26 UTC using normal TLS/proxy verification. An earlier HTTP 403 entry remains in that history; the later successful receipt records the retrieved file.

[Official PDF resource](https://open.alberta.ca/dataset/7714457c-7527-443a-a7db-dd8c1c8ead86/resource/e6c7f85c-73bc-44d3-af00-edebf01d82a1/download/goa-annual-report-2024-2025.pdf).

The archived Final Results remains primary for continuity. Fresh retrieval corroborates the document and provenance; it does not constitute independently collected fiscal measurements.

## Method and the 2022–23 discrepancy

Re-extracted both original source pages using pdfplumber and the separately verified numeric-layout parser in [verify_functional_expenses_independent.py](../research/budget/verify_functional_expenses_independent.py). Compared all values using Decimal arithmetic with the existing PyMuPDF ledger. No fresh values were substituted into the primary dataset.

The fresh full report also prints 2022–23 Other Program Expense of $13,769M and Total Program Expense of $61,691M, with Health $25,486M, Education $15,220M and Social Services $7,222M. The $6M discrepancy therefore persists in the current official publication. This corroboration does not repair or explain the anomaly. Retain the source flag rather than treating website publication as proof that every table reconciles.

## Budget columns are expressly restated

The fresh report, physical p. 8 / printed p. 6, says:

- 2023–24 Actual and 2024–25 Budget/Actual were reclassified for government structure changes and Provincial Health Act amendments.
- 2023–24 Actual includes a $5.85M Alberta Enterprise Corporation investment-related revenue/expense reclassification.
- “2024-25 budget numbers have been restated to reflect adoption of the new Public Private Partnerships (P3) accounting standard.”

[Exact page text](current_website_original_reclassification_note_physical8_printed6.txt) is retained. Paired budget figures from these tables should be called **source-reported restated/reclassified budget comparisons**, not independently reconstructed original appropriations. Functional expense, ministry operating expense and accounting expense types remain separate measures.

No original PDFs, completed Infrastructure Analysis files or primary functional CSVs were edited.
