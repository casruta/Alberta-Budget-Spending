"""Independent pdfplumber + Decimal verification, separate from PyMuPDF extractor."""
from pathlib import Path
from decimal import Decimal,getcontext
import csv,json,re
import pdfplumber
getcontext().prec=32
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCES=[('2022-23','2022-2023 Budget.pdf',13,2008),('2023-24','tbf-goa-2023-2024 Budget.pdf',14,2009),('2024-25','2024-2025 Budget.pdf',14,2013)]
FIELDS={11:'health_expense_million',12:'basic_advanced_education_expense_million',13:'social_services_expense_million',14:'other_program_expense_million',15:'total_program_expense_million',16:'debt_servicing_expense_million',17:'pension_provisions_recovery_million',18:'total_expense_million'}

def numbers(fragment):
    # pdfplumber preserves extra space inside source formatted numeric spans.
    # Join only separated leading digit + comma-group and one + two digits.
    cleaned=re.sub(r'\b(\d)\s+(\d,\d{3})\b',r'\1\2',fragment)
    cleaned=re.sub(r'(?<=\d)\s+,',',',cleaned)
    cleaned=re.sub(r'\b(\d)\s+(\d{2})\b',r'\1\2',cleaned)
    cleaned=re.sub(r'\b(\d)\s+(\d)\b',r'\1\2',cleaned)
    cleaned=re.sub(r'\(\s+','(',cleaned)
    tokens=re.findall(r'\(?\d[\d,]*(?:\.\d+)?\)?',cleaned)
    return [Decimal(t.replace(',','').replace('(','-').replace(')','')) for t in tokens]

def function_rows(text,expected):
    out={}
    for line in text.splitlines():
        m=re.match(r'^(1[1-8]) (.*)$',line)
        if not m:continue
        number=int(m[1]); label,value_text=re.split(r' (?=\(?\d)',m[2],maxsplit=1)
        values=numbers(value_text)
        if len(values)!=expected:raise ValueError((number,label,len(values),values))
        out[FIELDS[number]]=values
    if len(out)!=8:raise ValueError(('Functional rows',len(out)))
    return out

def main():
    vintages=[];latest=None
    for vintage,name,page,start in SOURCES:
        with pdfplumber.open(ROOT/'Budget PDFs'/name) as doc:
            text=doc.pages[page-1].extract_text()
            series=function_rows(text,int(vintage.split('-')[0])-start+1)
            i=2022-start
            row={'source_vintage':vintage,'observation_fiscal_year':'2022-23','source_file':name,'pdf_page':page,**{k:str(v[i]) for k,v in series.items()}}
            row['program_sum_minus_reported_total_million']=str(sum(series[FIELDS[k]][i] for k in [11,12,13,14])-series[FIELDS[15]][i])
            vintages.append(row)
            if vintage=='2024-25':
                latest=series
                econ=doc.pages[12].extract_text()
                popline=next(l for l in econ.splitlines() if l.startswith('Population (July 1, thousands)'))
                cpiline=next(l for l in econ.splitlines() if l.startswith('Alberta consumer price index'))
                population=numbers(popline.split('Population (July 1, thousands)',1)[1])
                cpi=[Decimal(x) for x in re.findall(r'\d+\.\d+',cpiline.split('Alberta consumer price index',1)[1])]
                assert len(population)==12 and len(cpi)==12
    with pdfplumber.open(ROOT/'Budget PDFs/2024-2025 Budget.pdf') as doc:
        text=doc.pages[6].extract_text().split('Operating Expense by Ministry',1)[1].split('Capital Grants',1)[0]
        ministry_values=[]
        total=None
        for line in text.splitlines():
            m=re.match(r'^(\d+)\s*([A-Za-z].*)$',line)
            if not m:continue
            number=int(m[1])
            if number>27:continue
            label,fragment=re.split(r' (?=\(?\d)',m[2],maxsplit=1)
            values=numbers(fragment)[:3]
            if number==27:total=values
            else:ministry_values.append(values)
        assert len(ministry_values)==26 and total is not None
        ministry_residuals=[str(sum(v[i] for v in ministry_values)-total[i]) for i in range(3)]
    primary={int(r['calendar_year']):r for r in csv.DictReader((HERE/'latest_vintage_functional_expenses_2015_2024.csv').open())}
    for y,r in primary.items():
        assert population[y-2013]==Decimal(r['population_july_1_thousands'])
        assert cpi[y-2013]==Decimal(r['alberta_calendar_annual_cpi_growth_pct'])
        for field,values in latest.items():
            if Decimal(r[field])!=values[y-2013]:raise ValueError(('Parser mismatch',y,field))
    results=[]
    for base in [2015,2018,2019]:
        b=base-2013;e=11
        inflation=Decimal(1)
        for rate in cpi[b+1:e+1]:inflation*=Decimal(1)+rate/100
        popratio=population[e]/population[b]
        for field,values in latest.items():
            if field=='pension_provisions_recovery_million':continue
            ratio=values[e]/values[b]
            results.append({'baseline':f'{base}-{str(base+1)[-2:]}','endpoint':'2024-25','metric':field,'nominal_total_growth_pct':str((ratio-1)*100),'population_growth_pct':str((popratio-1)*100),'cpi_growth_pct':str((inflation-1)*100),'cpi_adjusted_per_resident_growth_pct':str((ratio/popratio/inflation-1)*100),'calculation':'Independent pdfplumber source extraction + Decimal; allocation intensity, not outcome'})
    for name,rows in [('functional_cross_vintage_2022_independent.csv',vintages),('functional_baseline_sensitivity_independent.csv',results)]:
        with (HERE/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (HERE/'independent_functional_verification.json').write_text(json.dumps({'financial_parser_agreement':'All80current functional cells match PyMuPDF extraction','cross_vintage_2022':vintages,'decimal_comparison_rows':len(results),'independent_ministry_sum_minus_reported_total_budget_current_prior_million':ministry_residuals,'population_thousands':[str(x) for x in population],'cpi_annual_rates':[str(x) for x in cpi]},indent=2)+'\n')
    print(json.dumps({'vintages':vintages,'comparison_rows':len(results)},indent=2))
if __name__=='__main__':main()
