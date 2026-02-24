import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df