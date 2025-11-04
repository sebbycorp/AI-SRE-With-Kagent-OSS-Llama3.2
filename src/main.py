"""
Main entry point for AI-SRE Agent
"""

import logging
import argparse
from .agent import AISDREAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI-SRE Agent')
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--mode',
        choices=['daemon', 'once'],
        default='once',
        help='Run mode: daemon for continuous monitoring, once for single run'
    )
    
    args = parser.parse_args()
    
    logger.info("Starting AI-SRE Agent...")
    
    try:
        agent = AISDREAgent(config_path=args.config)
        
        if args.mode == 'once':
            # Single run - get system state
            state = agent.monitor.get_current_state()
            logger.info(f"Current system state: {state}")
            
            # Check for incidents
            metrics = state['metrics']
            if 'cpu' in metrics:
                test_metrics = {
                    'cpu_usage': metrics['cpu']['usage_percent'],
                    'memory_usage': metrics['memory']['percent']
                }
                
                incident = agent.detect_incident(test_metrics)
                if incident:
                    logger.warning(f"Incident detected: {incident.description}")
                    
                    # Suggest remediation
                    remediation = agent.suggest_remediation(incident)
                    logger.info(f"Suggested remediation: {remediation.action}")
                else:
                    logger.info("No incidents detected")
        
        elif args.mode == 'daemon':
            logger.info("Daemon mode not yet implemented")
            # TODO: Implement continuous monitoring loop
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
