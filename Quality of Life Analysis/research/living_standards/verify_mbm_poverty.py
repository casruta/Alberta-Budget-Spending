#!/usr/bin/env python3
"""Independent archive-reader regression checks; no extractor imports."""
from pathlib import Path
import csv,zipfile,io
H=Path(__file__).resolve().parent
clean=list(csv.DictReader((H/'mbm_poverty_all_persons_2015_2024.csv').open()))
expected={(r['mbm_base'],r['geography'],str(r['calendar_year'])):r for r in clean}
assert len(expected)==28
with zipfile.ZipFile(H/'11100135-eng.zip') as z:
 f=io.TextIOWrapper(z.open('11100135.csv'),encoding='utf-8-sig')
 reader=csv.reader(f);head=next(reader);idx={n:head.index(n) for n in head}
 matches=0
 for raw in reader:
  key=(raw[idx['Low income lines']],raw[idx['GEO']],raw[idx['REF_DATE']])
  if key not in expected or raw[idx['Persons in low income']]!='All persons' or raw[idx['Statistics']]!='Percentage of persons in low income':continue
  out=expected[key]
  for target,source in [('poverty_rate_pct','VALUE'),('quality_flag','STATUS'),('vector','VECTOR'),('coordinate','COORDINATE')]:assert out[target]==raw[idx[source]]
  assert raw[idx['UOM']]=='Percent';matches+=1
 assert matches==28
for geography in ['Alberta','Canada']:
 assert ('Market basket measure, 2018 base',geography,'2024') not in expected
 assert ('Market basket measure, 2023 base',geography,'2018') not in expected
 assert expected['Market basket measure, 2023 base',geography,'2024']['poverty_rate_pct']=='11.0'
assert expected['Market basket measure, 2018 base','Alberta','2019']['quality_flag']=='D'
print('Independent archive reader confirms28 values/flags/vectors; two bases unspliced; unavailable endpoint regressions passed.')

# Independently select exactly the requested dimensions with DictReader, preserving scalar/flags.
with zipfile.ZipFile(H/'11100135-eng.zip') as archive:
 reader=csv.DictReader(io.TextIOWrapper(archive.open('11100135.csv'),encoding='utf-8-sig'))
 chosen=[r for r in reader if r['GEO'] in ('Alberta','Canada') and r['Persons in low income']=='All persons' and r['Statistics']=='Percentage of persons in low income' and r['Low income lines'] in ('Market basket measure, 2018 base','Market basket measure, 2023 base')]
 assert len(chosen)==28
 assert all(r['UOM']=='Percent' and r['SCALAR_FACTOR']=='units' and r['SCALAR_ID']=='0' for r in chosen)
 assert len({r['VECTOR'] for r in chosen})==4
 for row in chosen:
  out=expected[row['Low income lines'],row['GEO'],row['REF_DATE']]
  assert row['VALUE']==out['poverty_rate_pct'] and row['STATUS']==out['quality_flag'] and row['VECTOR']==out['vector']
 assert {r['STATUS'] for r in chosen if r['Low income lines']=='Market basket measure, 2023 base' and r['GEO']=='Alberta'}=={'B','C'}
 text=archive.read('11100135_MetaData.csv').decode('utf-8-sig')
 assert 'B - Very good (CV between 2% and 4%)' in text
 assert 'C - Good (CV between 4% and 8%)' in text
 assert 'revised estimates from 2018 to 2023 based on population counts from the 2021 Census' in text
print('Second independent DictReader selector verifies geography/persons/statistic/base/scalar/units/vector/status and exact B/C CV definitions; no filled values.')
