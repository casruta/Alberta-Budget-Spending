"""Extract reviewed rows from government PDFs actually downloaded this session.

Offline rebuild only: source URLs and retrieval results live in download_manifest.json.
Never replace an unavailable observation with zero or read chart labels as exact data.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def page_text(path, page):
    text = subprocess.check_output(
        ['pdftotext', '-f', str(page), '-l', str(page), '-layout', str(path), '-'], text=True
    )
    (ROOT / f'{path.stem}_pdf_page{page}.txt').write_text(text)
    return text


def write_csv(name, rows):
    with (ROOT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def extract():
    safety = ROOT / 'downloads/pses-annual-report-2024-2025.pdf'
    mental = ROOT / 'downloads/mha-annual-report-2024-2025.pdf'
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [safety, mental]}
    safety_text = page_text(safety, 28)
    method = page_text(safety, 44)
    assert 'Historical' in method and 'revised annually' in method
    rows = []
    lines = safety_text.splitlines()
    labels = [('Alberta Violent Crime Rate', 'violent_crime', 'Alberta'),
              ('Alberta Property Crime Rate', 'property_crime', 'Alberta')]
    for label, metric, geo in labels:
        idx = next(i for i, line in enumerate(lines) if label in line)
        for delta, geography in [(0, geo), (2, 'Rural Alberta'), (4, 'Urban Alberta')]:
            # Blank-line spacing is checked by the reviewed row label, not trusted implicitly.
            candidates = [line for line in lines[idx:] if line.strip()]
            selected = candidates[delta // 2]
            expected = label if delta == 0 else ('Rural' if delta == 2 else 'Urban')
            assert selected.strip().startswith(expected), (expected, selected)
            values = re.findall(r'\d[\d,]*', selected)
            assert len(values) == 5, selected
            for year, value in zip(range(2019, 2024), values):
                rows.append(dict(metric=metric, geography=geography, calendar_year=year,
                                 value=int(value.replace(',', '')), unit='police-reported incidents per 100,000 residents',
                                 source_file=str(safety.relative_to(ROOT.parent.parent.parent)),
                                 source_pdf_page=28, source_printed_page=26,
                                 source_quote=selected.strip(), source_vintage='2024-25 annual report; data available July 2024',
                                 status='reported actual; historical results revised',
                                 caveat='Calendar-year data end in 2023; police reporting is not all victimization; rural/urban rates have separate denominators.'))
    write_csv('safety_outcomes_2019_2023.csv', rows)
    mental_text = page_text(mental, 35)
    page_text(mental, 36)
    page_text(mental, 37)
    page_text(mental, 28)
    page_text(mental, 46)
    line = next(line for line in mental_text.splitlines() if '20.7%' in line and '19.7%' in line)
    values = [float(x) for x in re.findall(r'(\d+\.\d+)%', line)]
    assert len(values) == 6 and values[-2:] == [17.9, 19.7], values
    rows = [dict(metric='First mental-health/addiction ED visit with no publicly funded service interaction in previous two fiscal years',
                 fiscal_year=f'{year}-{str(year+1)[-2:]}', value=value, unit='percent',
                 source_file=str(mental.relative_to(ROOT.parent.parent.parent)), source_pdf_page=35,
                 source_printed_page=33, source_quote=line.strip(),
                 status='reported actual; up to ten-month lag', target=17.9 if year == 2023 else '',
                 target_period='2023-24' if year == 2023 else '',
                 caveat='First visit per person/fiscal year; excludes invalid/missing PHN and less than two years AHCIP eligibility. Lower is preferred by source; measures prior contact, not recovery.')
            for year, value in zip(range(2019, 2024), values[:4] + [values[-1]])]
    write_csv('mental_health_access_2019_2023.csv', rows)
    (ROOT / 'safety_mental_source_hashes.json').write_text(json.dumps(source_hashes, indent=2)+'\n')
    print(f'Extracted 30 crime-rate observations and {len(rows)} mental-health access observations.')


if __name__ == '__main__':
    extract()
