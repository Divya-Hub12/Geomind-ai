import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Sample training data
data = {
    "production": [7000, 8500, 5000, 8700, 8000, 6500, 8800, 6000, 7500, 8200],
    "target": [9000, 9000, 9000, 9000, 9000, 9000, 9000, 9000, 9000, 9000],
    "reserve": [82000, 82000, 60000, 80000, 75000, 70000, 85000, 65000, 78000, 81000],
    "rainfall": [120, 50, 200, 80, 100, 180, 40, 220, 110, 70],
    "downtime": [18, 5, 30, 8, 12, 25, 4, 35, 15, 7],
    "risk": [
        "HIGH", "LOW", "HIGH", "LOW", "MEDIUM",
        "HIGH", "LOW", "HIGH", "MEDIUM", "LOW"
    ]
}

df = pd.DataFrame(data)

# Features and target
X = df[[
    "production",
    "target",
    "reserve",
    "rainfall",
    "downtime"
]]

y = df["risk"]

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save trained model
joblib.dump(model, "model.pkl")

print("ML model trained successfully!")