"""
Real-time feature extraction from CDR records
"""
from datetime import datetime
from collections import defaultdict
from typing import Dict, List
import pandas as pd

class FeatureExtractor:
    def __init__(self):
        # Store CDR records per caller (rolling window)
        self.cdr_store: Dict[str, List[Dict]] = defaultdict(list)
        self.max_records_per_caller = 1000  # Keep last 1000 calls per caller
    
    def add_cdr(self, caller_id: str, cdr: Dict):
        """
        Add a CDR record for a caller
        
        Args:
            caller_id: Phone number of caller
            cdr: {
                "destination": str,
                "duration": float,
                "timestamp": float or datetime,
                "origin_region": str,
                "target_region": str
            }
        """
        # Convert timestamp if needed
        if isinstance(cdr.get("timestamp"), (int, float)):
            cdr["timestamp"] = datetime.fromtimestamp(cdr["timestamp"])
        elif isinstance(cdr.get("timestamp"), str):
            cdr["timestamp"] = pd.to_datetime(cdr["timestamp"])
        
        self.cdr_store[caller_id].append(cdr)
        
        # Keep only last N records
        if len(self.cdr_store[caller_id]) > self.max_records_per_caller:
            self.cdr_store[caller_id] = self.cdr_store[caller_id][-self.max_records_per_caller:]
    
    def extract_features(self, caller_id: str) -> List[float]:
        """
        Extract behavioral features for a caller
        
        Returns:
            [avg_call_duration, total_calls, night_call_ratio, 
             unique_origin_regions, unique_target_regions]
        """
        if caller_id not in self.cdr_store or len(self.cdr_store[caller_id]) == 0:
            # Return default features for new caller
            return [0.0, 0.0, 0.0, 0.0, 0.0]
        
        records = self.cdr_store[caller_id]
        
        # Calculate features
        durations = [r.get("duration", 0) for r in records]
        avg_duration = sum(durations) / len(durations) if durations else 0.0
        total_calls = len(records)
        
        # Night call ratio (22:00 - 05:59)
        night_calls = 0
        for r in records:
            hour = r["timestamp"].hour if hasattr(r["timestamp"], "hour") else 0
            if hour >= 22 or hour < 6:
                night_calls += 1
        night_ratio = night_calls / total_calls if total_calls > 0 else 0.0
        
        # Unique regions
        origin_regions = len(set(r.get("origin_region", "") for r in records))
        target_regions = len(set(r.get("target_region", "") for r in records))
        
        return [
            float(avg_duration),
            float(total_calls),
            float(night_ratio),
            float(origin_regions),
            float(target_regions)
        ]
    
    def get_caller_stats(self, caller_id: str) -> Dict:
        """Get detailed stats for a caller"""
        if caller_id not in self.cdr_store:
            return {
                "total_calls": 0,
                "avg_duration": 0.0,
                "night_call_ratio": 0.0,
                "unique_origin_regions": 0,
                "unique_target_regions": 0,
                "last_call": None
            }
        
        records = self.cdr_store[caller_id]
        features = self.extract_features(caller_id)
        
        last_call = max((r.get("timestamp") for r in records), default=None)
        
        return {
            "total_calls": len(records),
            "avg_duration": features[0],
            "night_call_ratio": features[2],
            "unique_origin_regions": int(features[3]),
            "unique_target_regions": int(features[4]),
            "last_call": last_call.isoformat() if last_call else None
        }
