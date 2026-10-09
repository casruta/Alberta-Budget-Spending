"""Build auditable allocation and purchasing-power sensitivities, not a QoL score."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS = {
    'health_expense_million': 'Health',
    'basic_advanced_education_expense_million': 'Basic and advanced education',
    'social_services_expense_million': 'Social services',
    'other_program_expense_million': 'Other programs',
    'total_program_expense_million': 'Total programs',
    'debt_servicing_expense_million': 'Debt servicing',
    'total_expense_million': 'Total expense',
}


def analyze():
    (ROOT / 'data').mkdir(exist_ok=True)
    budget = pd.read_csv(ROOT / 'research/budget/latest_vintage_functional_expenses_2015_2024.csv')
    assert budget.calendar_year.tolist() == list(range(2015, 2025))
    # Recompute directly from the official annual growth row instead of trusting a cached index.
    budget['cpi_index_2015_100'] = 100.0
    for i in range(1, len(budget)):
        budget.loc[i, 'cpi_index_2015_100'] = (budget.loc[i-1, 'cpi_index_2015_100'] *
            (1 + budget.loc[i, 'alberta_calendar_annual_cpi_growth_pct'] / 100))
    budget['cpi_deflator_to_2024'] = budget.cpi_index_2015_100.iloc[-1] / budget.cpi_index_2015_100
    rows = []
    for source in budget.to_dict('records'):
        for field, name in FUNCTIONS.items():
            nominal = source[field] * 1_000_000
            population = source['population_july_1_thousands'] * 1000
            rows.append(dict(calendar_year=source['calendar_year'], fiscal_year=source['fiscal_year'],
                             function=name, nominal_million=source[field], population_july_1=population,
                             cpi_index_2015_100=source['cpi_index_2015_100'],
                             nominal_per_resident=nominal/population,
                             cpi_adjusted_per_resident_2024_cad=nominal/population*source['cpi_deflator_to_2024'],
                             expense_pdf_page=14, economic_pdf_page=13,
                             source_file='Budget PDFs/2024-2025 Budget.pdf',
                             status='actual expense; derived intensity sensitivity',
                             caution='Accounting changes; July population/calendar CPI proxies; not service volume or quality.'))
    panel = pd.DataFrame(rows)
    panel.to_csv(ROOT / 'data/functional_expense_intensity.csv', index=False)
    comparisons = []
    for base in [2015, 2018, 2019, 2023]:
        for name in FUNCTIONS.values():
            start = panel[(panel.calendar_year == base) & (panel.function == name)].iloc[0]
            end = panel[(panel.calendar_year == 2024) & (panel.function == name)].iloc[0]
            comparisons.append(dict(baseline_calendar_year=base, endpoint_calendar_year=2024, function=name,
                                    nominal_growth_pct=(end.nominal_million/start.nominal_million-1)*100,
                                    nominal_per_resident_growth_pct=(end.nominal_per_resident/start.nominal_per_resident-1)*100,
                                    cpi_adjusted_per_resident_growth_pct=(end.cpi_adjusted_per_resident_2024_cad/start.cpi_adjusted_per_resident_2024_cad-1)*100))
    pd.DataFrame(comparisons).to_csv(ROOT / 'data/functional_expense_baseline_comparisons.csv', index=False)
    econ = pd.read_csv(ROOT / 'research/living_standards/economic_indicators_source_ledger.csv')
    econ = econ[econ.panel == 'primary_same_vintage_2013_2024']
    assert not econ.duplicated(['calendar_year', 'metric']).any()
    wide = econ.pivot(index='calendar_year', columns='metric', values='value').reset_index()
    for metric in econ.metric.unique():
        definitions = econ[econ.metric == metric].set_index('calendar_year')
        wide[f'{metric}_status'] = wide.calendar_year.map(definitions.status)
        wide[f'{metric}_unit'] = wide.calendar_year.map(definitions.unit)
    wide['source_file'] = 'Budget PDFs/2024-2025 Budget.pdf'
    wide['source_pdf_page'] = 13
    wide['time_basis'] = 'calendar year'
    print('Economic metrics:', ', '.join(wide.columns))
    wide = wide.merge(budget[['calendar_year', 'cpi_index_2015_100']], on='calendar_year', validate='one_to_one')
    assert len(wide) == 10
    earnings_field = next(c for c in wide.columns if 'earnings' in c)
    wide['weekly_earnings_cpi_adjusted_2024_cad'] = wide[earnings_field] * budget.cpi_index_2015_100.iloc[-1] / wide.cpi_index_2015_100
    wide.to_csv(ROOT / 'data/economic_outcome_context.csv', index=False)
    metadata = dict(observation_fiscal_years='2015-16 through 2024-25',
                    source_report='2024-25 Final Results Year-End Report',
                    outcome_years='Economic series calendar 2015–2024; source marks selected values estimated',
                    cpi_index_2024=float(budget.cpi_index_2015_100.iloc[-1]),
                    statistical_scope='Descriptive source-backed calculation; no causal attribution or aggregate QoL score',
                    anomalies=['2022-23 function component sum exceeds source total by CAD6M; all published cells preserved'],
                    accounting_warning='Source says numbers not strictly comparable due to accounting policy changes; FY2019-20/2021-22 reorganizations.')
    (ROOT / 'data/analysis_metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(f'Built {len(panel)} function/year observations and {len(comparisons)} comparisons.')
    return panel, wide


if __name__ == '__main__':
    analyze()
