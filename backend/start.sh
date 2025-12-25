# Tested Dockerfile for Railway
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system packages
RUN apt-get update && \
    apt-get install -y gcc g++ libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ /app/

# Create non-root user (optional but recommended)
RUN useradd -m -u 1000 appuser && \
    mkdir -p uploads && \
    chown -R appuser:appuser /app
USER appuser

# Simple command that works
CMD uvicorn main:app --host 0.0.0.0 --port $PORT