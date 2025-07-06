import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import warnings

warnings.filterwarnings("ignore")

# ----------------------------
# Step 1: Create Dataset
# ----------------------------
data = pd.DataFrame({
    "N": [90, 55, 150, 40, 60],
    "P": [42, 50, 75, 60, 70],
    "K": [43, 45, 80, 50, 65],
    "temperature": [30, 25, 28, 35, 25],
    "humidity": [80, 60, 70, 50, 55],
    "ph": [5.5, 6.5, 6.2, 7.0, 6.8],
    "rainfall": [180, 100, 200, 85, 120],
    "label": ["rice", "maize", "sugarcane", "cotton", "soybean"]
})

X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# ----------------------------
# Step 2: Train the Model
# ----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ----------------------------
# Step 3: Streamlit Web UI
# ----------------------------
st.set_page_config(page_title="Crop Recommendation", page_icon="🌿")
st.title("🌿 Smart Crop Recommendation System")
st.markdown("Enter the details of soil nutrients and environmental factors to get the most suitable crop recommendation.")

# Input fields
col1, col2 = st.columns(2)

with col1:
    N = st.number_input("Nitrogen (N)", min_value=0)
    P = st.number_input("Phosphorus (P)", min_value=0)
    K = st.number_input("Potassium (K)", min_value=0)
    temperature = st.number_input("Temperature (°C)", min_value=0.0)

with col2:
    humidity = st.number_input("Humidity (%)", min_value=0.0)
    ph = st.number_input("Soil pH", min_value=0.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0)

# Predict button
if st.button("Predict Crop"):
    if 0 in [N, P, K] or temperature == 0.0 or humidity == 0.0 or ph == 0.0 or rainfall == 0.0:
        st.error("⚠️ Please fill in all the required fields to get a prediction.")
    else:
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(input_data)
        st.success(f"✅ Recommended Crop: **{prediction[0]}**")
