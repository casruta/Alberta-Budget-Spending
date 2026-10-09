"""Inventory local source coverage without treating absence as nonexistence."""
from pathlib import Path
import csv
import hashlib
import json
import re
from urllib.parse import quote
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/source_verification'
FULL_NAMES={
    '2011-2012 Budget.pdf','2012-2013 Budget.pdf','2013-2014 Annual Report.pdf',
    '2014-2015 Annual Report.pdf','2015-2016 Annual Report.pdf',
    '2016-2017 Budget.pdf','2017 Budget.pdf',
}


def build():
    rows=[]
    for path in sorted((ROOT.parent/'Budget PDFs').glob('*.pdf')):
        with fitz.open(path) as pdf:
            rows.append({'source_file':str(path.relative_to(ROOT.parent)),
                'pdf_pages':len(pdf),'pdf_title_metadata':pdf.metadata.get('title',''),
                'pdf_author_metadata':pdf.metadata.get('author',''),
                'source_form':'Full annual-report volume' if path.name in FULL_NAMES else 'Abbreviated final-results year-end report',
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'coverage_limit':'Page count/form do not establish absence of metrics in other publications; references to schedules outside this file do not make them available here.'})
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'corpus_inventory.csv').open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    (OUT/'corpus_inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
    text=['# Local official-source coverage inventory','',
        f'The repository contains **{len(rows)} PDFs with {sum(r["pdf_pages"] for r in rows):,} physical pages**. '
        'These files do not form a uniform series of complete annual-report volumes. '
        'Earlier full volumes include performance and detailed statement sections absent from the supplied later summaries. '
        'The analysis uses verified pages appropriate to each claim, rather than assuming that similarly named files contain comparable sections.','',
        '| Repository source | Physical pages | Source form | Internal PDF title |',
        '|---|---:|---|---|']
    for r in rows:
        name=Path(r['source_file']).name
        link='../../../Budget%20PDFs/'+quote(name)
        title=r['pdf_title_metadata'].replace('|','/')
        text.append(f'| [{name}]({link}) | {r["pdf_pages"]} | {r["source_form"]} | {title} |')
    text += ['', '## What this changes about inference', '',
        '- Recent filenames containing “Budget” identify final-results documents internally; proposed budgets and annual actuals must still be distinguished by the table columns.',
        '- A measure recovered from an older performance appendix has no automatic comparable observation in a later short summary. Its absence here does not mean the indicator was discontinued or its value stayed unchanged.',
        '- For example, the supplied 2019–20 year-end report has only 20 pages yet references detailed statement schedules outside this file. Those references are source targets, not locally recovered evidence for the unexplained 2018–19 investment revision.',
        '- The primary financial and population tables remain reproducible from the 2024–25 report. Wider physical/condition coverage requires additional departmental, institutional and municipal records.',
        '- Full-volume versus summary classification is a reviewed description of these local files, not an automated semantic conclusion from page count alone.', '',
        'Source checksums are in the CSV/JSON. All original repository PDFs are unchanged.']
    (OUT/'CORPUS_INVENTORY.md').write_text('\n'.join(text)+'\n')
    print(f'Inventoried {len(rows)} PDF files / {sum(r["pdf_pages"] for r in rows)} physical pages.')


if __name__=='__main__':build()
