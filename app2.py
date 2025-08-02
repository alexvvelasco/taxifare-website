import streamlit as st
import requests
from datetime import datetime
import pydeck as pdk
import pandas as pd
import uuid

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count

1.1 Show map of pickup and drop-off locations

'''
with st.echo():
    st.header("Enter ride details")

    pickup_date = st.date_input("Pickup date", datetime.today())
    pickup_time = st.time_input("Pickup time", datetime.now().time())
    pickup_datetime = datetime.combine(pickup_date, pickup_time)
    pickup_lon = st.number_input("Pickup longitude", value=-73.985428)
    pickup_lat = st.number_input("Pickup latitude", value=40.748817)
    dropoff_lon = st.number_input("Dropoff longitude", value=-73.985428)
    dropoff_lat = st.number_input("Dropoff latitude", value=40.758817)
    passenger_count = st.number_input("Passenger count", min_value=1, max_value=10, value=1)

    # ✅ Include 'type' and proper keys for tooltip
    pickup_df = pd.DataFrame([{
        "lat": pickup_lat,
        "lon": pickup_lon,
        "type": "Pickup"
    }])

    dropoff_df = pd.DataFrame([{
        "lat": dropoff_lat,
        "lon": dropoff_lon,
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
        latitude=(pickup_lat + dropoff_lat) / 2,
        longitude=(pickup_lon + dropoff_lon) / 2,
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

'''
## Once we have these, let's call our API in order to retrieve a prediction
See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...
🤔 How could we call our API ? Off course... The `requests` package 💡
'''
with st.echo():
    url = 'https://taxifare.lewagon.ai/predict'
    if url == 'https://taxifare.lewagon.ai/predict':
        st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''
2. Let's build a dictionary containing the parameters for our API...
'''
with st.echo():
    params = {
        "pickup_datetime": pickup_datetime.isoformat(),
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count
    }

'''
3. Let's call our API using the `requests` package...
'''

'''
4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
with st.echo():
    if st.button("Get fare prediction"):
        url = 'https://taxifare.lewagon.ai/predict'
        response = requests.get(url, params=params)

        if response.status_code == 200:
            prediction = response.json().get("fare", "No fare found")
            st.success(f"Predicted fare: ${prediction:.2f}")
        else:
            st.error("Failed to get a response from the API.")
