#!/bin/bash
# backend/start.sh

echo "🔧 Starting Academic Assignment Helper..."
echo "📊 PORT: $PORT"
echo "📊 PYTHONPATH: $PYTHONPATH"

# Set default port if not provided
PORT=${PORT:-8000}

# Check if we're in the right directory
echo "📁 Current directory: $(pwd)"
echo "📁 Files:"
ls -la

# Run database setup if needed
echo "🗄️  Checking database..."
python setup_db.py

# Start the server
echo "🚀 Starting server on port $PORT..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT