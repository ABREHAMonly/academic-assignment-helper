FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (adjust if needed)
COPY backend/ /app/
COPY .env.example /app/.env.example

# Create uploads directory
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Render uses PORT environment variable
ENV PORT=8000

# Command for Render
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]