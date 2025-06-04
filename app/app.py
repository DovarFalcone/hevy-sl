# app.py (Landing Page)

import pandas as pd
import streamlit as st

st.set_page_config(page_title="🏠 Home", layout="centered")

st.title("🏋️ Hevy Streamlit App")
st.markdown("Welcome! Upload your CSV to continue.")

uploaded_file = st.file_uploader("Upload your workout CSV file", type=["csv"])

if uploaded_file:
    # Load CSV using pandas
    df = pd.read_csv(uploaded_file)

    # Convert date columns
    for col in ["start_time", "end_time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d %b %Y, %H:%M", errors="coerce")
            df[col] = df[col].dt.strftime("%A, %B %-d, %Y at %I:%M %p")

    # Cast numeric columns if needed
    for col, dtype in {
        "weight_lbs": "float64",
        "reps": "Int64",
        "distance_miles": "float64",
        "duration_seconds": "float64",
        "rpe": "float64",
    }.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype, errors="ignore")

    # ✅ Save to session state
    st.session_state["data"] = df

    st.success("CSV uploaded and processed. Now choose a page:")

    pages = {
        "📊 Workout Dashboard": "pages/workout_dashboard.py",
        "🥇 Hall of Records": "pages/hall_of_records.py",
    }

    for label, path in pages.items():
        if st.button(label):
            st.switch_page(path)

else:
    st.info("Upload a Hevy CSV export to get started.")
