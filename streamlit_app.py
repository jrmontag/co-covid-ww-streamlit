from datetime import date, timedelta
from time import time
import altair as alt
import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="Page Config: Colorado COVID-19 Wastewater Data",
    page_icon="🔬",
    layout="centered",
)

st.title("Title: Colorado COVID-19 Wastewater Data")

st.write("All the same official data, without all the ArcGIS!")

st.write("TODO: add some pointers for less obvious utilities around Denver")


# TODO: query API for utilities
# utilities = requests.get('https://dummyjson.com/products/categories')

# select params via dropdown
col1, col2 = st.columns(2)
with col1:
    utility = st.selectbox(
        label="Choose a wastewater utility",
        # TODO: load options via request
        options=("Email", "Home phone", "Mobile phone"),
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
    start_param = start.isoformat()
    end_param = end.isoformat()

st.write(f"calculated daterange is {start=} - {end=} ")
