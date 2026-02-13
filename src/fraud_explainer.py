import pandas as pd
import numpy as np

# ==========================================
# LOAD FRAUD PREDICTIONS
# ==========================================

df = pd.read_csv("data/fraud_predictions.csv")

# Separate detected fraud callers
fraud_df = df[df["predicted_fraud"] == 1].copy()

# ==========================================
# COMPUTE POPULATION STATISTICS
# ==========================================

metrics = [
    "total_calls",
    "avg_call_duration",
    "night_call_ratio",
    "unique_target_regions"
]

population_mean = df[metrics].mean()
population_std = df[metrics].std()

# ==========================================
# EXPLANATION ENGINE
# ==========================================

def generate_statistical_explanation(row):

    reasons = []

    for metric in metrics:

        if population_std[metric] == 0:
            continue

        z_score = (row[metric] - population_mean[metric]) / population_std[metric]

        if abs(z_score) > 2:  # Strong deviation
            direction = "higher" if z_score > 0 else "lower"
            reasons.append(
                f"{metric.replace('_',' ').title()} significantly {direction} than average "
                f"(z-score = {z_score:.2f})"
            )

    if not reasons:
        reasons.append("Detected as multivariate anomaly by Isolation Forest")

    return " | ".join(reasons)

# Apply explanation
fraud_df["explanation"] = fraud_df.apply(generate_statistical_explanation, axis=1)

# ==========================================
# SAVE FULL FRAUD REPORT
# ==========================================

fraud_df.to_csv(
    "data/fraud_explanation_report.csv",
    index=False
)

print("\n==========================================")
print(" FRAUD EXPLANATION REPORT GENERATED ")
print("==========================================")
print(f"Total Detected Fraud Callers: {len(fraud_df)}")
print("Report saved to: data/fraud_explanation_report.csv")
print("==========================================\n")
