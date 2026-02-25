import pandas as pd
import streamlit as st
import plotly.express as px

from src.charts import plot_response_trend, plot_demo_bar, plot_sex_bar

# KPI METRICS
def header_metrics(df: pd.DataFrame) -> None:
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Records", len(df))
    with c2:
        dv = pd.to_numeric(df["Data_Value"], errors="coerce")
        dff = df.assign(Data_Value=dv).dropna(subset=["YearEnd", "Data_Value"])

        if dff.empty:
            st.metric("Year with Highest Avg.", "—", delta="—")
        else:
            overall_avg = dff["Data_Value"].mean()

            yearly_avg = (
                dff.groupby("YearEnd")["Data_Value"]
                .mean()
                .reset_index(name="YearAvg")
            )
            best = yearly_avg.loc[yearly_avg["YearAvg"].idxmax()]
            best_year = int(best["YearEnd"])
            best_val = float(best["YearAvg"])

            delta = best_val - overall_avg

            st.metric(
                "Year with Highest Avg.",
                f"{best_year}",
                delta=f"{delta:+.2f}%",
                delta_color="normal",
                help=f"{best_val:.2f}%"
            )
    with c3:
        q_avg = df.groupby("Topic")["Data_Value"].mean()
        if not q_avg.empty:
            top_q = q_avg.idxmax()
            top_val = q_avg[top_q]
            st.metric(
                "Inquiry with Highest Avg.",
                f"{top_val:.2f}%",
                delta="High" if top_val > 30 else "Moderate",
                delta_color="inverse" if top_val > 30 else "normal",
                help=top_q
            )
        else:
            st.metric("Inquiry with Highest Avg.", "—")
    with c4:
        demo_avg = df.groupby("Demographic")["Data_Value"].mean()
        if not demo_avg.empty:
            top_demo = demo_avg.idxmax()
            st.metric("Largest Demographic",f"{demo_avg[top_demo]:.2f}%",help=top_demo)
        else:
            st.metric("Largest Demographic", "—")
    with c5:
        smokealc = (df[df["Class"] == "Smoking and Alcohol Use"]["Data_Value"].dropna().reset_index(drop=True))
        cog = (df[df["Class"].isin(["Mental Health", "Cognitive Decline"])]["Data_Value"].dropna().reset_index(drop=True))
        sample = min(len(smokealc), len(cog))
        if sample == 0:
            st.metric("Smoking vs Cognitive Corr.", "—")
        else:
            r = smokealc[:sample].corr(cog[:sample])

            if abs(r) < 0.2:
                delta_text = "Neutral"
                delta_color = "off"
            elif r > 0:
                delta_text = "Positive"
                delta_color = "normal"
            else:
                delta_text = "Negative"
                delta_color = "inverse"

            st.metric(
                "Smoking/Drinking vs Cognitive Corr.",
                f"{r:.2f}",
                help=f"Sample size: {sample}",
                delta=delta_text,
                delta_color=delta_color
            )


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["By Demographic", "By Year","Map"])

    with t1:
        st.subheader("Count by Race/Ethnicity")
        st.write("Measure how many questions we're asked according to Race/Ethnicity")
        plot_demo_bar(df)

        st.subheader("Count by Sex")
        st.write("Measure how many questions we're asked according to Sex")
        plot_sex_bar(df)

    with t2:
        st.subheader("Percentage by Year")
        st.write("Calculates percentages by year")
        plot_response_trend(df)

    with t3:
        st.subheader("Map")
        st.dataframe(df, use_container_width=True, height=480)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download the filtered rows",
            data=csv,
            file_name="filtered_data.csv",
            mime='text/csv',
        )
