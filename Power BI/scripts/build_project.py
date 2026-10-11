"""Build a portable Power BI Desktop project from the reviewed chart snapshot.

Run transform_data.py first. No Desktop cache, network connection, credentials,
custom visual, absolute filesystem path, or PNG placeholder is required.
"""
from pathlib import Path
import base64, gzip, hashlib, json, shutil, uuid, zipfile

HOME = Path(__file__).resolve().parents[1]
DATA = HOME / 'data'
REPORT = HOME / 'AlbertaBudget.Report'
MODEL = HOME / 'AlbertaBudget.SemanticModel'
BASE = 'https://developer.microsoft.com/json-schemas/fabric/item/'
NAMESPACE = uuid.UUID('e0b05030-993f-4ef7-b092-ceb43e8ca847')


def identifier(value):
    return uuid.uuid5(NAMESPACE, value).hex[:20]


def lineage(value):
    return str(uuid.uuid5(NAMESPACE, value))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def quoted(value):
    return "'"+value.replace("'", "''")+"'"


def m_text(value):
    return '"'+value.replace('"', '""').replace('\n', '#(lf)').replace('\r', '#(cr)').replace('\t', '#(tab)')+'"'


def embedded_table(name, columns, rows, types, hidden=False, description=''):
    # Use one reproducible compressed array, decoded by native Power Query.
    raw=json.dumps(rows, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')
    encoded=base64.b64encode(gzip.compress(raw, mtime=0)).decode('ascii')
    lines=([f'/// {description.replace(chr(10), chr(32))}'] if description else [])+[f'table {quoted(name)}']
    if hidden:lines.append('\tisHidden')
    lines += [f'\tlineageTag: {lineage(name)}']
    if name=='ChartData':
        lines += ['', "\tmeasure 'Chart value' = IF(COUNTROWS(ChartData) = 1, MAX(ChartData[Value]), BLANK())", '\t\tformatString: #,0.00', f'\t\tlineageTag: {lineage(name+".Chart value")}']
        lines += ["\t\tformatStringDefinition = SWITCH(SELECTEDVALUE(ChartData[Unit]), \"Fiscal-start year\", \"0\", \"Incidents per 100,000\", \"#,0\", \"Units + households\", \"#,0\", \"CAD millions\", \"#,0\", \"CAD per resident\", \"#,0\", \"2024 CAD per resident\", \"#,0\", \"CAD per week\", \"#,0\", \"#,0.00\")"]
        for field in ['Unit','ObservationKind','Status','SourceRows','Transformation']:
            lines += ['',f'\tmeasure {quoted("Point "+field)} = SELECTEDVALUE(ChartData[{field}])', f'\t\tlineageTag: {lineage(name+".Point "+field)}']
    for column, dtype in zip(columns, types):
        lines += ['', f'\tcolumn {quoted(column)}', f'\t\tdataType: {dtype}', f'\t\tlineageTag: {lineage(name+"."+column)}', '\t\tsummarizeBy: none', f'\t\tsourceColumn: {column}']
        if dtype=='double':lines += ['\t\tformatString: #,0.00']
        if dtype=='int64':lines += ['\t\tformatString: 0']
    mtypes={'string':'type text','double':'type number','int64':'Int64.Type','boolean':'type logical'}
    cast=', '.join('{'+m_text(c)+', '+mtypes[t]+'}' for c,t in zip(columns,types))
    names=', '.join(m_text(c) for c in columns)
    lines += ['', f'\tpartition {quoted(name)} = m', '\t\tmode: import', '\t\tsource =', '\t\t\tlet', f'\t\t\t\tRows = Json.Document(Binary.Decompress(Binary.FromText("{encoded}", BinaryEncoding.Base64), Compression.GZip)),', f'\t\t\t\tSource = Table.FromRows(Rows, {{{names}}}),', f'\t\t\t\tTyped = Table.TransformColumnTypes(Source, {{{cast}}}, "en-US")', '\t\t\tin', '\t\t\t\tTyped', '']
    path=MODEL/'definition/tables'/f'{name}.tmdl'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('\n'.join(lines),encoding='utf-8')
    return {'name':name,'rows':len(rows),'columns':columns,'types':types,'payload_sha256':hashlib.sha256(raw).hexdigest(),'hidden':hidden}


def build_model():
    definitions=[]
    facts=json.loads((DATA/'chart_data.json').read_text());columns=list(facts[0])
    definitions.append(embedded_table('ChartData',columns,[[r[c] for c in columns] for r in facts],['double' if c=='Value' else 'string' for c in columns],description='One source-backed observation per ChartId, Panel, Period and Series. No relationships to duplicated source evidence.'))
    catalog=json.loads((DATA/'source_catalog.json').read_text());columns=list(catalog[0])
    definitions.append(embedded_table('SourceCatalog',columns,[[r[c] for c in columns] for r in catalog],['int64' if c in ['Rows','Columns'] else 'string' for c in columns],description='All original CSVs, hashes, inclusion status and corresponding hidden evidence tables.'))
    for table in json.loads((DATA/'source_tables.json').read_text()):
        # Preserve the source cells verbatim: do not guess dates, identifiers or suppression codes.
        definitions.append(embedded_table(table['name'],table['columns'],table['rows'],['string']*len(table['columns']),True,table['path']))
    write_json(MODEL/'definition.pbism',{'$schema':BASE+'semanticModel/definitionProperties/1.0.0/schema.json','version':'4.0','settings':{'qnaEnabled':False}})
    (MODEL/'definition/database.tmdl').write_text('database\n\tcompatibilityLevel: 1601\n')
    model='model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\nannotation PBI_QueryOrder = '+json.dumps([t['name'] for t in definitions])+'\n\nannotation __PBI_TimeIntelligenceEnabled = 0\n\n'
    model += '\n'.join('ref table '+quoted(t['name']) for t in definitions)+'\n'
    (MODEL/'definition/model.tmdl').write_text(model)
    return definitions


def column(field, alias=None):
    return {'Column':{'Expression':{'SourceRef':{'Source':alias} if alias else {'Entity':'ChartData'}},'Property':field}}


def measure(field):
    return {'Measure':{'Expression':{'SourceRef':{'Entity':'ChartData'}},'Property':field}}


def literal(value):
    if isinstance(value,bool):value='true' if value else 'false'
    elif isinstance(value,(int,float)):value=str(value)+'D'
    else:value=quoted(str(value))
    return {'expr':{'Literal':{'Value':value}}}


def fixed_filters(scope, values):
    filters=[]
    for field,value in values.items():
        condition={'In':{'Expressions':[column(field,'c')],
                         'Values':[[{'Literal':{'Value':quoted(value)}}]]}}
        filters.append({'name':identifier(scope+field),'field':column(field),
                        'type':'Categorical',
                        'filter':{'Version':2,'From':[{'Name':'c','Entity':'ChartData','Type':0}],
                                  'Where':[{'Condition':condition}]},
                        'howCreated':'User','isLockedInViewMode':True,
                        'isHiddenInViewMode':True})
    return {'filters':filters}


def textbox(page,key,text,x,y,w,h,size=12,bold=False,color='#263747'):
    name=identifier(page+key)
    return {'$schema':BASE+'report/definition/visualContainer/2.4.0/schema.json','name':name,'position':{'x':x,'y':y,'width':w,'height':h,'z':0,'tabOrder':0},'visual':{'visualType':'textbox','objects':{'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':text,'textStyle':{'fontFamily':'Segoe UI Semibold' if bold else 'Segoe UI','fontSize':str(size)+'pt','color':color}}]}]}}]}}}


def native_chart(page,c,p,rect,include_chart_filter=False):
    name=identifier(page+p['id']+c['id']);x,y,w,h=rect
    roles={}
    for role,field,expr in [('Category','Period',column('Period')),('Series','Series',column('Series')),('Y','Chart value',measure('Chart value'))]:
        projection={'field':expr,'queryRef':'ChartData.'+field}
        if role=='Category':projection['active']=True
        roles[role]={'projections':[projection]}
    roles['Tooltips']={'projections':[{'field':measure('Point '+field),'queryRef':'ChartData.Point '+field} for field in ['Unit','ObservationKind','Status','SourceRows','Transformation']]}
    filters={'Panel':p['id']}
    if include_chart_filter:filters['ChartId']=c['id']
    axis={'showAxisTitle':literal(True),'axisTitle':literal(p['unit']),'labelDisplayUnits':literal(1),'fontSize':literal(11)}
    if p['minimum'] is not None:axis['start']=literal(p['minimum'])
    if p['maximum'] is not None:axis['end']=literal(p['maximum'])
    return {'$schema':BASE+'report/definition/visualContainer/2.4.0/schema.json','name':name,'position':{'x':x,'y':y,'width':w,'height':h,'z':1,'tabOrder':1},'filterConfig':fixed_filters(name,filters),'visual':{'visualType':p['visual_type'],'query':{'queryState':roles,'sortDefinition':{'sort':[{'field':column('Period'),'direction':'Ascending'}],'isDefaultSort':False}},'objects':{'legend':[{'properties':{'show':literal(True),'showTitle':literal(False),'position':literal('Bottom'),'fontSize':literal(11)}}],'valueAxis':[{'properties':axis}],'categoryAxis':[{'properties':{'showAxisTitle':literal(False),'fontSize':literal(11)}}],'labels':[{'properties':{'show':literal(False)}}]},'visualContainerObjects':{'title':[{'properties':{'show':literal(True),'text':literal(p['title']+' · '+p['unit']),'fontSize':literal(14),'titleWrap':literal(True)}}]}}}


def no_interactions(visuals):
    names=[v['name'] for v in visuals if v['visual']['visualType']!='textbox']
    return [{'source':a,'target':b,'type':'NoFilter'} for a in names for b in names if a!=b]


def save_page(page,visuals):
    page['visualInteractions']=no_interactions(visuals)
    folder=REPORT/'definition/pages'/page['name']
    write_json(folder/'page.json',page)
    for visual in visuals:write_json(folder/'visuals'/visual['name']/'visual.json',visual)


def build_report():
    charts=json.loads((DATA/'chart_catalog.json').read_text());facts=json.loads((DATA/'chart_data.json').read_text());pages=[];binding=[]
    overview=identifier('overview');pages.append(overview)
    page={'$schema':BASE+'report/definition/page/2.0.0/schema.json','name':overview,'displayName':'00 Findings at a glance','displayOption':'FitToPage','width':1320,'height':980}
    visuals=[textbox(overview,'title',"Alberta’s budget: more dollars, uneven results",24,12,1272,54,27,True),textbox(overview,'intro','Reviewed actuals: program expense +30.9%, capital +19.6%; CPI-adjusted per resident −4.3% and −12.6% since 2018–19. Outcomes have different reporting windows.',24,70,1272,74,14)]
    selections=[('qol_02_allocation_change','p1'),('infra_02_spending_per_resident','p1'),('qol_08_emergency_and_imaging','p1'),('qol_09_surgery_and_ems','p1')]
    for n,(cid,pid) in enumerate(selections):
        c=next(c for c in charts if c['id']==cid);p=next(p for p in c['panels'] if p['id']==pid)
        rect=(24+(n%2)*648,152+(n//2)*356,624,340)
        v=native_chart(overview,c,p,rect,True);visuals.append(v);binding.append({'page':overview,'visual':v['name'],'chart':cid,'panel':pid})
    visuals.append(textbox(overview,'foot','Start here; use the page tabs for all 42 chart topics. Spending intensity is not service quality or causal attribution. Different units and periods stay in separate panels. Hover for evidence; use Filters to explore a selected visual.',24,870,1272,90,12))
    save_page(page,visuals)
    prefix={'Spending':'Budget','Living standards':'Living','Safety':'Safety','Education':'Education','Health':'Health','Housing':'Housing','Infrastructure':'Capital','Archive expenses':'Archive history','Archive Fiscal Plan':'Archive plan'}
    for n,c in enumerate(charts,1):
        pageid=identifier(c['id']);pages.append(pageid);count=len(c['panels'])
        dense_bar=any(p['visual_type']=='clusteredBarChart' and len({r['Period'] for r in facts if r['ChartId']==c['id'] and r['Panel']==p['id']})>14 for p in c['panels'])
        if dense_bar and count>1:height=1940;rects=[(24,124+j*842,1272,818) for j in range(count)]
        elif count==3:height=1440;rects=[(24,124+j*386,1272,370) for j in range(count)]
        elif count==2:height=900;rects=[(24+j*648,124,624,572) for j in range(count)]
        else:height=1000 if dense_bar else 900;rects=[(24,124,1272,height-314)]
        label=prefix.get(c['section'],c['section'])
        page={'$schema':BASE+'report/definition/page/2.0.0/schema.json','name':pageid,'displayName':f'{n:02d} {label} | '+c['title'].replace('Archive Fiscal Plan: ','').replace('Archive: ','')[:54],'displayOption':'FitToWidth' if height>1000 else 'FitToPage','width':1320,'height':height,'filterConfig':fixed_filters(pageid,{'ChartId':c['id']})}
        visuals=[textbox(pageid,'title',c['title'],24,12,1272,58,25,True),textbox(pageid,'scope',c['classification']+' · '+c['section']+' · '+str(n)+' / 42 chart topics',24,76,1272,38,12)]
        for p,rect in zip(c['panels'],rects):
            v=native_chart(pageid,c,p,rect);visuals.append(v);binding.append({'page':pageid,'visual':v['name'],'chart':c['id'],'panel':p['id']})
        caption=c['note']+'\nEvidence: hover over points for source CSV rows and transformations. Reviewed findings and PDF citations remain in the repository report.'
        footer_y=max(y+h for x,y,w,h in rects)+18
        page['height']=max(height,footer_y+174)
        visuals.append(textbox(pageid,'note',caption,24,footer_y,1272,150,12))
        save_page(page,visuals)
    write_json(REPORT/'definition.pbir',{'$schema':BASE+'report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../AlbertaBudget.SemanticModel'}}})
    write_json(REPORT/'definition/version.json',{'$schema':BASE+'report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
    write_json(REPORT/'definition/pages/pages.json',{'$schema':BASE+'report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':pages,'activePageName':overview})
    theme={'name':'Alberta Evidence','dataColors':['#176B87','#AC4949','#558353','#B98223','#775D99','#537B87','#8B6558','#596574'],'background':'#FFFFFF','foreground':'#263747','tableAccent':'#176B87','textClasses':{'label':{'fontFace':'Segoe UI','fontSize':11},'title':{'fontFace':'Segoe UI Semibold','fontSize':18}}}
    write_json(REPORT/'StaticResources/RegisteredResources/AlbertaEvidence.json',theme)
    write_json(REPORT/'definition/report.json',{'$schema':BASE+'report/definition/report/3.0.0/schema.json','themeCollection':{'customTheme':{'name':'AlbertaEvidence','reportVersionAtImport':{'visual':'2.4.0','page':'2.0.0','report':'3.0.0'},'type':'RegisteredResources'}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'AlbertaEvidence','path':'AlbertaEvidence.json','type':'CustomTheme'}]}],'settings':{'useDefaultAggregateDisplayName':True}})
    return binding,pages


def package():
    target=HOME/'downloads/AlbertaBudget-PowerBI.zip';target.parent.mkdir(exist_ok=True)
    files=[HOME/'AlbertaBudget.pbip',HOME/'README.md']
    for folder in [REPORT,MODEL]:files.extend(p for p in sorted(folder.rglob('*')) if p.is_file() and '.pbi' not in p.parts)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for p in files:
            entry=zipfile.ZipInfo('AlbertaBudget-PowerBI/'+p.relative_to(HOME).as_posix(),date_time=(2026,10,11,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o644<<16
            archive.writestr(entry,p.read_bytes())
    return {'path':target.relative_to(HOME).as_posix(),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}


def main():
    for folder in [REPORT/'definition',REPORT/'StaticResources',MODEL/'definition']:
        if folder.exists():shutil.rmtree(folder)
    write_json(HOME/'AlbertaBudget.pbip',{'version':'1.0','artifacts':[{'report':{'path':'AlbertaBudget.Report'}}],'settings':{'enableAutoRecovery':True}})
    tables=build_model();bindings,pages=build_report()
    manifest={'format':'Power BI Desktop PBIP / PBIR / TMDL import model','tables':tables,'pages':len(pages),'chart_topics':42,'native_chart_visuals':len(bindings),'bindings':bindings,'desktop_render_verified':False,'service_published':False,'external_connections':0,'snapshot':'Repository evidence reviewed 2026-10-09; project generated 2026-10-11'}
    if (HOME/'README.md').exists():manifest['download']=package()
    write_json(DATA/'project_manifest.json',manifest)
    print(f'Built {len(pages)} pages, {len(bindings)} native charts, {len(tables)} embedded tables. Desktop open/render pending Windows verification.')


if __name__=='__main__':main()
