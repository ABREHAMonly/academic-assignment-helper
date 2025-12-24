# Dockerfile (at project root)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory
COPY backend/ .

# Create uploads directory
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application with proper PORT handling
CMD ["sh", "-c", "python setup_db.py && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]