"""
Example: Incident Detection
"""

from src.agent import AISDREAgent

def main():
    # Initialize the agent
    agent = AISDREAgent(config_path='config/config.yaml')
    
    # Simulate high resource usage scenario
    print("Simulating high resource usage scenario...\n")
    
    test_metrics = {
        'cpu_usage': 95.5,
        'memory_usage': 92.0,
        'error_rate': 15
    }
    
    print(f"Current Metrics:")
    for metric, value in test_metrics.items():
        print(f"  {metric}: {value}")
    print()
    
    # Detect incident
    print("Checking for incidents...")
    incident = agent.detect_incident(test_metrics)
    
    if incident:
        print("\n🚨 INCIDENT DETECTED 🚨\n")
        print(f"Incident ID: {incident.id}")
        print(f"Timestamp: {incident.timestamp}")
        print(f"Severity: {incident.severity.upper()}")
        print(f"Description: {incident.description}")
        print(f"Affected Systems: {', '.join(incident.affected_systems)}")
        
        # Get remediation suggestions
        print("\n=== Remediation Suggestions ===")
        remediation = agent.suggest_remediation(incident)
        
        print(f"Action: {remediation.action}")
        print(f"Description: {remediation.description}")
        print(f"Auto-remediate: {remediation.auto_remediate}")
        print(f"Estimated Duration: {remediation.estimated_duration} minutes")
        
        if remediation.commands:
            print(f"\nCommands to execute:")
            for cmd in remediation.commands:
                print(f"  - {cmd}")
    else:
        print("✅ No incidents detected. System is healthy.")


if __name__ == '__main__':
    main()
