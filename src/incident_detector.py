"""
Incident Detection Module
"""

import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class IncidentDetector:
    """Detect incidents based on metrics and patterns"""
    
    def __init__(self, config: Dict):
        """
        Initialize incident detector
        
        Args:
            config: Configuration dictionary
        """
        self.thresholds = config.get('thresholds', {
            'cpu_usage': 90,
            'memory_usage': 85,
            'error_rate': 10
        })
        logger.info("Initialized Incident Detector")
    
    def check_thresholds(self, metrics: Dict[str, float]) -> bool:
        """
        Check if any metric exceeds threshold
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            True if threshold exceeded, False otherwise
        """
        for metric, value in metrics.items():
            threshold_key = metric
            if threshold_key in self.thresholds:
                if value >= self.thresholds[threshold_key]:
                    logger.warning(f"Threshold exceeded: {metric}={value} >= {self.thresholds[threshold_key]}")
                    return True
        
        return False
    
    def analyze_trends(self, historical_metrics: list) -> Optional[Dict]:
        """
        Analyze metric trends for anomalies
        
        Args:
            historical_metrics: List of historical metric readings
            
        Returns:
            Trend analysis or None
        """
        if len(historical_metrics) < 2:
            return None
        
        # Simple trend detection
        recent = historical_metrics[-1]
        previous = historical_metrics[-2]
        
        trends = {}
        for key in recent.keys():
            if key in previous and isinstance(recent[key], (int, float)):
                change = recent[key] - previous[key]
                percent_change = (change / previous[key] * 100) if previous[key] != 0 else 0
                
                if abs(percent_change) > 20:  # 20% change threshold
                    trends[key] = {
                        'change': change,
                        'percent_change': percent_change,
                        'direction': 'increasing' if change > 0 else 'decreasing'
                    }
        
        return trends if trends else None
