#!/bin/bash
echo "🚀 Starting Academic Assignment Helper..."
echo "📦 Python version: $(python --version)"
echo "🌐 Host: 0.0.0.0"
echo "🔢 Port: ${PORT}"
echo "🗄️ Database: ${DATABASE_URL:0:50}..."

# Initialize database
python -c "
from sqlalchemy import create_engine, text
from models import Base
import os

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(bind=engine)
print('✅ Database tables verified')
"

# Start the server
exec uvicorn main:app --host 0.0.0.0 --port ${PORT}