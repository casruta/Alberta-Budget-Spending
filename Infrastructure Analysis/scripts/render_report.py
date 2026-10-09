"""Render report/README from reviewed outputs; create a notebook companion."""
from pathlib import Path
import sys
import pandas as pd
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def pct(number, signed=False):
    return f'{number:+.1f}%' if signed else f'{number:.1f}%'


def dollars(number):
    return f'${number:,.0f}'


def markdown_table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |',
        '| '+' | '.join(['---']*len(headers))+' |'] +
        ['| '+' | '.join(map(str,row))+' |' for row in rows])


def render():
    data = pd.read_csv(ROOT/'data/capital_population_analysis.csv').set_index('calendar_year')
    comparisons = pd.read_csv(ROOT/'data/baseline_comparisons.csv').set_index('baseline')
    periods = pd.read_csv(ROOT/'data/tenure_summary.csv')
    replacements = {}
    for year in [2015,2018,2019,2022,2023,2024]:
        row = data.loc[year]
        replacements[f'capital_{year}_b'] = f'${row.capital_nominal_cad/1e9:.2f}'
        replacements[f'pc_{year}_nominal'] = dollars(row.capital_nominal_per_resident_cad)
        replacements[f'pc_{year}_real'] = dollars(row.capital_cpi_adjusted_per_resident_2024_cad)
    for year in [2015,2018,2019,2022,2023]:
        row = comparisons.loc[f'{year}-{str(year+1)[-2:]}']
        for suffix, field in [('nominal','nominal_capital_growth_pct'),
                             ('population','population_growth_pct'),
                             ('cpi','cpi_growth_pct'),
                             ('nominal_pc','nominal_per_resident_growth_pct'),
                             ('real_pc','cpi_adjusted_per_resident_growth_pct')]:
            replacements[f'growth_{year}_{suffix}'] = pct(row[field])
    # Grammar in the report says "fell", so show a positive decline magnitude.
    replacements['growth_2018_real_pc'] = pct(abs(comparisons.loc['2018-19','cpi_adjusted_per_resident_growth_pct']))
    replacements['decline_2019_real_pc'] = pct(abs(comparisons.loc['2019-20','cpi_adjusted_per_resident_growth_pct']))
    replacements['decline_2015_real_pc'] = pct(abs(comparisons.loc['2015-16','cpi_adjusted_per_resident_growth_pct']))
    replacements['growth_2018_to_2019_nominal'] = pct(abs(data.loc[2019,'capital_nominal_cad']/data.loc[2018,'capital_nominal_cad']-1)*100)
    replacements['growth_2018_to_2019_real_pc'] = pct(abs(data.loc[2019,'capital_cpi_adjusted_per_resident_2024_cad']/data.loc[2018,'capital_cpi_adjusted_per_resident_2024_cad']-1)*100)
    row = comparisons.loc['2018-19']
    replacements['growth_2018_pop_cpi'] = pct(((1+row.population_growth_pct/100)*(1+row.cpi_growth_pct/100)-1)*100)
    replacements['benchmark_2018_b'] = f'${row.endpoint_constant_intensity_benchmark_cad/1e9:.2f}'
    replacements['benchmark_2018_difference_b'] = f'${abs(row.endpoint_difference_from_benchmark_cad)/1e9:.2f}'
    replacements['rounding_2018_low'] = pct(row.rounding_sensitivity_real_per_resident_growth_low_pct)
    replacements['rounding_2018_high'] = pct(row.rounding_sensitivity_real_per_resident_growth_high_pct)
    col='population_weighted_cpi_adjusted_per_resident_annual_2024_cad'
    pre,ucp,ex=periods.loc[0,col],periods.loc[1,col],periods.loc[2,col]
    replacements.update({'tenure_pre_real':dollars(pre),'tenure_ucp_real':dollars(ucp),
        'tenure_pre_without_spike_real':dollars(ex),
        'tenure_difference_pct':pct((ucp/pre-1)*100),
        'tenure_ex_spike_difference_pct':pct(abs((ucp/ex-1)*100))})
    replacements['annual_table']=markdown_table(
        ['Fiscal year','Capital spending, CAD B','July population, M','Nominal CAD/resident','2024 CPI-adjusted CAD/resident'],
        [[r.fiscal_year,f'{r.capital_nominal_cad/1e9:.3f}',f'{r.population_july_1/1e6:.3f}',
          dollars(r.capital_nominal_per_resident_cad),dollars(r.capital_cpi_adjusted_per_resident_2024_cad)]
         for _,r in data.iterrows()])
    replacements['comparison_table']=markdown_table(
        ['Baseline → 2024–25','Total nominal spending','Population','Consumer prices','Nominal per resident','CPI-adjusted per resident'],
        [[f'{label} → 2024–25',pct(r.nominal_capital_growth_pct,True),pct(r.population_growth_pct,True),
          pct(r.cpi_growth_pct,True),pct(r.nominal_per_resident_growth_pct,True),
          pct(r.cpi_adjusted_per_resident_growth_pct,True)] for label,r in comparisons.iloc[:3].iterrows()])
    execution=pd.read_csv(ROOT/'data/budget_execution_analysis.csv')
    replacements['execution_table']=markdown_table(
        ['Fiscal year','Paired budget, CAD M','Contemporary actual, CAD M','Actual / budget','Latest historical actual, CAD M'],
        [[r.fiscal_year,f'{r.budget_million:,.0f}',f'{r.contemporary_actual_million:,.0f}',
          pct(r.budget_execution_pct),f'{r.latest_2024_25_vintage_actual_million:,.0f}']
         for _,r in execution.iterrows()])
    envelopes=pd.read_csv(ROOT/'research/capital/actual_recent/recent_envelopes_all_vintages.csv')
    envelopes=envelopes.loc[envelopes.source_vintage=='2024-25']
    pivot=envelopes.pivot(index='envelope',columns='fiscal_year',values='actual_cad_millions')
    pivot=pivot.loc[~pivot.index.str.startswith('Total Capital Plan')]
    pivot['change']=pivot['2024-25']-pivot['2023-24']
    pivot=pivot.sort_values('change',ascending=False)
    replacements['latest_sector_table']=markdown_table(
        ['Capital envelope','2023–24 actual, CAD M','2024–25 actual, CAD M','Change, CAD M'],
        [[label,f'{r["2023-24"]:,.0f}',f'{r["2024-25"]:,.0f}',f'{r["change"]:+,.0f}']
         for label,r in pivot.iterrows()])
    template=(ROOT/'report_template.md').read_text()
    for key,value in replacements.items():
        template=template.replace('{{'+key+'}}',value)
    if '{{' in template:
        raise ValueError('Unfilled report variables')
    (ROOT/'REPORT.md').write_text(template)
    readme=f'''# Alberta infrastructure spending and delivery analysis

**Prepared October 9, 2026 · source actuals through March 31, 2025**

Actual capital spending rose **19.6% from 2018–19 to 2024–25**, but population growth and consumer-price inflation together exceeded that increase. **CPI-adjusted capital spending per resident fell 12.6%.** Identifiable schools, health facilities, highways, bridges and flood protection were delivered after 2019; available records do not establish aggregate net capacity or whether it kept pace with population. Projects often began before the UCP government.

Read the **[full report](REPORT.md)** for the financial evidence, baseline sensitivity, sector changes, physical deliveries and source limitations. Use the **[executed notebook](Alberta_Infrastructure_Analysis.ipynb)** for inspectable calculations and figures.

![Capital spending per resident](plots/02_spending_per_resident.png)

## Scope and important distinctions

- The political transition is the UCP taking office in April 2019; 2018–19 is the last full pre-UCP year. Earlier Alberta conservative governments are not treated as beginning in 2019.
- Ten accessible actual years cover **2015–16 through 2024–25**. As of October 2026 the latest completed decade is 2016–17 through 2025–26; that final year remains unavailable in the accessible corpus. No missing actuals were forecast or filled with zero.
- Primary figures are the fully consolidated **Capital Plan**, not operating expense or the Infrastructure ministry budget. Grants and investment have different accounting treatment; do not add the entire capital plan to expense.
- Consumer-price adjustment is a **sensitivity**, not a construction-volume measure. July population and starting-calendar-year annual CPI approximate fiscal alignment.
- A source's project completion is not necessarily operational opening, net-new capacity, or exclusive policy attribution. Missing net stock and condition data remain missing.
- The official historical table warns of accounting-policy changes even within the same source vintage. Recent sector comparisons use same-report reclassified pairs.

## Reproduce

The prepared cloud environment has Python 3.12 and `/workspace/.venv`. The existing checkout is already isolated; use it directly and do not create a Git worktree unless explicitly requested.

```bash
cd '/workspace/Alberta-Budget-Spending/Infrastructure Analysis'
export MPLCONFIGDIR=/workspace/.cache/matplotlib
export XDG_CACHE_HOME=/workspace/.cache
export IPYTHONDIR=/workspace/.cache/ipython
export JUPYTER_CONFIG_DIR=/workspace/.cache/alberta-analysis/jupyter
export JUPYTER_RUNTIME_DIR=/workspace/.cache/alberta-analysis/jupyter/runtime
export JUPYTER_DATA_DIR=/workspace/.venv/share/jupyter
/workspace/.venv/bin/python research/capital/extract_primary.py
/workspace/.venv/bin/python research/capital/extract_execution_composition.py
/workspace/.venv/bin/python research/demography/extract_demography.py
/workspace/.venv/bin/python research/demography/build_vintage_ledger.py
/workspace/.venv/bin/python research/demography/verify_vintage_ledger.py
/workspace/.venv/bin/python scripts/build_claim_register.py
/workspace/.venv/bin/python scripts/build_corpus_inventory.py
/workspace/.venv/bin/python scripts/analyze.py
/workspace/.venv/bin/python scripts/physical_figures.py
/workspace/.venv/bin/python scripts/price_sensitivity.py
/workspace/.venv/bin/python scripts/execution_figures.py
/workspace/.venv/bin/python scripts/render_report.py
/workspace/.venv/bin/python -m pytest tests -q
PATH=/workspace/.venv/bin:$PATH /workspace/.venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Alberta_Infrastructure_Analysis.ipynb
/workspace/.venv/bin/python scripts/quality_gate.py
# Optional self-contained notebook export; Classic preserves the authored image alternatives.
/workspace/.venv/bin/python -m jupyter nbconvert --to html --template classic --output Alberta_Infrastructure_Analysis_preview.html Alberta_Infrastructure_Analysis.ipynb
```

For a fresh machine, install the versions in [requirements.txt](requirements.txt) into a virtual environment before those commands. The demographic extraction also requires Poppler's `pdftotext` command (version 25.03.0 is verified here); Python requirements alone do not install it. The saved installer checks a functional Poppler extraction against the official population/CPI page. The extraction and analysis workflow runs from local files without official-site access. Source outputs are regenerated inside this new analysis directory; existing tracked datasets, PDFs and notebooks remain unchanged. Review generated results before replacing user-edited report text.

JupyterLab is optional for browsing/editing; notebook execution and the validation tests are required to demonstrate reproducibility. Startup and health checks are saved in the cloud environment configuration. A running Jupyter process does not survive an environment snapshot and must be restarted when needed.

```bash
# Optional authenticated local editor; the helper never prints a token or preview URL.
/workspace/.venv/bin/python scripts/jupyter_service.py start
/workspace/.venv/bin/python scripts/jupyter_service.py status
/workspace/.venv/bin/python scripts/jupyter_service.py verify-kernel
# Stop only the service started by this helper when it is no longer needed.
/workspace/.venv/bin/python scripts/jupyter_service.py stop
```

## Evidence and outputs

| Location | Contents |
|---|---|
| [REPORT.md](REPORT.md) | Narrative report, actual spending, population/CPI sensitivity, sector and physical evidence |
| [Alberta_Infrastructure_Analysis.ipynb](Alberta_Infrastructure_Analysis.ipynb) | Executed reproducible notebook with visible tables and figures |
| [data/](data/) | Analysis panel, baseline comparisons, weighted tenure summaries and run manifest |
| [plots/](plots/) | Standalone PNG and SVG figures |
| [research/capital/](research/capital/) | Source-extracted actual totals, reclassifications, budget comparisons and exact pages |
| [research/demography/](research/demography/) | Rounded official population/CPI inputs, provenance and robustness audit |
| [research/physical/](research/physical/) | Physical-output ledger, health evidence and audited 17-project status timeline |
| [review/](review/) | Independent review, calculation checks and correction log |
| [Claim register](research/source_verification/CLAIM_REGISTER.md) | Consequential claims linked to original source pages, extracts and interpretation limits |
| [Evidence gaps](research/source_verification/EVIDENCE_GAPS.md) | Missing sources/definitions and acceptance checks for a latest-decade or net-capacity extension |
| [Source inventory](research/source_verification/CORPUS_INVENTORY.md) | PDF identities, hashes and full-volume versus short-summary coverage |
| [tests/](tests/) | Source, arithmetic, reconciliation and artifact-consistency checks |

All main financial inputs come from [2024–25 Final Results, PDF pp. 13–14](../Budget%20PDFs/2024-2025%20Budget.pdf#page=13). The file is misleadingly named “Budget”; its internal title and source metadata identify a June 2025 final-results report. Exact paths, hashes, units, definitions and source vintages are retained. URLs in provenance are catalog/reference links, not a claim that blocked online sources were retrieved.

## Validation and remaining limits

See [validation log](review/validation_log.md) for the checks actually performed and corrections from independent review. The team separated capital extraction, population/price inputs, physical-project research and independent recomputation, with subagents handling recent sector tables and healthcare evidence.

The [quality gate](scripts/quality_gate.py) records a bounded validation loop in `review/quality_gate_history.json`. It checks substantive tests, actual notebook execution, nine rendered figures and alternative text, and verifies that embedded notebook images match the saved plots. A failing gate requires a real correction before rerunning. It stops on a pass and does not repeatedly run unchanged tests or fabricate missing data. Independent human-style source review remains separate from the automated gate. A clean virtual environment without system site packages also passed the checks, reducing the risk that preinstalled libraries conceal missing requirements; this does not test restoration in a new cloud task.

The additional source-verification loop distinguishes contemporary budget execution from revised historical actuals, records grants versus investment, and archives cross-vintage demographic revisions. The latest $943M nominal increase is $831M grants plus $112M investment; neither component proves net physical capacity. Two exact financial revision causes remain unresolved and are explicitly identified in the report.

Official Alberta and Statistics Canada retrieval currently returns proxy access errors. Required domains were saved in the configuration draft; review/save settings and publish the environment to enable future work under the supported flow. No secret is needed for these public sources. The report does not claim fresh-task restoration has been tested.

The Data report-app runtime is unavailable here, so no hosted interactive report was built or published. The delivered report is repository Markdown with standalone figures and an executed notebook companion. Province-wide net capacity, condition, construction-price adjustment and the 2025–26 actual year remain unresolved evidence requirements.
'''
    (ROOT/'README.md').write_text(readme)
    print('Rendered REPORT.md and analysis README.md from reviewed numerical outputs.')


def notebook():
    nb=nbformat.v4.new_notebook()
    cells=[]
    def md(text):cells.append(nbformat.v4.new_markdown_cell(text))
    def code(text):cells.append(nbformat.v4.new_code_cell(text))
    md('# Alberta infrastructure spending and delivery, 2015–16 to 2024–25\n\n## tl;dr\n\nActual capital spending rose 19.6% from 2018–19 to 2024–25, but CPI-adjusted spending per resident fell 12.6%. The latest year improved 7.1% on the adjusted per-resident measure. Selected physical deliveries are documented; net provincial capacity and condition remain unquantified.\n\nThis notebook accompanies [REPORT.md](REPORT.md), which contains the physical evidence and exact source references. Evidence ends March 31, 2025, although the analysis date is October 9, 2026.')
    md('## Context & Methods\n\n### Key assumptions\n\nCapital Plan actuals are financial inputs, not physical capacity. All primary values use the 2024–25 report vintage, whose historical table warns of accounting changes. July 1 population and starting-calendar-year CPI approximate fiscal alignment. Chaining rounded CPI rates measures consumer purchasing power, not construction volume. UCP tenure begins during 2019–20; 2018–19 is the last full pre-UCP baseline.\n\nThe ten-year window is lagged: 2025–26 actuals are unavailable in the accessible corpus. No missing year or physical metric is imputed. There is no causal-policy model.')
    code("from pathlib import Path\nimport sys\nimport pandas as pd\nfrom IPython.display import display, Image\nRUNTIME_EXECUTABLE = sys.executable\nprint('Python runtime:', RUNTIME_EXECUTABLE)\nROOT = Path.cwd()\nassert (ROOT / 'scripts/analyze.py').exists(), 'Execute from Infrastructure Analysis'\nsys.path.insert(0, str(ROOT / 'scripts'))\nfrom analyze import load_primary, compare, period_summary, build_figures\nDATA = load_primary()\nCOMPARISONS = pd.DataFrame([compare(DATA,y) for y in [2015,2018,2019,2022,2023]])\nPERIODS = period_summary(DATA)\nassert len(DATA) == 10 and DATA.fiscal_year.nunique() == 10\nassert DATA.status.eq('actual').all()")
    md('## Data\n\n### 1. Inspect the actual-spending panel\n\nSource: `Budget PDFs/2024-2025 Budget.pdf`, printed/PDF pages 13–14, June 2025 Final Results. CSV extracts preserve units, report vintage and exact page references. See `data/run_manifest.json` for source hashes. Population is in residents; original capital values are CAD millions.')
    code("display(DATA[['fiscal_year','capital_plan_actual_million','population_july_1','cpi_index_2015_100','capital_nominal_per_resident_cad','capital_cpi_adjusted_per_resident_2024_cad']].round(2))")
    md('### 2. Validate inputs and ratios\n\nOne-to-one joins prevent row multiplication. Independently reviewed demographic inputs must agree with the capital-source economic row. A compounded population × price benchmark is required; comparing each separately would understate their combined effect.')
    code("assert DATA.population_july_1.eq(DATA.population_july1_thousands*1000).all()\nbaseline = DATA.loc[DATA.calendar_year.eq(2018)].iloc[0]\nendpoint = DATA.loc[DATA.calendar_year.eq(2024)].iloc[0]\nratio = (endpoint.capital_nominal_cad / baseline.capital_nominal_cad) / (endpoint.population_july_1 / baseline.population_july_1) / (endpoint.cpi_index_2015_100 / baseline.cpi_index_2015_100)\nassert abs((ratio-1)*100 - COMPARISONS.loc[COMPARISONS.baseline.eq('2018-19'),'cpi_adjusted_per_resident_growth_pct'].iloc[0]) < 1e-9\nprint(f'2018–19 to 2024–25: CPI-adjusted spending per resident {(ratio-1)*100:+.4f}%')")
    md('## Results\n\n### 3. Actual capital spending\n\nThe 2017–18 peak partly reflects grants accelerated from future years; annual spending is not construction delivered that year. The initial UCP-period decline follows an earlier fall. Source: final-results historical table, p. 14.')
    code("build_figures(DATA,COMPARISONS,PERIODS)\ndisplay(Image(filename=str(ROOT/'plots/01_actual_capital_spending.png'), alt='Actual capital spending by fiscal year: 6.558 billion in 2015–16, 9.021 billion peak in 2017–18, 5.545 billion in 2019–20, and 7.243 billion in 2024–25. The government transition occurs in April 2019.'))" )
    md('### Reported budget execution and accounting composition\n\nEach final-results report supplies paired budget and contemporary actual columns. These differ from the latest historical actual series when revised. Budget execution is not a project-delivery or efficiency score; the 2020–21 program was revised substantially with $1.1B COVID/recovery support. Never add yearly undershoots into an infrastructure backlog. Capital grants and consolidated investment also have different ownership/accounting implications.')
    code("from execution_figures import build as build_execution_figure\nEXECUTION = build_execution_figure()\ndisplay(EXECUTION[['fiscal_year','budget_million','contemporary_actual_million','budget_execution_pct','latest_2024_25_vintage_actual_million']].round(2))\ndisplay(Image(filename=str(ROOT/'plots/09_reported_budget_execution.png'), alt='Paired capital budget and contemporary actual spending from each final-results report. Spending was below the paired budget in all ten years; execution was 74.9 percent in 2022–23 and 87.3 percent in 2024–25. The 2020–21 ratio of 99.1 percent masks a materially revised program.'))")
    code("composition = pd.read_csv(ROOT/'research/capital/capital_composition_original_vintages.csv')\nlatest_composition = composition.loc[composition.source_vintage.eq('2024-25') & composition.column_status.isin(['actual','prior_actual'])]\ndisplay(latest_composition[['observation_fiscal_year','column_status','capital_grants_million','capital_investment_million','total_capital_plan_million']])\nprint('Latest increase: grants +$831M and investment +$112M = total +$943M; grants explain 88.1% of net nominal growth. Neither component measures net physical capacity.')")
    md('### 4. Population-adjusted spending and the combined benchmark\n\nThe 2024–25 recovery remains below 2018–19 on a consumer-price-adjusted per-resident basis. This is not a measure of net school, hospital or road capacity.')
    code("display(Image(filename=str(ROOT/'plots/02_spending_per_resident.png'), alt='Nominal and 2024 CPI-adjusted capital spending per resident, 2015–16 through 2024–25. CPI-adjusted spending falls from about 1695 dollars in 2018–19 to 1481 dollars in 2024–25.'))" )
    code("display(Image(filename=str(ROOT/'plots/03_growth_benchmarks.png'), alt='Indices with 2018–19 equal to 100. Capital spending reaches about 119.6, population 113.9, and population multiplied by consumer prices about 136.8 in 2024–25.'))" )
    md('### 5. Baseline and period sensitivity\n\nThe first UCP year is already a lower baseline. Unequal tenure lengths require annual averages/intensity; this is descriptive and does not identify a causal government effect.')
    code("display(COMPARISONS[['baseline','endpoint','nominal_capital_growth_pct','population_growth_pct','cpi_growth_pct','cpi_adjusted_per_resident_growth_pct']].round(2))\ndisplay(Image(filename=str(ROOT/'plots/04_baseline_sensitivity.png'), alt='Three baseline comparisons to 2024–25. CPI-adjusted capital spending per resident changes by minus 25.8 percent from 2015–16, minus 12.6 percent from 2018–19, and minus 1.4 percent from 2019–20.'))" )
    code("display(PERIODS[['period','fiscal_years','population_weighted_cpi_adjusted_per_resident_annual_2024_cad']].round(2))\ndisplay(Image(filename=str(ROOT/'plots/06_tenure_sensitivity.png'), alt='Weighted annual CPI-adjusted capital spending per resident is about 2067 dollars pre-UCP, 1532 dollars during UCP tenure, and 1882 dollars pre-UCP excluding the 2017–18 spike. These comparisons are descriptive, not causal.'))" )
    md('### 6. Latest sector changes\n\nSource p. 17 supplies 2023–24 actuals reclassified into the 2024–25 structure. Maintenance and self-financed spending are separate, so named sector envelopes are not all-in sector totals. These changes measure financial allocations, not net service delivery.')
    code("display(Image(filename=str(ROOT/'plots/05_latest_sector_changes.png'), alt='Latest actual capital-envelope changes. Municipal infrastructure rises 489 million dollars and health rises 318 million; education falls 13 million and public safety falls 99 million. Components have a one-million rounding difference from the consolidated total.'))" )
    md('### 7. Rounding sensitivity\n\nWorst-case rounding bounds are deterministic, not confidence intervals. They do not cover accounting revisions, fiscal-calendar alignment or construction-price uncertainty. The small 2019 baseline decline is especially sensitive to those broader assumptions.')
    code("display(COMPARISONS[['baseline','cpi_adjusted_per_resident_growth_pct','rounding_sensitivity_real_per_resident_growth_low_pct','rounding_sensitivity_real_per_resident_growth_high_pct']].round(3))")
    md('### Price-measure sensitivity\n\nThe curve varies a hypothetical price factor while holding actual spending and population fixed. It is not observed construction inflation. A 5.0% cumulative factor is the break-even threshold for 2018–19 to 2024–25; the observed CPI chain is shown separately.')
    code("from price_sensitivity import build as build_price_sensitivity\nbuild_price_sensitivity()\ndisplay(Image(filename=str(ROOT/'plots/08_hypothetical_price_sensitivity.png'), alt='Illustrative price sensitivity for 2018–19 to 2024–25. A hypothetical cumulative price increase of 5.0 percent is the per-resident break-even threshold. Observed consumer inflation of 20.1 percent produces a minus 12.6 percent adjusted change. Construction inflation is not observed.'))" )
    md('### 8. Selected physical deliveries and missing net-capacity measures\n\nThe audited project ledger distinguishes inherited planning/construction, completed-status observations, explicitly dated construction completion and operational evidence. An as-of completed list need not record first completion in that year: Quest had operating evidence before its later listing. Unknown dates remain missing. Earlier work can concern the broader phased program, rather than initiation of the later named phase. See the full report for school-space definitions, mixed project counts, highway-unit conflicts and the health-count contradiction.')
    code("from physical_figures import build as build_physical_figure\nbuild_physical_figure()\ndisplay(Image(filename=str(ROOT/'plots/07_selected_project_stages.png'), alt='Selected project-stage observations show earlier work before 2019 and later listed completion for Grande Prairie hospital Phase 2, Calgary Cancer Centre, Misericordia emergency department, Peace River bridge, Calgary ring road and Springbank reservoir. Earlier observations are not initiation dates, and completion definitions differ.'))" )
    code("timeline = pd.read_csv(ROOT/'research/physical/gaploop/project_timeline_audited.csv')\ndisplay(timeline[['project','sector','first_observed_earlier_stage_year','first_reported_completed_status_fy','explicit_construction_completion_fy','operational_year_if_verified']].head(17))")
    md('## Takeaways\n\n1. Alberta spent more nominal capital dollars in 2024–25 than in 2018–19, but less per resident after the CPI adjustment.\n2. The latest rebound and the lower 2019 baseline matter; show both rather than selecting a single partisan comparison.\n3. Documented schools, health projects, roads, bridges and flood protection demonstrate physical deliveries across administrations.\n4. Consistent net capacity, operational readiness and condition data remain needed to establish adequacy relative to population. No spending ratio settles that question.\n\nReproduce using README.md. Independently recomputed calculations and correction history are retained in review/.')
    nb.cells=cells
    nb.metadata={'kernelspec':{'display_name':'Alberta analysis (Python 3)','language':'python','name':'alberta-analysis'},
                 'language_info':{'name':'python','version':'3.12'}}
    nbformat.validate(nb)
    nbformat.write(nb,ROOT/'Alberta_Infrastructure_Analysis.ipynb')
    print('Created notebook companion; execute it before delivery.')


if __name__=='__main__':
    render()
    if '--preserve-notebook' not in sys.argv:
        notebook()
