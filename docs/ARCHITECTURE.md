# AI-SRE Agent Architecture

## Overview

The AI-SRE Agent is designed as a modular, extensible system for intelligent Site Reliability Engineering operations. It leverages the Kagent framework for agent orchestration and Llama 3.2 for natural language understanding and decision-making.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI-SRE Agent Core                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   CLI/API    │  │  Main Agent  │  │   Metrics    │     │
│  │  Interface   │──│  Controller  │──│  Exporter    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                            │                                │
│         ┌──────────────────┼──────────────────┐            │
│         │                  │                  │            │
│         ▼                  ▼                  ▼            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   System     │  │     Log      │  │   Incident   │    │
│  │  Monitoring  │  │   Analysis   │  │   Detection  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                            ▼                                │
│                   ┌──────────────┐                         │
│                   │  LLM Client  │                         │
│                   │ (Llama 3.2)  │                         │
│                   └──────────────┘                         │
│                            │                                │
│                            ▼                                │
│                   ┌──────────────┐                         │
│                   │ Remediation  │                         │
│                   │    Engine    │                         │
│                   └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │   External Systems       │
              │  - Ollama (LLM Server)  │
              │  - System Resources     │
              │  - Log Files            │
              │  - Services             │
              └──────────────────────────┘
```

## Core Components

### 1. Agent Controller (`agent.py`)

The main orchestrator that coordinates all components:
- **Responsibilities:**
  - Initialize and manage all subsystems
  - Route requests to appropriate components
  - Aggregate results from multiple sources
  - Provide unified API for external interactions

- **Key Methods:**
  - `analyze_logs()`: Analyze log files for anomalies
  - `detect_incident()`: Detect incidents from metrics
  - `suggest_remediation()`: Generate remediation suggestions
  - `execute_remediation()`: Execute approved remediations
  - `query()`: Handle natural language queries

### 2. LLM Client (`llm_client.py`)

Interface to Llama 3.2 via Ollama:
- **Features:**
  - RESTful API communication with Ollama
  - Fallback responses when LLM unavailable
  - Configurable temperature and context window
  - Health checking

- **Configuration:**
  ```yaml
  llama:
    model: llama3.2
    temperature: 0.7
    context_window: 4096
    base_url: http://localhost:11434
  ```

### 3. System Monitor (`monitoring.py`)

Collects system metrics:
- **Metrics Collected:**
  - CPU usage and load average
  - Memory usage and availability
  - Disk usage and I/O
  - Network traffic and connections

- **Data Flow:**
  ```
  psutil → SystemMonitor → Structured Metrics → Agent
  ```

### 4. Log Analyzer (`log_analyzer.py`)

Analyzes log files:
- **Capabilities:**
  - Pattern-based log filtering
  - Error extraction and classification
  - Severity determination
  - Trend detection

- **Supported Formats:**
  - Syslog
  - Application logs
  - Custom formats (via configuration)

### 5. Incident Detector (`incident_detector.py`)

Detects system incidents:
- **Detection Methods:**
  - Threshold-based detection
  - Trend analysis
  - Anomaly detection (via LLM)

- **Threshold Configuration:**
  ```yaml
  incident_detection:
    thresholds:
      cpu_usage: 90
      memory_usage: 85
      disk_usage: 90
      error_rate: 10
  ```

### 6. Remediation Engine (`remediation.py`)

Executes remediation actions:
- **Safety Features:**
  - Command whitelisting
  - Manual approval option
  - Retry logic
  - Rollback capabilities (planned)

- **Whitelisted Commands:**
  - Service restart commands
  - Container management
  - Kubernetes operations
  - Safe system commands

## Data Flow

### Log Analysis Flow

```
1. User Request
   ↓
2. Agent.analyze_logs()
   ↓
3. LogAnalyzer.read_logs()
   ↓
4. LogAnalyzer.filter_by_pattern()
   ↓
5. LLMClient.generate() [Analysis Prompt]
   ↓
6. Agent._parse_anomalies()
   ↓
7. Return Results
```

### Incident Detection Flow

```
1. Metrics Collection (SystemMonitor)
   ↓
2. IncidentDetector.check_thresholds()
   ↓
3. [If Threshold Exceeded]
   ↓
4. LLMClient.generate() [Incident Analysis]
   ↓
5. Agent._parse_incident()
   ↓
6. RemediationEngine.suggest()
   ↓
7. [Optional] Execute Remediation
```

## Prompt Engineering

The agent uses carefully crafted prompts for different scenarios:

### Log Analysis Prompt
- Provides recent log entries
- Requests structured analysis
- Specifies output format (JSON)
- Asks for severity and recommendations

### Incident Detection Prompt
- Includes current metrics
- System context
- Historical data (when available)
- Root cause analysis request

### Remediation Prompt
- Incident details
- Affected systems
- Safety constraints
- Expected output format

## Extension Points

### Adding New Metrics

1. Extend `SystemMonitor`:
```python
def _get_custom_metrics(self) -> Dict:
    # Implement custom metric collection
    return {'metric_name': value}
```

2. Update configuration:
```yaml
monitoring:
  metrics:
    - cpu
    - memory
    - custom
```

### Adding New Log Parsers

1. Extend `LogAnalyzer`:
```python
def parse_custom_format(self, entry: str) -> Dict:
    # Parse custom log format
    return parsed_entry
```

### Custom Remediation Actions

1. Extend `RemediationEngine`:
```python
def execute_custom_action(self, action: CustomAction):
    # Implement custom remediation
    pass
```

2. Update whitelist in configuration

## Security Considerations

### Command Execution Safety

- All commands are validated against whitelist
- Dangerous commands are blocked
- Approval mechanism for sensitive operations
- Audit logging (planned)

### Data Privacy

- No data sent to external services (except configured Ollama)
- Sensitive information filtered from logs
- Credentials never logged

### Access Control

- Role-based access (planned)
- API authentication (planned)
- Audit trails (planned)

## Performance Considerations

### Scalability

- Async operations for I/O-bound tasks
- Batch processing for log analysis
- Caching for frequent queries
- Rate limiting for API calls

### Resource Management

- Configurable intervals for monitoring
- Memory-efficient log reading
- Connection pooling for Ollama
- Graceful degradation when LLM unavailable

## Future Architecture Enhancements

1. **Distributed Architecture**
   - Multiple agent instances
   - Shared knowledge base
   - Centralized coordination

2. **Machine Learning Integration**
   - Anomaly detection models
   - Predictive analytics
   - Custom model training

3. **Integration Framework**
   - Plugin system
   - External service connectors
   - Event streaming

4. **Advanced Features**
   - Multi-tenant support
   - Custom workflows
   - Advanced analytics
   - Real-time dashboards
