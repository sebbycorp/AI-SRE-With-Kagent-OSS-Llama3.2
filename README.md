# AI-SRE with Kagent and OSS Llama 3.2

An intelligent Site Reliability Engineering (SRE) agent powered by Kagent framework and open-source Llama 3.2 model. This project provides automated monitoring, incident detection, log analysis, and intelligent remediation capabilities.

## 🚀 Features

- **Intelligent Log Analysis**: Automatically analyze system logs and identify anomalies
- **Incident Detection**: Real-time monitoring and intelligent incident detection
- **Automated Remediation**: AI-powered automated responses to common issues
- **System Monitoring**: Track system metrics and performance indicators
- **Natural Language Interface**: Interact with your infrastructure using natural language
- **Knowledge Base**: Built-in SRE knowledge and best practices

## 🏗️ Architecture

```
┌─────────────────┐
│   User/Alert    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Kagent Agent   │◄──────┐
│  (Orchestrator) │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  Llama 3.2      │       │
│  (via Ollama)   │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  SRE Tools      │───────┘
│  - Monitoring   │
│  - Log Analysis │
│  - Remediation  │
└─────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- Ollama (for running Llama 3.2 locally)

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sebbycorp/AI-SRE-With-Kagent-OSS-Llama3.2.git
cd AI-SRE-With-Kagent-OSS-Llama3.2
```

### 2. Install Ollama and Llama 3.2

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Llama 3.2 model
ollama pull llama3.2
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the agent

```bash
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml with your settings
```

## 🎯 Quick Start

### Running the AI-SRE Agent

```bash
python src/main.py
```

### Using the CLI Interface

```bash
# Analyze logs
python src/cli.py analyze-logs /var/log/syslog

# Check system health
python src/cli.py health-check

# Interactive mode
python src/cli.py interactive
```

### Docker Deployment

```bash
# Build the image
docker build -t ai-sre-agent .

# Run the container
docker run -d \
  -v /var/log:/logs:ro \
  -v ./config:/app/config \
  --name ai-sre-agent \
  ai-sre-agent
```

## 📖 Usage Examples

### Example 1: Analyzing System Logs

```python
from src.agent import AISDREAgent

agent = AISDREAgent()

# Analyze logs for anomalies
results = agent.analyze_logs("/var/log/syslog")
print(f"Found {len(results.anomalies)} anomalies")

for anomaly in results.anomalies:
    print(f"- {anomaly.description}")
    print(f"  Severity: {anomaly.severity}")
    print(f"  Recommendation: {anomaly.recommendation}")
```

### Example 2: Incident Detection and Response

```python
from src.agent import AISDREAgent

agent = AISDREAgent()

# Monitor system and detect incidents
incident = agent.detect_incident({
    'cpu_usage': 95,
    'memory_usage': 90,
    'error_rate': 15
})

if incident:
    print(f"Incident detected: {incident.description}")
    
    # Get automated remediation suggestions
    remediation = agent.suggest_remediation(incident)
    print(f"Suggested action: {remediation.action}")
    
    # Optionally auto-remediate
    if remediation.auto_remediate:
        agent.execute_remediation(remediation)
```

### Example 3: Natural Language Queries

```python
from src.agent import AISDREAgent

agent = AISDREAgent()

# Ask questions in natural language
response = agent.query("Why is the API response time increasing?")
print(response)

response = agent.query("What services are consuming the most memory?")
print(response)
```

## 🔍 SRE Capabilities

### Monitoring
- CPU, Memory, Disk, Network metrics
- Application performance monitoring
- Custom metric collection

### Log Analysis
- Pattern detection
- Anomaly identification
- Error classification
- Trend analysis

### Incident Management
- Automated incident detection
- Root cause analysis
- Remediation suggestions
- Incident documentation

### Automation
- Self-healing capabilities
- Auto-scaling recommendations
- Resource optimization
- Preventive maintenance

## 🛠️ Configuration

The agent can be configured through `config/config.yaml`:

```yaml
llama:
  model: llama3.2
  temperature: 0.7
  context_window: 4096

monitoring:
  interval: 60  # seconds
  metrics:
    - cpu
    - memory
    - disk
    - network

log_analysis:
  paths:
    - /var/log/syslog
    - /var/log/application.log
  patterns:
    - error
    - warning
    - critical

remediation:
  auto_remediate: false
  require_approval: true
  max_retries: 3
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=src tests/
```

## 📊 Monitoring and Metrics

The agent exposes Prometheus metrics on port 8000:

```bash
curl http://localhost:8000/metrics
```

Key metrics:
- `ai_sre_incidents_detected_total` - Total incidents detected
- `ai_sre_remediations_executed_total` - Total remediations executed
- `ai_sre_log_analysis_duration_seconds` - Log analysis duration
- `ai_sre_model_inference_duration_seconds` - Model inference time

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Kagent](https://github.com/kagent/kagent) - Agent orchestration framework
- [Ollama](https://ollama.ai/) - Local LLM inference
- [Llama 3.2](https://ai.meta.com/llama/) - Open source language model
- The SRE community for best practices and patterns

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sebbycorp/AI-SRE-With-Kagent-OSS-Llama3.2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sebbycorp/AI-SRE-With-Kagent-OSS-Llama3.2/discussions)

## 🗺️ Roadmap

- [x] Basic agent implementation
- [x] Log analysis capabilities
- [x] Incident detection
- [ ] Integration with popular monitoring tools (Prometheus, Grafana, Datadog)
- [ ] Slack/Teams integration for alerts
- [ ] Custom plugin system
- [ ] Multi-cloud support (AWS, Azure, GCP)
- [ ] Advanced ML-based anomaly detection
- [ ] Distributed tracing analysis
