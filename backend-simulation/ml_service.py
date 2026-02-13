"""
ML Service for loading and using the trained fraud detection model
"""
import os
import joblib
import numpy as np
from pathlib import Path

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.is_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and scaler"""
        try:
            # Try to find model in multiple possible locations
            model_paths = [
                Path(__file__).parent.parent / "models" / "fraud_detector.pkl",
                Path(__file__).parent.parent / "src" / "models" / "fraud_detector.pkl",
                Path("models") / "fraud_detector.pkl",
            ]
            
            scaler_paths = [
                Path(__file__).parent.parent / "models" / "risk_scaler.pkl",
                Path(__file__).parent.parent / "src" / "models" / "risk_scaler.pkl",
                Path("models") / "risk_scaler.pkl",
            ]
            
            model_path = None
            scaler_path = None
            
            for path in model_paths:
                if path.exists():
                    model_path = path
                    break
            
            for path in scaler_paths:
                if path.exists():
                    scaler_path = path
                    break
            
            if model_path and scaler_path:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.is_loaded = True
                print(f"✓ ML Model loaded from {model_path}")
                print(f"✓ Scaler loaded from {scaler_path}")
            else:
                print("⚠️  ML Model not found. Using fallback scoring.")
                print("   Run: cd src && python train_model.py to generate model")
        except Exception as e:
            print(f"⚠️  Error loading ML model: {e}")
            print("   Using fallback scoring.")
    
    def predict(self, features: list) -> dict:
        """
        Predict fraud risk from features
        
        Args:
            features: [avg_call_duration, total_calls, night_call_ratio, 
                      unique_origin_regions, unique_target_regions]
        
        Returns:
            {
                "is_fraud": bool,
                "risk_score": float (0-100),
                "anomaly_score": float,
                "prediction": int (-1 = fraud, 1 = normal)
            }
        """
        if not self.is_loaded:
            # Fallback: simple heuristic
            return self._fallback_predict(features)
        
        try:
            # Convert to numpy array and reshape
            features_array = np.array(features).reshape(1, -1)
            
            # Get prediction (-1 = anomaly/fraud, 1 = normal)
            prediction = self.model.predict(features_array)[0]
            
            # Get anomaly score (more negative = more anomalous)
            anomaly_score = self.model.decision_function(features_array)[0]
            
            # Normalize to 0-100 risk score
            # Decision function returns negative for anomalies
            # We need to invert and scale
            risk_score_raw = -anomaly_score
            
            # Use scaler to normalize to 0-100
            risk_score = self.scaler.transform([[risk_score_raw]])[0][0]
            risk_score = max(0, min(100, risk_score))  # Clamp to 0-100
            
            return {
                "is_fraud": prediction == -1,
                "risk_score": float(risk_score),
                "anomaly_score": float(anomaly_score),
                "prediction": int(prediction)
            }
        except Exception as e:
            print(f"Error in ML prediction: {e}")
            return self._fallback_predict(features)
    
    def _fallback_predict(self, features: list) -> dict:
        """Fallback prediction using heuristics"""
        avg_duration, total_calls, night_ratio, origin_regions, target_regions = features
        
        # Heuristic: short calls + high volume + night calls = fraud
        risk_score = 0
        
        if avg_duration < 3:
            risk_score += 30
        if total_calls > 100:
            risk_score += 25
        if night_ratio > 0.4:
            risk_score += 20
        if origin_regions > 3:
            risk_score += 15
        if target_regions > 5:
            risk_score += 10
        
        risk_score = min(100, risk_score)
        is_fraud = risk_score > 50
        
        return {
            "is_fraud": is_fraud,
            "risk_score": float(risk_score),
            "anomaly_score": -risk_score if is_fraud else risk_score,
            "prediction": -1 if is_fraud else 1
        }
