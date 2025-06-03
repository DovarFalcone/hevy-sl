# app.py

import streamlit as st
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Workout CSV Analyzer", layout="wide")
st.title("🏋️ Workout CSV Analyzer (Polars)")

uploaded_file = st.file_uploader("Upload your workout CSV file", type=["csv"])

if uploaded_file:

    df = pl.read_csv(
        uploaded_file,
        try_parse_dates=True,
        infer_schema_length=10000,  # helps with larger CSVs
        schema_overrides={
            "weight_lbs": pl.Float64,
            "reps": pl.Int64,
            "distance_miles": pl.Float64,
            "duration_seconds": pl.Float64,
            "rpe": pl.Float64,
        }
    )
        # Cast time columns explicitly (if needed)
    df = df.with_columns([
        pl.col("start_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S", strict=False),
        pl.col("end_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S", strict=False),
    ])

    # Display raw data
    st.subheader("Raw Data Preview")
    st.dataframe(df.head(50).to_pandas())

    # Buckets
    numeric_cols = ["weight_lbs", "reps", "distance_miles", "duration_seconds", "rpe"]
    category_cols = ["title", "exercise_title", "set_type"]
    datetime_cols = ["start_time", "end_time"]

    st.sidebar.header("Column Buckets")
    st.sidebar.write("**Numeric:**", numeric_cols)
    st.sidebar.write("**Categorical:**", category_cols)
    st.sidebar.write("**Datetime:**", datetime_cols)

    # Visualization Options
    st.subheader("Visualize Metrics")
    chart_type = st.selectbox("Select chart type", ["Histogram", "Box Plot", "Line Chart", "Scatter Plot"])

    if chart_type == "Histogram":
        col = st.selectbox("Select a numeric column", numeric_cols)
        bins = st.slider("Number of bins", 5, 50, 20)
        fig, ax = plt.subplots()
        sns.histplot(df[col].drop_nulls().to_numpy(), bins=bins, kde=True, ax=ax)
        st.pyplot(fig)

    elif chart_type == "Box Plot":
        num_col = st.selectbox("Numeric column", numeric_cols)
        cat_col = st.selectbox("Categorical column", category_cols)
        fig, ax = plt.subplots()
        sns.boxplot(data=df.to_pandas(), x=cat_col, y=num_col, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        time_col = st.selectbox("Datetime column", datetime_cols)
        metric_col = st.selectbox("Numeric column", numeric_cols)
        df_sorted = df.sort(by=time_col)
        df_plot = df_sorted.select([time_col, metric_col]).drop_nulls().to_pandas()
        df_plot[time_col] = pd.to_datetime(df_plot[time_col])
        st.line_chart(df_plot.set_index(time_col))

    elif chart_type == "Scatter Plot":
        x = st.selectbox("X-axis (numeric)", numeric_cols, key="x")
        y = st.selectbox("Y-axis (numeric)", numeric_cols, key="y")
        color = st.selectbox("Color by (optional category)", [None] + category_cols)
        df_plot = df.select([x, y] + ([color] if color else [])).drop_nulls().to_pandas()
        fig, ax = plt.subplots()
        if color:
            sns.scatterplot(data=df_plot, x=x, y=y, hue=color, ax=ax)
        else:
            sns.scatterplot(data=df_plot, x=x, y=y, ax=ax)
        st.pyplot(fig)
