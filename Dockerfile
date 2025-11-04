FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create directory for logs
RUN mkdir -p /logs

# Expose metrics port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the agent
CMD ["python", "-m", "src.main", "--mode", "daemon"]
