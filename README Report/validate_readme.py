"""Validate the combined README against collected data; standard library only."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from datetime import datetime, timezone
import csv
import hashlib
import json
import math
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
text = README.read_text()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def rows(relative):
    with (ROOT / relative).open(newline='') as stream:
        return list(csv.DictReader(stream))

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# GitHub-style anchors for this document's plain-text section headings.
anchors = set()
for title in re.findall(r'^#{1,6} (.+)$', text, re.M):
    anchors.add(re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-'))
links = re.findall(r'!?\[([^\]]*)\]\(([^)]+)\)', text)
local_count = 0
for label, target in links:
    parts = urlsplit(target)
    if parts.scheme or parts.netloc:
        continue
    if parts.path:
        destination = ROOT / unquote(parts.path)
        require(destination.exists(), f'Missing local destination: {target}')
    elif parts.fragment:
        require(unquote(parts.fragment) in anchors, f'Missing README anchor: {target}')
    local_count += 1
images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)
actual_paths = [unquote(path) for _, path in images]
expected_paths = sorted(str(p.relative_to(ROOT)) for folder in (
    'Infrastructure Analysis/plots', 'Quality of Life Analysis/figures',
    '2011-2025 Expense Analysis/plots', '2026-2029 Fiscal Plan/plots'
) for p in (ROOT / folder).glob('*.png'))
require(sorted(actual_paths) == expected_paths, 'Chart inventory is incomplete or duplicated')
require(len(images) == 42, 'Expected 42 analytical figures')
image_details = []
for alt, relative in images:
    relative = unquote(relative)
    require(len(alt.split()) >= 8, f'Insufficient alternative text: {relative}')
    raw = (ROOT / relative).read_bytes()
    require(raw[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG header: {relative}')
    width, height = struct.unpack('>II', raw[16:24])
    require(width >= 800 and height >= 400, f'Undersized image: {relative}')
    image_details.append(dict(path=relative, width=width, height=height, sha256=sha256(ROOT / relative)))

# Independently calculate financial headline changes from nominal input rows.
capital = {int(r['calendar_year']): r for r in rows('Infrastructure Analysis/data/capital_population_analysis.csv')}
a, b = capital[2018], capital[2024]
pop_ratio = float(b['population_july_1']) / float(a['population_july_1'])
cpi_ratio = float(b['cpi_index_2015_100']) / float(a['cpi_index_2015_100'])
nominal_ratio = float(b['capital_plan_actual_million']) / float(a['capital_plan_actual_million'])
values = {
    'population_growth_pct': (pop_ratio - 1) * 100,
    'cpi_growth_pct': (cpi_ratio - 1) * 100,
    'combined_population_price_growth_pct': (pop_ratio * cpi_ratio - 1) * 100,
    'capital_nominal_growth_pct': (nominal_ratio - 1) * 100,
    'capital_adjusted_per_resident_growth_pct': (nominal_ratio / pop_ratio / cpi_ratio - 1) * 100,
}
functional = rows('Quality of Life Analysis/data/functional_expense_intensity.csv')
for function in ['Health', 'Basic and advanced education', 'Social services', 'Other programs', 'Total programs']:
    endpoints = {int(r['calendar_year']): float(r['nominal_million']) for r in functional if r['function'] == function}
    ratio = endpoints[2024] / endpoints[2018]
    values[function + '_nominal_growth_pct'] = (ratio - 1) * 100
    values[function + '_adjusted_per_resident_growth_pct'] = (ratio / pop_ratio / cpi_ratio - 1) * 100
expected = {
    'population_growth_pct': 13.9,
    'cpi_growth_pct': 20.1,
    'combined_population_price_growth_pct': 36.8,
    'capital_nominal_growth_pct': 19.6,
    'capital_adjusted_per_resident_growth_pct': -12.6,
    'Total programs_nominal_growth_pct': 30.9,
    'Total programs_adjusted_per_resident_growth_pct': -4.3,
    'Health_nominal_growth_pct': 34.8,
    'Health_adjusted_per_resident_growth_pct': -1.4,
    'Basic and advanced education_nominal_growth_pct': 15.8,
    'Basic and advanced education_adjusted_per_resident_growth_pct': -15.3,
    'Social services_nominal_growth_pct': 44.2,
    'Social services_adjusted_per_resident_growth_pct': 5.4,
    'Other programs_nominal_growth_pct': 35.8,
    'Other programs_adjusted_per_resident_growth_pct': -0.7,
}
for key, rounded in expected.items():
    require(math.isclose(round(values[key], 1), rounded, abs_tol=1e-9), f'Financial mismatch: {key}')
    require(f'{abs(rounded):.1f}%' in text, f'Missing reported financial value: {key}')
latest_functions = {r['function']: float(r['nominal_million']) for r in functional if int(r['calendar_year']) == 2024}
allocation_rows = {}
for line in text.splitlines():
    if line.startswith('|'):
        cells = [cell.strip().replace('**', '') for cell in line.strip('|').split('|')]
        if len(cells) == 4 and cells[0] in latest_functions:
            require(cells[0] not in allocation_rows, f'Duplicate allocation: {cells[0]}')
            allocation_rows[cells[0]] = cells[1:]
for function in ['Health', 'Basic and advanced education', 'Social services', 'Other programs', 'Total programs']:
    require(function in allocation_rows, f'Missing allocation row: {function}')
    observed = allocation_rows[function]
    expected_row = [f"${latest_functions[function] / 1000:.3f}B"] + [
        f"{values[function + suffix]:+.1f}%".replace('-', '−')
        for suffix in ['_nominal_growth_pct', '_adjusted_per_resident_growth_pct']
    ]
    require(observed == expected_row, f'Allocation amount, sign or growth mismatch for {function}: {observed} vs {expected_row}')
require(math.isclose(sum(latest_functions[k] for k in ['Health', 'Basic and advanced education', 'Social services', 'Other programs']), latest_functions['Total programs']), 'Latest program components do not reconcile')

outcome_checks = 0
poverty = rows('Quality of Life Analysis/research/living_standards/mbm_poverty_all_persons_2015_2024.csv')
for year, reported in [(2022, 10.5), (2023, 10.2), (2024, 11.0)]:
    selected = [r for r in poverty if r['geography'] == 'Alberta' and int(r['calendar_year']) == year and r['mbm_base'] == 'Market basket measure, 2023 base']
    require(len(selected) == 1 and float(selected[0]['poverty_rate_pct']) == reported, f'Poverty source mismatch: {year}')
    require(f'{reported:.1f}%' in text, f'Missing poverty observation: {year}')
    outcome_checks += 1
safety = rows('Quality of Life Analysis/research/source_verification/safety_outcomes_2019_2023.csv')
for metric, year, reported in [('violent_crime', 2019, 1462), ('violent_crime', 2023, 1591), ('property_crime', 2019, 5894), ('property_crime', 2023, 4752)]:
    selected = [r for r in safety if r['metric'] == metric and r['geography'] == 'Alberta' and int(r['calendar_year']) == year]
    require(len(selected) == 1 and float(selected[0]['value']) == reported, f'Safety source mismatch: {metric}/{year}')
    require(f'{reported:,}' in text, f'Missing safety observation: {metric}/{year}')
    outcome_checks += 1

preserved = 0
for folder, filename, key in [
    ('Infrastructure Analysis', 'review/second_loop_artifact_hashes.json', 'artifact_sha256'),
    ('Quality of Life Analysis', 'review/final_artifact_hashes.json', None),
]:
    manifest = json.loads((ROOT / folder / filename).read_text())
    hashes = manifest[key] if key else manifest
    for relative, recorded in hashes.items():
        require(sha256(ROOT / folder / relative) == recorded, f'Previously reviewed artifact changed: {folder}/{relative}')
        preserved += 1
result = {
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'readme_sha256': sha256(README),
    'local_destinations_checked': local_count,
    'analytical_figures': len(images),
    'main_figures': 21,
    'archive_figures': 21,
    'headline_financial_comparisons_checked': len(expected),
    'outcome_source_observations_checked': outcome_checks,
    'prior_reviewed_artifacts_preserved': preserved,
    'calculated_financial_values': values,
    'images': image_details,
    'status': 'passed',
    'limitations': 'Archive numerical claims were not newly source-audited; native GitHub browser rendering was not tested.',
}
(ROOT / 'README Report/validation_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(f"PASS: {local_count} local links/anchors; {len(images)} charts; {len(expected)} financial comparisons; {outcome_checks} outcome observations; {preserved} prior artifacts preserved.")
