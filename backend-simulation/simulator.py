import random
import time
from faker import Faker
import uuid
from ml_service import MLService
from feature_extractor import FeatureExtractor
from cluster_detector import ClusterDetector
from alert_generator import AlertGenerator

fake = Faker('en_IN')

class FraudSimulator:
    def __init__(self):
        # Initialize services
        self.ml_service = MLService()
        self.feature_extractor = FeatureExtractor()
        self.cluster_detector = ClusterDetector()
        self.alert_generator = AlertGenerator()
        
        # Data storage
        self.caller_predictions = {}  # caller_id -> latest prediction
        self.global_stats = {
            "total_calls": 0,
            "blocked_threats": 0,
            "active_campaigns_count": 0,
            "total_fraud_detected": 0
        }
        
        # Initialize with some mock data for demo (will be replaced by real data)
        self._init_demo_data()
    
    def _init_demo_data(self):
        """Initialize with some demo data for immediate functionality"""
        # This will be replaced as real CDR data comes in
        pass

    def process_cdr(self, cdr_data: dict) -> dict:
        """
        Process a CDR record: extract features, run ML, detect clusters, generate alerts
        
        Args:
            cdr_data: {
                "caller_id": str,
                "destination": str,
                "duration": float,
                "timestamp": float,
                "origin_region": str,
                "target_region": str
            }
        
        Returns:
            {
                "caller_id": str,
                "risk_score": float,
                "is_fraud": bool,
                "cluster_id": str or None,
                "fraud_type": str,
                "alerts": list
            }
        """
        caller_id = cdr_data.get("caller_id") or cdr_data.get("source")
        
        # Add CDR to feature extractor
        self.feature_extractor.add_cdr(caller_id, cdr_data)
        
        # Extract features
        features = self.feature_extractor.extract_features(caller_id)
        
        # Run ML prediction
        prediction = self.ml_service.predict(features)
        
        # Determine fraud type based on features
        fraud_type = self._determine_fraud_type(features, prediction)
        
        # Detect cluster
        cluster_id = self.cluster_detector.detect_cluster(
            caller_id, 
            prediction["risk_score"], 
            fraud_type
        )
        
        # Generate alerts
        alerts = self.cluster_detector.check_and_generate_alerts(
            caller_id,
            prediction["risk_score"],
            cluster_id,
            fraud_type
        )
        
        # Store prediction
        self.caller_predictions[caller_id] = {
            **prediction,
            "cluster_id": cluster_id,
            "fraud_type": fraud_type,
            "features": features,
            "timestamp": time.time()
        }
        
        # Update stats
        self.global_stats["total_calls"] += 1
        if prediction["is_fraud"]:
            self.global_stats["blocked_threats"] += 1
            self.global_stats["total_fraud_detected"] += 1
        
        return {
            "caller_id": caller_id,
            "risk_score": prediction["risk_score"],
            "is_fraud": prediction["is_fraud"],
            "cluster_id": cluster_id,
            "fraud_type": fraud_type,
            "anomaly_score": prediction["anomaly_score"],
            "alerts": [a["id"] for a in alerts]
        }
    
    def _determine_fraud_type(self, features: list, prediction: dict) -> str:
        """Determine fraud type based on behavioral patterns"""
        avg_duration, total_calls, night_ratio, origin_regions, target_regions = features
        
        if not prediction["is_fraud"]:
            return "Legitimate"
        
        # Pattern matching for fraud types
        if avg_duration < 3 and total_calls > 50:
            return "Wangiri"
        elif night_ratio > 0.5 and total_calls > 100:
            return "IRS Impersonation"
        elif target_regions > 5:
            return "Lottery Fraud"
        elif origin_regions > 3:
            return "KYC Phishing"
        else:
            return "Unknown Fraud"
    
    def generate_batch(self, size=5):
        """
        Generate a batch of simulated events for WebSocket streaming
        Uses real ML predictions if available, otherwise generates demo data
        """
        events = []
        for _ in range(size):
            # Generate demo CDR
            caller_id = fake.phone_number()
            destination = fake.phone_number()
            duration = random.randint(0, 300)
            
            # Create CDR
            cdr = {
                "caller_id": caller_id,
                "destination": destination,
                "duration": duration,
                "timestamp": time.time(),
                "origin_region": fake.city(),
                "target_region": fake.city()
            }
            
            # Process through pipeline
            result = self.process_cdr(cdr)
            
            # Create event for WebSocket
            event = {
                "id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "source": caller_id,
                "destination": destination,
                "duration": duration,
                "risk_score": result["risk_score"],
                "type": "Fraud" if result["is_fraud"] else "Legitimate",
                "location": cdr["origin_region"],
                "cluster_id": result.get("cluster_id"),
                "fraud_type": result.get("fraud_type")
            }
            events.append(event)
        
        # Update campaign count
        self.global_stats["active_campaigns_count"] = len(self.cluster_detector.get_active_clusters())
        
        return {
            "events": events,
            "stats": self.global_stats
        }

    def get_active_campaigns(self):
        """Get active fraud clusters"""
        clusters = self.cluster_detector.get_active_clusters()
        return clusters
    
    def get_global_stats(self):
        """Get aggregated global statistics"""
        # Update with real counts
        self.global_stats["active_campaigns_count"] = len(self.cluster_detector.get_active_clusters())
        return self.global_stats
    
    def lookup_number(self, number: str) -> dict:
        """
        Lookup a phone number and return risk assessment
        
        Returns:
            {
                "status": "SAFE" | "SUSPICIOUS" | "DANGEROUS",
                "risk_score": float,
                "category": str,
                "reports": int,
                "carrier": str,
                "last_active": str,
                "fraud_type": str,
                "cluster_id": str,
                "anomaly_score": float,
                "explanation": str
            }
        """
        # Check if we have prediction for this number
        if number in self.caller_predictions:
            pred = self.caller_predictions[number]
            stats = self.feature_extractor.get_caller_stats(number)
            cluster = self.cluster_detector.get_cluster_by_caller(number)
            
            # Determine status
            if pred["risk_score"] >= 85:
                status = "DANGEROUS"
            elif pred["risk_score"] >= 50:
                status = "SUSPICIOUS"
            else:
                status = "SAFE"
            
            # Generate explanation
            explanation = self._generate_explanation(pred, stats)
            
            return {
                "status": status,
                "risk_score": int(pred["risk_score"]),
                "category": pred.get("fraud_type", "Legitimate"),
                "reports": stats["total_calls"],
                "carrier": self._get_carrier(number),
                "last_active": stats["last_call"] or "Unknown",
                "fraud_type": pred.get("fraud_type", "None"),
                "cluster_id": pred.get("cluster_id"),
                "anomaly_score": float(pred["anomaly_score"]),
                "explanation": explanation
            }
        
        # New number - return safe default
        return {
            "status": "SAFE",
            "risk_score": 0,
            "category": "Legitimate",
            "reports": 0,
            "carrier": self._get_carrier(number),
            "last_active": "Never",
            "fraud_type": None,
            "cluster_id": None,
            "anomaly_score": 0.0,
            "explanation": "No historical data available for this number."
        }
    
    def _generate_explanation(self, prediction: dict, stats: dict) -> str:
        """Generate human-readable explanation"""
        parts = []
        
        if prediction["risk_score"] >= 85:
            parts.append(f"High risk score ({prediction['risk_score']:.1f}/100)")
        
        if stats["avg_duration"] < 3:
            parts.append("Very short call durations detected")
        
        if stats["night_call_ratio"] > 0.4:
            parts.append("High proportion of night calls")
        
        if stats["total_calls"] > 100:
            parts.append(f"Unusually high call volume ({stats['total_calls']} calls)")
        
        if prediction.get("cluster_id"):
            parts.append(f"Associated with fraud cluster {prediction['cluster_id']}")
        
        if not parts:
            return "No significant anomalies detected."
        
        return ". ".join(parts) + "."
    
    def _get_carrier(self, number: str) -> str:
        """Mock carrier detection based on number prefix"""
        if not number:
            return "Unknown"
        
        # Simple heuristic for Indian carriers
        if number.startswith("91"):
            number = number[2:]
        
        first_digit = number[0] if number else "0"
        
        carriers = {
            "9": "Jio",
            "8": "Airtel",
            "7": "Vi India",
            "6": "BSNL"
        }
        
        return carriers.get(first_digit, "Unknown")