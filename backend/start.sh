#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting Academic Assignment Helper..."
echo "📦 Python version: $(python --version)"
echo "🌐 Host: 0.0.0.0"
echo "🔢 Port: ${PORT}"
echo "🗄️ Database configured: $(if [ -n "$DATABASE_URL" ]; then echo "Yes"; else echo "No"; fi)"

# Check for required environment variables
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable is not set"
    exit 1
fi

if [ -z "$JWT_SECRET_KEY" ]; then
    echo "⚠️ WARNING: JWT_SECRET_KEY environment variable is not set"
    echo "⚠️ Using default secret key - NOT RECOMMENDED FOR PRODUCTION"
fi

# Initialize database if needed
echo "🔧 Setting up database..."
python -c "
import sys
import os
sys.path.insert(0, '/app')

from sqlalchemy import create_engine, text
from models import Base

try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    Base.metadata.create_all(bind=engine)
    print('✅ Database tables verified')
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Database connection successful')
except Exception as e:
    print(f'⚠️ Database setup warning: {e}')
    # Don't exit - continue anyway
"

echo "🚀 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --log-level info