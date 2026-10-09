# Independent review of pay/unemployment evidence and visual

**Mathematical, visual and export-status checks pass after the identified export correction.** Reviewed `scripts/analyze_inputs.py`, `data/economic_outcome_context.csv`, the source economic ledger and official PDF page 13, and the rendered `figures/03_pay_and_unemployment.png`. No original repository file, Infrastructure Analysis asset, or root-owned script was edited.

## Independent source and Decimal calculation

Parsed the original 2024-25 Final Results economic page directly with `pdftotext`, then used **Decimal precision 35** to recompute annual CPI factors and adjusted weekly earnings. This check neither imported the main analysis nor consumed the Infrastructure Analysis CPI index. All ten exported CPI-adjusted earnings levels agree within **1e-7 CAD/week**; every unemployment observation matches the official row. Full precision results are saved in `economic_decimal_verification.json`.

For 2018–2024, average weekly nominal earnings increase **15.6794%**, the rounded annual CPI chain increases **20.1257%**, and adjusted average weekly earnings decline **3.7013%**. For 2019–2024 the adjusted decline is **3.3155%**. For 2015–2024 it is **8.0459%**. The adjustment uses the product of rates after the baseline year, not the baseline year's own growth rate. The terminal 2024 nominal/adjusted earnings levels correctly coincide at **$1,328/week**. Earnings are not divided by population because this source is already an average earnings measure; doing so would be erroneous.

The 2024 primary household income row is **7.1% annual aggregate growth**, marked `a`; the same page says **“2024 is an estimate.”** It is neither final actual income nor average/median per-person income, after-tax household resources or affordability. The source table's `a` marks only selected rows and does not classify all economic rows as forecasts.

## Required export correction

The current pivot retains values but drops per-metric source status/units. Consequently `economic_outcome_context.csv` exports 2024 `primary_household_income_growth=7.1` without its **estimate** flag. Generic metadata saying selected values are estimated is insufficient for a consumer of that row. Retain an explicit per-row primary household income status column, and retain units or provide structured per-field metadata pointing to the authoritative source ledger. Employment values are **thousands of employed persons**, not exact individuals; earnings are **nominal CAD/week**, unemployment is **percent of labour force**, and housing starts are **units started**. The figure itself uses only earnings and unemployment, so it does not misplot this estimated income value.

## Visual semantics and readability

The two panels use separate labelled axes and calendar-year dates, avoiding incompatible pay/rate scales on one axis. The pay legend distinguishes nominal earnings from a 2024 CPI basis; unemployment is explicitly labelled as a percent. The pay axis starts above zero, which is acceptable for a clearly labelled line chart of changes but must not be read as a bar-chart magnitude comparison. The unemployment axis includes zero and preserves the pandemic peak and subsequent rise.

The image is readable, without substantive clipping. The source footer explicitly cautions that earnings depend on employment mix/hours and are not median after-tax household income, poverty or household-specific affordability. The title does not claim improved welfare or a causal policy effect. Minor spacing improvements are recommended: **“CPI-adjusted 2024 CAD/week”**, and **“Source: Final Results PDF p. 13, calendar-year rows”**. These are presentation issues rather than numerical failures.

The underlying earnings series can change because of employment mix, employment hours, worker coverage and wages. Its CPI adjustment is a consumer-price sensitivity; it does not directly observe fixed-worker purchasing power, household living standards or distribution. The report should call the result **CPI-adjusted average weekly earnings**, rather than household real income.

## Scope and remaining gaps

The reviewed economic panel ends in **2024**, with no manufactured 2025 outcomes. Canada comparisons, poverty, food insecurity, core housing need and distributional outcomes are not inferred from these earnings and unemployment series. No synthetic quality-of-life score is produced. At review time the root report was still being assembled; its final prose should preserve these qualifications.

## Export correction verified

The rebuilt economic export now retains all six per-metric status/unit columns plus source file, source page and time basis. The 2024 primary household income value explicitly retains its estimate status. The previously identified export issue is resolved.
