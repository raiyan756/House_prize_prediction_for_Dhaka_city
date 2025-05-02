import streamlit as st
import pickle
import pandas as pd
from geopy.geocoders import Nominatim
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load models and preprocessing pipelines
with open('sell_best_model.pkl', 'rb') as f:
    sell_model = pickle.load(f)

with open('rent_best_model.pkl', 'rb') as f:
    rent_model = pickle.load(f)

with open('sell_preprocessor.pkl', 'rb') as f:
    sell_preprocessor = pickle.load(f)

with open('rent_preprocessor.pkl', 'rb') as f:
    rent_preprocessor = pickle.load(f)

# Function to convert location to latitude and longitude
def get_location_coordinates(location):
    geolocator = Nominatim(user_agent="house_prediction")
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Streamlit UI
st.title('House Price Prediction')
st.subheader('Enter house details to predict the selling and rental price')

# User inputs
sqft = st.number_input('House Size in Sqft:', min_value=0)
bedrooms = st.number_input('Number of Bedrooms:', min_value=1)
bathrooms = st.number_input('Number of Bathrooms:', min_value=1)
location = st.text_input('Enter Location (e.g., Dhaka, Gulshan, etc.):')

# Location to coordinates
lat, long = get_location_coordinates(location)

if lat and long:
    st.write(f'Location Coordinates: Latitude={lat}, Longitude={long}')
else:
    st.error("Location not found. Please try a valid address.")
    
# Predict price category based on size and other factors (adjust this to your logic)
price_category = 'Medium'  # You can implement your logic to categorize price.

# Button to predict sell and rent prices
if st.button('Predict'):
    # Prepare the data for prediction
    input_data = pd.DataFrame([[sqft, bedrooms, bathrooms, lat, long, price_category]],
                              columns=['sqft', 'bedrooms', 'bathrooms', 'latitude', 'longitude', 'price_category'])
    
    # Preprocess the input for selling and renting models
    processed_sell_input = sell_preprocessor.transform(input_data)
    processed_rent_input = rent_preprocessor.transform(input_data)

    # Predict the prices using the models
    sell_price = sell_model.predict(processed_sell_input)
    rent_price = rent_model.predict(processed_rent_input)

    # Display the results
    st.write(f"Predicted Sell Price: {sell_price[0]}")
    st.write(f"Predicted Rent Price (per month): {rent_price[0]}")
