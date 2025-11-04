"""
AI-SRE Agent - Main Agent Implementation
Powered by Kagent and Llama 3.2
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import json

from .llm_client import LlamaClient
from .monitoring import SystemMonitor
from .log_analyzer import LogAnalyzer
from .incident_detector import IncidentDetector
from .remediation import RemediationEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Anomaly:
    """Represents a detected anomaly"""
    timestamp: datetime
    description: str
    severity: str
    recommendation: str
    source: str


@dataclass
class Incident:
    """Represents a detected incident"""
    id: str
    timestamp: datetime
    description: str
    severity: str
    affected_systems: List[str]
    metrics: Dict[str, Any]


@dataclass
class Remediation:
    """Represents a remediation action"""
    action: str
    description: str
    auto_remediate: bool
    commands: List[str]
    estimated_duration: int


class AISDREAgent:
    """
    AI-powered Site Reliability Engineering Agent
    
    This agent uses Llama 3.2 via Ollama and the Kagent framework
    to provide intelligent SRE capabilities including:
    - Log analysis
    - Incident detection
    - Automated remediation
    - System monitoring
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the AI-SRE Agent
        
        Args:
            config_path: Path to configuration file
        """
        logger.info("Initializing AI-SRE Agent...")
        
        self.config = self._load_config(config_path)
        self.llm_client = LlamaClient(self.config.get('llama', {}))
        self.monitor = SystemMonitor(self.config.get('monitoring', {}))
        self.log_analyzer = LogAnalyzer(self.config.get('log_analysis', {}))
        self.incident_detector = IncidentDetector(self.config.get('incident_detection', {}))
        self.remediation_engine = RemediationEngine(self.config.get('remediation', {}))
        
        logger.info("AI-SRE Agent initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file"""
        import yaml
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'llama': {
                'model': 'llama3.2',
                'temperature': 0.7,
                'context_window': 4096
            },
            'monitoring': {
                'interval': 60,
                'metrics': ['cpu', 'memory', 'disk', 'network']
            },
            'log_analysis': {
                'paths': ['/var/log/syslog'],
                'patterns': ['error', 'warning', 'critical']
            },
            'incident_detection': {
                'thresholds': {
                    'cpu_usage': 90,
                    'memory_usage': 85,
                    'error_rate': 10
                }
            },
            'remediation': {
                'auto_remediate': False,
                'require_approval': True,
                'max_retries': 3
            }
        }
    
    def analyze_logs(self, log_path: str) -> Dict[str, List[Anomaly]]:
        """
        Analyze logs for anomalies
        
        Args:
            log_path: Path to log file
            
        Returns:
            Dictionary with anomalies list
        """
        logger.info(f"Analyzing logs from: {log_path}")
        
        # Read and parse logs
        log_entries = self.log_analyzer.read_logs(log_path)
        
        # Use LLM to analyze patterns
        analysis_prompt = self._build_log_analysis_prompt(log_entries)
        llm_response = self.llm_client.generate(analysis_prompt)
        
        # Parse anomalies
        anomalies = self._parse_anomalies(llm_response, log_entries)
        
        logger.info(f"Found {len(anomalies)} anomalies")
        
        return {
            'anomalies': anomalies,
            'total_entries': len(log_entries),
            'analyzed_at': datetime.now().isoformat()
        }
    
    def detect_incident(self, metrics: Dict[str, float]) -> Optional[Incident]:
        """
        Detect incidents based on system metrics
        
        Args:
            metrics: Dictionary of system metrics
            
        Returns:
            Incident object if detected, None otherwise
        """
        logger.info(f"Analyzing metrics for incidents: {metrics}")
        
        # Check thresholds
        if self.incident_detector.check_thresholds(metrics):
            # Use LLM for intelligent incident analysis
            incident_prompt = self._build_incident_prompt(metrics)
            llm_response = self.llm_client.generate(incident_prompt)
            
            # Create incident object
            incident = self._parse_incident(llm_response, metrics)
            logger.warning(f"Incident detected: {incident.description}")
            
            return incident
        
        return None
    
    def suggest_remediation(self, incident: Incident) -> Remediation:
        """
        Suggest remediation actions for an incident
        
        Args:
            incident: Incident to remediate
            
        Returns:
            Remediation object with suggested actions
        """
        logger.info(f"Generating remediation for incident: {incident.id}")
        
        # Build context for LLM
        remediation_prompt = self._build_remediation_prompt(incident)
        llm_response = self.llm_client.generate(remediation_prompt)
        
        # Parse remediation actions
        remediation = self._parse_remediation(llm_response)
        
        logger.info(f"Remediation suggested: {remediation.action}")
        
        return remediation
    
    def execute_remediation(self, remediation: Remediation) -> bool:
        """
        Execute remediation actions
        
        Args:
            remediation: Remediation to execute
            
        Returns:
            True if successful, False otherwise
        """
        if not self.config.get('remediation', {}).get('auto_remediate', False):
            logger.warning("Auto-remediation is disabled")
            return False
        
        logger.info(f"Executing remediation: {remediation.action}")
        
        try:
            result = self.remediation_engine.execute(remediation)
            logger.info(f"Remediation executed successfully")
            return result
        except Exception as e:
            logger.error(f"Remediation failed: {e}")
            return False
    
    def query(self, question: str) -> str:
        """
        Query the agent using natural language
        
        Args:
            question: Natural language question
            
        Returns:
            Answer from the agent
        """
        logger.info(f"Processing query: {question}")
        
        # Get current system state
        system_state = self.monitor.get_current_state()
        
        # Build context-aware prompt
        query_prompt = self._build_query_prompt(question, system_state)
        response = self.llm_client.generate(query_prompt)
        
        return response
    
    def _build_log_analysis_prompt(self, log_entries: List[str]) -> str:
        """Build prompt for log analysis"""
        recent_logs = '\n'.join(log_entries[-100:])  # Last 100 entries
        
        return f"""You are an expert SRE analyzing system logs. 
Identify any anomalies, errors, or concerning patterns in these logs:

{recent_logs}

Provide:
1. List of anomalies found
2. Severity level (critical, high, medium, low)
3. Recommendations for each issue

Format your response as JSON with keys: anomalies, each containing: description, severity, recommendation"""
    
    def _build_incident_prompt(self, metrics: Dict[str, float]) -> str:
        """Build prompt for incident detection"""
        return f"""You are an expert SRE analyzing system metrics.
Current metrics:
{json.dumps(metrics, indent=2)}

Analyze these metrics and determine:
1. Is there an active incident?
2. What is the severity? (critical, high, medium, low)
3. What systems are affected?
4. What is the likely root cause?

Provide a detailed incident description."""
    
    def _build_remediation_prompt(self, incident: Incident) -> str:
        """Build prompt for remediation suggestions"""
        return f"""You are an expert SRE providing remediation guidance.
Incident Details:
- Description: {incident.description}
- Severity: {incident.severity}
- Affected Systems: {', '.join(incident.affected_systems)}
- Metrics: {json.dumps(incident.metrics, indent=2)}

Suggest specific remediation actions including:
1. Immediate actions to stabilize the system
2. Commands or steps to execute
3. Whether this can be safely automated
4. Estimated time to resolve

Format as JSON with keys: action, description, auto_remediate (bool), commands (list), estimated_duration (minutes)"""
    
    def _build_query_prompt(self, question: str, system_state: Dict) -> str:
        """Build prompt for natural language queries"""
        return f"""You are an AI-powered SRE assistant with access to system information.

Current System State:
{json.dumps(system_state, indent=2)}

User Question: {question}

Provide a helpful, accurate answer based on the current system state and your SRE expertise."""
    
    def _parse_anomalies(self, llm_response: str, log_entries: List[str]) -> List[Anomaly]:
        """Parse anomalies from LLM response"""
        try:
            # Try to parse as JSON
            data = json.loads(llm_response)
            anomalies = []
            
            for item in data.get('anomalies', []):
                anomalies.append(Anomaly(
                    timestamp=datetime.now(),
                    description=item.get('description', ''),
                    severity=item.get('severity', 'medium'),
                    recommendation=item.get('recommendation', ''),
                    source='log_analysis'
                ))
            
            return anomalies
        except json.JSONDecodeError:
            # Fallback: create single anomaly from response
            return [Anomaly(
                timestamp=datetime.now(),
                description=llm_response[:200],
                severity='medium',
                recommendation='Review logs manually',
                source='log_analysis'
            )]
    
    def _parse_incident(self, llm_response: str, metrics: Dict[str, float]) -> Incident:
        """Parse incident from LLM response"""
        import uuid
        
        return Incident(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            description=llm_response[:500],
            severity='high',
            affected_systems=['system'],
            metrics=metrics
        )
    
    def _parse_remediation(self, llm_response: str) -> Remediation:
        """Parse remediation from LLM response"""
        try:
            data = json.loads(llm_response)
            return Remediation(
                action=data.get('action', 'Manual investigation required'),
                description=data.get('description', llm_response[:200]),
                auto_remediate=data.get('auto_remediate', False),
                commands=data.get('commands', []),
                estimated_duration=data.get('estimated_duration', 30)
            )
        except json.JSONDecodeError:
            return Remediation(
                action='Manual investigation required',
                description=llm_response[:200],
                auto_remediate=False,
                commands=[],
                estimated_duration=30
            )
