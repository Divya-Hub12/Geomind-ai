import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title="GeoMind AI",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 GeoMind AI")
st.subheader("Manganese Mine Intelligence Dashboard")
st.write("AI/ML-based prototype for reserve and production risk analysis.")

# -----------------------------
# Sample training dataset
# -----------------------------
data = {
    "production": [7000, 8500, 5000, 8700, 8000, 6500, 8800, 6000, 7500, 8200,
                    6800, 8300, 5400, 8900, 7200, 6400, 8100, 5800, 8600, 7900],
    "target": [9000] * 20,
    "reserve": [82000, 82000, 60000, 80000, 75000, 70000, 85000, 65000, 78000, 81000,
                70000, 84000, 62000, 86000, 74000, 68000, 79000, 61000, 83000, 77000],
    "rainfall": [120, 50, 200, 80, 100, 180, 40, 220, 110, 70,
                 150, 60, 190, 30, 130, 170, 55, 210, 45, 90],
    "downtime": [18, 5, 30, 8, 12, 25, 4, 35, 15, 7,
                 20, 6, 28, 3, 16, 22, 9, 32, 5, 11],
    "risk": [
        "HIGH", "LOW", "HIGH", "LOW", "MEDIUM",
        "HIGH", "LOW", "HIGH", "MEDIUM", "LOW",
        "MEDIUM", "LOW", "HIGH", "LOW", "MEDIUM",
        "HIGH", "MEDIUM", "HIGH", "LOW", "MEDIUM"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# Train ML model
# -----------------------------
features = [
    "production",
    "target",
    "reserve",
    "rainfall",
    "downtime"
]

X = df[features]
y = df["risk"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# -----------------------------
# User inputs
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    production = st.number_input(
        "Current Production (tonnes)",
        min_value=0,
        value=7600
    )

with col2:
    target = st.number_input(
        "Production Target (tonnes)",
        min_value=0,
        value=9000
    )

with col3:
    reserve = st.number_input(
        "Estimated Reserve (tonnes)",
        min_value=0,
        value=82000
    )

col4, col5 = st.columns(2)

with col4:
    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0,
        value=120
    )

with col5:
    downtime = st.number_input(
        "Equipment Downtime (hours)",
        min_value=0,
        value=18
    )

# -----------------------------
# ML Prediction
# -----------------------------
if st.button("🔍 Analyse Mine Risk"):

    input_data = pd.DataFrame([[
        production,
        target,
        reserve,
        rainfall,
        downtime
    ]], columns=features)

    prediction = model.predict(input_data)[0]

    shortfall = target - production

    if prediction == "HIGH":
        risk = "🔴 HIGH"
        recommendation = "Adjust mine schedule and review equipment availability."
    elif prediction == "MEDIUM":
        risk = "🟠 MEDIUM"
        recommendation = "Monitor weather conditions and equipment performance."
    else:
        risk = "🟢 LOW"
        recommendation = "Continue planned operations."

    st.divider()
    st.header("📊 Analysis Result")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("Production Shortfall", f"{shortfall} tonnes")

    with r2:
        st.metric("Estimated Reserve", f"{reserve} tonnes")

    with r3:
        st.metric("ML Risk Prediction", risk)

    st.info("🤖 AI Recommendation: " + recommendation)

st.caption("Prototype demonstration using sample data.")
