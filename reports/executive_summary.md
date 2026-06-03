# Executive Summary — Bank Customer Churn

## Business objective
Reduce preventable attrition by prioritizing retention actions on customers with the highest predicted churn risk and the segments with the highest observed churn.

## Key churn insights (observed)
- Portfolio size: **10,127** customers.
- Observed churn rate: **16.07%** (1,627 attrited customers).
- Highest observed churn segments:
- card_category = Platinum (20 customers): **25.0%** observed churn
- inactivity_band = 4-6 mo (737 customers): **24.6%** observed churn
- inactivity_band = 2-3 mo (7128 customers): **18.7%** observed churn

## High-risk segments and customers (model-based)
- High-risk threshold: **0.500** predicted churn probability.
- Customers flagged for follow-up: **1,594** (15.74% of portfolio).
- Segments with highest average predicted risk:
- card_category = Platinum (20 customers): **25.0%** average predicted risk
- inactivity_band = 4-6 mo (737 customers): **23.8%** average predicted risk
- card_category = Gold (116 customers): **18.9%** average predicted risk
- **Power BI (single file):** import `reports/tables/power_bi_master.csv` (one row per customer with observed churn, scores, and segment bands).

## Model performance summary
Holdout test metrics for **lightgbm**: ROC-AUC 0.992, recall 0.857, precision 0.921.

## Assumptions and limitations
- Observed churn reflects historical labels; it is not proof of future behavior.
- Model scores rank relative risk; they should be combined with policy and capacity constraints.
- Segment bands (age, tenure, inactivity) use fixed business bins defined in this notebook.
- Naive Bayes leakage columns are excluded from scoring, consistent with EDA and modeling rules.
- Patterns are associative, not causal.

## Recommended next actions
1. Route `high_risk_customers.csv` to retention teams for proactive outreach.
2. Design offers for the top observed-churn segments while monitoring contact fatigue.
3. Review threshold trade-offs (precision vs recall) with stakeholders quarterly.
4. Refresh scores when new customers or retrained models are available.
