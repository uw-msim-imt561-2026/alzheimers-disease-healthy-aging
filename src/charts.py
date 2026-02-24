import pandas as pd
import plotly.express as px
import streamlit as st


def plot_response_trend(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No rows match your filters.")
        return

    counts = (
        df.groupby("YearEnd")
        .size()
        .reset_index(name="Count")
        .sort_values("YearEnd")
    )

    fig = px.line(
        counts,
        x="YearEnd",
        y="Count",
        markers=True,
        title=None,
    )
    fig.update_xaxes(dtick=1)
    fig.update_traces(line=dict(width=2))

    st.plotly_chart(fig, use_container_width=True)


def plot_demo_bar(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No rows match your filters.")
        return

    agg = (
        df[df["DemographicCategory"] == "Race/Ethnicity"]
        .groupby("Demographic", as_index=False)
        .size()
        .rename(columns={"size": "Count"})
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        agg,
        x="Demographic",
        y="Count",
        title=None,
    )
    st.plotly_chart(fig, use_container_width=True)
