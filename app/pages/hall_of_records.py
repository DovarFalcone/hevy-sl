# hall_of_records.py

import streamlit as st

st.set_page_config(page_title="🏅 Home", layout="centered")


if "data" in st.session_state:
    df = st.session_state["data"]

    numeric_cols = ["weight_lbs", "reps", "distance_miles", "duration_seconds", "rpe"]
    category_cols = ["title", "exercise_title", "set_type"]
    datetime_cols = ["start_time", "end_time"]

    st.divider()
    st.subheader("Raw Data")
    st.dataframe(df.head(50))

