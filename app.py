import streamlit as st
import pandas as pd
import plotly.express as px

from src.data import load_data
from src.filters import render_filters, apply_filters
from src.charts import plot_response_trend, plot_demo_bar
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

    row_count = len(df)
    st.write("Total Number of Rows:", row_count)
    st.write(df['Class'].value_counts())

    # -------------------------
    # Filters (sidebar by default)
    # -------------------------
    # render_filters returns a dictionary of user selections
    selections = render_filters(df)

    # apply_filters returns a filtered dataframe based on selections
    df_f = apply_filters(df, selections)

    header_metrics(df_f)
    st.divider()

    # -------------------------
    # Main body
    # -------------------------
    # Tabs layout by default (3 tabs)
    tab_choice = st.radio(
        "Please select a tab:",
        ["Data Visualizations (4)", "Table"],
        horizontal=True,
        help="Graphs and table are both interactive"
    )

    if tab_choice == "Data Visualizations (4)":
        body_layout_tabs(df_f)
    else:
        st.subheader("Table")
        st.dataframe(df_f, use_container_width=True, height=420)

    st.divider()

    st.write("test map")
    df[['Longitude', 'Latitude']] = df['Geolocation'].str.extract(
        r'POINT \(([-\d.]+) ([-\d.]+)\)'
    ).astype(float)

    st.write(df[['Geolocation', 'Latitude', 'Longitude']].head())

    st.subheader("Interactive Map of Responses")
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Class",  # optional: color by a column
        hover_name="Topic",  # optional: hover info
        zoom=2,  # starting zoom
        height=500
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
