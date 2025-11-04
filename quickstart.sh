#!/bin/bash
# Quick Start Script for AI-SRE Agent

set -e

echo "🚀 AI-SRE Agent Quick Start"
echo "============================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "❌ Python 3 is required"; exit 1; }
echo "✅ Python found"
echo ""

# Check if Ollama is installed
echo "Checking for Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found"
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "✅ Ollama installed"
else
    echo "✅ Ollama found"
fi
echo ""

# Check if Llama 3.2 model is available
echo "Checking for Llama 3.2 model..."
if ! ollama list | grep -q "llama3.2"; then
    echo "⚠️  Llama 3.2 model not found"
    echo "Pulling Llama 3.2 model (this may take a few minutes)..."
    ollama pull llama3.2
    echo "✅ Llama 3.2 model installed"
else
    echo "✅ Llama 3.2 model found"
fi
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create config if it doesn't exist
if [ ! -f "config/config.yaml" ]; then
    echo "Creating configuration file..."
    cp config/config.example.yaml config/config.yaml
    echo "✅ Config created"
fi
echo ""

# Run system monitoring example
echo "Running system monitoring example..."
echo "===================================="
PYTHONPATH=. python examples/system_monitoring_example.py
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Customize config/config.yaml for your environment"
echo "  2. Run the agent: python -m src.main"
echo "  3. Try the CLI: python -m src.cli health-check"
echo "  4. Explore examples/ directory for more usage patterns"
echo ""
echo "Documentation: https://github.com/sebbycorp/AI-SRE-With-Kagent-OSS-Llama3.2"
