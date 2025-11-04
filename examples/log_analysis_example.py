"""
Example: Basic Log Analysis
"""

from src.agent import AISDREAgent

def main():
    # Initialize the agent
    agent = AISDREAgent(config_path='config/config.yaml')
    
    # Create a sample log file for demonstration
    sample_log = "/tmp/sample.log"
    with open(sample_log, 'w') as f:
        f.write("2025-11-04 10:00:00 INFO Application started\n")
        f.write("2025-11-04 10:01:00 INFO Processing request\n")
        f.write("2025-11-04 10:02:00 ERROR Database connection failed\n")
        f.write("2025-11-04 10:03:00 WARNING High memory usage detected\n")
        f.write("2025-11-04 10:04:00 CRITICAL Service unavailable\n")
        f.write("2025-11-04 10:05:00 ERROR Timeout while connecting to API\n")
    
    # Analyze the logs
    print("Analyzing logs...")
    results = agent.analyze_logs(sample_log)
    
    print(f"\n=== Analysis Results ===")
    print(f"Total entries analyzed: {results['total_entries']}")
    print(f"Anomalies found: {len(results['anomalies'])}")
    print(f"Analyzed at: {results['analyzed_at']}\n")
    
    # Display anomalies
    for i, anomaly in enumerate(results['anomalies'], 1):
        print(f"{i}. [{anomaly.severity.upper()}] {anomaly.description}")
        print(f"   Source: {anomaly.source}")
        print(f"   Recommendation: {anomaly.recommendation}\n")


if __name__ == '__main__':
    main()
