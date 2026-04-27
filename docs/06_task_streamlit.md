# 06_task_streamlit.md

## Goal

Create a simple app to use the model.

---

## Features

* Brief business context within the existing layout
* Single customer prediction from manual feature inputs
* Batch prediction from uploaded CSV

---

## Deliverables

* `app/streamlit_app.py`
* `data/processed/sample_batch_prediction_input.csv`

---

## Requirements

* Load model from `artifacts/models/`
* Validate manual inputs before scoring
* Handle missing or invalid values safely
* Keep UI simple
* Use a clean, modern, and demo-friendly visual style
* Use exactly two tabs in the app UI:

  * `Single Prediction`
  * `Batch Prediction`

* Show the final predicted class as `0` or `1`
* Show the predicted probability
* Display a probability risk range using colors

---

## Functional Requirements

### UI Structure

The app should use a simple two-tab layout only:

* `Single Prediction`
* `Batch Prediction`

Do not add extra tabs for other sections.
If business context, model notes, or limitations are shown, include them within the existing layout without creating additional tabs.

Use a clear visual hierarchy:

* one main title
* short section headings
* concise helper text
* consistent spacing and alignment

Prefer native Streamlit components such as:

* forms
* containers
* columns
* metrics
* dataframes
* download buttons

Avoid clutter, long text blocks, and unnecessary UI elements.

---

### UI / Design Requirements

The UI should be aesthetically clean and easy to demo.

Use these design principles:

* prefer a wide layout
* keep the interface visually balanced and easy to scan
* make the prediction results visually prominent
* use accessible, colorblind-friendly colors
* do not rely on color alone to communicate risk
* pair color with text labels, ordering, and clear annotations
* use minimal custom CSS only if it clearly improves the interface
* prioritize readability and consistency over decorative styling

Suggested layout:

* `Single Prediction`:

  * feature input form near the top
  * prediction result displayed prominently below the form
  * probability, predicted class, and risk level shown in a clean result block
  * model notes or limitations shown below the result without overwhelming the page

* `Batch Prediction`:

  * file uploader near the top
  * validation feedback and file preview after upload
  * prediction output table below
  * download button for the output CSV in a visible location

---

### 1. Single Prediction

The app must allow the user to manually enter the model features for one customer and generate:

* the final prediction as `0` or `1`
* the churn probability
* a color-coded risk indication based on the predicted probability

Suggested risk display:

* low risk
* medium risk
* high risk

The exact probability thresholds can be chosen by the implementer, but they must be documented clearly in the app.

### 2. Batch Prediction from CSV

The app must allow the user to upload a `.csv` file containing multiple customers and the required model features.

The app must return a downloadable CSV with one row per customer and at least:

* the original input columns
* the final prediction as `0` or `1`
* the predicted probability

If the uploaded file includes `CLIENTNUM`, preserve it in the output CSV as a customer identifier.

`CLIENTNUM` should be treated as an identifier only and not as a modeling feature unless the modeling pipeline explicitly expects it to be removed before inference.

The app should validate that the uploaded CSV contains the expected columns and show a clear error if required features are missing.

The task must also generate a ready-to-use sample input file for batch testing:

* save it as `data/processed/sample_batch_prediction_input.csv`
* include a small set of example customers with the required inference columns
* include `CLIENTNUM` if available
* make it immediately usable in the app without extra manual editing

---

## Optional (Advanced)

* Show prediction timestamp
* Log predictions
* Display model version
