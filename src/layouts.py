import pandas as pd
import streamlit as st
import plotly.express as px

from src.charts import plot_response_hist, plot_borough_bar

# KPI METRICS
def header_metrics(df: pd.DataFrame) -> None:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Questions", len(df))
    with c2:
        median_val = df["Data_Value"].median()
        st.metric("Median Values", round(float(median_val), 2))
    with c3:
        most_common = df["Class"].dropna().mode().squeeze() or "—"
        st.metric("Most common topic", str(most_common))


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["Distribution", "By Age", "Map"])

    with t1:
        st.subheader("Response Time Distribution")
        plot_response_hist(df)
        st.write("From this chart, we can see that common response times for complaints usually are within 3-7 days.")

    with t2:
        st.subheader("Data Value by Age Group")
        plot_borough_bar(df)

        # TODO (IN-CLASS): Add a second view here (e.g., count by borough)
        st.subheader("Count by Age Group")
        counts = df["AgeGroup"].value_counts().sort_values()
        st.bar_chart(counts)

    with t3:
        st.subheader("Filtered Rows")
        st.dataframe(df, use_container_width=True, height=480)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download the filtered rows",
            data=csv,
            file_name="filtered_data.csv",
            mime='text/csv',
        )
