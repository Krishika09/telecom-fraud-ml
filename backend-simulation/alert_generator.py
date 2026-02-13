"""
Alert generation system
"""
from typing import Dict, List
import time
from enum import Enum

class AlertSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class AlertGenerator:
    def __init__(self):
        self.alerts: List[Dict] = []
        self.alert_counter = 4920
        self.max_alerts = 100  # Keep last 100 alerts
    
    def generate_alert(self, 
                      severity: AlertSeverity,
                      title: str,
                      description: str = None,
                      cluster_id: str = None,
                      caller_id: str = None) -> Dict:
        """
        Generate a new alert
        
        Returns:
            Alert dictionary
        """
        alert = {
            "id": self.alert_counter,
            "severity": severity.value,
            "title": title,
            "description": description or "",
            "cluster_id": cluster_id,
            "caller_id": caller_id,
            "status": "Open",
            "created_at": time.time(),
            "time": self._format_time(time.time())
        }
        
        self.alert_counter += 1
        self.alerts.append(alert)
        
        # Keep only last N alerts
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        return alert
    
    def check_and_generate_alerts(self, 
                                  caller_id: str,
                                  risk_score: float,
                                  cluster_id: str = None,
                                  fraud_type: str = None):
        """Check conditions and generate alerts if needed"""
        alerts_generated = []
        
        # Critical: Very high risk
        if risk_score >= 95:
            alerts_generated.append(
                self.generate_alert(
                    AlertSeverity.CRITICAL,
                    f"Critical Fraud Detected - {fraud_type or 'Unknown Type'}",
                    f"Caller {caller_id} flagged with risk score {risk_score:.1f}",
                    cluster_id,
                    caller_id
                )
            )
        
        # High: High risk cluster growth
        elif risk_score >= 85 and cluster_id:
            alerts_generated.append(
                self.generate_alert(
                    AlertSeverity.HIGH,
                    f"High-Risk Cluster Expansion - {fraud_type or 'Unknown'}",
                    f"Cluster {cluster_id} expanding with new high-risk caller",
                    cluster_id,
                    caller_id
                )
            )
        
        # Medium: New cluster formation
        elif risk_score >= 75 and cluster_id:
            alerts_generated.append(
                self.generate_alert(
                    AlertSeverity.MEDIUM,
                    f"New Fraud Cluster Detected - {fraud_type or 'Unknown'}",
                    f"New cluster {cluster_id} identified with {fraud_type} pattern",
                    cluster_id,
                    caller_id
                )
            )
        
        return alerts_generated
    
    def get_alerts(self, 
                   severity: str = None,
                   status: str = None,
                   limit: int = 50) -> List[Dict]:
        """Get alerts with optional filtering"""
        filtered = self.alerts
        
        if severity:
            filtered = [a for a in filtered if a["severity"] == severity]
        
        if status:
            filtered = [a for a in filtered if a["status"] == status]
        
        # Sort by creation time (newest first)
        filtered.sort(key=lambda x: x["created_at"], reverse=True)
        
        return filtered[:limit]
    
    def _format_time(self, timestamp: float) -> str:
        """Format timestamp to relative time string"""
        diff = time.time() - timestamp
        
        if diff < 60:
            return f"{int(diff)}s ago"
        elif diff < 3600:
            return f"{int(diff / 60)}m ago"
        elif diff < 86400:
            return f"{int(diff / 3600)}h ago"
        else:
            return f"{int(diff / 86400)}d ago"
    
    def mark_resolved(self, alert_id: int):
        """Mark an alert as resolved"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["status"] = "Resolved"
                break
