"""Bank Churn — Streamlit scoring app (single + batch)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Paths (repo root = parent of app/)
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
MODEL_PATH = ROOT / "artifacts" / "models" / "churn_model_pipeline.joblib"
LOG_PATH = ROOT / "artifacts" / "logs" / "prediction_log.csv"
SAMPLE_PATH = ROOT / "data" / "processed" / "sample_batch_prediction_input.csv"

# Risk bands for UI (documented in sidebar)
RISK_LOW_MAX = 0.35
RISK_MEDIUM_MAX = 0.70

EDUCATION_OPTIONS = [
    "Unknown",
    "Uneducated",
    "High School",
    "College",
    "Graduate",
    "Post-Graduate",
    "Doctorate",
]
INCOME_OPTIONS = [
    "Unknown",
    "Less than $40K",
    "$40K - $60K",
    "$60K - $80K",
    "$80K - $120K",
    "$120K +",
]
GENDER_OPTIONS = ["M", "F"]
MARITAL_OPTIONS = ["Single", "Married", "Divorced", "Unknown"]
CARD_OPTIONS = ["Blue", "Silver", "Gold", "Platinum"]


def find_root() -> Path:
    if MODEL_PATH.exists():
        return ROOT
    alt = Path.cwd()
    if (alt / "artifacts" / "models" / "churn_model_pipeline.joblib").exists():
        return alt
    return ROOT


@st.cache_resource
def load_artifact(model_path: str):
    raw = joblib.load(model_path)
    if isinstance(raw, dict):
        pipeline = raw["pipeline"]
        threshold = float(raw.get("threshold", 0.5))
        meta = raw.get("metadata", {})
        feature_columns = list(meta.get("feature_columns", []))
        model_name = meta.get("model_name", "churn_model")
    else:
        pipeline = raw
        threshold = 0.5
        feature_columns = list(getattr(pipeline, "feature_names_in_", []))
        model_name = type(pipeline).__name__
    return pipeline, threshold, feature_columns, model_name


def risk_label(probability: float, decision_threshold: float) -> tuple[str, str]:
    """Return (label, css_color) for accessibility (label + color)."""
    if probability >= decision_threshold:
        return "High risk", "#c0392b"
    if probability >= RISK_MEDIUM_MAX:
        return "Elevated risk", "#e67e22"
    if probability >= RISK_LOW_MAX:
        return "Medium risk", "#f1c40f"
    return "Low risk", "#27ae60"


def validate_features(frame: pd.DataFrame, required: list[str]) -> list[str]:
    return [c for c in required if c not in frame.columns]


def score_frame(
    frame: pd.DataFrame,
    pipeline,
    feature_columns: list[str],
    threshold: float,
) -> pd.DataFrame:
    X = frame[feature_columns].copy()
    prob = pipeline.predict_proba(X)[:, 1]
    out = frame.copy()
    out["churn_probability"] = prob
    out["churn_prediction"] = (prob >= threshold).astype(int)
    return out


def append_log(rows: pd.DataFrame, mode: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = rows.copy()
    log["logged_at_utc"] = datetime.now(timezone.utc).isoformat()
    log["prediction_mode"] = mode
    header = not LOG_PATH.exists()
    log.to_csv(LOG_PATH, mode="a", header=header, index=False)


def render_result(probability: float, prediction: int, threshold: float) -> None:
    label, color = risk_label(probability, threshold)
    st.markdown(
        f"""
        <div style="padding:1rem 1.25rem;border-radius:8px;border:1px solid #ddd;background:#fafafa;">
          <p style="margin:0;font-size:1.1rem;"><strong>Predicted class:</strong> {prediction}</p>
          <p style="margin:0.5rem 0 0;font-size:1.1rem;"><strong>Churn probability:</strong> {probability:.1%}</p>
          <p style="margin:0.5rem 0 0;font-size:1.1rem;"><strong>Risk level:</strong>
            <span style="color:{color};font-weight:700;">{label}</span>
          </p>
          <p style="margin:0.75rem 0 0;font-size:0.9rem;color:#555;">
            Class 1 if probability ≥ decision threshold ({threshold:.2f}).
            Color bands: Low &lt; {RISK_LOW_MAX:.0%}, Medium &lt; {RISK_MEDIUM_MAX:.0%},
            Elevated &lt; threshold, High ≥ threshold.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Bank Churn Prediction", layout="wide")
    root = find_root()
    model_path = root / "artifacts" / "models" / "churn_model_pipeline.joblib"

    st.title("Bank Churn Prediction")
    st.caption(
        "Prioritize retention outreach using the trained churn model. "
        "Scores are probabilistic rankings, not guaranteed outcomes."
    )

    with st.sidebar:
        st.subheader("Model context")
        if not model_path.exists():
            st.error(f"Model not found at `{model_path}`. Run `notebooks/02_modeling.ipynb` first.")
            st.stop()
        pipeline, threshold, feature_columns, model_name = load_artifact(str(model_path))
        st.write(f"**Model:** {model_name}")
        st.write(f"**Decision threshold:** {threshold:.2f}")
        st.write(f"**Features:** {len(feature_columns)}")
        st.markdown(
            f"""
            **Risk color guide**
            - Low: &lt; {RISK_LOW_MAX:.0%}
            - Medium: {RISK_LOW_MAX:.0%} – {RISK_MEDIUM_MAX:.0%}
            - Elevated: {RISK_MEDIUM_MAX:.0%} – {threshold:.0%}
            - High: ≥ {threshold:.0%}
            """
        )
        st.markdown("**Limitations**")
        st.markdown(
            "- Correlation-based patterns; not causal advice.\n"
            "- Trained on a historical snapshot; monitor drift.\n"
            "- False positives/negatives expected — combine with banker judgment."
        )

    tab_single, tab_batch = st.tabs(["Single Prediction", "Batch Prediction"])

    # Defaults from training data when available
    defaults: dict = {}
    ref: pd.DataFrame | None = None
    sample_raw = root / "data" / "raw" / "BankChurners.csv"
    if sample_raw.exists():
        ref = pd.read_csv(sample_raw, nrows=200)
        for col in feature_columns:
            if col not in ref.columns:
                continue
            if ref[col].dtype in ("int64", "float64"):
                defaults[col] = float(ref[col].median())
            else:
                defaults[col] = ref[col].mode().iloc[0]

    with tab_single:
        st.subheader("Score one customer")
        st.write("Enter feature values, then submit the form.")

        with st.form("single_form"):
            cols = st.columns(3)
            inputs = {}
            for i, col in enumerate(feature_columns):
                slot = cols[i % 3]
                if col == "Education_Level":
                    inputs[col] = slot.selectbox(col, EDUCATION_OPTIONS, index=EDUCATION_OPTIONS.index(defaults.get(col, "Unknown")))
                elif col == "Income_Category":
                    inputs[col] = slot.selectbox(col, INCOME_OPTIONS, index=INCOME_OPTIONS.index(defaults.get(col, "Unknown")))
                elif col == "Gender":
                    inputs[col] = slot.selectbox(col, GENDER_OPTIONS, index=0)
                elif col == "Marital_Status":
                    inputs[col] = slot.selectbox(col, MARITAL_OPTIONS, index=MARITAL_OPTIONS.index(defaults.get(col, "Married")))
                elif col == "Card_Category":
                    inputs[col] = slot.selectbox(col, CARD_OPTIONS, index=CARD_OPTIONS.index(defaults.get(col, "Blue")))
                elif ref is not None and col in ref.columns:
                    if pd.api.types.is_numeric_dtype(ref[col]):
                        inputs[col] = slot.number_input(
                            col,
                            value=float(defaults.get(col, 0)),
                            min_value=0.0,
                        )
                    else:
                        inputs[col] = slot.text_input(col, value=str(defaults.get(col, "")))
                else:
                    inputs[col] = slot.number_input(col, value=float(defaults.get(col, 0.0)))

            submitted = st.form_submit_button("Predict churn risk", type="primary")

        if submitted:
            row = pd.DataFrame([inputs])
            try:
                scored = score_frame(row, pipeline, feature_columns, threshold)
                prob = float(scored["churn_probability"].iloc[0])
                pred = int(scored["churn_prediction"].iloc[0])
                render_result(prob, pred, threshold)
                append_log(scored, "single")
                st.success(f"Prediction logged to `{LOG_PATH.relative_to(root)}`.")
            except Exception as exc:
                st.error(f"Scoring failed: {exc}")

    with tab_batch:
        st.subheader("Batch scoring from CSV")
        st.write(
            f"Upload a CSV with required feature columns. "
            f"Optional `CLIENTNUM` is preserved. "
            f"Sample file: `{SAMPLE_PATH.relative_to(root)}`."
        )

        if SAMPLE_PATH.exists():
            st.download_button(
                "Download sample batch input",
                data=SAMPLE_PATH.read_bytes(),
                file_name=SAMPLE_PATH.name,
                mime="text/csv",
            )

        uploaded = st.file_uploader("Upload customer CSV", type=["csv"])

        if uploaded is not None:
            try:
                batch = pd.read_csv(uploaded)
            except Exception as exc:
                st.error(f"Could not read CSV: {exc}")
                st.stop()

            missing = validate_features(batch, feature_columns)
            if missing:
                st.error(f"Missing required columns: {', '.join(missing)}")
                st.stop()

            st.write("Preview (first 5 rows)")
            st.dataframe(batch.head(), use_container_width=True)

            if st.button("Run batch predictions", type="primary"):
                try:
                    scored = score_frame(batch, pipeline, feature_columns, threshold)
                    if "CLIENTNUM" in batch.columns and "CLIENTNUM" not in feature_columns:
                        scored.insert(0, "CLIENTNUM", batch["CLIENTNUM"].values)

                    st.success(f"Scored {len(scored):,} customers.")
                    st.dataframe(
                        scored[
                            [c for c in ["CLIENTNUM", "churn_prediction", "churn_probability"] if c in scored.columns]
                            + feature_columns[:3]
                        ].head(20),
                        use_container_width=True,
                    )

                    csv_bytes = scored.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Download predictions CSV",
                        data=csv_bytes,
                        file_name=f"churn_predictions_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                    )
                    append_log(
                        scored[["churn_prediction", "churn_probability"]].head(500),
                        "batch",
                    )
                except Exception as exc:
                    st.error(f"Batch scoring failed: {exc}")


if __name__ == "__main__":
    main()
