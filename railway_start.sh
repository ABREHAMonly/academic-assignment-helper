#!/bin/bash
# railway_start.sh
echo "🚂 Railway Deployment Starting..."

# Set environment
export PYTHONPATH=/app

# Debug info
echo "=== Environment Variables ==="
echo "PORT: $PORT"
echo "DATABASE_URL length: ${#DATABASE_URL}"
echo "JWT_SECRET_KEY length: ${#JWT_SECRET_KEY}"
echo "OPENAI_API_KEY length: ${#OPENAI_API_KEY}"
echo "============================="

# Check Python and dependencies
echo "=== System Check ==="
python --version
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|openai)"
echo "===================="

# Run database setup
cd /app
python setup_db.py

# Start the server
echo "🚀 Starting Uvicorn on port $PORT..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT