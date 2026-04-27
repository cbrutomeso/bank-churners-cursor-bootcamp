# 04_task_eda.md

## Goal

Understand the dataset and identify potential churn drivers.

---

## Questions

* What is the churn rate?
* Which variables differ most between churn vs non-churn?
* Are there strong behavioral patterns?
* Are there data quality issues?

---

## Deliverables

* Notebook: `notebooks/01_eda.ipynb`

* At least 20 meaningful charts, including:

  * target distribution
  * key numerical variables
  * key categorical variables
  * churn vs feature comparisons
  * correlation analysis including the target

* Charts must be saved to `reports/figures/`

* Written insights:

  * short, clear interpretation for each key chart
  * summary of main churn drivers

* Outputs:

  * list of candidate features for modeling
  * list of candidate feature engineering decisions to carry into modeling
  * list of data quality issues

* Optional:

  * initial hypotheses about churn behavior

---

## Requirements

### Analysis

* Include data quality checks:

  * missing values
  * inconsistent categories
  * outliers

* Include:

  * univariate analysis
  * bivariate analysis vs churn

* Keep the distinction clear:

  * univariate analysis = study each variable on its own
  * bivariate analysis = study the relationship between one variable and the target

* Use chart types intelligently:

  * for continuous numerical variables, prefer density-style plots such as KDE when the distribution is meaningful to inspect smoothly
  * for discrete numerical variables, prefer histograms or count-based plots
  * for categorical variables, prefer proportion charts or count plots that make category comparisons easy to read
  * add a correlation heatmap that includes the target in numeric form

* For categorical analysis and preparation:

  * identify ordinal categorical variables and document an ordinal numeric mapping that starts at `1` and increases with hierarchy
  * identify nominal categorical variables and document that they should be encoded with `N-1` dummies for modeling to avoid perfect multicollinearity
  * be explicit about which variables are ordinal versus nominal and justify the choice when needed

* Add interpretation for key charts (not just plots)

* Explicitly document candidate feature engineering decisions, such as:

  * handling of "Unknown" categories
  * encoding considerations
  * ordinal mappings
  * nominal dummy encoding with `N-1` dummies
  * outlier treatment ideas
  * variables to exclude because of leakage or weak business meaning

* Explicitly flag:

  * potential leakage variables
  * suspicious or derived features

---

### Format (Important)

* Structure the notebook clearly with sections:

  * Data Loading
  * Data Quality
  * Univariate Analysis
  * Bivariate Analysis
  * Key Insights

* Each chart must include:

  * a clear title
  * labeled axes
  * readable formatting

* Use consistent styling across plots
* Use color palettes and chart formatting that are accessible and colorblind-friendly
* Do not rely on color alone to communicate the main message when labels, ordering, or annotations can help

* Each key chart must be followed by a short markdown explanation

* Keep the notebook readable and presentation-ready

---

## Constraints

* Do NOT assume causality (correlation ≠ causation)
* Keep explanations clear, simple, and business-friendly
* Avoid overcomplicated visualizations
* Prefer accessible visual design over decorative styling
