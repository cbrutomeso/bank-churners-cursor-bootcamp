# 03_success_criteria.md

## Definition of Done

A task is complete ONLY if:

* Code runs end-to-end
* Outputs are generated (artifacts or reports)
* Results are reproducible
* Assumptions are explicitly stated
* No obvious data leakage
* Outputs are interpretable

---

## EDA

* Includes data quality checks
* Includes churn-focused analysis
* Includes clear written insights
* Avoids causal claims

---

## Modeling

* Includes a baseline model
* Uses proper data split
* Preserves target class proportion during splitting
* Evaluates on holdout data
* Reports metrics clearly
* Uses `ROC-AUC` as the primary ranking metric
* Reports `precision`, `recall`, and `F1` for the churn class
* Final model improves on the baseline on validation and keeps that improvement on test
* Target test `ROC-AUC >= 0.80`
* Target churn-class `recall >= 0.60` at the selected decision threshold
* Final decision threshold is explicitly justified
* Final model choice is explicitly justified
* Includes a feature importance plot or equivalent interpretation for the final model
* Mentions limitations

---

## App

* Runs locally
* Handles invalid input safely
* Produces predictions
* Displays limitations

---

## Reporting

* Clear KPIs
* Business-friendly language
* Clean tables for BI
* No exaggerated conclusions
