"""Telemetry collection and analytics"""

from typing import Dict, Any, List
from datetime import datetime


class TelemetryCollector:
    """Collects usage analytics and performance metrics"""
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.stats = {
            "total_requests": 0,
            "total_cost": 0.0,
            "total_tokens": 0,
            "average_cost": 0.0,
            "average_quality": 0.0,
            "average_response_time": 0.0,
            "cost_savings": 0.0,
            "savings_percent": 0.0,
        }
    
    def record_request(self, event_data: Dict[str, Any]) -> None:
        """Record a request event"""
        event_data["timestamp"] = datetime.utcnow().isoformat()
        self.events.append(event_data)
        self._update_stats(event_data)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return self.stats.copy()
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all recorded events"""
        return self.events.copy()
    
    def clear_events(self) -> None:
        """Clear all recorded events"""
        self.events.clear()
        self.stats = {
            "total_requests": 0,
            "total_cost": 0.0,
            "total_tokens": 0,
            "average_cost": 0.0,
            "average_quality": 0.0,
            "average_response_time": 0.0,
            "cost_savings": 0.0,
            "savings_percent": 0.0,
        }
    
    def _update_stats(self, event_data: Dict[str, Any]) -> None:
        """Update internal statistics"""
        self.stats["total_requests"] += 1
        
        if "cost" in event_data:
            self.stats["total_cost"] += event_data["cost"]
            self.stats["average_cost"] = self.stats["total_cost"] / self.stats["total_requests"]
        
        if "tokens_used" in event_data:
            self.stats["total_tokens"] += event_data["tokens_used"]