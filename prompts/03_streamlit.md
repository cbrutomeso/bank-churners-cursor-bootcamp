Read these files:
- README.md
- docs/03_success_criteria.md
- docs/06_task_streamlit.md
- docs/02_dataset_dictionary.md

Assume `.venv`, the dataset, and the modeling artifacts already exist.
If any required dependency or artifact is missing locally, restore it before proceeding.

If they already exist, also review the current modeling artifacts and reusable inference code in:
- `artifacts/models/`
- `artifacts/predictions/`
- `reports/tables/`
- `src/`

Then propose a Streamlit app plan for this repository.

Requirements:
1. Cover both app workflows: single-customer prediction and batch CSV prediction
2. Use exactly two tabs in the proposed UI: `Single Prediction` and `Batch Prediction`
3. Explain how the app will load the trained model and reuse preprocessing/inference logic from `src/`
4. Explain input validation, error handling, risk-color display, downloadable batch output, sample batch input creation, and prediction logging
5. List the exact files expected to be created or updated
6. Explain how limitations, model version, and prediction context will be shown in the UI without adding extra tabs
7. Do not write code yet

Keep the plan practical, modular, and aligned with the task document.