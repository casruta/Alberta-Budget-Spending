"""Validate actual execution, offline delivery, source integrity and authored links."""
from pathlib import Path
from html.parser import HTMLParser
import base64
import hashlib
import json
import re
import urllib.parse
import nbformat

ROOT=Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self):super().__init__();self.images=[]
    def handle_starttag(self,tag,attrs):
        if tag=='img':self.images.append(dict(attrs))


def validate():
    notebook=nbformat.read(ROOT/'Alberta_Budget_Quality_of_Life.ipynb',as_version=4)
    cells=[cell for cell in notebook.cells if cell.cell_type=='code']
    assert all(cell.execution_count is not None for cell in cells), 'Unexecuted notebook code cells'
    errors=[output for cell in cells for output in cell.outputs if output.output_type=='error']
    assert not errors,errors
    receipts=json.loads((ROOT/'data/figure_receipts.json').read_text())
    assert len(receipts)==12 and len({item['id'] for item in receipts})==12
    report=(ROOT/'REPORT.md').read_text()
    assert '{{' not in report
    authored_images=re.findall(r'!\[([^\]]+)\]\(([^)]+)\)',report)
    assert len(authored_images)==len(receipts)
    broken=[]
    for target in re.findall(r'\]\(([^)]+)\)',report):
        if target.startswith(('https://','http://')):continue
        path=urllib.parse.unquote(target.split('#')[0])
        if not (ROOT/path).exists():broken.append(target)
    assert not broken,broken
    for name,digest in json.loads((ROOT/'data/run_manifest.json').read_text())['source_hashes'].items():
        assert hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()==digest,name
    html=(ROOT/'Alberta_Budget_Quality_of_Life_preview.html').read_text()
    parser=Images();parser.feed(html)
    fig_images=[img for img in parser.images if img.get('alt')]
    for alt,path in authored_images:
        matches=[img for img in fig_images if img.get('alt')==alt]
        assert len(matches)==1,(path,len(matches))
        src=matches[0].get('src','')
        assert src.startswith('data:image/png;base64,'),(path,'PNG not embedded')
        assert base64.b64decode(src.split(',',1)[1])==(ROOT/path).read_bytes(),path
    result=dict(status='passed within reviewed delivery scope',executed_code_cells=len(cells),
                notebook_errors=0,authored_figures=len(receipts),embedded_images_verified=len(receipts),
                source_hashes_verified=len(json.loads((ROOT/'data/run_manifest.json').read_text())['source_hashes']),
                report_links_verified=True,
                limits='Static report/notebook export; no hosted-app/browser interaction or causal validation claimed')
    (ROOT/'review/delivery_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':validate()
