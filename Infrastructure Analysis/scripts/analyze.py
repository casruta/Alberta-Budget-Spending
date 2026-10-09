"""Reproducible descriptive analysis of Alberta's capital plan.

Inputs are source-reviewed local official report extracts, not operating budgets.
This module deliberately makes no causal or physical-capacity inference.
"""
from pathlib import Path
import os
import json
import hashlib
import platform
import importlib.metadata
os.environ.setdefault('MPLCONFIGDIR', '/workspace/.cache/matplotlib')
os.environ.setdefault('XDG_CACHE_HOME', '/workspace/.cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
BLUE = '#205E8C'
GOLD = '#B47717'
INK = '#263746'
GREY = '#697783'
ORANGE = '#B65829'


def load_primary():
    capital = pd.read_csv(ROOT / 'research/capital/latest_vintage_actual_series.csv')
    population = pd.read_csv(ROOT / 'research/demography/demography_cpi_2015_2024.csv')
    capital = capital.loc[capital.calendar_year.between(2015, 2024)].copy()
    if capital.calendar_year.duplicated().any() or population.calendar_year.duplicated().any():
        raise ValueError('Duplicate year would multiply rows in the join')
    data = capital.merge(population, on=['calendar_year', 'fiscal_year'],
                         how='left', validate='one_to_one', suffixes=('_capital', '_demography'))
    required = ['capital_plan_actual_million', 'population_july_1',
                'alberta_annual_cpi_growth_pct', 'cpi_chained_index_2015_100']
    if len(data) != 10 or data[required].isna().any().any():
        raise ValueError('Missing observations: do not fill missing actuals with zero')
    data = data.sort_values('calendar_year').reset_index(drop=True)
    if not (data.status == 'actual').all():
        raise ValueError('Forecasts are not eligible for this actual-spending analysis')
    if not (data.population_july_1 == data.population_july1_thousands * 1000).all():
        raise ValueError('Independent population extracts disagree')
    cpi = np.ones(10) * 100
    for i in range(1, len(data)):
        cpi[i] = cpi[i - 1] * (1 + data.loc[i, 'alberta_annual_cpi_growth_pct'] / 100)
    if not np.allclose(cpi, data.cpi_chained_index_2015_100, atol=1e-7):
        raise ValueError('CPI chain does not reconcile')
    data['cpi_index_2015_100'] = cpi
    data['cpi_deflator_2024'] = cpi[-1] / cpi
    data['capital_nominal_cad'] = data.capital_plan_actual_million * 1_000_000
    data['capital_nominal_per_resident_cad'] = data.capital_nominal_cad / data.population_july_1
    data['capital_cpi_adjusted_2024_cad'] = data.capital_nominal_cad * data.cpi_deflator_2024
    data['capital_cpi_adjusted_per_resident_2024_cad'] = (
        data.capital_cpi_adjusted_2024_cad / data.population_july_1)
    data['nominal_yoy_pct'] = data.capital_nominal_cad.pct_change() * 100
    data['real_per_resident_yoy_pct'] = data.capital_cpi_adjusted_per_resident_2024_cad.pct_change() * 100
    # First annual observation includes the May 2015 PC-to-NDP transition.
    data['government_period'] = np.where(data.calendar_year >= 2019,
        'UCP tenure; 2019-20 transition', 'NDP tenure; 2015-16 transition')
    data['source_cutoff'] = '2025-03-31'
    return data


def compare(data, base_year, end_year=2024):
    base = data.loc[data.calendar_year == base_year].iloc[0]
    end = data.loc[data.calendar_year == end_year].iloc[0]
    fields = {
        'nominal_capital_growth_pct': 'capital_nominal_cad',
        'population_growth_pct': 'population_july_1',
        'cpi_growth_pct': 'cpi_index_2015_100',
        'nominal_per_resident_growth_pct': 'capital_nominal_per_resident_cad',
        'cpi_adjusted_per_resident_growth_pct': 'capital_cpi_adjusted_per_resident_2024_cad',
    }
    result = {'baseline': base.fiscal_year, 'endpoint': end.fiscal_year}
    result.update({key: float((end[col] / base[col] - 1) * 100) for key, col in fields.items()})
    # Benchmark: hold baseline CPI-adjusted spending per resident constant.
    benchmark = base.capital_nominal_cad * end.population_july_1 / base.population_july_1
    benchmark *= end.cpi_index_2015_100 / base.cpi_index_2015_100
    result['endpoint_constant_intensity_benchmark_cad'] = float(benchmark)
    result['endpoint_difference_from_benchmark_cad'] = float(end.capital_nominal_cad - benchmark)
    result['benchmark_interpretation'] = ('Arithmetic constant-intensity comparison; '
        'not a quantified infrastructure need, fiscal target, funding gap or service shortfall.')
    # Rounding sensitivity only. CPI rates rounded to one decimal; population to 1000.
    rates = data.loc[data.calendar_year.between(base_year + 1, end_year),
                     'alberta_annual_cpi_growth_pct'].to_numpy()
    inflation_low = np.prod(1 + (rates - .05) / 100)
    inflation_high = np.prod(1 + (rates + .05) / 100)
    spend_low = (end.capital_plan_actual_million - .5) / (base.capital_plan_actual_million + .5)
    spend_high = (end.capital_plan_actual_million + .5) / (base.capital_plan_actual_million - .5)
    pop_low = (end.population_july_1 - 500) / (base.population_july_1 + 500)
    pop_high = (end.population_july_1 + 500) / (base.population_july_1 - 500)
    result['rounding_sensitivity_real_per_resident_growth_low_pct'] = float(
        (spend_low / pop_high / inflation_high - 1) * 100)
    result['rounding_sensitivity_real_per_resident_growth_high_pct'] = float(
        (spend_high / pop_low / inflation_low - 1) * 100)
    result['rounding_sensitivity_interpretation'] = (
        'Deterministic worst-case rounded-input bounds, not confidence intervals. '
        'Excludes revisions, fiscal-calendar alignment and construction-price uncertainty.')
    return result


def period_summary(data):
    periods = [
        ('2015-16 to 2018-19', data.calendar_year < 2019),
        ('2019-20 to 2024-25', data.calendar_year >= 2019),
        ('2015-16 to 2018-19 excluding 2017-18 spike',
         (data.calendar_year < 2019) & (data.calendar_year != 2017)),
        ('2022-23 to 2024-25', data.calendar_year >= 2022),
    ]
    rows = []
    for label, mask in periods:
        subset = data.loc[mask]
        rows.append({
            'period': label, 'fiscal_years': len(subset),
            'nominal_capital_total_cad': float(subset.capital_nominal_cad.sum()),
            'nominal_capital_annual_mean_cad': float(subset.capital_nominal_cad.mean()),
            'cpi_adjusted_capital_annual_mean_2024_cad': float(subset.capital_cpi_adjusted_2024_cad.mean()),
            'population_weighted_nominal_per_resident_annual_cad': float(
                subset.capital_nominal_cad.sum() / subset.population_july_1.sum()),
            'population_weighted_cpi_adjusted_per_resident_annual_2024_cad': float(
                subset.capital_cpi_adjusted_2024_cad.sum() / subset.population_july_1.sum()),
            'median_cpi_adjusted_per_resident_annual_2024_cad': float(
                subset.capital_cpi_adjusted_per_resident_2024_cad.median()),
            'interpretation': 'Descriptive tenure comparison, unequal periods, not causal policy effect',
        })
    return pd.DataFrame(rows)


def latest_envelopes():
    raw = pd.read_csv(ROOT / 'research/capital/actual_recent/recent_envelopes_all_vintages.csv')
    # The latest report supplies a same-classification pair; never splice sectors across vintages.
    raw = raw.loc[raw.source_vintage == '2024-25'].copy()
    return raw


def style():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
        'axes.titlesize': 16, 'axes.labelsize': 11, 'axes.spines.top': False,
        'axes.spines.right': False, 'axes.edgecolor': GREY, 'axes.labelcolor': INK,
        'text.color': INK, 'xtick.color': INK, 'ytick.color': INK,
        'figure.facecolor': 'white', 'axes.facecolor': 'white',
        'savefig.facecolor': 'white', 'lines.linewidth': 2.4,
        'svg.hashsalt': 'alberta-infrastructure-analysis-v1'})


def save(fig, filename, note, left=.10, bottom=.20, top=.86):
    title = fig.axes[0].get_title()
    fig.axes[0].set_title('')
    fig.suptitle(title, x=.5, y=.94, fontsize=16)
    fig.text(.09, .025, note, fontsize=9, color=GREY, ha='left', va='bottom')
    fig.subplots_adjust(bottom=bottom, top=top, left=left, right=.96)
    for extension in ['png', 'svg']:
        fig.savefig(ROOT / 'plots' / f'{filename}.{extension}', dpi=180,
                    metadata={'Date':'2026-10-09','Creator':'Alberta infrastructure analysis'})
    plt.close(fig)


def temporal_axis(ax, data, zero=True):
    ax.set_xticks(data.calendar_year)
    ax.set_xticklabels([str(y) for y in data.calendar_year])
    ax.set_xlabel('Fiscal year beginning in April of the labelled year')
    ax.grid(axis='y', color='#E5E9EC', linewidth=.7)
    ax.set_axisbelow(True)
    if zero:
        ax.set_ylim(bottom=0)
    ax.axvline(2018.5, linestyle=':', color=GREY, linewidth=1.4)


def build_figures(data, comparisons, periods):
    style()
    (ROOT / 'plots').mkdir(exist_ok=True)
    source = 'Source: Alberta 2024–25 Final Results, pp. 13–14. Actuals end March 31, 2025.'
    fig, ax = plt.subplots(figsize=(11.8, 6))
    values = data.capital_nominal_cad / 1e9
    ax.bar(data.calendar_year, values, color=BLUE, width=.65)
    for x, y in zip(data.calendar_year, values):
        ax.text(x, y+.12, f'{y:.2f}', ha='center', fontsize=10)
    ax.set_title('Actual capital spending declined in 2019, then recovered')
    ax.set_ylabel('Capital Plan spending, nominal CAD billions')
    ax.set_ylim(0, 10.1)
    temporal_axis(ax, data)
    ax.text(2018.55, 9.75, 'UCP takes office\nApril 2019', fontsize=10, va='top')
    save(fig, '01_actual_capital_spending', source+'\nIncludes grants and capital investment; spending is a flow, not infrastructure capacity.')

    fig, ax = plt.subplots(figsize=(11.8, 6))
    ax.plot(data.calendar_year, data.capital_nominal_per_resident_cad,
            marker='o', color=BLUE, label='Nominal dollars per resident')
    ax.plot(data.calendar_year, data.capital_cpi_adjusted_per_resident_2024_cad,
            marker='s', linestyle='--', color=GOLD, label='2024 consumer-price-adjusted dollars per resident')
    ax.set_title('The 2024–25 rebound remains below pre-UCP spending intensity')
    ax.set_ylabel('Capital spending per resident, CAD')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'${v:,.0f}'))
    temporal_axis(ax, data)
    ax.set_ylim(0, 2900)
    fig.legend(loc='upper center', bbox_to_anchor=(.56,.90), frameon=False, fontsize=10)
    save(fig, '02_spending_per_resident', source+'\nJuly 1 population; chained rounded annual CPI. CPI adjustment does not measure construction volume.', top=.78)

    fig, ax = plt.subplots(figsize=(11.8, 6))
    base = data.loc[data.calendar_year == 2018].iloc[0]
    population_index = data.population_july_1 / base.population_july_1 * 100
    population_price_index = population_index * data.cpi_index_2015_100 / base.cpi_index_2015_100
    ax.plot(data.calendar_year, data.capital_nominal_cad / base.capital_nominal_cad * 100,
            marker='o', color=BLUE, label='Actual nominal capital spending')
    ax.plot(data.calendar_year, population_index, linestyle='--', color=GREY,
            label='Population')
    ax.plot(data.calendar_year, population_price_index, linestyle='-.', color=GOLD,
            label='Population × consumer prices')
    temporal_axis(ax, data)
    ax.set_title('Capital spending grew less than population and consumer prices combined')
    ax.set_ylabel('Index, 2018–19 = 100')
    ax.set_ylim(0, 170)
    ax.axhline(100, color=INK, linewidth=.7)
    fig.legend(loc='upper center', bbox_to_anchor=(.56,.90), frameon=False, fontsize=10)
    save(fig, '03_growth_benchmarks', source+'\nPopulation × CPI is an arithmetic spending-intensity benchmark, not assessed infrastructure need.', top=.75)

    fig, ax = plt.subplots(figsize=(11.8, 6))
    view = comparisons.iloc[:3]
    positions = np.arange(len(view))
    labels = [f'{v} → 2024–25' for v in view.baseline]
    series = [('nominal_capital_growth_pct', 'Total nominal spending', BLUE),
              ('nominal_per_resident_growth_pct', 'Nominal spending per resident', GREY),
              ('cpi_adjusted_per_resident_growth_pct', 'CPI-adjusted spending per resident', GOLD)]
    for i, (field, label, color) in enumerate(series):
        bars = ax.barh(positions+(i-1)*.22, view[field], height=.20, color=color, label=label)
        for bar, v in zip(bars, view[field]):
            ax.text(v+(1 if v>=0 else -1), bar.get_y()+bar.get_height()/2,
                    f'{v:+.1f}%', va='center', ha='left' if v>=0 else 'right', fontsize=10)
    ax.set_yticks(positions, labels)
    ax.axvline(0, color=INK, linewidth=1)
    ax.set_xlim(-35, 45)
    ax.set_xlabel('Change from the specified baseline, percent')
    ax.set_title('The baseline changes the answer: show all three comparisons')
    fig.legend(loc='upper center', bbox_to_anchor=(.56,.90), frameon=False, fontsize=10)
    ax.grid(axis='x', color='#E5E9EC', linewidth=.7)
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=.23)
    save(fig, '04_baseline_sensitivity', source+'\n2018–19 is the last full pre-UCP fiscal year; 2019–20 already includes UCP tenure.', left=.23, top=.75)

    # Exact-value table determines the signed additive changes; all from one report vintage.
    envelopes = pd.read_csv(ROOT / 'research/capital/actual_recent/recent_envelopes_all_vintages.csv')
    envelopes = envelopes.loc[envelopes.source_vintage == '2024-25']
    pivot = envelopes.pivot(index='envelope', columns='fiscal_year', values='actual_cad_millions')
    totals = pivot.index.str.contains('Total|Fully Consolidated|Core Government', case=False)
    pivot = pivot.loc[~totals]
    if {'2023-24', '2024-25'}.issubset(pivot.columns):
        change = (pivot['2024-25'] - pivot['2023-24']).dropna().sort_values()
        fig, ax = plt.subplots(figsize=(12, 7.6))
        display = {'Agriculture, Natural Resources, and Business Development': 'Agriculture / resources / business',
                   'Schools, universities, colleges, health entities (SUCH) sector – self-financed investment': 'SUCH self-financed investment',
                   'Schools, universities, colleges, health entities (SUCH) sector - self-financed investment': 'SUCH self-financed investment'}
        labels = [display.get(k, k) for k in change.index]
        ax.barh(labels, change, color=[BLUE if v>=0 else ORANGE for v in change])
        for i, v in enumerate(change):
            ax.text(v+(8 if v>=0 else -8), i, f'{v:+,.0f}', va='center',
                    ha='left' if v>=0 else 'right', fontsize=10)
        ax.axvline(0, color=INK, linewidth=1)
        ax.set_title('Municipal and health envelopes drove the latest spending rebound')
        ax.set_xlabel('2024–25 minus reclassified 2023–24 actuals, CAD millions')
        ax.set_xlim(min(-180, change.min()-90), change.max()+120)
        ax.grid(axis='x', color='#E5E9EC', linewidth=.7)
        ax.set_axisbelow(True)
        save(fig, '05_latest_sector_changes', 'Source: Alberta 2024–25 Final Results, p. 17; same-vintage classifications.\nEnvelope changes are financial allocations; they do not establish net capacity. Rounding may affect sums.', left=.38)

    fig, ax = plt.subplots(figsize=(11.8, 6))
    labels = ['Pre-UCP\n2015–16 to 2018–19', 'UCP tenure\n2019–20 to 2024–25',
              'Pre-UCP excluding\n2017–18 spike', 'Recent three years\n2022–23 to 2024–25']
    vals = periods.population_weighted_cpi_adjusted_per_resident_annual_2024_cad
    ax.bar(np.arange(4), vals, color=BLUE, width=.58)
    for i, v in enumerate(vals):
        ax.text(i, v+40, f'${v:,.0f}', ha='center')
    ax.set_xticks(np.arange(4), labels)
    ax.set_title('The tenure-average difference persists when the 2017–18 spike is excluded')
    ax.set_ylabel('Annual capital dollars per resident, 2024 CPI basis')
    ax.set_ylim(0, 2500)
    ax.grid(axis='y', color='#E5E9EC', linewidth=.7)
    ax.set_axisbelow(True)
    save(fig, '06_tenure_sensitivity', source+'\nSum of CPI-adjusted annual spending ÷ sum of annual populations. Descriptive, not a causal estimate.')


def main():
    (ROOT / 'data').mkdir(exist_ok=True)
    data = load_primary()
    comparisons = pd.DataFrame([compare(data, year) for year in [2015, 2018, 2019, 2022, 2023]])
    periods = period_summary(data)
    data.to_csv(ROOT / 'data/capital_population_analysis.csv', index=False)
    comparisons.to_csv(ROOT / 'data/baseline_comparisons.csv', index=False)
    periods.to_csv(ROOT / 'data/tenure_summary.csv', index=False)
    inputs = [ROOT / 'research/capital/latest_vintage_actual_series.csv',
              ROOT / 'research/demography/demography_cpi_2015_2024.csv',
              ROOT / 'research/capital/actual_recent/recent_envelopes_all_vintages.csv',
              ROOT / 'research/capital/early_ucp_paired_ministry_comparisons.csv',
              ROOT / 'research/physical/physical_metrics_evidence.csv',
              ROOT / 'research/physical/health/health_project_evidence.csv',
              ROOT / 'research/physical/round2/project_timeline.csv']
    inputs += [ROOT / 'research/capital/budget_execution_original_vintage.csv',
               ROOT / 'research/capital/capital_composition_original_vintages.csv',
               ROOT / 'research/capital/adjacent_vintage_revision_ledger.csv',
               ROOT / 'research/demography/population_cpi_cross_vintage_ledger.csv',
               ROOT / 'research/demography/cross_vintage_revision_summary.csv',
               ROOT / 'research/source_verification/claim_register.json']
    inputs += [ROOT / 'research/physical/gaploop/project_timeline_audited.csv',
               ROOT / 'research/physical/gaploop/additional_indicators.csv',
               ROOT / 'research/source_verification/corpus_inventory.csv']
    inputs += sorted((ROOT.parent / 'Budget PDFs').glob('*.pdf'))
    manifest = {'analysis_as_of': '2026-10-09', 'source_cutoff': '2025-03-31',
                'years': data.fiscal_year.tolist(), 'input_sha256': {
                    str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in inputs}, 'python': platform.python_version(),
                'versions': {k: importlib.metadata.version(k)
                    for k in ['pandas', 'numpy', 'matplotlib', 'pdfplumber']},
                'causal_inference': False, 'construction_volume_inferred': False,
                'scope_gap': '2025-26 actual spending unavailable in accessible source corpus; no invented observations'}
    (ROOT / 'data/run_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    build_figures(data, comparisons, periods)
    print(comparisons[['baseline', 'endpoint', 'nominal_capital_growth_pct',
                       'cpi_adjusted_per_resident_growth_pct']].to_string(index=False))
    print(f'Validated {len(data)} actual fiscal years; wrote data tables and figures.')


if __name__ == '__main__':
    main()
