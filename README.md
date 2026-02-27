# Alberta Budget Analysis

**Prepared by:** Kacper Ruta
**Date:** February 2026

A data-driven analysis of the Government of Alberta's provincial finances, covering 14 years of historical operating expenditures (2011-2025) and a forward-looking assessment of the 2026-2029 Fiscal Plan. All data is extracted directly from official budget documents using Python, with analysis performed in Jupyter notebooks.

---

## Analyses

### [2011-2025 Expense Analysis](2011-2025%20Expense%20Analysis/)

Historical analysis of Alberta's operating expenditures across 14 fiscal years. Examines ministry-level spending trends normalized for population growth (29.6%) and inflation (34.9%), finding that real per-capita spending increased by only 3.8% over the period. Includes 6 visualizations covering spending composition, per-capita trends, inflation-adjusted spending, and health spending deep dives.

### [2026-2029 Fiscal Plan Analysis](2026-2029%20Fiscal%20Plan/)

Comprehensive analysis of the Government of Alberta's Fiscal Plan 2026-2029, tabled February 26, 2026. Documents the structural deficit ($9.4B peak in 2026-27, $28B cumulative), the bitumen royalty collapse (-43.6%), and the 61% growth in taxpayer-supported debt. Includes macroeconomic context, interprovincial comparisons, revenue diversification options (PST analysis, Heritage Fund reform, international lessons), expenditure efficiency assessments, and 15 visualizations.

---

## Shared Resources

| Folder | Contents |
|---|---|
| `Data/` | Extracted CSV datasets for both analyses (historical ministry expenses, 2026-2029 fiscal plan projections) |
| `Budget PDFs/` | 14 source budget documents from the Government of Alberta (2011-12 through 2024-25) |

## Software Requirements

```
pandas
numpy
matplotlib
seaborn
pdfplumber
```
