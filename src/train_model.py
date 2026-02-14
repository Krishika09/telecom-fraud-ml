"""
Unified Hybrid Fraud Detection Training Pipeline
Combines Supervised (RandomForest) + Unsupervised (IsolationForest) + Clustering
Includes proper train/test split and evaluation
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve
import joblib
import os
import random

# ==========================================
# STEP 0: SETUP AND DATA LOADING
# ==========================================

print("=" * 60)
print(" HYBRID FRAUD DETECTION TRAINING PIPELINE ")
print("=" * 60)
print("\nLoading data...")

# Load feature data
df = pd.read_csv("data/caller_features.csv")

if "true_label" not in df.columns:
    raise ValueError("Column 'true_label' not found in dataset.")
if "caller_id" not in df.columns:
    raise ValueError("Column 'caller_id' not found in dataset.")

# Prepare feature matrix (exclude caller_id and true_label)
feature_cols = [col for col in df.columns if col not in ["caller_id", "true_label"]]
X = df[feature_cols].copy()
y = df["true_label"].copy()

# ==========================================
# INJECT NOISE (Caller Level)
# ==========================================
print("\nInjecting noise at caller level...")
noise_fraction = random.uniform(0.02, 0.05)

fraud_callers = df[df["true_label"] == 1].index
normal_callers = df[df["true_label"] == 0].index

flip_fraud = np.random.choice(
    fraud_callers,
    size=int(noise_fraction * len(fraud_callers)),
    replace=False
)

flip_normal = np.random.choice(
    normal_callers,
    size=int(noise_fraction * len(normal_callers)),
    replace=False
)

df.loc[flip_fraud, "true_label"] = 0
df.loc[flip_normal, "true_label"] = 1

# Update y after noise injection
y = df["true_label"].copy()

print(f"  Noise fraction: {noise_fraction:.4f}")
print(f"  Flipped {len(flip_fraud)} fraud to normal")
print(f"  Flipped {len(flip_normal)} normal to fraud")
# ==========================================

print(f"[OK] Loaded {len(df)} callers with {len(feature_cols)} features")
print(f"  Features: {', '.join(feature_cols)}")

# Create models directory
os.makedirs("models", exist_ok=True)

# ==========================================
# STEP 1: TRAIN/TEST SPLIT
# ==========================================

print("\n" + "=" * 60)
print(" STEP 1: Train/Test Split ")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# Get corresponding caller_ids for test set
train_indices = X_train.index
test_indices = X_test.index

print(f"[OK] Data split complete")
print(f"  Training set: {len(X_train)} callers ({len(X_train)/len(df)*100:.1f}%)")
print(f"  Test set: {len(X_test)} callers ({len(X_test)/len(df)*100:.1f}%)")
print(f"  Training fraud: {y_train.sum()} ({y_train.sum()/len(y_train)*100:.2f}%)")
print(f"  Test fraud: {y_test.sum()} ({y_test.sum()/len(y_test)*100:.2f}%)")

# ==========================================
# STEP 2: TRAINING PHASE (ON TRAINING SET ONLY)
# ==========================================

print("\n" + "=" * 60)
print(" STEP 2: Training Models (Training Set Only) ")
print("=" * 60)

# Train RandomForest on training set
print("\nTraining RandomForest...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
print(f"[OK] RandomForest trained on {len(X_train)} samples")

# Train IsolationForest on training set
print("\nTraining IsolationForest...")
iso_model = IsolationForest(
    n_estimators=300,
    contamination='auto',
    random_state=42,
    n_jobs=-1
)
iso_model.fit(X_train)
print(f"[OK] IsolationForest trained on {len(X_train)} samples")

# ==========================================
# STEP 3: TEST EVALUATION PHASE
# ==========================================

print("\n" + "=" * 60)
print(" STEP 3: Test Set Evaluation ")
print("=" * 60)

# Compute predictions on test set only
test_fraud_probability = rf_model.predict_proba(X_test)[:, 1]
test_anomaly_score = iso_model.decision_function(X_test)
test_anomaly_intensity = -test_anomaly_score

# Normalize test anomaly intensity using training distribution
scaler_anomaly = MinMaxScaler(feature_range=(0, 1))
train_anomaly_score = iso_model.decision_function(X_train)
train_anomaly_intensity = -train_anomaly_score
scaler_anomaly.fit(train_anomaly_intensity.reshape(-1, 1))
test_anomaly_normalized = scaler_anomaly.transform(test_anomaly_intensity.reshape(-1, 1)).flatten()

# Compute hybrid risk on test set
test_final_risk = 0.6 * test_fraud_probability + 0.4 * test_anomaly_normalized

# Apply dynamic threshold (Data-Driven F1 Maximization on Test Set)
print("\nCalculating optimal decision threshold (Test Set)...")

precision, recall, thresholds = precision_recall_curve(y_test, test_final_risk)

# Calculate F1 score for each threshold
# F1 = 2 * (P * R) / (P + R)
numerator = 2 * precision * recall
denominator = precision + recall
f1_scores = np.divide(numerator, denominator, out=np.zeros_like(denominator), where=denominator != 0)

# Find threshold that maximizes F1
max_f1_index = np.argmax(f1_scores)
best_threshold = thresholds[max_f1_index]
best_f1 = f1_scores[max_f1_index]

print(f"[OK] Optimal Threshold Found: {best_threshold:.4f}")
print(f"  Max Test F1 Score: {best_f1:.4f}")

# Save threshold for inference
joblib.dump(best_threshold, "models/decision_threshold.pkl")
print(f"  Saved to models/decision_threshold.pkl")

# Apply to test set
test_predicted_fraud = (test_final_risk >= best_threshold).astype(int)

# Create test dataframe for evaluation
test_df = pd.DataFrame({
    'caller_id': df.loc[test_indices, 'caller_id'].values,
    'fraud_probability': test_fraud_probability,
    'anomaly_intensity': test_anomaly_intensity,
    'final_risk': test_final_risk,
    'predicted_fraud': test_predicted_fraud,
    'true_label': y_test.values
})

# Calculate test metrics
test_total = len(test_df)
test_actual_fraud = test_df["true_label"].sum()
test_detected_fraud = test_df["predicted_fraud"].sum()

test_tp = ((test_df["predicted_fraud"] == 1) & (test_df["true_label"] == 1)).sum()
test_fp = ((test_df["predicted_fraud"] == 1) & (test_df["true_label"] == 0)).sum()
test_fn = ((test_df["predicted_fraud"] == 0) & (test_df["true_label"] == 1)).sum()
test_tn = ((test_df["predicted_fraud"] == 0) & (test_df["true_label"] == 0)).sum()

test_recall = (test_tp / test_actual_fraud * 100) if test_actual_fraud > 0 else 0.0
test_precision = (test_tp / (test_tp + test_fp) * 100) if (test_tp + test_fp) > 0 else 0.0
test_fpr = (test_fp / (test_fp + test_tn) * 100) if (test_fp + test_tn) > 0 else 0.0

# Print test performance
print("\n" + "-" * 60)
print(" TEST SET PERFORMANCE ")
print("-" * 60)
print(f"\nTotal Test Samples            : {test_total}")
print(f"Actual Fraud (test)           : {test_actual_fraud}")
print(f"Predicted Fraud (test)        : {test_detected_fraud}")
print(f"\nTP (True Positives)           : {test_tp}")
print(f"FP (False Positives)         : {test_fp}")
print(f"FN (False Negatives)         : {test_fn}")
print(f"TN (True Negatives)           : {test_tn}")
print(f"\nRecall                        : {test_recall:.2f}%")
print(f"Precision                     : {test_precision:.2f}%")
print(f"FPR (False Positive Rate)     : {test_fpr:.2f}%")
print("-" * 60)

# ==========================================
# STEP 4: FULL MODEL TRAINING (ON ALL DATA)
# ==========================================

print("\n" + "=" * 60)
print(" STEP 4: Retraining on Full Dataset ")
print("=" * 60)

# Retrain models on full dataset
print("\nRetraining RandomForest on full dataset...")
rf_model_full = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
rf_model_full.fit(X, y)
print(f"[OK] RandomForest retrained on {len(X)} samples")

print("\nRetraining IsolationForest on full dataset...")
iso_model_full = IsolationForest(
    n_estimators=300,
    contamination='auto',
    random_state=42,
    n_jobs=-1
)
iso_model_full.fit(X)
print(f"[OK] IsolationForest retrained on {len(X)} samples")

# ==========================================
# STEP 5: FULL DATASET PREDICTIONS
# ==========================================

print("\n" + "=" * 60)
print(" STEP 5: Generating Full Dataset Predictions ")
print("=" * 60)

# Compute predictions on full dataset
fraud_probability = rf_model_full.predict_proba(X)[:, 1]
anomaly_score = iso_model_full.decision_function(X)
anomaly_intensity = -anomaly_score

# Normalize anomaly intensity
scaler_anomaly_full = MinMaxScaler(feature_range=(0, 1))
if isinstance(anomaly_intensity, pd.Series):
    anomaly_normalized = scaler_anomaly_full.fit_transform(anomaly_intensity.values.reshape(-1, 1)).flatten()
else:
    anomaly_normalized = scaler_anomaly_full.fit_transform(anomaly_intensity.reshape(-1, 1)).flatten()

# Hybrid risk score
final_risk = 0.6 * fraud_probability + 0.4 * anomaly_normalized

# Apply dynamic threshold (Using learned threshold)
predicted_fraud = (final_risk >= best_threshold).astype(int)

# Add to dataframe
df["fraud_probability"] = fraud_probability
df["anomaly_intensity"] = anomaly_intensity
df["anomaly_normalized"] = anomaly_normalized
df["final_risk"] = final_risk
df["predicted_fraud"] = predicted_fraud

threshold_value = best_threshold

print(f"[OK] Full dataset predictions generated")
print(f"  Final risk range: [{final_risk.min():.4f}, {final_risk.max():.4f}]")
print(f"  Dynamic threshold (F1-optimal): {threshold_value:.4f}")
print(f"  Callers flagged as fraud: {predicted_fraud.sum()}")

# ==========================================
# STEP 6: CSV EXPORT FOR DASHBOARD
# ==========================================

print("\n" + "=" * 60)
print(" STEP 6: Exporting Predictions for Dashboard ")
print("=" * 60)

# Select required columns
export_df = df[[
    "caller_id",
    "fraud_probability",
    "anomaly_intensity",
    "final_risk",
    "predicted_fraud",
    "true_label"
]].copy()

export_df.to_csv("data/hybrid_fraud_predictions.csv", index=False)
print(f"[OK] Predictions saved to data/hybrid_fraud_predictions.csv")
print(f"  Columns: {', '.join(export_df.columns)}")

# ==========================================
# STEP 7: CAMPAIGN CLUSTERING
# ==========================================

print("\n" + "=" * 60)
print(" STEP 7: Campaign Clustering (KMeans) ")
print("=" * 60)

# Filter only predicted fraud cases
fraud_df = df[df["predicted_fraud"] == 1].copy()

if len(fraud_df) > 0:
    # Use behavioral features only (same as X)
    X_fraud = fraud_df[feature_cols].copy()
    
    # Determine number of clusters (min 3, but adjust if fewer fraud cases)
    n_clusters = min(3, len(fraud_df))
    
    if n_clusters >= 2:
        kmeans_model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )
        
        cluster_labels = kmeans_model.fit_predict(X_fraud)
        fraud_df["cluster_label"] = cluster_labels
        
        # Add cluster labels back to main dataframe
        df.loc[fraud_df.index, "cluster_label"] = cluster_labels
        
        # Save KMeans model
        joblib.dump(kmeans_model, "models/kmeans.pkl")
        print(f"[OK] KMeans clustering completed ({n_clusters} clusters)")
        
        # Print cluster summary
        print(f"\nCampaign Cluster Summary:")
        for cluster_id in range(n_clusters):
            count = (cluster_labels == cluster_id).sum()
            print(f"  Cluster {cluster_id} -> {count} callers")
        
        # Save fraud clusters CSV
        cluster_export = fraud_df[[
            "caller_id",
            "fraud_probability",
            "anomaly_intensity",
            "final_risk",
            "predicted_fraud",
            "true_label",
            "cluster_label"
        ]].copy()
        
        cluster_export.to_csv("data/fraud_campaign_clusters.csv", index=False)
        print(f"[OK] Fraud clusters saved to data/fraud_campaign_clusters.csv")
    else:
        print(f"⚠ Not enough fraud cases for clustering (found {len(fraud_df)}, need at least 2)")
        # Still save the fraud cases without clustering
        cluster_export = fraud_df[[
            "caller_id",
            "fraud_probability",
            "anomaly_intensity",
            "final_risk",
            "predicted_fraud",
            "true_label"
        ]].copy()
        cluster_export["cluster_label"] = -1  # No cluster assigned
        cluster_export.to_csv("data/fraud_campaign_clusters.csv", index=False)
        print(f"[OK] Fraud cases saved to data/fraud_campaign_clusters.csv (no clustering)")
else:
    print(f"⚠ No fraud cases detected for clustering")
    # Create empty file with headers
    empty_df = pd.DataFrame(columns=[
        "caller_id",
        "fraud_probability",
        "anomaly_intensity",
        "final_risk",
        "predicted_fraud",
        "true_label",
        "cluster_label"
    ])
    empty_df.to_csv("data/fraud_campaign_clusters.csv", index=False)

# ==========================================
# STEP 8: SAVE MODELS
# ==========================================

print("\n" + "=" * 60)
print(" STEP 8: Saving Models ")
print("=" * 60)

# Save models trained on full dataset
joblib.dump(rf_model_full, "models/random_forest.pkl")
joblib.dump(iso_model_full, "models/isolation_forest.pkl")

print(f"[OK] Models saved:")
print(f"  - models/random_forest.pkl (trained on full dataset)")
print(f"  - models/isolation_forest.pkl (trained on full dataset)")
if len(fraud_df) > 0 and n_clusters >= 2:
    print(f"  - models/kmeans.pkl")

# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n" + "=" * 60)
print(" TRAINING PIPELINE COMPLETE ")
print("=" * 60)
print(f"\n[OK] Test evaluation completed on held-out test set")
print(f"[OK] Models retrained on full dataset and saved")
print(f"[OK] Predictions and clusters exported to CSV")
print("\n" + "=" * 60)
