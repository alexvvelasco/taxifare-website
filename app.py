import streamlit as st
import datetime
import requests
import pandas as pd

st.markdown("""
Predict taxi prices in New York City using a machine learning model
""")


d = st.date_input("Date of pickup", datetime.date(2019, 7, 6))
t = st.time_input("Time of pickup", datetime.time(8, 45))

print(f"date:{d}, time: {t}")

pickup_datetime = datetime.datetime.combine(d, t).strftime("%Y-%m-%d %H:%M:%S")

longitude_pick = st.number_input("Pickup longitude", min_value=40.5, max_value=40.9, format="%.5f")
latitude_pick = st.number_input("Pickup latitude", min_value=-74.3, max_value=-73.7, format="%.5f")
longitude_drop = st.number_input("Dropoff longitude", min_value=40.5, max_value=40.9, format="%.5f")
latitude_drop = st.number_input("Dropoff latitude", min_value=-74.3, max_value=-73.7, format="%.5f")

passenger_count = st.number_input("Number of passengers", min_value=1, max_value=6, value=1)

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
        print(fare)
        st.success(f"Predicted fare: ${fare:.2f}")
    else:
        st.error("API request failed")

locations_df = pd.DataFrame({
    "lat": [latitude_pick, latitude_drop],
    "lon": [longitude_pick, longitude_drop]
})

st.map(locations_df)
