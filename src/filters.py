import pandas as pd
import streamlit as st
import plotly.express as px

def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""

    st.sidebar.header("Filters")

    # --- Initialize saved_views ---
    if "saved_views" not in st.session_state:
        st.session_state.saved_views = {}

    if "active_view" not in st.session_state:
        st.session_state.active_view = ""

    # --- Determine selected view ---
    saved_keys = list(st.session_state.saved_views.keys())
    selected_view = st.sidebar.selectbox("Switch View", ["Default View/ Full Dataset"] + saved_keys, key="active_view")

    # selected view?
    if "last_active_view" not in st.session_state:
        st.session_state.last_active_view = ""

    if st.session_state.active_view != st.session_state.last_active_view:

        if st.session_state.active_view in st.session_state.saved_views:
            saved = st.session_state.saved_views[st.session_state.active_view]

            for key, value in saved.items():
                st.session_state[key] = value

        st.session_state.last_active_view = st.session_state.active_view
        st.rerun()

    # --- Prepare defaults ---
    if st.session_state.active_view in st.session_state.saved_views:
        defaults = st.session_state.saved_views[st.session_state.active_view]
    else:
        defaults = {
            "AgeGroup": st.session_state.get("AgeGroup", "All Age Groups"),
            "Demographic": st.session_state.get("Demographic", "All"),
            "Topic": st.session_state.get("Topic", []),
            "rt_range": st.session_state.get(
                "rt_range", (int(df["YearStart"].min()), int(df["YearEnd"].max()))
            ),
            "cap_outliers": st.session_state.get("cap_outliers", False),
        }

    # --- Render widgets with defaults ---
    age_options = ["All Age Groups"] + sorted(df["AgeGroup"].unique())
    age_index = age_options.index(defaults["AgeGroup"]) if defaults["AgeGroup"] in age_options else 0
    ageGroup = st.sidebar.selectbox("Age Group", age_options, index=age_index, key="AgeGroup")

    dem_options = ["All"] + sorted(df["Demographic"].dropna().astype(str).unique())
    dem_index = dem_options.index(defaults["Demographic"]) if defaults["Demographic"] in dem_options else 0
    demographic = st.sidebar.selectbox("Sex/Ethnicity", dem_options, index=dem_index, key="Demographic")

    topic_options = sorted(df["Topic"].dropna().astype(str).unique())
    topic = st.sidebar.multiselect("Topic", topic_options, default=defaults["Topic"], key="Topic")

    min_rt = int(df["YearStart"].dropna().min())
    max_rt = int(df["YearEnd"].dropna().max())
    rt_range = st.sidebar.slider("Year Range", min_rt, max_rt, value=defaults["rt_range"], step=1, key="rt_range")

    cap_outliers = st.sidebar.checkbox("Cap extreme data values", value=defaults["cap_outliers"], key="cap_outliers")

    # --- Save view section ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Saved Views")
    view_name = st.sidebar.text_input("Save current view as:")

    if st.sidebar.button("Save View") and view_name:
        st.session_state.saved_views[view_name] = {
            "AgeGroup": ageGroup,
            "Demographic": demographic,
            "Topic": topic,
            "rt_range": rt_range,
            "cap_outliers": cap_outliers,
        }
        st.sidebar.success("View saved!")

    st.sidebar.markdown("---")
    st.sidebar.subheader('Clear Session?')
    st.sidebar.subheader("Warning! This clears your saved views")

    if st.sidebar.button("Clear All Saved Views and restore to default view"):
        st.session_state.saved_views = {}
        st.session_state.last_active_view = ""
        st.sidebar.success("All saved views cleared!")
        st.rerun()

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
