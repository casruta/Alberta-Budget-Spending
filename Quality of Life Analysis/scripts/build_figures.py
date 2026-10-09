"""Standalone notebook-oriented figures from reviewed source rows; no synthetic score."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from render_report import polish

ROOT = Path(__file__).resolve().parents[1]
COLORS = ['#176B87', '#9A3B3B', '#4C7F52', '#B57B18', '#76568D']
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11, 'axes.spines.top':False,
                     'axes.spines.right':False, 'axes.titleweight':'bold', 'figure.facecolor':'white',
                     'axes.prop_cycle':plt.cycler(color=COLORS)})
RECEIPTS = []


def save(fig, name, alt, source):
    source=polish(source)
    fig.subplots_adjust(bottom=.27, top=.86, left=.1, right=.95)
    fig.text(.1, .025, source, fontsize=9, color='#444444', va='bottom', wrap=True)
    for label in fig.findobj(matplotlib.text.Text):
        label.set_text(polish(label.get_text()))
    fig.savefig(ROOT/'figures'/f'{name}.png', dpi=170, bbox_inches='tight')
    fig.savefig(ROOT/'figures'/f'{name}.svg', bbox_inches='tight')
    plt.close(fig)
    RECEIPTS.append(dict(id=name, png=f'figures/{name}.png', svg=f'figures/{name}.svg',
                         alt=alt, source=source))


def build():
    (ROOT/'figures').mkdir(exist_ok=True)
    panel = pd.read_csv(ROOT/'data/functional_expense_intensity.csv')
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), sharey=True)
    selected = ['Health', 'Basic and advanced education', 'Social services', 'Total programs']
    for name, color in zip(selected, COLORS):
        rows = panel[panel.function == name].sort_values('calendar_year')
        for ax, field in zip(axes, ['nominal_million','cpi_adjusted_per_resident_2024_cad']):
            indexed = rows[field]/rows.loc[rows.calendar_year==2018, field].iloc[0]*100
            ax.plot(rows.calendar_year, indexed, label=name, color=color, linewidth=2.3)
            ax.axhline(100, color='#777777', linewidth=.7)
            ax.set_xticks([2015,2018,2021,2024]); ax.set_xlabel('Fiscal-start calendar year')
            ax.grid(axis='y', alpha=.18)
    axes[0].set_title('Nominal functional expense');axes[1].set_title('CPI-adjusted expense per resident')
    axes[0].set_ylabel('Index: 2018–19 = 100');axes[0].legend(fontsize=9, loc='upper left')
    fig.suptitle('Spending growth changes after population and inflation adjustments', fontsize=15)
    save(fig,'01_spending_intensity',
         'Two line charts index expenses to 2018–19=100. By2024–25 nominal health,education andsocial spending rose; CPI-adjusted per-resident health is98.6,education84.7,social105.4,totalprogram95.7.',
         'Source:2024–25 Final Results PDF pp13–14. Accounting breaks; July population and calendar CPI proxies.\nInput intensity, not service volume or quality; functions are not operating-only.')
    comp = pd.read_csv(ROOT/'data/functional_expense_baseline_comparisons.csv')
    rows = comp[(comp.baseline_calendar_year==2018) & comp.function.isin(selected)].copy()
    fig,ax=plt.subplots(figsize=(10,5.2))
    ax.barh(rows.function,rows.cpi_adjusted_per_resident_growth_pct,color=[COLORS[selected.index(x)] for x in rows.function])
    ax.axvline(0,color='#555555',linewidth=1);ax.set_xlim(-19,9)
    for i,row in enumerate(rows.itertuples()):
        x=row.cpi_adjusted_per_resident_growth_pct
        ax.text(x+(.35 if x>=0 else -.35),i,f'{x:+.1f}%',va='center',ha='left' if x>=0 else 'right')
    ax.set_xlabel('Change in CPI-adjusted expense per resident (%)');ax.invert_yaxis()
    ax.set_title('2018–19 to 2024–25: resource intensity varies by function')
    save(fig,'02_allocation_change','Horizontal bars show CPI-adjusted expense per resident:health−1.4%,basic/advancededucation−15.3%,socialservices+5.4%,totalprograms−4.3%.',
         'Source:Final Results pp13–14; same-vintage actuals. Education combines basic and advanced education.\nTotal residents are not students or patients; CPI is not a sector cost index; accounting changes apply.')
    econ=pd.read_csv(ROOT/'data/economic_outcome_context.csv')
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    axes[0].plot(econ.calendar_year,econ.average_weekly_earnings,label='Nominal CAD/week',linewidth=2.3)
    axes[0].plot(econ.calendar_year,econ.weekly_earnings_cpi_adjusted_2024_cad,label='CPI-adjusted 2024 CAD/week',linewidth=2.3)
    axes[0].set_ylabel('Average weekly earnings (CAD)');axes[0].legend(fontsize=9);axes[0].set_title('Pay: levels do not equal purchasing power')
    axes[1].plot(econ.calendar_year,econ.unemployment_rate,marker='o',linewidth=2.3)
    axes[1].set_ylim(0,13);axes[1].set_ylabel('Unemployment rate (%)');axes[1].set_title('Unemployment: pandemic and recovery')
    for ax in axes:ax.set_xticks([2015,2018,2021,2024]);ax.set_xlabel('Calendar year');ax.grid(axis='y',alpha=.18)
    save(fig,'03_pay_and_unemployment','Averageweeklyearnings1148CAD2018→1328CAD2024 rose15.7%nominally butfell3.7%CPI-adjusted. Unemployment6.5%2018→7.0%2024;2020peak11.4%.',
         'Source:Final Results PDF p13,calendar-year rows. Earnings depend on employment mix/hours.\nNot median after-tax household income, poverty or household-specific affordability; no causal attribution.')
    crime=pd.read_csv(ROOT/'research/source_verification/safety_outcomes_2019_2023.csv')
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    for ax,metric,title in zip(axes,['violent_crime','property_crime'],['Violent crime rose','Property crime fell']):
        for geo,color in zip(['Alberta','Rural Alberta','Urban Alberta'],COLORS):
            rows=crime[(crime.metric==metric)&(crime.geography==geo)]
            ax.plot(rows.calendar_year,rows.value,label=geo,color=color,marker='o',linewidth=2)
        ax.set_title(title);ax.set_ylim(bottom=0);ax.set_xticks(range(2019,2024));ax.grid(axis='y',alpha=.18)
        ax.set_xlabel('Calendar year');ax.set_ylabel('Police-reported incidents /100,000')
    axes[0].legend(fontsize=9)
    save(fig,'04_safety','Separate charts show2019–2023violentcrimeAlberta1462→1591incidents/100000(+8.8%);property5894→4752(−19.4%). Ruralratesexceedurban for both. Eachchart hasindependent yscale.',
         'Source:PSES2024–25 annual report PDF p28 (printed26),method p44. Data end2023; revised.\nPolice-reported incidents, not all victimization or perceived safety. Independent y scales; no causal attribution.')
    edu=pd.read_csv(ROOT/'research/education_safety/current_education_observations.csv')
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    for metric,name,color in [('five_year_high_school_completion','All students',COLORS[0]),('FNMI_five_year_high_school_completion','Self-identified FNMI students',COLORS[1])]:
        rows=edu[(edu.metric==metric)&(edu.record_kind=='result')]
        axes[0].plot(rows.observation_period,rows.value,label=name,color=color,marker='o',linewidth=2.3)
        target=edu[(edu.metric==metric)&(edu.record_kind=='target')].iloc[-1]
        axes[1].barh(name,target.value,color='#D9DDE2',height=.6)
        actual=rows.value.iloc[-1];axes[1].barh(name,actual,color=color,height=.3)
        axes[1].text(actual-1,name,f'{actual:.1f}%',va='center',ha='right',color='white',fontsize=10)
        axes[1].text(target.value+.7,name,f'Target{target.value:.1f}%',va='center',fontsize=9)
    axes[0].set_ylim(0,100);axes[0].set_ylabel('Five-year completion (%)');axes[0].legend(fontsize=9,loc='lower left');axes[0].tick_params(axis='x',rotation=30)
    axes[0].set_title('School/cohort endpoints; not diploma-only');axes[1].set_xlim(0,110);axes[1].set_xlabel('Completion (%)');axes[1].set_title('2023–24: results below matched targets')
    save(fig,'05_completion','Fiveyearcompletionoverall86.2%2019–20→87.1%2023–24 after88.6%peak. FNMI68.1→69.7%. Latesttargets88.8overall/71.5FNMI bothmissed. OverallincludesFNMI.',
         'Source: Education 2024–25 annual PDF pp25,43; method pp89–90. One-year reporting lag.\nCOVID exam/mark changes affect cohorts; overall includes FNMI and is not a non-FNMI comparison.')
    fig,ax=plt.subplots(figsize=(10,5.4))
    for match,label,color in [('grade9_PAT_language_arts_acceptable_standard','Language arts',COLORS[0]),('grade9_PAT_mathematics_acceptable_standard','Mathematics',COLORS[1])]:
        rows=edu[(edu.metric==match)&(edu.record_kind=='result')]
        if rows.empty:
            raise ValueError(f'Expected reviewed education metric {match}; found {edu.metric.unique()}')
        ax.plot(rows.observation_period,rows.value,label=label,color=color,marker='o',linewidth=2.3)
        target=edu[(edu.metric==match)&(edu.record_kind=='target')].iloc[-1]
        ax.scatter(target.observation_period,target.value,color=color,marker='D',facecolors='none',s=75,zorder=4)
        ax.annotate(f'Target {target.value:.1f}%',(target.observation_period,target.value),xytext=(-8,7),textcoords='offset points',ha='right',color=color,fontsize=9)
    ax.set_ylim(0,100);ax.set_ylabel('Weighted acceptable-standard result (%)');ax.set_xlabel('School year');ax.set_title('Grade9 achievement: mathematics declined; latest targets missed');ax.legend(loc='lower left');ax.grid(axis='y',alpha=.18)
    save(fig,'06_grade9','Grade9acceptable-standard languagearts69.4→69.7%andmathematics53.1→51.7%2021–22to2024–25. Latesttargets72.0/55.3missed; participationchanged.',
         'Source: Education 2024–25 Annual Report Update PDF pp5–7,18–19. Weighted/enrolment-based outcomes.\n2020–21 missing (COVID); security/wildfire disruptions; changing participation; Grade6 curriculum break.')
    mental=pd.read_csv(ROOT/'research/source_verification/mental_health_access_2019_2023.csv')
    fig,ax=plt.subplots(figsize=(10,5.2));ax.plot(mental.fiscal_year,mental.value,marker='o',linewidth=2.3)
    ax.scatter('2023-24',17.9,marker='D',s=70,color=COLORS[1]);ax.annotate('Matched target17.9%',('2023-24',17.9),xytext=(-120,-22),textcoords='offset points',color=COLORS[1])
    ax.set_ylim(0,25);ax.set_ylabel('First ED visits without prior contact (%)');ax.set_xlabel('Observed fiscal year');ax.set_title('Mental-health access: modest decrease, latest target missed')
    save(fig,'07_mental_health','Eligiblefirstmental-health/addictionEDvisitswithoutpriorpublicservicecontact20.7%2019–20→19.7%2023–24;upfrom19.5prior year and above17.9matchedtarget. Lowerpreferred;not recovery.',
         'Source:Mental Health and Addiction2024–25 annual PDF pp35–36 (printed33–34). Up to10-month lag.\nEligibility/PHN exclusions; first visit/person/year. Prior contact measure, not recovery or all ED demand.')
    health=pd.read_csv(ROOT/'research/health/extracted/health_outcomes.csv')
    health=health[health.source_vintage=='2024-25']
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    ed=health[health.metric=='ED initial physician assessment wait']
    axes[0].plot(ed.period,ed.value,marker='o',linewidth=2.3,color=COLORS[1])
    axes[0].set_ylim(0,8);axes[0].set_ylabel('Hours at 90th percentile');axes[0].set_title('ED wait: longer at 16 largest sites')
    for group,color in zip(['MRI','CT'],COLORS):
        rows=health[(health.metric=='Diagnostic imaging within priority targets')&(health.group==group)]
        axes[1].plot(rows.period,rows.value,label=group,color=color,marker='o',linewidth=2.3)
    axes[1].set_ylim(0,100);axes[1].set_ylabel('Scans within priority targets (%)');axes[1].set_title('Diagnostic access: MRI share declined');axes[1].legend()
    for ax in axes:ax.set_xlabel('Fiscal year');ax.tick_params(axis='x',rotation=25);ax.grid(axis='y',alpha=.18)
    save(fig,'08_emergency_and_imaging','ED90thpercentilewait4.5hours2021–22→7.0hours2024–25at16largest sites. MRIwithinprioritytargets68→41%;CT87→80%. EDlatestworse than6.7hourpriorresult/target.',
         'Source: Health2024–25 annual PDF pp23,30. ED2021–22/2022–23 revised; excludes left without being seen.\nED is neither average nor province-wide; MRI/CT denominators and clinical priorities differ; source-method issue retained.')
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    for group,color in zip(['Hip','Knee','Cataract'],COLORS):
        rows=health[(health.metric=='Elective surgery within national wait benchmark')&(health.group==group)]
        axes[0].plot(rows.period,rows.value,label=group,color=color,marker='o',linewidth=2.3)
    axes[0].set_ylim(0,100);axes[0].set_ylabel('Procedures within national wait benchmark (%)');axes[0].set_title('Selected elective surgery access improved');axes[0].legend(fontsize=9,loc='lower right')
    for group,label,color in zip(['Metro/urban','Communities >3000 residents','Rural <3000 residents','Remote'],['Metro/urban','Communities >3,000','Rural <3,000','Remote'],COLORS):
        rows=health[(health.metric=='EMS urgent-call response')&(health.group==group)]
        axes[1].plot(rows.period,rows.value,label=label,color=color,marker='o',linewidth=2)
    axes[1].set_ylim(0,75);axes[1].set_ylabel('Response minutes at 90th percentile');axes[1].set_title('EMS: regional results differ');axes[1].legend(fontsize=9,loc='upper left')
    for ax in axes:ax.set_xlabel('Fiscal year');ax.tick_params(axis='x',rotation=25);ax.grid(axis='y',alpha=.18)
    save(fig,'09_surgery_and_ems','Hip/knee/cataractshareswithinbenchmarks2023–24→2024–25improved62.4→72.8%,53.3→62.5%,59.7→62.8%. EMS90thpercentilemetro13.8→14.2minworse;rural33.3→29.2andremote64.9→52improved.',
         'Source: Health2024–25 annual PDF pp24,26. Surgery excludes emergency procedures; completed-case denominator.\nEMS urgent Delta/Echo calls; higher-acuity Echo priority; regions differ. Pandemic baseline; no causal attribution.')
    social=pd.read_csv(ROOT/'research/living_standards/current_social_outcomes_2021_2024.csv')
    rows=social[social.metric=='new_affordable_housing_units_and_additional_rental_subsidies']
    fig,ax=plt.subplots(figsize=(10,5.3));ax.bar(rows.period,rows.value,color=COLORS[0])
    for row in rows.itertuples():ax.text(row.period,row.value+40,f'{int(row.value):,}',ha='center')
    ax.scatter('2024-25',1500,color=COLORS[1],marker='D',s=75);ax.annotate('Matched target 1,500',('2024-25',1500),xytext=(-8,12),ha='right',textcoords='offset points',color=COLORS[1])
    ax.set_ylim(0,2700);ax.set_xlabel('Fiscal year');ax.set_ylabel('Units + additional supported households');ax.set_title('Housing support expansion slowed; measure mixes units and subsidies')
    save(fig,'10_housing_support','Combined new affordable units and additional rent-supported households2243,2325,2302,798 FY2021–22to2024–25. Latest798below1500target;not798newhomes or netstock.',
         'Source: SCSS2024–25 annual PDF p38 (printed36),method p67. Combined access/output measure.\n2024–25 breakdown388 units +410 additional subsidy households; includes regenerated units; not net housing stock.')
    poverty=pd.read_csv(ROOT/'research/living_standards/mbm_poverty_all_persons_2015_2024.csv')
    fig,axes=plt.subplots(1,2,figsize=(12,5.4),sharey=True)
    for ax,base in zip(axes,['Market basket measure, 2018 base','Market basket measure, 2023 base']):
        for geo,color in zip(['Alberta','Canada'],COLORS):
            rows=poverty[(poverty.mbm_base==base)&(poverty.geography==geo)]
            ax.plot(rows.calendar_year,rows.poverty_rate_pct,color=color,label=geo,marker='o',linewidth=2.3)
        ax.set_title(base.replace('Market basket measure, ','MBM '));ax.set_ylim(0,16);ax.set_xlabel('Calendar year');ax.grid(axis='y',alpha=.18)
    axes[0].set_ylabel('All-person poverty rate (%)');axes[0].legend();axes[0].set_xticks([2015,2018,2021,2023]);axes[1].set_xticks(range(2020,2025))
    fig.suptitle('Poverty: compare within each basket base; do not join across bases',fontsize=15)
    save(fig,'11_poverty','Separate MBM bases:2018-base Alberta9.4%2018→10.0%2023;2024 absent.2023-base Alberta10.5%2022,10.2%2023,11.0%2024;Canada11.0%2024. No cross-base splice or significance claim.',
         'Source: Statistics Canada11-10-0135-01, downloaded9Oct2026; Canadian Income Survey, all persons.\nSurvey estimates/quality flags retained; Census revisions and2021/2022 method changes; pandemic-era lows not a counterfactual.')
    life_raw=pd.read_csv(ROOT/'research/health/life_tables/life_expectancy_age0_bothsexes.csv')
    life=life_raw[(life_raw.Element=='Life expectancy (in years) at age x (ex)')&(life_raw.REF_DATE.between(2015,2024))].copy()
    margins=life_raw[life_raw.Element=='Margin of error of the life expectancy (m.e.(ex))'][['REF_DATE','GEO','VALUE']].rename(columns={'VALUE':'margin_95'})
    life=life.merge(margins,on=['REF_DATE','GEO'],validate='one_to_one')
    assert len(life)==20 and not life.duplicated(['REF_DATE','GEO']).any()
    fig,ax=plt.subplots(figsize=(10,5.4))
    for geo,color in zip(['Alberta','Canada'],COLORS):
        rows=life[life.GEO==geo].sort_values('REF_DATE')
        ax.plot(rows.REF_DATE,rows.VALUE,label=geo,color=color,marker='o',linewidth=2.3)
        ax.fill_between(rows.REF_DATE,rows.VALUE-rows.margin_95,rows.VALUE+rows.margin_95,color=color,alpha=.14)
    ax.axvspan(2023,2024,color='#D9DDE2',alpha=.3,label='2023–24 preliminary')
    ax.set_ylim(79,83);ax.set_ylabel('Period life expectancy at birth (years)');ax.set_xlabel('Calendar year');ax.set_xticks([2015,2018,2019,2022,2024]);ax.set_title('Life expectancy recovered after2022, but remains below2019');ax.legend(fontsize=9);ax.grid(axis='y',alpha=.18)
    save(fig,'12_life_expectancy','Alberta period life expectancy at birth81.96years2019→80.19years2022→81.53years2024. Canada82.16years2024.2023–24preliminary; one currentvintage, separatefromarchivedAHCIP series.',
         'Source: Statistics Canada13-10-0837-01, single-year life table, age0/both sexes; downloaded9Oct2026.\nShading: source95% intervals (revision uncertainty excluded).2023–24 preliminary; period, not cohort/healthy life expectancy.')
    (ROOT/'data/figure_receipts.json').write_text(json.dumps(RECEIPTS,indent=2)+'\n')
    print(f'Built {len(RECEIPTS)} figures.')


if __name__=='__main__':build()
