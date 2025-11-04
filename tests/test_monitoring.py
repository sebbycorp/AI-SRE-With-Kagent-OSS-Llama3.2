"""
Unit tests for SystemMonitor
"""

import unittest
import sys
sys.path.insert(0, '.')

from src.monitoring import SystemMonitor


class TestSystemMonitor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'interval': 60,
            'metrics': ['cpu', 'memory', 'disk', 'network']
        }
        self.monitor = SystemMonitor(self.config)
    
    def test_initialization(self):
        """Test monitor initialization"""
        self.assertEqual(self.monitor.interval, 60)
        self.assertEqual(len(self.monitor.metrics), 4)
    
    def test_get_current_state(self):
        """Test getting current system state"""
        state = self.monitor.get_current_state()
        
        self.assertIn('timestamp', state)
        self.assertIn('metrics', state)
        
        metrics = state['metrics']
        self.assertIn('cpu', metrics)
        self.assertIn('memory', metrics)
        self.assertIn('disk', metrics)
        self.assertIn('network', metrics)
    
    def test_cpu_metrics(self):
        """Test CPU metrics structure"""
        state = self.monitor.get_current_state()
        cpu = state['metrics']['cpu']
        
        self.assertIn('usage_percent', cpu)
        self.assertIn('count', cpu)
        self.assertIsInstance(cpu['usage_percent'], (int, float))
        self.assertGreater(cpu['count'], 0)
    
    def test_memory_metrics(self):
        """Test memory metrics structure"""
        state = self.monitor.get_current_state()
        mem = state['metrics']['memory']
        
        self.assertIn('total', mem)
        self.assertIn('available', mem)
        self.assertIn('used', mem)
        self.assertIn('percent', mem)
        self.assertGreater(mem['total'], 0)
    
    def test_disk_metrics(self):
        """Test disk metrics structure"""
        state = self.monitor.get_current_state()
        disk = state['metrics']['disk']
        
        self.assertIn('total', disk)
        self.assertIn('used', disk)
        self.assertIn('free', disk)
        self.assertIn('percent', disk)
        self.assertGreater(disk['total'], 0)
    
    def test_network_metrics(self):
        """Test network metrics structure"""
        state = self.monitor.get_current_state()
        net = state['metrics']['network']
        
        self.assertIn('bytes_sent', net)
        self.assertIn('bytes_recv', net)
        self.assertIn('packets_sent', net)
        self.assertIn('packets_recv', net)


if __name__ == '__main__':
    unittest.main()
