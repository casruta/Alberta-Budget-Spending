#!/usr/bin/env python3
"""Reproduce source-backed demographic and CPI sensitivity inputs without network."""
import ast, csv, hashlib, json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'Budget PDFs' / '2024-2025 Budget.pdf'
NOTEBOOK = ROOT / '2011-2025 Expense Analysis' / 'Alberta_Expense_Analysis.ipynb'
SOURCE_URL = 'https://open.alberta.ca/publications/government-of-alberta-annual-report'
text = subprocess.check_output(['pdftotext', '-f', '13', '-l', '13', '-layout', str(SOURCE), '-'], text=True)
(HERE / 'population_cpi_source_page.txt').write_text(text)
assert '2024-25 Final Results | Year-End Report' in text
assert '2013' in text and '2024' in text

def values(prefix):
    lines=[line for line in text.splitlines() if line.strip().startswith(prefix)]
    assert len(lines)==1, (prefix, lines)
    result=re.findall(r'[\d,]+(?:\.\d+)?', lines[0].split(prefix,1)[1])
    assert len(result)==12, (prefix,result)
    return result

pop=[int(x.replace(',',''))*1000 for x in values('Population (July 1, thousands)')]
rates=[float(x) for x in values('Alberta consumer price index')]
assert pop==[3979000,4081000,4150000,4195000,4237000,4293000,4355000,4407000,4432000,4511000,4685000,4889000]
assert rates==[1.4,2.6,1.1,1.1,1.6,2.4,1.8,1.1,3.2,6.4,3.3,2.9]
# Chain rounded rates. This is NOT an official CPI level or fiscal-year deflator.
index=100.0
records=[]
for year,population,rate in zip(range(2013,2025),pop,rates):
    if year < 2015: continue
    if year > 2015:index*=1+rate/100
    records.append(dict(calendar_year=year,fiscal_year=f'{year}-{str(year+1)[-2:]}',population_july_1=population,population_precision='rounded to nearest 1000',population_basis='July 1 estimate; historical report vintage',alberta_annual_cpi_growth_pct=rate,cpi_chained_index_2015_100=round(index,8),cpi_deflator_to_2024=0,source_file=str(SOURCE.relative_to(ROOT)),source_pdf_page=13,source_printed_page=13,source_report='2024-25 Final Results Year-End Report',source_table='Key Economic Indicators 2013 to 2024',data_quality='official local PDF; rounded population and CPI growth; not latest StatsCan vintage'))
for row in records:row['cpi_deflator_to_2024']=round(index/row['cpi_chained_index_2015_100'],8)
with (HERE/'demography_cpi_2015_2024.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)

# Read hard-coded notebook inputs without running notebook code.
existing={}
for cell in json.loads(NOTEBOOK.read_text())['cells']:
    if cell['cell_type']!='code':continue
    try:tree=ast.parse(''.join(cell['source']))
    except SyntaxError:continue
    for node in tree.body:
        if isinstance(node,ast.Assign) and isinstance(node.value,ast.Dict):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in {'POP','CPI'}:existing[target.id]=ast.literal_eval(node.value)
comparison=[]
for row in records:
    fy=row['fiscal_year'];yr=row['calendar_year'];nbpop=existing['POP'][fy];nbcpi=existing['CPI'][fy]
    prev=existing['CPI'].get(f'{yr-1}-{str(yr)[-2:]}')
    nbrate=(nbcpi/prev-1)*100 if prev else None
    comparison.append(dict(fiscal_year=fy,notebook_population=nbpop,official_local_population_rounded=row['population_july_1'],population_difference=nbpop-row['population_july_1'],notebook_cpi=nbcpi,notebook_implied_cpi_growth_pct=round(nbrate,6),official_local_cpi_growth_pct=row['alberta_annual_cpi_growth_pct'],cpi_growth_difference_pp=round(nbrate-row['alberta_annual_cpi_growth_pct'],6)))
with (HERE/'existing_notebook_input_audit.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=comparison[0]);w.writeheader();w.writerows(comparison)
meta=dict(source_file=str(SOURCE.relative_to(ROOT)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),source_report='2024-25 Final Results | Year-End Report',table='Key Economic Indicators, 2013 to 2024',pdf_page=13,printed_page=13,report_table_metadata_date='2025-06-19',provenance_url=SOURCE_URL,provenance_url_status='catalog landing page; not independently retrieved in this environment',network_blocker='StatCan CSV download proxy 403; direct egress DNS unavailable',official_population_table='17-10-0009-01',official_annual_cpi_table='18-10-0005-01',official_monthly_cpi_table='18-10-0004-01',official_construction_price_table='18-10-0276-01',missing_years=[2025,2026],extrapolation='none',population_growth_2015_2024_pct=(pop[-1]/pop[2]-1)*100,population_growth_2019_2024_pct=(pop[-1]/pop[6]-1)*100,cpi_chained_growth_2015_2024_pct=index-100,rows=len(records))
(HERE/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({k:meta[k] for k in ['rows','population_growth_2015_2024_pct','population_growth_2019_2024_pct','cpi_chained_growth_2015_2024_pct']},indent=2))
