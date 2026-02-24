import pandas as pd
import streamlit as st
import plotly.express as px

from src.charts import plot_response_trend, plot_demo_bar

# KPI METRICS
def header_metrics(df: pd.DataFrame) -> None:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Records", len(df))
    with c2:
        avg_val = df["Data_Value"].mean()
        st.metric("Avg. Overall Reporting", f"{round(float(avg_val), 2):.2f}%")
    with c3:
        q_avg = df.groupby("Question")["Data_Value"].mean()
        if not q_avg.empty:
            top_q = q_avg.idxmax()
            st.metric("Highest Avg. Indicator",f"{q_avg[top_q]:.2f}%",help=top_q)
        else:
            st.metric("Highest Avg. Indicator", "—")
    with c4:
        demo_avg = df.groupby("Demographic")["Data_Value"].mean()
        if not demo_avg.empty:
            top_demo = demo_avg.idxmax()
            st.metric("Largest Demographic",f"{demo_avg[top_demo]:.2f}%",help=top_demo)
        else:
            st.metric("Largest Demographic", "—")


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["Count", "By Demographic", "Map"])

    with t1:
        st.subheader("Count of Questionnaires by Years")
        plot_response_trend(df)

    with t2:
        st.subheader("Count by Race/Ethnicity")
        plot_demo_bar(df)

        st.subheader("Count by Sex")
        counts = df[df["DemographicCategory"] == "Sex"]["Demographic"].value_counts().sort_values()
        st.bar_chart(counts)

    with t3:
        st.subheader("Map")
        st.dataframe(df, use_container_width=True, height=480)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download the filtered rows",
            data=csv,
            file_name="filtered_data.csv",
            mime='text/csv',
        )
