"""
LLM Client for Llama 3.2 via Ollama
"""

import logging
from typing import Dict, Optional, List
import requests
import json

logger = logging.getLogger(__name__)


class LlamaClient:
    """Client for interacting with Llama 3.2 via Ollama"""
    
    def __init__(self, config: Dict):
        """
        Initialize Llama client
        
        Args:
            config: Configuration dictionary
        """
        self.model = config.get('model', 'llama3.2')
        self.temperature = config.get('temperature', 0.7)
        self.context_window = config.get('context_window', 4096)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        
        logger.info(f"Initialized Llama client with model: {self.model}")
    
    def generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Generate text using Llama 3.2
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': self.temperature,
                        'num_predict': max_tokens or 512
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return self._fallback_response(prompt)
                
        except requests.exceptions.ConnectionError:
            logger.warning("Cannot connect to Ollama. Using fallback responses.")
            return self._fallback_response(prompt)
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Provide fallback response when LLM is unavailable"""
        if 'anomalies' in prompt.lower() or 'logs' in prompt.lower():
            return json.dumps({
                'anomalies': [{
                    'description': 'Unable to analyze logs - LLM service unavailable',
                    'severity': 'medium',
                    'recommendation': 'Check Ollama service and ensure Llama 3.2 model is installed'
                }]
            })
        elif 'incident' in prompt.lower():
            return "Potential incident detected based on metrics thresholds. Manual review recommended."
        elif 'remediation' in prompt.lower():
            return json.dumps({
                'action': 'Manual investigation required',
                'description': 'LLM service unavailable for automated remediation suggestions',
                'auto_remediate': False,
                'commands': [],
                'estimated_duration': 30
            })
        else:
            return "I'm unable to process your request at the moment. Please ensure Ollama is running and the Llama 3.2 model is installed."
    
    def check_health(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
