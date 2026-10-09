"""Render source-backed prose and an inspectable notebook companion."""
from pathlib import Path
import json
import re
import nbformat
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def polish(text):
    for a,b in {'FirstNations':'First Nations','MétisandInuit':'Métis and Inuit',
                'PublicSafetyandEmergencyServices':'Public Safety and Emergency Services',
                'MentalHealthandAddiction':'Mental Health and Addiction',
                'Jobs,EconomyandTrade':'Jobs, Economy and Trade','MarketBasketMeasure':'Market Basket Measure',
                'RockyMountainHouse':'Rocky Mountain House','InfrastructureAnalysis':'Infrastructure Analysis',
                'StatisticsCanada':'Statistics Canada','CanadianIncomeSurvey':'Canadian Income Survey',
                'Verygood':'Very good','ConnectCare':'Connect Care'}.items():
        text=text.replace(a,b)
    # Numeric source transcription notes are compact; prose needs readable spacing.
    text=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', text)
    text=re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)
    text=re.sub(r'(\d) (st|nd|rd|th)\b', r'\1\2', text)
    text=re.sub(r'(\d) ([BM])\b', r'\1\2', text)
    text=re.sub(r'(?<=[,;:])(?=[A-Za-z])', ' ', text)
    # Do not alter file paths, stable figure IDs or Markdown hrefs.
    return text


def render():
    receipts=json.loads((ROOT/'data/figure_receipts.json').read_text())
    template=(ROOT/'research/report_template.md').read_text()
    comparisons=pd.read_csv(ROOT/'data/functional_expense_baseline_comparisons.csv')
    subset=comparisons[comparisons.baseline_calendar_year==2018]
    spending='|Function|Nominal expense growth|CPI-adjusted expense/resident change|\n|---|---:|---:|\n'
    for row in subset.itertuples():
        spending+=f'|{row.function}|{row.nominal_growth_pct:+.1f}%|{row.cpi_adjusted_per_resident_growth_pct:+.1f}%|\n'
    template=template.replace('{{spending_table}}',spending)
    # Polish prose fragments before substituting link/figure markup, preserving actual paths.
    segments=re.split(r'(\]\([^\n]*?\)|\{\{figure_[^}]+\}\})',template)
    template=''.join(s if s.startswith('](') or s.startswith('{{figure_') else polish(s) for s in segments)
    for item in receipts:
        template=template.replace('{{figure_'+item['id']+'}}',f"![{polish(item['alt'])}]({item['png']})\n\n*{polish(item['source']).replace(chr(10),' ')}*")
    assert '{{' not in template, 'Unresolved report placeholders'
    (ROOT/'REPORT.md').write_text(template)
    cells=[nbformat.v4.new_markdown_cell('# Alberta budget and quality-of-life evidence\n\n'
        'This executed companion rebuilds derived data and figures from reviewed government sources. '
        'Read [REPORT.md](REPORT.md) for conclusions and row/source limitations. No composite QoL score or causal effect is estimated.'),
        nbformat.v4.new_code_cell("from pathlib import Path\nimport sys, subprocess, json\nimport pandas as pd\nfrom IPython.display import display, Markdown\nROOT=Path.cwd()\nassert (ROOT/'research/report_template.md').exists(), 'Run from Quality of Life Analysis'\nprint('Runtime:',sys.executable)\nprint('PDF extractor:',subprocess.check_output(['pdftotext','-v'],stderr=subprocess.STDOUT,text=True).splitlines()[0])"),
        nbformat.v4.new_markdown_cell('## Rebuild reviewed financial/economic sources\n\n'
        'Rebuilds from original PDFs with definition checks; it does not download or alter original files. '
        'Historical expense cells retain the published accounting anomaly.'),
        nbformat.v4.new_code_cell("for script in ['research/budget/extract_functional_expense.py','research/living_standards/extract_living_standards.py','research/living_standards/extract_current_social_outcomes.py','research/living_standards/extract_childcare_income_access.py','research/living_standards/extract_mbm_poverty.py','research/health/life_tables/extract_life_expectancy.py','research/source_verification/extract_safety_mental_health.py','research/health/extract_health_outcomes.py','scripts/analyze_inputs.py','scripts/build_figures.py']:\n    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)"),
        nbformat.v4.new_code_cell("comparison=pd.read_csv(ROOT/'data/functional_expense_baseline_comparisons.csv')\ndisplay(comparison[comparison.baseline_calendar_year.isin([2015,2018,2019])].round(2))"),
        nbformat.v4.new_markdown_cell('## Outcome evidence and matched periods\n\n'
        'Source vintages, observation periods, eligibility and targets are retained. '
        'Current school/cohort completion ends2023–24, Grade9 achievement ends2024–25, and crime ends calendar2023.'),
        nbformat.v4.new_code_cell("health=pd.read_csv(ROOT/'research/health/extracted/health_outcomes.csv')\ndisplay(health[health.source_vintage=='2024-25'][['metric','group','period','value','unit','target','physical_pdf_page','limitations']])"),
        nbformat.v4.new_code_cell("education=pd.read_csv(ROOT/'research/education_safety/current_education_observations.csv')\ndisplay(education[['metric','observation_period','value','record_kind','source_pdf_page']])"),
        nbformat.v4.new_code_cell("economy=pd.read_csv(ROOT/'data/economic_outcome_context.csv')\ndisplay(economy[['calendar_year','average_weekly_earnings','weekly_earnings_cpi_adjusted_2024_cad','unemployment_rate','primary_household_income_growth','primary_household_income_growth_status']])"),
        nbformat.v4.new_code_cell("social=pd.read_csv(ROOT/'research/living_standards/current_social_outcomes_2021_2024.csv')\ndisplay(social[['period','metric','value','unit','status','source_pdf_page','interpretation_limit']])"),
        nbformat.v4.new_code_cell("poverty=pd.read_csv(ROOT/'research/living_standards/mbm_poverty_all_persons_2015_2024.csv')\ndisplay(poverty[['calendar_year','geography','mbm_base','poverty_rate_pct','quality_flag','quality_definition','comparability']])\nassert poverty[(poverty.mbm_base=='Market basket measure, 2018 base') & (poverty.calendar_year==2024)].empty, 'Do not invent a missing base/year'"),
        nbformat.v4.new_code_cell("life=pd.read_csv(ROOT/'research/health/life_tables/life_expectancy_age0_bothsexes.csv')\nlife=life[(life.Element=='Life expectancy (in years) at age x (ex)') & (life.REF_DATE.between(2015,2024))].copy()\nlife['source_status']=life.REF_DATE.map(lambda y:'preliminary (metadata Note3)' if y in [2023,2024] else 'current source-vintage estimate')\ndisplay(life[['REF_DATE','GEO','VALUE','source_status','VECTOR']])\nprint('Blank raw status does not override metadata preliminary note.')"),
        nbformat.v4.new_markdown_cell('## Standalone figures\n\nEach figure has visible source/definition notes and an alternative description. '
        'Different outcome domains are not added or averaged.')]
    for item in receipts:
        cells.append(nbformat.v4.new_code_cell(
            f"display(Markdown({('!['+polish(item['alt'])+']('+item['png']+')')!r}))"))
    cells += [nbformat.v4.new_markdown_cell('## Independent verification\n\n'
        'Direct-source second-parser checks and Decimal calculations are separate from the main extraction. '
        'Inspect review memos and source hashes for exact scope.'),
        nbformat.v4.new_code_cell("for script in ['research/budget/verify_functional_expenses_independent.py','research/living_standards/verify_living_standards.py','research/living_standards/verify_mbm_poverty.py','research/health/verify_bbox_values.py']:\n    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)")]
    notebook=nbformat.v4.new_notebook(cells=cells)
    notebook.metadata={'kernelspec':{'display_name':'Alberta analysis','language':'python','name':'alberta-analysis'},
                       'language_info':{'name':'python','version':sys_version()}}
    nbformat.write(notebook,ROOT/'Alberta_Budget_Quality_of_Life.ipynb')
    print(f'Rendered report and notebook with{len(receipts)}figures and{sum(c.cell_type=="code" for c in cells)}code cells.')


def sys_version():
    import platform
    return platform.python_version()


if __name__=='__main__':render()
