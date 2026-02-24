import streamlit as st
import pandas as pd
import plotly.express as px

from src.data import load_data
from src.filters import render_filters, apply_filters
from src.charts import plot_response_hist, plot_borough_bar
from src.layouts import header_metrics, body_layout_tabs

def main() -> None:
    st.set_page_config(
        page_title="Alzheimer's Disease & Healthy Aging Dashboard",
        layout="wide",
    )

    st.title("CDC Alzheimer's Disease and Healthy Aging Dashboard")
    st.caption("Data recorded is from 2015-2022. This data set contains data from Behavioral Risk Factor Surveillance System (BRFSS).")
    st.caption("Last updated on: February 14th, 2025")

    df = load_data("data/sample.csv")

    # -------------------------
    # TODO (DEMO): Add a quick 'data sanity' check
    # - show row count
    # - show first 5 rows (optional)
    # -------------------------
    # HINT: st.write / st.dataframe
    # st.write(...)
    # st.dataframe(...)
    row_count = len(df)
    st.write("Number of rows:", row_count)
    st.dataframe(df.head(), use_container_width=True)
    st.write(df['Class'].value_counts())

    # -------------------------
    # Filters (sidebar by default)
    # -------------------------
    # render_filters returns a dictionary of user selections
    selections = render_filters(df)

    # apply_filters returns a filtered dataframe based on selections
    df_f = apply_filters(df, selections)

    # -------------------------
    # Header metrics
    # -------------------------
    # TODO (IN-CLASS): Replace placeholder metrics with real calculations
    header_metrics(df_f)
    st.divider()

    # -------------------------
    # Main body
    # -------------------------
    # Tabs layout by default (3 tabs)
    tab_choice = st.radio(
        "Choose a layout for the body (lab demo uses tabs; assignment can remix):",
        ["Tabs (3)", "Two Columns"],
        horizontal=True,
    )

    if tab_choice == "Tabs (3)":
        body_layout_tabs(df_f)
    else:
        # -------------------------
        # TODO (DEMO): Implement a 2-column layout
        # - left column: a chart
        # - right column: a table
        # -------------------------
        # HINT: st.columns(2)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Count of Topic Data")
            plot_response_hist(df_f)

        with col2:
            st.subheader("Filtered Rows")
            st.dataframe(df_f, use_container_width=True, height=420)

if __name__ == "__main__":
    main()
