"""
Review Models and Training Data
Inspect trained models and generated predictions
"""
import joblib
import pandas as pd
import os

print("=" * 60)
print(" MODEL AND DATA REVIEW ")
print("=" * 60)

# ==========================================
# Review Model Files
# ==========================================

models_dir = "../models"
data_dir = "../data"

print("\n1. MODEL FILES")
print("-" * 60)

model_files = {
    "RandomForest": "random_forest.pkl",
    "IsolationForest": "isolation_forest.pkl",
    "KMeans": "kmeans.pkl"
}

for model_name, filename in model_files.items():
    filepath = os.path.join(models_dir, filename)
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath) / 1024  # KB
        print(f"\n{model_name}:")
        print(f"  File: {filename}")
        print(f"  Size: {file_size:.2f} KB")
        
        try:
            model = joblib.load(filepath)
            print(f"  Type: {type(model).__name__}")
            
            # Model-specific info
            if hasattr(model, 'n_estimators'):
                print(f"  Estimators: {model.n_estimators}")
            if hasattr(model, 'n_clusters'):
                print(f"  Clusters: {model.n_clusters}")
            if hasattr(model, 'feature_names_in_'):
                print(f"  Features: {len(model.feature_names_in_)}")
                print(f"    {', '.join(model.feature_names_in_)}")
            if hasattr(model, 'contamination'):
                print(f"  Contamination: {model.contamination}")
        except Exception as e:
            print(f"  Error loading: {e}")
    else:
        print(f"\n{model_name}: NOT FOUND")

# ==========================================
# Review Data Files
# ==========================================

print("\n\n2. DATA FILES")
print("-" * 60)

data_files = {
    "Hybrid Predictions": "hybrid_fraud_predictions.csv",
    "Fraud Clusters": "fraud_campaign_clusters.csv",
    "Caller Features": "caller_features.csv"
}

for data_name, filename in data_files.items():
    filepath = os.path.join(data_dir, filename)
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            print(f"\n{data_name} ({filename}):")
            print(f"  Rows: {len(df):,}")
            print(f"  Columns: {len(df.columns)}")
            print(f"  Columns: {', '.join(df.columns)}")
            
            # Show statistics for key columns
            if 'predicted_fraud' in df.columns:
                fraud_count = df['predicted_fraud'].sum()
                print(f"  Predicted Fraud: {fraud_count} ({fraud_count/len(df)*100:.2f}%)")
            
            if 'true_label' in df.columns:
                actual_fraud = df['true_label'].sum()
                print(f"  Actual Fraud: {actual_fraud} ({actual_fraud/len(df)*100:.2f}%)")
            
            if 'final_risk' in df.columns:
                print(f"  Final Risk Range: [{df['final_risk'].min():.4f}, {df['final_risk'].max():.4f}]")
                print(f"  Final Risk Mean: {df['final_risk'].mean():.4f}")
            
            if 'cluster_label' in df.columns:
                clusters = df['cluster_label'].value_counts().sort_index()
                print(f"  Clusters:")
                for cluster_id, count in clusters.items():
                    print(f"    Cluster {cluster_id}: {count} callers")
            
            # Show first few rows
            print(f"\n  First 3 rows:")
            print(df.head(3).to_string(index=False))
            
        except Exception as e:
            print(f"\n{data_name}: Error reading - {e}")
    else:
        print(f"\n{data_name}: NOT FOUND")

# ==========================================
# Summary Statistics
# ==========================================

print("\n\n3. SUMMARY STATISTICS")
print("-" * 60)

try:
    pred_file = os.path.join(data_dir, "hybrid_fraud_predictions.csv")
    if os.path.exists(pred_file):
        df = pd.read_csv(pred_file)
        
        if 'predicted_fraud' in df.columns and 'true_label' in df.columns:
            tp = ((df['predicted_fraud'] == 1) & (df['true_label'] == 1)).sum()
            fp = ((df['predicted_fraud'] == 1) & (df['true_label'] == 0)).sum()
            fn = ((df['predicted_fraud'] == 0) & (df['true_label'] == 1)).sum()
            tn = ((df['predicted_fraud'] == 0) & (df['true_label'] == 0)).sum()
            
            recall = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0
            precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0
            
            print(f"\nConfusion Matrix:")
            print(f"  True Positives:  {tp}")
            print(f"  False Positives: {fp}")
            print(f"  False Negatives: {fn}")
            print(f"  True Negatives:  {tn}")
            print(f"\nMetrics:")
            print(f"  Recall:    {recall:.2f}%")
            print(f"  Precision: {precision:.2f}%")
except Exception as e:
    print(f"Error calculating statistics: {e}")

print("\n" + "=" * 60)
print(" REVIEW COMPLETE ")
print("=" * 60)
