# workout_dashboard.py

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="📊 Workout Dashboard", layout="wide", initial_sidebar_state="collapsed"
)
st.title("📊 Workout Dashboard")

if "data" in st.session_state:
    df = st.session_state["data"]

    numeric_cols = ["weight_lbs", "reps", "distance_miles", "duration_seconds", "rpe"]
    category_cols = ["title", "exercise_title", "set_type"]
    datetime_cols = ["start_time", "end_time"]

    st.divider()

    # Histogram Section
    with st.expander("📊 Histogram"):
        col = st.selectbox(
            "Select numeric column for histogram", numeric_cols, key="hist_col"
        )
        bins = st.slider("Number of bins", 5, 50, 20, key="hist_bins")
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna().to_numpy(), bins=bins, kde=True, ax=ax)
        st.pyplot(fig)

    # Box Plot Section
    with st.expander("📦 Box Plot"):
        num_col = st.selectbox("Numeric column", numeric_cols, key="box_num")
        cat_col = st.selectbox("Categorical column", category_cols, key="box_cat")
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x=cat_col, y=num_col, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Line Chart Section
    with st.expander("📈 Line Chart"):
        time_col = st.selectbox("Datetime column", datetime_cols, key="line_time")
        metric_col = st.selectbox("Numeric column", numeric_cols, key="line_metric")
        df_sorted = df.sort_values(by=time_col)
        df_plot = df_sorted[[time_col, metric_col]].dropna()
        df_plot[time_col] = pd.to_datetime(df_plot[time_col])
        st.line_chart(df_plot.set_index(time_col))

    with st.expander("🟠 Scatter Plot"):
        x = st.selectbox("X-axis (numeric)", numeric_cols, key="scatter_x")
        y = st.selectbox("Y-axis (numeric)", numeric_cols, key="scatter_y")
        color = st.selectbox(
            "Color by (optional category)", [None] + category_cols, key="scatter_color"
        )

        cols = [x, y]
        if color and color in df.columns:
            cols.append(color)

        df_plot = df[cols].dropna()

        # Debug prints - remove after confirming
        st.write("Scatter plot data sample:", df_plot.head())
        st.write("Data types:", df_plot.dtypes)

        fig, ax = plt.subplots()
        if color and color in df.columns:
            sns.scatterplot(data=df_plot, x=x, y=y, hue=color, ax=ax)
        else:
            sns.scatterplot(data=df_plot, x=x, y=y, ax=ax)
        st.pyplot(fig)

    st.divider()
    st.subheader("Raw Data")
    st.dataframe(df.head(50))

else:
    st.warning("⚠️ Please upload your Hevy CSV export on the main page.")
