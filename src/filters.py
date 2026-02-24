import pandas as pd
import streamlit as st
import plotly.express as px


def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""
    st.sidebar.header("Filters")

    ageGroup = ["All Age Groups"] + sorted(df["AgeGroup"].unique().tolist())
    demographic = ["All"] + sorted(df["Demographic"].dropna().astype(str).str.strip().unique().tolist())
    topic = sorted(df["Topic"].dropna().astype(str).unique().tolist())

    ageGroup = st.sidebar.selectbox("Age Group", ageGroup, index=0)
    demographic = st.sidebar.selectbox("Sex/Ethnicity", demographic, index=0)

    # TODO (DEMO): Convert this selectbox to a multiselect (and update filtering logic)
    topic = st.sidebar.multiselect(
        "Topic",
        topic,
        default=[]
    )

    min_rt = df["YearStart"].dropna().min()
    max_rt = df["YearStart"].dropna().max()
    rt_range = st.sidebar.slider(
        "Year Range",
        min_value=int(min_rt),
        max_value=int(max_rt),
        value=(int(min_rt), int(max_rt)),
        step=1,
    )
    cap_outliers = st.sidebar.checkbox("Cap extreme data values", value=False)

    return {
        "AgeGroup": ageGroup,
        "Demographic": demographic,
        "Topic": topic,
        "rt_range": rt_range,
        "cap_outliers": cap_outliers,
    }


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    out = df.copy()

    if selections["AgeGroup"] != "All Age Groups":
        out = out[out["AgeGroup"] == selections["AgeGroup"]]

    if selections["Demographic"] != "All":
        out = out[out["Demographic"] == selections["Demographic"]]

    if selections["Topic"]:
        out = out[out["Topic"].isin(selections["Topic"])]

    lo, hi = selections["rt_range"]
    out = out[(out["YearStart"] >= lo) & (out["YearEnd"] <= hi)]

    if selections.get("cap_outliers") and {"Low_Confidence_Limit", "High_Confidence_Limit"} <= set(out.columns):
        width = (out["High_Confidence_Limit"] - out["Low_Confidence_Limit"]).abs()
        cutoff = width.quantile(0.99)
        out = out[width <= cutoff]

    return out.reset_index(drop=True)
