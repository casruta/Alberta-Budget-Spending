# Independent financial-report audit, round 3

Reviewed REPORT.md sections 2–6 and 8, the six figure-generation calculations in scripts/analyze.py, primary source tables and rendered figure 05. Recomputed figures independently using Python standard-library CSV/math from the source extract, not by importing the analysis functions.

## Verdict

**Financial sections pass with minor presentation improvements. No material numerical correction required.** Financial source definitions, no-double-counting warning, main changes, per-resident calculations, CPI chaining, rounded table values, recent sector comparison and net-deferred-contribution stock caveat match the source-reviewed inputs. Source warnings appropriately limit physical/causal interpretation.

## Verified numerical evidence

- Latest historical actual capital spending:6558,6578,9021,6057,5545,6896,6622,5633,6300,7243 $million. All report rows match.
- 2018–19→2024–25:nominal19.58065%; population13.88307%; CPI20.12571%; nominal/resident5.00301%; CPI-adjusted/resident−12.58906%. Rounded report19.6/13.9/20.1/5.0/−12.6% is correct.
- 2019–20→2024–25:nominal30.62218%; population12.26177%; CPI18.00168%; nominal/resident16.35500%; CPI-adjusted/resident−1.39547%. Report30.6/12.3/18.0/16.4/−1.4% is correct.
- 2015–16→2024–25:nominal10.44526%; population17.80723%; CPI26.35161%; nominal/resident−6.24917%; adjusted/resident−25.80163%. Report matches rounding.
- 2023–24→2024–25:nominal14.96825%; adjusted/resident7.06613%, rounding15.0/7.1%.
- CPI-adjusted annual/resident series:1996.660,1959.709,2618.980,1694.855,1502.455,1826.380,1689.845,1327.341,1383.714,1481.489 CAD. Rounded report values match all ten rows.
- Weighted tenure values2066.948 vs1532.123; excluding2017–18 pre-period1881.875. Differences−25.875% and−18.585%, consistent report−25.9/−18.6%.
- Constant-intensity benchmark8286.148m; actual7243m; actual minus benchmark−1043.148m. Report8.29bn and−1.04bn accurate. Population×CPI growth36.80284%, rounds36.8%.
- Rounding-only 2018–19 sensitivity−12.87527 to−12.30178%, report−12.9 to−12.3% correct. 2019–20 sensitivity−1.67064 to−1.11940%; the small decline remains negative under rounded-input uncertainty, but construction-price/fiscal-alignment/accounting uncertainty remains unbounded. Treat−1.4% as a descriptive sensitivity, not robust evidence of service shortfall.
- Latest eleven core envelopes sum actual6499 and budget7732; prior sum5567 versus core5568 ($1 rounding). Core growth931 + SUCH12 = fully consolidated943; individual displayed changes sum944 ($1 rounding). Report sector table all values match p17. Municipal489+health318=807;807/943=85.57794%, rounds85.6%.
- Undershoot1056/8299=12.72442%, rounds12.7%. Health505, municipal287, school133 below budget are exact p17. Source text says cash flows/project scheduling; report correctly avoids equating variance with cancellations.
- Maintenance1347/7243=18.59727%, rounds18.6%. Bridge/highway rehabilitation673m explicitly p16, separately from Roads/Bridges envelope542m.
- Asset arithmetic62925−4080=58845 and61515−3964=57551 verified p12→p14. Gross nonfinancial assets include capital/inventories/prepaids/intangibles; report does not mistake the net historical row for physical infrastructure stock.

## Exact source check: accelerated grants

2017–18 report PDF p23 / printed p21: “$1,648 million Municipal Sustainability Initiative grants, including $800 million reprofiled from future years”. Therefore REPORT section3's800m advanced-grants statement and pp22–23 citation are accurate. p22 also attributes spike to accelerated municipal transportation/CLP and project progress. This is legitimate context for sensitivity excluding2017–18; excluding the whole observation is correctly described as coarse, not an800m-adjusted normalized baseline.

## Definitions and figures

Capital Plan combines investment in consolidated owned assets and capital grants outside government; report's double-counting warning is correct (latest p16 definitions). Some existing assets are renewed rather than expanded. Figure05 shows signed envelope changes with correct twelve bars, including SUCH and excluding total rows. Rendered labels, zero baseline, units and caveat are legible. Figures01–04/06 calculations independently agree with report numbers; no use of quarantined ministry CSV or net accounting-stock column found. Common-vintage totals do not establish full accounting comparability, and REPORT section2 states this clearly.

## Actionable refinements (minor)

1. Section4 change “a difference of $-1.04 billion” to “actual spending was $1.04 billion below that arithmetic benchmark.” This expresses the sign plainly and avoids awkward currency-negative formatting.
2. Section6 add one sentence after sector decomposition: “Displayed envelope changes sum to $944M versus the reported $943M total because of rounding.” Figure footnote already covers this; prose helps anyone summing table rows.
3. Section5/summary's2019–20 comparison should continue to be labeled CPI-adjusted sensitivity. Its−1.4% estimate is small relative to methodological uncertainty beyond rounding; consider saying “approximately flat on this CPI-based measure (−1.4%)”. This is optional editorial judgment, not a numerical correction.
4. A local source chart itself has an apparent error: latest PDF p16 labels SUCH744m as12%, but744/7243=10.27%. Delivered figures/report do not repeat that percentage and should continue using recalculated values.

No changes were made to REPORT.md or analysis outputs by this reviewer.
