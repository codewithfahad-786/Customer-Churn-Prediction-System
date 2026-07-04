import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Customer Churn App", layout="wide")

API_URL = "https://your-app.onrender.com"
# ======================
# TITLE
# ======================
st.title("📊 Customer Churn Prediction System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Single Prediction", "Batch Prediction"]
)

# ======================
# SINGLE PREDICTION
# ======================
if menu == "Single Prediction":

    st.subheader("🔮 Predict Single Customer Churn")

    gender = st.selectbox("Gender", ["Male", "Female"])
    SeniorCitizen = st.number_input("Senior Citizen (0/1)", 0, 1)
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.number_input("Tenure", 0, 100)
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
    MonthlyCharges = st.number_input("Monthly Charges")
    TotalCharges = st.number_input("Total Charges")

    if st.button("Predict Churn"):

        payload = {
            "gender": gender,
            "SeniorCitizen": SeniorCitizen,
            "Partner": Partner,
            "Dependents": Dependents,
            "tenure": tenure,
            "PhoneService": PhoneService,
            "MonthlyCharges": MonthlyCharges,
            "TotalCharges": TotalCharges
        }

        response = requests.post(f"{API_URL}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()

            st.success("Prediction Completed")

            st.write("### Result:")
            st.write(result)

            st.metric("Churn Probability", result["churn_probability"])
            st.metric("Risk Level", result["risk_level"])

        else:
            st.error("API Error")

# ======================
# BATCH PREDICTION
# ======================
elif menu == "Batch Prediction":

    st.subheader("📂 Batch Prediction (Upload CSV)")

    file = st.file_uploader("Upload CSV File")

    if file is not None:

        df = pd.read_csv(file)
        st.write("Preview:", df.head())

        if st.button("Predict All"):

            response = requests.post(
                f"{API_URL}/predict-batch",
                json=df.to_dict(orient="records")
            )

            if response.status_code == 200:
                st.success("Batch Prediction Done")
                st.write(response.json())

            else:
                st.error("API Error")