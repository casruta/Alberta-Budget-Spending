"""Independent checks of the additional evidence and temporal semantics."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote
import pandas as pd
import pdfplumber
import pytest

ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
    ('2015-16','2015-2016 Annual Report.pdf',10),
    ('2016-17','2016-2017 Budget.pdf',12),
    ('2017-18','2017 Budget.pdf',12),
    ('2018-19','2018-19 Budget.pdf',3),
    ('2019-20','2019-20 Budget.pdf',3),
    ('2020-21','2020-21 Budget.pdf',3),
    ('2021-22','2021-22 Budget.pdf',3),
    ('2022-23','2022-2023 Budget.pdf',3),
    ('2023-24','tbf-goa-2023-2024 Budget.pdf',3),
    ('2024-25','2024-2025 Budget.pdf',3),
]


def large_numbers(line):
    # All first three consolidated capital totals are four-digit $M amounts.
    return [int(re.sub(r'[\s,]','',n)) for n in re.findall(r'\d\s*,\s*\d{3}',line)]


@pytest.mark.parametrize('year,file,page',SOURCES)
def test_execution_columns_against_independent_pdf_text(year,file,page):
    # Extraction production code uses PyMuPDF's line-oriented cells. This test
    # independently reads horizontally assembled pdfplumber source rows.
    with pdfplumber.open(ROOT.parent/'Budget PDFs'/file) as pdf:
        text=pdf.pages[page-1].extract_text()
        title=pdf.metadata.get('Title','')
    # Filenames are misleading in this repository. Check internal identity and
    # the observed fiscal header, rather than treating the filename as evidence.
    assert str(int(year[:4])) in title
    normalized_period=re.sub(r'\s+','',text.replace('\u2013','-').replace('\u2014','-'))
    assert year in normalized_period
    assert 'Actual' in text and 'Budget' in text
    # Some PDF rows join their numeric row label directly to "Total". Restrict
    # to the actual capital section so narrative references cannot match instead.
    block=text.split('CAPITAL PLAN',1)[1]
    line=next(s for s in block.splitlines() if 'Total Capital Plan' in s)
    budget,actual,prior=large_numbers(line)[:3]
    rows=pd.read_csv(ROOT/'research/capital/budget_execution_original_vintage.csv')
    row=rows.loc[rows.fiscal_year.eq(year)].iloc[0]
    assert row.budget_million==budget
    assert row.contemporary_actual_million==actual
    assert row.budget_execution_pct==pytest.approx(actual/budget*100)
    assert row.actual_minus_budget_million==actual-budget
    assert row.source_file=='Budget PDFs/'+file and row.pdf_page==page
    # Prior-year observation must retain its year rather than join on report year.
    c=pd.read_csv(ROOT/'research/capital/capital_composition_original_vintages.csv')
    previous=c.loc[c.source_vintage.eq(year)&c.column_status.eq('prior_actual')].iloc[0]
    start=int(year[:4])-1
    assert previous.observation_fiscal_year==f'{start}-{str(start+1)[-2:]}'
    assert previous.total_capital_plan_million==prior


def test_latest_grant_investment_decomposition_from_source():
    with pdfplumber.open(ROOT.parent/'Budget PDFs/2024-2025 Budget.pdf') as pdf:
        text=pdf.pages[2].extract_text().split('CAPITAL PLAN',1)[1]
    lines=text.splitlines()
    grant=large_numbers(next(s for s in lines if 'Capital grants' in s))[:3]
    investment=large_numbers(next(s for s in lines if 'Capital investment' in s))[:3]
    total=large_numbers(next(s for s in lines if 'Total Capital Plan' in s))[:3]
    assert grant==[3469,2934,2103]
    assert investment==[4830,4309,4197]
    assert total==[8299,7243,6300]
    dg,di,dt=grant[1]-grant[2],investment[1]-investment[2],total[1]-total[2]
    assert (dg,di,dt)==(831,112,943)
    assert dg+di==dt
    assert round(dg/dt*100,1)==88.1


def test_financial_revisions_remain_separate_from_execution_and_component_rounding():
    revisions=pd.read_csv(ROOT/'research/capital/adjacent_vintage_revision_ledger.csv')
    assert len(revisions)==9 and revisions.fiscal_year_revised.nunique()==9
    assert revisions.set_index('fiscal_year_revised').loc['2018-19','investment_revision_million']==-123
    assert revisions.set_index('fiscal_year_revised').loc['2022-23','grant_revision_million']==-11
    # A one-million component residual is allowed, rather than forced away.
    residual=revisions.total_revision_million-revisions.grant_revision_million-revisions.investment_revision_million
    assert residual.abs().max()<=1
    assert residual.loc[revisions.fiscal_year_revised.eq('2019-20')].iloc[0]==-1


def test_audited_project_status_years_do_not_impute_completion_or_opening():
    timeline=pd.read_csv(ROOT/'research/physical/gaploop/project_timeline_audited.csv')
    assert len(timeline)==17 and timeline.project.nunique()==17
    assert timeline.first_reported_completed_status_fy.notna().all()
    assert timeline.explicit_construction_completion_fy.notna().sum()==4
    assert timeline.operational_year_if_verified.notna().sum()==1
    known=timeline.loc[timeline.operational_year_if_verified.notna()].iloc[0]
    assert known.project=='Edmonton Anthony Henday Drive ring road'
    assert known.operational_year_if_verified==2016
    assert not timeline.operational_year_if_verified.dropna().eq(0).any()


def test_claim_register_links_original_pages_and_limits_automated_verdicts():
    records=json.loads((ROOT/'research/source_verification/claim_register.json').read_text())
    assert len(records)>=39
    assert len({r['claim_id'] for r in records})==len(records)
    for record in records:
        assert record['interpretation_limit']
        assert 'anchors alone do not establish the claim' in record['verification_scope']
        for source in record['sources']:
            path=ROOT.parent/source['source_path']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==source['source_pdf_sha256']
            excerpt=(ROOT/'research/source_verification'/source['extracted_page']).read_text()
            normalized=re.sub(r'\s+',' ',excerpt).casefold()
            for anchor in source['anchors']:
                assert re.sub(r'\s+',' ',anchor).casefold() in normalized
    register=ROOT/'research/source_verification/CLAIM_REGISTER.md'
    for target in re.findall(r'\]\(([^)]+)\)',register.read_text()):
        assert (register.parent/unquote(target.split('#')[0])).exists(),target
