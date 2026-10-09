#!/usr/bin/env python3
"""Re-extract inspectable health tables from archived and downloaded official PDFs.

Only stdlib and pdftotext are needed. Tables are deliberately source-specific:
publication vintage, date basis, definition, and missingness remain explicit.
Values transcribed from graphics are labeled; no later observations are imputed.
"""
from pathlib import Path
import csv, json, re, subprocess, hashlib
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
OUT=HERE/'extracted';OUT.mkdir(exist_ok=True)
rows=[];used={}
def page(source,n):
 p=REPO/source
 cached=OUT/(p.stem+'.txt')
 if not cached.exists():subprocess.run(['pdftotext','-layout',str(p),str(cached)],check=True)
 t=cached.read_text().split('\f')[n-1]
 used[(source,n)]=t
 return t

def emit(source,n,vintage,metric,group,unit,years,values,definition,limitations,targets=None,quote=None,primary=True,period='fiscal year',transcription='table numeric row',direction='higher is better'):
 t=page(source,n)
 assert len(years)==len(values)
 if targets is not None:assert len(targets)==len(years)
 for i,(year,value) in enumerate(zip(years,values)):
  rows.append(dict(metric=metric,group=group,period=year,period_type=period,value=value,unit=unit,target=None if targets is None else targets[i],preferred_direction=direction,source_vintage=vintage,primary_within_definition=primary,source_pdf=source,physical_pdf_page=n,source_sha256=hashlib.sha256((REPO/source).read_bytes()).hexdigest(),transcription=transcription,definition=definition,limitations=limitations,source_quote=quote or t))

def section_values(source,n,start,end,pattern,expected):
 t=page(source,n);a=t.index(start);z=t.index(end,a) if end else len(t)
 vals=[float(x) for x in re.findall(pattern,t[a:z])]
 assert vals==expected,(source,n,start,vals,expected)
 return vals

cur='Quality of Life Analysis/research/health/current/hlth-annual-report-2024-2025.pdf'
old='Quality of Life Analysis/research/health/current/health-2019-2020.pdf'
prev='Quality of Life Analysis/research/health/current/health-2023-2024.pdf'
y4=['2021-22','2022-23','2023-24','2024-25'];y5=['2020-21','2021-22','2022-23','2023-24','2024-25']
vals=section_values(cur,23,' ED wait times: 90th','Source:',r'(?<!\d)(\d+\.\d+)\*?', [4.5,6.2,6.7,7.0])
emit(cur,23,'2024-25','ED initial physician assessment wait','16 largest hospital sites','hours at 90th percentile',y4,vals,'Time from triage to initial physician assessment for included patients; 90th percentile, not mean or median.','2021-22 and2022-23 revised to exclude Left Without Being Seen; no connection to older median/17site/acuity-group metric. Current methodology appendix mistakenly includes an EMS paragraph; table and narrative plus2023-24 method support ED interpretation.',targets=[None,None,None,'below 2023-24 value (6.7h)'],direction='lower is better')
for group,start,end,v in [('Metro/urban',' Metro/urban',' Communities with',[14.6,17.5,13.8,14.2]),('Communities >3000 residents',' Communities with',' Rural communities',[18.6,18.9,16.3,16.4]),('Rural <3000 residents',' Rural communities',' Remote',[33.8,33.9,33.3,29.2]),('Remote',' Remote','Source:',[55.4,61.8,64.9,52.0])]:
 vals=section_values(cur,24,start,end,r'(?<!\d)(\d+\.\d+)',v)
 emit(cur,24,'2024-25','EMS urgent-call response',group,'minutes at 90th percentile',y4,vals,'Event-level 911 response interval for Delta/Echo life-threatening calls, grouped by geographic location.','Excludes interfacility transfers, other acuity categories, missing timestamps. Aggregate geography is not individual patient access or outcome.',targets=[None,None,None,'below 2023-24 result'],direction='lower is better')
for group,start,end,benchmark,v in [('Hip',' Hip replacement 1',' Knee replacement 2',182,[51.6,51.2,43.0,62.4,72.8]),('Knee',' Knee replacement 2',' Cataract surgery',182,[43.3,39.7,32.5,53.3,62.5]),('Cataract',' Cataract surgery','Source:',112,[45.3,64.7,64.7,59.7,62.8])]:
 vals=section_values(cur,26,start,end,r'(\d+(?:\.\d+)?)%',v)
 emit(cur,26,'2024-25','Elective surgery within national wait benchmark',group,'percent of completed valid RTT cases',y5,vals,f'Ready-to-treat to procedure within{benchmark}days. Emergency care and invalid RTT dates excluded; cataract first eye only; RTT excludes voluntary/patient delays.','Completed-case denominator excludes still-waiting patients; case mix and clearing old queues affect percentage. Primary current vintage2020-25; historical2019 vintage retained separately. No causal attribution.')
for group,start,end,v in [('MRI',' Percentage of MRI scans within',' Percentage of CT scans within',[68,49,42,41]),('CT',' Percentage of CT scans within','Source:',[87,80,80,80])]:
 vals=section_values(cur,30,start,end,r'(\d+(?:\.\d+)?)%',v)
 emit(cur,30,'2024-25','Diagnostic imaging within priority targets',group,'percent',y4,vals,'Priority-dependent thresholds; ED within24h; MRI inpatient24-72h and scheduled7/30/90days; CT inpatient24h and scheduled7/30/60days.','Changing urgency mix, demand, equipment and staffing limit interpretation; not a single wait threshold.')
vals=section_values(cur,42,' Percentage of patients with an','Source:',r'(\d+(?:\.\d+)?)%', [13.2,12.9,12.6,12.7,12.7])
emit(cur,42,'2024-25','Unplanned medical hospital readmission within30days','included medical acute-care discharges','percent',y5,vals,'Unplanned readmission within30days after a medical discharge.','Excludes surgery,pregnancy/childbirth,mental health,palliative care,cancer therapy. Not all hospital readmissions; depends on patient case mix and continuity of care.',direction='lower is better')
for group,start,end,v in [('Hip','      Hip replacement','      Knee replacement',[80.5,80.2,70.5,68.5,65.5]),('Knee','      Knee replacement','      Cataract surgery',[77.7,75.2,64.6,65.0,61.5]),('Cataract','      Cataract surgery',' Source:',[60.6,56.8,53.3,48.2,45.1])]:
 vals=section_values(old,30,start,end,r'(\d+(?:\.\d+)?)%',v)
 emit(old,30,'2019-20','Elective surgery within national wait benchmark',group,'percent of completed valid RTT cases',['2015-16','2016-17','2017-18','2018-19','2019-20'],vals,'Historical source uses national182day hip/knee and112day cataract benchmarks, excluding emergency procedures.','Historical2019-20 publication vintage; do not silently splice into2024-25 vintage.2019-20 endpoint values are reproduced by2023-24 report but full revisions across2015-19 not audited.',primary=False)
# Survey annual-result table extraction: explicit row order differs by report.
for source,n,vintage,fy,actual,target in [
('Budget PDFs/2011-2012 Budget.pdf',93,'2011-12','2011-12',62,65),
('Budget PDFs/2012-2013 Budget.pdf',118,'2012-13','2012-13',63,68),
('Budget PDFs/2013-2014 Annual Report.pdf',135,'2013-14','2013-14',66,65),
('Budget PDFs/2014-2015 Annual Report.pdf',119,'2014-15','2014-15',68,70)]:
 t=page(source,n);a=t.index('Satisfaction with Health Care Services Received');seg=t[a:t.index('Continuing Care',a)] if 'Continuing Care' in t[a:] else t[a:t.index('Healthy Alberta',a)]
 assert str(actual)+'%' in seg and str(target)+'%' in seg
 emit(source,n,vintage,'Satisfaction with health services personally received','eligible Alberta survey respondents','percent satisfied or very satisfied',[fy],[actual],'Telephone survey of personal health services received in prior year; excludes those without such experience.','Survey estimates and perception, with changing samples; not hospital outcomes or current quality.2014-15 question sample1361 and stated±2.5pp; no retrieved2015+ series.',targets=[target],quote=seg)
# Latest archived single-vintage graph; value-year pairing manually inspected.
source='Budget PDFs/2017 Budget.pdf';n=131;t=page(source,n)
for group,v in [('First Nations',[71.9,70.9,69.9,70.9,70.7]),('Non-First Nations',[82.1,82.2,82.2,82.3,82.2])]:
 assert all(str(x) in t for x in v)
 emit(source,n,'2017-18','Life expectancy at birth',group,'years',['2013','2014','2015','2016','2017'],v,'Period life-table based on age-sex-specific mortality; excludes specified non-AHCIP populations.','Small FirstNations numbers cause annual fluctuations; length oflife not quality; do not join differently revised2018-19 Health series.',period='calendar year',transcription='graph values transcribed and visually audited')
# Older population-wide life expectancy graph retained within one vintage.
source='Budget PDFs/2015-2016 Annual Report.pdf';n=103;t=page(source,n)
for group,v,primary in [('Provincial',[81.59,81.68,81.71,81.79,81.87],True),('First Nations',[70.79,72.15,72.52,71.60,70.36],False),('Non-First Nations',[82.00,82.02,82.07,82.19,82.30],False)]:
 assert all(f'{x:.2f}' in t for x in v)
 emit(source,n,'2015-16','Life expectancy at birth',group,'years',['2011','2012','2013','2014','2015'],v,'Period life table; graph presents provincial and FirstNations/nonFirstNations populations.','Older source vintage; group estimates overlap but differ from later2017/2018 publications. Never join vintages without reconciliation; not recent outcomes.',primary=primary,period='calendar year',transcription='graph values manually paired withyear; sourcepage saved')
# Archived perceived access differs from current operational waiting-time measures.
for source,n,vintage,fy,phys,ed,overall,targets in [
('Budget PDFs/2011-2012 Budget.pdf',93,'2011-12','2011-12',80,52,63,[83,65,73]),
('Budget PDFs/2012-2013 Budget.pdf',118,'2012-13','2012-13',79,65,70,[85,70,73])]:
 for metric,value,target in [('Perceived ease of physician access',phys,targets[0]),('Perceived ease of emergency department access',ed,targets[1]),('Public overall health system rating',overall,targets[2])]:
  emit(source,n,vintage,metric,'eligible Alberta survey respondents','percent',[fy],[value],'Survey perception: easy/veryeasy access among service users; overall system excellent/good rating across respondents.','Perceived access is not measured waittime.2011-12 results revised into fiscalperiods; sample/nonresponse and media/context can affect ratings. No current comparable series.',targets=[target])

# Later ministry publication retained as a distinct, unresolved source-vintage series.
source='Quality of Life Analysis/research/health/current/health-2018-2019.pdf';n=24;t=page(source,n)
for group,start,end,v in [('First Nations','  First Nations','  Non-First Nations',[68.7,69.9,69.1,67.7,67.9]),('Non-First Nations','  Non-First Nations','Sources:',[80.1,79.9,80.0,79.9,80.0])]:
 segment=t[t.index(start):t.index(end,t.index(start))]
 emit(source,n,'2018-19','Life expectancy at birth',group,'years',['2014','2015','2016','2017','2018'],v,'Ministry indicator uses AHCIP Adjusted Population and period life-table methodology.','2018 preliminary; large overlapping-year differences versus2017-18 whole-government graph remain unreconciled. Do not interpret between-vintage shifts as mortality changes.',primary=False,period='calendar year',quote=segment,transcription='table values; terminalfootnote1 stripped')
with (OUT/'health_outcomes.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(OUT/'health_outcomes.json').write_text(json.dumps(rows,indent=2))
(OUT/'source_pages.txt').write_text('\n\n'.join(f'SOURCE{source} PHYSICALPDFPAGE{n}\n{t}' for (source,n),t in used.items()))
print(f'Extracted{len(rows)}observations from{len(used)}source pages; no missing observations filled.')
