"""Extract same-vintage historical rows from the supplied official final-results PDF.
Run with repository Python environment. Requires PyMuPDF. Writes only sibling CSV.
"""
from pathlib import Path
import csv
import re
import fitz
BASE = Path(__file__).resolve().parents[3]
SOURCE = BASE / 'Budget PDFs' / '2024-2025 Budget.pdf'
OUT = Path(__file__).parent

def values_between(text, label, end, count=12):
    fragment = text.split(label, 1)[1].split(end, 1)[0]
    tokens = [x.strip() for x in fragment.splitlines() if x.strip()]
    vals=[]
    for token in tokens:
        if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?',token):
            vals.append(float(token.replace(',','').replace('(','-').replace(')','')))
    assert len(vals) == count, (label,vals)
    return vals

def extract():
    doc=fitz.open(SOURCE)
    fiscal=doc[13].get_text()
    econ=doc[12].get_text()
    series={
      'capital_plan_actual_million': values_between(fiscal,'Capital Plan b','Statement of Financial Position'),
      'total_revenue_actual_million': values_between(fiscal,'10\nTotal Revenue','Expense by Function'),
      'total_expense_actual_million': values_between(fiscal,'18\nTotal Expense','19\nSurplus'),
      'net_capital_nonfinancial_assets_after_deferred_contributions_million': values_between(fiscal,'30\nCapital / non-fin. Assets','31\nNet Assets'),
      'population_july1_thousands': values_between(econ,'Population (July 1, thousands)','Population growth'),
      'alberta_cpi_annual_pct': values_between(econ,'Alberta consumer price index','Population (July 1, thousands)'),
    }
    with (OUT/'latest_vintage_actual_series.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['fiscal_year','calendar_year']+list(series)+['status','source_file','fiscal_pdf_page','economic_pdf_page'])
        writer.writeheader()
        for i,y in enumerate(range(2013,2025)):
            writer.writerow(dict(fiscal_year=f'{y}-{str(y+1)[-2:]}',calendar_year=y,
                **{k:v[i] for k,v in series.items()},status='actual',source_file='Budget PDFs/2024-2025 Budget.pdf',fiscal_pdf_page=14,economic_pdf_page=13))
    return series
if __name__ == '__main__':
    print(extract())
