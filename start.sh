#!/bin/bash
echo "🚀 Starting Academic Assignment Helper..."

# Wait for database to be ready (for container environments)
sleep 2

# Run database setup
python setup_db.py

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info