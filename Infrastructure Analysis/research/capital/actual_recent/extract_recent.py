from pathlib import Path
import re,csv,json,hashlib
R=Path(__file__).parent
files={'2022-23':'2022-2023 Budget.pdf','2023-24':'tbf-goa-2023-2024 Budget.pdf','2024-25':'2024-2025 Budget.pdf'}
rows=[]; manifest=[]
for vintage,file in files.items():
 pages=(R/(vintage+'.txt')).read_text().split('\f')
 for page,p in enumerate(pages,1):
  if 'BY ENVELOPE' not in p:continue
  lines=p[p.index('BY ENVELOPE'):].splitlines()[1:]
  for line in lines:
   m=re.match(r'^\s*(.*?)\s{2,}([\d,(\)\-]+)\s+([\d,(\)\-]+)\s+([\d,(\)\-]+)\s+([\d,(\)\-]+)\s+([\d,(\)\-]+)\s*$',line)
   if not m:continue
   label=m[1].strip()
   if 'Fully Consolidated' in label:label='Total Capital Plan - Fully Consolidated'
   if label=='investment':label='SUCH self-financed investment'
   if '(SUCH) Sector' in label:label='SUCH self-financed investment'
   vals=[int(x.replace(',','').replace('(','-').replace(')','')) if x!='-' else 0 for x in m.groups()[1:]]
   previous=f'{int(vintage[:4])-1}-{int(vintage[5:])-1:02}'
   for year,value,status in [(vintage,vals[1],'current_actual'),(previous,vals[2],'prior_actual')]:
    rows.append({'fiscal_year':year,'source_vintage':vintage,'envelope':label,'actual_cad_millions':value,'budget_cad_millions':vals[0] if status=='current_actual' else '', 'status':status,'pdf_page':page,'source_file':file})
   if 'Fully Consolidated' in label:break
  (R/(vintage+'_envelope_evidence.txt')).write_text(p)
 f=R.parents[3]/'Budget PDFs'/file
 manifest.append({'source_file':file,'title':f'{vintage} Final Results: Year-end Report','publication_month':f'June {int(vintage[:4])+1}','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source_url':None,'source_url_status':'not recovered; official Alberta report identity established from PDF cover/header; repository filename mislabeled Budget'})
with (R/'recent_envelopes_all_vintages.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
latest={}
for row in rows:
 key=(row['fiscal_year'],row['envelope']);latest[key]=row
with (R/'recent_envelopes_latest_comparative.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(latest.values())
(R/'source_manifest.json').write_text(json.dumps(manifest,indent=2))
print('rows',len(rows))
