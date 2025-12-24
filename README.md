# Academic Assignment Helper & Plagiarism Detector

A RAG-powered system for academic assignment analysis with plagiarism detection.

## Features
- JWT-based authentication
- Assignment file upload (PDF, DOCX, TXT)
- RAG-based source suggestions
- AI-powered plagiarism detection
- PostgreSQL with pgvector for embeddings
- n8n workflow automation
- Docker support

## Project Structure
academic-assignment-helper/
├── backend/ # FastAPI backend
├── workflows/ # n8n workflows
├── data/ # Sample data
├── docker-compose.yml
├── .env.example
└── README.md


## Quick Start

### Option 1: Docker (Production)
1. Clone the repository
2. Copy `.env.example` to `.env` and configure variables
3. Run: `docker-compose up -d`
4. Access:
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - n8n: http://localhost:5678

### Option 2: Local Development
1. Install Python 3.11+ and PostgreSQL
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Set up environment variables in `.env`
6. Initialize database: `python backend/setup_db.py`
7. Run backend: `python backend/main.py`
8. Run n8n separately if needed

## Environment Variables
See `.env.example` for all required variables:
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for JWT tokens
- `OPENAI_API_KEY`: OpenAI API key
- `USE_VECTOR`: Enable pgvector (true/false)

## API Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT
- `POST /upload` - Upload assignment
- `GET /analysis/{id}` - Get analysis results
- `GET /sources` - Search academic sources
- `GET /health` - Health check

## Testing
Run local tests: `python test_local.py`
Run API tests: `python test_api.py`

## Development
- Local setup: `python backend/local_setup.py`
- Database setup: `python backend/setup_db.py`
- Use `.env` for configuration

## Production Deployment
1. Use Docker Compose for production
2. Configure proper SSL/TLS
3. Use secure passwords for JWT and database
4. Set up monitoring and logging
5. Configure backup for database

## License
MIT

setup.sh (Setup script)

#!/bin/bash

echo "🔧 Setting up Academic Assignment Helper..."

# Check Python version
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration"
fi

# Create necessary directories
mkdir -p uploads workflows data

echo "✅ Setup complete!"
echo "📋 Next steps:"
echo "  1. Update .env file with your configuration"
echo "  2. Run: python backend/setup_db.py"
echo "  3. Run: python backend/main.py"
echo "  4. Access: http://localhost:8000/docs"


.env.example

# Database Configuration
# For Docker: postgresql://student:secure_password@postgres:5432/academic_helper
# For Local: postgresql://username:password@localhost:5432/academic_helper
DATABASE_URL=postgresql://student:secure_password@localhost:5432/academic_helper

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# OpenAI API
OPENAI_API_KEY=your-openai-api-key-here

# Vector Database (pgvector)
USE_VECTOR=false

# n8n Configuration
N8N_WEBHOOK_URL=http://localhost:5678/webhook/assignment
N8N_ACCESS_TOKEN=your-jwt-secret

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000

# PostgreSQL (for Docker)
POSTGRES_DB=academic_helper
POSTGRES_USER=student
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

2. DEPLOYMENT INSTRUCTIONS
Option A: Docker Deployment (Production)

# 1. Clone and setup
git clone <repository-url>
cd academic-assignment-helper

# 2. Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key and other settings

# 3. Start all services
docker-compose up -d

# 4. Check services
docker-compose ps

# 5. View logs
docker-compose logs -f backend


Option B: Local Development (Without Docker)

# 1. Setup (one-time)
chmod +x setup.sh
./setup.sh

# 2. Configure .env file
nano .env  # Update with your Neon DB connection string

# 3. Initialize database
python backend/setup_db.py

# 4. Start backend
python backend/main.py

# 5. Start n8n (optional)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# 6. Import workflow to n8n
# Upload workflows/assignment_analysis_workflow.json to n8n UI


3. KEY FEATURES
Dual-Mode Architecture
Production Mode (Docker): Uses pgvector, full n8n automation

Development Mode (Local): Works with Neon DB, simplified RAG

Security Implementation
JWT authentication with bcrypt password hashing

Protected API endpoints

Secure file handling

Environment-based configuration

Database Support
PostgreSQL with pgvector for production

PostgreSQL without vector for development (Neon DB compatible)

SQLAlchemy ORM with migrations

File Processing
PDF, DOCX, TXT file support

Automatic text extraction

Secure file storage and cleanup

RAG Integration
Vector embeddings with pgvector

Fallback text search for non-vector databases

OpenAI embeddings and analysis

4. TESTING
bash
# Test local API
python test_local.py

# Test authentication and endpoints
python test_api.py

# Manual testing with curl
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@student.edu","password":"testpassword123","full_name":"Test Student","student_id":"S001"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@student.edu","password":"testpassword123"}'
5. PRODUCTION NOTES
Security: Change all default passwords in production

SSL/TLS: Add HTTPS termination (nginx or similar)

Monitoring: Add logging and monitoring (Prometheus/Grafana)

Backup: Regular database backups

Scaling: Consider adding Redis for caching

