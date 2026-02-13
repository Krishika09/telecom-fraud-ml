"""
Cluster detection for fraud campaigns
"""
from typing import Dict, List
from collections import defaultdict
import time
import uuid

class ClusterDetector:
    def __init__(self):
        self.clusters: Dict[str, Dict] = {}
        self.caller_to_cluster: Dict[str, str] = {}
        self.cluster_counter = 100
    
    def detect_cluster(self, caller_id: str, risk_score: float, fraud_type: str = None) -> str:
        """
        Detect if caller belongs to an existing cluster or create new one
        
        Args:
            caller_id: Phone number
            risk_score: ML risk score (0-100)
            fraud_type: Type of fraud detected
        
        Returns:
            cluster_id: ID of the cluster
        """
        # Only cluster high-risk callers
        if risk_score < 70:
            return None
        
        # Check if caller already in a cluster
        if caller_id in self.caller_to_cluster:
            cluster_id = self.caller_to_cluster[caller_id]
            self._update_cluster(cluster_id, caller_id, risk_score)
            return cluster_id
        
        # Find similar clusters or create new
        cluster_id = self._find_or_create_cluster(caller_id, risk_score, fraud_type)
        return cluster_id
    
    def _find_or_create_cluster(self, caller_id: str, risk_score: float, fraud_type: str) -> str:
        """Find existing cluster or create new one"""
        # Simple clustering: group by fraud type and similar risk
        # In production, would use DBSCAN or similar
        
        fraud_type = fraud_type or "Unknown"
        
        # Find existing cluster with same type and similar risk
        for cid, cluster in self.clusters.items():
            if (cluster["fraud_type"] == fraud_type and 
                abs(cluster["avg_risk"] - risk_score) < 15):
                # Add to existing cluster
                self.caller_to_cluster[caller_id] = cid
                self._update_cluster(cid, caller_id, risk_score)
                return cid
        
        # Create new cluster
        cluster_id = f"cluster_{self.cluster_counter}"
        self.cluster_counter += 1
        
        self.clusters[cluster_id] = {
            "id": cluster_id,
            "name": f"Cluster #{self.cluster_counter - 1} - {fraud_type}",
            "fraud_type": fraud_type,
            "callers": [caller_id],
            "risk_score": risk_score,
            "avg_risk": risk_score,
            "affected_users": 1,
            "status": "Active",
            "created_at": time.time(),
            "last_updated": time.time()
        }
        
        self.caller_to_cluster[caller_id] = cluster_id
        return cluster_id
    
    def _update_cluster(self, cluster_id: str, caller_id: str, risk_score: float):
        """Update cluster with new caller"""
        if cluster_id not in self.clusters:
            return
        
        cluster = self.clusters[cluster_id]
        
        # Add caller if not already in cluster
        if caller_id not in cluster["callers"]:
            cluster["callers"].append(caller_id)
            cluster["affected_users"] = len(cluster["callers"])
        
        # Update average risk
        total_risk = cluster["avg_risk"] * (cluster["affected_users"] - 1) + risk_score
        cluster["avg_risk"] = total_risk / cluster["affected_users"]
        cluster["risk_score"] = int(cluster["avg_risk"])
        cluster["last_updated"] = time.time()
    
    def get_active_clusters(self) -> List[Dict]:
        """Get all active clusters"""
        # Filter active clusters (updated in last 24 hours)
        cutoff = time.time() - 86400  # 24 hours
        
        active = [
            {
                "id": c["id"],
                "name": c["name"],
                "risk_score": c["risk_score"],
                "affected_users": c["affected_users"],
                "status": c["status"]
            }
            for c in self.clusters.values()
            if c["last_updated"] > cutoff
        ]
        
        # Sort by risk score descending
        active.sort(key=lambda x: x["risk_score"], reverse=True)
        return active
    
    def get_cluster_by_caller(self, caller_id: str) -> Dict:
        """Get cluster info for a caller"""
        cluster_id = self.caller_to_cluster.get(caller_id)
        if not cluster_id:
            return None
        
        return self.clusters.get(cluster_id)
