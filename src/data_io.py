"""Load and prepare the Bank Churners raw dataset for EDA and modeling."""

from __future__ import annotations

import pandas as pd

from churn_config import (
    ATTRITED_LABEL,
    CHURN_COLUMN,
    RAW_CSV_PATH,
    TARGET_COLUMN,
    exclude_from_modeling_columns,
)

CATEGORICAL_STR_COLUMNS = (
    "Attrition_Flag",
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
)


def load_raw_churners(
    path: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the raw CSV and return (full_df, analysis_df).

    * ``full_df`` includes all columns from the file plus binary ``churn``.
    * ``analysis_df`` drops identifier and leakage columns when present.
    """
    csv_path = RAW_CSV_PATH if path is None else path
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    for col in CATEGORICAL_STR_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df[CHURN_COLUMN] = (df[TARGET_COLUMN] == ATTRITED_LABEL).astype(int)

    drop_cols = exclude_from_modeling_columns(df.columns)
    analysis_df = df.drop(columns=drop_cols, errors="ignore").copy()

    return df, analysis_df


def churn_rate(df: pd.DataFrame) -> float:
    """Return fraction of attrited customers (0–1)."""
    return float(df[CHURN_COLUMN].mean())


def quality_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Build a compact data-quality summary table."""
    rows = []
    for col in df.columns:
        if col == CHURN_COLUMN:
            continue
        series = df[col]
        unknown_n = int((series.astype(str) == "Unknown").sum()) if series.dtype == object else 0
        rows.append(
            {
                "column": col,
                "dtype": str(series.dtype),
                "missing": int(series.isna().sum()),
                "unknown": unknown_n,
                "n_unique": int(series.nunique(dropna=True)),
            }
        )
    return pd.DataFrame(rows)
