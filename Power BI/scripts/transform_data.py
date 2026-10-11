"""Transform repository evidence into chart-grain Power BI data without changing sources."""
from pathlib import Path
import ast, csv, hashlib, json, math, re
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Power BI/data'
ROWS, CHARTS, SOURCES = [], [], {}


def load(path):
    p=ROOT/path
    with p.open(encoding='utf-8-sig',newline='') as f:
        records=list(csv.DictReader(f))
    for i,r in enumerate(records,2):
        r['_path']=path;r['_row']=i
    SOURCES[path]=hashlib.sha256(p.read_bytes()).hexdigest()
    return records


def number(value):
    if value in ['',None]:return None
    result=float(value)
    if not math.isfinite(result):raise ValueError('Nonfinite evidence value')
    return result


def chart(key,title,original,note,section,classification='Reviewed'):
    item={'id':key,'title':title,'original_figure':original,'note':note,'section':section,
          'classification':classification,'panels':[]}
    CHARTS.append(item);return item


def panel(c,title,unit,kind='lineChart',minimum=0,maximum=None):
    item={'id':f"p{len(c['panels'])+1}",'title':title,'unit':unit,'visual_type':kind,
          'minimum':minimum,'maximum':maximum}
    c['panels'].append(item);return item


def add(c,p,period,series,value,sources,field,transform='identity',kind='Reported actual',status=''):
    value=number(value)
    if value is None:return
    if isinstance(sources,dict):sources=[sources]
    for r in sources:
        SOURCES[r['_path']]=hashlib.sha256((ROOT/r['_path']).read_bytes()).hexdigest()
    ROWS.append({'ChartId':c['id'],'Panel':p['id'],'Period':str(period),'Series':str(series),
                 'Value':value,'Unit':p['unit'],'ObservationKind':kind,'Status':status,
                 'SourcePaths':' | '.join(dict.fromkeys(r['_path'] for r in sources)),
                 'SourceRows':' | '.join(f"{r['_path']}:{r['_row']}" for r in sources),
                 'SourceFields':field,'Transformation':transform})


def meta(c,p,records,period,field,series):
    for r in records:add(c,p,r[period],series,r[field],r,field)


def build_reviewed():
    q='Quality of Life Analysis/';i='Infrastructure Analysis/'
    receipt=json.loads((ROOT/q/'data/figure_receipts.json').read_text())
    notes={x['id']:x['source'].replace('\n',' ') for x in receipt}
    def qc(stem,title,section):return chart('qol_'+stem,title,q+'figures/'+stem+'.png',notes[stem],section)
    functional=load(q+'data/functional_expense_intensity.csv')
    chosen=['Health','Basic and advanced education','Social services','Total programs']
    c=qc('01_spending_intensity','Spending growth and purchasing power','Spending')
    for field,title in [('nominal_million','Nominal expense, index 2018–19 = 100'),('cpi_adjusted_per_resident_2024_cad','Adjusted expense per resident, index 2018–19 = 100')]:
        p=panel(c,title,'Index, 2018–19 = 100',minimum=75)
        for name in chosen:
            base=next(r for r in functional if r['function']==name and r['calendar_year']=='2018')
            for r in functional:
                if r['function']==name:add(c,p,r['fiscal_year'],name,float(r[field])/float(base[field])*100,[r,base],field,'row / fixed 2018 baseline * 100')
    c=qc('02_allocation_change','Resource intensity by function, 2018–19 to 2024–25','Spending')
    p=panel(c,'CPI-adjusted expense per resident','Percent change','clusteredBarChart',-19,9)
    for r in load(q+'data/functional_expense_baseline_comparisons.csv'):
        if r['baseline_calendar_year']=='2018' and r['function'] in chosen:add(c,p,r['function'],'Change',r['cpi_adjusted_per_resident_growth_pct'],r,'cpi_adjusted_per_resident_growth_pct')
    economic=load(q+'data/economic_outcome_context.csv')
    c=qc('03_pay_and_unemployment','Earnings and unemployment','Living standards')
    p=panel(c,'Weekly earnings','CAD per week')
    for field,label in [('average_weekly_earnings','Nominal'),('weekly_earnings_cpi_adjusted_2024_cad','CPI-adjusted 2024 dollars')]:meta(c,p,economic,'calendar_year',field,label)
    p=panel(c,'Unemployment','Percent of labour force',maximum=13);meta(c,p,economic,'calendar_year','unemployment_rate','Unemployment')
    crime=load(q+'research/source_verification/safety_outcomes_2019_2023.csv')
    c=qc('04_safety','Police-reported crime, 2019–2023','Safety')
    for metric,title in [('violent_crime','Violent crime'),('property_crime','Property crime')]:
        p=panel(c,title,'Incidents per 100,000')
        for r in crime:
            if r['metric']==metric:add(c,p,r['calendar_year'],r['geography'],r['value'],r,'value',status=r['status'])
    education=load(q+'research/education_safety/current_education_observations.csv')
    for stem,title,metrics in [
        ('05_completion','Five-year high-school completion',{'five_year_high_school_completion':'All students','FNMI_five_year_high_school_completion':'Self-identified FNMI'}),
        ('06_grade9','Grade 9 acceptable-standard results',{'grade9_PAT_language_arts_acceptable_standard':'Language arts','grade9_PAT_mathematics_acceptable_standard':'Mathematics'})]:
        c=qc(stem,title,'Education');p=panel(c,'Reported results by school/cohort year','Percent',maximum=100)
        relevant=[r for r in education if r['metric'] in metrics]
        for r in relevant:
            if r['record_kind']=='result':add(c,p,r['observation_period'],metrics[r['metric']],r['value'],r,'value',status=r['status'])
        p=panel(c,'Latest results and matched targets','Percent','clusteredBarChart',maximum=100)
        for metric,label in metrics.items():
            targets=[r for r in relevant if r['metric']==metric and r['record_kind']=='target'];target=max(targets,key=lambda r:r['observation_period'])
            result=next(r for r in relevant if r['metric']==metric and r['record_kind']=='result' and r['observation_period']==target['observation_period'])
            add(c,p,label+' ('+target['observation_period']+')','Result',result['value'],result,'value')
            add(c,p,label+' ('+target['observation_period']+')','Target',target['value'],target,'value',kind='Target')
    mental=load(q+'research/source_verification/mental_health_access_2019_2023.csv')
    c=qc('07_mental_health','Mental-health and addiction service contact','Health')
    p=panel(c,'Eligible first ED visits without prior public-service contact','Percent',maximum=25);meta(c,p,mental,'fiscal_year','value','Result')
    p=panel(c,'Latest result and matched target','Percent','clusteredColumnChart',maximum=25)
    r=max(mental,key=lambda r:r['fiscal_year']);add(c,p,r['fiscal_year'],'Result',r['value'],r,'value');add(c,p,r['target_period'],'Target',r['target'],r,'target',kind='Target')
    health=[r for r in load(q+'research/health/extracted/health_outcomes.csv') if r['source_vintage']=='2024-25']
    c=qc('08_emergency_and_imaging','Emergency and imaging access','Health')
    p=panel(c,'ED initial physician assessment, 90th percentile','Hours',maximum=8)
    for r in health:
        if r['metric']=='ED initial physician assessment wait':add(c,p,r['period'],'16 largest sites',r['value'],r,'value',status=r['limitations'])
    p=panel(c,'Scans within clinical priority targets','Percent',maximum=100)
    for r in health:
        if r['metric']=='Diagnostic imaging within priority targets':add(c,p,r['period'],r['group'],r['value'],r,'value')
    c=qc('09_surgery_and_ems','Completed surgery and ambulance response','Health')
    for metric,title,unit,maximum in [('Elective surgery within national wait benchmark','Completed procedures within benchmarks','Percent',100),('EMS urgent-call response','Urgent ambulance response, 90th percentile','Minutes',75)]:
        p=panel(c,title,unit,maximum=maximum)
        for r in health:
            if r['metric']==metric:add(c,p,r['period'],r['group'],r['value'],r,'value',status=r['limitations'])
    social=load(q+'research/living_standards/current_social_outcomes_2021_2024.csv')
    c=qc('10_housing_support','Affordable housing and rent-support access','Housing')
    p=panel(c,'Combined units and additional supported households','Units + households','clusteredColumnChart',maximum=2700)
    relevant=[r for r in social if r['metric']=='new_affordable_housing_units_and_additional_rental_subsidies']
    for r in relevant:add(c,p,r['period'],'Result',r['value'],r,'value')
    target=next(r for r in social if r['metric']=='housing_combined_measure_target')
    add(c,p,target['period'],'Matched target',target['value'],target,'value',kind='Target')
    poverty=load(q+'research/living_standards/mbm_poverty_all_persons_2015_2024.csv')
    c=qc('11_poverty','Poverty: separate Market Basket Measure bases','Living standards')
    for base in ['Market basket measure, 2018 base','Market basket measure, 2023 base']:
        p=panel(c,base,'Percent of survey-covered persons',maximum=16)
        for r in poverty:
            if r['mbm_base']==base:add(c,p,r['calendar_year'],r['geography'],r['poverty_rate_pct'],r,'poverty_rate_pct',kind='Survey estimate',status=r['quality_flag']+'; '+r['comparability'])
    life=load(q+'research/health/life_tables/life_expectancy_age0_bothsexes.csv')
    c=qc('12_life_expectancy','Period life expectancy at birth','Health')
    c['note']=c['note'].replace('Shading: source 95% intervals (revision uncertainty excluded).2023–24 preliminary;', 'Source 95% bounds exclude revision uncertainty; calendar 2023 and 2024 preliminary;')
    c['note']+=' Native lines show the estimate and lower/upper source 95% bounds; not filled confidence bands.'
    for geo in ['Alberta','Canada']:
        p=panel(c,geo+': estimate and source 95% bounds','Years',minimum=79,maximum=83)
        for r in life:
            if r['GEO']!=geo or not 2015<=int(r['REF_DATE'])<=2024 or r['Element']!='Life expectancy (in years) at age x (ex)':continue
            margin=next(m for m in life if m['GEO']==geo and m['REF_DATE']==r['REF_DATE'] and m['Element']=='Margin of error of the life expectancy (m.e.(ex))')
            for label,delta in [('Estimate',0),('Lower 95%',-1),('Upper 95%',1)]:add(c,p,r['REF_DATE'],label,float(r['VALUE'])+delta*float(margin['VALUE']),[r,margin],'VALUE','estimate + sign * source margin',kind='Period life-table estimate',status='Preliminary' if int(r['REF_DATE'])>=2023 else 'Historical estimate')
    capital=load(i+'data/capital_population_analysis.csv')
    infra_note='2024–25 Final Results, PDF pp13–17. July population/calendar CPI proxies; accounting changes. Spending is not net service capacity.'
    def ic(stem,title):return chart('infra_'+stem,title,i+'plots/'+stem+'.png',infra_note,'Infrastructure')
    c=ic('01_actual_capital_spending','Actual Capital Plan spending');p=panel(c,'Actual capital spending','CAD billions','clusteredColumnChart')
    for r in capital:add(c,p,r['fiscal_year'],'Actual',float(r['capital_plan_actual_million'])/1000,r,'capital_plan_actual_million','CAD millions / 1000')
    c=ic('02_spending_per_resident','Capital spending per resident');p=panel(c,'Nominal and CPI-adjusted spending','CAD per resident')
    for field,label in [('capital_nominal_per_resident_cad','Nominal'),('capital_cpi_adjusted_per_resident_2024_cad','CPI-adjusted 2024 dollars')]:meta(c,p,capital,'fiscal_year',field,label)
    c=ic('03_growth_benchmarks','Capital, population and price-growth benchmark');p=panel(c,'Growth indices, 2018–19 = 100','Index, 2018–19 = 100',minimum=75)
    base=next(r for r in capital if r['calendar_year']=='2018')
    for r in capital:
        pop=float(r['population_july_1'])/float(base['population_july_1']);prices=float(r['cpi_index_2015_100'])/float(base['cpi_index_2015_100']);spend=float(r['capital_nominal_cad'])/float(base['capital_nominal_cad'])
        for label,value,field in [('Capital spending',spend,'capital_nominal_cad'),('Population',pop,'population_july_1'),('Population × CPI',pop*prices,'population_july_1; cpi_index_2015_100')]:add(c,p,r['fiscal_year'],label,value*100,[r,base],field,'row / fixed baseline; population-price product')
    c=ic('04_baseline_sensitivity','Capital spending under different baselines');p=panel(c,'Change to 2024–25','Percent change','clusteredBarChart',minimum=-30)
    for r in load(i+'data/baseline_comparisons.csv'):
        if r['baseline'] not in ['2015-16','2018-19','2019-20']:continue
        for field,label in [('nominal_capital_growth_pct','Nominal total'),('nominal_per_resident_growth_pct','Nominal per resident'),('cpi_adjusted_per_resident_growth_pct','CPI-adjusted per resident')]:add(c,p,r['baseline'],label,r[field],r,field)
    c=ic('05_latest_sector_changes','Latest capital-envelope changes');p=panel(c,'2023–24 to 2024–25, same classification','CAD millions','clusteredBarChart',minimum=-120)
    excluded=['Core Government Capital Plan','Fully Consolidated Capital Plan','Total','Total capital plan']
    for r in load(i+'research/capital/2024_25_envelope_audit.csv'):
        if 'total' in r['envelope'].lower() or r['envelope'] in excluded:continue
        add(c,p,r['envelope'],'Change',float(r['actual_million'])-float(r['prior_actual_million']),r,'actual_million; prior_actual_million','actual minus same-vintage prior actual')
    c=ic('06_tenure_sensitivity','Government-period spending intensity');c['note']+=' Unequal windows and inherited projects; descriptive, not causal.'
    p=panel(c,'Population-weighted annual adjusted spending','2024 CAD per resident','clusteredBarChart')
    for r in load(i+'data/tenure_summary.csv'):add(c,p,r['period'],'Adjusted annual intensity',r['population_weighted_cpi_adjusted_per_resident_annual_2024_cad'],r,'population_weighted_cpi_adjusted_per_resident_annual_2024_cad')
    c=ic('07_selected_project_stages','Selected project stages: recorded years');c['note']='Year of earlier documented work and first recovered report listing completed status. Not opening dates, continuous construction or net capacity.'
    p=panel(c,'Fiscal-start year first recorded','Fiscal-start year','clusteredBarChart',minimum=2014,maximum=2025)
    for r in load(i+'data/selected_project_stages.csv'):
        for field,label in [('earlier_year','Earlier work'),('reported_status_year','Completed-status report')]:add(c,p,r['project'],label,r[field],r,field)
    c=ic('08_hypothetical_price_sensitivity','Hypothetical construction-price sensitivity');c['classification']='Hypothetical scenario';c['note']='Hypothetical price-growth assumptions, not observed construction inflation. Spending inputs are actual; no construction-volume verdict.'
    p=panel(c,'Adjusted per-resident change versus assumed price growth','Percent change',minimum=-30,maximum=10)
    for r in load(i+'data/hypothetical_price_scenarios.csv'):add(c,p,f"{float(r['assumed_cumulative_price_growth_pct']):05.1f}",'Scenario',r['calculated_price_adjusted_spending_per_resident_growth_pct'],r,'calculated_price_adjusted_spending_per_resident_growth_pct','retained hypothetical scenario',kind='Hypothetical scenario')
    execution=load(i+'data/budget_execution_analysis.csv')
    c=ic('09_reported_budget_execution','Capital Plan budget and financial execution');c['note']+=' Contemporary paired columns can be restated; execution is not cancellation or procurement efficiency.'
    p=panel(c,'Contemporary paired budget and actual','CAD billions','clusteredColumnChart')
    for r in execution:
        for field,label in [('budget_million','Paired budget'),('contemporary_actual_million','Contemporary actual')]:add(c,p,r['fiscal_year'],label,float(r[field])/1000,r,field,'CAD millions / 1000',kind='Paired budget' if label=='Paired budget' else 'Reported actual')
    p=panel(c,'Actual as a share of paired budget','Percent');meta(c,p,execution,'fiscal_year','budget_execution_pct','Execution')


def literal_assignment(path,name,notebook=False):
    text=(ROOT/path).read_text()
    if notebook:text='\n'.join(''.join(c['source']) for c in json.loads(text)['cells'] if c['cell_type']=='code')
    for node in ast.walk(ast.parse(text)):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):return ast.literal_eval(node.value)
    raise KeyError(name)


def build_archive():
    folder='2011-2025 Expense Analysis/'
    notebook=folder+'Alberta_Expense_Analysis.ipynb'
    pop=literal_assignment(notebook,'POP',True);cpi=literal_assignment(notebook,'CPI',True)
    SOURCES[notebook]=hashlib.sha256((ROOT/notebook).read_bytes()).hexdigest()
    historical=load('Data/ministry_expenses.csv');wide=load('Data/ministry_expenses_wide.csv')
    categories=['Health','Education (K-12)','Advanced Education','Social Services','Other']
    note='Archive: original ministry mapping and notebook population/CPI inputs, not the reviewed functional series. Latest-year estimate/actual classification is unresolved in the old narrative.'
    def hc(stem,title):return chart('history_'+stem,title,folder+'plots/'+stem+'.png',note,'Archive expenses','Original archive')
    c=hc('expense_composition','Archive: operating-expense composition');p=panel(c,'Ministry operating expense','CAD billions','columnChart')
    for r in historical:add(c,p,r['fiscal_year'],r['ministry_normalized'],float(r['operating_expense_millions'])/1000,r,'operating_expense_millions','CAD millions / 1000',kind='Archive observation')
    p=panel(c,'Share of original operating expense','Percent','columnChart',maximum=100)
    for r in wide:
        for cat in categories:add(c,p,r['fiscal_year'],cat,float(r[cat])/float(r['total_operating'])*100,r,cat+'; total_operating','category / original operating total * 100',kind='Archive derived')
    c=hc('expense_percapita','Archive: operating expense per resident');p=panel(c,'Original notebook population denominator','CAD per resident')
    for r in wide:
        for cat in categories:add(c,p,r['fiscal_year'],cat,float(r[cat])*1e6/pop[r['fiscal_year']],r,cat+'; notebook POP','expense * 1e6 / original notebook population',kind='Archive derived')
    p=panel(c,'Selected original years, per-resident expense','CAD per resident','clusteredBarChart')
    for r in wide:
        if r['fiscal_year'] not in ['2011-12','2017-18','2024-25']:continue
        for cat in categories:add(c,p,cat,r['fiscal_year'],float(r[cat])*1e6/pop[r['fiscal_year']],r,cat+'; notebook POP','expense * 1e6 / original notebook population',kind='Archive derived')
    c=hc('expense_real_spending','Archive: nominal and adjusted operating expense');p=panel(c,'Total expense, original notebook deflator','CAD billions')
    for r in wide:
        for label,scale in [('Nominal',1),('CPI-adjusted 2024–25 dollars',cpi['2024-25']/cpi[r['fiscal_year']])]:add(c,p,r['fiscal_year'],label,float(r['total_operating'])*scale/1000,r,'total_operating; notebook CPI','original notebook deflator; CAD millions / 1000',kind='Archive derived')
    p=panel(c,'CPI-adjusted total operating expense per resident','2024 CAD per resident','clusteredColumnChart')
    for r in wide:add(c,p,r['fiscal_year'],'Adjusted per resident',float(r['total_operating'])*cpi['2024-25']/cpi[r['fiscal_year']]*1e6/pop[r['fiscal_year']],r,'total_operating; notebook CPI; notebook POP','total expense * original CPI deflator * 1e6 / original population',kind='Archive derived')
    c=hc('expense_health_deep_dive','Archive: health operating expense')
    p=panel(c,'Health expense','CAD billions')
    for r in wide:
        for label,scale in [('Nominal',1),('CPI-adjusted',cpi['2024-25']/cpi[r['fiscal_year']])]:add(c,p,r['fiscal_year'],label,float(r['Health'])*scale/1000,r,'Health; notebook CPI','original notebook deflator; CAD millions / 1000',kind='Archive derived')
    p=panel(c,'Health share of operating expense','Percent')
    for r in wide:add(c,p,r['fiscal_year'],'Health share',float(r['Health'])/float(r['total_operating'])*100,r,'Health; total_operating','Health / total operating * 100',kind='Archive derived')
    p=panel(c,'Original health expense per resident','CAD per resident')
    for r in wide:
        for label,scale in [('Nominal',1),('CPI-adjusted 2024 dollars',cpi['2024-25']/cpi[r['fiscal_year']])]:add(c,p,r['fiscal_year'],label,float(r['Health'])*scale*1e6/pop[r['fiscal_year']],r,'Health; notebook CPI; notebook POP','health expense * original CPI deflator * 1e6 / original population',kind='Archive derived')
    c=hc('expense_growth_indexed','Archive: indexed ministry expense');p=panel(c,'Nominal growth, 2011–12 = 100','Index, 2011–12 = 100',minimum=75)
    base=next(r for r in wide if r['fiscal_year']=='2011-12')
    for r in wide:
        for cat in categories:add(c,p,r['fiscal_year'],cat,float(r[cat])/float(base[cat])*100,[r,base],cat,'row / fixed 2011 baseline * 100',kind='Archive derived')
    c=hc('alberta_fiscal_summary_infographic','Archive: Alberta fiscal history, 2000–01 to 2024–25');c['note']='Archive fiscal history. Fiscal Plan basis through 2007–08; consolidated financial statements thereafter. Source vintages and accounting definitions differ.'
    fiscalhist=load('Data/alberta_surplus_deficit.csv')
    p=panel(c,'Revenue and expense','CAD billions','clusteredColumnChart')
    for r in fiscalhist:
        for field,label in [('total_revenue_millions','Revenue'),('total_expense_millions','Expense')]:add(c,p,r['fiscal_year'],label,float(r[field])/1000,r,field,'CAD millions / 1000',kind=r['reporting_basis'])
    for field,label,kind in [('surplus_deficit_millions','Surplus / deficit','clusteredColumnChart'),('resource_revenue_millions','Resource revenue','lineChart')]:
        p=panel(c,label,'CAD billions',kind,minimum=None)
        for r in fiscalhist:add(c,p,r['fiscal_year'],label,float(r[field])/1000,r,field,'CAD millions / 1000',kind=r['reporting_basis'])
    build_fiscal_plan()


def build_fiscal_plan():
    folder='2026-2029 Fiscal Plan/'
    fiscal=load('Data/fiscal_plan_2026_fiscal_summary.csv');ministry=load('Data/fiscal_plan_2026_ministry_expenses.csv');detail=load('Data/fiscal_plan_2026_revenue.csv');position=load('Data/fiscal_plan_2026_financial_position.csv')
    revenue=load(folder+'revenue_comparison.csv');expense=load(folder+'expense_comparison.csv');summary=load(folder+'revenue_vs_expense_summary.csv')
    cols=['2024-25 Actual','2025-26 Forecast','2026-27 Estimate','2027-28 Target','2028-29 Target']
    def get(records,field,value):return next(r for r in records if r[field]==value)
    def pc(stem,title):return chart('plan_'+stem,'Archive Fiscal Plan: '+title,folder+'plots/'+stem+'.png','Original Fiscal Plan inputs: 2024–25 actual; 2025–26 forecast; 2026–27 estimate; 2027–29 targets. Projections are not realized results; original policy comparisons were not re-audited.','Archive Fiscal Plan','Original projections')
    def kinds(col):return col.split(' ',1)[1]
    for stem,title in [('scissors_effect','revenue and expense paths'),('revenue_vs_expense_gap','revenue–expense gap')]:
        c=pc(stem,title);p=panel(c,'Revenue and total expense','CAD billions')
        for r in summary:
            col=next(k for k in cols if k.startswith(r['Fiscal_Year']))
            for field,label in [('Total_Revenue','Revenue'),('Total_Expense','Expense')]:add(c,p,r['Fiscal_Year'],label,float(r[field])/1000,r,field,'CAD millions / 1000',kind=kinds(col))
        if stem=='revenue_vs_expense_gap':
            p=panel(c,'Reported fiscal balance','CAD billions','clusteredColumnChart',minimum=None)
            for r in summary:add(c,p,r['Fiscal_Year'],'Surplus / deficit',float(r['Surplus_Deficit'])/1000,r,'Surplus_Deficit','CAD millions / 1000',kind=kinds(next(k for k in cols if k.startswith(r['Fiscal_Year']))))
    c=pc('fiscal_balance_waterfall','balance reconciliation');c['note']+=' Reported balances can differ from revenue minus expense by CAD 1M; rounding residuals are retained. Native bars separate revenue changes, negative expense changes and reported balances; totals are not added as increments.'
    p=panel(c,'Revenue and expense contributions versus prior year','CAD billions','clusteredColumnChart',minimum=None)
    for before,after in zip(summary,summary[1:]):
        for field,label,sign in [('Total_Revenue','Revenue change',1),('Total_Expense','Expense contribution',-1)]:add(c,p,after['Fiscal_Year'],label,(float(after[field])-float(before[field]))*sign/1000,[before,after],field,'signed current minus prior; CAD millions / 1000',kind='Plan change')
    p=panel(c,'Reported balances, separate from increments','CAD billions','clusteredColumnChart',minimum=None)
    for r in summary:add(c,p,r['Fiscal_Year'],'Surplus / deficit',float(r['Surplus_Deficit'])/1000,r,'Surplus_Deficit','CAD millions / 1000',kind='Actual / forecast / estimate / target by year')
    c=pc('revenue_composition','revenue composition');c['note']+=' Category sums exceed reported total revenue by CAD 1M in 2027–28 and 2028–29; source values are retained.';p=panel(c,'Category totals; no subtotal double counting','CAD billions','columnChart')
    catitems={'Tax revenue':['Total tax revenue'],'Resource revenue':['Total non-renewable resource revenue'],'Federal transfers':['Transfers from Government of Canada'],'Investment income':['Investment income'],'Other revenue':['Net income from govt. business enterprises','Premiums, fees and licences','Other']}
    for label,items in catitems.items():
        rr=[get(detail,'Item',item) for item in items]
        for col in cols:add(c,p,col[:7],label,sum(float(r[col]) for r in rr)/1000,rr,col,'sum mutually exclusive selected category rows / 1000',kind=kinds(col))
    c=pc('revenue_resource_risk','resource-revenue trajectory');c['note']+=' Reported totals differ from rounded component sums by CAD 1M in 2025–26 and 2028–29; source values are retained.';p=panel(c,'Resource revenue items','CAD billions')
    for r in revenue:
        if not any(t in r['Item'].lower() for t in ['bitumen','oil','gas','coal','non-renewable']):continue
        for col in cols:
            field=col.replace(' ','_');add(c,p,col[:7],r['Item'],float(r[field])/1000,r,field,'CAD millions / 1000',kind=kinds(col))
    r=get(detail,'Item','Total non-renewable resource revenue')
    for col in cols:add(c,p,col[:7],'Reported resource total',float(r[col])/1000,r,col,'CAD millions / 1000; total shown alongside its components, not stacked',kind=kinds(col))
    def revenue_category(item):
        t=item.lower()
        if 'itumen' in t or 'non-renewable' in t:return 'Resource revenue'
        if 'income tax' in t:return 'Income taxes'
        if 'tax' in t or 'levy' in t:return 'Other taxes and levies'
        if 'transfer' in t or 'canada' in t:return 'Federal transfers'
        if 'investment' in t or 'enterprise' in t:return 'Investment and enterprises'
        return 'Other revenue'
    c=pc('revenue_dependency_comparison','revenue dependencies');p=panel(c,'2024–25 actual and 2026–27 estimate','CAD billions','columnChart')
    groups=defaultdict(list)
    for r in revenue:groups[revenue_category(r['Item'])].append(r)
    for label,rr in groups.items():
        for col in ['2024-25 Actual','2026-27 Estimate']:
            field=col.replace(' ','_');add(c,p,col[:7],label,sum(float(r[field]) for r in rr)/1000,rr,field,'same original leaf-item categorization; sum / 1000',kind=kinds(col))
    c=pc('expense_ministry_ranking','ministry spending');p=panel(c,'Actual and estimate by ministry','CAD billions','clusteredBarChart')
    for r in expense:
        for col in ['2024-25 Actual','2026-27 Estimate']:
            field=col.replace(' ','_');add(c,p,r['Ministry'],col,float(r[field])/1000,r,field,'CAD millions / 1000',kind=kinds(col))
    c=pc('expense_changes_tornado','ministry expense changes');p=panel(c,'2026–27 estimate minus 2024–25 actual','CAD millions','clusteredBarChart',minimum=None)
    for r in expense:add(c,p,r['Ministry'],'Change',float(r['2026-27_Estimate'])-float(r['2024-25_Actual']),r,'2026-27_Estimate; 2024-25_Actual','estimate minus actual',kind='Plan comparison')
    category_map={'Health':['Hospital and Surgical Health Services','Primary and Preventative Health Services','Mental Health and Addiction'],'Education':['Education and Childcare','Advanced Education'],'Social services':['Assisted Living and Social Services','Children and Family Services'],'Infrastructure':['Transportation and Economic Corridors','Infrastructure','Municipal Affairs'],'Public safety':['Justice','Public Safety and Emergency Services']}
    def category(name):return next((cat for cat,names in category_map.items() if name in names),'Other')
    groups=defaultdict(list)
    for r in expense:groups[category(r['Ministry'])].append(r)
    c=pc('expense_composition_categories','expense by policy category');p=panel(c,'Share of selected ministry expense','Percent','columnChart',maximum=100)
    for col in cols:
        field=col.replace(' ','_');denom=sum(float(r[field]) for r in expense)
        for label,rr in groups.items():add(c,p,col[:7],label,sum(float(r[field]) for r in rr)/denom*100,expense,field,'category sum / all selected ministry expense * 100',kind=kinds(col))
    c=pc('expense_growth_vs_size','expense growth and ministry size')
    p=panel(c,'2026–27 estimate versus 2024–25 actual','Percent change','clusteredBarChart',minimum=None)
    for r in expense:
        base=float(r['2024-25_Actual'])
        if base:add(c,p,r['Ministry'],'Growth',(float(r['2026-27_Estimate'])/base-1)*100,r,'2026-27_Estimate; 2024-25_Actual','(estimate / actual - 1) * 100',kind='Plan comparison')
    p=panel(c,'2026–27 ministry size','CAD billions','clusteredBarChart')
    for r in expense:add(c,p,r['Ministry'],'Estimate',float(r['2026-27_Estimate'])/1000,r,'2026-27_Estimate','CAD millions / 1000',kind='Estimate')
    c=pc('health_spending_deep_dive','health ministry spending')
    health=[r for r in ministry if r['Ministry'] in category_map['Health']];total=get(ministry,'Ministry','Total program expense')
    p=panel(c,'Three ministry expense rows','CAD billions','clusteredColumnChart')
    for r in health:
        for col in cols:add(c,p,col[:7],r['Ministry'],float(r[col])/1000,r,col,'CAD millions / 1000',kind=kinds(col))
    p=panel(c,'Combined health share of program expense','Percent')
    for col in cols:add(c,p,col[:7],'Health share',sum(float(r[col]) for r in health)/float(total[col])*100,health+[total],col,'health rows / total program expense * 100',kind=kinds(col))
    c=pc('per_dollar_breakdown','expense per revenue dollar');c['note']+=' Values are cents per total revenue dollar, not shares summing to 100.'
    p=panel(c,'2026–27 estimate','Cents per revenue dollar','clusteredBarChart')
    revtotal=get(fiscal,'Item','Total revenue');denom=float(revtotal['2026-27 Estimate'])
    known=0;known_sources=[]
    for label,rr in groups.items():
        if label=='Other':continue
        amount=sum(float(r['2026-27_Estimate']) for r in rr);known+=amount;known_sources.extend(rr)
        add(c,p,label,'Expense',amount/denom*100,rr+[revtotal],'2026-27_Estimate; 2026-27 Estimate','category ministry expense / total revenue * 100',kind='Estimate')
    debt=[get(fiscal,'Item',item) for item in ['Taxpayer-supported debt servicing costs','Self-supported debt servicing costs']]
    amount=sum(float(r['2026-27 Estimate']) for r in debt);known+=amount;known_sources.extend(debt)
    add(c,p,'Debt servicing','Expense',amount/denom*100,debt+[revtotal],'2026-27 Estimate','combined debt servicing / total revenue * 100',kind='Estimate')
    total_expense=get(fiscal,'Item','Total expense')
    add(c,p,'Other government services and residual','Expense',(float(total_expense['2026-27 Estimate'])-known)/denom*100,[total_expense,revtotal]+known_sources,'2026-27 Estimate; 2026-27_Estimate','(total expense - named policy groups - debt servicing) / total revenue * 100',kind='Estimate')
    c=pc('cumulative_deficit','deficits and borrowing');p=panel(c,'Annual amounts','CAD billions','clusteredColumnChart')
    deficit=get(fiscal,'Item','Surplus / (deficit)');borrow=get(fiscal,'Item','Direct borrowing required')
    running_deficit=running_borrow=0;acc=[]
    for col in cols[1:]:
        dv=-float(deficit[col]);bv=float(borrow[col]);running_deficit+=dv;running_borrow+=bv
        add(c,p,col[:7],'Deficit',dv/1000,deficit,col,'negative fiscal balance / 1000',kind=kinds(col));add(c,p,col[:7],'Borrowing',bv/1000,borrow,col,'CAD millions / 1000',kind=kinds(col));acc.append((col,running_deficit,running_borrow))
    p=panel(c,'Cumulative amounts from 2025–26','CAD billions')
    for col,dv,bv in acc:
        add(c,p,col[:7],'Cumulative deficit',dv/1000,deficit,'; '.join(cols[1:cols.index(col)+1]),'cumulative negative balance / 1000',kind='Plan cumulative');add(c,p,col[:7],'Cumulative borrowing',bv/1000,borrow,'; '.join(cols[1:cols.index(col)+1]),'cumulative borrowing / 1000',kind='Plan cumulative')
    c=pc('debt_trajectory','debt and net assets');c['note']+=' Components differ from reported debt totals by CAD 1M in March 2026 and 2027; source values are retained. All amounts are consistently expressed in CAD billions, correcting the old graphic’s axis wording.'
    p=panel(c,'Taxpayer-supported debt components','CAD billions','columnChart')
    poscols=[k for k in position[0] if k.startswith('At March')]
    for item in ['Direct borrowing for the Capital Plan','P3s (Capital Plan)','Teachers Pension Plan debt','Direct borrowing for the Fiscal Plan']:
        r=get(position,'Item',item)
        for col in poscols:
            year=re.search(r'20\d\d',col).group();add(c,p,'March '+year,item,float(r[col])/1000,r,col,'CAD millions / 1000',kind=re.search(r'\((.*?)\)',col).group(1))
    p=panel(c,'Net assets','CAD billions','clusteredColumnChart',minimum=None)
    rr=[r for r in position if 'net assets' in r['Item'].lower()]
    if len(rr)!=1:raise ValueError('Expected one net asset row: '+str(rr))
    r=rr[0]
    for col in poscols:add(c,p,'March '+re.search(r'20\d\d',col).group(),'Net assets',float(r[col])/1000,r,col,'CAD millions / 1000',kind=re.search(r'\((.*?)\)',col).group(1))
    c=pc('debt_servicing_escalation','debt-servicing costs');p=panel(c,'Taxpayer and self-supported servicing','CAD billions','columnChart')
    rr=[get(fiscal,'Item',item) for item in ['Taxpayer-supported debt servicing costs','Self-supported debt servicing costs']]
    for r in rr:
        for col in cols:add(c,p,col[:7],r['Item'],float(r[col])/1000,r,col,'CAD millions / 1000',kind=kinds(col))
    p=panel(c,'Debt servicing share of total revenue','Percent')
    for col in cols:add(c,p,col[:7],'Debt servicing / revenue',sum(float(r[col]) for r in rr)/float(revtotal[col])*100,rr+[revtotal],col,'total debt servicing / total revenue * 100',kind=kinds(col))


def catalog_sources():
    catalog=[];tables=[]
    originals=[p for p in sorted(ROOT.rglob('*.csv')) if 'Power BI' not in p.relative_to(ROOT).parts and not any(x.startswith('.') for x in p.relative_to(ROOT).parts)]
    for i,p in enumerate(originals,1):
        path=p.relative_to(ROOT).as_posix()
        if '_MetaData.csv' in p.name:role='StatCan documentation; not a rectangular fact table'
        elif 'DRAFT_DO_NOT_USE' in p.name:role='Quarantined unverified draft; excluded from model'
        else:role='Original evidence table; kept separate from chart facts'
        with p.open(encoding='utf-8-sig',newline='') as f:raw=list(csv.reader(f))
        columns=raw[0];data=raw[1:]
        model_table=None
        if role.startswith('Original'):
            if any(len(r)!=len(columns) for r in data):raise ValueError('Ragged source CSV: '+path)
            model_table=f'Source{i:03d}';tables.append({'name':model_table,'path':path,'columns':columns,'rows':data})
        catalog.append({'SourceId':f'S{i:03d}','Path':path,'Rows':len(data),'Columns':len(columns),'Role':role,'ModelTable':model_table,'SHA256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return catalog,tables


def main():
    ROWS.clear();CHARTS.clear();SOURCES.clear()
    OUT.mkdir(exist_ok=True,parents=True)
    build_reviewed();build_archive()
    keys=[(r['ChartId'],r['Panel'],r['Period'],r['Series']) for r in ROWS]
    assert len(keys)==len(set(keys)), 'Duplicate chart grain'
    original=sorted(p.relative_to(ROOT).as_posix() for f in ['Quality of Life Analysis/figures','Infrastructure Analysis/plots','2011-2025 Expense Analysis/plots','2026-2029 Fiscal Plan/plots'] for p in (ROOT/f).glob('*.png'))
    assert sorted(c['original_figure'] for c in CHARTS)==original
    assert len(CHARTS)==42
    catalog,tables=catalog_sources()
    (OUT/'chart_data.json').write_text(json.dumps(ROWS,ensure_ascii=False,indent=2)+'\n')
    with (OUT/'chart_data.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(ROWS[0]),lineterminator='\n');w.writeheader();w.writerows(ROWS)
    (OUT/'chart_catalog.json').write_text(json.dumps(CHARTS,ensure_ascii=False,indent=2)+'\n')
    (OUT/'source_catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    (OUT/'source_tables.json').write_text(json.dumps(tables,ensure_ascii=False,separators=(',',':'))+'\n')
    (OUT/'transformation_manifest.json').write_text(json.dumps({'source_sha256':SOURCES,'charts':42,'chart_rows':len(ROWS),'source_csv_files':len(catalog),'imported_evidence_tables':len(tables),'excluded':[{k:r[k] for k in ['Path','Role']} for r in catalog if not r['ModelTable']],'fact_grain':['ChartId','Panel','Period','Series'],'missing_policy':'Missing inputs produce no point; never fill missing rates with zero.','status':'Transformed source-backed snapshot; native Power BI rendering not yet tested.'},indent=2)+'\n')
    print(f'Transformed {len(catalog)} source CSVs: {len(tables)} evidence tables, 42 charts, {len(ROWS)} native chart rows.')


if __name__=='__main__':main()
