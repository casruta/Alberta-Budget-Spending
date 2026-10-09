#!/usr/bin/env python3
"""Independent direct-PDF economic-row verification; does not import extractor."""
import csv,re
from pathlib import Path
from pypdf import PdfReader
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
rows=list(csv.DictReader((H/'economic_indicators_source_ledger.csv').open()))
labels={'employment':'Employment (thousands)','employment_growth':'Employment growth','unemployment_rate':'Unemployment rate','average_weekly_earnings':'Average weekly earnings ($ / week)','primary_household_income_growth':'Primary household income','housing_starts':'Housing starts (number of units)'}
for name,page,start,end in [('2024-2025 Budget.pdf',13,2013,2024),('2022-2023 Budget.pdf',12,2011,2022)]:
 text=PdfReader(ROOT/'Budget PDFs'/name).pages[page-1].extract_text()
 for metric,label in labels.items():
  matches=[line for line in text.splitlines() if line.strip().startswith(label)];assert len(matches)==1
  suffix=matches[0].split(label,1)[1]
  if not re.search(r'\d',suffix):
   lines=text.splitlines();suffix+=' '+lines[lines.index(matches[0])+1]
  tokens=[token for token in suffix.split() if re.fullmatch(r'\(?-?\d[\d,]*(?:\.\d+)?\)?',token)]
  vals=[-float(t.strip('()').replace(',','')) if t.startswith('(') else float(t.replace(',','')) for t in tokens]
  assert len(vals)==end-start+1
  expected=dict(zip(range(start,end+1),vals))
  subset=[r for r in rows if r['source_file']=='Budget PDFs/'+name and r['metric']==metric]
  assert len(subset)==len(expected)
  for row in subset:
   y=int(row['calendar_year']);assert y<=end and float(row['value'])==expected[y]
   should_estimate=metric=='primary_household_income_growth' and y==end
   assert row['status'].startswith('estimate')==should_estimate
# Specific accounting-sign regression and latest-row sanity checks.
assert any(r['calendar_year']=='2016' and r['metric']=='primary_household_income_growth' and float(r['value'])==-10.9 for r in rows)
assert any(r['calendar_year']=='2024' and r['metric']=='unemployment_rate' and float(r['value'])==7.0 for r in rows)
print(f'Independent PDF reader verified{len(rows)} observations, negative-income regression, and2 explicitly flagged estimated income endpoints; no2025 rows.')
