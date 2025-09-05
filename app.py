import gradio as gr
import joblib
import numpy as np
import os

# Load scaler and models
scaler = joblib.load("models/scaler.joblib")

models = {
    'Logistic Regression': joblib.load("models/Logistic_Regression.joblib"),
    'LDA': joblib.load("models/LDA.joblib"),
    'Ridge': joblib.load("models/Ridge.joblib"),
    'Decision Tree': joblib.load("models/Decision_Tree.joblib"),
    'Random Forest': joblib.load("models/Random_Forest.joblib"),
    'Gradient Boosting': joblib.load("models/Gradient_Boosting.joblib"),
    'XGBoost': joblib.load("models/XGBoost.joblib"),
    'LightGBM': joblib.load("models/LightGBM.joblib"),
    'CatBoost': joblib.load("models/CatBoost.joblib"),
    'Linear SVM': joblib.load("models/Linear_SVM.joblib"),
    'Kernel SVM (RBF)': joblib.load("models/Kernel_SVM_(RBF).joblib"),
    'Kernel SVM (Poly)': joblib.load("models/Kernel_SVM_(Poly).joblib"),
    'KNN': joblib.load("models/KNN.joblib"),
    'Gaussian NB': joblib.load("models/Gaussian_NB.joblib"),
    'Bernoulli NB': joblib.load("models/Bernoulli_NB.joblib"),
    'Multinomial NB': joblib.load("models/Multinomial_NB.joblib"),
    'Voting Classifier': joblib.load("models/Voting_Classifier.joblib"),
    'Stacking Classifier': joblib.load("models/Stacking_Classifier.joblib")
}

# Define prediction function
def predict(
    model_name,
    age,
    sex,
    is_smoking,
    cigsPerDay,
    BPMeds,
    prevalentStroke,
    prevalentHyp,
    sysBP,
    BMI,
    glucose,
    hdl_cholestrol
):
    # Prepare input
    features = np.array([[age, sex, is_smoking, cigsPerDay, BPMeds,
                          prevalentStroke, prevalentHyp, sysBP,
                          BMI, glucose, hdl_cholestrol]])
    features_scaled = scaler.transform(features)

    # Select model and predict
    model = models[model_name]
    prediction = model.predict(features_scaled)[0]

    return str(prediction)

# Gradio interface
iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Dropdown(list(models.keys()), value=list(models.keys())[0], label="Select Model"),
        gr.Number(value=61, label="Age"),
        gr.Radio(["0", "1"], value="0", label="Sex (0=Female, 1=Male)"),
        gr.Radio(["0", "1"], value="0", label="Is Smoking (0=No, 1=Yes)"),
        gr.Number(value=3, label="Cigarettes Per Day"),
        gr.Radio(["0", "1"], value="0", label="On BP Meds (0=No, 1=Yes)"),
        gr.Radio(["0", "1"], value="0", label="Prevalent Stroke (0=No, 1=Yes)"),
        gr.Radio(["0", "1"], value="1", label="Prevalent Hypertension (0=No, 1=Yes)"),
        gr.Number(value=182, label="Systolic BP"),
        gr.Number(value=32.8, label="BMI"),
        gr.Number(value=65, label="Glucose"),
        gr.Number(value=26, label="HDL Cholesterol")
    ],
    outputs=gr.Textbox(label="Model Prediction"),
    allow_flagging="never"
)

# Launch Space
iface.launch()
