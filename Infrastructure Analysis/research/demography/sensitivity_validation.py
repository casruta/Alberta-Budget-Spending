#!/usr/bin/env python3
"""Independent standard-library checks of analysis formulas and rounding bounds."""
import csv, math, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
capital={int(r['calendar_year']):r for r in csv.DictReader((ROOT/'capital/latest_vintage_actual_series.csv').open())}
pop={int(r['calendar_year']):r for r in csv.DictReader((HERE/'demography_cpi_2015_2024.csv').open())}
comparisons=list(csv.DictReader((HERE.parents[1]/'data/baseline_comparisons.csv').open()))
results=[]
for comparison in comparisons:
 b=int(comparison['baseline'][:4]);e=int(comparison['endpoint'][:4])
 B=float(capital[b]['capital_plan_actual_million']);E=float(capital[e]['capital_plan_actual_million'])
 P=float(pop[b]['population_july_1']);Q=float(pop[e]['population_july_1'])
 rates=[float(pop[y]['alberta_annual_cpi_growth_pct']) for y in range(b+1,e+1)]
 factor=math.prod(1+r/100 for r in rates)
 actual=(E/B)/(Q/P)/factor-1
 lo=((E-.5)/(B+.5))/((Q+500)/(P-500))/math.prod(1+(r+.05)/100 for r in rates)-1
 hi=((E+.5)/(B-.5))/((Q-500)/(P+500))/math.prod(1+(r-.05)/100 for r in rates)-1
 assert math.isclose(actual*100,float(comparison['cpi_adjusted_per_resident_growth_pct']),abs_tol=1e-10)
 assert math.isclose(lo*100,float(comparison['rounding_sensitivity_real_per_resident_growth_low_pct']),abs_tol=1e-10)
 assert math.isclose(hi*100,float(comparison['rounding_sensitivity_real_per_resident_growth_high_pct']),abs_tol=1e-10)
 break_even=(E/B)/(Q/P)
 results.append(dict(baseline=b,endpoint=e,nominal_per_person_growth_pct=(break_even-1)*100,break_even_cumulative_construction_inflation_pct=(break_even-1)*100,break_even_annualized_inflation_pct=(break_even**(1/(e-b))-1)*100,cpi_cumulative_growth_pct=(factor-1)*100,cpi_adjusted_per_person_growth_pct=actual*100,rounding_low_pct=lo*100,rounding_high_pct=hi*100,break_even_price_rounding_low_pct=(((E-.5)/(B+.5))/((Q+500)/(P-500))-1)*100,break_even_price_rounding_high_pct=(((E+.5)/(B-.5))/((Q-500)/(P+500))-1)*100,population_growth_factor_for_constant_CPI_adjusted_intensity=(E/B)/factor))
(HERE/'sensitivity_validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
print('All published point estimates and rounding bounds independently reconcile.')
