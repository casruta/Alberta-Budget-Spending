# Round 2: early UCP comparisons and execution audit

## Primary historical caution

Latest-vintage historical total capital spending is the preferred common-source series, but **same vintage does not remove historical accounting-policy discontinuities**. Latest report PDF p14 footnote a explicitly states numbers are not strictly comparable owing to numerous accounting changes. Comparison is descriptive, and cannot isolate a government causal effect. The decline from the accelerated-grant 2017–18 peak began in 2018–19 before the UCP took office.

## Paired ministry comparisons around the transition

`early_ucp_paired_ministry_comparisons.csv` takes each current/prior comparison from the **same** official annual-report table, and retains original attribution. These are ministry financial rows, not stable functional sectors or physical output. Prior-year columns have been revised and should not be chained naively.

| Report/table | Prior actual | Current actual | Difference ($m) |
|---|---:|---:|---:|
| 2019–20 PDF p15, total | 6,057 | 5,564 | –493 by rounded displayed numbers; source change column –494 |
| 2020–21 PDF p18, total | 5,545 | 6,896 | +1,351 |

2019–20 paired Ministry capital rows ($m), 2018–19→2019–20: Education 678→600 (–78); Health 925→1,083 (+158); Infrastructure269→125 (–144); Transportation1,757→1,551 (–206); Municipal Affairs889→1,124 (+235); Advanced Education694→554 (–140). The 2019–20 text says under-budget spending principally reprofiled transportation grants, school capital, carbon capture/storage, and other projects into later years due to slower progress (p15). The paired table retains residual attribution limitations; it does not prove cancellation or reduced delivered capacity.

2020–21 paired rows ($m), revised 2019–20→2020–21: Education599→782 (+183); Health1,083→1,111 (+28); Infrastructure123→164 (+41); Transportation1,537→1,979 (+442); Municipal Affairs1,128→1,730 (+602); Advanced Education554→484 (–70). Source p2 explains **$19m of 2019–20 capital grants reclassified into operating expense**, including Education0.5, Infrastructure2, Service Alberta2, Transportation14 (rounded). Thus 2019–20 total5,564 becomes5,545 in next-year comparative. This is not a spending cut: total expense and total taxpayer debt were unchanged. Education600→599 and Infrastructure125→123 are affected. Municipal Affairs1124→1128 also reflects presentation revisions and rounding; source excerpt does not establish its exact causal basis.

The first UCP fiscal year's aggregate decline was followed by a large pandemic/recovery-era capital rebound, particularly reported municipal/transport investment. 2020–21 report p19 gives a functional picture: capital maintenance/renewal$1,249m; Roads/Bridges$1,125m; municipal support$2,075m; health$999m; educational infrastructure$510m. These early envelope totals **include SUCH investment embedded in envelopes**, unlike the 2022–25 tables with SUCH self-financed investment separated. Do not plot early and recent categories as a continuous series without harmonization.

For context, 2018–19 report p2 explicitly shifted construction managed for school boards/AHS into Infrastructure(+420m), Education(–134m), Health(–285m), with old budget/prior figures not restated. This prevents a ministry-attribution decade chart around the political transition.

## 2024–25 budget execution: arithmetic verified

`2024_25_envelope_audit.csv` reproduces Budget/Actual/Prior Actual/changes from latest report p17. Eleven core-government envelope budget/actual sums exactly equal reported totals7,732/6,499. Prior envelope sums5,567 versus displayed core5,568, **$1m rounding**. Core changes sum–1,233m. SUCH financing567→744 contributes+177m, producing fully consolidated variance–1,056m and actual7,243m. Prior fully consolidated5,568+732=6,300; current6,499+744=7,243. The displayed source values reconcile.

Budget shortfalls by envelope ($m): health505; municipal287; educational133; housing/social120; agriculture/business116; service delivery79; roads55; arts24; skills5. Offsets: maintenance+76; public safety+15; SUCH self-financing+177. Health and municipal account for792/1,056 =75.0% of the **net** fully consolidated shortfall, though all gross shortfalls total1,324 and increases268 offset them.

Source p17 explains adjustments/refinement of project cash flows to progress and schedules. Health505m:393 for assorted named health facilities,79 for recovery communities while scopes/designs defined,34 for continuing care planning delays (subcomponents total506 due rounding). Municipal287m:110 slower municipal transport delivery,87 LRT,66 slower Calgary Rivers District/Event Centre construction,22 federal grant programs (subcomponents285, source rounding/detail not exhaustive). Education133m reflects schedules and cash-flow timing. Roads55m:47 west Calgary ring-road south connection timing plus8 other twinning/widening/expansion. p18 housing120m and service79m are also project timing/scheduling; agriculture116m includes Raven Creek45,carbon capture incentive41,other29 (sum115 due rounding). **Budget execution variance is not a count/value of permanently cancelled infrastructure.**

Health actual nevertheless increased318m versus revised2023–24(+84.6%); municipal increased489m(+30.9%); education decreased13m(–2.2%). Underspending against an annual budget can coexist with substantial growth against last year's actual.

## Historical stock independently checked

Latest historical p14 `Capital / non-fin. Assets`58,845 in2024–25 is **net of spent deferred capital contributions**: p12 reports capital/other nonfinancial assets62,925 less4,080=58,845. Prior61,515–3,964=57,551, matching2023–24 historical row. It is an accounting stock, includes inventories/prepaids/purchased intangibles, and is not a pure tangible-infrastructure series. Extractor and primary CSV now call it `net_capital_nonfinancial_assets_after_deferred_contributions_million`.
