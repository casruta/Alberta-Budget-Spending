#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import urllib.request,urllib.error,json,hashlib,concurrent.futures,datetime
H=Path(__file__).resolve().parent
INDEX=H.parent/'source_verification/annual_reports.html'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and d.get('href','').endswith(('scss-annual-report-2024-2025.pdf','jet-annual-report-2024-2025.pdf','au-annual-report-2024-2025.pdf')):self.links.append(d['href'])
p=Links();p.feed(INDEX.read_text())
def fetch(u):
 rec={'url':u,'source_index_file':str(INDEX),'retrieval_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=urllib.request.urlopen(u,timeout=35);data=r.read();rec.update(http_status=r.status,bytes=len(data))
  if data.startswith(b'%PDF'):
   dest=H/u.rsplit('/',1)[-1];dest.write_bytes(data);rec.update(file=dest.name,sha256=hashlib.sha256(data).hexdigest())
  else:rec['error']='response is not a PDF'
 except Exception as e:rec.update(error=type(e).__name__+': '+str(e),http_status=getattr(e,'code',None))
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:out=list(pool.map(fetch,list(dict.fromkeys(p.links))))
(H/'linked_report_download_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
for r in out:print(r['url'].rsplit('/',1)[-1],r.get('http_status'),r.get('bytes'),r.get('error',''))
