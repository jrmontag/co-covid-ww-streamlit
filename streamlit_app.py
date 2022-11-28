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

st.title("📱-friendly Colorado COVID-19 Wastewater Monitoring Data ✨")

st.markdown(
    """_All the same official data, without all the ArcGIS!_

---

# What is this?
The official COVID wastewater data from CDPHE, presented in a mobile-friendly format (fast and responsive).

# Why is this?
The state health department maintains a very cool, interactive, map-based 
[website to monitor COVID wastewater](https://cdphe.maps.arcgis.com/apps/dashboards/d79cf93c3938470ca4bcc4823328946b) 
sampling trends. However that site is nearly impossible to use on a mobile device, which is usually what I have 
handy when I'm trying to catch up on trends.

# Who is this?
Hi, I'm Josh 👋

Feel free to say hi, ask questions, or make feature requests:
🐦 [@jrmontag](https://twitter.com/jrmontag)
🐙 [jrmontag](https://github.com/jrmontag/co-covid-ww-streamlit)

---

Here are some Denver metro regions with less obvious utility names:
- most of Denver, Lakewood, Englewood: `Metro WW - Platte/Central`
- Arvada, Wheat Ridge, Westminster: `Metro WW - Clear Creek`
- Centennial, Littleton, Ken Caryl: `South Platte`

For maps of all utilities, check out 
[the CDPHE page](https://cdphe.maps.arcgis.com/apps/dashboards/d79cf93c3938470ca4bcc4823328946b) (from a computer).

"""
)
st.write("")

# TODO: set up proper DNS
base_url = "http://146.190.50.82"
utilities_q = "/api/utilities"

# TODO: cache this with ttl
# TODO: add header info to id this app in access logs
utilities = requests.get(base_url + utilities_q).json()["utilities"]

# construct API query via dropdown selections
col1, col2 = st.columns(2)
with col1:
    utility = st.selectbox(
        label="Choose a wastewater utility",
        options=utilities,
        # TODO: find metro platte programmatically
        index=38,
    )
with col2:
    lookback = st.selectbox(
        label="Choose a lookback period",
        options=("3 months", "6 months", "12 months", "All history"),
        index=0,
    )
    end = date.today()
    if lookback == "3 months":
        diff = timedelta(days=30 * 3)
    elif lookback == "6 months":
        diff = timedelta(days=30 * 6)
    elif lookback == "12 months":
        diff = timedelta(days=30 * 12)
    else:
        diff = timedelta(days=30 * 12 * 3)
    start = end - diff

api_q = (
    f"/api/samples?utility={utility}&start={start.isoformat()}&end={end.isoformat()}"
)

# TODO: cache with ttl
data = requests.get(base_url + api_q).json()

this_utility = data["parameters"]["utility"]
this_start = data["parameters"]["start"]
this_end = data["parameters"]["end"]
this_report = data["samples"]


report_frame = pd.DataFrame(this_report, columns=["Date", "Samples"]).sort_values(
    by="Date", ascending=False
)

# TODO: improve table formatting
#report_frame["Date"] = pd.to_datetime(report_frame["Date"])

st.bar_chart(report_frame, x="Date", y="Samples")

st.table(report_frame)
