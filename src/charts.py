import pandas as pd
import plotly.express as px
import streamlit as st


def plot_response_hist(df: pd.DataFrame) -> None:
    """Plotting a simple histogram of response times."""
    if df.empty:
        st.info("No rows match your filters.")
        return

    fig = px.histogram(
        df,
        x="YearEnd",
        nbins=30,
        title=None,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_borough_bar(df: pd.DataFrame) -> None:
    """Plotting median response time by borough."""
    if df.empty:
        st.info("No rows match your filters.")
        return

    agg = (
        df.groupby("AgeGroup", as_index=False)["Data_Value"]
        .median()
        .rename(columns={"Data_Value": "Data_Value"})
        .sort_values("Data_Value", ascending=False)
    )

    fig = px.bar(
        agg,
        x="AgeGroup",
        y="Data_Value",
        title=None,
    )
    st.plotly_chart(fig, use_container_width=True)
