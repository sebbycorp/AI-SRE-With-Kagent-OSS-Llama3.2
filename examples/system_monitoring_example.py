"""
Example: System Monitoring
"""

from src.agent import AISDREAgent
import time

def main():
    # Initialize the agent
    agent = AISDREAgent(config_path='config/config.yaml')
    
    print("=== System Monitoring Example ===\n")
    
    # Get current system state
    state = agent.monitor.get_current_state()
    
    print(f"Timestamp: {state['timestamp']}\n")
    
    # Display CPU metrics
    if 'cpu' in state['metrics']:
        cpu = state['metrics']['cpu']
        print("📊 CPU Metrics:")
        print(f"  Usage: {cpu['usage_percent']:.1f}%")
        print(f"  Count: {cpu['count']} cores")
        if 'load_average' in cpu:
            print(f"  Load Average: {cpu['load_average']}")
        print()
    
    # Display memory metrics
    if 'memory' in state['metrics']:
        mem = state['metrics']['memory']
        print("💾 Memory Metrics:")
        print(f"  Usage: {mem['percent']:.1f}%")
        print(f"  Total: {mem['total'] / (1024**3):.2f} GB")
        print(f"  Used: {mem['used'] / (1024**3):.2f} GB")
        print(f"  Available: {mem['available'] / (1024**3):.2f} GB")
        print()
    
    # Display disk metrics
    if 'disk' in state['metrics']:
        disk = state['metrics']['disk']
        print("💿 Disk Metrics:")
        print(f"  Usage: {disk['percent']:.1f}%")
        print(f"  Total: {disk['total'] / (1024**3):.2f} GB")
        print(f"  Used: {disk['used'] / (1024**3):.2f} GB")
        print(f"  Free: {disk['free'] / (1024**3):.2f} GB")
        print()
    
    # Display network metrics
    if 'network' in state['metrics']:
        net = state['metrics']['network']
        print("🌐 Network Metrics:")
        print(f"  Bytes Sent: {net['bytes_sent'] / (1024**2):.2f} MB")
        print(f"  Bytes Received: {net['bytes_recv'] / (1024**2):.2f} MB")
        print(f"  Packets Sent: {net['packets_sent']}")
        print(f"  Packets Received: {net['packets_recv']}")
        print()
    
    # Check for any issues
    print("=== Health Check ===")
    metrics = {
        'cpu_usage': state['metrics']['cpu']['usage_percent'],
        'memory_usage': state['metrics']['memory']['percent'],
        'disk_usage': state['metrics']['disk']['percent']
    }
    
    incident = agent.detect_incident(metrics)
    if incident:
        print(f"⚠️  Issue detected: {incident.description}")
    else:
        print("✅ System is healthy")


if __name__ == '__main__':
    main()
