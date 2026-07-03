from fastapi import FastAPI
import pandas as pd
import joblib

from schemas import CustomerData

app = FastAPI()

# Load model files
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")
features = joblib.load("features.joblib")


# ======================
# HEALTH CHECK API
# ======================
@app.get("/health")
def health():
    return {"status": "API is running"}


# ======================
# MODEL INFO API
# ======================
@app.get("/model-info")
def model_info():
    return {
        "model": "Random Forest (or your best model)",
        "version": "1.0",
        "features_used": len(features)
    }


# ======================
# PREDICTION API
# ======================
@app.post("/predict")
def predict(data: CustomerData):

    input_data = pd.DataFrame([data.dict()])

    # One-hot encoding
    input_encoded = pd.get_dummies(input_data)

    # Align with training features
    input_encoded = input_encoded.reindex(columns=features, fill_value=0)

    # Scaling
    input_scaled = scaler.transform(input_encoded)

    # Prediction
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    # Risk logic
    if probability < 0.3:
        risk = "Low"
    elif probability < 0.7:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "churn_prediction": int(prediction),
        "churn_probability": float(probability),
        "risk_level": risk
    }