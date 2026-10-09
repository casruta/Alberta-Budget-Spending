# Health outcome source audit

## Sources and reproducibility

Four ministry PDFs were successfully downloaded from URLs actually linked by Alberta's official annual-report index: Health 2018–19,2019–20,2023–24 and 2024–25. `current/download_manifest.json` records exact URLs, PDF byte counts, SHA256, recording timestamps, and independent header checks returningHTTP 200. Normal TLS/proxy verification remained enabled. Failed whole-government PDF resources reported elsewhere do not invalidate these successful ministry-specific downloads. Previously described missing recent Health outcomes are now partly filled.

`extract_health_outcomes.py` produces `extracted/health_outcomes.csv`/JSON with 108 observations, source vintage, calendar/fiscal period, units, definition, target where known, exact one-indexed **physical PDF pages**, source hashes and raw page quotes. Printed footer pages in the recent Health PDFs are generally two pages lower than physical indices. `extracted/source_pages.txt` preserves the selected pages. No unknown observations were filled with zero.

Run:

```sh
python 'Quality of Life Analysis/research/health/extract_health_outcomes.py'
python 'Quality of Life Analysis/research/health/verify_bbox_values.py'
```

The first parser reads layout text and asserts expected numeric rows. The second independently selects table words using PDF bounding-box coordinates. **All 48 current values across 11 ED/EMS/surgery/imaging/readmission table rows matched.** Its results are saved in `extracted/bbox_verification.json`. The 2015 and 2017 life-expectancy graphics were separately rendered and visually checked, preserving year/group pairings. Independent `sha256sum` checks passed for all four downloaded PDFs; results are saved in `extracted/independent_hash_verification.json`.

## Current comparable access and outcome series

| Measure | Latest observation and comparison | Physical PDF page, Health 2024–25 | Definition limit |
|---|---|---|---|
| ED time to initial physician assessment,16 largest sites |90 th percentile 7.0 h versus 6.7 h prior year;2021–22=4.5 h and 2022–23=6.2 h revised |23 |Not mean wait; excludes specified unobserved/unseen visits.2024–25 goal was below the prior result and was not achieved. |
| Urgent EMS response |Metro 14.2 min versus 13.8; rural 29.2 versus 33.3; remote 52.0 versus 64.9 |24 |90 th percentile Delta/Echo events, geographic groups; not all calls or individual clinical outcomes. |
| Hip/knee/cataract operations within national benchmarks |72.8%,62.5%,62.8% versus 62.4%,53.3%,59.7% |26 |Completed valid ready-to-treat cases; excludes emergency care/patient delays; not everyone awaiting surgery. |
| MRI/CT within priority targets |41%/80% versus 42%/80% |30 |Priority-specific limits; case mix changes can move aggregate percentages. |
| Unplanned medical readmission within 30 days |12.7%, unchanged from 2023–24;2020–21=13.2% |42 |Selected medical acute-care discharges; excludes surgery,pregnancy/childbirth,mental health,palliative,cancer therapy. |

These show **mixed performance**, with improved surgical timeliness and rural/remote EMS access alongside worse ED assessment waits and a slight MRI-target decline. They do not establish that budget changes or a political administration caused the movements. Pandemic disruption, case mix, ageing, staffing, demand, referral processes and clearance of old waiting cases remain confounders. Changes in percentages are percentage points unless explicitly described otherwise.

## Two ED methodology-documentation errors

The 2024–25 methods page 56 labels ED performance measure 1 a as time to initial physician assessment and says time between triage and assessment, but the next paragraph incorrectly refers to **EMS communications Delta/Echo events**. That paragraph belongs to the separate EMS metric 1 b. Do not use it to redefine ED data.

The 2023–24 methods page 57 also has an incorrect introductory sentence describing arrival-to-inpatient-bed time. Its explicit **Step 1 formula** instead states:

> (physician initial assessment time) − minimum(registration time,triage time)

Step 2 calculates its 90 th percentile in hours. Listed exclusions include missing/invalid physician assessment timestamps, non-face-to-face visits, nonphysician providers, leaving without triage/being seen, and dead-on-arrival cases. The table heading and explicit formula support interpreting the results as initial physician assessment, not total ED length of stay. The start-time shorthand differs between report narratives; use the metric's heading and document the formula rather than pretending the prose is perfectly consistent. Both reports explicitly revised 2021–22 from 4.6 to 4.5 h and 2022–23 from 6.3 to 6.2 h after excluding Left Without Being Seen data.

## Targets, denominators and population

Surgical volume exceeded the 310,000 target:318,601 operations versus 304,595 prior (2024–25 physicalp 25). Using the existing latest-vintage July populations 4.889 M and 4.685 M yields roughly 65.17 versus 65.01 operations per 1,000 residents, an approximately 0.24%rise. This is a **throughput proxy**, not unique patients, age-adjusted need, health improvement or infrastructure adequacy. Population ratios cannot replace clinical/case-mix denominators.

The samep 25 reports 74,928 cases currently waiting,57.8%within clinically recommended timelines. That **waiting-case snapshot** differs from the completed-case denominator in the hip/knee/cataract indicators. Do not compare 57.8%with 72.8%as though they measure the same patients or threshold. The national 182 dayhip/knee and 112 dayfirst-eye-cataract benchmarks are per-case thresholds, not a documented provincial percentage target.

## Historical life expectancy and source-vintage conflict

The 2015–16 whole-government report(p 103) gives provincial life expectancy 81.59,81.68,81.71,81.79,81.87 years for calendar 2011–15 within one publication vintage. Its group values are retained as older-vintage observations. The 2017–18 whole-government report(p 131) gives First Nations 71.9,70.9,69.9,70.9,70.7 and nonFirst Nations 82.1,82.2,82.2,82.3,82.2 years for 2013–17. Its 2017 gap is 11.5 years. The source cautions small First Nations annual numbers fluctuate and life expectancy measures length,not quality,of life. Methods and excluded non-AHCIP populations appearp 152.

Health 2018–19(p 24) reports markedly different overlapping group values using AHCIP**Adjusted Population**, with 2018 figures preliminary. For example,2017 nonFirst Nations is 79.9 years versus 82.2 in the earlier whole-government graph;2017 First Nations 67.7 versus 70.7. Those differences are unreconciled. Do not append 2018 to the earlier series or call the cross-vintage difference a real mortality change. The later source is retained with `primary_within_definition=False` for audit. These archived observations do not measure the post-2019 period. The later Statistics Canada single-year source now fills recent all-population life expectancy through preliminary 2024; see `LIFE_EXPECTANCY_AUDIT.md`. Preserve its distinct source vintage and definitions.

## Historical satisfaction and perceived access

Personal health-service satisfaction was 62%,63%,66%,68%in fiscal 2011–12 through 2014–15, against 65%,68%,65%,70%targets (physicalPDFpages 93,118,135,119 respectively). These are survey estimates. The 2014–15 method (p 128) gives 1,361 question respondents and an approximate±2.5 percentage-point margin at 95%confidence. Treat meeting/missing a numeric target as an arithmetic comparison,not proof of a statistically significant change.

Old perceived ease of physician/ED access and public overall health-system ratings are distinct survey concepts,not measured waits. The 2011–12 source explicitly revised date labels into fiscal rather than calendar periods. Those perceptions should not be joined to current ED 90 th-percentile waits.

The current 92%lab-experience satisfaction statement(Health 2024–25 p 30) lacks a sample/method/date in that passage and concerns a narrower lab service. It is **not an updated provincewide personal-health-services satisfaction rate**. CT/MRI and lab before/after median waits in that paragraph likewise lack explicit comparison-period anchors; `contextual_health_evidence.csv` keeps them outside annual comparable series.

## Continuing-care responsibility transfer and scope

The separate `continuing_care/` package preserves seven early admission-timeliness years and 2018–19 extension, old provincial waitlist snapshots, recent 14-largest-hospital waitlists and revised homecare totals as different definitions. Health 2024–25 p 42 explains metric 2 b moved to Seniors, Community and Social Services; omission is not zero access or zero capacity. The SCSS 2024–25 report fills the latest timeliness gap: physical PDF p64 reports 63.0% preliminary against a 66.0% target. Its 2023–24 comparator, 62.5%, is incomplete because some zones could not report after Connect Care implementation. The 0.5 percentage-point change therefore does not establish complete-population improvement. The admitted-client denominator and types A/B inclusion, type C exclusion are defined on physical p71. See `continuing_care/scss_bridge.md`; the 2019–20 timeliness value remains missing.

## Verified operational infrastructure dates now available

Contextual evidence also fills selected previous infrastructure gaps: Misericordia ED opened 21 November 2023(Health 2023–24 p 26), with 26→64 treatmentrooms and 12→18 acute spaces; Arthur Child Cancer Centre became fully operational 28 October 2024(Health 2024–25 p 25), with gross 160 inpatientbeds/90 chemotherapyspaces; Rocky Mountain House's secondOR became operationalApril 2024(p 23), adding one operating room and six recovery beds. These are **local facility measures with distinct units**, not a reconciled provincial staffed-bed series or causal proof of provincial waiting-time changes. Preserve predecessor capacity,operational timing and denominator boundaries when linking infrastructure to outcomes.
