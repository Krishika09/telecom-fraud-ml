import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import joblib

# ==========================================
# LOAD FEATURE DATA
# ==========================================

df = pd.read_csv("data/caller_features.csv")

if "true_label" not in df.columns:
    raise ValueError("Column 'true_label' not found in dataset.")

# Separate ground truth
true_labels = df["true_label"]

# Remove non-feature columns
X = df.drop(columns=["caller_id", "true_label"])

# ==========================================
# TRAIN ISOLATION FOREST (NO FORCED FRAUD %)
# ==========================================

model = IsolationForest(
    n_estimators=300,
    contamination="auto",   # Do NOT assume fraud %
    random_state=42
)

model.fit(X)

# ==========================================
# GENERATE ANOMALY SCORES
# ==========================================

# Lower score = more anomalous
df["anomaly_score"] = model.decision_function(X)

# Convert to positive anomaly intensity
df["anomaly_intensity"] = -df["anomaly_score"]

# ==========================================
# DYNAMIC THRESHOLD SELECTION
# ==========================================

# Sort callers by anomaly intensity (highest risk first)
df_sorted = df.sort_values(by="anomaly_intensity", ascending=False)

risk_percent = 0.03

top_k = max(1, int(risk_percent * len(df)))

threshold = df_sorted["anomaly_intensity"].iloc[top_k - 1]

df["predicted_fraud"] = df["anomaly_intensity"] >= threshold

print(f"Risk percentile used: {risk_percent * 100}%")
print(f"Number of high-risk callers selected: {top_k}")
print(f"Dynamic threshold value: {round(threshold, 5)}")



# ==========================================
# RISK SCORE NORMALIZATION (0–100)
# ==========================================

scaler = MinMaxScaler(feature_range=(0, 100))
df["risk_score"] = scaler.fit_transform(df[["anomaly_intensity"]])

# ==========================================
# PERFORMANCE REPORT
# ==========================================

total_callers = len(df)
total_fraud = df["true_label"].sum()
total_normal = total_callers - total_fraud

detected_fraud = df["predicted_fraud"].sum()

true_positive = ((df["predicted_fraud"] == 1) & (df["true_label"] == 1)).sum()
false_positive = ((df["predicted_fraud"] == 1) & (df["true_label"] == 0)).sum()
false_negative = ((df["predicted_fraud"] == 0) & (df["true_label"] == 1)).sum()
true_negative = ((df["predicted_fraud"] == 0) & (df["true_label"] == 0)).sum()

# Safe metric calculations
detection_rate = (true_positive / total_fraud * 100) if total_fraud != 0 else 0
precision = (true_positive / (true_positive + false_positive) * 100) if (true_positive + false_positive) != 0 else 0
false_positive_rate = (false_positive / (false_positive + true_negative) * 100) if (false_positive + true_negative) != 0 else 0
fraud_ratio = (total_fraud / total_callers * 100) if total_callers != 0 else 0

# ==========================================
# PRINT CLEAN REPORT
# ==========================================

print("\n======================================")
print(" TELECOM FRAUD DETECTION REPORT ")
print("======================================\n")

print(f"Total Callers Analysed        : {total_callers}")
print(f"Actual Fraud Callers          : {total_fraud}")
print(f"Actual Normal Callers         : {total_normal}")
print(f"Fraud Ratio in Dataset        : {fraud_ratio:.2f}%\n")

print(f"Fraud Callers Detected        : {detected_fraud}")
print(f"True Positives                : {true_positive}")
print(f"False Positives               : {false_positive}")
print(f"False Negatives               : {false_negative}")
print(f"True Negatives                : {true_negative}\n")

print("----------- METRICS -----------")
print(f"Detection Rate (Recall)       : {detection_rate:.2f}%")
print(f"Precision                     : {precision:.2f}%")
print(f"False Positive Rate           : {false_positive_rate:.2f}%")
print("======================================\n")

# ==========================================
# SAVE OUTPUTS
# ==========================================

df.to_csv("data/fraud_predictions.csv", index=False)
joblib.dump(model, "models/isolation_forest.pkl")

print("Model training, evaluation, and saving complete.")

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