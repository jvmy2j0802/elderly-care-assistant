import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load CSV
df = pd.read_csv("health_monitoring.csv")

# Keep only numeric data
numeric_df = df.select_dtypes(include=["number"]).dropna()

# Train Isolation Forest
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(numeric_df)

# Save model
joblib.dump(model, "anomaly_detector.pkl")
print("✅ Anomaly model trained and saved as 'anomaly_detector.pkl'")
