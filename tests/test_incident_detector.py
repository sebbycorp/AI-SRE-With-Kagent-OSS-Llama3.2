"""
Unit tests for IncidentDetector
"""

import unittest
import sys
sys.path.insert(0, '.')

from src.incident_detector import IncidentDetector


class TestIncidentDetector(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'thresholds': {
                'cpu_usage': 90,
                'memory_usage': 85,
                'error_rate': 10
            }
        }
        self.detector = IncidentDetector(self.config)
    
    def test_initialization(self):
        """Test detector initialization"""
        self.assertEqual(self.detector.thresholds['cpu_usage'], 90)
        self.assertEqual(self.detector.thresholds['memory_usage'], 85)
        self.assertEqual(self.detector.thresholds['error_rate'], 10)
    
    def test_check_thresholds_exceeded(self):
        """Test threshold checking when exceeded"""
        metrics = {
            'cpu_usage': 95,
            'memory_usage': 80
        }
        result = self.detector.check_thresholds(metrics)
        self.assertTrue(result)
    
    def test_check_thresholds_not_exceeded(self):
        """Test threshold checking when not exceeded"""
        metrics = {
            'cpu_usage': 50,
            'memory_usage': 60
        }
        result = self.detector.check_thresholds(metrics)
        self.assertFalse(result)
    
    def test_check_thresholds_edge_case(self):
        """Test threshold checking at exact threshold"""
        metrics = {
            'cpu_usage': 90,
            'memory_usage': 85
        }
        result = self.detector.check_thresholds(metrics)
        self.assertTrue(result)
    
    def test_analyze_trends_no_data(self):
        """Test trend analysis with insufficient data"""
        result = self.detector.analyze_trends([])
        self.assertIsNone(result)
    
    def test_analyze_trends_with_change(self):
        """Test trend analysis with significant change"""
        historical = [
            {'cpu_usage': 50},
            {'cpu_usage': 75}
        ]
        result = self.detector.analyze_trends(historical)
        
        self.assertIsNotNone(result)
        self.assertIn('cpu_usage', result)
        self.assertIn('change', result['cpu_usage'])
        self.assertIn('percent_change', result['cpu_usage'])
        self.assertIn('direction', result['cpu_usage'])


if __name__ == '__main__':
    unittest.main()
