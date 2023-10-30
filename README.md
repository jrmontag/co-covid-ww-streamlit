# 📱-friendly CO COVID-19 Wastewater Data ✨

_All the same official data, without all the ArcGIS!_

---

# What is this?
The official COVID wastewater data from CDPHE, presented in a mobile-friendly format 
(fast and responsive). Check out the hosted version here: 
[https://colorado-covid-wastewater.streamlit.app/](https://colorado-covid-wastewater.streamlit.app/)

When the line in the chart is going up (or the numbers in the table), that means the selected 
community has recently had an increase in the number of people with COVID infections. 

The latest data is typically one to two weeks behind the calendar, so it's a bit of a 
trailing indicator of infections. When the data is seen to increase, community infection 
levels have been higher for a week or two already! 


# Why is this?
The state health department maintains a very cool, interactive, map-based 
[website to monitor COVID wastewater](https://cdphe.maps.arcgis.com/apps/dashboards/d79cf93c3938470ca4bcc4823328946b) 
sampling trends. However that site is nearly impossible to use on a mobile device, 
which is usually what I have handy when I'm trying to catch up on trends.

Read more about Colorado's wastewater monitoring program [here](https://cdphe.colorado.gov/covid-19/wastewater).

# Who is this?
Hi, I'm Josh 👋

Feel free to say hi, ask questions, or make feature requests:
- 🐦 [@jrmontag](https://twitter.com/jrmontag)
- 🐙 [jrmontag](https://github.com/jrmontag/co-covid-ww-streamlit)

# I can haz more details?

This is a lightweight [Streamlit](streamlit.io/) app to display data from the API I created to 
supply this information in a queryable fashion. You can see that project 
[over here](https://github.com/jrmontag/co-covid-ww).
