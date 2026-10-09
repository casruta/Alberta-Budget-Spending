"""Meaningful source/analysis/artifact checks; no source-data imputation."""
from pathlib import Path
import hashlib
import json
import re
from decimal import Decimal
import sys
import pandas as pd
import numpy as np
import pytest
import pdfplumber
import nbformat

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from analyze import load_primary, compare, period_summary


@pytest.fixture(scope='module')
def panel():return load_primary()


def test_actual_window_has_ten_unique_complete_years(panel):
    assert panel.calendar_year.tolist()==list(range(2015,2025))
    assert panel.fiscal_year.nunique()==10
    assert panel.status.eq('actual').all()
    assert panel.source_cutoff.eq('2025-03-31').all()
    assert 2025 not in panel.calendar_year.values


def test_primary_pdf_title_and_economic_rows():
    with pdfplumber.open(ROOT.parent/'Budget PDFs/2024-2025 Budget.pdf') as pdf:
        economic=pdf.pages[12].extract_text()
        historical=pdf.pages[13].extract_text()
        title=pdf.pages[1].extract_text()
    assert 'Final Results' in title and 'June 2025' in title
    population_line=[s for s in economic.splitlines() if s.startswith('Population (July')][0]
    for value in ['4,150','4,293','4,355','4,685','4,889']:
        assert value in population_line
    assert 'Alberta consumer price index' in economic
    assert 'Numbers are not strictly comparable' in historical
    assert 'capital grants and other support included in expense' in historical


def test_source_capital_history_independent_text_read(panel):
    with pdfplumber.open(ROOT.parent/'Budget PDFs/2024-2025 Budget.pdf') as pdf:
        text=pdf.pages[13].extract_text()
    line=next(s for s in text.splitlines() if s.startswith('Capital Plan b'))
    numbers=re.findall(r'\d\s*,\s*\d{3}',line)
    # The layout contains spaces inside numbers; normalization is deliberately explicit.
    values=[int(n.replace(',','').replace(' ','')) for n in numbers]
    assert values==[5770,6181,6558,6578,9021,6057,5545,6896,6622,5633,6300,7243]
    assert panel.capital_plan_actual_million.astype(int).tolist()==values[2:]


@pytest.mark.parametrize('base_year,expected_nominal,expected_real',[
    (2015,10.445257700518,-25.801631477424),
    (2018,19.58065048704,-12.589056616679),
    (2019,30.622182146078,-1.395467489858),
])
def test_principal_ratios_independent_decimal(panel,base_year,expected_nominal,expected_real):
    capital={2015:6558,2018:6057,2019:5545,2024:7243}
    population={2015:4150000,2018:4293000,2019:4355000,2024:4889000}
    rates={2016:'1.1',2017:'1.6',2018:'2.4',2019:'1.8',2020:'1.1',
           2021:'3.2',2022:'6.4',2023:'3.3',2024:'2.9'}
    price_ratio=Decimal(1)
    for year in range(base_year+1,2025):
        price_ratio*=1+Decimal(rates[year])/100
    spend_ratio=Decimal(capital[2024])/Decimal(capital[base_year])
    population_ratio=Decimal(population[2024])/Decimal(population[base_year])
    independent=float((spend_ratio/population_ratio/price_ratio-1)*100)
    result=compare(panel,base_year)
    assert result['nominal_capital_growth_pct']==pytest.approx(float((spend_ratio-1)*100),abs=1e-9)
    assert result['cpi_adjusted_per_resident_growth_pct']==pytest.approx(independent,abs=1e-9)
    # Published rounded headlines must retain the same direction and magnitude.
    assert round(result['nominal_capital_growth_pct'],1)==round(expected_nominal,1)
    assert round(result['cpi_adjusted_per_resident_growth_pct'],1)==round(expected_real,1)


def test_cpi_index_does_not_include_baseline_year_rate(panel):
    assert panel.loc[0,'cpi_index_2015_100']==100
    assert panel.loc[1,'cpi_index_2015_100']==pytest.approx(101.1)
    assert panel.loc[9,'cpi_index_2015_100']==pytest.approx(126.3516085848)


def test_population_independent_extracts_agree(panel):
    assert np.array_equal(panel.population_july_1.to_numpy(),
                          panel.population_july1_thousands.to_numpy()*1000)
    assert panel.population_july_1.gt(0).all()
    assert panel.capital_nominal_cad.gt(0).all()


def test_combined_benchmark_is_multiplicative(panel):
    r=compare(panel,2018)
    nominal_factor=1+r['nominal_capital_growth_pct']/100
    population_factor=1+r['population_growth_pct']/100
    prices_factor=1+r['cpi_growth_pct']/100
    assert (nominal_factor/(population_factor*prices_factor)-1)*100 == pytest.approx(
        r['cpi_adjusted_per_resident_growth_pct'])
    assert r['endpoint_constant_intensity_benchmark_cad']>7_243_000_000
    assert 'not a quantified infrastructure need' in r['benchmark_interpretation']


def test_rounding_bounds_contain_estimate_and_are_not_confidence_interval(panel):
    for base in [2015,2018,2019,2022,2023]:
        r=compare(panel,base)
        assert r['rounding_sensitivity_real_per_resident_growth_low_pct'] < r['cpi_adjusted_per_resident_growth_pct'] < r['rounding_sensitivity_real_per_resident_growth_high_pct']
        assert 'not confidence intervals' in r['rounding_sensitivity_interpretation']


def test_tenure_weighting_uses_person_year_denominator(panel):
    p=period_summary(panel)
    for row,years in [(0,[2015,2016,2017,2018]),(1,list(range(2019,2025))),
                      (2,[2015,2016,2018]),(3,[2022,2023,2024])]:
        subset=panel.loc[panel.calendar_year.isin(years)]
        independent=sum(subset.capital_cpi_adjusted_2024_cad)/sum(subset.population_july_1)
        assert p.loc[row,'population_weighted_cpi_adjusted_per_resident_annual_2024_cad']==pytest.approx(independent)
        assert p.loc[row,'fiscal_years']==len(years)
    assert p.loc[0,'nominal_capital_total_cad']==28_214_000_000
    assert p.loc[1,'nominal_capital_total_cad']==38_239_000_000


def test_latest_sector_pair_reconciles_to_totals_with_disclosed_rounding():
    e=pd.read_csv(ROOT/'research/capital/actual_recent/recent_envelopes_all_vintages.csv')
    e=e.loc[e.source_vintage.eq('2024-25')]
    assert not e.duplicated(['fiscal_year','envelope']).any()
    p=e.pivot(index='envelope',columns='fiscal_year',values='actual_cad_millions')
    p=p.loc[~p.index.str.startswith('Total Capital Plan')]
    assert abs(p['2024-25'].sum()-7243)<=1
    assert abs(p['2023-24'].sum()-6300)<=1
    assert p.loc['Municipal Infrastructure Support','2024-25']-p.loc['Municipal Infrastructure Support','2023-24']==489
    assert p.loc['Protect Quality Health Care','2024-25']-p.loc['Protect Quality Health Care','2023-24']==318
    assert 7243-8299==-1056


def test_asset_stock_reconciliation_and_label():
    assert 62925-4080==58845
    assert 61515-3964==57551
    source=pd.read_csv(ROOT/'research/capital/latest_vintage_actual_series.csv')
    assert 'net_capital_nonfinancial_assets_after_deferred_contributions_million' in source.columns
    assert 'capital_nonfinancial_assets_million' not in source.columns


def test_supporting_2023_budget_transcription_matches_official_pair():
    with pdfplumber.open(ROOT.parent/'Budget PDFs/tbf-goa-2023-2024 Budget.pdf') as pdf:
        text=pdf.pages[15].extract_text()
    line=next(s for s in text.splitlines() if s.startswith('Total Capital Plan - Fully Consolidated Basis'))
    values=[int(n.replace(',','').replace(' ','')) for n in re.findall(r'\d\s*,\s*\d{3}',line)]
    assert values[:3]==[8005,6300,5633]
    supporting=(ROOT/'research/capital/FINDINGS.md').read_text()
    assert '2023–24 8,005/6,300' in supporting
    assert '2023–24 7,537/6,300' not in supporting


def test_source_hash_matches_execution_manifest():
    manifest=json.loads((ROOT/'data/run_manifest.json').read_text())
    for relative,digest in manifest['input_sha256'].items():
        assert hashlib.sha256((ROOT.parent/relative).read_bytes()).hexdigest()==digest
    assert not manifest['causal_inference']
    assert not manifest['construction_volume_inferred']


def test_missing_opening_dates_are_not_zero():
    timeline=pd.read_csv(ROOT/'research/physical/round2/project_timeline.csv')
    assert len(timeline)==17
    assert timeline.operational_year_if_verified.isna().all()
    assert not timeline.net_new_measure_if_known.fillna('').astype(str).eq('0').any()


def test_report_no_unresolved_variables_and_required_scope_caveats():
    report=(ROOT/'REPORT.md').read_text()
    assert '{{' not in report
    for fragment in ['12.6%','19.6%','2016–17 through 2025–26','2015–16 through 2024–25',
                     'not strictly comparable','not a construction deflator','not a statistical confidence interval',
                     '17 in progress','not 96 newly opened schools','not built or published']:
        assert fragment in report,fragment
    assert 'fell -' not in report


def test_report_and_readme_relative_local_links_exist():
    for path in [ROOT/'REPORT.md',ROOT/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' in target:continue
            from urllib.parse import unquote
            local=unquote(target.split('#')[0])
            assert (path.parent/local).exists(),(path.name,target)


def test_notebook_valid_structure():
    nb=nbformat.read(ROOT/'Alberta_Infrastructure_Analysis.ipynb',as_version=4)
    nbformat.validate(nb)
    headings='\n'.join(c.source for c in nb.cells if c.cell_type=='markdown')
    for heading in ['## tl;dr','## Context & Methods','## Data','## Results','## Takeaways']:
        assert heading in headings
    assert nb.metadata.kernelspec.name=='alberta-analysis'


def test_all_financial_figures_exported():
    figures=['01_actual_capital_spending','02_spending_per_resident','03_growth_benchmarks',
             '04_baseline_sensitivity','05_latest_sector_changes','06_tenure_sensitivity']
    figures+=['07_selected_project_stages','08_hypothetical_price_sensitivity','09_reported_budget_execution']
    for figure in figures:
        for extension in ['png','svg']:
            path=ROOT/'plots'/f'{figure}.{extension}'
            assert path.exists() and path.stat().st_size>10000


def test_hypothetical_price_scenarios_are_labelled_and_reconcile(panel):
    scenarios=pd.read_csv(ROOT/'data/hypothetical_price_scenarios.csv')
    assert scenarios.scenario_status.eq('hypothetical; not observed construction inflation').all()
    r=compare(panel,2018)
    for inflation in [0,5,10,20,30]:
        row=scenarios.loc[np.isclose(scenarios.assumed_cumulative_price_growth_pct,inflation)].iloc[0]
        expected=((1+r['nominal_per_resident_growth_pct']/100)/(1+inflation/100)-1)*100
        assert row.calculated_price_adjusted_spending_per_resident_growth_pct==pytest.approx(expected)


def test_selected_timeline_has_observations_not_imputed_openings():
    selected=pd.read_csv(ROOT/'data/selected_project_stages.csv')
    assert selected.first_observed_earlier_stage_year.notna().all()
    assert selected.operational_year_if_verified.notna().sum()==1
    operational=selected.loc[selected.operational_year_if_verified.notna()].iloc[0]
    assert operational.project=='Edmonton Anthony Henday Drive ring road'
    assert operational.operational_year_if_verified==2016
    assert (selected.earlier_year<=selected.reported_status_year).all()
    assert 'completion_year' not in selected.columns
    assert 'Highway43X Grande Prairie bypass' not in selected.project.values
