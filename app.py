import streamlit as st
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler

# --- Load Model and Scaler ---
@st.cache_resource
def load_model_and_scaler():
    model = joblib.load("xgb_model.joblib")
    scaler = joblib.load("scaler.joblib")
    feature_names = joblib.load("feature_names.joblib")
    return model, scaler, feature_names

model, scaler, feature_names = load_model_and_scaler()

# --- App Header ---
st.title("🩺 Cardiovascular Disease Risk Predictor")
st.write("Enter your health details to estimate your 10-year CHD risk.")

# --- User Inputs ---
age = st.number_input("Age", 20, 100, 50)
sex = st.selectbox("Sex", ["Male", "Female"])
is_smoking = st.selectbox("Do you smoke?", ["Yes", "No"])
if is_smoking == 'Yes': 
    cigsPerDay = st.slider("Cigarettes per day", 1, 20, 0)
BPMeds = st.selectbox("On blood pressure medication?", ["Yes", "No"])
prevalentStroke = st.selectbox("History of Stroke?", ["Yes", "No"])
prevalentHyp = st.selectbox("Has Hypertension?", ["Yes", "No"])
diabetes = st.selectbox("Has Diabetes?", ["Yes", "No"])
totChol = st.number_input("Total Cholesterol", 100, 600, 200)
sysBP = st.number_input("Systolic BP", 90, 250, 120)
diaBP = st.number_input("Diastolic BP", 50, 150, 80)
BMI = st.number_input("BMI", 10.0, 60.0, 25.0)
heartRate = st.number_input("Heart Rate", 40, 200, 75)
glucose = st.number_input("Glucose Level", 50, 500, 85)

# --- Prepare Input ---
user_data = pd.DataFrame([{
    'age': age,
    'cigsPerDay': cigsPerDay,
    'totChol': totChol,
    'sysBP': sysBP,
    'diaBP': diaBP,
    'BMI': BMI,
    'heartRate': heartRate,
    'glucose': glucose,
    'sex_Male': 1 if sex == 'Male' else 0,
    'is_smoking_Yes': 1 if is_smoking == 'Yes' else 0,
    'BPMeds_Yes': 1 if BPMeds == 'Yes' else 0,
    'prevalentStroke_Yes': 1 if prevalentStroke == 'Yes' else 0,
    'prevalentHyp_Yes': 1 if prevalentHyp == 'Yes' else 0,
    'diabetes_Yes': 1 if diabetes == 'Yes' else 0
}])

# Align with training features
for col in feature_names:
    if col not in user_data.columns:
        user_data[col] = 0
user_data = user_data[feature_names]

# --- Scale Features ---
user_scaled = scaler.transform(user_data)

# --- Predict ---
if st.button("Predict CHD Risk"):
    prediction = model.predict(user_scaled)[0]
    prob = model.predict_proba(user_scaled)[0][1]
    if prediction == 1:
        st.error(f"⚠️ High Risk of CHD ({prob:.2%} probability)")
    else:
        st.success(f"✅ Low Risk of CHD ({prob:.2%} probability)")
