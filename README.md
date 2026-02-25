# Busy Bee's Alzheimer's Disease & Healthy Aging Dashboard  (Group 6)
### Michael Gov, Nicole Ni, Shawn Canonizado <br> 
Shane A McGarry <br> 
IMT 561, Winter 2026 <br> 
Feb 24, 2026

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
