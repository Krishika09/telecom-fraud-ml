"""
Inference Pipeline for Testing Saved Models on New Unseen Data
Loads trained models and applies them to new caller_features.csv
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

print("=" * 60)
print(" INFERENCE PIPELINE - Testing on New Data ")
print("=" * 60)

# ==========================================
# STEP 1: LOAD SAVED MODELS
# ==========================================

print("\nLoading saved models...")

models_dir = "models"

# Load RandomForest
rf_path = os.path.join(models_dir, "random_forest.pkl")
if not os.path.exists(rf_path):
    raise FileNotFoundError(f"Model not found: {rf_path}")
rf_model = joblib.load(rf_path)
print(f"[OK] RandomForest loaded from {rf_path}")

# Load IsolationForest
iso_path = os.path.join(models_dir, "isolation_forest.pkl")
if not os.path.exists(iso_path):
    raise FileNotFoundError(f"Model not found: {iso_path}")
iso_model = joblib.load(iso_path)
print(f"[OK] IsolationForest loaded from {iso_path}")

# Load KMeans (optional)
kmeans_path = os.path.join(models_dir, "kmeans.pkl")
kmeans_model = None
if os.path.exists(kmeans_path):
    kmeans_model = joblib.load(kmeans_path)
    print(f"[OK] KMeans loaded from {kmeans_path}")
else:
    print(f"[INFO] KMeans model not found (optional)")

# ==========================================
# STEP 2: LOAD NEW DATA
# ==========================================

print("\nLoading new dataset...")
data_path = "data/caller_features.csv"

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data file not found: {data_path}")

df = pd.read_csv(data_path)

if "caller_id" not in df.columns:
    raise ValueError("Column 'caller_id' not found in dataset.")

# Check if true_label exists (for evaluation)
has_labels = "true_label" in df.columns

# Prepare feature matrix (exclude caller_id and true_label if exists)
feature_cols = [col for col in df.columns if col not in ["caller_id", "true_label"]]
X = df[feature_cols].copy()

print(f"[OK] Loaded {len(df)} callers with {len(feature_cols)} features")
print(f"  Features: {', '.join(feature_cols)}")
if has_labels:
    print(f"  Ground truth labels available: {df['true_label'].sum()} fraud cases")
else:
    print(f"  No ground truth labels (inference only)")

# ==========================================
# STEP 3: COMPUTE PREDICTIONS
# ==========================================

print("\n" + "=" * 60)
print(" Computing Predictions ")
print("=" * 60)

# Fraud probability from RandomForest
print("\nComputing fraud probability...")
fraud_probability = rf_model.predict_proba(X)[:, 1]
print(f"[OK] Fraud probability range: [{fraud_probability.min():.4f}, {fraud_probability.max():.4f}]")

# Anomaly scores from IsolationForest
print("\nComputing anomaly scores...")
anomaly_score = iso_model.decision_function(X)
anomaly_intensity = -anomaly_score
print(f"[OK] Anomaly intensity range: [{anomaly_intensity.min():.4f}, {anomaly_intensity.max():.4f}]")

# Normalize anomaly intensity to 0-1 range
# Use the same normalization approach as training
scaler_anomaly = MinMaxScaler(feature_range=(0, 1))
if isinstance(anomaly_intensity, pd.Series):
    anomaly_normalized = scaler_anomaly.fit_transform(anomaly_intensity.values.reshape(-1, 1)).flatten()
else:
    anomaly_normalized = scaler_anomaly.fit_transform(anomaly_intensity.reshape(-1, 1)).flatten()
print(f"[OK] Normalized anomaly range: [{anomaly_normalized.min():.4f}, {anomaly_normalized.max():.4f}]")

# Hybrid risk score
print("\nComputing hybrid risk score...")
final_risk = 0.6 * fraud_probability + 0.4 * anomaly_normalized
print(f"[OK] Final risk range: [{final_risk.min():.4f}, {final_risk.max():.4f}]")

# ==========================================
# STEP 4: APPLY DYNAMIC THRESHOLD
# ==========================================

print("\nLoading decision threshold...")
threshold_path = os.path.join(models_dir, "decision_threshold.pkl")
if not os.path.exists(threshold_path):
    raise FileNotFoundError(f"Threshold file not found: {threshold_path}")

decision_threshold = joblib.load(threshold_path)
print(f"[OK] Decision threshold loaded: {decision_threshold:.4f}")

print("\nApplying dynamic threshold...")
predicted_fraud = (final_risk >= decision_threshold).astype(int)

print(f"[OK] Dynamic threshold applied")
print(f"  Threshold value: {decision_threshold:.4f}")
print(f"  Callers flagged as fraud: {predicted_fraud.sum()} ({predicted_fraud.sum()/len(df)*100:.2f}%)")

# ==========================================
# STEP 5: INFERENCE REPORT
# ==========================================

print("\n" + "=" * 60)
print(" INFERENCE REPORT ")
print("=" * 60)

print(f"\nTotal Callers                 : {len(df):,}")
print(f"Predicted Fraud Count         : {predicted_fraud.sum()}")
print(f"Risk Score Range              : [{final_risk.min():.4f}, {final_risk.max():.4f}]")
print(f"Risk Score Mean               : {final_risk.mean():.4f}")

# If true_label exists, compute evaluation metrics
if has_labels:
    true_label = df["true_label"].values
    
    tp = ((predicted_fraud == 1) & (true_label == 1)).sum()
    fp = ((predicted_fraud == 1) & (true_label == 0)).sum()
    fn = ((predicted_fraud == 0) & (true_label == 1)).sum()
    tn = ((predicted_fraud == 0) & (true_label == 0)).sum()
    
    actual_fraud = true_label.sum()
    
    recall = (tp / actual_fraud * 100) if actual_fraud > 0 else 0.0
    precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0.0
    
    print(f"\nActual Fraud                  : {actual_fraud}")
    print(f"\nTP (True Positives)           : {tp}")
    print(f"FP (False Positives)         : {fp}")
    print(f"FN (False Negatives)         : {fn}")
    print(f"TN (True Negatives)           : {tn}")
    print(f"\nRecall                        : {recall:.2f}%")
    print(f"Precision                     : {precision:.2f}%")
else:
    print(f"\n[INFO] No ground truth labels available for evaluation")

# ==========================================
# STEP 6: SAVE INFERENCE RESULTS
# ==========================================

print("\n" + "=" * 60)
print(" Saving Inference Results ")
print("=" * 60)

# Create results dataframe
results_df = pd.DataFrame({
    "caller_id": df["caller_id"].values,
    "fraud_probability": fraud_probability,
    "anomaly_intensity": anomaly_intensity,
    "final_risk": final_risk,
    "predicted_fraud": predicted_fraud
})

# Add true_label if available
if has_labels:
    results_df["true_label"] = df["true_label"].values

# Save to CSV
output_path = "data/inference_results.csv"
results_df.to_csv(output_path, index=False)

print(f"[OK] Inference results saved to {output_path}")
print(f"  Columns: {', '.join(results_df.columns)}")
print(f"  Rows: {len(results_df):,}")

# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n" + "=" * 60)
print(" INFERENCE PIPELINE COMPLETE ")
print("=" * 60)
print(f"\n[OK] Models loaded and applied to new dataset")
print(f"[OK] Predictions generated using hybrid scoring")
print(f"[OK] Results saved to {output_path}")
print("\n" + "=" * 60)
