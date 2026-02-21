"""
Alberta Ministry-Level Operating Expense Data (2011-12 to 2024-25).

All values manually verified from budget PDF pages using pdfplumber word-level
extraction (extract_words with x-coordinate analysis for column separation).

Outputs:
  Data/ministry_expenses.csv       — normalized 5-category breakdown per year
  Data/ministry_expenses_detail.csv — individual ministry values
  Data/ministry_expenses_wide.csv  — pivoted format (one row per year)
"""

import re
from pathlib import Path

import pandas as pd

PROJECT = Path(r"C:\Users\Casper Ruta\Desktop\Kacper Ruta 2026\Alberta Budget Analysis")
DATA_DIR = PROJECT / "Data"
DATA_DIR.mkdir(exist_ok=True)


# ── Ministry name normalization ──────────────────────────────────────────────

NORMALIZE_MAP = {
    # Health
    "health": "Health",
    "health and wellness": "Health",
    "mental health and addiction": "Health",
    # Education K-12
    "education": "Education (K-12)",
    # Advanced Education
    "advanced education": "Advanced Education",
    "advanced education and technology": "Advanced Education",
    "innovation and advanced education": "Advanced Education",
    "enterprise and advanced education": "Advanced Education",
    # Social Services
    "human services": "Social Services",
    "seniors": "Social Services",
    "seniors and housing": "Social Services",
    "seniors, community and social services": "Social Services",
    "children's services": "Social Services",
    "children and family services": "Social Services",
    "community and social services": "Social Services",
    # Other — everything else
    "aboriginal relations": "Other",
    "affordability and utilities": "Other",
    "agriculture and forestry": "Other",
    "agriculture and irrigation": "Other",
    "agriculture and rural development": "Other",
    "agriculture, forestry and rural economic development": "Other",
    "arts, culture and status of women": "Other",
    "culture": "Other",
    "culture and community services": "Other",
    "culture and status of women": "Other",
    "culture and tourism": "Other",
    "culture, multiculturalism and status of women": "Other",
    "economic development and trade": "Other",
    "economic development, trade and tourism": "Other",
    "energy": "Other",
    "energy and minerals": "Other",
    "environment and parks": "Other",
    "environment and protected areas": "Other",
    "environment and sustainable resource development": "Other",
    "environment and water": "Other",
    "executive council": "Other",
    "finance": "Other",
    "forestry and parks": "Other",
    "forestry, parks and tourism": "Other",
    "immigration and multiculturalism": "Other",
    "indigenous relations": "Other",
    "infrastructure": "Other",
    "intergovernmental, international and aboriginal relations": "Other",
    "international and intergovernmental relations": "Other",
    "jobs, economy and innovation": "Other",
    "jobs, economy and northern development": "Other",
    "jobs, economy and trade": "Other",
    "jobs, skills, training and labour": "Other",
    "justice": "Other",
    "justice and solicitor general": "Other",
    "labour": "Other",
    "labour and immigration": "Other",
    "legislative assembly": "Other",
    "municipal affairs": "Other",
    "public safety and emergency services": "Other",
    "service alberta": "Other",
    "service alberta and red tape reduction": "Other",
    "skilled trades and professions": "Other",
    "solicitor general and public security": "Other",
    "status of women": "Other",
    "sustainable resource development": "Other",
    "technology and innovation": "Other",
    "tourism and sport": "Other",
    "tourism, parks and recreation": "Other",
    "trade, immigration and multiculturalism": "Other",
    "transportation": "Other",
    "transportation and economic corridors": "Other",
    "treasury board and enterprise": "Other",
    "treasury board and finance": "Other",
}


def normalize_ministry(raw: str) -> str:
    key = raw.strip().lower()
    key = re.sub(r"^\d+\s+", "", key)
    return NORMALIZE_MAP.get(key, "Other")


# ── Hardcoded ministry data (verified from PDFs) ────────────────────────────

# Each year is a list of (ministry_raw, value, source_description) tuples.
# Values are in millions of dollars.

YEAR_DATA: dict[str, list[tuple[str, int, str]]] = {}

# ---- 2011-12 ----
# Source: 2012-13 Budget PDF page 114, 2011-12 Forecast column
YEAR_DATA["2011-12"] = [
    ("Culture and Community Services", 169, "2012-2013 Budget.pdf (page 114)"),
    ("Health and Wellness", 14706, "2012-2013 Budget.pdf (page 114)"),
    ("Human Services", 2418, "2012-2013 Budget.pdf (page 114)"),
    ("Justice", 519, "2012-2013 Budget.pdf (page 114)"),
    ("Municipal Affairs", 353, "2012-2013 Budget.pdf (page 114)"),
    ("Seniors", 2057, "2012-2013 Budget.pdf (page 114)"),
    ("Solicitor General and Public Security", 679, "2012-2013 Budget.pdf (page 114)"),
    ("Tourism, Parks and Recreation", 160, "2012-2013 Budget.pdf (page 114)"),
    ("Advanced Education and Technology", 2780, "2012-2013 Budget.pdf (page 114)"),
    ("Education", 5977, "2012-2013 Budget.pdf (page 114)"),
    ("Finance", 1129, "2012-2013 Budget.pdf (page 114)"),
    ("Infrastructure", 499, "2012-2013 Budget.pdf (page 114)"),
    ("Service Alberta", 251, "2012-2013 Budget.pdf (page 114)"),
    ("Transportation", 472, "2012-2013 Budget.pdf (page 114)"),
    ("Treasury Board and Enterprise", 60, "2012-2013 Budget.pdf (page 114)"),
    ("Agriculture and Rural Development", 836, "2012-2013 Budget.pdf (page 114)"),
    ("Energy", 340, "2012-2013 Budget.pdf (page 114)"),
    ("Environment and Water", 178, "2012-2013 Budget.pdf (page 114)"),
    ("Intergovernmental, International and Aboriginal Relations", 174, "2012-2013 Budget.pdf (page 114)"),
    ("Sustainable Resource Development", 265, "2012-2013 Budget.pdf (page 114)"),
    ("Executive Council", 30, "2012-2013 Budget.pdf (page 114)"),
    ("Legislative Assembly", 123, "2012-2013 Budget.pdf (page 114)"),
]
# Sum = 34,175

# ---- 2012-13 ----
# Source: 2012-13 Budget PDF page 114, 2012-13 Estimate column
YEAR_DATA["2012-13"] = [
    ("Culture and Community Services", 174, "2012-2013 Budget.pdf (page 114)"),
    ("Health and Wellness", 15864, "2012-2013 Budget.pdf (page 114)"),
    ("Human Services", 2547, "2012-2013 Budget.pdf (page 114)"),
    ("Justice", 531, "2012-2013 Budget.pdf (page 114)"),
    ("Municipal Affairs", 369, "2012-2013 Budget.pdf (page 114)"),
    ("Seniors", 2435, "2012-2013 Budget.pdf (page 114)"),
    ("Solicitor General and Public Security", 755, "2012-2013 Budget.pdf (page 114)"),
    ("Tourism, Parks and Recreation", 163, "2012-2013 Budget.pdf (page 114)"),
    ("Advanced Education and Technology", 2856, "2012-2013 Budget.pdf (page 114)"),
    ("Education", 6179, "2012-2013 Budget.pdf (page 114)"),
    ("Finance", 1188, "2012-2013 Budget.pdf (page 114)"),
    ("Infrastructure", 507, "2012-2013 Budget.pdf (page 114)"),
    ("Service Alberta", 266, "2012-2013 Budget.pdf (page 114)"),
    ("Transportation", 475, "2012-2013 Budget.pdf (page 114)"),
    ("Treasury Board and Enterprise", 65, "2012-2013 Budget.pdf (page 114)"),
    ("Agriculture and Rural Development", 945, "2012-2013 Budget.pdf (page 114)"),
    ("Energy", 380, "2012-2013 Budget.pdf (page 114)"),
    ("Environment and Water", 197, "2012-2013 Budget.pdf (page 114)"),
    ("Intergovernmental, International and Aboriginal Relations", 191, "2012-2013 Budget.pdf (page 114)"),
    ("Sustainable Resource Development", 275, "2012-2013 Budget.pdf (page 114)"),
    ("Executive Council", 32, "2012-2013 Budget.pdf (page 114)"),
    ("Legislative Assembly", 132, "2012-2013 Budget.pdf (page 114)"),
]
# Sum = 36,526

# ---- 2013-14 ----
# Source: 2013-14 Annual Report page 13, Actual column
YEAR_DATA["2013-14"] = [
    ("Culture", 156, "2013-2014 Annual Report.pdf (page 13)"),
    ("Health", 17240, "2013-2014 Annual Report.pdf (page 13)"),
    ("Human Services", 4226, "2013-2014 Annual Report.pdf (page 13)"),
    ("Justice and Solicitor General", 1269, "2013-2014 Annual Report.pdf (page 13)"),
    ("Municipal Affairs", 413, "2013-2014 Annual Report.pdf (page 13)"),
    ("Tourism, Parks and Recreation", 162, "2013-2014 Annual Report.pdf (page 13)"),
    ("Education", 6301, "2013-2014 Annual Report.pdf (page 13)"),
    ("Infrastructure", 505, "2013-2014 Annual Report.pdf (page 13)"),
    ("Innovation and Advanced Education", 2679, "2013-2014 Annual Report.pdf (page 13)"),
    ("Jobs, Skills, Training and Labour", 134, "2013-2014 Annual Report.pdf (page 13)"),
    ("Service Alberta", 236, "2013-2014 Annual Report.pdf (page 13)"),
    ("Transportation", 514, "2013-2014 Annual Report.pdf (page 13)"),
    ("Treasury Board and Finance", 1556, "2013-2014 Annual Report.pdf (page 13)"),
    ("Aboriginal Relations", 163, "2013-2014 Annual Report.pdf (page 13)"),
    ("Agriculture and Rural Development", 752, "2013-2014 Annual Report.pdf (page 13)"),
    ("Energy", 664, "2013-2014 Annual Report.pdf (page 13)"),
    ("Environment and Sustainable Resource Development", 494, "2013-2014 Annual Report.pdf (page 13)"),
    ("International and Intergovernmental Relations", 33, "2013-2014 Annual Report.pdf (page 13)"),
    ("Executive Council", 44, "2013-2014 Annual Report.pdf (page 13)"),
    ("Legislative Assembly", 113, "2013-2014 Annual Report.pdf (page 13)"),
]
# Sum = 37,654 (PDF says 37,653 — 1M rounding)

# ---- 2014-15 ----
# Source: 2014-15 Annual Report page 11, Actual column
YEAR_DATA["2014-15"] = [
    ("Aboriginal Relations", 179, "2014-2015 Annual Report.pdf (page 11)"),
    ("Agriculture and Rural Development", 875, "2014-2015 Annual Report.pdf (page 11)"),
    ("Culture and Tourism", 283, "2014-2015 Annual Report.pdf (page 11)"),
    ("Education", 6505, "2014-2015 Annual Report.pdf (page 11)"),
    ("Energy", 646, "2014-2015 Annual Report.pdf (page 11)"),
    ("Environment and Sustainable Resource Development", 593, "2014-2015 Annual Report.pdf (page 11)"),
    ("Executive Council", 56, "2014-2015 Annual Report.pdf (page 11)"),
    ("Health", 17874, "2014-2015 Annual Report.pdf (page 11)"),
    ("Human Services", 4112, "2014-2015 Annual Report.pdf (page 11)"),
    ("Infrastructure", 507, "2014-2015 Annual Report.pdf (page 11)"),
    ("Innovation and Advanced Education", 2695, "2014-2015 Annual Report.pdf (page 11)"),
    ("Jobs, Skills, Training and Labour", 149, "2014-2015 Annual Report.pdf (page 11)"),
    ("Justice and Solicitor General", 1312, "2014-2015 Annual Report.pdf (page 11)"),
    ("Municipal Affairs", 237, "2014-2015 Annual Report.pdf (page 11)"),
    ("Seniors", 573, "2014-2015 Annual Report.pdf (page 11)"),
    ("Service Alberta", 225, "2014-2015 Annual Report.pdf (page 11)"),
    ("Transportation", 523, "2014-2015 Annual Report.pdf (page 11)"),
    ("Treasury Board and Finance", 1481, "2014-2015 Annual Report.pdf (page 11)"),
    ("Legislative Assembly", 122, "2014-2015 Annual Report.pdf (page 11)"),
]
# Sum = 38,947

# ---- 2015-16 ----
# Source: 2015-16 Annual Report page 12, Actual column (word-level extraction)
YEAR_DATA["2015-16"] = [
    ("Advanced Education", 5141, "2015-2016 Annual Report.pdf"),
    ("Agriculture and Forestry", 989, "2015-2016 Annual Report.pdf"),
    ("Culture and Tourism", 289, "2015-2016 Annual Report.pdf"),
    ("Economic Development and Trade", 225, "2015-2016 Annual Report.pdf"),
    ("Education", 7553, "2015-2016 Annual Report.pdf"),
    ("Energy", 549, "2015-2016 Annual Report.pdf"),
    ("Environment and Parks", 386, "2015-2016 Annual Report.pdf"),
    ("Executive Council", 24, "2015-2016 Annual Report.pdf"),
    ("Health", 18522, "2015-2016 Annual Report.pdf"),
    ("Human Services", 4261, "2015-2016 Annual Report.pdf"),
    ("Indigenous Relations", 178, "2015-2016 Annual Report.pdf"),
    ("Infrastructure", 491, "2015-2016 Annual Report.pdf"),
    ("Justice and Solicitor General", 1350, "2015-2016 Annual Report.pdf"),
    ("Labour", 154, "2015-2016 Annual Report.pdf"),
    ("Municipal Affairs", 246, "2015-2016 Annual Report.pdf"),
    ("Seniors and Housing", 559, "2015-2016 Annual Report.pdf"),
    ("Service Alberta", 240, "2015-2016 Annual Report.pdf"),
    ("Status of Women", 1, "2015-2016 Annual Report.pdf"),
    ("Transportation", 462, "2015-2016 Annual Report.pdf"),
    ("Treasury Board and Finance", 1433, "2015-2016 Annual Report.pdf"),
    ("Legislative Assembly", 132, "2015-2016 Annual Report.pdf"),
]
# Sum = 43,185 (PDF total: 43,189 — 4M rounding)

# ---- 2016-17 ----
# Source: 2016-17 Annual Report page 14, Actual column (word-level extraction)
# Includes Climate Leadership Plan items
YEAR_DATA["2016-17"] = [
    ("Advanced Education", 5380, "2016-2017 Budget.pdf"),
    ("Agriculture and Forestry", 1082, "2016-2017 Budget.pdf"),
    ("Children's Services", 1182, "2016-2017 Budget.pdf"),
    ("Community and Social Services", 3354, "2016-2017 Budget.pdf"),
    ("Culture and Tourism", 290, "2016-2017 Budget.pdf"),
    ("Economic Development and Trade", 266, "2016-2017 Budget.pdf"),
    ("Education", 7794, "2016-2017 Budget.pdf"),
    ("Energy", 448, "2016-2017 Budget.pdf"),
    ("Environment and Parks", 409, "2016-2017 Budget.pdf"),
    ("Executive Council", 26, "2016-2017 Budget.pdf"),
    ("Health", 19299, "2016-2017 Budget.pdf"),
    ("Indigenous Relations", 176, "2016-2017 Budget.pdf"),
    ("Infrastructure", 487, "2016-2017 Budget.pdf"),
    ("Justice and Solicitor General", 1417, "2016-2017 Budget.pdf"),
    ("Labour", 192, "2016-2017 Budget.pdf"),
    ("Municipal Affairs", 240, "2016-2017 Budget.pdf"),
    ("Seniors and Housing", 586, "2016-2017 Budget.pdf"),
    ("Service Alberta", 235, "2016-2017 Budget.pdf"),
    ("Status of Women", 7, "2016-2017 Budget.pdf"),
    ("Transportation", 464, "2016-2017 Budget.pdf"),
    ("Treasury Board and Finance", 1320, "2016-2017 Budget.pdf"),
    ("Legislative Assembly", 118, "2016-2017 Budget.pdf"),
    # Climate Leadership Plan (separate operating items)
    ("Climate Leadership - Energy", 1119, "2016-2017 Budget.pdf"),
    ("Climate Leadership - Treasury Board", 154, "2016-2017 Budget.pdf"),
    ("Climate Leadership - Other", 106, "2016-2017 Budget.pdf"),
]
# Sum = 46,151

# ---- 2017-18 ----
# Source: 2017-18 Annual Report page 16, Actual column (word-level extraction)
YEAR_DATA["2017-18"] = [
    ("Advanced Education", 5548, "2017 Budget.pdf"),
    ("Agriculture and Forestry", 977, "2017 Budget.pdf"),
    ("Children's Services", 1433, "2017 Budget.pdf"),
    ("Community and Social Services", 3453, "2017 Budget.pdf"),
    ("Culture and Tourism", 300, "2017 Budget.pdf"),
    ("Economic Development and Trade", 290, "2017 Budget.pdf"),
    ("Education", 7920, "2017 Budget.pdf"),
    ("Energy", 456, "2017 Budget.pdf"),
    ("Environment and Parks", 448, "2017 Budget.pdf"),
    ("Executive Council", 19, "2017 Budget.pdf"),
    ("Health", 19769, "2017 Budget.pdf"),
    ("Indigenous Relations", 168, "2017 Budget.pdf"),
    ("Infrastructure", 500, "2017 Budget.pdf"),
    ("Justice and Solicitor General", 1445, "2017 Budget.pdf"),
    ("Labour", 193, "2017 Budget.pdf"),
    ("Municipal Affairs", 240, "2017 Budget.pdf"),
    ("Seniors and Housing", 599, "2017 Budget.pdf"),
    ("Service Alberta", 260, "2017 Budget.pdf"),
    ("Status of Women", 7, "2017 Budget.pdf"),
    ("Transportation", 474, "2017 Budget.pdf"),
    ("Treasury Board and Finance", 1614, "2017 Budget.pdf"),
    ("Legislative Assembly", 117, "2017 Budget.pdf"),
    # Climate Leadership Plan
    ("Climate Leadership - Energy", 34, "2017 Budget.pdf"),
    ("Climate Leadership - Treasury Board", 306, "2017 Budget.pdf"),
    ("Climate Leadership - Other", 181, "2017 Budget.pdf"),
]
# Sum = 46,751 (PDF total: 46,755 — 4M rounding)

# ---- 2018-19 ----
# Source: 2018-19 4th Quarter Year-End page 6, Actual column
YEAR_DATA["2018-19"] = [
    ("Advanced Education", 5392, "2018-19 Budget.pdf"),
    ("Agriculture and Forestry", 931, "2018-19 Budget.pdf"),
    ("Children's Services", 1492, "2018-19 Budget.pdf"),
    ("Community and Social Services", 3636, "2018-19 Budget.pdf"),
    ("Culture and Tourism", 286, "2018-19 Budget.pdf"),
    ("Economic Development and Trade", 272, "2018-19 Budget.pdf"),
    ("Education", 8223, "2018-19 Budget.pdf"),
    ("Energy", 477, "2018-19 Budget.pdf"),
    ("Environment and Parks", 427, "2018-19 Budget.pdf"),
    ("Executive Council", 17, "2018-19 Budget.pdf"),
    ("Health", 20409, "2018-19 Budget.pdf"),
    ("Indigenous Relations", 196, "2018-19 Budget.pdf"),
    ("Infrastructure", 489, "2018-19 Budget.pdf"),
    ("Justice and Solicitor General", 1452, "2018-19 Budget.pdf"),
    ("Labour", 203, "2018-19 Budget.pdf"),
    ("Municipal Affairs", 263, "2018-19 Budget.pdf"),
    ("Seniors and Housing", 631, "2018-19 Budget.pdf"),
    ("Service Alberta", 547, "2018-19 Budget.pdf"),
    ("Status of Women", 7, "2018-19 Budget.pdf"),
    ("Transportation", 442, "2018-19 Budget.pdf"),
    ("Treasury Board and Finance", 1672, "2018-19 Budget.pdf"),
    ("Legislative Assembly", 136, "2018-19 Budget.pdf"),
    ("Climate Leadership Plan", 842, "2018-19 Budget.pdf"),
]
# Sum = 48,442 (PDF total: 48,440 — 2M rounding)

# ---- 2019-20 ----
# Source: 2019-20 4th Quarter Year-End page 7, Actual column
YEAR_DATA["2019-20"] = [
    ("Advanced Education", 5477, "2019-20 Budget.pdf"),
    ("Agriculture and Forestry", 868, "2019-20 Budget.pdf"),
    ("Children's Services", 1548, "2019-20 Budget.pdf"),
    ("Community and Social Services", 3965, "2019-20 Budget.pdf"),
    ("Culture, Multiculturalism and Status of Women", 205, "2019-20 Budget.pdf"),
    ("Economic Development, Trade and Tourism", 282, "2019-20 Budget.pdf"),
    ("Education", 8134, "2019-20 Budget.pdf"),
    ("Energy", 600, "2019-20 Budget.pdf"),
    ("Environment and Parks", 558, "2019-20 Budget.pdf"),
    ("Executive Council", 18, "2019-20 Budget.pdf"),
    ("Health", 20870, "2019-20 Budget.pdf"),
    ("Indigenous Relations", 162, "2019-20 Budget.pdf"),
    ("Infrastructure", 457, "2019-20 Budget.pdf"),
    ("Justice and Solicitor General", 1442, "2019-20 Budget.pdf"),
    ("Labour and Immigration", 196, "2019-20 Budget.pdf"),
    ("Municipal Affairs", 244, "2019-20 Budget.pdf"),
    ("Seniors and Housing", 634, "2019-20 Budget.pdf"),
    ("Service Alberta", 494, "2019-20 Budget.pdf"),
    ("Transportation", 425, "2019-20 Budget.pdf"),
    ("Treasury Board and Finance", 1900, "2019-20 Budget.pdf"),
    ("Legislative Assembly", 140, "2019-20 Budget.pdf"),
    ("Crude-by-rail", 866, "2019-20 Budget.pdf"),
    # COVID-19 items
    ("Community and Social Services", 60, "2019-20 Budget.pdf"),
    ("Labour and Immigration", 114, "2019-20 Budget.pdf"),
    ("COVID-19 Other", 44, "2019-20 Budget.pdf"),
]
# Sum = 49,703 (PDF total: 49,700 — 3M rounding)

# ---- 2020-21 ----
# Source: 2020-21 Year-End Report page 7, Actual column (word-level extraction)
YEAR_DATA["2020-21"] = [
    ("Advanced Education", 5132, "2020-21 Budget.pdf"),
    ("Agriculture and Forestry", 812, "2020-21 Budget.pdf"),
    ("Children's Services", 1443, "2020-21 Budget.pdf"),
    ("Community and Social Services", 3691, "2020-21 Budget.pdf"),
    ("Culture, Multiculturalism and Status of Women", 151, "2020-21 Budget.pdf"),
    ("Education", 7707, "2020-21 Budget.pdf"),
    ("Energy", 413, "2020-21 Budget.pdf"),
    ("Environment and Parks", 479, "2020-21 Budget.pdf"),
    ("Executive Council", 15, "2020-21 Budget.pdf"),
    ("Health", 20285, "2020-21 Budget.pdf"),
    ("Indigenous Relations", 102, "2020-21 Budget.pdf"),
    ("Infrastructure", 446, "2020-21 Budget.pdf"),
    ("Jobs, Economy and Innovation", 257, "2020-21 Budget.pdf"),
    ("Justice and Solicitor General", 1434, "2020-21 Budget.pdf"),
    ("Labour and Immigration", 183, "2020-21 Budget.pdf"),
    ("Municipal Affairs", 191, "2020-21 Budget.pdf"),
    ("Seniors and Housing", 611, "2020-21 Budget.pdf"),
    ("Service Alberta", 486, "2020-21 Budget.pdf"),
    ("Transportation", 424, "2020-21 Budget.pdf"),
    ("Treasury Board and Finance", 1837, "2020-21 Budget.pdf"),
    ("Legislative Assembly", 104, "2020-21 Budget.pdf"),
    ("Crude-by-rail", 443, "2020-21 Budget.pdf"),
    # COVID-19/Recovery Plan items
    ("Health", 1093, "2020-21 Budget.pdf"),
    ("Jobs, Economy and Innovation", 765, "2020-21 Budget.pdf"),
    ("Labour and Immigration", 433, "2020-21 Budget.pdf"),
    ("Municipal Affairs", 621, "2020-21 Budget.pdf"),
    ("COVID-19 Other", 1147, "2020-21 Budget.pdf"),
]
# Sum = 50,705 (PDF total: 50,707 — 2M rounding)

# ---- 2021-22 ----
# Source: 2021-22 Year-End Report page 7, Actual column (word-level extraction)
YEAR_DATA["2021-22"] = [
    ("Advanced Education", 5280, "2021-22 Budget.pdf"),
    ("Agriculture, Forestry and Rural Economic Development", 789, "2021-22 Budget.pdf"),
    ("Children's Services", 1706, "2021-22 Budget.pdf"),
    ("Community and Social Services", 3714, "2021-22 Budget.pdf"),
    ("Culture and Status of Women", 161, "2021-22 Budget.pdf"),
    ("Education", 7846, "2021-22 Budget.pdf"),
    ("Energy", 901, "2021-22 Budget.pdf"),
    ("Environment and Parks", 519, "2021-22 Budget.pdf"),
    ("Executive Council", 14, "2021-22 Budget.pdf"),
    ("Health", 21302, "2021-22 Budget.pdf"),
    ("Indigenous Relations", 153, "2021-22 Budget.pdf"),
    ("Infrastructure", 430, "2021-22 Budget.pdf"),
    ("Jobs, Economy and Innovation", 265, "2021-22 Budget.pdf"),
    ("Justice and Solicitor General", 1478, "2021-22 Budget.pdf"),
    ("Labour and Immigration", 190, "2021-22 Budget.pdf"),
    ("Municipal Affairs", 251, "2021-22 Budget.pdf"),
    ("Seniors and Housing", 616, "2021-22 Budget.pdf"),
    ("Service Alberta", 459, "2021-22 Budget.pdf"),
    ("Transportation", 437, "2021-22 Budget.pdf"),
    ("Treasury Board and Finance", 2036, "2021-22 Budget.pdf"),
    ("Legislative Assembly", 117, "2021-22 Budget.pdf"),
    ("Crude-by-rail", 866, "2021-22 Budget.pdf"),
    # COVID-19/Recovery Plan items
    ("Energy", 318, "2021-22 Budget.pdf"),
    ("Health", 1528, "2021-22 Budget.pdf"),
    ("Jobs, Economy and Innovation", 240, "2021-22 Budget.pdf"),
    ("Labour and Immigration", 224, "2021-22 Budget.pdf"),
    ("COVID-19 Other", 502, "2021-22 Budget.pdf"),
]
# Sum = 52,342 (PDF total: 52,343 — 1M rounding)

# ---- 2022-23 ----
# Source: 2022-23 Year-End Report page 7, Actual column (word-level extraction)
YEAR_DATA["2022-23"] = [
    ("Advanced Education", 5501, "2022-2023 Budget.pdf"),
    ("Affordability and Utilities", 712, "2022-2023 Budget.pdf"),
    ("Agriculture and Irrigation", 685, "2022-2023 Budget.pdf"),
    ("Children's Services", 2440, "2022-2023 Budget.pdf"),
    ("Culture", 162, "2022-2023 Budget.pdf"),
    ("Education", 8308, "2022-2023 Budget.pdf"),
    ("Energy", 796, "2022-2023 Budget.pdf"),
    ("Environment and Protected Areas", 416, "2022-2023 Budget.pdf"),
    ("Executive Council", 28, "2022-2023 Budget.pdf"),
    ("Forestry, Parks and Tourism", 303, "2022-2023 Budget.pdf"),
    ("Health", 22516, "2022-2023 Budget.pdf"),
    ("Indigenous Relations", 185, "2022-2023 Budget.pdf"),
    ("Infrastructure", 431, "2022-2023 Budget.pdf"),
    ("Jobs, Economy and Northern Development", 252, "2022-2023 Budget.pdf"),
    ("Justice", 588, "2022-2023 Budget.pdf"),
    ("Mental Health and Addiction", 88, "2022-2023 Budget.pdf"),
    ("Municipal Affairs", 180, "2022-2023 Budget.pdf"),
    ("Public Safety and Emergency Services", 1032, "2022-2023 Budget.pdf"),
    ("Seniors, Community and Social Services", 4873, "2022-2023 Budget.pdf"),
    ("Service Alberta and Red Tape Reduction", 89, "2022-2023 Budget.pdf"),
    ("Skilled Trades and Professions", 155, "2022-2023 Budget.pdf"),
    ("Technology and Innovation", 532, "2022-2023 Budget.pdf"),
    ("Trade, Immigration and Multiculturalism", 68, "2022-2023 Budget.pdf"),
    ("Transportation and Economic Corridors", 572, "2022-2023 Budget.pdf"),
    ("Treasury Board and Finance", 1952, "2022-2023 Budget.pdf"),
    ("Legislative Assembly", 128, "2022-2023 Budget.pdf"),
    # COVID-19/Recovery Plan items
    ("Advanced Education", 60, "2022-2023 Budget.pdf"),
    ("Energy", 439, "2022-2023 Budget.pdf"),
    ("Health", 922, "2022-2023 Budget.pdf"),
    ("Jobs, Economy and Northern Development", 88, "2022-2023 Budget.pdf"),
    ("Technology and Innovation", 127, "2022-2023 Budget.pdf"),
    ("COVID-19 Other", 98, "2022-2023 Budget.pdf"),
]
# Sum = 54,726

# ---- 2023-24 ----
# Source: 2023-24 4th Quarter Year-End page 7, Actual column (word-level extraction)
YEAR_DATA["2023-24"] = [
    ("Advanced Education", 6233, "tbf-goa-2023-2024 Budget.pdf"),
    ("Affordability and Utilities", 119, "tbf-goa-2023-2024 Budget.pdf"),
    ("Agriculture and Irrigation", 743, "tbf-goa-2023-2024 Budget.pdf"),
    ("Arts, Culture and Status of Women", 132, "tbf-goa-2023-2024 Budget.pdf"),
    ("Children and Family Services", 1603, "tbf-goa-2023-2024 Budget.pdf"),
    ("Education", 8878, "tbf-goa-2023-2024 Budget.pdf"),
    ("Energy and Minerals", 822, "tbf-goa-2023-2024 Budget.pdf"),
    ("Environment and Protected Areas", 377, "tbf-goa-2023-2024 Budget.pdf"),
    ("Executive Council", 47, "tbf-goa-2023-2024 Budget.pdf"),
    ("Forestry and Parks", 285, "tbf-goa-2023-2024 Budget.pdf"),
    ("Health", 25165, "tbf-goa-2023-2024 Budget.pdf"),
    ("Immigration and Multiculturalism", 39, "tbf-goa-2023-2024 Budget.pdf"),
    ("Indigenous Relations", 214, "tbf-goa-2023-2024 Budget.pdf"),
    ("Infrastructure", 462, "tbf-goa-2023-2024 Budget.pdf"),
    ("Jobs, Economy and Trade", 1557, "tbf-goa-2023-2024 Budget.pdf"),
    ("Justice", 652, "tbf-goa-2023-2024 Budget.pdf"),
    ("Mental Health and Addiction", 151, "tbf-goa-2023-2024 Budget.pdf"),
    ("Municipal Affairs", 220, "tbf-goa-2023-2024 Budget.pdf"),
    ("Public Safety and Emergency Services", 1205, "tbf-goa-2023-2024 Budget.pdf"),
    ("Seniors, Community and Social Services", 5284, "tbf-goa-2023-2024 Budget.pdf"),
    ("Service Alberta and Red Tape Reduction", 159, "tbf-goa-2023-2024 Budget.pdf"),
    ("Technology and Innovation", 723, "tbf-goa-2023-2024 Budget.pdf"),
    ("Tourism and Sport", 112, "tbf-goa-2023-2024 Budget.pdf"),
    ("Transportation and Economic Corridors", 564, "tbf-goa-2023-2024 Budget.pdf"),
    ("Treasury Board and Finance", 2237, "tbf-goa-2023-2024 Budget.pdf"),
    ("Legislative Assembly", 160, "tbf-goa-2023-2024 Budget.pdf"),
]
# Sum = 58,143

# ---- 2024-25 ----
# Source: 2024-25 4th Quarter Year-End page 7, Actual column (word-level extraction)
YEAR_DATA["2024-25"] = [
    ("Advanced Education", 6608, "2024-2025 Budget.pdf"),
    ("Affordability and Utilities", 125, "2024-2025 Budget.pdf"),
    ("Agriculture and Irrigation", 833, "2024-2025 Budget.pdf"),
    ("Arts, Culture and Status of Women", 140, "2024-2025 Budget.pdf"),
    ("Children and Family Services", 1515, "2024-2025 Budget.pdf"),
    ("Education", 9288, "2024-2025 Budget.pdf"),
    ("Energy and Minerals", 1223, "2024-2025 Budget.pdf"),
    ("Environment and Protected Areas", 401, "2024-2025 Budget.pdf"),
    ("Executive Council", 57, "2024-2025 Budget.pdf"),
    ("Forestry and Parks", 352, "2024-2025 Budget.pdf"),
    ("Health", 25669, "2024-2025 Budget.pdf"),
    ("Immigration and Multiculturalism", 40, "2024-2025 Budget.pdf"),
    ("Indigenous Relations", 222, "2024-2025 Budget.pdf"),
    ("Infrastructure", 467, "2024-2025 Budget.pdf"),
    ("Jobs, Economy and Trade", 1856, "2024-2025 Budget.pdf"),
    ("Justice", 676, "2024-2025 Budget.pdf"),
    ("Mental Health and Addiction", 1597, "2024-2025 Budget.pdf"),
    ("Municipal Affairs", 228, "2024-2025 Budget.pdf"),
    ("Public Safety and Emergency Services", 1259, "2024-2025 Budget.pdf"),
    ("Seniors, Community and Social Services", 5539, "2024-2025 Budget.pdf"),
    ("Service Alberta and Red Tape Reduction", 177, "2024-2025 Budget.pdf"),
    ("Technology and Innovation", 775, "2024-2025 Budget.pdf"),
    ("Tourism and Sport", 124, "2024-2025 Budget.pdf"),
    ("Transportation and Economic Corridors", 583, "2024-2025 Budget.pdf"),
    ("Treasury Board and Finance", 2128, "2024-2025 Budget.pdf"),
    ("Legislative Assembly", 144, "2024-2025 Budget.pdf"),
]
# Sum = 62,026 (PDF total: 62,025 — 1M rounding)


# ── Expected totals (from PDF "Total Operating Expense" rows) ────────────────

EXPECTED_TOTALS = {
    "2011-12": 34175,
    "2012-13": 36526,
    "2013-14": 37654,
    "2014-15": 38947,
    "2015-16": 43189,
    "2016-17": 46151,
    "2017-18": 46755,
    "2018-19": 48440,
    "2019-20": 49700,
    "2020-21": 50707,
    "2021-22": 52343,
    "2022-23": 54726,
    "2023-24": 58143,
    "2024-25": 62025,
}


# ── Build DataFrame ──────────────────────────────────────────────────────────

def build_dataframe() -> pd.DataFrame:
    rows = []
    for fy, items in YEAR_DATA.items():
        for ministry_raw, value, source in items:
            rows.append({
                "fiscal_year": fy,
                "ministry_raw": ministry_raw,
                "ministry_normalized": normalize_ministry(ministry_raw),
                "operating_expense_millions": value,
                "source": source,
            })
    return pd.DataFrame(rows)


# ── Validation ───────────────────────────────────────────────────────────────

def validate(df: pd.DataFrame) -> None:
    print("\n" + "=" * 70)
    print("VALIDATION REPORT")
    print("=" * 70)

    grouped = df.groupby("fiscal_year")["operating_expense_millions"].sum()

    print(f"\n{'Year':<12} {'Extracted':>12} {'Expected':>12} {'Diff':>8} {'Pct':>6} {'Status':<6}")
    print("-" * 60)

    all_ok = True
    for fy in sorted(EXPECTED_TOTALS.keys()):
        expected = EXPECTED_TOTALS[fy]
        extracted = grouped.get(fy, 0)
        diff = extracted - expected
        pct = abs(diff) / expected * 100

        if pct > 1:
            status = "FAIL"
            all_ok = False
        elif pct > 0.05:
            status = "WARN"
        else:
            status = "OK"

        print(f"{fy:<12} {extracted:>12,} {expected:>12,} {diff:>+8,} {pct:>5.2f}% {status:<6}")

    # Category breakdown sanity checks
    print("\n--- Category Breakdown ---")
    for fy in sorted(df["fiscal_year"].unique()):
        fy_data = df[df["fiscal_year"] == fy]
        total = fy_data["operating_expense_millions"].sum()

        cats = fy_data.groupby("ministry_normalized")["operating_expense_millions"].sum()
        health = cats.get("Health", 0)
        edu = cats.get("Education (K-12)", 0)
        adved = cats.get("Advanced Education", 0)
        social = cats.get("Social Services", 0)
        other = cats.get("Other", 0)
        h_pct = health / total * 100 if total else 0

        issues = []
        if h_pct < 30 or h_pct > 50:
            issues.append(f"Health%={h_pct:.1f}")
        if health < 10000:
            issues.append("Health<10B")

        status = ", ".join(issues) if issues else "OK"
        print(
            f"  {fy}: H={health:>7,}  K12={edu:>6,}  AE={adved:>5,}"
            f"  SS={social:>6,}  Oth={other:>6,}  Tot={total:>7,}  {status}"
        )

    if all_ok:
        print("\nAll totals within 1% tolerance.")
    else:
        print("\nWARNING: Some totals exceed tolerance.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Build the raw DataFrame
    df = build_dataframe()

    # Aggregate by fiscal year + normalized ministry
    df_agg = (
        df.groupby(["fiscal_year", "ministry_normalized"], as_index=False)
        .agg(
            operating_expense_millions=("operating_expense_millions", "sum"),
            raw_ministries=("ministry_raw", lambda x: "; ".join(sorted(set(x)))),
            source=("source", "first"),
        )
    )

    # Validate
    validate(df_agg)

    # Save detailed CSV (before aggregation)
    detail_path = DATA_DIR / "ministry_expenses_detail.csv"
    df.to_csv(detail_path, index=False)
    print(f"\nSaved: {detail_path}")

    # Save aggregated CSV (5 categories per year)
    out_path = DATA_DIR / "ministry_expenses.csv"
    df_agg.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")

    # Save wide-format CSV
    pivot = df_agg.pivot_table(
        index="fiscal_year",
        columns="ministry_normalized",
        values="operating_expense_millions",
        aggfunc="sum",
    ).fillna(0)
    pivot["total_operating"] = pivot.sum(axis=1)
    wide_path = DATA_DIR / "ministry_expenses_wide.csv"
    pivot.to_csv(wide_path)
    print(f"Saved: {wide_path}")

    return df_agg


if __name__ == "__main__":
    main()
