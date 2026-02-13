import pandas as pd


df = pd.read_csv("data/fraud_predictions.csv")

# Filter only detected fraud callers
fraud_df = df[df["predicted_fraud"] == 1].copy()


def generate_explanation(row):

    reasons = []

    if row["total_calls"] > 2000:
        reasons.append("Extremely high call volume")

    elif row["total_calls"] > 1000:
        reasons.append("High call frequency")

    if row["avg_call_duration"] < 40:
        reasons.append("Very short average call duration")

    if row["night_call_ratio"] > 0.4:
        reasons.append("High night activity")

    if row["unique_target_regions"] > 3:
        reasons.append("Multi-region targeting")

    if row["risk_score"] > 80:
        reasons.append("Very high anomaly risk score")

    if not reasons:
        reasons.append("Anomalous behavioural deviation")

    return " | ".join(reasons)


# Apply explanation
fraud_df["explanation"] = fraud_df.apply(generate_explanation, axis=1)

report_columns = [
    "caller_id",
    "risk_score",
    "total_calls",
    "avg_call_duration",
    "night_call_ratio",
    "unique_target_regions",
    "explanation"
]

fraud_df[report_columns].to_csv(
    "data/fraud_explanation_report.csv",
    index=False
)

print("\n==========================================")
print(" FRAUD EXPLANATION REPORT GENERATED ")
print("==========================================")
print(f"Total Detected Fraud Callers: {len(fraud_df)}")
print("Report saved to: data/fraud_explanation_report.csv")
print("==========================================\n")
