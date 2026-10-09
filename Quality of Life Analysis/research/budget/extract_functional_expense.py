"""Extract official latest-vintage functional expenses and paired 2024 comparisons.

No protected repository files are modified. Inputs: supplied Final Results PDF.
Output fiscal years2015-16..2024-25; all amounts CAD millions. Requires PyMuPDF.
"""
from pathlib import Path
import csv,hashlib,json,re
import fitz
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'Budget PDFs/2024-2025 Budget.pdf'

def parse_numbers(fragment,count):
    tokens=[s.strip() for s in fragment.splitlines() if s.strip()]
    vals=[]
    for token in tokens:
        if re.fullmatch(r'(?:-|\(?[\d,]+(?:\.\d+)?\)?)',token):
            # A nil dash in a present accounting cell is not an absent observation.
            vals.append(0 if token=='-' else float(token.replace(',','').replace('(','-').replace(')','')))
            if len(vals)==count:break
        elif vals:break
    if len(vals)!=count:raise ValueError((count,vals))
    return vals

def historical_row(text,label,next_label):
    return parse_numbers(text.split(label,1)[1].split(next_label,1)[0],12)

def accounting_row(text,label):
    match=re.search(r'^\d+(?:\s*\n|\s+)'+re.escape(label)+r'\s*$',text,re.M)
    if match is None:raise ValueError('Missing accounting label:'+label)
    return parse_numbers(text[match.end():],5)

def write_csv(name,rows):
    with (HERE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    doc=fitz.open(SOURCE);history=doc[13].get_text();economic=doc[12].get_text()
    definitions=[
      ('health_expense_million','11\nHealth','12\nBasic / advanced education'),
      ('basic_advanced_education_expense_million','12\nBasic / advanced education','13\nSocial services'),
      ('social_services_expense_million','13\nSocial services','14\nOther program expense'),
      ('other_program_expense_million','14\nOther program expense','15\nTotal program expense'),
      ('total_program_expense_million','15\nTotal program expense','16\nDebt servicing costs'),
      ('debt_servicing_expense_million','16\nDebt servicing costs','17\nPension provisions / recovery'),
      ('pension_provisions_recovery_million','17\nPension provisions / recovery','18\nTotal Expense'),
      ('total_expense_million','18\nTotal Expense','19\nSurplus / (Deficit)'),
    ]
    series={key:historical_row(history,start,end) for key,start,end in definitions}
    series['population_july_1_thousands']=historical_row(economic,'Population (July 1, thousands)','Population growth')
    series['alberta_calendar_annual_cpi_growth_pct']=historical_row(economic,'Alberta consumer price index','Population (July 1, thousands)')
    rows=[]
    for i,y in enumerate(range(2013,2025)):
        r=dict(fiscal_year=f'{y}-{str(y+1)[-2:]}',calendar_year=y,**{k:v[i] for k,v in series.items()})
        r['program_component_rounding_residual_million']=r['total_program_expense_million']-sum(r[k] for k in ['health_expense_million','basic_advanced_education_expense_million','social_services_expense_million','other_program_expense_million'])
        r['total_component_rounding_residual_million']=r['total_expense_million']-r['total_program_expense_million']-r['debt_servicing_expense_million']-r['pension_provisions_recovery_million']
        # Preserve source inconsistencies; do not silently repair published values.
        r['program_reconciliation_status']='source anomaly; exceeds ordinary rounding' if abs(r['program_component_rounding_residual_million'])>2 else 'within ordinary integer rounding'
        r['total_reconciliation_status']='source anomaly; investigate' if abs(r['total_component_rounding_residual_million'])>2 else 'within ordinary integer rounding'
        r.update(status='actual',source_vintage='2024-25 Final Results',source_file=str(SOURCE.relative_to(ROOT)),expense_pdf_page=14,economic_pdf_page=13,measure_scope='Consolidated expense by function; not operating-only and not capital investment')
        if y>=2015:rows.append(r)
    write_csv('latest_vintage_functional_expenses_2015_2024.csv',rows)
    summary=doc[2].get_text().split('Expense\n',1)[1].split('CAPITAL PLAN',1)[0]
    labels=['Operating expense','Capital grants','Disaster and emergency assistance','Capital amort. / inventory consump. / asset disposal losses','Debt servicing costs - general','Debt servicing costs - Capital Plan','Pension recovery','Contingency','Total Expense']
    snapshot=[]
    for label in labels:
        v=accounting_row(summary,label)
        snapshot.append(dict(source_reporting_fiscal_year='2024-25',category=label,budget_2024_25_million=v[0],actual_2024_25_million=v[1],actual_2023_24_million=v[2],source_reported_budget_change_million=v[3],source_reported_prior_change_million=v[4],source_file=str(SOURCE.relative_to(ROOT)),pdf_page=3,scope='Expense by accounting type; not expense by function; source-paired budget comparison'))
    write_csv('expense_accounting_components_2024_budget_actual.csv',snapshot)
    ministry_text=doc[6].get_text().split('Operating Expense by Ministry',1)[1].split('Capital Grants',1)[0]
    ministry=[]
    for m in re.finditer(r'^([1-9]|1\d|2[0-6])\n([A-Za-z][^\n]+)\n',ministry_text,re.M):
        label=m[2].strip();v=parse_numbers(ministry_text[m.end():],5)
        ministry.append(dict(source_reporting_fiscal_year='2024-25',ministry=label,budget_2024_25_million=v[0],actual_2024_25_million=v[1],actual_2023_24_million=v[2],source_reported_budget_change_million=v[3],source_reported_prior_change_million=v[4],source_file=str(SOURCE.relative_to(ROOT)),pdf_page=7,scope='Operating expense by ministry; not total functional expense'))
    if len(ministry)!=26:raise ValueError(('Ministry count',len(ministry)))
    write_csv('ministry_operating_expense_2024_budget_actual.csv',ministry)
    checks={}
    for col in ['budget_2024_25_million','actual_2024_25_million','actual_2023_24_million']:
        checks[col]=sum(r[col] for r in ministry)-snapshot[0][col]
        if abs(checks[col])>3:raise ValueError(('Ministry rounding',col,checks[col]))
    manifest=dict(source_file=str(SOURCE.relative_to(ROOT)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),source_pdf_metadata=doc.metadata,source_reconciliation_anomalies=[{'fiscal_year':r['fiscal_year'],'program_component_residual_million':r['program_component_rounding_residual_million']} for r in rows if abs(r['program_component_rounding_residual_million'])>2],source_landing_url='https://www.alberta.ca/government-and-ministry-annual-reports',original_online_pdf_url='Unverified; local supplied source used',fiscal_actual_cutoff='2025-03-31',financial_historical_page=14,economic_page=13,accounting_snapshot_page=3,ministry_snapshot_page=7,functional_observations=len(rows),ministry_sum_rounding_residuals=checks)
    (HERE/'functional_expense_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for page in [3,6,7,8,13,14]:
        (HERE/f'2024_25_final_results_original_pdf_page{page}.txt').write_text(doc[page-1].get_text())
    print(json.dumps({'functional_rows':len(rows),'ministry_rows':len(ministry),'rounding_checks':checks,'latest_functional':rows[-1]},indent=2))
if __name__=='__main__':main()
