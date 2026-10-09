"""Independently compare rendered official HTML data with downloaded CSV values."""
from pathlib import Path
import csv,json
B=Path(__file__).resolve().parent
r=list(csv.DictReader((B/'life_expectancy_age0_bothsexes.csv').open()))
checks=[]
for fn,geo in [('table.html','Canada'),('alberta_table.html','Alberta')]:
 s=(B/fn).read_text(); start=s.index('prepareTable(')+len('prepareTable('); obj,end=json.JSONDecoder().raw_decode(s[start:])
 columns=obj['headers']['columnHeaders']
 assert columns[0]['values'][0]['value']==geo
 assert columns[1]['values'][0]['value']=='Both sexes'
 assert columns[2]['values'][0]['value']=='Life expectancy (in years) at age x (ex)'
 years=[v['value'] for v in columns[3]['values']]
 row=next(x for x in obj['rows'] if x['values'][0]['value']=='0 years')
 for year,v in zip(years,row['values'][1:]):
  csvrow=next(x for x in r if x['REF_DATE']==year and x['GEO']==geo and x['Element'].startswith('Life expectancy (in years)'))
  ok=float(v['value'])==float(csvrow['VALUE']);assert ok
  checks.append({'year':year,'geography':geo,'html_value':v['value'],'csv_value':csvrow['VALUE'],'pass':ok})
(B/'html_verification.json').write_text(json.dumps(checks,indent=2)+'\n')
print(len(checks),'official HTML-to-CSV values passed')
