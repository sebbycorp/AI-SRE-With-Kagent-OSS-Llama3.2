"""
Remediation Engine Module
"""

import logging
import subprocess
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class RemediationEngine:
    """Execute remediation actions"""
    
    def __init__(self, config: Dict):
        """
        Initialize remediation engine
        
        Args:
            config: Configuration dictionary
        """
        self.auto_remediate = config.get('auto_remediate', False)
        self.require_approval = config.get('require_approval', True)
        self.max_retries = config.get('max_retries', 3)
        logger.info("Initialized Remediation Engine")
    
    def execute(self, remediation) -> bool:
        """
        Execute remediation actions
        
        Args:
            remediation: Remediation object with actions
            
        Returns:
            True if successful, False otherwise
        """
        if not self.auto_remediate:
            logger.warning("Auto-remediation disabled. Manual action required.")
            return False
        
        if not remediation.auto_remediate:
            logger.warning("This remediation is not marked for auto-execution")
            return False
        
        logger.info(f"Executing remediation: {remediation.action}")
        
        success = True
        for command in remediation.commands:
            if not self._execute_command(command):
                success = False
                break
        
        return success
    
    def _execute_command(self, command: str) -> bool:
        """
        Execute a single command
        
        Args:
            command: Command to execute
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Executing command: {command}")
            
            # Safety check - only allow whitelisted commands
            if not self._is_safe_command(command):
                logger.error(f"Command not in whitelist: {command}")
                return False
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Command successful: {command}")
                return True
            else:
                logger.error(f"Command failed: {command}, Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return False
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return False
    
    def _is_safe_command(self, command: str) -> bool:
        """
        Check if command is safe to execute
        
        Args:
            command: Command to check
            
        Returns:
            True if safe, False otherwise
        """
        # Whitelist of safe commands for SRE operations
        safe_commands = [
            'systemctl restart',
            'systemctl stop',
            'systemctl start',
            'docker restart',
            'kubectl rollout restart',
            'service restart',
            'pkill -HUP',
        ]
        
        # Check if command starts with any whitelisted pattern
        return any(command.strip().startswith(safe_cmd) for safe_cmd in safe_commands)
    
    def dry_run(self, remediation) -> Dict:
        """
        Simulate remediation without executing
        
        Args:
            remediation: Remediation to simulate
            
        Returns:
            Simulation results
        """
        return {
            'action': remediation.action,
            'commands': remediation.commands,
            'estimated_duration': remediation.estimated_duration,
            'would_execute': self.auto_remediate and remediation.auto_remediate,
            'safe_commands': [
                self._is_safe_command(cmd) for cmd in remediation.commands
            ]
        }
