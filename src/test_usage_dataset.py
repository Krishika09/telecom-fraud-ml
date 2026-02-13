import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler


# Replace with your actual file name
df = pd.read_csv("data/your_usage_dataset.csv")

print("\nDataset Loaded Successfully")
print("Total Records:", len(df))


# Convert Yes/No columns to 1/0 if present
for col in ["international plan", "voice mail plan"]:
    if col in df.columns:
        df[col] = df[col].map({"Yes": 1, "No": 0})

# Drop non-feature columns
drop_columns = ["state", "area code", "phone number", "churn"]

X = df.drop(columns=[col for col in drop_columns if col in df.columns])

# Keep only numeric columns
X = X.select_dtypes(include=["int64", "float64"])

print("Features Used for Anomaly Detection:")
print(X.columns.tolist())


model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Predict anomalies
df["anomaly"] = model.predict(X)
df["usage_anomaly_flag"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

# Risk score
df["raw_score"] = model.decision_function(X)
scaler = MinMaxScaler(feature_range=(0, 100))
df["risk_score"] = scaler.fit_transform(-df[["raw_score"]])

total_accounts = len(df)
detected_anomalies = df["usage_anomaly_flag"].sum()
anomaly_ratio = (detected_anomalies / total_accounts) * 100

print("\n======================================")
print(" TELECOM USAGE ANOMALY REPORT ")
print("======================================")
print(f"Total Accounts Analysed   : {total_accounts}")
print(f"Anomalous Accounts Found  : {detected_anomalies}")
print(f"Anomaly Ratio             : {anomaly_ratio:.2f}%")
print("======================================\n")

# Save report
df.to_csv("data/usage_anomaly_report.csv", index=False)

print("Usage anomaly report saved to data/usage_anomaly_report.csv")
