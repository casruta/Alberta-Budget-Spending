# Recent life expectancy: verified Statistics Canada source

The official table **13-10-0837-01**, “Life expectancy and other elements of the complete life table, single-year estimates, Canada, all provinces except Prince Edward Island,” was successfully retrieved with normal TLS. The table page and full CSV ZIP are preserved locally. The page reports release date **2026-01-13**; its page-modified date is 2026-10-08. These are separate from calendar observation years. URL, bytes, SHA256 and recording timestamp are in `download_manifest.json`.

`extract_life_expectancy.py` filters the full CSV to Alberta and Canada, **0 years**, **Both sexes**, and the life-expectancy and margin-of-error elements. It preserves every original column, including vector, coordinate, decimals and status. Output includes 180 unique observations: two regions × 45 years (1980–2024) × two elements. No old Alberta annual-report vintage was overwritten or joined to this new vintage.

| Calendar year | Alberta life expectancy at birth, years | Canada, years | Alberta margin of error, years |
|---|---:|---:|---:|
| 2014 | 81.34 | 81.87 | 0.15 |
| 2015 | 81.45 | 81.92 | 0.15 |
| 2016 | 81.50 | 82.02 | 0.15 |
| 2017 | 81.38 | 81.88 | 0.15 |
| 2018 | 81.44 | 81.87 | 0.15 |
| 2019 | 81.96 | 82.22 | 0.14 |
| 2020 | 80.84 | 81.58 | 0.15 |
| 2021 | 80.24 | 81.50 | 0.14 |
| 2022 | 80.19 | 81.13 | 0.14 |
| 2023 | 80.71 | 81.68 | 0.14 |
| 2024 | 81.53 | 82.16 | 0.14 |

Alberta fell 1.77 years from 2019 to 2022 and recovered 1.34 years by 2024, leaving the preliminary 2024 value 0.43 years below 2019 and 0.09 years above 2018. Canada fell 1.09 years from 2019 to 2022 and recovered 1.03 years by 2024. The Alberta–Canada difference is −0.26 years in 2019, −0.94 in 2022 and −0.63 in 2024. These are descriptive differences in a common publication vintage, not estimates of government causation. Calendar 2019 straddles the April government change. Small differences such as 2018 versus 2024 must be considered with uncertainty and revisions.

## Exact metadata definitions and limits

`13100837_MetaData.csv` note 10 defines life expectancy as:

> Average number of years remaining to be lived by persons surviving to age x if those persons would experience, during their lifetimes, the mortality observed over the reference period.

Thus age-zero life expectancy is a period mortality summary, not the observed eventual lifespan of babies born that year and not quality-adjusted life expectancy.

Note 3 states:

> Life tables for the years 2023 and 2024 are considered “preliminary”. These tables will be updated at a later time to take into account deaths that could have occurred but have not yet been recorded (late registrations).

**Selected CSV STATUS cells are blank; this does not override the explicit table-wide preliminary caveat.** Notes must accompany latest values.

Note 2 states population estimates are final intercensal up to 2021 and updated postcensal from 2022 to April 2025. Historical numbers in this current table need not match older ministry/Measuring Up publications. Do not interpret those vintage discrepancies as mortality changes.

Note 12 says the life-expectancy margin of error forms a 95% confidence interval by adding/subtracting the published margin. Alberta 2024 is therefore approximately 81.39–81.67 years before future preliminary-data revisions. Published margins do not capture all revision uncertainty, and separate-year margins alone do not establish a formal test of change.

Note 13 explains single-year tables are suitable for granular temporal changes, while three-year tables provide more robust, less volatile estimates and may be preferable for regional or long-term comparisons. This extraction deliberately preserves single-year data; it does not label them three-year averages.

Note 4 says complete single-year tables exist for Canada as a whole and nine provinces. Prince Edward Island and the territories have separate three-year abridged tables because their populations are too small for sufficiently accurate complete tables. Their omission from provincial single-year rows does **not** mean the Canada total excludes them. No reservation, First Nations, federal-personnel or AHCIP-specific exclusion is stated in these inspected table notes, and none is imported from unrelated ministry methods.

This source closes the recent all-population mortality gap. It does not supply a recent First Nations/non-First Nations breakdown, a causal mechanism, disability-adjusted health, or measured effects of capital spending.

## Compact reproducibility

The authoritative full CSV remains inside `13100837-eng.zip`. The maintained extractor streams that ZIP entry directly with `ZipFile` and `TextIOWrapper`; a separate streaming SHA256 pass records the uncompressed CSV hash. The generated 243 MB unpacked CSV was removed after confirming its hash exactly matches the ZIP entry. Selected CSV/JSON remain 180 rows, and independent HTML verification reads only the selected CSV. `metadata_period_status.json` exports the table-note preliminary flags for 2023–2024 separately; original selected STATUS cells remain unchanged.
