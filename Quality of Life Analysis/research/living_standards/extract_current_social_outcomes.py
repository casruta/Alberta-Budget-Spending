#!/usr/bin/env python3
"""Source-reviewed current SCSS outcome extraction; no population-wide substitutes."""
from pathlib import Path
from pypdf import PdfReader
import csv,json,hashlib
H=Path(__file__).resolve().parent
P=H/'scss-annual-report-2024-2025.pdf';r=PdfReader(P)
manifest=json.loads((H/'curl_linked_report_download_manifest.json').read_text())
u=next(x['url'] for x in manifest if x.get('file')==P.name)
for page in [38,49,67]:
 (H/f'scss_source_p{page}.txt').write_text(r.pages[page-1].extract_text())
housing=r.pages[37].extract_text();jobs=r.pages[48].extract_text();definition=r.pages[66].extract_text()
assert all(str(x) in housing for x in ['2,243','2,325','2,302','798','641','388','1,661','410','1,500'])
assert 'comparable' in housing and '2021-22' in housing
assert all(str(x)+'%' in jobs for x in [61,66,75,68,65,67])
assert 'occupancy permit' in definition and 'regenerated' in definition
rows=[]
def add(period,metric,value,unit,page,quote,limit,status='reported actual / prior-year result'):
 rows.append(dict(period=period,metric=metric,value=value,unit=unit,status=status,source_file=P.name,source_url=u,source_pdf_page=page,source_printed_page=page-2,exact_source_quote=quote,interpretation_limit=limit))
for period,value in [('2021-22',2243),('2022-23',2325),('2023-24',2302),('2024-25',798)]:
 add(period,'new_affordable_housing_units_and_additional_rental_subsidies',value,'mixed units plus additional supported households',38,'This measure reports on the number of new affordable housing units and new rental subsidies the ministry has funded or supported for Albertans in need within a fiscal year.','Mixed delivery/access measure, not net physical housing stock or population core-housing-need rate; comparable results unavailable before2021-22; definitions include regenerated completed units.')
add('2024-25','housing_combined_measure_target',1500,'mixed units plus additional supported households',38,'2024-25 Target','Target, not observed delivery',status='target')
for period,units,households in [('2023-24',641,1661),('2024-25',388,410)]:
 add(period,'newly_built_units_breakdown',units,'housing units',38,'Newly built units','Published breakdown label; do not conflate with combined measure or infer net stock/removals.')
 add(period,'additional_households_supported_rent_supplement',households,'additional supported households',38,'Additional households supported though Rent Supplements','Incremental program household count; not completed housing units or population housing adequacy.')
for year,value in zip(range(2020,2025),[61,66,75,68,67]):
 add(str(year),'former_CEIS_clients_employed_three_months_after_services',value,'percent of former surveyed service clients',49,'This performance measure captures the proportion (per cent) of former CEIS clients who found employment within three months after completing one of the following CEIS services: Exposure Course, Job Placement, Workshop, and Disability Related Employment Supports (DRES).','Selected service-client survey; not provincial employment rate or causal program effect; excludes nonsurveyed service types.')
with (H/'current_social_outcomes_2021_2024.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
assert 388+410==798 and 641+1661==2302
# Preserve the conflicting unemployment contextual quote separately; never overwrite primary official series.
conflict=dict(source_pdf_page=49,source_printed_page=47,source_quote='Alberta’s unemployment rate increased from an average of 5.8 per cent in 2023 to 7.1 per cent in 2024',comparison='2024-25 Final Results p13 reports5.9% in2023 and7.0% in2024',handling='Retain primary final-results economic table; archive conflict, no averaging or selective substitution',source_url=u)
(H/'unemployment_source_conflict.json').write_text(json.dumps(conflict,indent=2)+'\n')
print(f'Archived {len(rows)} current social outcome/target rows; housing breakdowns reconcile; source conflict flagged.')
