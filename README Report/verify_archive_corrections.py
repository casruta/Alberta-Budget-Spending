"""Independently verify corrected archive narrative against retained source cells."""
from pathlib import Path
import csv,json,math,re

ROOT=Path(__file__).resolve().parents[1]

def rows(path):
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def item(records,field,value):return next(r for r in records if r[field]==value)

text=(ROOT/'2026-2029 Fiscal Plan/README.md').read_text()
revenue=rows('Data/fiscal_plan_2026_revenue.csv');ministry=rows('Data/fiscal_plan_2026_ministry_expenses.csv');position=rows('Data/fiscal_plan_2026_financial_position.csv')
checks={}
for name in ['Total tax revenue','Transfers from Government of Canada','Total non-renewable resource revenue']:
    r=item(revenue,'Item',name);start=float(r['2024-25 Actual']);end=float(r['2026-27 Estimate']);growth=(end/start-1)*100
    label={'Total tax revenue':'Tax Revenue','Transfers from Government of Canada':'Federal Transfers','Total non-renewable resource revenue':'Resource Revenue'}[name]
    cells=next(line for line in text.splitlines() if line.startswith('| '+label+' |')).strip('|').split('|');cells=[x.strip() for x in cells]
    expected=[label,f'${start/1000:.1f}',f'${end/1000:.1f}',f"${float(r['2028-29 Target'])/1000:.1f}",f'{growth:+.1f}%']
    assert cells==expected,(cells,expected)
    checks[name]={'2024_25_actual_million':start,'2026_27_estimate_million':end,'change_pct':growth,'2028_29_target_million':float(r['2028-29 Target'])}
col='2026-27 Estimate';groups=['Hospital and Surgical Health Services','Primary and Preventative Health Services','Mental Health and Addiction','Education and Childcare','Advanced Education','Assisted Living and Social Services','Children and Family Services']
numerator=sum(float(r[col]) for r in ministry if r['Ministry'] in groups);denominator=float(item(ministry,'Ministry','Total program expense')[col]);share=numerator/denominator*100
assert f'{share:.1f}% of 2026–27 program expense' in text
checks['health_education_social_share']={'ministries':groups,'numerator_million':numerator,'denominator_million':denominator,'share_pct':share}
for name,values in [('Net assets',[24508,-3483]),('Net financial assets / (debt)',[-34337,-69750])]:
    r=item(position,'Item',name);actual=float(r['At March 31, 2025 (Actual)']);target=float(r['At March 31, 2029 (Target)']);assert [actual,target]==values
    for value in values:assert f'{abs(value)/1000:.3f}B' in text
    checks[name]={'march_2025_actual_million':actual,'march_2029_target_million':target}
assert 'liabilities will exceed financial assets for the first time' not in text
assert 'not been independently verified' in text
assert 'projections show persistent deficits' in text and 'do not isolate the structural or cyclical share' in text
root_text=(ROOT/'README.md').read_text();assert 'Median AISH' in root_text and 'continuing-care placement within 30 days' in root_text
result={'status':'passed','evidence':'Original retained CSV cells; arithmetic independent of Power BI display helpers','corrected_comparisons':checks,'limits':'Selected archive financial corrections; historical external comparisons and policy scenarios are not fully audited.'}
(ROOT/'README Report/archive_correction_results.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: corrected revenue table, policy-group denominator and both net-assets definitions match retained source cells.')
