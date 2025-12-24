# Academic Assignment Helper & Plagiarism Detector (RAG-Powered)

A comprehensive backend system with n8n automation for academic assignment processing, RAG-based research suggestions, and AI-powered plagiarism detection.

## Features

- **JWT Authentication**: Secure API endpoints with student registration/login
- **File Upload**: Support for PDF, DOCX, and TXT files
- **RAG Pipeline**: Vector similarity search for academic sources
- **AI Analysis**: GPT-powered assignment analysis and suggestions
- **Plagiarism Detection**: Comparison against academic database
- **n8n Automation**: Workflow orchestration for processing pipeline
- **Dockerized**: Complete containerized setup with PostgreSQL + pgvector

## Architecture
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐
│ Client │────▶│ FastAPI │────▶│ n8n │────▶│ OpenAI │
│ (Web) │◀────│ Backend │◀────│ Workflow │◀────│ API │
└─────────┘ └──────────┘ └──────────┘ └─────────────┘
│ │ │
▼ ▼ ▼
┌──────────┐ ┌──────────┐ ┌─────────────┐
│ JWT │ │ Academic │ │ Embedding │
│ Auth │ │ Sources │ │ Generation │
└──────────┘ └──────────┘ └─────────────┘
│ │ │
▼ ▼ ▼
┌─────────────────────────────────────────────┐
│ PostgreSQL + pgvector │
│ (Vector Database & Storage) │
└─────────────────────────────────────────────┘

text

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- OpenAI API Key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd academic-assignment-helper
Configure environment variables:

bash
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
Initialize and start services:

bash
make init
Or manually:

bash
# Build and start services
docker-compose up -d --build

# Initialize database
docker-compose exec backend python scripts/init_db.py

# Seed with sample data
docker-compose exec backend python scripts/seed_academic_data.py
API Documentation
Once running, access the API documentation at:

Swagger UI: http://localhost:8000/api/docs

ReDoc: http://localhost:8000/api/redoc

Authentication Endpoints
text
POST /api/v1/auth/register    # Register new student
POST /api/v1/auth/login       # Login and get JWT token
Assignment Endpoints
text
POST /api/v1/assignments/upload    # Upload assignment file
GET  /api/v1/assignments           # List user assignments
Analysis Endpoints
text
GET /api/v1/analysis/{id}          # Get analysis results
GET /api/v1/analysis/{id}/sources  # Get RAG-based source suggestions
GET /api/v1/analysis/{id}/plagiarism  # Get detailed plagiarism report
n8n Workflow
Access n8n at http://localhost:5678

The workflow includes:

Webhook trigger from FastAPI

Document parsing and text extraction

Embedding generation using OpenAI

Vector similarity search in PostgreSQL

AI analysis with GPT-4

Plagiarism detection

Results storage and status update

Database Schema
Main Tables
students: User accounts with authentication

assignments: Assignment metadata and text

analysis_results: Analysis output and suggestions

academic_sources: Vector-embedded academic content

Vector Search
The system uses PostgreSQL with pgvector extension for:

Storing 1536-dimensional embeddings

Efficient similarity search using IVFFlat indexing

RAG-based context retrieval

Testing
Run tests with:

bash
make test
Or manually:

bash
docker-compose exec backend pytest /app/src/tests -v
Production Deployment
Environment Variables
Set these in production:

bash
JWT_SECRET_KEY=secure-random-string
OPENAI_API_KEY=your-production-key
POSTGRES_PASSWORD=strong-password
Security Considerations
Use HTTPS in production

Configure CORS appropriately

Set up firewall rules

Regular database backups

Monitor OpenAI API usage

Development
Running Locally
bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://student:secure_password@localhost/academic_helper
export OPENAI_API_KEY=your_key

# Run migrations
alembic upgrade head

# Start backend
uvicorn src.main:app --reload
Adding New Features
Create database migration:

bash
alembic revision --autogenerate -m "description"
Add API endpoints in src/api/v1/endpoints/

Add tests in src/tests/

Update n8n workflow if needed

Performance Optimization
Vector indexes for similarity search

Connection pooling for database

Redis caching for frequent queries

Async processing for long-running tasks

File size limits and validation

License
MIT

text

## 9. Setup Instructions

### Step-by-Step Setup:

1. **Clone and navigate to project:**
```bash
git clone <your-repo-url>
cd academic-assignment-helper
Set up environment:

bash
cp .env.example .env
# Edit .env with your OpenAI API key
Start all services:

bash
docker-compose up -d --build
Initialize database:

bash
docker-compose exec backend python scripts/init_db.py
Seed with academic data:

bash
docker-compose exec backend python scripts/seed_academic_data.py
Access services:

API: http://localhost:8000/api/docs

n8n: http://localhost:5678

PGAdmin: http://localhost:5050 (admin@academic.com / admin123)

Testing the API:
bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "student@example.com", "password": "password123", "full_name": "John Doe", "student_id": "STU001"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "student@example.com", "password": "password123"}'

# Use the token for upload
curl -X POST "http://localhost:8000/api/v1/assignments/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample_assignment.pdf"
Key Features Implemented:
Professional FastAPI Structure: Modular, well-organized codebase

Complete JWT Authentication: Secure endpoints with proper validation

RAG Pipeline: Full vector search with pgvector integration

n8n Automation: Complete workflow for assignment processing

Database Schema: Optimized with indexes and relationships

Error Handling: Comprehensive error handling and logging

Testing: Complete test suite with fixtures

Docker Orchestration: Multi-service setup with health checks

CI/CD Ready: Structure supports easy deployment

Production Configuration: Environment variables, security considerations