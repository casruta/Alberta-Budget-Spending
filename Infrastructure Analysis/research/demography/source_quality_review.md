# Source-quality review: population definitions, census vintages and CPI base

## Standalone source verification

`verify_vintage_ledger.py` uses **pypdf**, rather than the ledger builder's `pdftotext`, and imports neither the ledger-building module nor the main analysis. It independently opens all seven original PDFs, verifies each cover says Final Results / Year-End Report, obtains the fiscal reporting year from the cover, reads the archived economic table's precise PDF page, parses the calendar-year headers and exact population/CPI source rows, and compares every ledger observation.

Result: **78 source rows match seven official Final Results reports**. Unique year keys, contiguous source years, row counts, source-report endpoint years, exact published values and source hashes are checked. Every economic observation's calendar year is no later than the fiscal-year starting calendar year. No later calendar forecast appears in the ledger. Status remains **historical demographic estimate**, not census enumeration or exact population count. `independent_source_verification.json` records the inspection results and missing metadata by source.

## What the economic pages actually define

The table itself supplies **Population (July 1, thousands)** and **Alberta consumer price index**, beneath **Calendar year, % change unless otherwise noted**. Thus July1/thousands governs population, and annual percentage change governs CPI. The CPI row does not publish an index level. Neither row is marked with the `a` estimate footnote attached to other macroeconomic fields. A footnote such as “2024 is an estimate” therefore must not be used to label the entire historical table or population/CPI observations as budget forecasts. Demographic estimates remain estimates regardless of that separate economic-field footnote.

These pages do **not** provide a Statistics Canada table identifier, retrieval timestamp, census base, or preliminary/updated/intercensal estimate classification beside the population row. Nor do they explicitly explain the precise cause of each across-report population revision. The general official tables named in our methodology are retrieval targets, not evidence that this local report's exact demographic vintage was independently downloaded from Statistics Canada.

The ledger demonstrates changes across report vintages, but it cannot establish which report is strictly “pre-2021-census rebasing” and which is “post-2021-census rebasing”. Report dates alone are insufficient to identify the particular estimate series delivered to the provincial table. **Do not attribute these local revision differences specifically to census rebasing without additional source-series metadata.** The appropriate report wording is “demographic revisions across report vintages”, with classification unresolved.

## CPI index base is not the source of these rates

The primary official local table reports growth rates, so a claim that these inputs are **CPI index levels with 2002=100** would be unsupported. The constructed series has its own transparent **2015=100** arithmetic normalization and is labelled as a chain of rounded annual rates. A change in index base, applied consistently to an exact series, multiplies all levels by a constant and **cancels in a ratio**. Thus index-base normalization itself does not alter cumulative inflation or adjusted growth. A mixture of incompatible series, a fiscal/calendar mismatch, or rounding could alter it; these must be assessed separately.

If each rounded annual growth rate differs from the underlying true rate by at most 0.05 percentage points, worst-case cumulative CPI growth ranges are:

| Interval | Published-rate chain growth | Rate-rounding-only cumulative bounds |
|---|---:|---:|
| 2015–2024 | 26.3516% | 25.7986% to 26.9067% |
| 2018–2024 | 20.1257% | 19.7766% to 20.4757% |
| 2019–2024 | 18.0017% | 17.7165% to 18.2874% |

For 2018–2024 this corresponds to approximately **±0.29% in the price factor**, not ±0.29 percentage points in cumulative inflation. These deterministic bounds explain what exact official CPI levels could improve **if annual rates are rounded from the same annual-average level series**. They do not cover fiscal-average alignment or substituting construction prices. Because no official local annual CPI-level row or remotely retrieved index series is available, we cannot report an empirical exact-level-versus-rounded-chain discrepancy.

## Material implications

The existing one-vintage demographic denominator and rounded-growth CPI sensitivity remain justified by the available evidence. Source definitions should remain explicit, index levels should not be invented, and census-rebasing explanations should not be inferred solely from report date. Recovering a compatible construction-price series and fiscal-average observations would improve inference more than re-expressing the same CPI chain in a different numerical base.

No change to the headline calculations is required by this inspection. The three unresolved source-quality gaps are **census/estimate-vintage metadata**, **exact annual/monthly CPI levels**, and **appropriate construction-price coverage**. The source corpus supports historical spending-intensity descriptions; it still does not establish net infrastructure capacity per person.

## Signed-value regression found and corrected

A reviewer identified that the original cross-vintage ledger parser lost accounting parentheses around the 2009 CPI rate `(0.1)` in the 2018-19 report, incorrectly storing +0.1 rather than **−0.1%**. The ledger builder now preserves parenthesized negatives and explicit minus signs. The standalone verifier uses a separately implemented whitespace/token parser and asserts this exact source regression directly. All 78 archived rows now reconcile. The error was outside the 2015–2024 analysis window; primary inputs, revision summaries for those years, comparisons and headline results are unchanged.

## Reproducibility refresh check

The ledger builder now refreshes `pdftotext -layout` output directly from its seven explicitly scoped local PDFs before extraction. It no longer relies on potentially stale archived text. Original PDFs are read-only inputs; source hashes are recorded and checked for preservation. Unrelated older cached texts cannot enter the ledger. Rebuilding from fresh PDFs and running the independent direct-PDF verifier preserved both CSV hashes exactly: ledger `c20a8e8e0cae18a3da56ad8124a1830da32d265f147e8ecb85edaf31e0e51f21`; revision summary `ceba516344329bb6f2ff77c9875ab0c131c53bbcd55f0773db8cf7b5f2fe4ad3`.
