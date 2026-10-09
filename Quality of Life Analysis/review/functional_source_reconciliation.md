# Independent functional expense reconciliation and baseline audit

## Verification method

Used **pdfplumber** to re-extract original PDF rows independently of the primary **PyMuPDF** extractor. All80functional source cells(8measures×10years) agree with primary extraction. Independently extracted July1population and annual CPI rows from latest p13; all10population/CPI pairs agree too. Inspected the rendered original latest p14(`research/budget/latest_original_functional_page14.png`):2022–23Other13,769 andTotalProgram61,691 are visibly printed in that column.

Maintained independent verifier:`research/budget/verify_functional_expenses_independent.py`. It uses Decimal precision32for baseline arithmetic,checks demographic counts and primary-parser agreement,and preserves original source values. Decimal CPI parsing is separate from integer-cell whitespace normalization to avoid merging adjacent decimal rates. Outputs are `functional_cross_vintage_2022_independent.csv`,`functional_baseline_sensitivity_independent.csv`,and `independent_functional_verification.json`.

##2022–23 inconsistency is in latest source,not extraction

|Original report vintage/page|Health|Education|Social|Other|Program total|Component sum minus program total|
|---|---:|---:|---:|---:|---:|---:|
|2022–23,p13|25,486|15,220|7,222|13,743|61,671|0|
|2023–24,p14|25,486|15,220|7,222|13,766|61,694|0|
|2024–25,p14|25,486|15,220|7,222|13,769|61,691|+6|

All amounts areCADmillions. Earlier vintages reconcile;the latest changesOther+3andTotalProgram−3relative to the preceding vintage,resulting in6Mdisagreement. Debt2829→2828,and latestTotalExpense64,498 still equals latest reportedProgram61,691+Debt2,828−PensionRecovery21.

This demonstrates a **newly published source inconsistency alongside legitimate revisions**. It does not identify which source entry is erroneous. No local narrative isolates the precise functional correction;do not invent a repair.6M is about0.010%ofprogram expense,and does not affect2015/2018/2019→2024endpoint ratios. Astacked2022expense chart must show/note the residual rather than silently alteringOtherorTotal. General accounting-policy/reorganization warnings remain inforce.

##Independent Decimal baseline calculations

For each baselineyearb:

`CPIratio=product[1+AlbertaAnnualCPI(t)/100] for t=b+1..2024`

`AdjustedExpensePerResidentChange%=[Expense(2024)/Expense(b)/(Population(2024)/Population(b))/CPIratio−1]×100`

Population isJuly1fiscal-startyear;CPI iscalendar-year annualgrowth. The baselineyear's own growth is not included twice. All inputs come directly from original latest sourcevia independentparser. Rounded-to4decimal results:

|Function|2015–16→2024–25|2018–19→2024–25|2019–20→2024–25|
|---|---:|---:|---:|
|Health|−1.2740%|−1.4290%|−0.4179%|
|Basic/advanced education|−15.5040%|−15.3378%|−13.2875%|
|Social services|+19.6310%|+5.4294%|+2.9796%|
|Total program expense|−2.0239%|−4.3231%|−4.6461%|
|Debt servicing|+178.3342%|+19.2338%|+8.5884%|
|Total expense|+1.5351%|−3.6985%|−4.1149%|

The requested2018headline checks **Health−1.43%,Education−15.34%,Social+5.43%** are confirmed independently. Debt comparison is consolidated expenditure,not taxpayer-only direct-debt cost;2015's much smaller base explains very large proportional increase. Neither thisnorotherbaselines estimate causal government effect or household outcomes. Health's small change must retain price/fiscal-alignment uncertainty language.

##2024ministry rounding independently checked

Second-parser p7ministry summation confirms:

- Budget26ministry sum60,124 versus reportedOperatingTotal60,124:residual0M.
- Currentactualsum62,026 versusreported62,025:residual+1M.
- Prioractualsum58,148 versusreported58,149:residual−1M.

These1Mdeviations are consistent with26integer-roundedministry cells and oneinteger-roundedtotal. SourceHealth budget24,648/currentactual25,669 imply displayedsubtraction1,021,butreportedchange1,020canreflectunroundedsource arithmetic. Preserve bothreportedchangesandcomputeddisplayed differences ratherthan“correcting”source1Mvariance. Ministry andfunctionalcategories mustremain distinct.

No completedInfrastructure Analysis files or original PDFs were altered. Financial-claims review should continue when the quality-of-life report is available.
