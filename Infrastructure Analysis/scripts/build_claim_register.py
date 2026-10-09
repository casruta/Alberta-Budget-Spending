"""Create a navigable source-page register for consequential report claims.

Anchors locate the reviewed page, not prove the interpretation. Exact extracted
page text and its PDF hash accompany each entry so source judgment is inspectable.
Never fill unavailable physical capacity or remote sources from this register.
"""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import quote
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/source_verification'
LATEST = '2024-2025 Budget.pdf'


def source(file, page, *anchors):
    return {'file': file, 'pdf_page': page, 'anchors': list(anchors)}


# Curated source references. A register entry is not an exhaustive evidence claim.
CLAIMS = [
    ('F01', 'Ten actual capital-plan observations', 'Financial input',
     [source(LATEST, 14, 'Capital Plan', '7,243', 'Numbers are not strictly comparable')],
     'Latest local vintage; historical accounting-policy changes remain.',
     'research/capital/latest_vintage_actual_series.csv'),
    ('F02', 'July population and annual CPI inputs', 'Demographic / price input',
     [source(LATEST, 13, 'Population (July 1, thousands)', '4,889', 'Alberta consumer price index')],
     'Rounded demographic estimates; calendar timing and consumer prices do not measure construction volume.',
     'research/demography/demography_cpi_2015_2024.csv'),
    ('F03', 'Capital grants and investment have different accounting treatment', 'Accounting definition',
     [source(LATEST, 16, 'Capital Investment', 'Capital Grants', 'Statement of Operations')],
     'Grants fund assets outside provincial consolidation; do not add the full Capital Plan to expense.', ''),
    ('F04', 'Latest increase separates grants from investment', 'Financial decomposition',
     [source(LATEST, 3, 'Capital grants', '2,934', '2,103', 'Capital investment', '4,309', '4,197')],
     'Grant growth is not automatically growth in provincially owned assets; neither component is physical capacity.',
     'research/capital/capital_composition_original_vintages.csv'),
    ('F05', 'Municipal and health envelopes drive latest increase', 'Financial decomposition',
     [source(LATEST, 17, 'Municipal Infrastructure Support', '489', 'Protect Quality Health Care', '318')],
     'Separate maintenance / self-finance; component rounding differs from total change by $1M.',
     'research/capital/actual_recent/recent_envelopes_all_vintages.csv'),
    ('F06', 'Latest actual spending is below its budget', 'Budget execution',
     [source(LATEST, 17, '8,299', '7,243', '1,056', 'project cash flows')],
     'Undershoot is not proof of cancellation or permanent loss of funding.',
     'research/capital/budget_execution_original_vintage.csv'),
    ('F07', 'Source pie has an inconsistent SUCH percentage', 'Source discrepancy',
     [source(LATEST, 16, '$744 or 12%'), source(LATEST, 17, '744', '7,243')],
     '744/7243 is about 10.3%; the source percentage is not repeated as a valid share.', ''),
    ('F08', 'Source health-completion counts conflict internally', 'Source discrepancy',
     [source(LATEST, 15, '17 health facility projects'),
      source(LATEST, 20, '2 health facility projects', '17 health facility projects'),
      source(LATEST, 23, 'Rockyview', 'Lethbridge')],
     'Use granular completed/in-progress and named-project evidence; retain the disagreement.', ''),
    ('F09', 'Historical nonfinancial row differs from gross balance-sheet amount', 'Accounting reconciliation',
     [source(LATEST, 12, '62,925', '4,080'), source(LATEST, 14, '58,845')],
     'Subtract spent deferred contributions; this is not a clean physical tangible-asset stock.',
     'review/stock_accounting_check.md'),
    ('F10', 'Capital-asset investment is offset by amortization and other changes', 'Accounting reconciliation',
     [source(LATEST, 11, '$3.9 billion in capital investment', '$2.6 billion in amortization'),
      source(LATEST, 3, 'Capital investment', '4,309')],
     'Book value is not physical capacity. The $4.309B plan flow is not reconciled to the rounded $3.9B asset narrative in this summary; no exact gap or cause is asserted.',
     'research/capital/INVESTMENT_TO_ASSET_ROLLFORWARD_GAP.md'),
    ('F11', 'MSI grants were advanced into the pre-UCP spending peak', 'Timing / policy context',
     [source('2017 Budget.pdf', 23, '$800 million'), source('2018-19 Budget.pdf', 10, '$800 million', '$400 million')],
     'Advanced cash transfers are not construction all delivered in that year.', ''),
    ('F12', '2019 capital-grant total was reclassified into operating expense', 'Accounting revision',
     [source('2020-21 Budget.pdf', 2, '$19 million', 'operating expense')],
     'The reclassification is not an additional $19M infrastructure cut.',
     'research/capital/early_ucp_comparisons.md'),
    ('F13', '2018 ministry attribution changed', 'Accounting revision',
     [source('2018-19 Budget.pdf', 2, 'Infrastructure', 'school boards', 'Alberta Health Services')],
     'A ministry row is not a stable functional-sector series.', ''),
    ('P01', '2024 school spaces mix new and modernized', 'Physical output',
     [source(LATEST, 20, '11,000+', 'new and modernized', '87 school projects')],
     'Completed gross/mixed spaces and the pipeline are distinct; neither is reconciled net seats.', ''),
    ('P02', '2021 school new spaces are separately reported', 'Physical output',
     [source('2021-22 Budget.pdf', 20, '5,000+ new', '5,900+', 'modernized')],
     'Gross new seats cannot be compared with a mixed new/modernized total.', ''),
    ('P03', '2018 supportive-living construction added reported spaces', 'Physical output',
     [source('2018-19 Budget.pdf', 10, '1,177', 'Affordable Supportive Living')],
     'Selected gross long-term-care additions do not reconcile provincial closures or staffing.',
     'research/physical/round2/explicit_capacity_observations.csv'),
    ('P04', 'Grande Prairie hospital has separately completed phases', 'Project stage',
     [source('2020-21 Budget.pdf', 23, 'Grande Prairie', 'Phase 1'),
      source('2021-22 Budget.pdf', 23, 'Grande Prairie', 'Phase 2')],
     'Do not count combined multiyear project funding twice or infer net provincial staffed beds.',
     'research/physical/health/health_project_evidence.csv'),
    ('P05', 'Calgary cancer construction completion differs from anticipated opening', 'Project stage',
     [source('2022-2023 Budget.pdf', 23, 'Calgary Cancer', '2024')],
     'The anticipated public-opening date in this source is not a verified actual opening date.', ''),
    ('P06', 'Misericordia emergency design volume is not observed throughput', 'Design capacity',
     [source('tbf-goa-2023-2024 Budget.pdf', 23, 'Misericordia', '60,000')],
     'Designed visits per year do not establish actual visits, waits or net beds.', ''),
    ('P07', 'High Prairie completed project introduced dialysis stations', 'Physical output',
     [source('2021-22 Budget.pdf', 23, 'High Prairie', 'renal dialysis', 'six stations')],
     'Local gross delivery, not net provincial station growth or treatment volume.', ''),
    ('P08', 'Open recovery communities are distinct from planned beds', 'Operational stock / pipeline',
     [source(LATEST, 15, '200 treatment', '500', 'open in Red Deer, Lethbridge and Gunn')],
     'Do not double-count Gunn; addiction treatment beds are not acute hospital beds.', ''),
    ('P09', 'Bow River westbound bridge expands by one lane', 'Physical output',
     [source(LATEST, 23, '3 lanes to 4 lanes', 'new eastbound bridge')],
     'Local corridor improvement does not supply provincial net lane kilometres.', ''),
    ('P10', 'Road-network stock unit labels differ across reports', 'Source comparability gap',
     [source('tbf-goa-2023-2024 Budget.pdf', 20, 'two lanes equivalent length'),
      source(LATEST, 20, 'lane kilometres')],
     'No network-growth rate is derived from the inconsistent labels.', ''),
    ('P11', 'Springbank reservoir is flood protection', 'Project stage',
     [source(LATEST, 23, 'Completed Projects', 'dry reservoir', 'flood protection')],
     'Construction completion does not establish operational certification or drinking-water capacity.', ''),
    ('P12', 'Housing completions and pipeline are separately stated', 'Physical output / pipeline',
     [source(LATEST, 20, '388 housing units', '617 housing units', '60,000+')],
     'Gross deliveries are not net housing stock after removals, ownership or eligibility changes.', ''),
    ('P13', 'Rural project basket includes transport and water', 'Financial support',
     [source(LATEST, 15, '$236 million', '125 projects', 'Strategic Transportation')],
     'Not 125 water projects or 125 completed projects.', ''),
    ('P14', 'MSI to LGFF program change is a narrow grant comparison', 'Financial support',
     [source('tbf-goa-2023-2024 Budget.pdf', 16, '$487 million'),
      source(LATEST, 15, '$724 million', '53 per cent')],
     'Not all municipal funding or a measure of local asset delivery.', ''),
    ('P15', 'Broadband financial allocation is not connected households', 'Financial input',
     [source(LATEST, 17, '$48 million', 'Broadband Strategy')],
     'Verified connections and service quality are absent from this cited financial row.', ''),
    ('P16', 'Project completion definition changes over time', 'Source comparability gap',
     [source('2021-22 Budget.pdf', 23, 'completed when they are operational'),
      source(LATEST, 23, 'completed when construction has ended')],
     'Reported completed-year series does not consistently measure operational opening.', ''),
    ('P17', 'Older school overview reports separate new and modernized spaces', 'Physical output',
     [source('2017 Budget.pdf', 93, '21,600', '15,000')],
     'Selected September 2017 context; not a reconciled net-seat series or political productivity ratio.',
     'research/physical/gaploop/additional_indicators.csv'),
    ('P18', '2022 source reports gross continuing-care completions', 'Physical output',
     [source('2022-2023 Budget.pdf', 15, '871', 'continuing care')],
     'Broader care scope differs from earlier long-term-care figures; closures and staffing unknown.', ''),
    ('P19', 'Highway 19 source reports a specific twinned route segment', 'Physical output',
     [source('tbf-goa-2023-2024 Budget.pdf', 23, 'Highway 19', '3.5 km')],
     'Route kilometres, not lane kilometres or provincial net-network additions.', ''),
    ('P20', 'Red Deer Justice Centre has reported courtroom capacity', 'Design / facility capacity',
     [source('tbf-goa-2023-2024 Budget.pdf', 23, 'Red Deer Justice Centre', '12 courtrooms')],
     'Gross facility capacity; predecessor courtroom retirements unknown.', ''),
    ('P21', 'Conklin construction describes fifteen housing units', 'Physical output',
     [source(LATEST, 23, 'Conklin', 'five four-', '10 two-and-three-')],
     'Units are not buildings; no provincial net-stock or household-demand conclusion.', ''),
    ('P22', 'Northern Lights supply pipeline has a reported route length', 'Physical output',
     [source('2021-22 Budget.pdf', 23, 'Northern Lights', '100 kilometres')],
     'Local supply-line length, not connected-household or production-capacity count.', ''),
    ('P23', 'Government data centres were consolidated', 'Digital infrastructure change',
     [source('2020-21 Budget.pdf', 23, '37', 'three enterprise')],
     'Fewer centres do not mean lower digital service capacity; observed service outcomes unavailable.', ''),
    ('P24', 'Quest had operating evidence before its later completed-status listing', 'Source comparability gap',
     [source('2016-2017 Budget.pdf', 17, 'first full year of injections'),
      source('2021-22 Budget.pdf', 23, 'Quest')],
     'A completed-status list is not always a list of first completions during the fiscal year.',
     'research/physical/gaploop/completion_year_audit.md'),
    ('F14', 'ARO adoption revised asset book values', 'Accounting policy change',
     [source('2022-2023 Budget.pdf', 2, '$692 million', 'tangible capital assets')],
     'Accounting value revision is not automatically a physical infrastructure addition.', ''),
    ('F15', 'P3 adoption revised opening book values without comparable restatement', 'Accounting policy change',
     [source('tbf-goa-2023-2024 Budget.pdf', 2, '$415 million', 'without restating prior year')],
     'Accounting value revision is not automatically demolished infrastructure.', ''),
    ('P25', 'Lethbridge science replacement has an explicitly dated completion', 'Dated physical delivery',
     [source('2019-20 Budget.pdf', 19, 'Lethbridge', 'Completed January 2020', 'replacing')],
     'Replacement does not quantify net student seats or capacity relative to enrolment.', ''),
]


def normalize(text):
    return re.sub(r'\s+', ' ', text).strip().casefold()


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'pages').mkdir(exist_ok=True)
    records = []
    page_cache = {}
    for claim_id, claim, kind, sources, limit, supporting in CLAIMS:
        locators = []
        for item in sources:
            file, page = item['file'], item['pdf_page']
            key = (file, page)
            path = ROOT.parent/'Budget PDFs'/file
            if key not in page_cache:
                with fitz.open(path) as pdf:
                    text = pdf[page-1].get_text()
                filename = f'{Path(file).stem}__pdf_page_{page}.txt'
                (OUT/'pages'/filename).write_text(text)
                page_cache[key] = (text, filename)
            text, filename = page_cache[key]
            missing = [a for a in item['anchors'] if normalize(a) not in normalize(text)]
            if missing:
                raise ValueError(f'{claim_id}: source locator anchors absent: {missing}')
            locators.append({**item, 'source_path': 'Budget PDFs/'+file,
                'source_pdf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'extracted_page': 'pages/'+filename, 'locator_anchors_present': True})
        records.append({'claim_id': claim_id, 'claim': claim, 'evidence_type': kind,
            'sources': locators, 'interpretation_limit': limit,
            'supporting_artifact': supporting or None,
            'verification_scope': 'Source locator plus reviewed interpretation; anchors alone do not establish the claim.'})
    (OUT/'claim_register.json').write_text(json.dumps(records, indent=2)+'\n')
    lines = ['# Claim-to-source verification register', '',
        'This register makes consequential claims in REPORT.md traceable to local official PDF pages. '
        'It is selective, not a claim that every sentence has been verified automatically. '
        'The links include exact extracted page text and original PDF pages. '
        'Locator anchors only detect a wrong page or changed extraction; arithmetic, definitions and interpretation still require source review.', '',
        'For calculated spending comparisons, consult `data/baseline_comparisons.csv`, the executed notebook and independent Decimal checks in `tests/test_analysis.py`. '
        'Those calculations use F01 and F02; no physical-capacity conclusion follows from them.', '']
    for r in records:
        lines += [f'## {r["claim_id"]}: {r["claim"]}', '', f'**Evidence type:** {r["evidence_type"]}.', '']
        for s in r['sources']:
            pdf_link = '../../../Budget%20PDFs/'+quote(s['file'])+f'#page={s["pdf_page"]}'
            text_link = quote(s['extracted_page'])
            lines.append(f'- [{s["file"]}, PDF p. {s["pdf_page"]}]({pdf_link}) · [extracted page]({text_link})')
        lines += ['', '**Interpretation limit:** '+r['interpretation_limit'], '']
        if r['supporting_artifact']:
            target = '../../'+quote(r['supporting_artifact'])
            lines += [f'[Supporting artifact]({target})', '']
    (OUT/'CLAIM_REGISTER.md').write_text('\n'.join(lines)+'\n')
    print(f'Built {len(records)} claim entries from {len(page_cache)} unique source pages.')


if __name__ == '__main__':
    build()
