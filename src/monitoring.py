"""
System Monitoring Module
"""

import logging
import psutil
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitor system metrics and health"""
    
    def __init__(self, config: Dict):
        """
        Initialize system monitor
        
        Args:
            config: Configuration dictionary
        """
        self.interval = config.get('interval', 60)
        self.metrics = config.get('metrics', ['cpu', 'memory', 'disk', 'network'])
        logger.info("Initialized System Monitor")
    
    def get_current_state(self) -> Dict:
        """
        Get current system state
        
        Returns:
            Dictionary with current metrics
        """
        state = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {}
        }
        
        if 'cpu' in self.metrics:
            state['metrics']['cpu'] = self._get_cpu_metrics()
        
        if 'memory' in self.metrics:
            state['metrics']['memory'] = self._get_memory_metrics()
        
        if 'disk' in self.metrics:
            state['metrics']['disk'] = self._get_disk_metrics()
        
        if 'network' in self.metrics:
            state['metrics']['network'] = self._get_network_metrics()
        
        return state
    
    def _get_cpu_metrics(self) -> Dict:
        """Get CPU metrics"""
        return {
            'usage_percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
        }
    
    def _get_memory_metrics(self) -> Dict:
        """Get memory metrics"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent
        }
    
    def _get_disk_metrics(self) -> Dict:
        """Get disk metrics"""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    
    def _get_network_metrics(self) -> Dict:
        """Get network metrics"""
        net = psutil.net_io_counters()
        return {
            'bytes_sent': net.bytes_sent,
            'bytes_recv': net.bytes_recv,
            'packets_sent': net.packets_sent,
            'packets_recv': net.packets_recv
        }
