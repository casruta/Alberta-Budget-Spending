"""Extract original-vintage budget execution and capital composition from official PDFs.

Preserves original reporting, including separately reported Climate Leadership Plan
capital grants/investment in 2017-18. No inference of physical capacity or cancellation.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import fitz
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCES=[
 ('2015-16','2015-2016 Annual Report.pdf',10),
 ('2016-17','2016-2017 Budget.pdf',12),
 ('2017-18','2017 Budget.pdf',12),
 ('2018-19','2018-19 Budget.pdf',3),
 ('2019-20','2019-20 Budget.pdf',3),
 ('2020-21','2020-21 Budget.pdf',3),
 ('2021-22','2021-22 Budget.pdf',3),
 ('2022-23','2022-2023 Budget.pdf',3),
 ('2023-24','tbf-goa-2023-2024 Budget.pdf',3),
 ('2024-25','2024-2025 Budget.pdf',3),
]

def row(block,label):
    # Source extraction is line oriented. Full label avoids matching regular grant
    # row in separate Climate Leadership Plan row.
    match=re.search(r'^\d+\s+'+re.escape(label)+r'\s*$',block,re.M)
    if match is None: return None
    vals=[]
    for item in block[match.end():].splitlines():
        item=item.strip()
        if not item:continue
        if not re.fullmatch(r'(?:-|\(?[\d,]+\)?)',item):break
        # A dash within this present five-cell accounting row denotes nil.
        # Absent rows/observations stay None and never become imputed zeros.
        vals.append(0 if item=='-' else int(item.replace(',','').replace('(','-').replace(')','')))
    if len(vals)!=5:raise ValueError((label,vals))
    return vals

def write_csv(name,rows):
    with (HERE/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    latest={r['fiscal_year']:float(r['capital_plan_actual_million']) for r in csv.DictReader((HERE/'latest_vintage_actual_series.csv').open())}
    panel=[];components=[];manifest=[]
    for year,name,page in SOURCES:
        path=ROOT/'Budget PDFs'/name
        doc=fitz.open(path);text=doc[page-1].get_text();block=text.split('CAPITAL PLAN',1)[1]
        (HERE/(name+f'.composition_summary_page{page}.txt')).write_text(text)
        total=row(block,'Total Capital Plan')
        if total is None:raise ValueError('Missing total '+name)
        component_rows={label:row(block,label) for label in ['Capital grants','Capital investment','Climate Leadership Plan capital grants','Climate Leadership Plan capital investment']}
        amounts={}
        for i,status in enumerate(['budget','actual','prior_actual']):
            grants=sum(values[i] for label,values in component_rows.items() if values is not None and label.endswith('grants'))
            investment=sum(values[i] for label,values in component_rows.items() if values is not None and label.endswith('investment'))
            residual=total[i]-grants-investment
            if abs(residual)>1:raise ValueError(('Component reconciliation',year,status,residual))
            amounts[status]=(grants,investment)
            observation_year=int(year.split('-')[0])-(1 if status=='prior_actual' else 0)
            observation_fy=f'{observation_year}-{str(observation_year+1)[-2:]}'
            components.append(dict(fiscal_year=year,observation_fiscal_year=observation_fy,column_status=status,total_capital_plan_million=total[i],capital_grants_million=grants,capital_investment_million=investment,component_rounding_residual_million=residual,grant_share_pct=grants/total[i]*100,investment_share_pct=investment/total[i]*100,source_file='Budget PDFs/'+name,pdf_page=page,source_vintage=year))
        panel.append(dict(fiscal_year=year,budget_million=total[0],contemporary_actual_million=total[1],budget_execution_pct=total[1]/total[0]*100,actual_minus_budget_million=total[1]-total[0],source_reported_budget_difference_million=total[3],budget_difference_rounding_residual_million=total[3]-(total[1]-total[0]),latest_2024_25_vintage_actual_million=latest[year],latest_minus_contemporary_actual_million=latest[year]-total[1],contemporary_grants_actual_million=amounts['actual'][0],contemporary_investment_actual_million=amounts['actual'][1],source_file='Budget PDFs/'+name,pdf_page=page,source_vintage=year))
        manifest.append(dict(fiscal_year=year,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),pdf_page=page,pdf_title=doc.metadata['title'],pdf_author=doc.metadata['author']))
    write_csv('budget_execution_original_vintage.csv',panel)
    write_csv('capital_composition_original_vintages.csv',components)
    (HERE/'execution_composition_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    original={r['fiscal_year']:r for r in components if r['column_status']=='actual'}
    revisions=[]
    for r in components:
        if r['column_status']!='prior_actual':continue
        year=int(r['fiscal_year'].split('-')[0])-1
        fy=f'{year}-{str(year+1)[-2:]}'
        if fy not in original:continue
        old=original[fy]
        revisions.append(dict(fiscal_year_revised=fy,next_source_vintage=r['fiscal_year'],
            original_total_million=old['total_capital_plan_million'],
            next_comparative_total_million=r['total_capital_plan_million'],
            total_revision_million=r['total_capital_plan_million']-old['total_capital_plan_million'],
            original_grants_million=old['capital_grants_million'],
            next_grants_million=r['capital_grants_million'],
            grant_revision_million=r['capital_grants_million']-old['capital_grants_million'],
            original_investment_million=old['capital_investment_million'],
            next_investment_million=r['capital_investment_million'],
            investment_revision_million=r['capital_investment_million']-old['capital_investment_million'],
            source_file=r['source_file'],pdf_page=r['pdf_page']))
    write_csv('adjacent_vintage_revision_ledger.csv',revisions)
    print(json.dumps(panel,indent=2))
if __name__=='__main__':main()
