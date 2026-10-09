"""Bounded validation loop for the README, report and runnable evidence.

This runs a meaningful gate, records failures for correction, and reruns only
after the relevant files change. It never rewrites prose or guesses missing data.
Agent review supplies repairs; machine checks verify the repaired artifact.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import nbformat

ROOT=Path(__file__).resolve().parents[1]


def digest_inputs():
    paths=[ROOT/'README.md',ROOT/'REPORT.md',ROOT/'Alberta_Infrastructure_Analysis.ipynb']
    paths+=[ROOT/'report_template.md', ROOT/'data/run_manifest.json']
    paths+=sorted((ROOT/'scripts').glob('*.py'))
    paths+=sorted((ROOT/'tests').glob('*.py'))
    paths+=sorted((ROOT/'research').rglob('*.csv'))
    paths+=sorted((ROOT/'research/source_verification').glob('*.md'))
    return hashlib.sha256(b''.join(p.read_bytes() for p in paths)).hexdigest()


def notebook_checks():
    notebook=nbformat.read(ROOT/'Alberta_Infrastructure_Analysis.ipynb',as_version=4)
    nbformat.validate(notebook)
    code_cells=[c for c in notebook.cells if c.cell_type=='code']
    errors=[o for c in code_cells for o in c.get('outputs',[]) if o.output_type=='error']
    figures=[o for c in code_cells for o in c.get('outputs',[])
             if 'image/png' in o.get('data',{})]
    missing_alt=[o for o in figures if not o.get('metadata',{}).get('image/png',{}).get('alt')]
    if any(c.execution_count is None for c in code_cells):
        raise RuntimeError('At least one authored code cell has not executed')
    if errors:raise RuntimeError('Notebook contains execution errors')
    if len(figures)!=9:raise RuntimeError('Expected nine rendered authored figures')
    if missing_alt:raise RuntimeError('Figure alternative text is missing')
    matched_files=[]
    for cell in code_cells:
        filenames=re.findall(r"plots/([^'\"]+\.png)",cell.source)
        images=[o for o in cell.get('outputs',[]) if 'image/png' in o.get('data',{})]
        if len(filenames)!=len(images):
            raise RuntimeError('Cannot pair the authored plot files with notebook images')
        for filename,output in zip(filenames,images):
            embedded=base64.b64decode(output['data']['image/png'])
            if embedded!=(ROOT/'plots'/filename).read_bytes():
                raise RuntimeError(f'Notebook embeds a stale figure: {filename}; execute it after plot changes')
            matched_files.append(filename)
    return {'executed_code_cells':len(code_cells),'error_outputs':len(errors),
            'rendered_figures':len(figures),'figures_with_alt_text':len(figures)-len(missing_alt),
            'embedded_figures_matching_saved_plots':len(matched_files)}


def run_gate():
    record={'time_utc':datetime.now(timezone.utc).isoformat(),'input_digest':digest_inputs(),
            'human_source_review':'See review/second_loop_final_adversarial_audit.md and earlier reviews; automated checks do not replace source judgment'}
    tests=subprocess.run([sys.executable,'-m','pytest','tests','-q'],cwd=ROOT,
        capture_output=True,text=True)
    record['tests_exit_code']=tests.returncode
    record['tests_result']=tests.stdout.strip()
    try:
        record['notebook']=notebook_checks()
        notebook_ok=True
    except Exception as error:
        record['notebook_error']=str(error)
        notebook_ok=False
    record['verdict']='pass_with_documented_evidence_limits' if tests.returncode==0 and notebook_ok else 'needs_revision'
    path=ROOT/'review/quality_gate_history.json'
    history=json.loads(path.read_text()) if path.exists() else []
    history.append(record)
    path.write_text(json.dumps(history,indent=2)+'\n')
    return record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=1,
        help='Maximum gates; additional rounds require a changed input digest')
    args=parser.parse_args()
    if not 1<=args.rounds<=10:parser.error('Use 1–10 bounded rounds')
    previous_digest=None
    result=None
    for iteration in range(args.rounds):
        current=digest_inputs()
        if current==previous_digest:
            print('Inputs unchanged; an identical rerun adds no validation evidence.')
            break
        result=run_gate()
        print(json.dumps({'iteration':iteration+1,'verdict':result['verdict'],
            'tests_exit_code':result['tests_exit_code'],
            'notebook':result.get('notebook',result.get('notebook_error'))},indent=2))
        if result['verdict']=='pass_with_documented_evidence_limits':break
        previous_digest=current
        # Repairs require actual analysis/authoring judgment. Do not auto-fill gaps.
        print('Correct the recorded failure, then run this gate after the files change.')
    return 0 if result and result['verdict']=='pass_with_documented_evidence_limits' else 1


if __name__=='__main__':raise SystemExit(main())
