"""
Log Analysis Module
"""

import logging
import re
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class LogAnalyzer:
    """Analyze system logs for anomalies"""
    
    def __init__(self, config: Dict):
        """
        Initialize log analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.paths = config.get('paths', ['/var/log/syslog'])
        self.patterns = config.get('patterns', ['error', 'warning', 'critical'])
        logger.info("Initialized Log Analyzer")
    
    def read_logs(self, log_path: str, lines: int = 1000) -> List[str]:
        """
        Read log entries from file
        
        Args:
            log_path: Path to log file
            lines: Number of recent lines to read
            
        Returns:
            List of log entries
        """
        try:
            with open(log_path, 'r') as f:
                # Read last N lines efficiently
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except FileNotFoundError:
            logger.warning(f"Log file not found: {log_path}")
            return []
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
            return []
    
    def filter_by_pattern(self, log_entries: List[str]) -> List[str]:
        """
        Filter log entries by configured patterns
        
        Args:
            log_entries: List of log entries
            
        Returns:
            Filtered log entries
        """
        filtered = []
        
        for entry in log_entries:
            for pattern in self.patterns:
                if re.search(pattern, entry, re.IGNORECASE):
                    filtered.append(entry)
                    break
        
        return filtered
    
    def extract_errors(self, log_entries: List[str]) -> List[Dict]:
        """
        Extract error messages from logs
        
        Args:
            log_entries: List of log entries
            
        Returns:
            List of error dictionaries
        """
        errors = []
        error_pattern = re.compile(r'(error|exception|failed|failure)', re.IGNORECASE)
        
        for entry in log_entries:
            if error_pattern.search(entry):
                errors.append({
                    'timestamp': datetime.now().isoformat(),
                    'message': entry.strip(),
                    'severity': self._determine_severity(entry)
                })
        
        return errors
    
    def _determine_severity(self, log_entry: str) -> str:
        """Determine severity from log entry"""
        entry_lower = log_entry.lower()
        
        if any(word in entry_lower for word in ['critical', 'fatal', 'emergency']):
            return 'critical'
        elif any(word in entry_lower for word in ['error', 'exception']):
            return 'high'
        elif 'warning' in entry_lower:
            return 'medium'
        else:
            return 'low'
