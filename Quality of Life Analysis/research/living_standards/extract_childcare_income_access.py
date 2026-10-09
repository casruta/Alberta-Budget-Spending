#!/usr/bin/env python3
from pathlib import Path
from pypdf import PdfReader
import csv,json
H=Path(__file__).resolve().parent
man=json.loads((H/'curl_linked_report_download_manifest.json').read_text())
rows=[]
def add(file,page,period,metric,value,unit,status,quote,limit):
 r=PdfReader(H/file);t=r.pages[page-1].extract_text();(H/(file.removesuffix('.pdf')+f'_source_p{page}.txt')).write_text(t)
 assert str(value) in t or f'{value:,}' in t,(file,page,value)
 rows.append(dict(period=period,metric=metric,value=value,unit=unit,status=status,source_file=file,source_url=next(x['url'] for x in man if x.get('file')==file),source_pdf_page=page,source_printed_page=page-2,exact_source_quote=quote,interpretation_limit=limit))
s='scss-annual-report-2024-2025.pdf'
for period,v in zip(['2020-21','2021-22','2022-23','2023-24','2024-25'],[5.9,9.1,11.6,4.3,5.3]):
 add(s,36,period,'median_AISH_medical_adjudication_wait',v,'weeks','actual/prior-year result','This performance measure captures the median time between when an AISH application is ready for adjudication (all documents required to confirm general and medical eligibility have been received from the AISH applicant) and when the medical eligibility decision has been made.','Starts after complete documentation; not total initial application waiting time, client income adequacy or poverty.')
f='jet-annual-report-2024-2025.pdf'
for period,v in zip(['2020-21','2021-22','2022-23','2023-24','2024-25'],[4,6,8,9,10]):
 add(f,73,period,'all_licensed_childcare_spaces_growth',v,'percent year-over-year fiscal March count','actual/prior-year result','Percentage change in the number of licensed child care spaces','Includes out-of-school care as well as preschool/daycare/familyhomes; not same coverage as up-to-kindergarten-age count; maximumcapacity not actualattendance.')
add(f,65,'January2024','licensed_up_to_kindergarten_average_childcare_fee',15,'CAD per day','reported historical average fee','with further reductions to an average of $15 per day in January 2024','Source-reported average under CanadaAlbertaagreement; not allfamilies or household aftertax resources; cannot isolate provincial contribution.')
add(f,65,'April1,2025','fulltime_flat_parent_monthly_fee_announced',326.25,'CAD per month','announced future implementation after fiscal cutoff','In January 2025, Alberta’s government announced that as of April 1, 2025, it would implement a new flat monthly parent fee of $326.25 for full-time care','AfterMarch31,2025 evidencecutoff; exclude from2024-25actualresults.')
add(f,66,'March31,2025','licensed_childcare_spaces_up_to_kindergarten',142700,'licensed spaces','reported actual stock','As of March 31, 2025, 142,700 licensed child care spaces were available across the province for children up to kindergarten age','Capacitystock, not enrollment, staffedavailability or adequate supply relativetoeligiblechildren.')
add(f,66,'2024-25','net_new_licensed_spaces_up_to_kindergarten',14300,'net new licensed spaces','reported actual addition','In 2024-25, 14,300 net new licensed spaces were created, an increase of 11 per cent compared to 2023-24.','Same up-to-kindergarten coverage, differsfromalllicensedspace10%KPI; do not use planned8000spaces as additionalactuals.')
with (H/'childcare_income_access_2020_2025.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(f'Archived {len(rows)} access/capacity/fee observations with explicit one post-cutoff announced fee.')
