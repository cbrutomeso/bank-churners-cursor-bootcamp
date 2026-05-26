# Bank Churn — Cursor Bootcamp

## Overview

This project is designed as a hands-on bootcamp to learn how to use AI (via Cursor) to accelerate a full data workflow:

* Exploratory Data Analysis (EDA)
* Machine Learning modeling (churn prediction)
* Simple production simulation (Streamlit app)
* Business reporting (BI-ready outputs)

The focus is not only on building a churn model, but on **how to work effectively with AI in a structured, reproducible way**.

---

## Dataset

We use the **Bank Churners dataset**.

Goal:
Predict customer churn and identify key drivers behind attrition.

Dataset source:
[`https://www.kaggle.com/datasets/syviaw/bankchurners`](https://www.kaggle.com/datasets/syviaw/bankchurners)

Expected local file:
* Download the dataset and store the CSV as `data/raw/BankChurners.csv`
* If Kaggle provides a different filename, rename it to `BankChurners.csv` or update your data-loading code explicitly

---

## How to Work in This Project

Before starting, read `docs/00_cursor_quickstart.md`.

For every task:

1. Read the relevant task file in `docs/`
2. Ask the AI to propose a plan
3. Implement the solution step by step
4. Validate results against success criteria
5. Store outputs in the appropriate folders

---

## Required Project Structure

You must follow this structure:

* `docs/` → task definitions and context
* `data/raw/` → original dataset (read-only)
* `data/processed/` → cleaned data generated during the workflow
* `notebooks/` → EDA, feature engineering decisions, modeling, and BI/reporting analysis
* `artifacts/` → models, predictions, logs
* `app/` → Streamlit application
* `reports/` → figures, tables, executive summary

### Important Rules

* Do NOT create alternative top-level directories
* Always reuse existing folders
* Keep notebooks organized, reproducible, and presentation-ready
* EDA, modeling, and BI/reporting work should be implemented in notebooks
* Outputs must be saved under `artifacts/` or `reports/`

---

## Development Workflow

Typical flow:

1. Explore data in notebooks
2. Identify useful features and preprocessing decisions during EDA
3. Train and evaluate models in notebooks
4. Save models, predictions, and logs to `artifacts/`
5. Build a simple app in `app/`
6. Generate BI-ready outputs in `reports/`

---

## Bootstrap Setup

Recommended Python version:
* `Python 3.11`

Initial setup:

1. Create a virtual environment:
   * Windows PowerShell: `python -m venv .venv`
   * macOS / Linux: `python3 -m venv .venv`
2. Activate it:
   * Windows PowerShell: `.venv\Scripts\Activate.ps1`
   * macOS / Linux: `source .venv/bin/activate`
3. Install dependencies:
   * `pip install --upgrade pip`
   * `pip install -r requirements.txt`
4. Download the dataset from Kaggle and place it in:
   * `data/raw/BankChurners.csv`

Installation note:
* If `lightgbm` installation or import fails on macOS, install `libomp` first, for example with `brew install libomp`

Dependency rule:
* `requirements.txt` must use exact pinned versions, for example `pandas==2.2.3`
* If you add a new library, document it with an exact version instead of leaving it unpinned
* The initial `requirements.txt` is only a starting point and may be updated as the project evolves
* Update `requirements.txt` whenever a task adds, removes, or changes dependencies
* By the end of the project, `requirements.txt` should contain only the libraries that are actually used, each with an exact pinned version

---

## Success Criteria

See `docs/03_success_criteria.md`.

A task is NOT complete until it meets those conditions.

---

## Guidelines for Working with AI

* Always ask for a plan before coding
* Break tasks into small steps
* Validate outputs explicitly
* Do not assume correctness
* Be explicit about assumptions and limitations

---

## What You Should NOT Do

* Do not leave notebooks disorganized or hard to reproduce
* Do not duplicate logic unnecessarily across notebooks
* Do not invent results or conclusions
* Do not ignore missing or inconsistent data
* Do not overcomplicate models without justification

---

## Final Goal

By the end of this project, you should have:

* A clear EDA with business insights
* A working churn prediction model
* A simple Streamlit app for predictions
* Clean datasets ready for BI tools
* An understanding of how to structure AI-assisted workflows
