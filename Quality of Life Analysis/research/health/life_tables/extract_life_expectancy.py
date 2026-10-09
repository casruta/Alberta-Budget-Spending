"""Extract official single-year age-zero life expectancy, preserving source status."""
from pathlib import Path
import csv,hashlib,json,datetime,zipfile,io
B=Path(__file__).resolve().parent
source=B/'13100837-eng.zip'
selected=[]
csv_hasher=hashlib.sha256()
with zipfile.ZipFile(source) as archive:
 with archive.open('13100837.csv') as raw:
  for chunk in iter(lambda: raw.read(1024*1024), b''):
   csv_hasher.update(chunk)
 with archive.open('13100837.csv') as raw, io.TextIOWrapper(raw,encoding='utf-8-sig',newline='') as f:
  rows=csv.DictReader(f)
  for r in rows:
   if r['GEO'] in ('Alberta','Canada') and r['Age group']=='0 years' and r['Sex']=='Both sexes' and r['Element'] in ('Life expectancy (in years) at age x (ex)','Margin of error of the life expectancy (m.e.(ex))'):
    selected.append(r)
assert len(selected)==180
assert len({(r['REF_DATE'],r['GEO'],r['Element']) for r in selected})==180
with (B/'life_expectancy_age0_bothsexes.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=selected[0].keys());w.writeheader();w.writerows(selected)
(B/'life_expectancy_age0_bothsexes.json').write_text(json.dumps(selected,indent=2)+'\n')
manifest=json.loads((B/'download_manifest.json').read_text()) if (B/'download_manifest.json').exists() else {'downloads':[]}
manifest['extraction_verified_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest['selection_rows']=len(selected)
manifest['downloads']=[r for r in manifest['downloads'] if r['file'] not in ('table.html','13100837-eng.zip')]
for fn,url in [('table.html','https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310083701'),('13100837-eng.zip','https://www150.statcan.gc.ca/n1/tbl/csv/13100837-eng.zip')]:
 p=B/fn;manifest['downloads'].append({'file':fn,'url':url,'curl_fail_on_http_error':True,'download_succeeded':True,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest['csv_sha256']=csv_hasher.hexdigest()
(B/'download_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for r in selected:
 if int(r['REF_DATE'])>=2014 and 'Life expectancy (in years)' in r['Element']: print(r['REF_DATE'],r['GEO'],r['VALUE'],r['STATUS'])

metadata_status=[{'calendar_year':year,'table_status':'preliminary' if year in (2023,2024) else 'not flagged preliminary in inspected note','source':'13100837_MetaData.csv, Note3','raw_selected_status_preserved':True} for year in range(1980,2025)]
(B/'metadata_period_status.json').write_text(json.dumps(metadata_status,indent=2)+'\n')
