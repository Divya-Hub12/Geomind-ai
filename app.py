import folium
from streamlit_folium import st_folium
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

st.write(
    "AI/ML-based prototype for manganese potential identification "
    "and mine production risk analysis."
)

# =========================================================
# ML TRAINING DATA - SAMPLE PROTOTYPE
# =========================================================

data = {
    "production": [
        7000, 8500, 5000, 8700, 8000,
        6500, 8800, 6000, 7500, 8200,
        6800, 8300, 5400, 8900, 7200,
        6400, 8100, 5800, 8600, 7900
    ],

    "target": [9000] * 20,

    "reserve": [
        82000, 82000, 60000, 80000, 75000,
        70000, 85000, 65000, 78000, 81000,
        70000, 84000, 62000, 86000, 74000,
        68000, 79000, 61000, 83000, 77000
    ],

    "rainfall": [
        120, 50, 200, 80, 100,
        180, 40, 220, 110, 70,
        150, 60, 190, 30, 130,
        170, 55, 210, 45, 90
    ],

    "downtime": [
        18, 5, 30, 8, 12,
        25, 4, 35, 15, 7,
        20, 6, 28, 3, 16,
        22, 9, 32, 5, 11
    ],

    "risk": [
        "HIGH", "LOW", "HIGH", "LOW", "MEDIUM",
        "HIGH", "LOW", "HIGH", "MEDIUM", "LOW",
        "MEDIUM", "LOW", "HIGH", "LOW", "MEDIUM",
        "HIGH", "MEDIUM", "HIGH", "LOW", "MEDIUM"
    ]
}

df = pd.DataFrame(data)

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

# =========================================================
# PRODUCTION RISK ANALYSIS
# =========================================================

st.divider()

st.header("📊 Mine Production Risk Analysis")

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

    input_data = pd.DataFrame(
        [[
            production,
            target,
            reserve,
            rainfall,
            downtime
        ]],
        columns=features
    )

    prediction = model.predict(input_data)[0]

    shortfall = max(target - production, 0)

    if prediction == "HIGH":
        risk = "🔴 HIGH"
        recommendation = (
            "Adjust mine schedule and review equipment availability."
        )

    elif prediction == "MEDIUM":
        risk = "🟠 MEDIUM"
        recommendation = (
            "Monitor weather conditions and equipment performance."
        )

    else:
        risk = "🟢 LOW"
        recommendation = (
            "Continue planned operations."
        )

    st.divider()

    st.subheader("📈 Analysis Result")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "Production Shortfall",
            f"{shortfall} tonnes"
        )

    with r2:
        st.metric(
            "Estimated Reserve",
            f"{reserve} tonnes"
        )

    with r3:
        st.metric(
            "ML Risk Level",
            risk
        )

    st.info(
        "🤖 AI Recommendation: " + recommendation
    )

# =========================================================
# MANGANESE POTENTIAL ZONE IDENTIFICATION
# =========================================================

st.divider()

st.header("🛰️ AI-Based Manganese Potential Zone Identification")
st.subheader("📂 Exploration Input Data")

uploaded_file = st.file_uploader(
    "Upload Geological / Satellite Sample Data (CSV)",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_data = pd.read_csv(uploaded_file)

    st.success("✅ Input data uploaded successfully")

    st.dataframe(
        uploaded_data,
        use_container_width=True
    )

    st.subheader("🤖 ML Prediction")

    required_columns = [
        "production",
        "target",
        "reserve",
        "rainfall",
        "downtime"
    ]

    if all(column in uploaded_data.columns for column in required_columns):
        st.success("✅ Required input columns found")

        st.dataframe(
            uploaded_data[required_columns],
            use_container_width=True
        )

    else:
        st.warning(
            "⚠️ CSV must contain: production, target, reserve, rainfall, downtime"
        )

st.write(
    "Prototype analysis using satellite and geological indicators "
    "to estimate manganese mineralisation potential."
)

col6, col7 = st.columns(2)

with col6:
    latitude = st.number_input(
        "Latitude",
        value=21.1500,
        format="%.4f"
    )

with col7:
    longitude = st.number_input(
        "Longitude",
        value=79.0900,
        format="%.4f"
    )

st.subheader("🔬 Exploration Indicators")

col8, col9, col10 = st.columns(3)

with col8:
    satellite_index = st.slider(
        "Satellite Spectral Index",
        min_value=0.0,
        max_value=1.0,
        value=0.70
    )

with col9:
    magnetic_anomaly = st.slider(
        "Magnetic Anomaly Index",
        min_value=0.0,
        max_value=1.0,
        value=0.65
    )

with col10:
    geological_score = st.slider(
        "Geological Suitability",
        min_value=0.0,
        max_value=1.0,
        value=0.75
    )
if "potential_score" not in st.session_state:
    st.session_state.potential_score = None

if "show_map" not in st.session_state:
    st.session_state.show_map = False

if st.button("🛰️ Identify Manganese Potential Zone"):
    st.session_state.show_map = True

    st.session_state.potential_score = (
        satellite_index * 0.40
        + magnetic_anomaly * 0.25
        + geological_score * 0.35
    ) * 100

    potential_score = st.session_state.potential_score
    
    if potential_score >= 70:

        zone = "🔴 HIGH POTENTIAL"

        action = (
            "Prioritize this zone for geological validation "
            "and targeted exploration."
        )

    elif potential_score >= 45:

        zone = "🟡 MEDIUM POTENTIAL"

        action = (
            "Conduct additional geological and geochemical "
            "investigation."
        )

    else:

        zone = "🟢 LOW POTENTIAL"

        action = (
            "Low priority for immediate exploration."
        )

    st.divider()

    st.subheader("🗺️ Manganese Potential Analysis")

    z1, z2 = st.columns(2)

    with z1:
        st.metric(
            "Manganese Potential Score",
            f"{potential_score:.1f}%"
        )

    with z2:
        st.metric(
            "Zone Classification",
            zone
        )

    st.info(
        "🤖 AI Recommendation: " + action
    )

    

    # Create Folium Map centered at user latitude and longitude
    st.subheader("🗺️ Manganese Potential Zone Map")
    m = folium.Map(location=[latitude, longitude], zoom_start=11)

    # Sample zone data points with their respective scores
    sample_zones = [
        {"lat": latitude, "lon": longitude, "score": potential_score},
        {"lat": latitude + 0.08, "lon": longitude + 0.10, "score": 75.0},
        {"lat": latitude - 0.06, "lon": longitude + 0.07, "score": 55.0},
        {"lat": latitude + 0.12, "lon": longitude - 0.08, "score": 30.0},
        {"lat": latitude - 0.10, "lon": longitude - 0.12, "score": 60.0}
    ]

    # Iterate through each point and set dynamic marker colors based on the potential score
    for point in sample_zones:
        score = point["score"]
        
        if score >= 70:
            color = "red"
            status = "High Potential"
        elif score >= 45:
            color = "orange"  # For Yellow/Orange indicator
            status = "Medium Potential"
        else:
            color = "green"
            status = "Low Potential"

        folium.CircleMarker(
            location=[point["lat"], point["lon"]],
            radius=9,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=f"{status} ({score:.1f}%)"
        ).add_to(m)
    st_folium(m, width=700, height=400)
    st.write("🔴 High Potential | 🟠 Medium Potential | 🟢 Low Potential")

# =========================================================
# FOOTER
# =========================================================

st.caption(
    "GeoMind AI | Prototype demonstration using sample data"
)
