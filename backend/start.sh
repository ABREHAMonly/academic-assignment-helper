#!/bin/bash
# backend/start.sh
echo "🔧 Starting server..."
echo "PORT: ${PORT:-8000}"

# Run database setup
python setup_db.py

# Start the server
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}#!/bin/bash
# backend/start.sh
echo "🔧 Starting server..."
echo "PORT: ${PORT:-8000}"

# Run database setup
python setup_db.py

# Start the server
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}