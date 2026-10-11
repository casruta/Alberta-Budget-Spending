"""Independent financial arithmetic and consequential reporting boundaries."""
from pathlib import Path
import csv,hashlib,json,math,subprocess,sys
import pytest

HOME=Path(__file__).resolve().parents[1]
ROOT=HOME.parent
FACTS=json.loads((HOME/'data/chart_data.json').read_text())
CHARTS=json.loads((HOME/'data/chart_catalog.json').read_text())


def source(path):
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def points(chart,panel='p1'):
    return [r for r in FACTS if r['ChartId']==chart and r['Panel']==panel]


def point(chart,period,series,panel='p1'):
    rr=[r for r in points(chart,panel) if r['Period']==period and r['Series']==series]
    assert len(rr)==1
    return rr[0]['Value']


@pytest.mark.parametrize('function',['Health','Basic and advanced education','Social services','Total programs'])
def test_functional_adjustment_reconciles_to_independent_population_price_benchmark(function):
    capital={int(r['calendar_year']):r for r in source('Infrastructure Analysis/data/capital_population_analysis.csv')}
    base,latest=capital[2018],capital[2024]
    denominator=float(latest['population_july_1'])/float(base['population_july_1'])*float(latest['cpi_index_2015_100'])/float(base['cpi_index_2015_100'])
    nominal={int(r['calendar_year']):float(r['nominal_million']) for r in source('Quality of Life Analysis/data/functional_expense_intensity.csv') if r['function']==function}
    expected=(nominal[2024]/nominal[2018]/denominator-1)*100
    assert point('qol_02_allocation_change',function,'Change')==pytest.approx(expected)
    assert point('qol_01_spending_intensity','2024-25',function,'p2')==pytest.approx(expected+100)


def test_capital_latest_actual_and_execution_use_paired_budget():
    assert point('infra_01_actual_capital_spending','2024-25','Actual')==pytest.approx(7.243)
    assert point('infra_09_reported_budget_execution','2024-25','Paired budget')==pytest.approx(8.299)
    assert point('infra_09_reported_budget_execution','2024-25','Execution','p2')==pytest.approx(7.243/8.299*100)


def test_all_four_government_period_sensitivities_preserved():
    assert len(points('infra_06_tenure_sensitivity'))==4
    assert any(r['Period']=='2022-23 to 2024-25' for r in points('infra_06_tenure_sensitivity'))


def test_poverty_bases_not_spliced_and_quality_flags_retained():
    original=source('Quality of Life Analysis/research/living_standards/mbm_poverty_all_persons_2015_2024.csv')
    for p,base in [('p1','Market basket measure, 2018 base'),('p2','Market basket measure, 2023 base')]:
        expected=[r for r in original if r['mbm_base']==base];actual=points('qol_11_poverty',p)
        assert len(actual)==len(expected)
        for r in expected:
            assert point('qol_11_poverty',r['calendar_year'],r['geography'],p)==float(r['poverty_rate_pct'])
            record=next(x for x in actual if x['Period']==r['calendar_year'] and x['Series']==r['geography'])
            assert r['quality_flag'] in record['Status']
    assert not any(r['Period']=='2024' for r in points('qol_11_poverty','p1'))


def test_missing_grade9_period_is_not_fabricated():
    assert not any(r['Period']=='2020-21' for r in points('qol_06_grade9'))
    assert all(r['ObservationKind']=='Target' for r in points('qol_06_grade9','p2') if r['Series']=='Target')


def test_housing_target_and_mixed_output_are_distinct_source_rows():
    rr=points('qol_10_housing_support');result=next(r for r in rr if r['Period']=='2024-25' and r['Series']=='Result');target=next(r for r in rr if r['Series']=='Matched target')
    assert result['Value']==798 and target['Value']==1500
    assert result['SourceRows']!=target['SourceRows']
    assert target['ObservationKind']=='Target' and target['Unit']=='Units + households'


def test_life_expectancy_source_bounds_and_preliminary_status():
    assert point('qol_12_life_expectancy','2024','Estimate')==81.53
    assert point('qol_12_life_expectancy','2024','Lower 95%')==pytest.approx(81.53-.14)
    assert point('qol_12_life_expectancy','2024','Upper 95%')==pytest.approx(81.53+.14)
    assert all(r['Status']=='Preliminary' for r in points('qol_12_life_expectancy') if r['Period'] in ['2023','2024'])


def test_resource_totals_reconcile_without_stacking_components_twice():
    residual={'2024-25':0,'2025-26':1,'2026-27':0,'2027-28':0,'2028-29':-1}
    for year in residual:
        a=point('plan_revenue_resource_risk',year,'Bitumen royalty');b=point('plan_revenue_resource_risk',year,'Other non-renewable resource revenue')
        assert (a+b-point('plan_revenue_resource_risk',year,'Reported resource total'))*1000==pytest.approx(residual[year],abs=1e-8)
    chart=next(c for c in CHARTS if c['id']=='plan_revenue_resource_risk')
    assert chart['panels'][0]['visual_type']=='lineChart'


def test_revenue_composition_reconciles_to_original_fiscal_summary():
    revenue=next(r for r in source('Data/fiscal_plan_2026_fiscal_summary.csv') if r['Item']=='Total revenue')
    residual={'2024-25':0,'2025-26':0,'2026-27':0,'2027-28':1,'2028-29':1}
    for col in ['2024-25 Actual','2025-26 Forecast','2026-27 Estimate','2027-28 Target','2028-29 Target']:
        rr=[r for r in points('plan_revenue_composition') if r['Period']==col[:7]]
        assert sum(r['Value'] for r in rr)*1000-float(revenue[col])==pytest.approx(residual[col[:7]],abs=1e-8)
        assert {r['ObservationKind'] for r in rr}=={col.split(' ',1)[1]}


def test_per_dollar_expense_includes_debt_and_residual_and_can_exceed_100():
    rr=points('plan_per_dollar_breakdown');labels={r['Period'] for r in rr}
    assert 'Debt servicing' in labels and 'Other government services and residual' in labels
    assert sum(r['Value'] for r in rr)==pytest.approx(83922/74550*100)
    assert sum(r['Value'] for r in rr)>100


def test_debt_components_reconcile_to_reported_total():
    original=next(r for r in source('Data/fiscal_plan_2026_financial_position.csv') if r['Item']=='Total taxpayer-supported debt')
    residual={'2025':0,'2026':1,'2027':-1,'2028':0,'2029':0}
    for col in original:
        if not col.startswith('At March'):continue
        year=next(y for y in ['2025','2026','2027','2028','2029'] if y in col)
        assert sum(r['Value'] for r in points('plan_debt_trajectory') if r['Period']=='March '+year)*1000-float(original[col])==pytest.approx(residual[year],abs=1e-8)


def test_original_historical_subpanels_retained_without_unit_mixing():
    assert len(points('history_expense_composition','p2'))==70
    for year in {r['Period'] for r in points('history_expense_composition','p2')}:
        assert sum(r['Value'] for r in points('history_expense_composition','p2') if r['Period']==year)==pytest.approx(100)
    assert len(points('history_expense_percapita','p2'))==15
    assert len(points('history_expense_real_spending','p2'))==14
    assert len(points('history_expense_health_deep_dive','p3'))==28


def test_hypothetical_values_never_labelled_as_observed_prices():
    rr=points('infra_08_hypothetical_price_sensitivity')
    assert rr and {r['ObservationKind'] for r in rr}=={'Hypothetical scenario'}
    assert all('hypothetical_price_scenarios.csv' in r['SourcePaths'] for r in rr)


def test_source_hashes_and_exclusions_match_preserved_evidence():
    catalog=json.loads((HOME/'data/source_catalog.json').read_text())
    excluded=[r for r in catalog if not r['ModelTable']]
    assert len(excluded)==3 and sum('DRAFT_DO_NOT_USE' in r['Path'] for r in excluded)==1
    for r in catalog:assert hashlib.sha256((ROOT/r['Path']).read_bytes()).hexdigest()==r['SHA256']
    assert not any('DRAFT_DO_NOT_USE' in r['SourcePaths'] for r in FACTS)


def test_rebuild_is_deterministic_and_does_not_modify_sources():
    tracked=[HOME/'data/chart_data.json',HOME/'data/chart_catalog.json',HOME/'data/source_catalog.json',HOME/'data/source_tables.json',HOME/'data/transformation_manifest.json',HOME/'data/project_manifest.json',HOME/'downloads/AlbertaBudget-PowerBI.zip']
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    for script in ['transform_data.py','build_project.py']:
        subprocess.run([sys.executable,str(HOME/'scripts'/script)],check=True,capture_output=True)
    assert {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}==before
