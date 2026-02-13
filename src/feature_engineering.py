import pandas as pd

# Load dataset
df = pd.read_csv("data/call_data.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract hour
df["hour"] = df["timestamp"].dt.hour

# Night call flag
df["is_night"] = df["hour"].apply(lambda x: 1 if x >= 22 or x <= 5 else 0)

# Aggregate behaviour per caller
features = df.groupby("caller_id").agg({
    "call_duration": ["mean", "count"],
    "is_night": "mean",
    "origin_region": "nunique",
    "target_region": "nunique",
    "true_label": "max"  # Preserve fraud ground truth
})

features.columns = [
    "avg_call_duration",
    "total_calls",
    "night_call_ratio",
    "unique_origin_regions",
    "unique_target_regions",
    "true_label"
]

features = features.reset_index()

features.to_csv("data/caller_features.csv", index=False)

print("Feature engineering complete!")
print(f"Total callers processed: {len(features)}")
