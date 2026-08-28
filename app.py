import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title="GeoMind AI",
    page_icon="🌍",
    layout="wide"
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
# HEADER & KPI CARDS
# =========================================================

st.title("🌍 GeoMind AI")
st.subheader("Manganese Mine Intelligence Dashboard")

st.write(
    "AI/ML-based prototype for manganese potential identification "
    "and mine production risk analysis."
)

# --- Quick Stats KPI Cards ---
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        label="🎯 Target Production",
        value=f"{df['target'].iloc[0]:,} T"
    )

with kpi2:
    st.metric(
        label="📊 Avg Historical Production",
        value=f"{int(df['production'].mean()):,} T"
    )

with kpi3:
    st.metric(
        label="⚠️ High Risk Occurrences",
        value=f"{(df['risk'] == 'HIGH').sum()} Mines"
    )
# =========================================================
# HISTORICAL PRODUCTION TRENDS
# =========================================================

st.divider()
st.subheader("📈 Historical Production Trends")

chart_data = pd.DataFrame({
    "Year": ["2021", "2022", "2023", "2024", "2025"],
    "Production (Tonnes)": [6500, 7100, 6800, 7400, 7380]
}).set_index("Year")

st.line_chart(chart_data)


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

col4, col5, col6 = st.columns(3)

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
        value=18,
        help="Enter total downtime in hours"
    )

with col6:
    blasting_delay = st.number_input(
        "Blasting Delay (hours) 💣",
        min_value=0,
        value=2,
        help="Enter delay in blasting operations"
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
            "Re-deploy equipment from low-priority zones, optimize blasting parameters, and adjust mine schedule to avoid shortfall."
        )

    elif prediction == "MEDIUM":
        risk = "🟠 MEDIUM"
        recommendation = (
            "Monitor weather forecasts, clear blasting delays, and review equipment maintenance logs."
        )

    else:
        risk = "🟢 LOW"
        recommendation = (
            "Operations running smoothly. Continue planned production schedules."
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

sample_csv_data = df[features].head(5).to_csv(index=False).encode('utf-8')

st.download_button(
    label="💡 Download Sample CSV for Testing",
    data=sample_csv_data,
    file_name="sample_mine_data.csv",
    mime="text/csv"
)

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

        # Batch Prediction for Uploaded File
        predictions = model.predict(uploaded_data[required_columns])
        uploaded_data["Predicted_Risk_Level"] = predictions

        st.subheader("📋 Batch Risk Prediction Results")
        st.dataframe(uploaded_data, use_container_width=True)

        csv_download = uploaded_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Predicted Results (CSV)",
            data=csv_download,
            file_name="manganese_risk_predictions.csv",
            mime="text/csv",
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

col8, col9, col10, col11 = st.columns(4)

with col8:
    satellite_index = st.slider(
        "Satellite Spectral Index (NDVI/Iron Oxide)",
        min_value=0.0,
        max_value=1.0,
        value=0.70,
        help="Higher values indicate spectral signatures of Manganese minerals"
    )

with col9:
    magnetic_anomaly = st.slider(
        "Magnetic / Soil Moisture Anomaly",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        help="Sub-surface geophysical inputs from satellite imagery"
    )

with col10:
    geological_score = st.slider(
        "Geological Suitability",
        min_value=0.0,
        max_value=1.0,
        value=0.75
    )

with col11:
    land_temp = st.slider(
        "Land Surface Temperature 🌡️",
        min_value=0.0,
        max_value=1.0,
        value=0.60,
        help="Thermal satellite inputs for surface anomaly identification"
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

# =========================================================
# SHOW RESULT AND MAP
# =========================================================

if st.session_state.show_map:

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

    # =====================================================
    # MAP
    # =====================================================

    st.subheader("🗺️ Manganese Potential Zone Map")

    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=11
    )

    sample_zones = [
        {
            "lat": latitude,
            "lon": longitude,
            "score": potential_score
        },
        {
            "lat": latitude + 0.08,
            "lon": longitude + 0.10,
            "score": 75.0
        },
        {
            "lat": latitude - 0.06,
            "lon": longitude + 0.07,
            "score": 55.0
        },
        {
            "lat": latitude + 0.12,
            "lon": longitude - 0.08,
            "score": 30.0
        },
        {
            "lat": latitude - 0.10,
            "lon": longitude - 0.12,
            "score": 60.0
        }
    ]

    for point in sample_zones:

        score = point["score"]

        if score >= 70:
            color = "red"
            status = "High Potential"

        elif score >= 45:
            color = "orange"
            status = "Medium Potential"

        else:
            color = "green"
            status = "Low Potential"

        folium.CircleMarker(
            location=[
                point["lat"],
                point["lon"]
            ],
            radius=9,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=f"{status} ({score:.1f}%)"
        ).add_to(m)

    st_folium(
        m,
        width=700,
        height=400,
        key="manganese_map"
    )

    st.write(
        "🔴 High Potential | 🟠 Medium Potential | 🟢 Low Potential"
    )

# =========================================================
# FOOTER
# =========================================================

st.caption(
    "GeoMind AI | Prototype demonstration using sample data"
)
