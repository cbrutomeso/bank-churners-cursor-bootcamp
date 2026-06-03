# Final Report — Bank Customer Churn

## Executive summary

This project built an end-to-end churn analytics workflow: exploratory analysis, a validated prediction model, BI-ready reporting, and a Streamlit app for single and batch scoring. The portfolio shows **16.1% observed churn** (10,127 customers). A **LightGBM** model ranks customers by churn probability (test ROC-AUC **0.992**, churn recall **0.86** at the selected threshold). **1,594 customers** are flagged as high risk for proactive retention. Patterns are **associational**, not causal.

---

## Business problem

The bank wants to reduce credit-card attrition by:

1. Understanding which segments exhibit higher historical churn.
2. Predicting which active customers are most likely to churn next.
3. Equipping retention teams with actionable lists and a simple scoring tool.

Success is measured by better prioritization of outreach, not by replacing relationship managers.

---

## EDA insights (descriptive)

Evidence: `notebooks/01_eda.ipynb`, `reports/figures/`, `reports/tables/eda_data_quality_summary.csv`.

| Finding | Implication |
|---------|-------------|
| Churn rate ~16% | Class imbalance — use recall-aware metrics and stratified splits |
| Behavioral variables (inactivity, contacts, transactions) differ by churn status | Strong candidates for modeling; monitor in campaigns |
| Unknown categories in education/income | Document encoding; do not drop silently |
| Naive Bayes classifier columns present | **Excluded** — leakage risk |
| Correlation among credit variables | Watch multicollinearity in interpretation |

Key figures: `target_distribution.png`, `correlation_heatmap_with_target.png`, bivariate boxplots for inactivity and transactions.

*These insights describe historical labels; they do not prove that changing one variable will cause retention.*

---

## Modeling approach

Evidence: `notebooks/02_modeling.ipynb`, `artifacts/models/churn_model_pipeline.joblib`.

| Step | Choice |
|------|--------|
| Split | 70% train / 15% validation / 15% test, stratified |
| Baseline | Logistic regression |
| Candidates | Random Forest, XGBoost, LightGBM |
| Tuning | Optuna (25 trials/model), optimize validation ROC-AUC |
| Preprocessing | Scale numerics; ordinal education/income; N-1 dummies for nominal fields |
| Selection | Highest validation ROC-AUC among models beating baseline |
| Threshold | Validation scan targeting churn recall ≥ 0.60 |

**Final model:** LightGBM  
**Decision threshold:** 0.50 (from saved artifact)

---

## Model performance

Evidence: `reports/tables/modeling_final_metrics.csv`, `modeling_final_selection.csv`, `model_metrics_summary.csv`.

| Split | ROC-AUC | Precision (churn) | Recall (churn) | F1 |
|-------|---------|-------------------|----------------|-----|
| Validation | 0.995 | 0.952 | 0.889 | 0.919 |
| Test (holdout) | **0.992** | 0.921 | **0.857** | 0.887 |

The final model beats the logistic baseline on validation and test AUC. Train metrics near 1.0 suggest some overfitting — treat scores as **ranking**, monitor drift, and retrain periodically.

---

## Churn drivers (model interpretation)

Evidence: `reports/figures/modeling_feature_importance.png`, `reports/tables/modeling_feature_importance.csv`.

Top contributors in the selected tree model typically include:

- Months inactive (12 months)
- Transaction counts and amounts
- Relationship count and utilization
- Change metrics (Q4 vs Q1)

Use drivers to **prioritize hypotheses** for retention design, not as causal levers without experiments.

---

## High-risk customer insights

Evidence: `reports/tables/high_risk_customers.csv`, `churn_by_segment.csv`, `reports/figures/churn_by_segment.png`.

**Observed churn (historical):**

- Higher rates in some **Platinum** and **high-inactivity** bands.

**Model-based risk (threshold 0.50):**

- **1,594** customers flagged (~15.7% of portfolio).
- Elevated average predicted risk in inactive and premium card bands.

Operational file for CRM/BI: `reports/tables/high_risk_customers.csv` (includes `CLIENTNUM`, probability, prediction, segment fields).

---

## Production simulation (Streamlit)

Evidence: `app/streamlit_app.py`, `data/processed/sample_batch_prediction_input.csv`.

- **Single Prediction:** form-based scoring with probability, class 0/1, and color-coded risk labels.
- **Batch Prediction:** CSV upload, validation, downloadable results; sample file provided.
- Logs appended to `artifacts/logs/prediction_log.csv` (timestamp + mode).

Run locally:

```powershell
streamlit run app/streamlit_app.py
```

---

## Limitations

- Snapshot data; no time-to-churn modeling.
- High AUC on this dataset may reflect separable patterns; validate on new cohorts.
- Threshold trades false alarms vs missed churners — align with business capacity.
- Correlation ≠ causation; pilot interventions before scaling offers.

---

## Recommendations and next steps

1. **Immediate:** Distribute `high_risk_customers.csv` to retention teams for outreach pilots.
2. **Segment plays:** Target high-inactivity and premium-card segments with tailored offers.
3. **Governance:** Quarterly threshold review with precision/recall and contact-capacity constraints.
4. **Monitoring:** Track monthly churn, score drift, and campaign uplift.
5. **Iteration:** A/B test interventions; retrain model when feature distributions shift.

---

## Project artifacts index

| Area | Location |
|------|----------|
| EDA | `notebooks/01_eda.ipynb` |
| Modeling | `notebooks/02_modeling.ipynb` |
| BI | `notebooks/03_bi_reporting.ipynb` |
| Model | `artifacts/models/churn_model_pipeline.joblib` |
| Predictions | `artifacts/predictions/` |
| BI tables | `reports/tables/churn_*.csv`, `high_risk_customers.csv`, **`power_bi_master.csv`** (Power BI) |
| Executive summary | `reports/executive_summary.md` |
| App | `app/streamlit_app.py` |
