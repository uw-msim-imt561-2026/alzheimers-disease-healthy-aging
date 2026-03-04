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

    st.title(""" :material/medical_information: CDC Alzheimer's Disease and Healthy Aging Dashboard """)

    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"]:has(#info-box){
          padding: 28px 28px;
          border-radius: 22px;
          background: linear-gradient(120deg, rgba(99,102,241,.28), rgba(16,185,129,.24));
          border: 1px solid rgba(148,163,184,.35);
          box-shadow: 0 8px 28px rgba(15,23,42,.08);
          margin: 14px 0 18px 0;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .stApp{
          background: #0d1f2b;
          color: #e2e8f0;
        }
        h1,h2,h3, p, span, label{
          color: #e2e8f0 !important;
        }
        div[data-testid="stMetric"]{
          color: #e2e8f0 !important;
        }
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricValue"]{
          color: #e2e8f0 !important;
        }
        div[data-testid="stMarkdownContainer"] a{
          color: #61a5ff !important;
        }

        header[data-testid="stHeader"]{
          background: rgba(13, 23, 42, 0.92);
          border-bottom: 1px solid rgba(148,163,184,.18);
        }
        header[data-testid="stHeader"] *{
          color: rgba(226,232,240,.92) !important;
        }

        div[data-testid="stCaptionContainer"] p{
          color: rgba(226,232,240,.75) !important;
          font-size: 0.95rem;
        }

        div[data-testid="stCaptionContainer"] a,
        div[data-testid="stMarkdownContainer"] a{
          color: rgba(147,197,253,.95) !important;
          text-decoration: underline;
        }

        div[data-testid="stMarkdownContainer"] p{
          color: rgba(226,232,240,.82);
        }

        div[data-testid="stMetricLabel"]{
          color: rgba(226,232,240,.72) !important;
        }
        div[data-testid="stMetricValue"]{
          color: rgba(226,232,240,.95) !important;
        }

        section[data-testid="stSidebar"] > div{
          background: #0f172b;
          border-right: 1px solid rgba(148,163,184,.14);
        }

        section[data-testid="stSidebar"] *{
          color: rgba(226,232,240,.92) !important;
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] .stMarkdown{
          color: rgba(226,232,240,.78) !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div{
          background: rgba(2,6,23,.55) !important;
          border: 1px solid rgba(148,163,184,.18) !important;
          border-radius: 12px !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="slider"]{
          padding-top: 6px;
        }
        
        div[data-testid="stButton"] button{
          background: rgba(2,6,23,.55) !important;
          border: 1px solid rgba(148,163,184,.18) !important;
          color: rgba(226,232,240,.92) !important;
          border-radius: 8px !important;
        }
        
        div[data-testid="stButton"] button:hover{
          border-color: rgba(148,163,184,.4) !important;
          color: rgba(226,232,240,1) !important;
        }
        
        div[data-testid="stTextInput"] input{
          background: #0f172b !important;
          border: 1px solid rgba(148,163,184,.18) !important;
          color: rgba(226,232,240,.92) !important;
          border-radius: 8px !important;
        }
        
        div[data-testid="stTextInput"] input:focus{
          border-color: rgba(148,163,184,.4) !important;
          outline: none !important;
        }
        
        div[data-testid="stElementToolbar"]{
          background: transparent !important;
          box-shadow: none !important;
          border: none !important;
        }
        div[data-testid="stDataFrame"] iframe{
          color-scheme: dark;
        }
        div[data-testid="stDataFrameResizable"]{
          outline: 2px solid #0d1f2b !important;
          outline-offset: -1px !important;
          border-radius: 8px !important;
          overflow: hidden !important;
        }
        
        div[data-testid="stElementToolbar"] button{
          background: rgba(13,23,42,.85) !important;
          border: none !important;
          border-radius: 8px !important;
          box-shadow: none !important;
        }
        div[data-testid="stElementToolbarButtonContainer"]{
          background: rgba(13,23,42,.85) !important;
          border: none !important;
          border-radius: 8px !important;
          box-shadow: none !important;
        }
        
        div[data-testid="stElementToolbar"] button svg path{
          fill: rgba(226,232,240,.75) !important;
        }

        div[data-testid="stMetricDelta"]{
          font-weight: 600;
          filter: brightness(2.5) saturate(1.5) !important;
        }
        
        div[data-testid="stTooltipHoverTarget"] svg{
        color: rgba(226,232,240,.75) !important;
        fill: rgba(226,232,240,.75) !important;
        }
        
        div[data-testid="stTooltipHoverTarget"] svg{
        color: rgba(226,232,240,.75) !important;
        fill: rgba(226,232,240,.75) !important;
        }
        
        div[data-testid="stTooltipContent"],
        div[data-baseweb="tooltip"]{
        background: #1e293b !important;
        border: 1px solid rgba(148,163,184,.25) !important;
        border-radius: 8px !important;
        }
        
        div[data-testid="stTooltipContent"] *,
        div[data-baseweb="tooltip"] *{
        color: rgba(226,232,240,.92) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<span id="info-box"></span>', unsafe_allow_html=True)

    with st.container():
        st.caption(
            "Data recorded is from 2015-2022. This dataset is from the Behavioral Risk Factor Surveillance System (BRFSS) and published"
            " by the Division of Population Health.")
        st.caption(
            "[Click here to access the Github Repository](https://github.com/uw-msim-imt561-2026/alzheimers-disease-healthy-aging)")
        st.caption(
            "Dataset last updated on: [February 14th, 2025](https://data.cdc.gov/Healthy-Aging/Alzheimer-s-Disease-and-Healthy-Aging-Data/hfr9-rurv/about_data)")

    df = load_data("data/sample.csv")

    # Basic Stats to check for data
    # row_count = len(df)
    # st.write("Total Number of Rows:", row_count)
    # st.write(df['Class'].value_counts())

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
        #only important rows
        cols_to_show = [
            "YearStart",
            "YearEnd",
            "LocationDesc",
            "Class",
            "Topic",
            "Data_Value",
            "AgeGroup",
            "DemographicCategory",
            "Demographic"
        ]

        df_table = df_f[[col for col in cols_to_show if col in df_f.columns]].copy()

        st.dataframe(df_table, use_container_width=True, height=420)



    st.divider()


if __name__ == "__main__":
    main()