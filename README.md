# Busy Bee's Alzheimer's Disease & Healthy Aging Dashboard  (Group 6)
### Michael Gov, Nicole Ni, Shawn Canonizado <br> 
Shane A McGarry <br> 
IMT 561, Winter 2026 <br> 
Feb 24, 2026

## Live Dashboard
https://uw-msim-imt561-2026-alzheimers-disease-healthy-aging-app-zlc5iq.streamlit.app/

## Description

This dashboard presents data from the **CDC’s Alzheimer’s Disease and Healthy Aging** dataset, collected between 2015 and 
2022 through the Behavioral Risk Factor Surveillance System (BRFSS). The visualizations focus on indicators **related to
cognitive decline, mental health, smoking, and alcohol use**, allowing users to explore trends and demographic patterns 
across multiple dimensions of public health. The dashboard features four interactive visualizations, including **bar 
charts, a line chart, a geographic map, and polar chart**, each designed to support exploratory 
analysis and comparison across variables. 

Users can dynamically filter results by **age group, demographic category, topic, and year range,** enabling customized 
views tailored to specific analytical questions. To improve interpretability and consistency, percentage values can be 
standardized using a percentile cap selection to reduce the influence of extreme values and support clearer comparisons 
across years and groups.

### Stakeholders

The primary stakeholders for this dashboard are public health decision-makers at the local, state, and federal levels. 
These include roles such as:
<ul>
<li>State and local health department officials</li>
<li>Public health analysts</li>
<li>Directors of regional/county health organizations</li>
</ul>

These stakeholders are responsible for:
<ul>
<li>Monitoring population health trends</li>
<li>Identifying at-risk populations</li>
<li>Allocating public health resources</li>
<li>Developing prevention and intervention strategies</li>
</ul>

Because their work involves large-scale policy development and strategic planning, 
they require tools that allow them to quickly interpret patterns across geographic regions, 
demographic groups, and time periods. This dashboard supports high-level analytical needs by 
transforming complex survey data into accessible visual insights.

### Dataset

The dataset used in this dashboard comes from the Centers for Disease Control and Prevention (CDC) and is sourced
from the Behavioral Risk Factor Surveillance System (BRFSS). The dataset comes from **2015-2022**, includes percentage-based survey responses
and covers topics related to:
<ul>
<li>Cognitive decline and mental health</li>
<li>Overall health</li>
<li>Substance and medication usage</li>
<li>Questions concerning varied situations (weight, diet, injuries)</li>
<li>Questions concerning most recent check-ups and care</li>
</ul>

For the purpose of identifying responses specifically related to Alzheimer’s disease, 
this dashboard **focuses more closely on indicators concerning cognitive decline and mental health.**

The data is aggregated by age group, demographic characteristics (sex and race/ethnicity), state or region, and year. 
This structure enables comparative analysis across distinct population segments and supports longitudinal trend 
evaluation. As a result, stakeholders can identify disparities and patterns to leverage these insights 
to inform public health planning, policy development, and targeted risk assessment for specific populations.

### Context & Goals

This dashboard was designed to support stakeholders who must analyze population-level health trends and demographic risk
patterns to inform policy and intervention decisions.

Public health authorities may use the dashboard to examine relationships between:
<ul>
<li>Cognitive decline and age group</li>
<li>Cognitive decline and demographic</li>
<li>Geographic/demographic variations in reporting</li>
<li>Cognitive decline correlated with smoking or alcohol use</li>
</ul>

By filtering by demographic variables, topic categories, and year ranges, the dashboard supports exploratory analysis
and evidence-based decision-making. These capabilities align with the dashboard’s goal of helping stakeholders answer 
critical public health questions and identify meaningful trends across populations. 

Altogether, they can answer key analytical questions such as:
<ul>
    <li>Which states show the highest prevalence of cognitive decline?</li>
    <li>Which demographic groups are most at risk?</li>
    <li>How have trends changed over time?</li>
    <li>How do smoking and alcohol use relate to cognitive decline?</li>
</ul>

## Quickstart
```bash
# For Windows Users
py -m venv .venv
.venv\Scripts\activate
streamlit run app.py
```

```bash
# For Mac Users
python -m venv .venv
source .venv/bin/activate
streamlit run app.py
```
