# Independent sensitivity validation

Checked `scripts/analyze.py` against a separate **standard-library implementation** in `sensitivity_validation.py`; it imports no analysis code. Reproduction output is saved in `sensitivity_validation.json`. Every reported point estimate and deterministic rounding bound in `data/baseline_comparisons.csv` reconciles within 1e-10 percentage points.

## Formulas and baseline indexing

Let capital spending be C, population P, and a price index D. The price-adjusted per-resident change is `(C_end/C_base)/(P_end/P_base)/(D_end/D_base) - 1`. For a baseline of 2018 and endpoint 2024, chain **2019, 2020, 2021, 2022, 2023 and 2024** annual inflation rates. Do not include the 2018 inflation rate: the baseline index already embodies that year's level. Both `load_primary()` and `compare()` use this indexing correctly. The 2015=100 starting index excludes 2015 inflation when subsequently building the 2015–2024 price change; this is correct.

2018-19 is the last full pre-UCP fiscal year. Starting at 2019-20 instead changes the economic question because the endpoint ratio omits the first decline during UCP tenure. Neither temporal comparison identifies a causal government effect.

## Rounded-input bounds

The script's ±0.05 **percentage-point** bound for CPI rates published to one decimal, ±500 persons for population reported in thousands, and ±0.5 million dollars for spending reported in millions are arithmetically correct under nearest-unit rounding. Spending is monotone upward in endpoint C and baseline P, downward in baseline C and endpoint P and inflation. The computed low/high combinations respect these directions. These are deterministic worst-case input-rounding scenarios, **not confidence intervals**, and do not capture revisions, source classification, fiscal alignment or deflator selection.

| Baseline to 2024-25 | Point CPI-adjusted per-person change | Worst-case rounding range |
|---|---:|---:|
| 2015-16 | −25.802% | −26.153% to −25.448% |
| 2018-19 | −12.589% | −12.875% to −12.302% |
| 2019-20 | −1.395% | −1.671% to −1.119% |
| 2022-23 | +11.613% | +11.464% to +11.763% |
| 2023-24 | +7.066% | +6.976% to +7.156% |

Rounding alone does not reverse any reported direction. This does not establish robustness to a different appropriate construction deflator.

## Break-even construction-price scenario

For 2018-19 to 2024-25, capital spending rose **19.5807%**, while population rose **13.8831%**. Nominal spending per resident therefore rose **5.0030%**. A hypothetical construction-price factor that exactly preserves per-person purchasing power is:

`D_2024/D_2018 = (C_2024/C_2018)/(P_2024/P_2018) = 1.050030134`.

Thus **5.0030% cumulative construction inflation**, or approximately **0.8170% annually over six intervals**, is the break-even scenario. Using rounded spending/population bounds gives a break-even cumulative range of **4.9641%–5.0419%**. Above that hypothetical price growth, price-adjusted capital spending per resident would be lower; below it, higher. These are mathematical thresholds, not observed construction inflation.

The observed rounded annual CPI chain rises **20.1257%** over the same six intervals, producing **−12.5891%** consumer-price-adjusted spending per resident. CPI exceeds the break-even threshold by approximately 15.12 percentage points but does not establish how construction prices actually moved. Do not label this comparison an estimate of infrastructure volume, physical capacity, service shortfall or investment need.

Illustrative construction-price scenarios, holding source spending/population fixed:

| Assumed cumulative construction-price growth, 2018–2024 | Calculated per-person price-adjusted change |
|---|---:|
| 0% | +5.003% |
| 5% | approximately +0.003% |
| 10% | −4.543% |
| 20% | −12.497% |
| 30% | −19.228% |

## July 1 versus fiscal-year alignment

July 1 in the fiscal starting calendar year is an explicit annual denominator. It falls **three months into** an April–March fiscal year; it is not the fiscal-year midpoint (approximately October 1). A preferred robustness exercise would calculate the average of April 1, July 1, October 1 and January 1 estimates, consistently for all years, and rerun the comparisons. Neither annual fiscal-average population nor that quarter-based average can be reconstructed exactly from a single July observation.

With CPI fixed, reversal of the 2018–2024 result would require the true endpoint-to-baseline fiscal-average population ratio to be **0.995463 or lower**, versus the observed July ratio of **1.138831**. That is a 12.589% smaller growth factor. This states the magnitude of alignment change needed, without asserting unavailable quarterly values. The closer 2019–2024 result is more fragile: its break-even population ratio is **1.106952**, versus observed July **1.122618**; a 1.395% smaller growth factor could change its sign. Therefore do not present the 2019 baseline's small CPI-adjusted difference as robust to all timing choices.

Likewise exact April–March CPI averages require **monthly index levels**, not arithmetic averages of annual percentage rates. No such monthly series was available in these local annual reports. Do not manufacture a fiscal CPI from rounded calendar growth rates or treat a weighted annual-rate approximation as an observation.

## Cross-report corroboration and next checks

Local official annual-report extracts independently corroborate historical **calendar-year** CPI rates: `2020-21 Budget.txt` economic indicator row includes 2015–2020 rates **1.1, 1.1, 1.6, 2.4, 1.8, 1.1%**; `2021-22 Budget.txt` reports 2021 **3.2%**; `tbf-goa-2023-2024 Budget.txt` reports 2022 **6.4%** and 2023 **3.3%**. These corroborate the primary 2024-25 Final Results table. Despite their filenames, source contents are year-end final-results reports. Their population histories differ by revision/vintage, reinforcing the choice to use one vintage consistently. They do not supply a verified April–March monthly CPI panel.

Once official data access works: archive latest quarterly population source rows; construct consistent fiscal averages; archive monthly Alberta all-items CPI levels; compare calendar versus fiscal CPI; and add explicitly scoped Edmonton/Calgary non-residential building-price sensitivity with coverage/base-year checks. Province-wide engineering works and project mix still require separate treatment. None of these unavailable series should be substituted by invented values.
