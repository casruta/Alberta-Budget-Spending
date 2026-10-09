# Demographic denominators and price sensitivity

The cleaned CSV uses **July 1 population in the calendar year that starts each fiscal year**. Thus 2019-20 spending is divided by July 1, 2019 population. All ten years 2015-16 through 2024-25 use one consistent official report vintage: the Government of Alberta **2024-25 Final Results | Year-End Report**, printed page 13 / PDF page 13, “Key Economic Indicators, 2013 to 2024”. The repository PDF is misleadingly named `Budget PDFs/2024-2025 Budget.pdf`; its contents are final results, not a proposed budget. The extracted table's production metadata is dated June 19, 2025.

Population rises from **4,150,000 in July 2015 to 4,889,000 in July 2024: 17.807%**. From July 2019 it grows **12.262%**. These are population estimates rounded to the nearest thousand, not exact counts. Demographic estimates can be revised; do not combine this series with the hard-coded notebook series as though both were the same vintage. Fiscal-year population averages would be preferable for annual expenditure intensity but require consistent quarterly estimates. This within-fiscal-year snapshot is explicit, reproducible, and requires no invented population forecasts. July 1 is three months into the fiscal year; the fiscal-year midpoint is approximately October 1.

No 2025 or 2026 population values were extrapolated. The local table ends at 2024. Obtain later observations from Statistics Canada Table **17-10-0009-01** before computing later-year per-capita results. The first attempted official downloads returned a network proxy **403 Forbidden**; a direct-egress diagnostic failed DNS resolution. No remote source was represented as successfully retrieved.

## CPI sensitivity, not construction output

The source reports Alberta calendar-year annual CPI **growth percentages**, not CPI index levels. `cpi_chained_index_2015_100` chains the *rounded* annual rates for 2016–2024 onto 2015=100; the resulting 2024 index is **126.3516**. `cpi_deflator_to_2024` is the ratio of that terminal index to each year's chained index. This permits a **rough CPI-adjusted spending sensitivity in 2024 calendar-year consumer purchasing-power dollars**. It is not an official CPI series, not a fiscal-year-average CPI adjustment, and not construction purchasing power. Rounded growth rates introduce small compounding differences from the official level series.

For preferred CPI inputs, use Statistics Canada annual Table **18-10-0005-01**, Alberta, all-items, index (2002=100), or monthly Table **18-10-0004-01** and average April–March monthly levels. Retain the source vintage, units and exact source rows.

For infrastructure construction costs, examine official Building Construction Price Index Table **18-10-0276-01**, Edmonton and Calgary, non-residential construction, with correct published index base and comparable overlapping coverage. Do not apply a city/building index to all Alberta infrastructure as if it covered provincial roads, bridges, engineering works, land, equipment, grants and labour uniformly. A carefully scoped sensitivity is useful; a construction-volume claim requires asset-specific prices and physical output. No construction price observations were available locally or successfully downloaded, so none are manufactured here.

## Existing notebook audit

`existing_notebook_input_audit.csv` compares the existing operating-expense notebook’s hard-coded population/CPI inputs with this official local table; the notebook is read without execution and is unchanged.

- Population differences beyond source rounding become material in 2024: notebook 4,909,030 versus official local rounded 4,889,000. A revised vintage could explain this, but notebook inputs have no archived source or retrieval date establishing it.
- Several implied annual CPI rates differ materially from the official table: the notebook's 161.8/158.5 implies **2.082%** for 2024 versus **2.9%** in the report. Notebook 2021 CPI implies approximately **3.974%** versus official **3.2%**. A rounding/vintage difference does not establish validity; verify underlying CPI levels before using that notebook as a source.
- Calendar-year CPI values labelled fiscal-year CPI should be described as a calendar-year proxy, or replaced with actual April–March average index levels.
- A spending category must exceed the **product** of population and CPI indexes to increase in real per-capita terms. Merely exceeding each separately is insufficient.
- Real spending per person measures expenditure intensity, not delivered service quality, infrastructure capacity, efficiency, or causal political effect.

## Reproduce and validate

Run `python extract_demography.py` from any directory. Requires Python standard library and `pdftotext`; it does not install packages or alter existing files. It checks the report identity, exact parsed row lengths, and expected table values, writes source text, clean CSV, audit CSV, and source SHA-256 metadata. Original PDFs remain unchanged. The script intentionally fails if the underlying local report changes so a reviewer rechecks the extraction.

`raw_local/` contains layout-preserving text extracted from existing official PDFs for corroboration and report identification. `population_cpi_source_page.txt` is the exact selected page extraction. `provenance.json` records the local source hash and remote-source limitations. A second extraction with `pypdf` confirms the same table values and page location.

For cross-vintage evidence, run `python build_vintage_ledger.py`, then `python verify_vintage_ledger.py`. The builder refreshes layout-preserving text directly from the **seven explicitly reviewed original PDFs** on every invocation, rather than trusting cached `raw_local` files. Other cached report texts cannot add unnoticed observations. It records source SHA-256 hashes in `vintage_ledger_source_hashes.json` and checks that source PDFs remain unchanged. The independent verifier uses `pypdf` and separately parses direct source rows, including the parenthesized negative 2009 CPI regression.
