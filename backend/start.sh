# Alternative Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python packages
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ /app/

# Create uploads directory
RUN mkdir -p uploads

# Set Python path
ENV PYTHONPATH=/app

# Run setup then start server
CMD python setup_db.py && exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}