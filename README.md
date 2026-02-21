# Alberta Budget Spending Analysis (2011-12 to 2024-25)

An in-depth analysis of 14 years of Alberta provincial operating expenses, extracted from official budget PDFs and normalized into consistent spending categories across three governing parties (PC, NDP, UCP).

## Key Question

**Alberta's operating budget grew from $34.2B to $62.0B (+81.5%) in 14 years. But how much of that is real growth, and how much is just population and inflation?**

After adjusting for both, real per-capita spending only grew **+3.8%** over the entire period — from $12,176 to $12,635 per Albertan (in 2024-25 dollars).

---

## Key Findings

### The Headline Numbers (2011-12 to 2024-25)

| Metric | 2011-12 | 2024-25 | Change |
|--------|---------|---------|--------|
| Total Operating Expense | $34.2B | $62.0B | +81.5% |
| Population | 3.79M | 4.91M | +29.6% |
| Real Per-Capita Spending (2024-25 $) | $12,176 | $12,635 | +3.8% |

### Where Every Dollar Goes

| Category | 2011-12 | 2024-25 | Growth | Budget Share |
|----------|---------|---------|--------|-------------|
| Health | $14.7B | $27.3B | +85% | 43.0% &rarr; 44.0% |
| Education (K-12) | $6.0B | $9.3B | +55% | 17.5% &rarr; 15.0% |
| Advanced Education | $2.8B | $6.6B | +138% | 8.1% &rarr; 10.7% |
| Social Services | $4.5B | $7.1B | +58% | 13.1% &rarr; 11.4% |
| Other | $6.2B | $11.8B | +89% | 18.3% &rarr; 19.0% |

### Three Insights

1. **Health consumes 44 cents of every operating dollar** and its share is still growing. Per-capita health spending rose from $3,883 to $5,554, but after inflation that's only a 6% real increase.

2. **K-12 Education is losing ground.** Its budget share fell from 17.5% to 15.0% even as nominal spending grew 55% — population growth and inflation consumed the increase.

3. **Advanced Education saw the largest relative surge** (+138%), driven by post-secondary funding restructuring that shifted capital grants into operating budgets.

---

## Visualizations

### Spending Composition
![Expense Composition](plots/expense_composition.png)

Alberta's operating budget nearly doubled from $34B to $62B over 14 years. The top panel shows absolute spending growth by category; the bottom shows each category's share of total operating expense. Background shading indicates the governing party: PC (blue), NDP (orange), UCP (green).

---

### Per-Capita Spending
![Per-Capita Spending](plots/expense_percapita.png)

Adjusting for Alberta's 29.6% population growth reveals a different picture. Health per-capita spending accelerated sharply from 2019-20 onward, while Education (K-12) per-capita spending barely kept pace. The grouped bars compare three political eras side by side.

---

### Inflation-Adjusted (Real) Spending
![Real Spending](plots/expense_real_spending.png)

The top panel compares nominal vs real (2024-25 dollar) total operating expense — the yellow shaded area represents the inflation illusion. The bottom panel shows real per-capita spending with direction-colored bars: red for year-over-year increases, green for decreases. Real per-capita spending peaked in 2016-17 at $13,712 under the NDP and fell back to $12,635 by 2024-25.

---

### Health Spending Deep Dive
![Health Deep Dive](plots/expense_health_deep_dive.png)

Health is Alberta's dominant expense. The left panel shows absolute spending (bars) alongside its budget share (white line) — the share dipped during the NDP era before climbing back to 44%. The right panel reveals that in real per-capita terms, health spending grew only 6% over 14 years ($5,239 to $5,554 in 2024-25 dollars).

---

### Cumulative Growth by Category
![Growth Indexed](plots/expense_growth_indexed.png)

All categories indexed to 2011-12 = 100. The dashed white line (population) and dotted purple line (CPI) serve as benchmarks. Categories growing faster than both lines represent real per-capita increases. Social Services and Health track closely until 2019-20, when Health spending accelerated due to COVID-19 pressures.

---

### Fiscal Overview (Revenue vs. Expense)
![Fiscal Summary](plots/alberta_fiscal_summary_infographic.png)

The broader fiscal context: Alberta's revenue vs. expense over 25 years (2000-01 to 2024-25), the resulting surplus/deficit, and the volatility of non-renewable resource revenue that drives Alberta's boom-bust fiscal cycles.

---

## Data Sources

| Source | Description |
|--------|-------------|
| [Alberta Budget Documents](https://open.alberta.ca/publications/budget) | 14 official budget PDFs (2011-12 to 2024-25) — ministry-level operating expense tables |
| [Statistics Canada Table 17-10-0009-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901) | Alberta quarterly population estimates (midyear July values) |
| [Statistics Canada Table 18-10-0004-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000401) | Alberta CPI, All-items, annual average (2002=100) |

## Methodology

### Ministry Normalization

Alberta restructures its ministries frequently. To enable meaningful comparison across 14 years, ~80+ raw ministry names were mapped into 5 stable analytical categories:

- **Health** — Alberta Health, Alberta Health Services, Mental Health & Addiction
- **Education (K-12)** — Education, including school capital and operations
- **Advanced Education** — Advanced Education, post-secondary institutions, student aid
- **Social Services** — Human Services, Children & Family Services, Community & Social Services, Seniors & Housing
- **Other** — Justice, Infrastructure, Transportation, Agriculture, Energy, Municipal Affairs, Environment, Treasury Board, Executive Council, and all remaining ministries

### Inflation Adjustment

All real (inflation-adjusted) figures use Alberta-specific CPI deflated to constant 2024-25 dollars:
```
Real Value = Nominal Value x (CPI_2024-25 / CPI_year)
```

### Extraction & Validation

Ministry-level data was extracted from budget PDFs using pdfplumber word-level extraction with x-coordinate column analysis. All 14 years were validated against:
- Within-PDF "Total Operating Expense" rows (max deviation: 0.01%)
- Cross-year prior-year actual comparisons
- Ground-truth checks against pre-extracted Excel data for 2023-25

## Project Structure

```
Alberta Budget Analysis/
├── README.md
├── Alberta_Expense_Analysis.ipynb    # Main analysis notebook
├── extract_ministry_expenses.py      # PDF extraction & normalization pipeline
├── generate_fiscal_infographic.py    # Revenue/expense/surplus infographic
├── Data/
│   ├── alberta_surplus_deficit.csv   # 25-year fiscal summary
│   ├── ministry_expenses.csv         # Aggregated 5-category data
│   ├── ministry_expenses_detail.csv  # Individual ministry values
│   └── ministry_expenses_wide.csv    # Pivoted format (years x categories)
├── Budget PDFs/                      # 14 source PDFs (2011-12 to 2024-25)
└── plots/
    ├── expense_composition.png
    ├── expense_percapita.png
    ├── expense_real_spending.png
    ├── expense_health_deep_dive.png
    ├── expense_growth_indexed.png
    └── alberta_fiscal_summary_infographic.png
```

## Requirements

```
pandas
numpy
matplotlib
pdfplumber
```

## License

This project uses publicly available Government of Alberta budget data and Statistics Canada open data. Analysis and visualizations are original work.
