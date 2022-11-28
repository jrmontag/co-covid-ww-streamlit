from datetime import date, timedelta
from time import time
import altair as alt
import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="CO COVID-19 Wastewater",
    page_icon="🔬",
    layout="wide",
)

st.title("Colorado COVID-19 Wastewater Data")

st.write(
    """
All the same official data, without all the ArcGIS!

- TODO: add context for why this exists
- TODO: add links to CDPHE site
- TODO: add some names for less obvious utilities around Denver
"""
)


# TODO: cache this with ttl
# TODO: add header info to id this app in access logs
utilities = requests.get("https://dummyjson.com/products/categories")

# construct API query via dropdowns
col1, col2 = st.columns(2)
with col1:
    utility = st.selectbox(
        label="Choose a wastewater utility",
        options=utilities,
        index=0,
    )
with col2:
    lookback = st.selectbox(
        label="Choose a lookback period",
        options=("6 months", "12 months", "All history"),
        index=0,
    )
    end = date.today()
    if lookback == "6 months":
        diff = timedelta(days=30 * 6)
    elif lookback == "12 months":
        diff = timedelta(days=30 * 12)
    else:
        diff = timedelta(days=30 * 12 * 3)
    start = end - diff

# TODO: set up proper DNS
base_url = "http://146.190.50.82"
api_params = (
    f"/api/samples?utility={utility}&start={start.isoformat()}&end={end.isoformat()}"
)

# TODO: cache with ttl
data = requests.get(base_url + api_params).json()

this_utility = data["parameters"]["utility"]
this_start = data["parameters"]["start"]
this_end = data["parameters"]["end"]
this_report = data["samples"]

st.write(f"Displaying results for {this_utility} over range {this_start} - {this_end}")

report_frame = pd.DataFrame(this_report, columns=["Date", "Samples"])

st.bar_chart(report_frame)

st.table(report_frame)
