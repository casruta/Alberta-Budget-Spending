"""Regression checks for consequential definition, date and missingness boundaries."""
from pathlib import Path
import csv
import json
from decimal import Decimal
import pandas as pd
import pytest
import pypdf

ROOT=Path(__file__).resolve().parents[1]


def test_poverty_bases_do_not_create_missing_endpoints():
    f=pd.read_csv(ROOT/'research/living_standards/mbm_poverty_all_persons_2015_2024.csv')
    assert not f.duplicated(['calendar_year','geography','mbm_base']).any()
    assert f[(f.mbm_base=='Market basket measure, 2018 base')&(f.calendar_year==2024)].empty
    assert f[(f.mbm_base=='Market basket measure, 2023 base')&(f.calendar_year==2018)].empty
    rows=f[(f.geography=='Alberta')&(f.mbm_base=='Market basket measure, 2023 base')].set_index('calendar_year')
    assert rows.loc[2024,'poverty_rate_pct']==11.0 and rows.loc[2024,'quality_flag']=='B'
    assert rows.loc[2023,'poverty_rate_pct']==10.2
    assert rows.loc[2024,'source_status']=='historical survey estimate; latest downloaded vintage'


@pytest.mark.parametrize('metric,period,result,target',[
    ('five_year_high_school_completion','2023-24',87.1,88.8),
    ('FNMI_five_year_high_school_completion','2023-24',69.7,71.5),
    ('grade9_PAT_language_arts_acceptable_standard','2024-25',69.7,72.0),
    ('grade9_PAT_mathematics_acceptable_standard','2024-25',51.7,55.3),
])
def test_education_targets_match_the_observed_period(metric,period,result,target):
    f=pd.read_csv(ROOT/'research/education_safety/current_education_observations.csv')
    rows=f[(f.metric==metric)&(f.observation_period==period)]
    assert rows[rows.record_kind=='result'].value.tolist()==[result]
    assert rows[rows.record_kind=='target'].value.tolist()==[target]
    assert not ((f.metric==metric)&(f.observation_period=='2020-21')&(f.value==0)).any()


def test_earnings_calculation_has_separate_estimate_status():
    f=pd.read_csv(ROOT/'data/economic_outcome_context.csv').set_index('calendar_year')
    assert 'estimate' in f.loc[2024,'primary_household_income_growth_status']
    assert f.loc[2024,'primary_household_income_growth_unit']
    # Independent rounded source cells and Decimal chain, without importing production helpers.
    factor=Decimal(1)
    for pct in ['1.8','1.1','3.2','6.4','3.3','2.9']:
        factor*=1+Decimal(pct)/100
    change=(Decimal(1328)/Decimal(1148)/factor-1)*100
    observed=(f.loc[2024,'weekly_earnings_cpi_adjusted_2024_cad']/f.loc[2018,'weekly_earnings_cpi_adjusted_2024_cad']-1)*100
    assert abs(observed-float(change))<1e-9


def test_financial_source_anomaly_is_preserved_not_silently_repaired():
    f=pd.read_csv(ROOT/'research/budget/latest_vintage_functional_expenses_2015_2024.csv').set_index('calendar_year')
    source=pypdf.PdfReader(ROOT.parent/'Budget PDFs/2024-2025 Budget.pdf').pages[13].extract_text()
    assert '13,769' in source and '61,691' in source
    row=f.loc[2022]
    assert row.other_program_expense_million==13769 and row.total_program_expense_million==61691
    assert row.program_component_rounding_residual_million==-6
    assert 'source anomaly' in row.program_reconciliation_status
    assert f.total_component_rounding_residual_million.abs().max()==0


def test_health_series_keeps_old_definitions_and_vintages_separate():
    f=pd.read_csv(ROOT/'research/health/extracted/health_outcomes.csv')
    assert not f.duplicated(['metric','group','period','source_vintage']).any()
    rows=f[(f.source_vintage=='2024-25')&(f.metric=='ED initial physician assessment wait')]
    assert rows.period.tolist()==['2021-22','2022-23','2023-24','2024-25']
    assert rows.value.tolist()==[4.5,6.2,6.7,7.0]
    assert rows.group.unique().tolist()==['16 largest hospital sites']
    assert (rows.unit=='hours at 90th percentile').all()
    unresolved=f[(f.metric=='Life expectancy at birth')&(f.source_vintage=='2018-19')]
    assert (unresolved.primary_within_definition==False).all()


def test_housing_units_are_not_subsidies_or_net_stock():
    f=pd.read_csv(ROOT/'research/living_standards/current_social_outcomes_2021_2024.csv')
    current=f[f.period=='2024-25'].set_index('metric')
    assert current.loc['new_affordable_housing_units_and_additional_rental_subsidies','value']==798
    assert current.loc['newly_built_units_breakdown','value']==388
    assert current.loc['additional_households_supported_rent_supplement','value']==410
    assert current.loc['housing_combined_measure_target','value']==1500
    assert 'mixed' in current.loc['new_affordable_housing_units_and_additional_rental_subsidies','unit']


def test_crime_calendar_end_and_separate_geographies():
    f=pd.read_csv(ROOT/'research/source_verification/safety_outcomes_2019_2023.csv')
    assert f.calendar_year.max()==2023 and len(f)==30
    assert not f.duplicated(['metric','geography','calendar_year']).any()
    ab=f[(f.metric=='violent_crime')&(f.geography=='Alberta')]
    assert ab.value.tolist()==[1462,1455,1519,1561,1591]


def test_mental_access_target_does_not_move_to_publication_year():
    f=pd.read_csv(ROOT/'research/source_verification/mental_health_access_2019_2023.csv')
    row=f[f.fiscal_year=='2023-24'].iloc[0]
    assert row.value==19.7 and row.target==17.9 and row.target_period=='2023-24'
    assert f[f.fiscal_year=='2024-25'].empty


def test_life_table_elements_and_latest_preliminary_status():
    f=pd.read_csv(ROOT/'research/health/life_tables/life_expectancy_age0_bothsexes.csv')
    rows=f[(f.GEO=='Alberta')&(f.REF_DATE==2024)].set_index('Element')
    assert rows.loc['Life expectancy (in years) at age x (ex)','VALUE']==81.53
    assert rows.loc['Margin of error of the life expectancy (m.e.(ex))','VALUE']==.14
    assert (f['Age group']=='0 years').all() and (f.Sex=='Both sexes').all()
    assert not f.duplicated(['REF_DATE','GEO','Element']).any()
    metadata=(ROOT/'research/health/life_tables/13100837_MetaData.csv').read_text()
    assert '2023' in metadata and '2024' in metadata and 'preliminary' in metadata
    assert '95%' in metadata or '95%' in (ROOT/'research/health/LIFE_EXPECTANCY_AUDIT.md').read_text()
