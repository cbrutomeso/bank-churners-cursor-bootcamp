from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "artifacts" / "models" / "churn_model_pipeline.joblib"
METADATA_PATH = ROOT / "artifacts" / "models" / "churn_model_metadata.json"
RAW_DATA_PATH = ROOT / "data" / "raw" / "BankChurners.csv"
SAMPLE_INPUT_PATH = ROOT / "data" / "processed" / "sample_batch_prediction_input.csv"
LOG_PATH = ROOT / "artifacts" / "logs" / "streamlit_predictions.csv"
DEFAULT_PROBABILITY_RANGE = (0.70, 0.80)

NUMERIC_INPUT_MINIMUMS = {
    "Customer_Age": 18,
    "Dependent_count": 0,
    "Credit_Limit": 0,
    "Total_Revolving_Bal": 0,
    "Avg_Open_To_Buy": 0,
    "Months_on_book": 0,
    "Total_Relationship_Count": 0,
    "Months_Inactive_12_mon": 0,
    "Contacts_Count_12_mon": 0,
    "Total_Trans_Amt": 0,
    "Total_Trans_Ct": 0,
    "Total_Amt_Chng_Q4_Q1": 0,
    "Total_Ct_Chng_Q4_Q1": 0,
    "Avg_Utilization_Ratio": 0,
}

NUMERIC_INPUT_MAXIMUMS = {
    "Customer_Age": 100,
    "Dependent_count": 10,
    "Credit_Limit": 100_000,
    "Total_Revolving_Bal": 100_000,
    "Avg_Open_To_Buy": 100_000,
    "Months_on_book": 120,
    "Total_Relationship_Count": 20,
    "Months_Inactive_12_mon": 12,
    "Contacts_Count_12_mon": 20,
    "Total_Trans_Amt": 100_000,
    "Total_Trans_Ct": 500,
    "Total_Amt_Chng_Q4_Q1": 10,
    "Total_Ct_Chng_Q4_Q1": 10,
    "Avg_Utilization_Ratio": 1,
}

RISK_BANDS = {
    "Low": {"max": 0.30, "color": "#0072B2", "detail": "Below 30% predicted churn probability"},
    "Medium": {"max": 0.52, "color": "#E69F00", "detail": "30% to below the decision threshold"},
    "High": {"max": 1.01, "color": "#D55E00", "detail": "At or above the decision threshold"},
}

FEATURE_GROUPS = {
    "Customer Profile": [
        "Customer_Age",
        "Gender",
        "Dependent_count",
        "Education_Level",
        "Marital_Status",
        "Income_Category",
    ],
    "Product and Tenure": [
        "Card_Category",
        "Credit_Limit",
        "Total_Revolving_Bal",
        "Avg_Open_To_Buy",
        "Months_on_book",
        "Total_Relationship_Count",
    ],
    "Behavior and Transactions": [
        "Months_Inactive_12_mon",
        "Contacts_Count_12_mon",
        "Total_Trans_Amt",
        "Total_Trans_Ct",
        "Total_Amt_Chng_Q4_Q1",
        "Total_Ct_Chng_Q4_Q1",
        "Avg_Utilization_Ratio",
    ],
}


st.set_page_config(page_title="Bank Churn App", layout="wide")


@st.cache_resource(show_spinner=False)
def load_artifacts() -> tuple[Any, dict[str, Any]]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model pipeline not found at {MODEL_PATH}")
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"Model metadata not found at {METADATA_PATH}")

    model = joblib.load(MODEL_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return model, metadata


@st.cache_data(show_spinner=False)
def load_raw_data() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(RAW_DATA_PATH)


@st.cache_data(show_spinner=False)
def build_input_config(metadata: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_data = load_raw_data()
    numeric_features = metadata["numeric_features"]
    categorical_features = metadata["categorical_features"]
    config: dict[str, dict[str, Any]] = {}

    for feature in numeric_features:
        if feature in raw_data:
            series = pd.to_numeric(raw_data[feature], errors="coerce")
            observed_minimum = float(series.min())
            observed_maximum = float(series.max())
            default = float(series.median())
            is_integer = bool(series.dropna().mod(1).eq(0).all())
        else:
            observed_minimum = 0.0
            observed_maximum = 1_000_000.0
            default = 0.0
            is_integer = False

        minimum = float(NUMERIC_INPUT_MINIMUMS.get(feature, observed_minimum))
        maximum = float(NUMERIC_INPUT_MAXIMUMS.get(feature, observed_maximum))

        config[feature] = {
            "kind": "numeric",
            "min": minimum,
            "max": maximum,
            "default": default,
            "is_integer": is_integer,
            "observed_min": observed_minimum,
            "observed_max": observed_maximum,
        }

    for feature in categorical_features:
        if feature in raw_data:
            values = raw_data[feature].dropna().astype(str).value_counts()
            options = values.index.tolist()
            default = options[0] if options else ""
        else:
            options = []
            default = ""

        config[feature] = {
            "kind": "categorical",
            "options": options,
            "default": default,
        }

    return config


@st.cache_data(show_spinner=False)
def build_demo_default_values(_model: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    raw_data = load_raw_data()
    required = required_features(metadata)
    config = build_input_config(metadata)

    fallback = {feature: details["default"] for feature, details in config.items()}
    if raw_data.empty or any(feature not in raw_data.columns for feature in required):
        return fallback

    inference_frame, errors = validate_input_frame(raw_data[required], metadata)
    if errors or inference_frame is None:
        return fallback

    probabilities = positive_class_probability(_model, inference_frame)
    low_probability, high_probability = DEFAULT_PROBABILITY_RANGE
    in_range = probabilities[(probabilities >= low_probability) & (probabilities <= high_probability)]
    if in_range.empty:
        target_probability = sum(DEFAULT_PROBABILITY_RANGE) / 2
        default_index = (probabilities - target_probability).abs().idxmin()
    else:
        default_index = in_range.sort_values(ascending=False).index[0]

    row = raw_data.loc[default_index, required].to_dict()

    for feature in metadata["numeric_features"]:
        row[feature] = float(row[feature])
        if config[feature]["is_integer"]:
            row[feature] = int(round(row[feature]))
    for feature in metadata["categorical_features"]:
        row[feature] = str(row[feature])

    return row


def required_features(metadata: dict[str, Any]) -> list[str]:
    return metadata["inference_contract"]["input_columns_required"]


def selected_threshold(metadata: dict[str, Any]) -> float:
    return float(metadata["selected_threshold"])


def positive_class_probability(model: Any, frame: pd.DataFrame) -> pd.Series:
    probabilities = model.predict_proba(frame)
    classes = list(getattr(model, "classes_", [0, 1]))
    positive_index = classes.index(1) if 1 in classes else 1
    return pd.Series(probabilities[:, positive_index], index=frame.index)


def risk_level(probability: float, threshold: float) -> str:
    if probability >= threshold:
        return "High"
    if probability >= RISK_BANDS["Low"]["max"]:
        return "Medium"
    return "Low"


def risk_badge(level: str, probability: float) -> str:
    color = RISK_BANDS[level]["color"]
    return (
        f"<div class='risk-card' style='border-left-color: {color};'>"
        f"<div class='risk-label'>{level} Risk</div>"
        f"<div class='risk-prob'>{probability:.1%}</div>"
        "<div class='risk-subtitle'>Predicted churn probability</div>"
        f"<div class='risk-detail'>{RISK_BANDS[level]['detail']}</div>"
        "</div>"
    )


def validate_input_frame(
    frame: pd.DataFrame,
    metadata: dict[str, Any],
    *,
    allow_extra_columns: bool = True,
) -> tuple[pd.DataFrame | None, list[str]]:
    required = required_features(metadata)
    numeric_features = metadata["numeric_features"]
    categorical_features = metadata["categorical_features"]
    errors: list[str] = []

    missing = [column for column in required if column not in frame.columns]
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return None, errors

    if not allow_extra_columns:
        extra = [column for column in frame.columns if column not in required]
        if extra:
            errors.append(f"Unexpected columns: {', '.join(extra)}")

    inference = frame[required].copy()

    for column in numeric_features:
        inference[column] = pd.to_numeric(inference[column], errors="coerce")
        if inference[column].isna().any():
            errors.append(f"`{column}` must contain valid numeric values.")

    for column in categorical_features:
        inference[column] = inference[column].astype("string").str.strip()
        if inference[column].isna().any() or inference[column].eq("").any():
            errors.append(f"`{column}` must not be blank.")

    if errors:
        return None, errors

    return inference, []


def score_frame(model: Any, frame: pd.DataFrame, metadata: dict[str, Any]) -> pd.DataFrame:
    threshold = selected_threshold(metadata)
    probability_col = metadata["inference_contract"]["output_probability_name"]
    prediction_col = metadata["inference_contract"]["thresholded_output_name"]
    probabilities = positive_class_probability(model, frame)

    scored = frame.copy()
    scored[probability_col] = probabilities.round(6)
    scored[prediction_col] = (probabilities >= threshold).astype(int)
    scored["risk_level"] = probabilities.map(lambda value: risk_level(float(value), threshold))
    scored["prediction_timestamp"] = datetime.now(timezone.utc).isoformat()
    scored["model_name"] = metadata["model_name"]
    scored["decision_threshold"] = threshold
    return scored


def append_prediction_log(workflow: str, scored: pd.DataFrame, metadata: dict[str, Any]) -> None:
    prediction_col = metadata["inference_contract"]["thresholded_output_name"]
    log_row = pd.DataFrame(
        [
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "workflow": workflow,
                "row_count": len(scored),
                "model_name": metadata["model_name"],
                "decision_threshold": selected_threshold(metadata),
                "predicted_churn_count": int(scored[prediction_col].sum()),
                "predicted_non_churn_count": int((scored[prediction_col] == 0).sum()),
            }
        ]
    )
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_row.to_csv(LOG_PATH, mode="a", index=False, header=not LOG_PATH.exists())


def csv_bytes(frame: pd.DataFrame) -> bytes:
    return frame.to_csv(index=False).encode("utf-8")


def render_model_notes(metadata: dict[str, Any]) -> None:
    test_metrics = metadata.get("test_metrics_at_selected_threshold", {})
    with st.expander("Model notes, version, and limitations"):
        st.write(
            "This app is a local production simulation for prioritizing churn follow-up. "
            "Predictions should support business review, not replace human judgment."
        )
        st.write(
            f"Model: `{metadata['model_name']}` | Decision threshold: "
            f"`{selected_threshold(metadata):.2f}` | Random seed: `{metadata.get('random_seed', 'n/a')}`"
        )
        if test_metrics:
            st.write(
                "Holdout test metrics at the selected threshold: "
                f"ROC-AUC `{test_metrics['roc_auc']:.3f}`, "
                f"churn recall `{test_metrics['recall_churn']:.3f}`, "
                f"churn precision `{test_metrics['precision_churn']:.3f}`."
            )
        st.write(
            "Known exclusions from inference include `CLIENTNUM`, `Attrition_Flag`, and the "
            "`Naive_Bayes_Classifier_*` leakage columns. Model drivers are correlations, not causal claims."
        )


def render_header(metadata: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <section class="hero">
            <div>
                <p class="eyebrow">Bank Churn Prediction</p>
                <h1>Customer churn risk simulator</h1>
                <p class="hero-copy">
                    Score one customer or upload a CSV batch with the trained
                    <strong>{metadata['model_name']}</strong> pipeline.
                </p>
            </div>
            <div class="hero-card">
                <span>Decision threshold</span>
                <strong>{selected_threshold(metadata):.2f}</strong>
                <small>Class 1 = predicted churn</small>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_single_prediction(model: Any, metadata: dict[str, Any]) -> None:
    config = build_input_config(metadata)
    default_values = build_demo_default_values(model, metadata)
    threshold = selected_threshold(metadata)

    st.subheader("Single Customer Prediction")
    st.info(
        "The form starts with a real example near 70%-80% churn probability. "
        "Edit any field and press the button to refresh the prediction."
    )

    with st.form("single_prediction_form", clear_on_submit=False):
        values: dict[str, Any] = {}
        for group_name, features in FEATURE_GROUPS.items():
            st.markdown(f"#### {group_name}")
            columns = st.columns(3)
            for index, feature in enumerate(features):
                feature_config = config[feature]
                default_value = default_values.get(feature, feature_config["default"])
                with columns[index % 3]:
                    if feature_config["kind"] == "categorical":
                        options = feature_config["options"]
                        default = str(default_value)
                        default_index = options.index(default) if default in options else 0
                        values[feature] = st.selectbox(
                            feature,
                            options=options,
                            index=default_index,
                            key=f"single_{feature}",
                        )
                    else:
                        is_integer = feature_config["is_integer"]
                        step = 1 if is_integer else 0.01
                        format_string = "%d" if is_integer else "%.3f"
                        widget_value = st.number_input(
                            feature,
                            min_value=int(feature_config["min"]) if is_integer else float(feature_config["min"]),
                            max_value=int(feature_config["max"]) if is_integer else float(feature_config["max"]),
                            value=int(round(float(default_value))) if is_integer else float(default_value),
                            step=step,
                            format=format_string,
                            key=f"single_{feature}",
                        )
                        values[feature] = widget_value

        submitted = st.form_submit_button("Refresh churn prediction", type="primary")

    values = {
        feature: st.session_state.get(f"single_{feature}", default_values.get(feature, config[feature]["default"]))
        for feature in required_features(metadata)
    }
    input_frame = pd.DataFrame([values], columns=required_features(metadata))
    inference_frame, errors = validate_input_frame(input_frame, metadata, allow_extra_columns=False)
    if errors or inference_frame is None:
        for error in errors:
            st.error(error)
        return

    try:
        scored = score_frame(model, inference_frame, metadata)
        if submitted:
            append_prediction_log("single", scored, metadata)
    except Exception as exc:
        st.error(f"Prediction failed safely: {exc}")
        return

    probability_col = metadata["inference_contract"]["output_probability_name"]
    prediction_col = metadata["inference_contract"]["thresholded_output_name"]
    probability = float(scored.loc[0, probability_col])
    prediction = int(scored.loc[0, prediction_col])
    level = str(scored.loc[0, "risk_level"])

    result_col, context_col = st.columns([1.15, 1])
    with result_col:
        st.markdown(risk_badge(level, probability), unsafe_allow_html=True)
    with context_col:
        metric_col_1, metric_col_2 = st.columns(2)
        metric_col_1.metric("Predicted class", prediction)
        metric_col_2.metric("Decision threshold", f"{threshold:.2f}")
        st.caption("Class `1` means predicted attrition/churn; class `0` means predicted existing customer.")

    render_model_notes(metadata)


def render_batch_prediction(model: Any, metadata: dict[str, Any]) -> None:
    st.subheader("Batch CSV Prediction")
    st.write(
        "Upload a CSV with the required inference columns. `CLIENTNUM` is preserved as an "
        "identifier if present, but it is not used as a model feature."
    )

    uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])
    if uploaded_file is None:
        render_model_notes(metadata)
        return

    try:
        uploaded = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the uploaded CSV: {exc}")
        render_model_notes(metadata)
        return

    st.write("Uploaded file preview")
    st.dataframe(uploaded.head(20), use_container_width=True)

    inference_frame, errors = validate_input_frame(uploaded, metadata)
    if errors or inference_frame is None:
        st.error("The uploaded CSV cannot be scored yet.")
        for error in errors:
            st.write(f"- {error}")
        with st.expander("Required columns"):
            st.write(required_features(metadata))
        render_model_notes(metadata)
        return

    try:
        scored_features = score_frame(model, inference_frame, metadata)
        output = uploaded.copy()
        prediction_columns = [
            metadata["inference_contract"]["output_probability_name"],
            metadata["inference_contract"]["thresholded_output_name"],
            "risk_level",
            "prediction_timestamp",
            "model_name",
            "decision_threshold",
        ]
        for column in prediction_columns:
            output[column] = scored_features[column].values
        append_prediction_log("batch", scored_features, metadata)
    except Exception as exc:
        st.error(f"Prediction failed safely: {exc}")
        render_model_notes(metadata)
        return

    prediction_col = metadata["inference_contract"]["thresholded_output_name"]
    st.success(f"Scored {len(output):,} rows successfully.")
    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("Rows scored", f"{len(output):,}")
    metric_col_2.metric("Predicted churn", int(output[prediction_col].sum()))
    metric_col_3.metric("Threshold", f"{selected_threshold(metadata):.2f}")

    st.dataframe(output.head(100), use_container_width=True)
    st.download_button(
        "Download prediction output",
        data=csv_bytes(output),
        file_name=f"bank_churn_predictions_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        type="primary",
    )

    render_model_notes(metadata)


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --accent: #D55E00;
            --accent-dark: #A54200;
            --panel: rgba(255, 255, 255, 0.82);
            --soft-border: rgba(49, 51, 63, 0.14);
        }
        html {
            font-size: 18px;
        }
        .block-container {
            max-width: 1500px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }
        .hero {
            display: flex;
            align-items: stretch;
            justify-content: space-between;
            gap: 1.25rem;
            padding: 1.5rem 1.75rem;
            margin-bottom: 1.25rem;
            border: 1px solid var(--soft-border);
            border-radius: 1.1rem;
            background:
                linear-gradient(135deg, rgba(213, 94, 0, 0.14), rgba(0, 114, 178, 0.08)),
                var(--panel);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.06);
        }
        .hero h1 {
            margin: 0.1rem 0 0.4rem;
            font-size: 2.35rem;
            line-height: 1.05;
        }
        .hero-copy {
            margin: 0;
            font-size: 1.05rem;
            opacity: 0.82;
        }
        .eyebrow {
            margin: 0;
            color: var(--accent-dark);
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .hero-card {
            min-width: 13rem;
            padding: 1rem 1.2rem;
            border-radius: 0.9rem;
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.8);
        }
        .hero-card span,
        .hero-card small {
            display: block;
            opacity: 0.72;
        }
        .hero-card strong {
            display: block;
            margin: 0.15rem 0;
            font-size: 2rem;
        }
        div[data-testid="stForm"] {
            padding: 1.25rem 1.35rem;
            border-radius: 1rem;
            border: 1px solid var(--soft-border);
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.04);
        }
        div[data-testid="stForm"] h4 {
            margin-top: 0.55rem;
            color: #31333f;
        }
        label, div[data-testid="stMarkdownContainer"] p {
            font-size: 0.98rem;
        }
        .stButton button,
        .stDownloadButton button {
            border-radius: 0.65rem;
            padding: 0.62rem 1.05rem;
            font-weight: 750;
        }
        .risk-card {
            border-left: 0.85rem solid;
            border-radius: 1rem;
            padding: 1.35rem 1.55rem;
            background: rgba(255, 255, 255, 0.92);
            border-top: 1px solid var(--soft-border);
            border-right: 1px solid var(--soft-border);
            border-bottom: 1px solid var(--soft-border);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.06);
        }
        .risk-label {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .risk-prob {
            font-size: 3.25rem;
            font-weight: 800;
            line-height: 1.1;
        }
        .risk-subtitle {
            font-size: 0.98rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }
        .risk-detail {
            margin-top: 0.35rem;
            opacity: 0.85;
        }
        div[data-testid="stMetricValue"] {
            font-size: 2.15rem;
        }
        div[data-testid="stAlert"] {
            border-radius: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    apply_styles()
    try:
        model, metadata = load_artifacts()
    except Exception as exc:
        st.title("Bank Churn Prediction")
        st.error(f"Unable to load model artifacts: {exc}")
        st.stop()

    render_header(metadata)
    single_tab, batch_tab = st.tabs(["Single Prediction", "Batch Prediction"])

    with single_tab:
        render_single_prediction(model, metadata)

    with batch_tab:
        render_batch_prediction(model, metadata)


if __name__ == "__main__":
    main()
