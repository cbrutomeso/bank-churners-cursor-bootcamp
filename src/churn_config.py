"""Shared paths and column rules for Bank Churners (EDA and modeling)."""

from __future__ import annotations

from pathlib import Path

# Repository root (parent of `src/`)
REPO_ROOT = Path(__file__).resolve().parent.parent

RAW_CSV_PATH = REPO_ROOT / "data" / "raw" / "BankChurners.csv"
FIGURES_DIR = REPO_ROOT / "reports" / "figures"

TARGET_COLUMN = "Attrition_Flag"
CHURN_COLUMN = "churn"
ID_COLUMN = "CLIENTNUM"

ATTRITED_LABEL = "Attrited Customer"
EXISTING_LABEL = "Existing Customer"

# Documented in docs/02_dataset_dictionary.md — exclude from training if present.
LEAKAGE_COLUMNS: tuple[str, ...] = (
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2",
)

NUMERICAL_COLUMNS: tuple[str, ...] = (
    "Customer_Age",
    "Dependent_count",
    "Credit_Limit",
    "Total_Revolving_Bal",
    "Avg_Open_To_Buy",
    "Months_on_book",
    "Total_Relationship_Count",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Total_Amt_Chng_Q4_Q1",
    "Total_Ct_Chng_Q4_Q1",
    "Avg_Utilization_Ratio",
)

# Discrete counts — histograms instead of KDE
DISCRETE_NUMERICAL_COLUMNS: tuple[str, ...] = (
    "Dependent_count",
    "Total_Relationship_Count",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Total_Trans_Ct",
)

CATEGORICAL_COLUMNS: tuple[str, ...] = (
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
)

ORDINAL_COLUMNS: tuple[str, ...] = (
    "Income_Category",
    "Education_Level",
    "Card_Category",
)

NOMINAL_COLUMNS: tuple[str, ...] = (
    "Gender",
    "Marital_Status",
)

# Ordinal mappings start at 1; Unknown kept as NaN for explicit handling in modeling.
INCOME_CATEGORY_ORDER: dict[str, int] = {
    "Less than $40K": 1,
    "$40K - $60K": 2,
    "$60K - $80K": 3,
    "$80K - $120K": 4,
    "$120K +": 5,
}

EDUCATION_LEVEL_ORDER: dict[str, int] = {
    "Uneducated": 1,
    "High School": 1,
    "College": 2,
    "Graduate": 3,
    "Post-Graduate": 4,
    "Doctorate": 5,
}

CARD_CATEGORY_ORDER: dict[str, int] = {
    "Blue": 1,
    "Silver": 2,
    "Gold": 3,
    "Platinum": 4,
}

ORDINAL_MAPPINGS: dict[str, dict[str, int]] = {
    "Income_Category": INCOME_CATEGORY_ORDER,
    "Education_Level": EDUCATION_LEVEL_ORDER,
    "Card_Category": CARD_CATEGORY_ORDER,
}

BIVARIATE_NUMERICAL: tuple[str, ...] = (
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Avg_Utilization_Ratio",
    "Months_on_book",
)

BIVARIATE_CATEGORICAL: tuple[str, ...] = (
    "Income_Category",
    "Card_Category",
    "Education_Level",
    "Marital_Status",
)

COLUMNS_WITH_UNKNOWN: tuple[str, ...] = (
    "Education_Level",
    "Income_Category",
    "Marital_Status",
)

# Plot defaults (colorblind-friendly)
RANDOM_SEED = 42
FIGURE_DPI = 120
FIGURE_FACECOLOR = "white"
SEABORN_PALETTE = "colorblind"
CHURN_HUE_LABELS = {0: "Existing", 1: "Churned"}


def exclude_from_modeling_columns(columns: list[str] | tuple[str, ...]) -> list[str]:
    """Return identifier + any leakage columns that exist in ``columns``."""
    cols = set(columns)
    out = []
    if ID_COLUMN in cols:
        out.append(ID_COLUMN)
    for name in LEAKAGE_COLUMNS:
        if name in cols:
            out.append(name)
    return out
