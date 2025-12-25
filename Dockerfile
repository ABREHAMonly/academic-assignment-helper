# Dockerfile (final version)
FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory
COPY backend/ .

# Create uploads directory
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Make startup script executable
RUN chmod +x start.sh

# Use the startup script
CMD ["./start.sh"]