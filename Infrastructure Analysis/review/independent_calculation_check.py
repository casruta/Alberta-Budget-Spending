from math import prod
from pathlib import Path
import csv,json
# Independent manual transcription from PDF pp13-14, inspected using pdfplumber.
years=list(range(2015,2025)); cap=[6558,6578,9021,6057,5545,6896,6622,5633,6300,7243]; pop=[4150,4195,4237,4293,4355,4407,4432,4511,4685,4889]; growth=[1.1,1.1,1.6,2.4,1.8,1.1,3.2,6.4,3.3,2.9]
real=[cap[i]*1000/pop[i]*prod(1+g/100 for g in growth[i+1:]) for i in range(10)]
root=Path('/workspace/Alberta-Budget-Spending/Infrastructure Analysis')
a=list(csv.DictReader((root/'data/capital_population_analysis.csv').open())); comparisons=list(csv.DictReader((root/'data/baseline_comparisons.csv').open())); tenure=list(csv.DictReader((root/'data/tenure_summary.csv').open()))
assert all(abs(real[i]-float(a[i]['capital_cpi_adjusted_per_resident_2024_cad']))<1e-8 for i in range(10))
for year in [2015,2018,2019]:
 i=year-2015; inflation=prod(1+g/100 for g in growth[i+1:]); value=(cap[-1]/cap[i]/(pop[-1]/pop[i])/inflation-1)*100
 row=next(r for r in comparisons if r['baseline']==f'{year}-{str(year+1)[-2:]}'); assert abs(value-float(row['cpi_adjusted_per_resident_growth_pct']))<1e-9
 print(year,{'nominal_pct':(cap[-1]/cap[i]-1)*100,'population_pct':(pop[-1]/pop[i]-1)*100,'inflation_pct':(inflation-1)*100,'real_per_person_pct':value})
weights=[]
for j,indices in enumerate([list(range(4)),list(range(4,10)),[0,1,3],list(range(7,10))]):
 weighted=sum(real[i]*pop[i] for i in indices)/sum(pop[i] for i in indices); assert abs(weighted-float(tenure[j]['population_weighted_cpi_adjusted_per_resident_annual_2024_cad']))<1e-8; weights.append(weighted); print('period',j,weighted)
print('UCP_vs_pre_pct',(weights[1]/weights[0]-1)*100,'UCP_vs_spike_excluded_pct',(weights[1]/weights[2]-1)*100)
print('All numerical assertions passed')
