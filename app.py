import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import uuid
from datetime import datetime

st.markdown("""
Predict taxi prices in New York City using a machine learning model
""")

#pickup_date = st.date_input("Pickup date", datetime.today())
#pickup_time = st.time_input("Pickup time", datetime.now().time())
#pickup_datetime = datetime.combine(pickup_date, pickup_time)
#d = st.date_input("Date of pickup", datetime.date(2019, 7, 6))
#t = st.time_input("Time of pickup", datetime.time(8, 45))



#pickup_datetime = datetime.datetime.combine(d, t).strftime("%Y-%m-%d %H:%M:%S")
pickup_date = st.date_input("Pickup date", datetime.today())
pickup_time = st.time_input("Pickup time", datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)
longitude_pick = st.number_input("Pickup longitude", value=-73.985428, format="%.6f",step=0.0001)
latitude_pick = st.number_input("Pickup latitude", value=40.748817,format="%.6f",step=0.0001)
longitude_drop = st.number_input("Dropoff longitude", value=-73.985428,format="%.6f",step=0.0001)
latitude_drop = st.number_input("Dropoff latitude", value=40.758817,format="%.6f",step=0.0001)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=10, value=1)
#longitude_pick = st.number_input("Pickup longitude", value=73.985428, format="%.5f")
#latitude_pick = st.number_input("Pickup latitude", value=-40.748817, format="%.5f")
#longitude_drop = st.number_input("Dropoff longitude", value=73.985428, format="%.5f")
#latitude_drop = st.number_input("Dropoff latitude", value=-40.758817, format="%.5f")

#passenger_count = st.number_input("Number of passengers", min_value=1, max_value=6, value=1)

#url = 'https://taxifare-197665747431.europe-west1.run.app/predict'
url = 'https://taxifare.lewagon.ai/predict'


params ={
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": longitude_pick,
    "pickup_latitude": latitude_pick,
    "dropoff_longitude": longitude_drop,
    "dropoff_latitude": latitude_drop,
    "passenger_count": passenger_count
}

if st.button("Predict fare"):
    response = requests.get(url, params=params)

    print(response.url)
    if response.status_code == 200:
        fare = response.json().get("fare")
        st.success(f"Predicted fare: ${fare:.2f}")
    else:
        st.error("API request failed")



pickup_df = pd.DataFrame([{
        "lat": latitude_pick,
        "lon": longitude_pick,
        "type": "Pickup"
    }])

dropoff_df = pd.DataFrame([{
        "lat": latitude_drop,
        "lon": longitude_drop,
        "type": "Dropoff"
    }])

pickup_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pickup_df,
        get_position='[lon, lat]',
        get_fill_color=[0, 128, 255, 180],  # Blue
        get_radius=60,
        pickable=True
    )

dropoff_layer = pdk.Layer(
        "ScatterplotLayer",
        data=dropoff_df,
        get_position='[lon, lat]',
        get_fill_color=[255, 0, 0, 180],  # Red
        get_radius=60,
        pickable=True
    )

view_state = pdk.ViewState(
        latitude=(latitude_pick + latitude_drop) / 2,
        longitude=(longitude_pick + longitude_drop) / 2,
        zoom=12
    )
tooltip = {
        "html": "<b>{type}</b><br/>Lat: {lat}<br/>Lon: {lon}",
        "style": {"color": "white"}
    }

st.subheader("🗺 Pickup & Dropoff Map")
st.pydeck_chart(pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        initial_view_state=view_state,
        layers=[pickup_layer, dropoff_layer],
        tooltip=tooltip
    ), key=str(uuid.uuid4()))
