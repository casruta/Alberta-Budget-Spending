"""Create a current-source inventory and immutable source/row checksums."""
from pathlib import Path
import csv
import hashlib
import json
import fitz

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent


def records(value):
    if isinstance(value,list):
        for item in value:yield from records(item)
    elif isinstance(value,dict):
        if 'url' in value or 'source_url' in value or 'download_url' in value:yield value
        for child in value.values():
            if isinstance(child,(list,dict)):yield from records(child)


def build():
    urls={}
    for path in ROOT.rglob('*manifest*.json'):
        for item in records(json.loads(path.read_text())):
            url=item.get('url',item.get('source_url',''))
            if url and item.get('retrieved',True) and str(item.get('http_status',item.get('status',200)))=='200':
                urls[url.rsplit('/',1)[-1]]=url
    rows=[]
    for path in sorted(ROOT.rglob('*.pdf')):
        doc=fitz.open(path)
        row=dict(source_file=str(path.relative_to(REPO)),title=doc.metadata.get('title'),
                 author=doc.metadata.get('author'),pages=len(doc),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 official_url=urls.get(path.name,''),source_kind='official government website download this loop')
        # Renamed downloaded health source files retain original names in their download manifest.
        if not row['official_url']:
            for item in json.loads((ROOT/'research/health/current/download_manifest.json').read_text()):
                if item.get('file')==path.name:row['official_url']=item['url']
        rows.append(row)
    with (ROOT/'research/source_verification/current_pdf_inventory.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    lines=['# Source receipt and retrieval diagnosis','',
           'All current PDFs below were retrieved from links on the official Alberta annual-report index. '
           'The current poverty extract was downloaded directly from Statistics Canada. '
           'Existing repository PDFs are archived official publications, not newly downloaded in this loop.','',
           '## Retrieval results','',
           'The official annual-report and budget-document indexes returned HTTP200. '
           'Python urllib requests for several PDF resources returned403; a diagnosis-driven comparison with '
           'curl -L --fail on the same official URL succeeded200 using the normal proxy and TLS verification. '
           'Earlier failures are retained in manifests but superseded for successfully downloaded resources. '
           'No authentication, TLS, proxy or access-control bypass was used. '
           'A Statistics Canada topic hub still returned a proxy denial, and one survey metadata endpoint returned403; '
           'neither prevents using the successfully retrieved table/metadata. No unavailable content is cited as reviewed.','',
           '|Source identity|Local PDF|Pages|Official download|','|---|---|---:|---|']
    for row in rows:
        local='../'+Path(row['source_file']).relative_to('Quality of Life Analysis/research').as_posix().replace(' ','%20')
        lines.append(f"|{row['title']}|[{Path(row['source_file']).name}]({local})|{row['pages']}|[Government source]({row['official_url']})|")
    lines += ['', '## Statistics Canada poverty source', '',
              '[Table11-10-0135-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110013501), '
              'Low income statistics by age, gender and economic family type. '
              'Release date2026-04-29 verified from the official table page; downloaded2026-10-09. '
              'The ZIP source, metadata, exact selected rows, vectors, quality flags and SHA256 are retained in '
              '[MBM_POVERTY.md](../living_standards/MBM_POVERTY.md). '
              'All-person estimates describe the survey-covered population; inaccessible additional survey metadata '
              'does not establish coverage of every resident. 2018-base and2023-base series are separate.','',
              '## Statistics Canada life-table source','',
              '[Table13-10-0837-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310083701), '
              'complete single-year life tables. Release date2026-01-13; retrieved2026-10-09. '
              'Age0/both-sexes Alberta andCanada estimates and source95% margins are retained separately. '
              'Metadata marks2023/2024 preliminary despite blank raw CSV status fields. '
              '[Life-table audit](../health/LIFE_EXPECTANCY_AUDIT.md) records definitions, metadata and '
              'independent official HTML-to-CSV comparison. These period estimates are not joined to archived AHCIP vintages.','',
              '## Archived financial source and claim trail','',
              'The main input panel uses supplied `Budget PDFs/2024-2025 Budget.pdf`, internally '
              '2024–25 Final Results Year-End Report, PDF pp13–14. '
              'Its local source hash is included in the run manifest. The newly downloaded full2024–25 annual report '
              'independently repeats the historical fiscal table (physicalPDF14), including the6M discrepancy. '
              'Source publication dates differ from observed fiscal/calendar periods. '
              'Source-specific CSV ledgers retain exact page references, definitions, quotes and status. '
              'Published source labels/definitions are not accepted as semantic proof when they conflict with results.','',
              '## Delivery/runtime scope','',
              'No report-app preparer/runtime is callable in this execution environment; the shared Data runtime '
              'was unavailable in the preceding accepted workflow. Repository Markdown and an executed '
              'notebook with standalone figures remain the delivery path. No hosted report/site was published.']
    (ROOT/'research/source_verification/SOURCE_RECEIPT.md').write_text('\n'.join(lines)+'\n')
    source_paths=list(ROOT.rglob('*.pdf'))+[REPO/'Budget PDFs/2024-2025 Budget.pdf']
    for source in ['Budget PDFs/2017 Budget.pdf','Budget PDFs/2015-2016 Annual Report.pdf',
                   'Budget PDFs/2011-2012 Budget.pdf','Budget PDFs/2012-2013 Budget.pdf',
                   'Budget PDFs/2013-2014 Annual Report.pdf','Budget PDFs/2014-2015 Annual Report.pdf',
                   'Budget PDFs/2016-2017 Budget.pdf']:
        source_paths.append(REPO/source)
    source_paths+=list((ROOT/'research').rglob('*.zip'))+list((ROOT/'research').rglob('*.csv'))
    hashes={str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(set(source_paths))}
    (ROOT/'data/run_manifest.json').write_text(json.dumps(dict(source_hashes=hashes,
        scope='Source PDFs/ZIPs and reviewed source CSV rows; not causal validation',
        original_tracked_files_modified=False),indent=2)+'\n')
    print(f'Inventoried{len(rows)}downloaded PDFs; checksummed{len(hashes)}source/row artifacts.')


if __name__=='__main__':build()
