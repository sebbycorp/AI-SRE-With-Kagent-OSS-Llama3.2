"""
CLI Interface for AI-SRE Agent
"""

import argparse
import logging
import sys
from .agent import AISDREAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def analyze_logs_command(args):
    """Analyze logs command"""
    agent = AISDREAgent(config_path=args.config)
    results = agent.analyze_logs(args.log_path)
    
    print(f"\n=== Log Analysis Results ===")
    print(f"Total entries analyzed: {results['total_entries']}")
    print(f"Anomalies found: {len(results['anomalies'])}\n")
    
    for i, anomaly in enumerate(results['anomalies'], 1):
        print(f"{i}. [{anomaly.severity.upper()}] {anomaly.description}")
        print(f"   Recommendation: {anomaly.recommendation}\n")


def health_check_command(args):
    """Health check command"""
    agent = AISDREAgent(config_path=args.config)
    state = agent.monitor.get_current_state()
    
    print("\n=== System Health Check ===")
    print(f"Timestamp: {state['timestamp']}\n")
    
    if 'cpu' in state['metrics']:
        cpu = state['metrics']['cpu']
        print(f"CPU Usage: {cpu['usage_percent']:.1f}%")
        print(f"CPU Count: {cpu['count']}")
    
    if 'memory' in state['metrics']:
        mem = state['metrics']['memory']
        print(f"Memory Usage: {mem['percent']:.1f}%")
        print(f"Memory Available: {mem['available'] / (1024**3):.2f} GB")
    
    if 'disk' in state['metrics']:
        disk = state['metrics']['disk']
        print(f"Disk Usage: {disk['percent']:.1f}%")
        print(f"Disk Free: {disk['free'] / (1024**3):.2f} GB")


def interactive_command(args):
    """Interactive mode command"""
    agent = AISDREAgent(config_path=args.config)
    
    print("\n=== AI-SRE Interactive Mode ===")
    print("Ask questions about your system or type 'exit' to quit\n")
    
    while True:
        try:
            question = input("You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            response = agent.query(question)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI-SRE Agent CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze logs command
    analyze_parser = subparsers.add_parser(
        'analyze-logs',
        help='Analyze log files for anomalies'
    )
    analyze_parser.add_argument('log_path', help='Path to log file')
    analyze_parser.set_defaults(func=analyze_logs_command)
    
    # Health check command
    health_parser = subparsers.add_parser(
        'health-check',
        help='Check system health'
    )
    health_parser.set_defaults(func=health_check_command)
    
    # Interactive command
    interactive_parser = subparsers.add_parser(
        'interactive',
        help='Interactive mode'
    )
    interactive_parser.set_defaults(func=interactive_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        args.func(args)
        return 0
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
