import streamlit as st
import numpy as np
import pickle

# Load the model
model = pickle.load(open("model.pkl", "rb"))

st.title("🏡 House Price Prediction App")
st.write("Fill in the property details below to get an estimated price (in Lacs):")

# Categorical options
posted_by = st.selectbox("Posted By", ["Builder", "Dealer", "Owner"])
posted_by_encoded = {"Builder": 0, "Dealer": 1, "Owner": 2}[posted_by]

under_construction = st.radio("Under Construction?", ["Yes", "No"])
under_construction_encoded = 1 if under_construction == "Yes" else 0

rera = st.radio("RERA Approved?", ["Yes", "No"])
rera_encoded = 1 if rera == "Yes" else 0

bhk_no = st.number_input("BHK Number", min_value=1, max_value=10, step=1)

bhk_or_rk = st.selectbox("Is it a BHK or RK?", ["BHK", "RK"])
bhk_or_rk_encoded = 1 if bhk_or_rk == "BHK" else 0

square_ft = st.number_input("Square Footage", min_value=100)

ready_to_move = st.radio("Ready to Move?", ["Yes", "No"])
ready_to_move_encoded = 1 if ready_to_move == "Yes" else 0

resale = st.radio("Is it a Resale Property?", ["Yes", "No"])
resale_encoded = 1 if resale == "Yes" else 0

longitude = st.number_input("Longitude", format="%.6f")
latitude = st.number_input("Latitude", format="%.6f")

# Prediction
if st.button("Predict Price"):
    input_features = np.array([[
        posted_by_encoded, under_construction_encoded, rera_encoded,
        bhk_no, bhk_or_rk_encoded, square_ft, ready_to_move_encoded,
        resale_encoded, longitude, latitude
    ]])
    
    prediction = model.predict(input_features)
    st.success(f"Estimated Price: ₹ {prediction[0]:,.2f} Lacs")
