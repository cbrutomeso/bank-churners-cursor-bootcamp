"""Plotting helpers for Bank Churners EDA."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from churn_config import (
    CHURN_COLUMN,
    DISCRETE_NUMERICAL_COLUMNS,
    EXISTING_LABEL,
    FIGURE_DPI,
    FIGURE_FACECOLOR,
    FIGURES_DIR,
    SEABORN_PALETTE,
    TARGET_COLUMN,
)

_figure_counter = 0
# When False, figures stay open so the notebook can call plt.show() before plt.close().
AUTO_CLOSE = True


def reset_figure_counter(start: int = 0) -> None:
    """Reset auto-numbering for saved figures (useful in tests)."""
    global _figure_counter
    _figure_counter = start


def apply_plot_style() -> None:
    """Set consistent, accessible matplotlib/seaborn defaults."""
    sns.set_theme(style="whitegrid", palette=SEABORN_PALETTE)
    plt.rcParams.update(
        {
            "figure.dpi": FIGURE_DPI,
            "figure.facecolor": FIGURE_FACECOLOR,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
        }
    )


def save_figure(fig: plt.Figure, slug: str, figures_dir: Path | None = None) -> Path:
    """Save figure as zero-padded PNG under ``reports/figures/``."""
    global _figure_counter
    _figure_counter += 1
    out_dir = FIGURES_DIR if figures_dir is None else figures_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{_figure_counter:02d}_{slug}.png"
    fig.savefig(path, bbox_inches="tight", dpi=FIGURE_DPI, facecolor=FIGURE_FACECOLOR)
    if AUTO_CLOSE:
        plt.close(fig)
    return path


def plot_target_distribution(df: pd.DataFrame, slug: str = "target_distribution") -> Path:
    """Bar chart of attrition flag counts."""
    apply_plot_style()
    counts = df[TARGET_COLUMN].value_counts().reindex([EXISTING_LABEL, "Attrited Customer"])
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(counts.index.astype(str), counts.values, color=sns.color_palette(SEABORN_PALETTE, 2))
    ax.set_title("Customer attrition distribution")
    ax.set_xlabel("Attrition flag")
    ax.set_ylabel("Count")
    for bar, val in zip(bars, counts.values):
        ax.annotate(f"{val:,}", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha="center", va="bottom", fontsize=9)
    return save_figure(fig, slug)


def plot_univariate_numeric(
    df: pd.DataFrame,
    column: str,
    slug: str | None = None,
) -> Path:
    """KDE for continuous numerics; histogram for discrete counts."""
    apply_plot_style()
    slug = slug or f"uni_{column.lower()}"
    series = df[column].dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    if column in DISCRETE_NUMERICAL_COLUMNS:
        sns.histplot(series, bins=min(int(series.max()) + 1, 30), kde=False, ax=ax, color=sns.color_palette(SEABORN_PALETTE)[0])
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")
    else:
        sns.kdeplot(series, fill=True, ax=ax, color=sns.color_palette(SEABORN_PALETTE)[0], linewidth=2)
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Density")
    return save_figure(fig, slug)


def plot_univariate_categorical(
    df: pd.DataFrame,
    column: str,
    slug: str | None = None,
) -> Path:
    """Proportion bar chart for a categorical column."""
    apply_plot_style()
    slug = slug or f"uni_{column.lower()}"
    props = df[column].value_counts(normalize=True).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=props.index.astype(str), y=props.values, ax=ax, color=sns.color_palette(SEABORN_PALETTE)[0])
    ax.set_title(f"Proportion by {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Proportion")
    ax.set_ylim(0, min(1.0, props.max() * 1.15))
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    for i, (cat, val) in enumerate(props.items()):
        ax.annotate(f"{val:.1%}", xy=(i, val), ha="center", va="bottom", fontsize=8)
    return save_figure(fig, slug)


def plot_bivariate_numeric(
    df: pd.DataFrame,
    column: str,
    slug: str | None = None,
) -> Path:
    """Overlay KDE or box plot of a numeric feature by churn status."""
    apply_plot_style()
    slug = slug or f"bivar_{column.lower()}_by_churn"
    plot_df = df[[column, CHURN_COLUMN]].dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    if column in DISCRETE_NUMERICAL_COLUMNS:
        sns.boxplot(data=plot_df, x=CHURN_COLUMN, y=column, ax=ax, palette=SEABORN_PALETTE)
        ax.set_xticklabels(["Existing", "Churned"])
    else:
        for churn_val, label in [(0, "Existing"), (1, "Churned")]:
            subset = plot_df.loc[plot_df[CHURN_COLUMN] == churn_val, column]
            sns.kdeplot(subset, ax=ax, label=label, linewidth=2)
        ax.legend(title="Status")
    ax.set_title(f"{column} by churn status")
    ax.set_xlabel("Churned (1) vs existing (0)" if column in DISCRETE_NUMERICAL_COLUMNS else column)
    if column in DISCRETE_NUMERICAL_COLUMNS:
        ax.set_xlabel("Customer status")
    return save_figure(fig, slug)


def plot_bivariate_categorical(
    df: pd.DataFrame,
    column: str,
    slug: str | None = None,
) -> Path:
    """Grouped churn rate by category."""
    apply_plot_style()
    slug = slug or f"bivar_{column.lower()}_churn_rate"
    rates = (
        df.groupby(column, observed=True)[CHURN_COLUMN]
        .mean()
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=rates.index.astype(str), y=rates.values, ax=ax, color=sns.color_palette(SEABORN_PALETTE)[1])
    ax.set_title(f"Churn rate by {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Churn rate")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    for i, val in enumerate(rates.values):
        ax.annotate(f"{val:.1%}", xy=(i, val), ha="center", va="bottom", fontsize=8)
    return save_figure(fig, slug)


def plot_correlation_heatmap(
    df: pd.DataFrame,
    numeric_columns: list[str],
    slug: str = "correlation_heatmap",
) -> Path:
    """Correlation matrix heatmap including binary churn."""
    apply_plot_style()
    cols = [c for c in numeric_columns if c in df.columns]
    if CHURN_COLUMN not in cols and CHURN_COLUMN in df.columns:
        cols = cols + [CHURN_COLUMN]
    corr = df[cols].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        square=True,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Pearson r"},
    )
    ax.set_title("Correlation heatmap (numeric features + churn)")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    plt.setp(ax.get_yticklabels(), rotation=0)
    return save_figure(fig, slug)


def outlier_flags_iqr(df: pd.DataFrame, column: str, k: float = 1.5) -> pd.Series:
    """Return boolean mask for rows outside Tukey IQR fences."""
    q1, q3 = df[column].quantile(0.25), df[column].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return (df[column] < lower) | (df[column] > upper)
