#!/usr/bin/env python3
"""Official archived report economic indicators, with exact source rows and status."""
from pathlib import Path
import subprocess,re,csv,json,hashlib
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
SOURCES=[('2024-2025 Budget.pdf',13,2013,2024,'primary_same_vintage_2013_2024'),('2022-2023 Budget.pdf',12,2011,2022,'supplementary_older_vintage_not_spliced')]
METRICS=[('employment','Employment (thousands)','thousands of employed persons',False),('employment_growth','Employment growth','calendar-year percent change',False),('unemployment_rate','Unemployment rate','percent of labour force',False),('average_weekly_earnings','Average weekly earnings ($ / week)','nominal dollars per week',False),('primary_household_income_growth','Primary household income','calendar-year percent change; aggregate income',True),('housing_starts','Housing starts (number of units)','number of housing units started',False)]
rows=[];sources=[]
for name,page,start,end,panel in SOURCES:
 p=ROOT/'Budget PDFs'/name
 t=subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(p),'-'],text=True)
 (H/(p.stem+f'_economic_p{page}.txt')).write_text(t)
 lines=t.splitlines()
 for key,label,unit,marked in METRICS:
  candidates=[l for l in lines if l.strip().startswith(label)]
  assert len(candidates)==1,(label,candidates)
  line=candidates[0];tail=line.split(label,1)[1]
  tokens=re.findall(r'\(?-?\d[\d,]*(?:\.\d+)?\)?',tail)
  assert len(tokens)==end-start+1,(label,tokens)
  vals=[-float(x[1:-1].replace(',','')) if x.startswith('(') else float(x.replace(',','')) for x in tokens]
  for year,value in zip(range(start,end+1),vals):
   status='historical report observation'
   if marked and year==end:status='estimate per a footnote; not final actual'
   rows.append(dict(panel=panel,calendar_year=year,metric=key,value=value,unit=unit,status=status,geography='Alberta',time_basis='calendar year',source_file=str(p.relative_to(ROOT)),source_pdf_page=page,source_printed_page=page,source_report=f'{end}-{str(end+1)[-2:]} Final Results Year-End Report',exact_source_row=line.strip(),source_definition='Calendar year, % change unless otherwise noted',footnote='a '+str(end)+' is an estimate' if marked and year==end else '',interpretation_limit={'employment':'Employment level; total provincial population is not working-age denominator.','employment_growth':'Published growth can differ from growth of rounded employment levels.','unemployment_rate':'Labour-force denominator; includes neither all population nor every non-employed person.','average_weekly_earnings':'Average nominal earnings; not median, household disposable income, or fixed worker wage.','primary_household_income_growth':'Aggregate primary income; not per-capita, median, after-tax/disposable income, or poverty rate.','housing_starts':'Starts, not completions; does not establish affordability, rents, ownership access, or net stock.'}[key]))
 sources.append(dict(source_file=str(p.relative_to(ROOT)),source_pdf_page=page,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),panel=panel,calendar_year_start=start,calendar_year_end=end))
with (H/'economic_indicators_source_ledger.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(H/'source_manifest.json').write_text(json.dumps(sources,indent=2)+'\n')
# Independent contextual evidence is preserved verbatim; no invented rates or comparator series.
from pypdf import PdfReader
selected=[('2024-2025 Budget.pdf',13),('2013-2014 Annual Report.pdf',145),('2014-2015 Annual Report.pdf',133)]
for name,page in selected:
 t=PdfReader(ROOT/'Budget PDFs'/name).pages[page-1].extract_text()
 (H/(Path(name).stem+f'_context_p{page}.txt')).write_text(t)
# Read-only denominator and CPI reuse; no write or regeneration in Infrastructure Analysis.
demo=list(csv.DictReader((ROOT/'Infrastructure Analysis/research/demography/demography_cpi_2015_2024.csv').open()))
demo={int(r['calendar_year']):r for r in demo}
primary={(int(r['calendar_year']),r['metric']):r for r in rows if r['panel']=='primary_same_vintage_2013_2024'}
calculations=[]
for base in [2015,2018,2019]:
 end=2024
 B=float(primary[base,'average_weekly_earnings']['value']);E=float(primary[end,'average_weekly_earnings']['value'])
 D=float(demo[end]['cpi_chained_index_2015_100'])/float(demo[base]['cpi_chained_index_2015_100'])
 calculations.append(dict(baseline_calendar_year=base,endpoint_calendar_year=end,average_weekly_earnings_nominal_growth_pct=(E/B-1)*100,average_weekly_earnings_cpi_adjusted_growth_pct=(E/B/D-1)*100,unemployment_rate_change_percentage_points=float(primary[end,'unemployment_rate']['value'])-float(primary[base,'unemployment_rate']['value']),status='derived sensitivity from rounded official rows; not household living-standard index',caveat='Changing employment mix/hours and calendar CPI proxy; not median/aftertax income or causal policy effect'))
with (H/'derived_earnings_sensitivity.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=calculations[0]);w.writeheader();w.writerows(calculations)
print(f'Archived {len(rows)} source observations in two explicitly separate vintages; primary covers2013–2024. No2025 observations or invented poverty/affordability metrics.')
# Preserve the limited historical comparator separately; no post-2019 extension.
index_source=ROOT/'Budget PDFs/2014-2015 Annual Report.pdf'
index_text=PdfReader(index_source).pages[121].extract_text()
(H/'2014-2015_Annual_Report_economic_wellbeing_p122.txt').write_text(index_text)
assert 'Goal Five Indicators (unaudited)' in index_text
historical=[]
for year,ab,ca in zip(range(2009,2014),[.692,.744,.757,.758,.727],[.543,.556,.562,.569,.562]):
 for geography,value in [('Alberta',ab),('Canada',ca)]:
  assert str(value) in index_text
  historical.append(dict(calendar_year=year,geography=geography,index_value=value,index_name='Index of Economic Well-Being',unit='dimensionless composite index; not poverty rate',status='historical unaudited indicator published in official annual report',source_file='Budget PDFs/2014-2015 Annual Report.pdf',source_pdf_page=122,source_printed_page=116,definition_pdf_page=133,definition_printed_page=127,provider='Centre for the Study of Living Standards',exact_definition_quote='The rating indicates Alberta’s and Canada’s position on an indexed scale derived from weighting four variables of economic well-being: consumption, wealth, equality and security.',limitation='2009–2013 only; no UCP-period counterpart; no contemporary Canada comparison or poverty estimate'))
with (H/'historical_wellbeing_comparator.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=historical[0]);w.writeheader();w.writerows(historical)
