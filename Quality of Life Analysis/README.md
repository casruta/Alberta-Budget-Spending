# Alberta budget and quality-of-life analysis

Read [REPORT.md](REPORT.md) for the supported assessment: recent outcomes are mixed, spending growth is an input, and this observational evidence does not identify a causal budget effect. Source-specific dates, definitions, targets, estimates and gaps remain visible. The report includes recent government website downloads and a direct Statistics Canada poverty extract, beyond the original archived financial PDFs.

The deliverable is a repository report, standalone PNG/SVG figures and an executed [notebook](Alberta_Budget_Quality_of_Life.ipynb), with an optional self-contained HTML notebook export. The Data report-app runtime is unavailable here; no hosted interactive report or site is claimed.

## Reproduce offline

Use Python3.12 and the pinned dependencies in [the prepared environment's requirements](../Infrastructure%20Analysis/requirements.txt). Poppler's `pdftotext` is an additional system dependency; version25.03.0 is verified. All source downloads are archived, so regeneration does not require live website access. Download manifests distinguish earlier HTTP-client failures from later successful curl retrievals with normal TLS.

```bash
cd '/workspace/Alberta-Budget-Spending/Quality of Life Analysis'
export MPLCONFIGDIR=/workspace/.cache/matplotlib
export XDG_CACHE_HOME=/workspace/.cache
export IPYTHONDIR=/workspace/.cache/ipython
export JUPYTER_CONFIG_DIR=/workspace/.cache/alberta-analysis/jupyter
export JUPYTER_RUNTIME_DIR=/workspace/.cache/alberta-analysis/jupyter/runtime
export JUPYTER_DATA_DIR=/workspace/.venv/share/jupyter
/workspace/.venv/bin/python research/budget/extract_functional_expense.py
/workspace/.venv/bin/python research/living_standards/extract_living_standards.py
/workspace/.venv/bin/python research/living_standards/extract_current_social_outcomes.py
/workspace/.venv/bin/python research/living_standards/extract_childcare_income_access.py
/workspace/.venv/bin/python research/living_standards/extract_mbm_poverty.py
/workspace/.venv/bin/python research/health/life_tables/extract_life_expectancy.py
/workspace/.venv/bin/python research/health/extract_health_outcomes.py
/workspace/.venv/bin/python research/source_verification/extract_safety_mental_health.py
/workspace/.venv/bin/python scripts/analyze_inputs.py
/workspace/.venv/bin/python scripts/build_figures.py
/workspace/.venv/bin/python scripts/render_report.py
/workspace/.venv/bin/python scripts/build_source_receipt.py
/workspace/.venv/bin/python -m pytest tests -q
PATH=/workspace/.venv/bin:$PATH /workspace/.venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Alberta_Budget_Quality_of_Life.ipynb
/workspace/.venv/bin/python -m jupyter nbconvert --to html --template classic --HTMLExporter.embed_images=True --output Alberta_Budget_Quality_of_Life_preview.html Alberta_Budget_Quality_of_Life.ipynb
/workspace/.venv/bin/python scripts/validate_delivery.py
```

Run source extractors before the renderer, then execute the notebook and export it. Rendering rewrites the report and unexecuted notebook from the reviewed template; do not render again after execution unless you intend to rerun the notebook. Do not overwrite user edits without review. This existing checkout is isolated; no Git worktree is needed.

Independent checks use different source parsers and direct calculations: functional PDF values via pdfplumber/Decimal, economic rows via pypdf, Health tables via Poppler bounding boxes, and MBM raw CSV fields via csv.DictReader. Their exact reviewed scope is recorded in `review/` and source verifiers; archived manual graph transcriptions are separately labeled and not claimed as fully machine-audited.

## Inspect evidence

|Location|Purpose|
|---|---|
|`research/budget/`|Consolidated functional expense, ministry operating expense, budget/actual and accounting caveats|
|`research/health/`|Current and historical outcome definitions, verified downloads, ED method errors and continuing-care bridge|
|`research/education_safety/`|Current Education annual report/update, cohort/achievement observations and revision caveats|
|`research/living_standards/`|Economic inputs, SCSS/childcare access, direct MBM poverty rows/bases/flags and source conflicts|
|[Source receipt](research/source_verification/SOURCE_RECEIPT.md)|Official URLs, document identities, retrieval diagnosis and hash inventory|
|`data/`|Derived tables, chart receipts and source hash manifest|
|`review/`|Independent numeric/semantic/visual reviews and loop completion evidence|

Tracked repository files, original PDFs/datasets/notebooks and completed Infrastructure Analysis artifacts are preserved. Configuration draft saving is separate from publication; fresh-task restoration is not claimed. Optional Jupyter editing can use the existing authenticated helper in Infrastructure Analysis; its live process must restart after a snapshot and its tokens must not be printed.
