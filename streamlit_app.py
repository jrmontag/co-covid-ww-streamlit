from datetime import date, timedelta
from time import time
from typing import List, Optional
import altair as alt
import pandas as pd
import requests
import streamlit as st


def get_utility_index(utilities: List[str], default="Metro WW - Platte/Central") -> int:
    """Try to set Denver as the default utility.

    In the event that something has changed in the underlying data, don't crash upon
    not finding Platte/Central. Use whatever is present in that case.
    """
    result: int = 0
    if default in utilities:
        result = utilities.index(default)
    return result


st.set_page_config(
    page_title="CO COVID-19 Wastewater",
    page_icon="🔬",
    layout="wide",
)

st.title("📱-friendly Colorado COVID-19 Wastewater Monitoring Data ✨")

st.markdown(
    """_All the same official data..._ 📊 

_... without all the ArcGIS!_ 🗺

---

# What is this?
The official COVID wastewater data from CDPHE, presented in a more mobile-friendly format (fast and responsive).

# Why is this?
The state health department maintains a very cool, interactive, map-based 
[website to monitor COVID wastewater](https://cdphe.maps.arcgis.com/apps/dashboards/d79cf93c3938470ca4bcc4823328946b) 
sampling trends. However that site is nearly impossible to use on a mobile device, which is usually what I have 
handy when I'm trying to catch up on trends.

---

"""
)

BASE_URL = "http://wastewater.jrmontag.xyz"
API_ROOT = "/api/v1"
UTILITIES_PATH = f"{API_ROOT}/utilities"

# TODO: cache this with ttl
# TODO: add header info to id this app in access logs
utilities = requests.get(BASE_URL + UTILITIES_PATH).json()["utilities"]

# construct API query via dropdown selections
col1, col2 = st.columns(2)
with col1:
    utility = st.selectbox(
        label="Choose a wastewater utility",
        options=utilities,
        index=get_utility_index(utilities),
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

st.markdown(
    """Here are some Denver metro regions with less obvious utility names:
- most of Denver, Lakewood, Englewood: `Metro WW - Platte/Central`
- Arvada, Wheat Ridge, Westminster: `Metro WW - Clear Creek`
- Centennial, Littleton, Ken Caryl: `South Platte`

For maps of all utilities and more information about the source data check out 
[the CDPHE app](https://cdphe.maps.arcgis.com/apps/dashboards/d79cf93c3938470ca4bcc4823328946b) 
(from a computer).
"""
)

SAMPLES_PATH = f"{API_ROOT}/samples?utility={utility}&start={start.isoformat()}&end={end.isoformat()}"

# TODO: cache with ttl
data = requests.get(BASE_URL + SAMPLES_PATH).json()

this_utility = data["parameters"]["utility"]
this_start = data["parameters"]["start"]
this_end = data["parameters"]["end"]
this_report = data["samples"]


date_col_name = "Date"
samples_col_name = "Samples (SARS-CoV-2 copies/L)"
report_frame = pd.DataFrame(
    this_report, columns=[date_col_name, samples_col_name]
).sort_values(by=date_col_name, ascending=False)

# TODO: improve table formatting
# TODO: cache resultant dataframe from construction and manipulation
report_frame[date_col_name] = pd.to_datetime(report_frame[date_col_name])

st.bar_chart(report_frame, x=date_col_name, y=samples_col_name)

# st.table(report_frame)
st.dataframe(report_frame.dropna(), use_container_width=True)

st.markdown(
    """# Who is this?
Hi, I'm Josh 👋

Feel free to say hi, ask questions, make feature requests, or buy me a coffee!
- :bird: [Twitter](https://twitter.com/jrmontag)
- :octopus: [Github](https://github.com/jrmontag/co-covid-ww-streamlit)
- :coffee: [Ko-fi](https://ko-fi.com/jrmontag)
    
## Looking for more seasonal information?

You might also be interested in the 
[CDC's weekly update data on influenza](https://www.cdc.gov/flu/weekly/index.htm). 
Take care of yourself out there!
    """
)
