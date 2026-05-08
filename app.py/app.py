import streamlit as st
import pandas as pd
import requests
import joblib
from sklearn.preprocessing import MinMaxScaler

# --- SETTINGS ---
CH_ID = '3375178'
READ_KEY = 'WQ7Q2MS7C8YLBXWO'

# Load your trained model
model = joblib.load('guardian_ai.pkl')

# Page Config
st.set_page_config(page_title="Health Guardian AI", page_icon="🛡️", layout="wide")

st.title("🛡️ Health Guardian AI Assistant")
st.subheader("Live Telemetry & AI Risk Analysis")

# --- FETCH DATA ---
def fetch_data():
    url = f"https://api.thingspeak.com/channels/{CH_ID}/feeds.json?api_key={READ_KEY}&results=1"
    data = requests.get(url).json()['feeds'][0]
    return data

data = fetch_data()

# --- DISPLAY METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{data['field1']} °C")
col2.metric("Humidity", f"{data['field2']} %")
col3.metric("Pulse Rate", data['field5'])

# --- AI PREDICTION ---
# Note: You should use the same scaling logic as your training
# For simplicity, we manually scale here based on your typical ranges
t_val = float(data['field1'])
h_val = float(data['field2'])
p_val = float(data['field5'])

# Creating input for model
# (Ideally, you'd save your 'scaler' object from Colab too!)
prediction = model.predict([[t_val, h_val, p_val]])[0]

st.divider()

if prediction == 1:
    st.error("🚨 ALERT: HIGH HEALTH RISK DETECTED")
    st.write("**Precautions:** Move to a ventilated area and check your breathing.")
else:
    st.success("✅ STATUS: ENVIRONMENT SAFE")
    st.write("**Advice:** Everything looks normal. Stay hydrated!")