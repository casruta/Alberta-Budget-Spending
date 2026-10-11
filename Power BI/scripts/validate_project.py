"""Offline checks of PBIR schemas, bindings, snapshots and portable archive.

This checks generated files. It does not run Power BI Desktop or its renderer.
"""
from pathlib import Path
import base64,gzip,hashlib,json,re,zipfile
from collections import Counter
from jsonschema import Draft7Validator
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT7

HOME=Path(__file__).resolve().parents[1]
ROOT=HOME.parent
BASE='https://developer.microsoft.com/json-schemas/'


def load(p):return json.loads(p.read_text())


def validate_schemas():
    folder=HOME/'tests/schemas';resources=[];documents={}
    for p in (folder/'fabric').rglob('*.json'):
        data=load(p);uri=BASE+p.relative_to(folder).as_posix();resource=Resource.from_contents(data,default_specification=DRAFT7)
        resources.append((uri,resource));documents[uri]=data
        if data.get('$id') and data['$id']!=uri:resources.append((data['$id'],resource))
    registry=Registry().with_resources(resources)
    files=[HOME/'AlbertaBudget.pbip',HOME/'AlbertaBudget.Report/definition.pbir',HOME/'AlbertaBudget.SemanticModel/definition.pbism']+list((HOME/'AlbertaBudget.Report/definition').rglob('*.json'))
    errors=[]
    for p in files:
        data=load(p)
        schema=load(folder/'pbip-1.0.json') if p.suffix=='.pbip' else documents[data['$schema']]
        validator=Draft7Validator(schema,registry=registry)
        for e in validator.iter_errors(data):errors.append(f'{p.relative_to(HOME)} {list(e.path)}: {e.message}')
    if errors:raise AssertionError('\n'.join(errors))
    return len(files)


def fixed_values(config):
    result={}
    for f in config.get('filters',[]):
        if f.get('filter'):
            assert f['isLockedInViewMode'] and f['isHiddenInViewMode']
            result[f['field']['Column']['Property']]=f['filter']['Where'][0]['Condition']['In']['Values'][0][0]['Literal']['Value'][1:-1].replace("''", "'")
    return result


def validate_bindings():
    facts=load(HOME/'data/chart_data.json');catalog=load(HOME/'data/chart_catalog.json');manifest=load(HOME/'data/project_manifest.json')
    lookup={(c['id'],p['id']):(c,p) for c in catalog for p in c['panels']}
    assert len({(r['ChartId'],r['Panel'],r['Period'],r['Series']) for r in facts})==len(facts)
    pages=HOME/'AlbertaBudget.Report/definition/pages';chart_count=0;seen=[]
    metadata=load(pages/'pages.json');assert len(metadata['pageOrder'])==43
    assert set(metadata['pageOrder'])=={p.parent.name for p in pages.glob('*/page.json')}
    for pageid in metadata['pageOrder']:
        page=load(pages/pageid/'page.json');pfilters=fixed_values(page.get('filterConfig',{}));native=[]
        for vf in (pages/pageid/'visuals').glob('*/visual.json'):
            v=load(vf);pos=v['position'];assert pos['x']>=0 and pos['y']>=0
            assert pos['x']+pos['width']<=page['width'] and pos['y']+pos['height']<=page['height'],vf
            if v['visual']['visualType']=='textbox':continue
            assert v['visual']['visualType'] in ['lineChart','clusteredBarChart','clusteredColumnChart','columnChart']
            filters={**pfilters,**fixed_values(v.get('filterConfig',{}))};scope=(filters['ChartId'],filters['Panel']);c,p=lookup[scope]
            rows=[r for r in facts if (r['ChartId'],r['Panel'])==scope]
            assert rows and {r['Unit'] for r in rows}=={p['unit']}
            values=[r['Value'] for r in rows]
            assert p['minimum'] is None or min(values)>=p['minimum']
            assert p['maximum'] is None or max(values)<=p['maximum']
            roles=v['visual']['query']['queryState']
            assert roles['Category']['projections'][0]['field']['Column']['Property']=='Period'
            assert roles['Series']['projections'][0]['field']['Column']['Property']=='Series'
            assert roles['Y']['projections'][0]['field']['Measure']['Property']=='Chart value'
            native.append(v['name']);seen.append(scope);chart_count+=1
        pairs={(v['source'],v['target']) for v in page['visualInteractions'] if v['type']=='NoFilter'}
        assert pairs=={(a,b) for a in native for b in native if a!=b}
    assert set(seen)==set(lookup)
    assert chart_count==manifest['native_chart_visuals']==71
    return chart_count


def validate_snapshots():
    manifest=load(HOME/'data/project_manifest.json');transform=load(HOME/'data/transformation_manifest.json');source_tables=load(HOME/'data/source_tables.json')
    facts=load(HOME/'data/chart_data.json');catalog=load(HOME/'data/source_catalog.json')
    expected={'ChartData':[[r[k] for k in facts[0]] for r in facts],'SourceCatalog':[[r[k] for k in catalog[0]] for r in catalog]}
    expected.update({t['name']:t['rows'] for t in source_tables})
    for table in manifest['tables']:
        text=(HOME/'AlbertaBudget.SemanticModel/definition/tables'/f"{table['name']}.tmdl").read_text()
        encoded=re.search(r'Binary.FromText\("([A-Za-z0-9+/=]+)"',text).group(1)
        raw=gzip.decompress(base64.b64decode(encoded));assert hashlib.sha256(raw).hexdigest()==table['payload_sha256']
        assert json.loads(raw)==expected[table['name']]
        assert len(expected[table['name']])==table['rows']
        assert not any(word in text for word in ['File.Contents','Web.Contents','Folder.Files','C:\\','/workspace'])
    for path,hashvalue in transform['source_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==hashvalue,path
    for r in catalog:assert hashlib.sha256((ROOT/r['Path']).read_bytes()).hexdigest()==r['SHA256'],r['Path']
    assert len(catalog)==69 and len(source_tables)==66
    assert len(transform['excluded'])==3
    assert all('DRAFT_DO_NOT_USE' not in r['SourcePaths'] for r in facts)
    # One observation is required by the DAX measure: no SUM of incompatible rates.
    dax=(HOME/'AlbertaBudget.SemanticModel/definition/tables/ChartData.tmdl').read_text()
    assert 'IF(COUNTROWS(ChartData) = 1, MAX(ChartData[Value]), BLANK())' in dax
    return len(manifest['tables'])


def validate_native_receipt():
    receipt=load(HOME/'data/native_model_validation.json')
    folder=HOME/'AlbertaBudget.SemanticModel/definition'
    value=''.join(p.relative_to(folder).as_posix()+'\n'+hashlib.sha256(p.read_bytes()).hexdigest()+'\n' for p in sorted(folder.rglob('*.tmdl')))
    assert hashlib.sha256(value.encode()).hexdigest()==receipt['definition_sha256'], 'Native parser receipt is stale; rerun the .NET TMDL check.'
    assert receipt['native_tmdl_parse_passed'] and receipt['source_column_bindings_verified']
    assert receipt['model_tables']==68 and receipt['hidden_evidence_tables']==66
    return receipt['tool']


def validate_archive():
    manifest=load(HOME/'data/project_manifest.json');info=manifest['download'];p=HOME/info['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==info['sha256']
    with zipfile.ZipFile(p) as archive:
        assert archive.testzip() is None
        assert 'AlbertaBudget-PowerBI/AlbertaBudget.pbip' in archive.namelist()
        assert 'AlbertaBudget-PowerBI/README.md' in archive.namelist()
        assert not any(n.endswith('.png') or '/.pbi/' in n or '..' in Path(n).parts for n in archive.namelist())
        for name in archive.namelist():assert archive.read(name)==(HOME/Path(name).relative_to('AlbertaBudget-PowerBI')).read_bytes(),name
    return info['bytes']


def main():
    result={'schema_validated_files':validate_schemas(),'native_chart_bindings':validate_bindings(),'verified_embedded_tables':validate_snapshots(),'portable_zip_bytes':validate_archive(),'native_tmdl_parser':validate_native_receipt(),'desktop_open_and_render':'Not run: Windows Power BI Desktop unavailable in this Linux environment','service_publication':'Not performed: no authenticated Power BI workspace'}
    (HOME/'data/validation_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
