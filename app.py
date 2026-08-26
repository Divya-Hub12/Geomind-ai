import streamlit as st

st.set_page_config(
    page_title="GeoMind AI",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 GeoMind AI")
st.subheader("Manganese Mine Intelligence Dashboard")

st.write("AI/ML-based prototype for reserve and production risk analysis.")

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

if st.button("🔍 Analyse Mine Risk"):

    shortfall = target - production

    if shortfall > 1000 or downtime > 20:
        risk = "🔴 HIGH"
        recommendation = "Adjust mine schedule and review equipment availability."
    elif shortfall > 500 or downtime > 10:
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
        st.metric("Risk Level", risk)

    st.info("🤖 AI Recommendation: " + recommendation)

st.caption("Prototype demonstration using sample data.")