"""
Agent 1 - Data Preparation for Revenue vs Expense Analysis.

Loads Alberta Budget 2026 CSVs and produces analysis-ready comparison files:
  - revenue_comparison.csv
  - expense_comparison.csv
  - revenue_vs_expense_summary.csv
  - top_changes.csv

All dollar values in $ millions.
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "Data"
OUT = Path(__file__).resolve().parent

YEAR_COLS = [
    "2024-25 Actual",
    "2025-26 Budget",
    "2025-26 Forecast",
    "2026-27 Estimate",
    "2027-28 Target",
    "2028-29 Target",
]

RENAME = {
    "2024-25 Actual": "2024-25_Actual",
    "2025-26 Budget": "2025-26_Budget",
    "2025-26 Forecast": "2025-26_Forecast",
    "2026-27 Estimate": "2026-27_Estimate",
    "2027-28 Target": "2027-28_Target",
    "2028-29 Target": "2028-29_Target",
}


def load_data():
    revenue = pd.read_csv(DATA / "fiscal_plan_2026_revenue.csv")
    expenses = pd.read_csv(DATA / "fiscal_plan_2026_ministry_expenses.csv")
    fiscal = pd.read_csv(DATA / "fiscal_plan_2026_fiscal_summary.csv")
    return revenue, expenses, fiscal


def build_revenue_comparison(revenue: pd.DataFrame) -> pd.DataFrame:
    """Leaf-level revenue items with change metrics vs 2024-25."""
    subtotal_keywords = ["subtotal", "total"]
    mask = ~revenue["Item"].str.lower().str.contains("|".join(subtotal_keywords))
    df = revenue.loc[mask, ["Item"] + YEAR_COLS].copy()

    # Drop the Budget column (task asks for Actual + forward projections)
    df = df.drop(columns=["2025-26 Budget"])
    df = df.rename(columns=RENAME)

    df["Change_vs_2024"] = df["2026-27_Estimate"] - df["2024-25_Actual"]
    df["Pct_Change_vs_2024"] = (
        (df["Change_vs_2024"] / df["2024-25_Actual"].replace(0, float("nan"))) * 100
    ).round(1)

    return df.reset_index(drop=True)


def build_expense_comparison(expenses: pd.DataFrame) -> pd.DataFrame:
    """Ministry expenses with change metrics and 2026-27 share."""
    mask = ~expenses["Ministry"].str.lower().str.contains("total")
    df = expenses.loc[mask].copy()
    df = df.rename(columns=RENAME)

    yr_cols_renamed = [RENAME[c] for c in YEAR_COLS]

    df["Change_vs_2024"] = df["2026-27_Estimate"] - df["2024-25_Actual"]
    df["Pct_Change_vs_2024"] = (
        (df["Change_vs_2024"] / df["2024-25_Actual"].replace(0, float("nan"))) * 100
    ).round(1)
    total_2026 = df["2026-27_Estimate"].sum()
    df["Share_2026"] = ((df["2026-27_Estimate"] / total_2026) * 100).round(1)

    return df.reset_index(drop=True)


def build_revenue_vs_expense_summary(fiscal: pd.DataFrame) -> pd.DataFrame:
    """Summary table of total revenue, expense, surplus by fiscal year."""
    rev_row = fiscal.loc[fiscal["Item"] == "Total revenue"].iloc[0]
    exp_row = fiscal.loc[fiscal["Item"] == "Total expense"].iloc[0]

    years = ["2024-25", "2025-26", "2026-27", "2027-28", "2028-29"]
    # Map display year to the column we should use
    year_col_map = {
        "2024-25": "2024-25 Actual",
        "2025-26": "2025-26 Forecast",
        "2026-27": "2026-27 Estimate",
        "2027-28": "2027-28 Target",
        "2028-29": "2028-29 Target",
    }

    rows = []
    prev_rev, prev_exp = None, None
    for yr in years:
        col = year_col_map[yr]
        rev = float(rev_row[col])
        exp = float(exp_row[col])
        surplus = rev - exp

        rev_chg = round((rev - prev_rev) / prev_rev * 100, 1) if prev_rev else None
        exp_chg = round((exp - prev_exp) / prev_exp * 100, 1) if prev_exp else None

        rows.append({
            "Fiscal_Year": yr,
            "Total_Revenue": int(rev),
            "Total_Expense": int(exp),
            "Surplus_Deficit": int(surplus),
            "Revenue_Change_Pct": rev_chg,
            "Expense_Change_Pct": exp_chg,
        })
        prev_rev, prev_exp = rev, exp

    return pd.DataFrame(rows)


def build_top_changes(
    rev_comp: pd.DataFrame, exp_comp: pd.DataFrame
) -> pd.DataFrame:
    """Top 10 biggest absolute $ changes (revenue + expense) from 2024-25 to 2026-27."""
    rev_items = rev_comp[["Item", "2024-25_Actual", "2026-27_Estimate", "Change_vs_2024", "Pct_Change_vs_2024"]].copy()
    rev_items.insert(0, "Type", "Revenue")
    rev_items = rev_items.rename(columns={
        "Change_vs_2024": "Change",
        "Pct_Change_vs_2024": "Pct_Change",
    })

    exp_items = exp_comp[["Ministry", "2024-25_Actual", "2026-27_Estimate", "Change_vs_2024", "Pct_Change_vs_2024"]].copy()
    exp_items.insert(0, "Type", "Expense")
    exp_items = exp_items.rename(columns={
        "Ministry": "Item",
        "Change_vs_2024": "Change",
        "Pct_Change_vs_2024": "Pct_Change",
    })

    combined = pd.concat([rev_items, exp_items], ignore_index=True)
    combined["Abs_Change"] = combined["Change"].abs()
    combined = combined.nlargest(10, "Abs_Change").drop(columns=["Abs_Change"])

    return combined.reset_index(drop=True)


def print_summary(rev_comp, exp_comp, summary, top_changes):
    print("=" * 70)
    print("ALBERTA BUDGET 2026 - DATA PREPARATION SUMMARY")
    print("=" * 70)

    print(f"\nRevenue items prepared:  {len(rev_comp)}")
    print(f"Expense items prepared:  {len(exp_comp)}")
    print(f"Fiscal years covered:    {len(summary)}")

    print("\n--- Revenue vs Expense Summary ($ millions) ---")
    print(summary.to_string(index=False))

    print("\n--- Top 10 Absolute Changes (2024-25 to 2026-27) ---")
    print(top_changes.to_string(index=False))

    total_rev_24 = summary.loc[summary["Fiscal_Year"] == "2024-25", "Total_Revenue"].iloc[0]
    total_rev_26 = summary.loc[summary["Fiscal_Year"] == "2026-27", "Total_Revenue"].iloc[0]
    total_exp_24 = summary.loc[summary["Fiscal_Year"] == "2024-25", "Total_Expense"].iloc[0]
    total_exp_26 = summary.loc[summary["Fiscal_Year"] == "2026-27", "Total_Expense"].iloc[0]

    print(f"\nTotal revenue change 2024-25 -> 2026-27:  ${total_rev_26 - total_rev_24:,}M ({(total_rev_26 - total_rev_24) / total_rev_24 * 100:.1f}%)")
    print(f"Total expense change 2024-25 -> 2026-27:  ${total_exp_26 - total_exp_24:,}M ({(total_exp_26 - total_exp_24) / total_exp_24 * 100:.1f}%)")
    print(f"Surplus/Deficit 2026-27:                   ${total_rev_26 - total_exp_26:,}M")
    print("=" * 70)


def main():
    revenue, expenses, fiscal = load_data()

    rev_comp = build_revenue_comparison(revenue)
    exp_comp = build_expense_comparison(expenses)
    summary = build_revenue_vs_expense_summary(fiscal)
    top_changes = build_top_changes(rev_comp, exp_comp)

    rev_comp.to_csv(OUT / "revenue_comparison.csv", index=False)
    exp_comp.to_csv(OUT / "expense_comparison.csv", index=False)
    summary.to_csv(OUT / "revenue_vs_expense_summary.csv", index=False)
    top_changes.to_csv(OUT / "top_changes.csv", index=False)

    print_summary(rev_comp, exp_comp, summary, top_changes)
    print(f"\nFiles written to: {OUT}")


if __name__ == "__main__":
    main()
