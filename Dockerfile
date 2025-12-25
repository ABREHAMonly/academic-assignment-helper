# Dockerfile (at project root)
FROM python:3.11-slim

# Set working directory to /app/backend
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from backend directory
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory to /app/backend
COPY backend/ .

# Create uploads directory in /app/backend
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (Railway will override)
EXPOSE 8000

# Use Railway's PORT environment variable directly
CMD uvicorn main:app --host 0.0.0.0 --port $PORT