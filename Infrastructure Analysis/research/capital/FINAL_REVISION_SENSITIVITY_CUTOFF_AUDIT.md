# Final improvement-loop audit: revision sensitivity and evidence cutoff

## Independent calculation directly from original PDFs

Opened original `Budget PDFs/2024-2025 Budget.pdf` and `Budget PDFs/2018-19 Budget.pdf` with PyMuPDF. Parsed capital totals directly from latest historical p14 and contemporary2018–19 fiscal summary p3. Parsed latest population/CPI directly from p13; did not import analysis scripts or consume analysis-output CSVs.

Latest p14:2018–19 capital6,057M;2024–25 capital7,243M. Contemporary2018–19 p3 actual6,180M. Latest p13 July2018/2024 population4,293/4,889 thousand; annual CPI2019–2024 rates1.8,1.1,3.2,6.4,3.3,2.9 percent. Their compounded CPI factor is1.2012570655721153; population ratio1.138830654553925.

Calculation:

`adjusted per-resident change = (7243 / baseline capital / (4889 / 4293) / product(1 + CPI2019..2024/100) − 1) ×100`

| Scenario |2018–19 baseline $M|Nominal capital growth|CPI-adjusted/resident change|Constant-intensity benchmark2024–25 $M|
|---|---:|---:|---:|---:|
|Recommended common latest vintage|6,057|+19.580650%|−12.589057%|8,286.147839|
|Deliberate mixed-vintage revision illustration|6,180|+17.200647%|−14.328789%|8,454.415328|

The unexplained−123M revision shifts the adjusted/resident comparison by **1.739732 percentage points**, from−14.33% to−12.59%; it changes magnitude appreciably but **does not reverse the sign** under this deliberately narrow calculation. The benchmark shifts168.267490M. This is **not a recommended alternative baseline series**, an accounting-adjusted causal estimate, or an uncertainty interval. It deliberately mixes the contemporary baseline with latest endpoint/demography to isolate arithmetic sensitivity to one known revision. It does not bound all accounting, fiscal-alignment, population-vintage or construction-price uncertainty.

## Source date is distinct from observation cutoff

Original PDF metadata identifies **2024–25 Final Results – Year-end Report**, author Government of Alberta–Treasury Board and Finance; creationJune25,2025, modificationJune26,2025. Filename “Budget” does not determine its status. It is a final-results report published after the fiscal cutoff.

Financial actual observations in p3/p14 end2024–25, i.e.March31,2025. The report’s annual infrastructure narrative includes later context: **p15 says the Compassionate Intervention Act passed in May2025**. This is post-cutoff legislation, not evidence of infrastructure physically delivered or fiscal spending during2024–25. It must not count as completed infrastructure byMarch31,2025.

Original latest p20 provides an explicit observation-date control: “This section highlights the total projects completed and underway by category, which also includes the total assets existing and in operation in the province **as of March31,2025**.” It identifies3 existing recovery communities/200beds,12 completed schools/11,000+ new-or-modernized spaces and other year-end stock/project statuses. This supports the report’s recovery-community inventory at the cutoff without relying solely on ambiguous p15 “open” prose.

## Delivered report check

Read current REPORT.md and searched for “May2025”, “Compassionate”, “Act”, “passed”, “cutoff” and physical-project rows. The delivered report:

- Correctly identifies the primary source as Final Results and the accounting/spending observation window as through2024–25.
- Does not count the May2025 Act as completed infrastructure or assign its passage any2024–25 expenditure.
- Treats School Construction Accelerator outputs as anticipated future pipeline, not delivered seats.
- Uses latest inventory/project records with explicit construction-versus-operation caveats; future projects retain expected stages and are not included as delivered.
- Documents the unknown2025–26 actuals coverage rather than extrapolating.

**Minor wording refinement:** heading “Evidence cutoff:March31,2025” could read **“Spending and year-end observation cutoff:March31,2025; primary source publishedJune2025”**. This distinguishes source publication/context dates from the measured window. Add p20 citation to the recovery200bed row if currently only p15 is linked; p20 explicitly supplies the cutoff-date inventory.

No source or analysis CSVs were modified by this audit.
