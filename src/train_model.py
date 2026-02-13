import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import joblib

# ===============================
# LOAD FEATURE DATA
# ===============================

df = pd.read_csv("data/caller_features.csv")

# Separate ground truth
true_labels = df["true_label"]

# Remove non-feature columns
X = df.drop(columns=["caller_id", "true_label"])

# ===============================
# TRAIN ISOLATION FOREST
# ===============================

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Predict anomalies
df["anomaly"] = model.predict(X)

# Convert predictions
df["predicted_fraud"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

# ===============================
# RISK SCORE GENERATION
# ===============================

# Get anomaly scores
df["raw_score"] = model.decision_function(X)

# Normalize to 0-100 risk score
scaler = MinMaxScaler(feature_range=(0, 100))
df["risk_score"] = scaler.fit_transform(-df[["raw_score"]])

# ===============================
# EVALUATION
# ===============================

true_positive = ((df["predicted_fraud"] == 1) & (df["true_label"] == 1)).sum()
false_positive = ((df["predicted_fraud"] == 1) & (df["true_label"] == 0)).sum()
false_negative = ((df["predicted_fraud"] == 0) & (df["true_label"] == 1)).sum()
true_negative = ((df["predicted_fraud"] == 0) & (df["true_label"] == 0)).sum()

total_fraud = df["true_label"].sum()

# Detection Rate (Recall)
detection_rate = (true_positive / total_fraud) * 100

# Precision
precision = (true_positive / (true_positive + false_positive)) * 100

# False Positive Rate
false_positive_rate = (false_positive / (false_positive + true_negative)) * 100

print(f"True Fraud Callers: {total_fraud}")
print(f"Detected Fraud Callers: {df['predicted_fraud'].sum()}")
print(f"True Positives: {true_positive}")
print(f"False Positives: {false_positive}")
print(f"False Negatives: {false_negative}")
print(f"True Negatives: {true_negative}")

print("\n=== PERFORMANCE METRICS ===")
print(f"Detection Rate (Recall): {detection_rate:.2f}%")
print(f"Precision: {precision:.2f}%")
print(f"False Positive Rate: {false_positive_rate:.2f}%")

# ===============================
# SAVE MODEL AND SCALER
# ===============================

import os
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/fraud_detector.pkl")
joblib.dump(scaler, "models/risk_scaler.pkl")

print("\n=== MODEL SAVED ===")
print("Model saved to: models/fraud_detector.pkl")
print("Scaler saved to: models/risk_scaler.pkl")