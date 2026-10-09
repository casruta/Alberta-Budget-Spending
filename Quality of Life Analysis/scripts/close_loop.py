"""Record completion only after the requested review-loop duration and real checks."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
START=datetime.fromisoformat('2026-10-09T03:31:14+00:00')


def close():
    now=datetime.now(timezone.utc)
    elapsed=(now-START).total_seconds()/60
    if elapsed<=40:
        raise SystemExit(f'Loop still in progress: {elapsed:.3f}minutes; completion must exceed40minutes.')
    test=subprocess.run([sys.executable,'-m','pytest','tests','-q'],cwd=ROOT,text=True,capture_output=True)
    if test.returncode:
        print(test.stdout);print(test.stderr);raise SystemExit(test.returncode)
    count=int(re.search(r'(\d+) passed',test.stdout).group(1))
    assert count==12,test.stdout
    subprocess.run([sys.executable,'scripts/validate_delivery.py'],cwd=ROOT,check=True)
    assert subprocess.run(['git','diff','--quiet'],cwd=ROOT).returncode==0
    assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
    infra=ROOT.parent/'Infrastructure Analysis'
    old=json.loads((infra/'review/second_loop_artifact_hashes.json').read_text())['artifact_sha256']
    assert all(hashlib.sha256((infra/name).read_bytes()).hexdigest()==digest for name,digest in old.items())
    deliverables=[ROOT/'REPORT.md',ROOT/'README.md',ROOT/'Alberta_Budget_Quality_of_Life.ipynb',
                  ROOT/'Alberta_Budget_Quality_of_Life_preview.html',ROOT/'data/run_manifest.json',
                  ROOT/'research/source_verification/SOURCE_RECEIPT.md',ROOT/'review/LOOP_CHANGELOG.md']
    deliverables+=list((ROOT/'figures').glob('*.png'))+list((ROOT/'figures').glob('*.svg'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(deliverables)}
    (ROOT/'review/final_artifact_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
    delivery=json.loads((ROOT/'review/delivery_validation.json').read_text())
    completed=datetime.now(timezone.utc)
    result=dict(started_utc=START.isoformat(),completed_utc=completed.isoformat(),
                elapsed_minutes=(completed-START).total_seconds()/60,
                focus='Evidence gaps and source verification, selected by the user',
                downloaded_government_pdfs=12,direct_statistics_canada_tables=2,
                tests_passed=count,executed_notebook_code_cells=delivery['executed_code_cells'],
                rendered_figures=delivery['authored_figures'],source_hashes_verified=delivery['source_hashes_verified'],
                final_deliverable_hashes=len(hashes),prior_deliverable_hashes_preserved=len(old),
                original_tracked_files_changed=False,
                runtime='Independent pinned environment; confirmed from actual executed notebook output',
                configuration_draft_revision=5,configuration_fields_saved=['start_skill'],
                configuration_published=False,fresh_task_restoration_verified=False,
                assessment='Mixed observed outcomes; share with stated caveats; no causal overall QoL verdict',
                remaining_gaps=['Healthy life expectancy, life satisfaction, food insecurity and housing cost burden',
                                'Need/sector-price-adjusted inputs and fuller subgroup distributions',
                                'Latest fiscal actuals and source revision/definition bridges',
                                'Program exposure and counterfactual design for causal evaluation',
                                'Hosted Data report-app runtime unavailable; no hosted publication'])
    (ROOT/'review/loop_session.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':close()
