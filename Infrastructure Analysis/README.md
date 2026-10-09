# Alberta infrastructure spending and delivery analysis

**Prepared October 9, 2026 · source actuals through March 31, 2025**

Actual capital spending rose **19.6% from 2018–19 to 2024–25**, but population growth and consumer-price inflation together exceeded that increase. **CPI-adjusted capital spending per resident fell 12.6%.** Identifiable schools, health facilities, highways, bridges and flood protection were delivered after 2019; available records do not establish aggregate net capacity or whether it kept pace with population. Projects often began before the UCP government.

Read the **[full report](REPORT.md)** for the financial evidence, baseline sensitivity, sector changes, physical deliveries and source limitations. Use the **[executed notebook](Alberta_Infrastructure_Analysis.ipynb)** for inspectable calculations and figures.

![Capital spending per resident](plots/02_spending_per_resident.png)

## Scope and important distinctions

- The political transition is the UCP taking office in April 2019; 2018–19 is the last full pre-UCP year. Earlier Alberta conservative governments are not treated as beginning in 2019.
- Ten accessible actual years cover **2015–16 through 2024–25**. As of October 2026 the latest completed decade is 2016–17 through 2025–26; that final year remains unavailable in the accessible corpus. No missing actuals were forecast or filled with zero.
- Primary figures are the fully consolidated **Capital Plan**, not operating expense or the Infrastructure ministry budget. Grants and investment have different accounting treatment; do not add the entire capital plan to expense.
- Consumer-price adjustment is a **sensitivity**, not a construction-volume measure. July population and starting-calendar-year annual CPI approximate fiscal alignment.
- A source's project completion is not necessarily operational opening, net-new capacity, or exclusive policy attribution. Missing net stock and condition data remain missing.
- The official historical table warns of accounting-policy changes even within the same source vintage. Recent sector comparisons use same-report reclassified pairs.

## Reproduce

The prepared cloud environment has Python 3.12 and `/workspace/.venv`. The existing checkout is already isolated; use it directly and do not create a Git worktree unless explicitly requested.

```bash
cd '/workspace/Alberta-Budget-Spending/Infrastructure Analysis'
export MPLCONFIGDIR=/workspace/.cache/matplotlib
export XDG_CACHE_HOME=/workspace/.cache
export IPYTHONDIR=/workspace/.cache/ipython
export JUPYTER_CONFIG_DIR=/workspace/.cache/alberta-analysis/jupyter
export JUPYTER_RUNTIME_DIR=/workspace/.cache/alberta-analysis/jupyter/runtime
export JUPYTER_DATA_DIR=/workspace/.venv/share/jupyter
/workspace/.venv/bin/python research/capital/extract_primary.py
/workspace/.venv/bin/python research/capital/extract_execution_composition.py
/workspace/.venv/bin/python research/demography/extract_demography.py
/workspace/.venv/bin/python research/demography/build_vintage_ledger.py
/workspace/.venv/bin/python research/demography/verify_vintage_ledger.py
/workspace/.venv/bin/python scripts/build_claim_register.py
/workspace/.venv/bin/python scripts/build_corpus_inventory.py
/workspace/.venv/bin/python scripts/analyze.py
/workspace/.venv/bin/python scripts/physical_figures.py
/workspace/.venv/bin/python scripts/price_sensitivity.py
/workspace/.venv/bin/python scripts/execution_figures.py
/workspace/.venv/bin/python scripts/render_report.py
/workspace/.venv/bin/python -m pytest tests -q
PATH=/workspace/.venv/bin:$PATH /workspace/.venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Alberta_Infrastructure_Analysis.ipynb
/workspace/.venv/bin/python scripts/quality_gate.py
# Optional self-contained notebook export; Classic preserves the authored image alternatives.
/workspace/.venv/bin/python -m jupyter nbconvert --to html --template classic --output Alberta_Infrastructure_Analysis_preview.html Alberta_Infrastructure_Analysis.ipynb
```

For a fresh machine, install the versions in [requirements.txt](requirements.txt) into a virtual environment before those commands. The demographic extraction also requires Poppler's `pdftotext` command (version 25.03.0 is verified here); Python requirements alone do not install it. The saved installer checks a functional Poppler extraction against the official population/CPI page. The extraction and analysis workflow runs from local files without official-site access. Source outputs are regenerated inside this new analysis directory; existing tracked datasets, PDFs and notebooks remain unchanged. Review generated results before replacing user-edited report text.

JupyterLab is optional for browsing/editing; notebook execution and the validation tests are required to demonstrate reproducibility. Startup and health checks are saved in the cloud environment configuration. A running Jupyter process does not survive an environment snapshot and must be restarted when needed.

```bash
# Optional authenticated local editor; the helper never prints a token or preview URL.
/workspace/.venv/bin/python scripts/jupyter_service.py start
/workspace/.venv/bin/python scripts/jupyter_service.py status
/workspace/.venv/bin/python scripts/jupyter_service.py verify-kernel
# Stop only the service started by this helper when it is no longer needed.
/workspace/.venv/bin/python scripts/jupyter_service.py stop
```

## Evidence and outputs

| Location | Contents |
|---|---|
| [REPORT.md](REPORT.md) | Narrative report, actual spending, population/CPI sensitivity, sector and physical evidence |
| [Alberta_Infrastructure_Analysis.ipynb](Alberta_Infrastructure_Analysis.ipynb) | Executed reproducible notebook with visible tables and figures |
| [data/](data/) | Analysis panel, baseline comparisons, weighted tenure summaries and run manifest |
| [plots/](plots/) | Standalone PNG and SVG figures |
| [research/capital/](research/capital/) | Source-extracted actual totals, reclassifications, budget comparisons and exact pages |
| [research/demography/](research/demography/) | Rounded official population/CPI inputs, provenance and robustness audit |
| [research/physical/](research/physical/) | Physical-output ledger, health evidence and audited 17-project status timeline |
| [review/](review/) | Independent review, calculation checks and correction log |
| [Claim register](research/source_verification/CLAIM_REGISTER.md) | Consequential claims linked to original source pages, extracts and interpretation limits |
| [Evidence gaps](research/source_verification/EVIDENCE_GAPS.md) | Missing sources/definitions and acceptance checks for a latest-decade or net-capacity extension |
| [Source inventory](research/source_verification/CORPUS_INVENTORY.md) | PDF identities, hashes and full-volume versus short-summary coverage |
| [tests/](tests/) | Source, arithmetic, reconciliation and artifact-consistency checks |

All main financial inputs come from [2024–25 Final Results, PDF pp. 13–14](../Budget%20PDFs/2024-2025%20Budget.pdf#page=13). The file is misleadingly named “Budget”; its internal title and source metadata identify a June 2025 final-results report. Exact paths, hashes, units, definitions and source vintages are retained. URLs in provenance are catalog/reference links, not a claim that blocked online sources were retrieved.

## Validation and remaining limits

See [validation log](review/validation_log.md) for the checks actually performed and corrections from independent review. The team separated capital extraction, population/price inputs, physical-project research and independent recomputation, with subagents handling recent sector tables and healthcare evidence.

The [quality gate](scripts/quality_gate.py) records a bounded validation loop in `review/quality_gate_history.json`. It checks substantive tests, actual notebook execution, nine rendered figures and alternative text, and verifies that embedded notebook images match the saved plots. A failing gate requires a real correction before rerunning. It stops on a pass and does not repeatedly run unchanged tests or fabricate missing data. Independent human-style source review remains separate from the automated gate. A clean virtual environment without system site packages also passed the checks, reducing the risk that preinstalled libraries conceal missing requirements; this does not test restoration in a new cloud task.

The additional source-verification loop distinguishes contemporary budget execution from revised historical actuals, records grants versus investment, and archives cross-vintage demographic revisions. The latest $943M nominal increase is $831M grants plus $112M investment; neither component proves net physical capacity. Two exact financial revision causes remain unresolved and are explicitly identified in the report.

Official Alberta and Statistics Canada retrieval currently returns proxy access errors. Required domains were saved in the configuration draft; review/save settings and publish the environment to enable future work under the supported flow. No secret is needed for these public sources. The report does not claim fresh-task restoration has been tested.

The Data report-app runtime is unavailable here, so no hosted interactive report was built or published. The delivered report is repository Markdown with standalone figures and an executed notebook companion. Province-wide net capacity, condition, construction-price adjustment and the 2025–26 actual year remain unresolved evidence requirements.
