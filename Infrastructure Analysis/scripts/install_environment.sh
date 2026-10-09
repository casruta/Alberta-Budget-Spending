#!/usr/bin/env bash
set -euo pipefail

cd /workspace/Alberta-Budget-Spending
export MPLCONFIGDIR=/workspace/.cache/matplotlib
export XDG_CACHE_HOME=/workspace/.cache
export IPYTHONDIR=/workspace/.cache/ipython
export JUPYTER_CONFIG_DIR=/workspace/.cache/alberta-analysis/jupyter
export JUPYTER_RUNTIME_DIR=/workspace/.cache/alberta-analysis/jupyter/runtime
export JUPYTER_DATA_DIR=/workspace/.venv/share/jupyter
mkdir -p "$MPLCONFIGDIR" "$IPYTHONDIR" "$JUPYTER_CONFIG_DIR" "$JUPYTER_RUNTIME_DIR"

# This task is already isolated. Reuse its checkout rather than making a worktree.
# Dependencies/configuration live outside the checkout; source/lockfiles stay intact.
if [ ! -x /workspace/.venv/bin/python ]; then
  python -m venv --system-site-packages /workspace/.venv
fi
/workspace/.venv/bin/python -m pip install --no-cache-dir -r 'Infrastructure Analysis/requirements.txt'
/workspace/.venv/bin/python -m ipykernel install --prefix /workspace/.venv \
  --name alberta-analysis --display-name 'Alberta analysis (Python 3)'
/workspace/.venv/bin/python - <<'PY'
import pandas, numpy, matplotlib, seaborn, pdfplumber, fitz, pypdf
import nbformat, nbconvert, ipykernel, jupyterlab, pytest
import subprocess
from pathlib import Path
with pdfplumber.open(Path('Budget PDFs') / '2024-2025 Budget.pdf') as source:
    assert 'Historical Fiscal Summary' in source.pages[13].extract_text()
economic_text = subprocess.check_output(['pdftotext', '-f', '13', '-l', '13',
    '-layout', 'Budget PDFs/2024-2025 Budget.pdf', '-'], text=True)
assert 'Population (July 1, thousands)' in economic_text
assert 'Alberta consumer price index' in economic_text
print('Analysis libraries, notebook tools, Poppler extraction and official PDF input verified.')
PY
