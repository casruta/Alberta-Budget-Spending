#!/usr/bin/env python3
"""Exact official MBM rows, distinct bases, quality flags and revision metadata."""
from pathlib import Path
import csv,zipfile,io,json,hashlib,datetime,re
H=Path(__file__).resolve().parent
P=H/'11100135-eng.zip'
URL='https://www150.statcan.gc.ca/n1/tbl/csv/11100135-eng.zip'
z=zipfile.ZipFile(P)
assert z.testzip() is None
assert set(z.namelist())=={'11100135.csv','11100135_MetaData.csv'}
meta=z.read('11100135_MetaData.csv').decode('utf-8-sig')
(H/'11100135_MetaData.csv').write_text(meta)
assert 'Low income statistics by age, gender and economic family type' in meta
assert 'With the release of the 2024 CIS data, Statistics Canada revised estimates from 2018 to 2023 based on population counts from the 2021 Census.' in meta
rows=[]
for r in csv.DictReader(io.TextIOWrapper(z.open('11100135.csv'),encoding='utf-8-sig')):
 if r['GEO'] in ['Alberta','Canada'] and r['Persons in low income']=='All persons' and r['Low income lines'] in ['Market basket measure, 2018 base','Market basket measure, 2023 base'] and r['Statistics']=='Percentage of persons in low income':
  assert r['UOM']=='Percent' and r['SCALAR_FACTOR']=='units' and r['VALUE']!=''
  assert r['STATUS'] in {'A','B','C','D','E','F',''}
  rows.append(r)
assert len(rows)==28
rows.sort(key=lambda r:(r['Low income lines'],r['GEO'],r['REF_DATE']))
with (H/'mbm_poverty_all_persons_exact_source_rows.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
flags={'A':'Excellent: CV0–2%','B':'Very good: CV2–4%','C':'Good: CV4–8%','D':'Acceptable: CV8–16%','E':'Use with caution: CV16–33.3%','F':'Too unreliable to publish'}
clean=[]
for r in rows:
 clean.append(dict(calendar_year=int(r['REF_DATE']),geography=r['GEO'],mbm_base=r['Low income lines'],persons='All persons',poverty_rate_pct=r['VALUE'],quality_flag=r['STATUS'],quality_definition=flags[r['STATUS']],vector=r['VECTOR'],coordinate=r['COORDINATE'],source_table='11-10-0135-01',source_url=URL,source_status='historical survey estimate; latest downloaded vintage',income_survey='Canadian Income Survey',comparability='Keep MBM bases separate;2018–2023 estimates revised to2021Census; methodology changes2021/2022; no causal attribution or significance test'))
with (H/'mbm_poverty_all_persons_2015_2024.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=clean[0]);w.writeheader();w.writerows(clean)
coverage={base:sorted({r['REF_DATE'] for r in rows if r['Low income lines']==base}) for base in ['Market basket measure, 2018 base','Market basket measure, 2023 base']}
assert coverage['Market basket measure, 2018 base']==[str(y) for y in range(2015,2024)]
assert coverage['Market basket measure, 2023 base']==[str(y) for y in range(2020,2025)]
look={(r['Low income lines'],r['GEO'],int(r['REF_DATE'])):r for r in rows}
assert look['Market basket measure, 2023 base','Alberta',2024]['VALUE']=='11.0'
assert look['Market basket measure, 2023 base','Canada',2024]['VALUE']=='11.0'
assert ('Market basket measure, 2018 base','Alberta',2024) not in look
info={'download_url':URL,'http_status':200,'client':'curl -L --fail; normal proxy and verified TLS','local_zip_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'metadata_sha256':hashlib.sha256(z.read('11100135_MetaData.csv')).hexdigest(),'extraction_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'title':'Low income statistics by age, gender and economic family type','table':'11-10-0135-01','persons':'All persons','statistics':'Percentage of persons in low income','bases_and_year_coverage':coverage,'rows':len(rows),'forecast_rows':0,'splicing':'none;2024 2018base absent;2023base prior2020 absent','revision_note_22':'With the release of the 2024 CIS data, Statistics Canada revised estimates from 2018 to 2023 based on population counts from the 2021 Census.','sampling_caution':'Quality flags are not standard errors or a significance test; do not infer difference significance.'}
page_file=H/'1110013501_table_page.html'
if page_file.exists():
 html=page_file.read_text()
 released=re.search(r'Release date:\s*(\d{4}-\d{2}-\d{2})',html)
 published=re.search(r'\"datePublished\":\s*\"(\d{4}-\d{2}-\d{2})\"',html)
 assert released and published and released[1]==published[1]
 info['table_release_date']=released[1]
 info['release_date_source']='Official table HTML Release date and JSON-LD datePublished, not ZIP metadata'
 info['table_page_sha256']=hashlib.sha256(page_file.read_bytes()).hexdigest()
 info['survey_coverage_exclusions']='Not specified in ZIP table footnotes; linked survey5200 HTTPS metadata returned403; no reserve coverage assertion'
(H/'mbm_poverty_provenance.json').write_text(json.dumps(info,indent=2)+'\n')
print('Archived28 exact official MBM poverty rows, distinct2018/2023 bases, complete availableyear ranges andqualityflags; no interpolation.')
