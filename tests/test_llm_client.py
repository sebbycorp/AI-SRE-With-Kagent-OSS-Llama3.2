"""
Unit tests for LlamaClient
"""

import unittest
import sys
sys.path.insert(0, '.')

from src.llm_client import LlamaClient


class TestLlamaClient(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'model': 'llama3.2',
            'temperature': 0.7,
            'context_window': 4096,
            'base_url': 'http://localhost:11434'
        }
        self.client = LlamaClient(self.config)
    
    def test_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.model, 'llama3.2')
        self.assertEqual(self.client.temperature, 0.7)
        self.assertEqual(self.client.context_window, 4096)
        self.assertEqual(self.client.base_url, 'http://localhost:11434')
    
    def test_fallback_response_logs(self):
        """Test fallback response for log analysis"""
        prompt = "Analyze these logs for anomalies"
        response = self.client._fallback_response(prompt)
        
        self.assertIsInstance(response, str)
        self.assertIn('anomalies', response.lower())
    
    def test_fallback_response_incident(self):
        """Test fallback response for incident detection"""
        prompt = "Analyze this incident"
        response = self.client._fallback_response(prompt)
        
        self.assertIsInstance(response, str)
        self.assertIn('incident', response.lower())
    
    def test_fallback_response_remediation(self):
        """Test fallback response for remediation"""
        prompt = "Suggest remediation"
        response = self.client._fallback_response(prompt)
        
        self.assertIsInstance(response, str)
        self.assertIn('remediation', response.lower())
    
    def test_fallback_response_generic(self):
        """Test fallback response for generic query"""
        prompt = "What is the meaning of life?"
        response = self.client._fallback_response(prompt)
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_check_health(self):
        """Test health check (will fail without Ollama running)"""
        # This test will return False if Ollama is not running
        # which is expected in most test environments
        result = self.client.check_health()
        self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()
