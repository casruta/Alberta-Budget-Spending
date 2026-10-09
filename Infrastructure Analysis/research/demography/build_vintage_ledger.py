#!/usr/bin/env python3
"""Archive cross-vintage local official population and annual CPI table rows."""
from pathlib import Path
import csv,re,json,hashlib,subprocess
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
# Fixed reviewed source scope: unrelated cached texts cannot add unnoticed vintages.
SOURCE_NAMES=[
 '2018-19 Budget.pdf', '2019-20 Budget.pdf', '2020-21 Budget.pdf',
 '2021-22 Budget.pdf', '2022-2023 Budget.pdf',
 'tbf-goa-2023-2024 Budget.pdf', '2024-2025 Budget.pdf',
]
(H/'raw_local').mkdir(exist_ok=True)
source_hashes={}
refreshed=[]
for name in SOURCE_NAMES:
 source=ROOT/'Budget PDFs'/name
 digest=hashlib.sha256(source.read_bytes()).hexdigest()
 result=subprocess.run(['pdftotext','-layout',str(source),'-'],check=True,
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 text=result.stdout
 assert 'Final Results' in text.split('\f',1)[0], name
 assert hashlib.sha256(source.read_bytes()).hexdigest()==digest, name
 target=H/'raw_local'/(source.stem+'.txt')
 target.write_text(text)
 source_hashes[str(source.relative_to(ROOT))]=digest
 refreshed.append(target)
rows=[]
for file in sorted(refreshed):
 for page_num,page in enumerate(file.read_text().split('\f'),1):
  lines=page.splitlines()
  pi=next((i for i,l in enumerate(lines) if l.strip().startswith('Population (July 1, thousands)')),None)
  if pi is None:continue
  years_candidates=[re.findall(r'\b20\d{2}\b',l) for l in lines[max(0,pi-40):pi] if len(re.findall(r'\b20\d{2}\b',l))>=8]
  assert years_candidates,(file,page_num)
  years=years_candidates[-1]
  pops=re.findall(r'\d[\d,]*',lines[pi].split('Population (July 1, thousands)',1)[1])
  cpi_lines=[l for l in lines if l.strip().startswith('Alberta consumer price index')]
  assert len(cpi_lines)==1,(file,page_num)
  cpi_tokens=re.findall(r'\(?-?\d+(?:\.\d+)?\)?',cpi_lines[0].split('Alberta consumer price index',1)[1])
  cpi=[-float(token[1:-1]) if token.startswith('(') else float(token) for token in cpi_tokens]
  assert len(years)==len(pops)==len(cpi),(file,page_num,years,pops,cpi)
  vintage=max(map(int,years))
  for y,p,c in zip(years,pops,cpi):
   rows.append(dict(source_file='Budget PDFs/'+file.stem+'.pdf',source_pdf_page=page_num,source_report_calendar_endpoint=vintage,calendar_year=int(y),population_july_1=int(p.replace(',',''))*1000,annual_alberta_cpi_growth_pct=float(c),population_precision='nearest thousand',cpi_precision='one decimal percentage point',series_type='calendar year CPI growth; July1 population',status='official local report table; demographic estimate; vintage-specific'))
with (H/'population_cpi_cross_vintage_ledger.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
# Audit same calendar years across vintages without mixing rows in primary analysis.
summary=[]
for year in range(2015,2025):
 obs=[r for r in rows if r['calendar_year']==year]
 if not obs:continue
 latest=max(obs,key=lambda x:x['source_report_calendar_endpoint'])
 p=[r['population_july_1'] for r in obs];c=[r['annual_alberta_cpi_growth_pct'] for r in obs]
 summary.append(dict(calendar_year=year,report_vintages=len(obs),population_min=min(p),population_max=max(p),population_range_persons=max(p)-min(p),latest_population=latest['population_july_1'],cpi_growth_min=min(c),cpi_growth_max=max(c)))
with (H/'cross_vintage_revision_summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=summary[0]);w.writeheader();w.writerows(summary)
(H/'vintage_ledger_source_hashes.json').write_text(json.dumps(source_hashes,indent=2)+'\n')
assert len(rows)==78 and len(source_hashes)==7
print(f'Refreshed {len(source_hashes)} reviewed PDFs and wrote {len(rows)} demographic/CPI rows; originals unchanged.')
