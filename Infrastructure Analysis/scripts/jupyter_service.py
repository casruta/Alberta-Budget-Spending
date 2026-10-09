"""Token-authenticated local Jupyter startup and functional readiness checks.

Never prints the token or emits a localhost preview URL. Processes are not part
of an environment snapshot; use start when an interactive editor is needed.
"""
from pathlib import Path
import argparse
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error
import uuid
from datetime import datetime,timezone

ANALYSIS=Path(__file__).resolve().parents[1]
REPOSITORY=ANALYSIS.parent
STATE=Path('/workspace/.cache/alberta-analysis/jupyter')
TOKEN=STATE/'token'
CONFIG=STATE/'server_config.py'
PID=STATE/'server.pid'
BASE='http://127.0.0.1:8888'


def request(path,method='GET',data=None):
    token=TOKEN.read_text().strip()
    req=urllib.request.Request(BASE+path,
        headers={'Authorization':'token '+token,'Content-Type':'application/json'},
        method=method,data=None if data is None else json.dumps(data).encode())
    with urllib.request.urlopen(req,timeout=5) as response:
        body=response.read()
        return response.status,json.loads(body) if body else None


def check():
    status,body=request('/api/status')
    if status!=200 or not all(k in body for k in ['connections','kernels','last_activity']):
        raise RuntimeError('Jupyter status API did not return the expected model')
    status,kernels=request('/api/kernelspecs')
    if status!=200 or 'alberta-analysis' not in kernels['kernelspecs']:
        raise RuntimeError('Analysis kernel is unavailable')
    status,notebook=request('/api/contents/Infrastructure%20Analysis/Alberta_Infrastructure_Analysis.ipynb')
    if status!=200 or notebook.get('type')!='notebook' or len(notebook['content']['cells'])<10:
        raise RuntimeError('Jupyter cannot read the analysis notebook')
    return {'service':'JupyterLab','status':'ready','authenticated_api':True,
            'analysis_kernel_present':True,'notebook_cells':len(notebook['content']['cells']),
            'public_preview_created':False}


def configure():
    STATE.mkdir(parents=True,exist_ok=True)
    (STATE/'runtime').mkdir(exist_ok=True)
    if not TOKEN.exists():
        TOKEN.write_text(secrets.token_urlsafe(32))
        TOKEN.chmod(0o600)
    CONFIG.write_text("from pathlib import Path\nc=get_config()\n"
        f"c.IdentityProvider.token=Path({str(TOKEN)!r}).read_text().strip()\n"
        "c.ServerApp.open_browser=False\nc.ServerApp.ip='127.0.0.1'\n"
        "c.ServerApp.port=8888\nc.ServerApp.port_retries=0\n"
        f"c.ServerApp.root_dir={str(REPOSITORY)!r}\n")
    CONFIG.chmod(0o600)


def start():
    configure()
    try:
        return check()
    except (OSError,urllib.error.URLError,RuntimeError):
        pass
    environment=os.environ.copy()
    environment.update({'JUPYTER_CONFIG_DIR':str(STATE),
        'JUPYTER_RUNTIME_DIR':str(STATE/'runtime'),
        'JUPYTER_DATA_DIR':'/workspace/.venv/share/jupyter',
        'IPYTHONDIR':'/workspace/.cache/ipython','XDG_CACHE_HOME':'/workspace/.cache',
        'MPLCONFIGDIR':'/workspace/.cache/matplotlib'})
    with (STATE/'server.log').open('a') as log:
        process=subprocess.Popen([sys.executable,'-m','jupyter','lab',
            '--config='+str(CONFIG)],cwd=REPOSITORY,env=environment,
            stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    PID.write_text(str(process.pid))
    deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        if process.poll() is not None:
            raise RuntimeError('Jupyter exited; inspect the local log with tokens redacted')
        try:return check()
        except (OSError,urllib.error.URLError,RuntimeError):time.sleep(.3)
    raise RuntimeError('Jupyter readiness did not complete within 20 seconds')


def stop():
    if not PID.exists():return {'status':'not_started_by_this_helper'}
    pid=int(PID.read_text())
    process_path=Path(f'/proc/{pid}/cmdline')
    if process_path.exists():
        command=process_path.read_bytes().replace(b'\x00',b' ').decode(errors='replace')
        if str(CONFIG) not in command:
            raise RuntimeError('Recorded PID belongs to another process; refusing to stop it')
        os.kill(pid,signal.SIGTERM)
        deadline=time.monotonic()+8
        while process_path.exists() and time.monotonic()<deadline:
            stat_path=Path(f'/proc/{pid}/stat')
            if not stat_path.exists() or stat_path.read_text().split(') ')[-1].startswith('Z '):
                break
            time.sleep(.1)
        else:
            if process_path.exists():
                raise RuntimeError('Helper-owned service did not stop within eight seconds')
    PID.unlink(missing_ok=True)
    return {'status':'stopped_only_helper_started_service'}


def verify_kernel():
    import websocket
    check()
    status,kernel=request('/api/kernels',method='POST',data={'name':'alberta-analysis'})
    if status!=201:raise RuntimeError('Could not create the analysis kernel')
    kernel_id=kernel['id']
    token=TOKEN.read_text().strip()
    connection=None
    try:
        connection=websocket.create_connection(
            f'ws://127.0.0.1:8888/api/kernels/{kernel_id}/channels',
            header=['Authorization: token '+token],timeout=20,
            http_no_proxy=['127.0.0.1','localhost'])
        message_id=uuid.uuid4().hex
        code=("from pathlib import Path\nimport pandas as pd\nimport pdfplumber\n"
            f"source=Path({str(REPOSITORY/'Budget PDFs/2024-2025 Budget.pdf')!r})\n"
            "with pdfplumber.open(source) as pdf:\n"
            "    assert 'Historical Fiscal Summary' in pdf.pages[13].extract_text()\n"
            f"data=pd.read_csv({str(ANALYSIS/'research/capital/latest_vintage_actual_series.csv')!r})\n"
            "panel=data[data.calendar_year.between(2015,2024)]\n"
            "assert len(panel)==10 and panel.status.eq('actual').all()\n"
            "assert panel.loc[panel.calendar_year.eq(2024),'capital_plan_actual_million'].iloc[0]==7243\n"
            "print('ALBERTA_KERNEL_CHECK: 10 actual fiscal years; latest capital 7243 million')")
        message={'header':{'msg_id':message_id,'username':'onboarding',
            'session':uuid.uuid4().hex,'date':datetime.now(timezone.utc).isoformat(),
            'msg_type':'execute_request','version':'5.3'},
            'parent_header':{},'metadata':{},'channel':'shell',
            'content':{'code':code,'silent':False,'store_history':False,
                       'user_expressions':{},'allow_stdin':False,'stop_on_error':True},'buffers':[]}
        connection.send(json.dumps(message))
        result_text=''
        deadline=time.monotonic()+30
        completed=False
        while time.monotonic()<deadline:
            response=json.loads(connection.recv())
            if response.get('parent_header',{}).get('msg_id')!=message_id:continue
            kind=response.get('msg_type',response.get('header',{}).get('msg_type'))
            if kind=='error':raise RuntimeError('Analysis kernel failed its PDF/data functional check')
            if kind=='stream':result_text+=response['content'].get('text','')
            if kind=='execute_reply' and response['content'].get('status')!='ok':
                raise RuntimeError('Analysis kernel returned a failed execute reply')
            if kind=='status' and response['content'].get('execution_state')=='idle':
                completed=True
                break
        if not completed or 'ALBERTA_KERNEL_CHECK: 10 actual fiscal years; latest capital 7243 million' not in result_text:
            raise RuntimeError('Functional computation did not complete with expected source results')
        return {'service_kernel_functional_check':'passed','actual_fiscal_years':10,
                'latest_capital_actual_cad_millions':7243,'pdf_and_pandas_exercised':True}
    finally:
        if connection is not None:connection.close()
        request('/api/kernels/'+kernel_id,method='DELETE')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['start','status','stop','verify-kernel'])
    arguments=parser.parse_args()
    result={'start':start,'status':check,'stop':stop,'verify-kernel':verify_kernel}[arguments.action]()
    print(json.dumps(result,indent=2))
