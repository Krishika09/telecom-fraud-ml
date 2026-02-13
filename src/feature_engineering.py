import pandas as pd

# Load raw call data
df = pd.read_csv("data/call_data.csv")

# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract hour from timestamp
df["hour"] = df["timestamp"].dt.hour

# Create night call indicator (10 PM to 5 AM)
df["is_night"] = df["hour"].apply(lambda x: 1 if x >= 22 or x <= 5 else 0)

# Aggregate behaviour per caller
features = df.groupby("caller_id").agg({
    "call_duration": ["mean", "count"],
    "is_night": "mean",
    "origin_region": "nunique",
    "target_region": "nunique"
})

# Rename columns properly
features.columns = [
    "avg_call_duration",
    "total_calls",
    "night_call_ratio",
    "unique_origin_regions",
    "unique_target_regions"
]

features = features.reset_index()

# Save behavioural dataset
features.to_csv("data/caller_features.csv", index=False)

print("Feature engineering complete!")
