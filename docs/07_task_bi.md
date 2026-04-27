# 07_task_bi.md

## Goal

Prepare outputs for business reporting.

---

## Deliverables

* BI-ready tables in `reports/tables/`
* BI-ready figures in `reports/figures/`
* Executive summary in `reports/executive_summary.md`

---

## Required Outputs

* Churn rate summary
* Segment-level churn analysis
* High-risk customer list
* Model performance summary

At minimum, produce:

* one overall churn KPI table
* at least two segment-level churn tables
* at least two business-friendly figures
* one high-risk customer export for operational follow-up
* one executive summary in plain business language

---

## Suggested Output Files

Tables in `reports/tables/`:

* `churn_rate_summary.csv`
* `churn_by_segment.csv`
* `model_metrics_summary.csv`
* `high_risk_customers.csv`

Figures in `reports/figures/`:

* `churn_overview.png`
* `churn_by_segment.png`

Executive summary:

* `reports/executive_summary.md`

---

## Requirements

* Business-friendly language
* Clear KPIs
* Clean, structured tables
* Consistent naming across tables, figures, and narrative
* Clear distinction between observed churn patterns and model predictions
* No overclaiming insights

---

## KPI Expectations

Include KPIs such as:

* overall churn rate
* customer counts by segment
* churn rate by segment
* model performance metrics used for business reporting
* count of high-risk customers based on model predictions

Use labels that are understandable to non-technical stakeholders.

---

## Segment Analysis

Include segment-level analysis for relevant business dimensions, for example:

* card category
* income category
* age bands
* tenure bands
* activity or transaction behavior

Explain which segments appear to have higher churn and which findings are descriptive versus model-based.

---

## High-Risk Customer Export

The high-risk customer output should be ready for BI or operational use.

If available, include:

* `CLIENTNUM`
* churn probability
* predicted class
* key segmentation fields useful for follow-up

Document the threshold used to define a customer as high risk.

---

## Executive Summary

The executive summary should be short, clear, and business-oriented.

Suggested sections:

* business objective
* key churn insights
* high-risk segments or customers
* model performance summary
* assumptions and limitations
* recommended next actions

---

## Notes

* Separate descriptive vs model-based insights
* Focus on clarity
* Avoid causal claims unless they are explicitly supported
* State important assumptions, filters, and thresholds used in the outputs
