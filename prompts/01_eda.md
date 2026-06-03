Before planning, ensure the dataset is available locally.

Also ensure the Python environment is ready.

If `.venv` does not exist yet, create it before continuing.
Use:
- Windows PowerShell: `python -m venv .venv`
- macOS / Linux: `python3 -m venv .venv`

Then activate the environment and install dependencies from `requirements.txt`.

If `data/raw/BankChurners.csv` does not exist yet, download it from:
- `https://www.kaggle.com/datasets/syviaw/bankchurners`

Then store the CSV as `data/raw/BankChurners.csv`.
If the downloaded file has a different name, rename it to `BankChurners.csv` before continuing.

Treat the initial `requirements.txt` as a starting point only.
You may update it as needed for the task.
Whenever you add, remove, or change a dependency:
- update `requirements.txt`
- pin exact versions with `==`
- keep only the libraries that are actually used by the project

By the end of the project, `requirements.txt` should contain only the real project dependencies and their exact versions.

After that, read these files:
- README.md
- docs/03_success_criteria.md
- docs/04_task_eda.md
- docs/02_dataset_dictionary.md

Then propose a concise, structured plan for the EDA task.

Requirements:
1. Explain how the EDA notebook will be structured
2. List the exact files expected to be created or updated
3. List the expected outputs in `reports/` and `artifacts/`
4. Call out data quality checks, leakage risks, and candidate feature ideas
5. Do not write code yet

Keep the plan explicit and practical for this repository.