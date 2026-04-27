# 05_task_modeling.md

## Goal

Build a churn prediction model.

---

## Steps

* Define a fixed train / validation / test split
* Prepare features and preprocessing pipeline
* Train a baseline model
* Train the required advanced models
* Tune each model with Bayesian optimization using Optuna
* Evaluate and compare performance

---

## Deliverables

* Notebook: `notebooks/02_modeling.ipynb`

* Reusable code in `src/`:

  * preprocessing
  * training
  * prediction

* Saved model in `artifacts/models/`

* Predictions saved in `artifacts/predictions/`

* Evaluation summary:

  * model comparison
  * key metrics
  * interpretation
  * feature importance or feature effect summary for the final selected model
  * explicit final model and threshold decision

---

## Requirements

### Data Split

* Use a fixed train / validation / test split:

  * 70% train
  * 15% validation
  * 15% test

* Preserve the target class proportion during splitting using stratified splits
* Use the validation set for model selection, threshold selection, and hyperparameter tuning
* Test set must NOT be used for training, tuning, or model selection

---

### Feature Preparation

* Use the candidate features and preprocessing decisions identified during EDA
* If you add new transformations during modeling, justify them clearly
* Keep reusable preprocessing logic in `src/`

---

### Baseline Model

* Start with a simple, interpretable model:

  * e.g., Logistic Regression or similar

---

### Improved Model

* Train these advanced models:

  * Random Forest
  * XGBoost
  * LightGBM

---

### Hyperparameter Tuning

* Tune each trained model, including the baseline and improved models
* Use Bayesian optimization with `Optuna`
* For each model, tune the 3 to 5 most common or impactful hyperparameters
* Choose parameter ranges that are reasonable and justified for the selected algorithm
* Document:

  * which hyperparameters were tuned
  * the search space used
  * the optimization metric
  * the best trial and best parameter set

* Keep the tuning process reproducible with fixed random seeds when supported

---

### Evaluation

* Evaluate using appropriate metrics:

  * precision / recall / F1
  * ROC-AUC (recommended)
  * accuracy (optional)

* Present the metrics in organized comparison tables, not as scattered notebook output
* Compare all four models:

  * Logistic Regression baseline
  * Random Forest
  * XGBoost
  * LightGBM

* Compare performance across all three dataset splits where relevant:

  * train
  * validation
  * test

* Include visual comparisons in addition to tables, for example:

  * bar charts for model metrics
  * line or grouped charts for train / validation / test comparison
  * threshold comparison plots

* Make the notebook presentation-ready and easy to scan
* Clearly compare model performance and highlight signs of overfitting or instability

---

### Model Interpretation

* Include feature importance analysis for the final selected model
* Plot the feature importance for the final selected model in the notebook
* Show which variables contribute most to churn prediction
* If the final model does not provide native feature importance, use an appropriate alternative interpretation method
* Explain the main drivers in clear language and avoid causal claims

---

### Threshold Analysis (recommended)

* Explore different classification thresholds
* Discuss trade-offs:

  * false positives vs false negatives

* Make the threshold selection explicit in the notebook
* State which threshold was chosen for the final model and why

---

### Notebook Presentation

The modeling notebook should be clear, organized, and presentation-ready.

It should explicitly include:

* a short section describing the train / validation / test split and the use of stratification
* a model-by-model comparison section with clean tables
* a visual comparison section for the main metrics
* a final model selection section
* a final threshold selection section
* a final feature importance section for the chosen model

Avoid leaving raw metric dictionaries or scattered printed outputs as the main presentation format.

---

## Constraints

* Avoid data leakage
* Avoid overfitting
* Prefer interpretability when possible
* Do not over-optimize without justification

---

## Notes

* Be explicit about assumptions
* Clearly state model limitations
* Keep explanations understandable for non-technical stakeholders
