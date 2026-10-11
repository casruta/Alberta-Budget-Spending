# Alberta budget — Power BI report

**Free Power BI Desktop for Windows · offline data snapshot · 42 chart topics**

[Download the complete project ZIP](https://github.com/casruta/Alberta-Budget-Spending/raw/refs/heads/main/Power%20BI/downloads/AlbertaBudget-PowerBI.zip) · [Read the visual report on GitHub](https://github.com/casruta/Alberta-Budget-Spending#readme)

The project contains a findings overview and all **42 existing chart topics**, rebuilt as **71 native Power BI chart panels** across **43 pages**. They use numeric data, rather than pictures of the original graphs. The model embeds **1,639 chart observations**, a source catalogue and **66 original evidence tables**. You can explore and edit the report locally without a paid Power BI license or a Power BI Service account.

**Verification status:** Microsoft JSON schemas, native TMDL model parsing, data, chart bindings and portable packaging are checked here. **Opening, refreshing and rendering in Windows Power BI Desktop have not been tested.** This download is a report project; a live Power BI Service report has not been published.

## Open on Windows

1. Install the current [free Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494).
2. Download the ZIP above and choose **Extract All**. Keep the report and semantic-model folders together.
3. Open **AlbertaBudget.pbip** from the extracted folder. If Desktop asks, enable **Power BI Project (.pbip)** and **enhanced report format (PBIR)** under **File → Options and settings → Options → Preview features**, then restart Desktop. Names and availability vary by release.
4. Choose **Home → Refresh** to load the embedded snapshot. The data queries do not need a local CSV path, credentials or internet access. Refresh reloads this snapshot; it does not fetch new government releases.
5. Start with **00 Findings at a glance**. Select a page tab for detail. Save a local copy as **.pbix** if you prefer a single Desktop file.

The ZIP contains the `.pbip`, report definitions, semantic model and these instructions. A ready-rendered `.pbix` is not included. Keep Desktop current if it reports an unsupported project version.

## Read the findings

| Pages | Content | Interpretation |
|---|---|---|
| 00 | Findings overview | Four selected panels; separate units and periods |
| 01–12 | Spending, health, education, living standards, housing and safety | Reviewed source series; dated results and matched targets |
| 13–21 | Capital spending, projects and sensitivity | Actuals and separate hypothetical price assumptions |
| 22–27 | Historical expense and fiscal archive | Original definitions and source vintages retained |
| 28–42 | 2026–29 Fiscal Plan archive | Actual / forecast / estimate / target explicitly distinguished |

**Explore:** hover over a data point for its unit, observation type, source CSV row and transformation. Select a chart and use **Filters on this visual** to choose periods or series. Chart and panel scope filters are fixed in viewing mode. Cross-filtering between panels is disabled because their definitions and units can differ. Desktop editing can change these settings; retain the scope filters when editing.

**Inspect the inputs:** `ChartData` contains the plotted numeric observations and their provenance. `SourceCatalog` maps each original CSV to its SHA-256 hash and model table. The 66 `Source###` evidence tables are hidden to keep the field list manageable; show hidden tables in Model view to inspect them. Their cells are preserved as source text, so suppression markers, identifiers and dates are not silently reinterpreted. They have no relationships to the chart facts, preventing duplicated evidence from being counted twice.

## Boundaries that matter

- Broad CPI and July population are proxies for financial purchasing power per resident, not sector costs, service volumes or quality.
- Poverty under the 2018 and 2023 Market Basket Measure bases stays in separate panels. No 2024 observation is invented for the old base.
- Life-expectancy panels show the source estimate and lower/upper 95% bounds as lines; 2023 and 2024 remain preliminary.
- Completion, achievement, access and housing measures retain their denominators and limitations. Combined housing units and subsidy households are not net new homes.
- Historical archive definitions differ from the reviewed functional series. Project dates are documented stages, not a complete provincial capacity series. Political windows are descriptive, not causal.
- Fiscal Plan projections and hypothetical price scenarios are separate from realized results. Fiscal-balance changes use contribution bars and a separate balance panel instead of an ambiguous waterfall.
- Published component sums and totals can differ by CAD 1M in the Fiscal Plan. These source residuals are retained and explained on the affected pages.
- The plotted-value measure returns a value only for one source observation. It returns blank for ambiguous totals; rates are never silently summed.

All **69 source CSVs** are catalogued. Two ragged StatCan metadata CSVs are documentation rather than fact tables, and one explicitly marked `DRAFT_DO_NOT_USE` table is quarantined. These three files stay in the repository and catalogue but are excluded from model evidence tables and plotted observations.

## Rebuild and verification

From the repository root, with Python 3.11 or newer:

```bash
python -m pip install -r "Power BI/requirements.txt"
python "Power BI/scripts/transform_data.py"
python "Power BI/scripts/build_project.py"
python "Power BI/scripts/validate_project.py"
python -m pytest "Power BI/tests/test_report_data.py"
```

The first script reads existing repository evidence. The second writes the Power Query import model, native PBIR visuals and portable ZIP. The third checks pinned Microsoft JSON schemas, every chart scope, axis bounds, embedded data, ZIP contents and the saved native parser receipt. Data tests check independent financial arithmetic and important source boundaries. Rebuilding does not regenerate the original analytical figures or change their source files.

For a changed semantic model, refresh the native parser receipt with the .NET 8 SDK before running `validate_project.py`:

```bash
dotnet run --project "Power BI/tests/tmdl" -- "Power BI/AlbertaBudget.SemanticModel/definition" "Power BI/data/native_model_validation.json"
```

This uses Microsoft’s `TmdlSerializer` to parse all 68 tables and check numeric types, import partitions and column bindings. It does not execute Power Query or DAX or render Desktop visuals. The saved receipt is matched to the exact model files; a changed model invalidates it.

[Chart catalogue](https://github.com/casruta/Alberta-Budget-Spending/blob/main/Power%20BI/data/chart_catalog.json) · [Transformed CSV](https://github.com/casruta/Alberta-Budget-Spending/blob/main/Power%20BI/data/chart_data.csv) · [Source catalogue](https://github.com/casruta/Alberta-Budget-Spending/blob/main/Power%20BI/data/source_catalog.json) · [Verification results](https://github.com/casruta/Alberta-Budget-Spending/blob/main/Power%20BI/data/validation_results.json)

No live Service URL exists for this project. A hosted interactive link would require a Power BI workspace and appropriate sharing access; this local report can be used without them. The GitHub README keeps the full static visual report available in a browser.
