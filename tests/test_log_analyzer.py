"""
Unit tests for LogAnalyzer
"""

import unittest
import tempfile
import os
import sys
sys.path.insert(0, '.')

from src.log_analyzer import LogAnalyzer


class TestLogAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'paths': ['/var/log/syslog'],
            'patterns': ['error', 'warning', 'critical']
        }
        self.analyzer = LogAnalyzer(self.config)
        
        # Create temporary log file
        self.temp_log = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_log.write("2025-11-04 10:00:00 INFO Application started\n")
        self.temp_log.write("2025-11-04 10:01:00 ERROR Database connection failed\n")
        self.temp_log.write("2025-11-04 10:02:00 WARNING High memory usage\n")
        self.temp_log.write("2025-11-04 10:03:00 CRITICAL Service unavailable\n")
        self.temp_log.write("2025-11-04 10:04:00 INFO Processing complete\n")
        self.temp_log.close()
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.unlink(self.temp_log.name)
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertEqual(len(self.analyzer.patterns), 3)
        self.assertIn('error', self.analyzer.patterns)
    
    def test_read_logs(self):
        """Test reading log entries"""
        entries = self.analyzer.read_logs(self.temp_log.name)
        self.assertEqual(len(entries), 5)
    
    def test_read_logs_nonexistent(self):
        """Test reading from nonexistent file"""
        entries = self.analyzer.read_logs('/nonexistent/file.log')
        self.assertEqual(len(entries), 0)
    
    def test_filter_by_pattern(self):
        """Test filtering logs by pattern"""
        entries = self.analyzer.read_logs(self.temp_log.name)
        filtered = self.analyzer.filter_by_pattern(entries)
        
        # Should find ERROR, WARNING, and CRITICAL entries
        self.assertGreaterEqual(len(filtered), 3)
    
    def test_extract_errors(self):
        """Test extracting error messages"""
        entries = self.analyzer.read_logs(self.temp_log.name)
        errors = self.analyzer.extract_errors(entries)
        
        # Should find ERROR entry
        self.assertGreater(len(errors), 0)
        
        for error in errors:
            self.assertIn('timestamp', error)
            self.assertIn('message', error)
            self.assertIn('severity', error)
    
    def test_determine_severity(self):
        """Test severity determination"""
        critical_entry = "2025-11-04 CRITICAL system failure"
        self.assertEqual(self.analyzer._determine_severity(critical_entry), 'critical')
        
        error_entry = "2025-11-04 ERROR database error"
        self.assertEqual(self.analyzer._determine_severity(error_entry), 'high')
        
        warning_entry = "2025-11-04 WARNING high load"
        self.assertEqual(self.analyzer._determine_severity(warning_entry), 'medium')


if __name__ == '__main__':
    unittest.main()
