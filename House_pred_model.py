import streamlit as st
import numpy as np
import pickle

# Load model and scaler
model = pickle.load(open("Model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.set_page_config(page_title="🏠 House Price Predictor", layout="centered")
st.title("🏠 House Price Prediction App")
st.markdown("Enter the house details below to predict its price (in ₹ Lacs):")

# Input Fields
posted_by = st.selectbox("Posted By", ["Owner", "Dealer", "Builder"])
under_construction = st.selectbox("Under Construction?", ["Yes", "No"])
rera = st.selectbox("RERA Approved?", ["Yes", "No"])
bhk = st.slider("Number of BHK", 1, 10)
rk_or_bhk = st.selectbox("BHK or RK", ["BHK", "RK"])
square_ft = st.number_input("Area (in Sq. Ft.)", min_value=100, max_value=10000, step=50)
ready_to_move = st.selectbox("Ready to Move?", ["Yes", "No"])
resale = st.selectbox("Is it a Resale?", ["Yes", "No"])
longitude = st.number_input("Longitude", min_value=50.0, max_value=100.0, step=0.01)
latitude = st.number_input("Latitude", min_value=5.0, max_value=40.0, step=0.01)

# Manual Encoding (same as model training)
posted_by_map = {"Owner": 1, "Dealer": 0, "Builder": 2}
rk_or_bhk_map = {"BHK": 1, "RK": 0}
binary_map = {"Yes": 1, "No": 0}

# Final feature input array in the correct order
input_data = np.array([[posted_by_map[posted_by],
                        binary_map[under_construction],
                        binary_map[rera],
                        bhk,
                        rk_or_bhk_map[rk_or_bhk],
                        square_ft,
                        binary_map[ready_to_move],
                        binary_map[resale],
                        longitude,
                        latitude]])

# Scale
scaled_input = scaler.transform(input_data)

# Predict
if st.button("Predict Price 💰"):
    prediction = model.predict(scaled_input)[0]
    prediction = max(0, prediction)  # Clip negatives
    st.success(f"Estimated Price: ₹ {prediction:.2f} Lacs")
