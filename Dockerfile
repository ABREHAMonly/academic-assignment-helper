# Dockerfile (debug version)
FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory
COPY backend/ .

# Debug: Show what was copied
RUN echo "🔍 Contents after COPY:" && \
    ls -la && \
    echo "🔍 backend directory:" && \
    ls -la backend/ 2>/dev/null || echo "No backend directory"

# Create uploads directory
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Debug: Check for start.sh
RUN if [ -f start.sh ]; then \
    echo "✅ Found start.sh, making executable" && \
    chmod +x start.sh; \
    else \
    echo "❌ start.sh not found, creating it" && \
    echo '#!/bin/bash' > start.sh && \
    echo 'echo "Starting server on port $PORT"' >> start.sh && \
    echo 'uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}' >> start.sh && \
    chmod +x start.sh; \
    fi

# Use the startup script
CMD ["./start.sh"]