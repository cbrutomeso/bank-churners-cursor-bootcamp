Read these files:
- README.md
- docs/03_success_criteria.md
- docs/05_task_modeling.md
- docs/02_dataset_dictionary.md

Assume `.venv` and `data/raw/BankChurners.csv` already exist.
If either is missing locally, create or restore them before proceeding.

If they already exist, also review:
- `notebooks/01_eda.ipynb`
- EDA figures or written insights in `reports/`

Then propose a structured modeling plan for this repository.

Requirements:
1. Cover the full flow: split, preprocessing, baseline, advanced models, Optuna tuning, evaluation, threshold selection, and final model selection
2. Explain what will live in `notebooks/` vs reusable code in `src/`
3. List the exact files expected to be created or updated
4. List the expected outputs in `artifacts/`, `reports/`, and any prediction exports
5. Explicitly address leakage prevention, reproducibility, train/inference consistency, and any dependency updates required in `requirements.txt`
6. Do not write code yet

Keep the plan explicit, repository-aware, and aligned with the task requirements.