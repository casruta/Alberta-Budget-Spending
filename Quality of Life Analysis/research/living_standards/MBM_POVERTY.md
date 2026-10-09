# Direct poverty evidence: official Statistics Canada MBM

**A direct welfare gap is now partially closed.** The official CSV archive for **Table 11-10-0135-01**, “Low income statistics by age, gender and economic family type”, was retrieved successfully using `curl -L --fail` with normal HTTPS proxy/TLS verification. The archive contains its full source CSV and metadata. The selected indicator is **Percentage of persons in low income**, **All persons**, **Alberta and Canada**, **Market Basket Measure**, with each base preserved separately. Units are percent, not population counts. These are historical survey estimates, not forecasts.

The measure compares families' disposable income to the cost of a specified basket representing a modest basic standard of living. The source 2023-base definition includes food, clothing, shelter, transportation, communication services and other items. The older base has a different basket definition. The 2023-base methodology resource is linked directly in the official metadata; no alternate poverty proxy is introduced.

## Critical base restriction

The downloaded table provides **2018-base MBM for 2015–2023**, and **2023-base MBM for 2020–2024**. It supplies **no 2018-base 2024 poverty rate** and **no 2023-base 2018/2019 rate**. Therefore **a single-base 2018–2024 comparison cannot be reported from this table**. Do not append the 2023-base 2024 figure to the 2018-base history and present it as one trend.

| Calendar year | Alberta, 2023-base (%) | Canada, 2023-base (%) | Alberta quality |
|---|---:|---:|---|
| 2020 | 6.0 | 7.0 | C: good |
| 2021 | 8.6 | 8.1 | C: good |
| 2022 | 10.5 | 10.6 | B: very good |
| 2023 | 10.2 | 11.1 | B: very good |
| 2024 | 11.0 | 11.0 | B: very good |

The latest-base Alberta point estimate rises **5.0 percentage points from 2020–2024**, with a dip in 2023; 2024 Alberta and Canada point estimates are both **11.0%**. This does not prove the underlying population rates are exactly equal or the changes statistically significant. Starting in pandemic year 2020 is a restriction of current-base availability, not a full pre-UCP evaluation.

For a separate same-base pre-UCP comparison, **2018-base** Alberta is **9.4% in 2018 and 10.0% in 2023**, a **0.6 percentage-point** increase; Canada is **11.2% and 10.4%**, a **0.8-point** decrease. Preserve that series' endpoint **2023**, its distinct base and sampling flags. In 2019, the Alberta 2018-base estimate is8.3% with **D: acceptable** quality. Differences should not be described as significant without suitable uncertainty information.

## Revisions, sampling and comparability

Metadata note22 states: **“With the release of the 2024 CIS data, Statistics Canada revised estimates from 2018 to 2023 based on population counts from the 2021 Census.”** This is a latest-vintage historical revision. Do not combine these rows with older published poverty estimates as if they were unchanged observations.

The source survey is the **Canadian Income Survey** for these years. Note18 identifies methodological changes: administrative personal-income masterfile data beginning in2021, increased sample size and improved weighting in2022, and a change in the target age for **income data** from16+ to15+. The selected poverty indicator remains **All persons**; that income-data age note does not transform this into an adult-only poverty rate.

Quality indicators depend on coefficient of variation and number of observations: A excellent(CV0–2%), B very good(2–4%), C good(4–8%), D acceptable(8–16%), E use with caution(16–33.3%). These flags are not supplied standard errors, confidence intervals or statistical-significance tests. All selected current-base Alberta rows areB orC; retain them in exports. Canada includes the territories from2018; the source states Canada excluded territories before2018. The chosen2018-onward comparisons avoid that stated coverage boundary.

Poverty outcomes are influenced by disposable incomes, benefits, household circumstances and regional basket costs. These descriptive rates cannot identify a provincial government's independent causal effect, isolate infrastructure changes, quantify food insecurity, or serve as a synthetic overall quality-of-life score.

## Reproducibility

- `11100135-eng.zip`: unchanged full official archive, with checksum in `mbm_poverty_provenance.json`.
- `11100135_MetaData.csv`: exact metadata text including definitions, methodology and revision notes.
- `mbm_poverty_all_persons_exact_source_rows.csv`:28 exact original rows retaining status, vectors and coordinates.
- `mbm_poverty_all_persons_2015_2024.csv`: labelled rows with distinct bases and sampling interpretation.
- `extract_mbm_poverty.py`: reproduces the selected data and provenance from the archived ZIP.
- `verify_mbm_poverty.py`: independent direct archive-reader check of all28 values, flags, vectors and absent-base endpoints.

Earlier statements that direct poverty data were unavailable are superseded by this verified retrieval, **subject to the base/time restrictions above**. No original tracked file or Infrastructure Analysis asset was changed.

## Publication date and population frame verified

The official table HTML was successfully retrieved. Its explicit **Release date** and JSON-LD **datePublished** both state **April29,2026**. This is the release of the downloaded table vintage, not the reference year of the observations. The ZIP metadata supplies reference-period coverage but does not itself publish a release date. `mbm_poverty_provenance.json` records the verified date and HTML checksum. A report using these rows should distinguish **calendar-year2024 outcomes** from **April2026 publication** and **October2026 retrieval**, rather than impose a blanket March2025 source-publication cutoff.

“All persons” is the selected **survey-population category**, not a claim that every resident or every community is enumerated. The ZIP table footnotes do not explicitly specify reserve/institutional population exclusions. The table page links the Canadian Income Survey SDDS5200 methodology page; an HTTPS request to that linked survey metadata endpoint returned403. Consequently this package **does not assert reserve coverage or exclusions without accessible source confirmation**. Canada/Alberta rates concern the survey-covered population, subject to its sampling frame. Table note16 independently confirms the territories boundary for Canada; that stated restriction is documented above.

An additional independent `DictReader` selector verifies all28 rows against the full archive using exact geography, all-persons category, statistic and base dimensions. It checks units=`Percent`, scalar=`units`/ID0, all four vectors, quality statuses, exact B/C coefficient-of-variation definitions from source note2, and unavailable-base endpoint regressions. There is no interpolation, forward fill or base splicing.
