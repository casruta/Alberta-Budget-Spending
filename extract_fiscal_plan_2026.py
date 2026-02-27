"""
Extract data from Alberta Fiscal Plan 2026-2029 PDF into structured CSVs.

Extracts three main tables:
1. Revenue detail (Schedule 3 / Schedule 4)
2. Ministry-level expense detail (Schedule 3)
3. Consolidated fiscal summary (Schedule 1)
4. Statement of Financial Position (Schedule 2)
"""

import csv
from pathlib import Path

DATA_DIR = Path("Data")
DATA_DIR.mkdir(exist_ok=True)

# Column headers for all tables
FISCAL_YEARS = [
    "2024-25 Actual",
    "2025-26 Budget",
    "2025-26 Forecast",
    "2026-27 Estimate",
    "2027-28 Target",
    "2028-29 Target",
]


def write_csv(filename, headers, rows):
    filepath = DATA_DIR / filename
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  Written: {filepath} ({len(rows)} rows)")


# =============================================================================
# 1. REVENUE DETAIL (from Schedule 4 / p.152-153)
# =============================================================================
revenue_rows = [
    # Income taxes
    ("Income Taxes", "Personal income tax", 16120, 15510, 14771, 15933, 16612, 17741),
    ("Income Taxes", "Corporate income tax", 8125, 6764, 7420, 7300, 7472, 7615),
    ("Income Taxes", "Subtotal income taxes", 24245, 22274, 22191, 23233, 24084, 25356),
    # Other taxes
    ("Other Taxes", "Education property tax", 2797, 3124, 3124, 3592, 3792, 3848),
    ("Other Taxes", "Fuel tax / electric vehicle tax", 1431, 1438, 1426, 1450, 1480, 1512),
    ("Other Taxes", "Tobacco / vaping tax", 414, 420, 406, 385, 355, 325),
    ("Other Taxes", "Insurance tax", 914, 972, 984, 1060, 1142, 1232),
    ("Other Taxes", "Cannabis tax", 232, 215, 225, 229, 232, 236),
    ("Other Taxes", "Tourism levy", 126, 122, 138, 200, 207, 214),
    ("Other Taxes", "Other taxes", 197, 272, 299, 321, 353, 453),
    ("Other Taxes", "Subtotal other taxes", 6111, 6563, 6603, 7237, 7562, 7821),
    # Total tax revenue
    ("Tax Revenue", "Total tax revenue", 30356, 28837, 28794, 30470, 31646, 33177),
    # Non-renewable resource revenue (from p.19 fiscal summary breakdown)
    ("Resource Revenue", "Bitumen royalty", 17167, 12830, 12669, 9688, 12102, 12765),
    ("Resource Revenue", "Other non-renewable resource revenue", 4819, 4237, 3617, 3525, 4132, 4126),
    ("Resource Revenue", "Total non-renewable resource revenue", 21986, 17067, 16285, 13213, 16234, 16892),
    # Federal transfers
    ("Federal Transfers", "Transfers from Government of Canada", 12618, 13305, 13566, 13715, 13826, 13839),
    # Investment income
    ("Investment Income", "Investment income", 4803, 2883, 4568, 4358, 4071, 4052),
    # Other revenue
    ("Other Revenue", "Net income from govt. business enterprises", 2053, 2016, 2194, 2621, 2709, 2759),
    ("Other Revenue", "Premiums, fees and licences", 5504, 5756, 5640, 6000, 6170, 6424),
    ("Other Revenue", "Other", 5149, 4273, 4245, 4173, 4259, 4376),
    # Total
    ("Total", "Total revenue", 82469, 74138, 75292, 74550, 78914, 81518),
]

print("Extracting Fiscal Plan 2026-2029 data...")
write_csv(
    "fiscal_plan_2026_revenue.csv",
    ["Category", "Item"] + FISCAL_YEARS,
    revenue_rows,
)

# =============================================================================
# 2. MINISTRY EXPENSE DETAIL (from Schedule 3 / p.152)
# =============================================================================
ministry_expense_rows = [
    ("Advanced Education", 7204, 7411, 7674, 7738, 7928, 8088),
    ("Affordability and Utilities", 133, 168, 148, 153, 153, 153),
    ("Agriculture and Irrigation", 1988, 984, 1704, 963, 906, 916),
    ("Arts, Culture and Status of Women", 238, 226, 223, 199, 218, 237),
    ("Assisted Living and Social Services", 10282, 11298, 11540, 12233, 12685, 12787),
    ("Children and Family Services", 1515, 1595, 1621, 1685, 1695, 1695),
    ("Education and Childcare", 11417, 12357, 12471, 13436, 13369, 13543),
    ("Energy and Minerals", 1400, 1122, 1028, 894, 968, 1031),
    ("Environment and Protected Areas", 440, 565, 545, 484, 481, 493),
    ("Executive Council", 84, 96, 100, 104, 106, 106),
    ("Forestry and Parks", 1089, 409, 1182, 421, 416, 411),
    ("Hospital and Surgical Health Services", 11491, 12157, 13002, 13832, 14601, 15098),
    ("Indigenous Relations", 235, 238, 256, 268, 268, 273),
    ("Infrastructure", 690, 921, 907, 961, 932, 918),
    ("Jobs, Economy, Trade and Immigration", 364, 416, 460, 422, 412, 399),
    ("Justice", 690, 707, 751, 773, 758, 758),
    ("Mental Health and Addiction", 1706, 1794, 1876, 2043, 2089, 2096),
    ("Municipal Affairs", 1287, 1388, 1404, 1386, 1506, 1497),
    ("Primary and Preventative Health Services", 11649, 11182, 12244, 12653, 13313, 14067),
    ("Public Safety and Emergency Services", 1446, 1350, 1449, 1509, 1531, 1517),
    ("Service Alberta and Red Tape Reduction", 181, 186, 196, 206, 203, 204),
    ("Technology and Innovation", 890, 1010, 1005, 1103, 908, 904),
    ("Tourism and Sport", 134, 133, 135, 127, 136, 112),
    ("Transportation and Economic Corridors", 2516, 2681, 2532, 2998, 2801, 2366),
    ("Treasury Board and Finance", 2123, 2199, 2073, 2115, 2090, 2124),
    ("Legislative Assembly", 144, 164, 172, 216, 218, 189),
]

# Add totals row
ministry_totals = tuple(
    sum(row[i] for row in ministry_expense_rows) for i in range(1, 7)
)

write_csv(
    "fiscal_plan_2026_ministry_expenses.csv",
    ["Ministry"] + FISCAL_YEARS,
    [row for row in ministry_expense_rows]
    + [("Total program expense",) + ministry_totals],
)

# =============================================================================
# 3. CONSOLIDATED FISCAL SUMMARY (Schedule 1 / p.150)
# =============================================================================
fiscal_summary_rows = [
    # Revenue
    ("Revenue", "Total revenue", 82469, 74138, 75292, 74550, 78914, 81518),
    # Expense breakdown
    ("Expense", "Operating expense", 62025, 64311, 67016, 70398, 72360, 74053),
    ("Expense", "Operating expense % change", 6.7, 3.7, 8.0, 5.0, 2.8, 2.3),
    ("Expense", "Capital grants", 2934, 3452, 3347, 3672, 3384, 2923),
    ("Expense", "Amortization / inventory consumption / loss on disposals", 4446, 4993, 4830, 4853, 4944, 5005),
    ("Expense", "Taxpayer-supported debt servicing costs", 2437, 2348, 2343, 2838, 3571, 4147),
    ("Expense", "Self-supported debt servicing costs", 777, 620, 579, 568, 651, 716),
    ("Expense", "Pension provisions", -403, -375, -196, -408, -415, -423),
    ("Expense", "Disaster and emergency assistance", 1932, 0, 1506, 0, 0, 0),
    ("Expense", "Expense before contingency", 74149, 75349, 79426, 81922, 84495, 86422),
    ("Expense", "Contingency (forecast unallocated)", 0, 4000, 0, 2000, 2000, 2000),
    ("Expense", "Total expense", 74149, 79349, 79426, 83922, 86495, 88422),
    # Surplus/deficit
    ("Balance", "Surplus / (deficit)", 8320, -5211, -4134, -9373, -7581, -6904),
    ("Balance", "Surplus / (deficit) before contingency", 8320, -1211, -4134, -7373, -5581, -4904),
    # Capital Plan
    ("Capital Plan", "Capital grants", 2934, 3452, 3347, 3672, 3384, 2923),
    ("Capital Plan", "Capital investment", 4309, 5187, 5340, 6297, 6614, 5426),
    ("Capital Plan", "Total capital plan", 7243, 8639, 8687, 9969, 9998, 8349),
    # Borrowing
    ("Borrowing", "Direct borrowing required", 0, 7357, 6425, 16304, 14713, 13193),
    ("Borrowing", "Total taxpayer-supported debt (capital + fiscal plan)", 85225, 82539, 92086, 108867, 123950, 137492),
]

write_csv(
    "fiscal_plan_2026_fiscal_summary.csv",
    ["Section", "Item"] + FISCAL_YEARS,
    fiscal_summary_rows,
)

# =============================================================================
# 4. STATEMENT OF FINANCIAL POSITION (Schedule 2 / p.151)
# =============================================================================
# Note: Financial position is at March 31, so years are 2025, 2026, 2027, 2028, 2029
POSITION_YEARS = [
    "At March 31, 2025 (Actual)",
    "At March 31, 2026 (Forecast)",
    "At March 31, 2027 (Estimate)",
    "At March 31, 2028 (Target)",
    "At March 31, 2029 (Target)",
]

financial_position_rows = [
    # Financial assets
    ("Financial Assets", "Alberta Heritage Savings Trust Fund", 24743, 29857, 32082, 34022, 35880),
    ("Financial Assets", "Alberta Heritage Foundation for Medical Research", 2370, 2618, 2838, 3017, 3187),
    ("Financial Assets", "Alberta Heritage Science and Engineering Research", 1374, 1520, 1646, 1748, 1842),
    ("Financial Assets", "Alberta Heritage Scholarship", 1539, 1702, 1843, 1954, 2059),
    ("Financial Assets", "Alberta Enterprise Corporation", 323, 319, 315, 311, 306),
    ("Financial Assets", "General Revenue Fund - surplus cash", 2571, 0, 0, 0, 0),
    ("Financial Assets", "General Revenue Fund - debt retirement", 9952, 1926, 0, 0, 0),
    ("Financial Assets", "Alberta Fund", 2571, 0, 0, 0, 0),
    ("Financial Assets", "Loans to local authorities", 13823, 15073, 15932, 16642, 17295),
    ("Financial Assets", "Agriculture Financial Services Corporation", 2920, 3247, 4439, 5789, 7327),
    ("Financial Assets", "Equity in commercial enterprises", 735, 638, 853, 1123, 1421),
    ("Financial Assets", "Student loans", 4936, 5077, 5265, 5441, 5646),
    ("Financial Assets", "TIER Fund", 1106, 1157, 1173, 1194, 1223),
    ("Financial Assets", "Other financial assets", 28972, 20961, 21783, 22555, 22377),
    ("Financial Assets", "Total financial assets", 97935, 84095, 88169, 93795, 98565),
    # Liabilities
    ("Liabilities", "Direct borrowing for the Capital Plan", 48045, 54471, 61849, 69555, 76206),
    ("Liabilities", "P3s (Capital Plan)", 2515, 2500, 2525, 2444, 2343),
    ("Liabilities", "Teachers Pension Plan debt", 451, 451, 451, 451, 451),
    ("Liabilities", "Direct borrowing for the Fiscal Plan", 34214, 34665, 44041, 51500, 58492),
    ("Liabilities", "Total taxpayer-supported debt", 85225, 92086, 108867, 123950, 137492),
    ("Liabilities", "Debt issued for loans to local authorities", 13823, 15073, 15932, 16642, 17295),
    ("Liabilities", "AFSC debt", 3434, 3672, 3907, 3947, 4072),
    ("Liabilities", "Total taxpayer and self-supported debt", 102482, 110832, 128705, 144538, 158859),
    ("Liabilities", "Coal phase-out liabilities", 514, 432, 353, 269, 182),
    ("Liabilities", "Pension liabilities", 7504, 7292, 6884, 6469, 6046),
    ("Liabilities", "Asset retirement obligations", 2579, 2579, 2567, 2554, 2542),
    ("Liabilities", "Other liabilities", 19193, 2659, 1023, 1387, 687),
    ("Liabilities", "Total liabilities", 132272, 123793, 139532, 155217, 168315),
    # Net position
    ("Net Position", "Net financial assets / (debt)", -34337, -39699, -51363, -61422, -69750),
    ("Net Position", "Capital / other non-financial assets", 62925, 64200, 66383, 68834, 70204),
    ("Net Position", "Spent deferred capital contributions", -4080, -4127, -4018, -3991, -3937),
    ("Net Position", "Net assets", 24508, 20374, 11002, 3421, -3483),
    ("Net Position", "Net debt to GDP", -7.2, -8.3, -10.5, -11.8, -12.9),
]

write_csv(
    "fiscal_plan_2026_financial_position.csv",
    ["Section", "Item"] + POSITION_YEARS,
    financial_position_rows,
)

# =============================================================================
# 5. COMBINED LONG-FORMAT CSV (for easy analysis)
# =============================================================================
long_rows = []

# Revenue in long format
for cat, item, *values in revenue_rows:
    for fy, val in zip(FISCAL_YEARS, values):
        long_rows.append(("Revenue", cat, item, fy, val))

# Ministry expenses in long format
for ministry, *values in ministry_expense_rows:
    for fy, val in zip(FISCAL_YEARS, values):
        long_rows.append(("Ministry Expense", "Operating", ministry, fy, val))

# Fiscal summary in long format
for section, item, *values in fiscal_summary_rows:
    for fy, val in zip(FISCAL_YEARS, values):
        long_rows.append(("Fiscal Summary", section, item, fy, val))

write_csv(
    "fiscal_plan_2026_long.csv",
    ["Table", "Category", "Item", "Fiscal Year", "Value ($ millions)"],
    long_rows,
)

print(f"\nDone! {len(long_rows)} total data points extracted.")
print("\nFiles created in Data/:")
print("  1. fiscal_plan_2026_revenue.csv          - Revenue by source")
print("  2. fiscal_plan_2026_ministry_expenses.csv - Expense by ministry")
print("  3. fiscal_plan_2026_fiscal_summary.csv    - Consolidated fiscal summary")
print("  4. fiscal_plan_2026_financial_position.csv - Balance sheet")
print("  5. fiscal_plan_2026_long.csv              - All data in long format")
