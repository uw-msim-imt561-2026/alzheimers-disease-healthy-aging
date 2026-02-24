import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["AgeGroup"] = df["AgeGroup"].replace("Overall", "Overall (Aggregate)")
    df = df[(df['Class'] == 'Mental Health') | (df['Class'] == 'Cognitive Decline') | (df['Class'] == 'Smoking and Alcohol Use')]
    return df