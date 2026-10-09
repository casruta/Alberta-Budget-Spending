#!/usr/bin/env python3
"""Independent PDF verifier: does not import extraction or main analysis modules."""
import csv,json,re,hashlib
from pathlib import Path
from pypdf import PdfReader
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
ledger=list(csv.DictReader((H/'population_cpi_cross_vintage_ledger.csv').open()))
groups={}
for row in ledger:groups.setdefault((row['source_file'],int(row['source_pdf_page'])),[]).append(row)
evidence=[]
for (relative,page),rows in groups.items():
 source=ROOT/relative
 reader=PdfReader(source)
 cover=reader.pages[0].extract_text()
 assert 'Final Results' in cover and re.search(r'Year[-– ]?end Report',cover,re.I),relative
 fiscal=re.search(r'(20\d{2})\s*[-–]\s*(\d{2})\s+Final Results',cover)
 assert fiscal,(relative,cover[:300])
 start=int(fiscal[1]);end=start+1
 text=reader.pages[page-1].extract_text()
 lines=text.splitlines()
 poplines=[l for l in lines if l.strip().startswith('Population (July 1, thousands)')]
 cpilines=[l for l in lines if l.strip().startswith('Alberta consumer price index')]
 assert len(poplines)==len(cpilines)==1,(relative,page)
 ps=re.findall(r'\d[\d,]*',poplines[0].split('Population (July 1, thousands)',1)[1])
 cpi_tail=cpilines[0].split('Alberta consumer price index',1)[1]
 cs=[]
 for token in cpi_tail.split():
  # Independent token-based parsing preserves accounting parentheses and minus signs.
  cs.append(-float(token.strip('()')) if token.startswith('(') else float(token))
 candidates=[re.findall(r'\b20\d{2}\b',l) for l in lines if len(re.findall(r'\b20\d{2}\b',l))>=8]
 assert len(candidates)==1,(relative,candidates)
 ys=list(map(int,candidates[0]))
 assert len(ys)==len(ps)==len(cs)==len(rows)
 assert ys==list(range(min(ys),max(ys)+1))
 assert max(ys)==start and max(ys)<end # completed calendar years; no future calendar forecasts
 expected={y:(int(p.replace(',',''))*1000,float(c)) for y,p,c in zip(ys,ps,cs)}
 assert len({int(r['calendar_year']) for r in rows})==len(rows)
 for row in rows:
  y=int(row['calendar_year']);assert y<=start
  assert int(row['source_report_calendar_endpoint'])==start
  assert expected[y]==(int(row['population_july_1']),float(row['annual_alberta_cpi_growth_pct']))
  assert row['status']=='official local report table; demographic estimate; vintage-specific'
 # Scope estimate footnotes: population/CPI rows do not carry superscript a.
 assert not re.search(r'Population \(July 1, thousands\)\s+a\b',poplines[0])
 assert not re.search(r'Alberta consumer price index\s+a\b',cpilines[0])
 evidence.append(dict(source_file=relative,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_pdf_page=page,report_fiscal_year=f'{start}-{str(end)[-2:]}',calendar_year_start=min(ys),calendar_year_end=max(ys),rows_verified=len(rows),source_population_definition='Population (July 1, thousands)',source_cpi_definition='Alberta consumer price index; calendar year percentage change',footnote_scope='Population and CPI rows unmarked; a-estimate footnote not blanket forecast status',historical_exclusion_check='All calendar years no later than fiscal starting year; report cover verified Final Results',census_base_metadata='not supplied in table',population_estimate_type='preliminary/updated/intercensal classification not supplied',official_cpi_base_level='not supplied; row is percentage change, not index level'))
regression=[r for r in ledger if r['source_file']=='Budget PDFs/2018-19 Budget.pdf' and int(r['calendar_year'])==2009]
assert len(regression)==1 and float(regression[0]['annual_alberta_cpi_growth_pct'])==-0.1
assert any(float(r['annual_alberta_cpi_growth_pct'])<0 for r in ledger)
(H/'independent_source_verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(f'Independent pypdf review verified {len(ledger)} source rows from {len(evidence)} Final Results reports. No future calendar forecast included.')
