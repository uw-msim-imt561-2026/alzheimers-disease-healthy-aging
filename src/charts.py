import pandas as pd
import plotly.express as px
import streamlit as st


def plot_response_trend(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No rows match your filters.")
        return

    yearly = (
        df.groupby("YearEnd")["Data_Value"]
          .mean()
          .reset_index(name="Percent")
          .sort_values("YearEnd")
    )

    overall_avg = df["Data_Value"].mean()

    fig = px.line(
        yearly,
        x="YearEnd",
        y="Percent",
        labels={"YearEnd": "year"},
        markers=True,
        title=None,
    )

    fig.add_hline(
        y=overall_avg,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Overall Avg: {overall_avg:.2f}%",
        annotation_position="top right"
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(ticksuffix="%", rangemode="tozero")
    fig.update_traces(line=dict(width=2), marker=dict(size=8))

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
        labels={"Demographic": "Race/Ethnicity"},
        y="Count",
        title=None,
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_sex_bar(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No rows match your filters.")
        return

    agg = (
        df[df["DemographicCategory"] == "Sex"]
        .groupby("Demographic", as_index=False)
        .size()
        .rename(columns={"size": "Count"})
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        agg,
        x="Demographic",
        labels={"Demographic": "Sex"},
        y="Count",
        title=None,
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_map(df: pd.DataFrame) -> None:

    if "LocationAbbr" not in df.columns:
        st.error("LocationAbbr column not found.")
        return

    # Count responses per state (respects filters automatically)
    state_counts = (
        df.groupby("LocationAbbr")
        .size()
        .reset_index(name="Count")
    )

    if state_counts.empty:
        st.warning("No data available.")
        return

    fig = px.choropleth(
        state_counts,
        locations="LocationAbbr",
        locationmode="USA-states",
        color="Count",
        scope="usa",
        color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
        labels={"Count": "Number of Responses"}
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

def plot_radial_bar(df: pd.DataFrame, value_col: str = "Percentage") -> None:
    if "LocationAbbr" not in df.columns:
        st.error("LocationAbbr column not found in dataframe.")
        return
    if value_col not in df.columns:
        st.error(f"{value_col} column not found in dataframe.")
        return

    df_sorted = df.sort_values(by=value_col, ascending=False)

    fig = px.bar_polar(
        df_sorted,
        r=value_col,  # radial length = percentage
        theta="LocationAbbr",  # angle = state
        color=value_col,  # color intensity = value
        color_continuous_scale=px.colors.sequential.Oranges,
        template="ggplot2",
        hover_data = {"LocationAbbr": True, value_col: ":.2f"}
    )

    fig.update_layout(
        height=600,
        font=dict(size=12),
        polar = dict(
            radialaxis=dict(
                tickfont=dict(size=14, color="black")
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)