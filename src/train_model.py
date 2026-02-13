import pandas as pd
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
# TRAIN ISOLATION FOREST
# ==========================================

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Predict anomalies
df["anomaly"] = model.predict(X)

# Convert prediction (-1 = fraud)
df["predicted_fraud"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

# ==========================================
# RISK SCORE GENERATION
# ==========================================

df["raw_score"] = model.decision_function(X)

scaler = MinMaxScaler(feature_range=(0, 100))
df["risk_score"] = scaler.fit_transform(-df[["raw_score"]])

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


print(f"Total Callers Analysed        : {total_callers}")
print(f"Total Fraud Callers (Actual)  : {total_fraud}")
print(f"Total Normal Callers          : {total_normal}")
print(f"Fraud Ratio in Dataset        : {fraud_ratio:.2f}%\n")

print(f"Fraud Callers Detected        : {detected_fraud}")
print(f"True Positives                : {true_positive}")
print(f"False Positives               : {false_positive}")
print(f"False Negatives               : {false_negative}")
print(f"True Negatives                : {true_negative}\n")

print("METRICS")
print(f"Detection Rate (Recall)       : {detection_rate:.2f}%")
print(f"Precision                     : {precision:.2f}%")
print(f"False Positive Rate           : {false_positive_rate:.2f}%")


# ==========================================
# SAVE OUTPUTS
# ==========================================

df.to_csv("data/fraud_predictions.csv", index=False)
joblib.dump(model, "models/isolation_forest.pkl")

print("Model training, evaluation, and saving complete.")
