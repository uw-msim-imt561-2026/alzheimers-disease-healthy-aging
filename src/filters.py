import pandas as pd
import streamlit as st
import plotly.express as px


def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""
    st.sidebar.header("Filters")

    AgeGroup = ["All Age Groups"] + sorted(df["AgeGroup"].unique().tolist())
    Demographic = ["All"] + sorted(df["Demographic"].dropna().astype(str).str.strip().unique().tolist())
    topic = sorted(df["Class"].dropna().astype(str).unique().tolist())

    AgeGroup = st.sidebar.selectbox("Age Group", AgeGroup, index=0)
    Demographic = st.sidebar.selectbox("Sex/Ethnicity", Demographic, index=0)

    # TODO (DEMO): Convert this selectbox to a multiselect (and update filtering logic)
    topic = st.sidebar.multiselect(
        "Topic",
        topic,
        default=[]
    )

    # Response time slider
    min_rt, max_rt = df["YearStart"].dropna().min(), df["YearEnd"].dropna().max()
    rt_range = st.sidebar.slider(
        "Year Range",
        min_value=int(min_rt),
        max_value=int(max_rt),
        value=(int(min_rt), int(max_rt)),
        step=1,
    )

    # TODO (IN-CLASS): Add a checkbox toggle to cap outliers (e.g., at 99th percentile)
    cap_outliers = st.sidebar.checkbox("Cap extreme data values", value=False)

    return {
        "AgeGroup": AgeGroup,
        "Demographic": Demographic,
        "Topic": topic,
        "rt_range": rt_range,
        "cap_outliers": cap_outliers,
    }


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    """Applying filter selections to the dataframe."""
    out = df.copy()

    if selections["AgeGroup"] != "All Age Groups":
        out = out[out["AgeGroup"] == selections["AgeGroup"]]

    if selections["Demographic"] != "All":
        out = out[out["Demographic"] == selections["Demographic"]]

    if selections["Topic"]:
        out = out[out["Class"].isin(selections["Topic"])]

    lo, hi = selections["rt_range"]
    out = out[(out["YearStart"] >= lo) & (out["YearEnd"] <= hi)]

    # TODO (IN-CLASS): Implement outlier capping when cap_outliers is checked
    # HINT: use out["response_time_days"].quantile(0.99)
    if selections["cap_outliers"]:
        cap = out["Data_Value"].quantile(0.99)
        out = out[out["Data_Value"] <= cap]

    return out.reset_index(drop=True)
