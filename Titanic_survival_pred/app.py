# import streamlit as st
# import joblib
# import numpy as np

# model=joblib.load("titanic_model.pkl")

# st.title("Titanic Survival Prediction 🛳️")

# pclass=st.selectbox("Pclass", [1,2,3])
# age=st.slider("Age", 1,80,25)
# fare=st.number_input("Fare", 0.0,600.0)
# sex=st.radio("Sex",["male","female"])
# sibsp=st.number_input("Number of Siblings/Spouses aboard",0,10,0)
# parch=st.number_input("Number of Parent/Children aboard",0,10,0)
# ticket=st.number_input("Ticket Number Encoded",0,999999,10000)
# embarked=st.selectbox("Port of Embarkation", ["C","Q","S"])

# embarked_mapping={"S":0,"C":1,"Q":2}
# embarked_encoded=embarked_mapping[embarked]
# sex_encoded= 1 if sex=="female" else 0
# input_data=np.array([[pclass,sex_encoded,age,sibsp,parch,fare,ticket,embarked_encoded]])
# if st.button("Predict"):
#     prediction=model.predict(input_data)
#     st.success(f"Prediction: {"Survived" if prediction[0]==1 else "Not Survived"}")

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Load model
model = joblib.load("titanic_model.pkl")

st.set_page_config(page_title="Titanic Survival Prediction", page_icon="🛳️", layout="centered")

st.title("🛳️ Titanic Survival Prediction")
st.write("Fill in the passenger details and find out the survival chance!")

# --- Input Form ---
with st.form("titanic_form"):
    col1, col2 = st.columns(2)

    with col1:
        pclass = st.selectbox("Ticket Class (Pclass)", [1, 2, 3])
        age = st.slider("Age", 1, 80, 25)
        sex = st.radio("Sex", ["male", "female"])
        sibsp = st.number_input("Siblings/Spouses aboard", 0, 10, 0)

    with col2:
        parch = st.number_input("Parents/Children aboard", 0, 10, 0)
        fare = st.number_input("Fare (in $)", 0.0, 600.0, 32.0)
        ticket = st.number_input("Ticket Number Encoded", 0, 999999, 10000)
        embarked = st.selectbox("Port of Embarkation", ["C", "Q", "S"])

    submitted = st.form_submit_button("🚀 Predict")

# --- Encoding ---
if submitted:
    embarked_mapping = {"S": 0, "C": 1, "Q": 2}
    embarked_encoded = embarked_mapping[embarked]
    sex_encoded = 1 if sex == "female" else 0

    input_data = np.array([[pclass, sex_encoded, age, sibsp, parch, fare, ticket, embarked_encoded]])

    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    # --- Passenger Summary ---
    st.subheader("👤 Passenger Profile")
    profile = pd.DataFrame({
        "Feature": ["Pclass", "Sex", "Age", "Siblings/Spouses", "Parents/Children", "Fare", "Ticket", "Embarked"],
        "Value": [pclass, sex, age, sibsp, parch, fare, ticket, embarked]
    })
    st.table(profile)

    # --- Prediction Result ---
    if prediction == 1:
        st.success("✅ Prediction: **Survived** 🎉")
    else:
        st.error("❌ Prediction: **Not Survived** 💔")

    # --- Probability Gauge ---
    st.subheader("📊 Survival Probability")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=proba[1] * 100,
        title={"text": "Chance of Survival (%)"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "green"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    # --- Probability Bars ---
    st.subheader("🔎 Prediction Breakdown")
    prob_df = pd.DataFrame({
        "Outcome": ["Not Survived", "Survived"],
        "Probability": proba
    })
    st.bar_chart(prob_df.set_index("Outcome"))
