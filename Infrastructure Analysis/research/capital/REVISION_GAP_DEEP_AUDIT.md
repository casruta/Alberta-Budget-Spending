# Deep source audit: unresolved revisions and recovery-support disagreement

## Search method and scope

Reopened original repository PDFs directly using PyMuPDF, not prior cached excerpts. Relevant corpus consists of selected Final Results Year-End reports, **not complete consolidated-financial-statement volumes**: 2019–20 contains20 PDF pages;2020–21 contains24;2022–23 contains24;2023–24 contains24. Thus referenced full annual-report financial schedules are not embedded locally in these files.

Searched every page of all supplied2018–19 through2024–25 reports for `123`, `11 million`, `restat`, `reclass`, `capital` with `invest`/`grant`, `accounting`, `consolidat`, `correction`, `prior year`, `comparative`. `revision_gap_search_results.json` retains107 matching source pages and382 search hits, including full page text and match snippets. `.full_text_revision_audit.txt` retains complete original extracted text for the five most relevant reports. This is a record of evidence searched, not a claim that missing accounting causes are identified.

## 2020–21 disagreement resolved visually

Re-rendered ORIGINAL2020–21 PDF p16 and p18. The stored images `2020_21_original_pdf_page16_verification.png` and `2020_21_original_pdf_page18_verification.png` allow independent inspection of the column layout.

- **p16 left column:** “In2020–21, Capital Plan spending was$6.9 billion, with **$1.1 billion added in response to COVID-19 and in support of Alberta’s Recovery Plan**.”
- **p16 middle column:** “Alberta’s Recovery Plan initiatives totalled **$1.1 billion in2020–21**.”
- **p18 beginning of narrative:** “2020–21 provided$6.9 billion in capital project spending, **$1.4 billion higher than2019–20**.” This is the rounded **total year-over-year capital-plan increase**6,896−5,545=1,351M, not the recovery-program amount.
- **p18 next bullet:** “During the year, **$1.1 billion in capital was spent in support of COVID-19 response and recovery**.”

Both amounts are correct for different concepts. **Do not change the recovery-support amount from1.1B to1.4B.** The proposed source-backed narrative distinguishes total spending change from program support. Rounded component listings on p18 total1,163M(627+475+46+15), whereas headline1.1B and possible overlaps/classification are not precisely reconciled by the excerpt. Avoid presenting an exact unrounded stimulus subtotal from those rounded narrative components.

## 2018–19 investment correction: location confirmed, cause still unresolved

**Original2018–19 report p3:** grants1,952M; investment4,228M; total6,180M.

**Next2019–20 report p3 prior-actual2018–19:** grants1,952M; investment4,105M; total6,057M.

The entire−123M adjustment is located in **capital investment**, not grants. Latest historical total6,057M retains that revised amount.

Additional checks:

1.2018–19 p9/10 explains Infrastructure construction attribution on behalf of schools/AHS. That transfer cannot safely be cited as explaining the−123M total correction; it shifts ministry attribution and the source says old ministry comparisons are not restated.
2.2018–19 p9 capital financing includes825M SUCH self-finance,88M asset disposal/valuation adjustment for Swan Hills,55M prior-financing withdrawal.2019–20 p9 prior cash requirement excluding SUCH changes3,404→3,280M, a124M displayed difference, consistent in broad location with investment cash requirements plus rounding. It is not explicit evidence of what adjustment created the−123M.
3.2019–20 p2's explicit restatement concerns Treasury Board and Finance third-party investment-management administration revenue/expense(52M actual,46M budget). This is not a stated explanation of capital investment−123M.
4.2019–20 p9 mentions123M withdrawal from the capital-plan financing account **in2019–20**. It is a financing flow, not the2018–19 investment restatement; matching number alone is not causal evidence.
5.2018–19 p10 reports123M post-secondary maintenance/renewal. This is a sector expenditure, not a revision explanation.
6.2019–20 p11 balance-sheet footnote refers to Schedule15,p70 in the **full2019–20 Government of Alberta Annual Report** for net-asset adjustments. That referenced financial statement is not among the locally available20page year-end excerpt. It is an actionable source to retrieve once network access changes, not a basis to invent an explanation now.

**Conclusion:** exact corrected row/value verified; specific accounting cause remains unresolved within supplied source corpus. Retain comparability warning and use common latest vintage. Do not call it a cancelled123M project, ministry transfer, lost revenue, or missing cash.

## 2022–23 capital-grant correction: narrowed to Other, cause unresolved

**2022–23 p3:** grants1,536M;investment4,108M;total5,644M.

**2023–24 p3 prior-actual2022–23:** grants1,525M;investment4,108M;total5,633M.

The−11M revision is entirely capital grants. Further original-page7 checks narrow the category:

| Capital grants2022–23 reported categories | Original actual2022–23 p7 | Next report prior actual2023–24 p7 |
|---|---:|---:|
| Culture / Arts,Culture,Status of Women |97|97|
| Energy / Energy and Minerals |53|53|
| Municipal Affairs |750|750|
| Transportation and Economic Corridors |452|452|
| Other |184|173|
| Total |1536|1525|

Thus the displayed−11M is in **Other capital grants** after the organizational revision, not Municipal Affairs/LRT or transportation grants. Labels are retained with explicit renaming; this small table is not a complete harmonized ministry panel.

2023–24 p2 states revised government organization under Orders in Council156/2023 and029/2024, and adoption of P3, Revenue and Purchased Intangibles standards. It does **not** identify the specific Other grant item/correction. Source numbers alone do not establish which ministry/program moved or whether the item became operating expenditure. The exact grant cause remains unresolved. Do not explain it solely as a P3 accounting adjustment: P3 opening stock−415M is a different explicitly stated accounting effect.

Search of all local reports returned no passage explicitly connecting an11M grant correction to a named program. References to11M amortization, health or lab projects elsewhere concern different concepts/years. Underlying full consolidated financial statements/ministry notes are needed to establish the correction.

## Integration recommendations

Keep the main financial series latest-vintage. Include the now-verified revision ledger as transparency, with unresolved causes explicitly marked. Treat budget-execution ratios as aggregate financial outcomes rather than original project delivery adherence. Present latest capital grants831M/investment112M decomposition using the same2024–25 source p3. Preserve the statement that common vintage cannot eliminate policy/accounting changes, and do not extrapolate accounting stocks to physical capacity.
