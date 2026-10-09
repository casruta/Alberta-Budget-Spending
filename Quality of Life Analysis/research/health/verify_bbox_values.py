#!/usr/bin/env python3
"""Independent coordinate-based audit of all48current Health table values.

Uses pdftotext bbox output and word positions rather than layout-line sections.
The table row coordinates were inspected independently; labels, years, units,
and targets are reviewed in health_source_audit.md.
"""
from pathlib import Path
import csv,json,re,subprocess,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
pdf=HERE/'current/hlth-annual-report-2024-2025.pdf'
bbox=pdf.with_name(pdf.stem+'_bbox.html')
if not bbox.exists():subprocess.run(['pdftotext','-bbox-layout',str(pdf),str(bbox)],check=True)
ns={'x':'http://www.w3.org/1999/xhtml'}
pages=ET.parse(bbox).getroot().findall('.//x:page',ns)
records=list(csv.DictReader((HERE/'extracted/health_outcomes.csv').open()))
specs=[
(23,569.92,'ED initial physician assessment wait','16 largest hospital sites'),
(24,554.80,'EMS urgent-call response','Metro/urban'),
(24,585.76,'EMS urgent-call response','Communities >3000 residents'),
(24,622.72,'EMS urgent-call response','Rural <3000 residents'),
(24,659.76,'EMS urgent-call response','Remote'),
(26,397.55,'Elective surgery within national wait benchmark','Hip'),
(26,434.51,'Elective surgery within national wait benchmark','Knee'),
(26,471.47,'Elective surgery within national wait benchmark','Cataract'),
(30,155.92,'Diagnostic imaging within priority targets','MRI'),
(30,217.00,'Diagnostic imaging within priority targets','CT'),
(42,434.08,'Unplanned medical hospital readmission within30days','included medical acute-care discharges')]
checks=[]
for n,y,metric,group in specs:
 cells=[]
 for w in pages[n-1].findall('.//x:word',ns):
  text=w.text or ''
  if abs(float(w.attrib['yMin'])-y)<=1.3 and float(w.attrib['xMin'])>180 and re.fullmatch(r'\d+(?:\.\d+)?[%*]?',text):
   cells.append((float(w.attrib['xMin']),float(text.rstrip('%*'))))
 got=[v for x,v in sorted(cells)]
 selected=sorted((r for r in records if r['metric']==metric and r['group']==group and r['source_vintage']=='2024-25'),key=lambda r:r['period'])
 expected=[float(r['value']) for r in selected]
 assert got==expected,(metric,group,got,expected)
 checks.append(dict(metric=metric,group=group,physical_pdf_page=n,coordinate_values=got,checked_count=len(got),passed=True))
(HERE/'extracted/bbox_verification.json').write_text(json.dumps(checks,indent=2))
print('PASS:',sum(x['checked_count'] for x in checks),'values;',len(checks),'table rows independently verified by word coordinates.')
