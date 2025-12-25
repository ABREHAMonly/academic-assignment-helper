# Academic Assignment Helper & Plagiarism Detector

<div align="center">

**RAG-Powered • AI-Enhanced • Production-Ready**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

*A production-ready academic analysis platform with intelligent plagiarism detection and research assistance*

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Deployment](#-deployment) • [Architecture](#-architecture)

</div>

## 🚀 Overview

**Academic Assignment Helper** is a comprehensive, RAG-powered platform that transforms how educational institutions handle student assignments. The system provides automated analysis, plagiarism detection, and personalized research suggestions using state-of-the-art AI technologies.

### Why This Platform?

| Problem | Our Solution |
|---------|--------------|
| Manual plagiarism checking is time-consuming | **AI-powered detection** with similarity scoring |
| Students struggle to find relevant sources | **RAG-based recommendations** from academic databases |
| No standardized assignment analysis | **Structured feedback** with citation recommendations |
| Security concerns with student data | **JWT authentication** with secure file handling |

## ✨ Features

### 🔒 **Security & Authentication**
- **JWT-based authentication** with bcrypt password hashing
- **Role-based access control** for students and instructors
- **Secure file uploads** with automatic cleanup
- **Environment-segregated configuration** for dev/production

### 📚 **Academic Analysis**
- **Multi-format support**: PDF, DOCX, TXT file processing
- **Intelligent text extraction** using PyPDF2 & python-docx
- **Academic level assessment** (Undergraduate/Graduate/PhD)
- **Research question identification** and topic extraction

### 🔍 **Plagiarism Detection**
- **AI-powered similarity analysis** using GPT models
- **Source-to-text comparison** with confidence scoring
- **Flagged section highlighting** for review
- **Academic database cross-referencing**

### 🤖 **AI-Powered RAG System**
- **Vector-based similarity search** with pgvector (production)
- **Text-based fallback search** for Neon DB (development)
- **Relevant source suggestions** from academic databases
- **Citation format recommendations** (APA, MLA, Chicago)

### 🔄 **Workflow Automation**
- **n8n workflow orchestration** for complex analysis pipelines
- **Automated database storage** of analysis results
- **Optional notifications** to instructors via Slack/Email
- **Batch processing capabilities**

## 📋 System Architecture

```mermaid
graph TB
    A[Student Upload] --> B[FastAPI Backend]
    B --> C[JWT Authentication]
    C --> D[File Processing]
    D --> E[Text Extraction]
    E --> F[RAG Query]
    F --> G[Vector/Text Search]
    G --> H[OpenAI Analysis]
    H --> I[Plagiarism Detection]
    I --> J[Result Structuring]
    J --> K[PostgreSQL Storage]
    J --> L[Student Response]
    
    M[n8n Workflow] --> N[Webhook Trigger]
    N --> O[Multi-step Analysis]
    O --> P[Database Integration]
    
    subgraph "Data Layer"
        Q[(PostgreSQL)]
        R[(pgvector)]
    end
    
    subgraph "AI Layer"
        S[OpenAI GPT]
        T[Embeddings]
    end
    
    F --> R
    G --> Q
    H --> S
```

## 🏗️ Project Structure

```
academic-assignment-helper/
├── backend/                    # FastAPI Application
│   ├── main.py               # Application entry point
│   ├── auth.py               # JWT authentication
│   ├── models.py             # SQLAlchemy models
│   ├── rag_service.py        # RAG implementation
│   ├── requirements.txt      # Python dependencies
│   ├── start.sh             # Production startup script
│   └── setup_db.py          # Database initialization
├── workflows/
│   └── assignment_analysis_workflow.json  # n8n automation
├── data/
│   └── sample_academic_sources.json       # Test data
├── uploads/                  # Temporary file storage
├── .env.example             # Environment template
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Local development
├── render.yaml              # Production deployment
├── README.md               # This document
└── test_api.py             # API test suite
```

## ⚡ Quick Start

### 🐳 **Docker Development (Recommended)**

```bash
# 1. Clone and setup
git clone https://github.com/ABREHAMonly/academic-assignment-helper.git
cd academic-assignment-helper

# 2. Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# 3. Start all services
docker-compose up -d

# 4. Access services
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# n8n Interface: http://localhost:5678
```

### 💻 **Local Development (Without Docker)**

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure environment
cp .env.example .env
# Update DATABASE_URL to your PostgreSQL/Neon DB connection

# 4. Initialize database
python backend/setup_db.py

# 5. Start the server
python backend/main.py

# 6. Test the API
python test_api.py
```

## 🌐 API Documentation

### Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://academic-assignment-helper-8t2n.onrender.com`

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `POST` | `/auth/register` | Register new student | ❌ |
| `POST` | `/auth/login` | Login and get JWT token | ❌ |

**Registration Example:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "secure_password",
    "full_name": "John Doe",
    "student_id": "S12345"
  }'
```

**Login Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@university.edu",
    "password": "secure_password"
  }'
```

### Assignment Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `POST` | `/upload` | Upload assignment file | ✅ |
| `GET` | `/analysis/{id}` | Get analysis results | ✅ |
| `GET` | `/sources` | Search academic sources | ✅ |
| `GET` | `/health` | System health check | ❌ |

**File Upload Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@assignment.pdf"
```

**Response Structure:**
```json
{
  "job_id": "12345",
  "message": "Assignment uploaded and analyzed successfully",
  "status": "completed",
  "assignment_id": 42,
  "suggested_sources": [...],
  "plagiarism_score": 15.5,
  "research_suggestions": "Consider adding more recent references...",
  "citation_recommendations": "APA 7th Edition"
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database Configuration
DATABASE_URL=postgresql+psycopg2://user:password@host/dbname

# JWT Authentication (generate with: openssl rand -hex 32)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# OpenAI API (required for AI features)
OPENAI_API_KEY=sk-...

# Vector Database
USE_VECTOR=false  # Set to true for pgvector support

# Application Configuration
BACKEND_HOST=0.0.0.0
UPLOAD_DIR=/app/uploads

# n8n Configuration (optional for local)
N8N_WEBHOOK_URL=http://localhost:5678/webhook/assignment
N8N_ACCESS_TOKEN=your-n8n-access-token
```

### Database Setup

**PostgreSQL with pgvector (Production):**
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT,
    authors TEXT,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT,
    embedding vector(1536)  -- For similarity search
);
```

**PostgreSQL without pgvector (Development/Neon DB):**
```sql
CREATE TABLE academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT,
    authors TEXT,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT
);

-- Create text search index
CREATE INDEX idx_academic_sources_search 
ON academic_sources USING gin(
    to_tsvector('english', title || ' ' || abstract || ' ' || authors)
);
```

## 🚀 Deployment

### Option A: Render (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. **Connect your GitHub repository** to Render
2. **Create a PostgreSQL database** on Render
3. **Create a Web Service** with these settings:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Health Check Path**: `/health`
4. **Set environment variables** in Render dashboard:
   - `DATABASE_URL`: From your Render PostgreSQL
   - `JWT_SECRET_KEY`: Generate a secure key
   - `OPENAI_API_KEY`: Your OpenAI API key

### Option B: Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. **Import your GitHub repository** on Railway
2. **Add PostgreSQL plugin**
3. **Set environment variables** as above
4. **Deploy automatically** on push

### Option C: Custom Server

```bash
# Build Docker image
docker build -t academic-helper .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e JWT_SECRET_KEY=... \
  -e OPENAI_API_KEY=... \
  academic-helper
```

## 🔄 n8n Workflow Automation

The system includes a sophisticated n8n workflow for automated assignment processing:

### Workflow Steps:
1. **Webhook Trigger** - Receives assignment from FastAPI
2. **Text Extraction** - Processes PDF/DOCX/TXT files
3. **RAG Source Search** - Queries academic database
4. **AI Analysis** - Extracts topic, themes, research questions
5. **Plagiarism Detection** - Compares with academic sources
6. **Result Storage** - Saves to PostgreSQL
7. **Notification** - Optional Slack/Email alerts

**To import workflow:**
1. Access n8n at `http://localhost:5678`
2. Go to **Workflows** → **Import from File**
3. Select `workflows/assignment_analysis_workflow.json`
4. Configure credentials and activate

## 🧪 Testing

### Automated Tests
```bash
# Run API tests
python test_api.py

# Test with curl
curl http://localhost:8000/health
```

### Manual Testing Examples

**1. Health Check:**
```bash
curl -s "http://localhost:8000/health" | jq
```

**2. Complete Workflow Test:**
```python
# test_complete_workflow.py
import requests

BASE_URL = "http://localhost:8000"

# 1. Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "test@student.edu",
    "password": "test123",
    "full_name": "Test Student",
    "student_id": "TEST001"
})
print(f"Registration: {response.status_code}")

# 2. Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@student.edu",
    "password": "test123"
})
token = response.json()["access_token"]
print(f"Token received: {token[:20]}...")

# 3. Search sources
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    f"{BASE_URL}/sources?query=machine+learning",
    headers=headers
)
print(f"Sources found: {len(response.json()['sources'])}")

# 4. Upload test file
with open("test_assignment.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        f"{BASE_URL}/upload",
        headers=headers,
        files=files
    )
print(f"Upload result: {response.json()}")
```

## 📊 Performance & Monitoring

### Health Endpoints
- `GET /health` - Basic service health
- `GET /metrics` - Prometheus metrics (if configured)
- Database connection status
- OpenAI API availability

### Logging
```python
# Structured logging example
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit secrets to version control
2. **Password Hashing**: bcrypt with proper salt rounds
3. **JWT Expiry**: Short-lived tokens with refresh capability
4. **File Validation**: Whitelist allowed file types
5. **SQL Injection Prevention**: Use SQLAlchemy ORM with parameterized queries
6. **Rate Limiting**: Implement API rate limiting in production
7. **CORS**: Configure appropriate CORS policies

## 📈 Scaling Considerations

### Vertical Scaling
- Increase Render/Heroku dyno size
- Upgrade PostgreSQL database plan
- Add more CPU/RAM to Docker containers

### Horizontal Scaling
- Add load balancer
- Implement Redis for session storage
- Use connection pooling for database
- Consider read replicas for PostgreSQL

### Performance Optimization
- Add caching layer with Redis
- Implement background job queue (Celery/RQ)
- Use CDN for static files
- Optimize database queries with indexes

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **OpenAI** for GPT models and embeddings
- **PostgreSQL & pgvector** for vector database support
- **n8n** for workflow automation
- **Render** for hosting infrastructure

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/ABREHAMonly/academic-assignment-helper/wiki)
- **Issues**: [GitHub Issues](https://github.com/ABREHAMonly/academic-assignment-helper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ABREHAMonly/academic-assignment-helper/discussions)

---

<div align="center">
  
**Ready to deploy?** [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

*Built with ❤️ for educational institutions worldwide*

</div>

---

### 📋 Changelog

#### v2.0.0 (Current)
- Production-ready Render deployment
- Dual-mode database support (pgvector/Neon DB)
- Enhanced RAG implementation
- Complete n8n workflow automation
- Comprehensive API documentation

#### v1.0.0
- Initial release with FastAPI backend
- Basic file upload and processing
- JWT authentication system
- PostgreSQL integration
- Local development setup

### 🎯 Roadmap

- [ ] **v2.1.0**: Instructor dashboard with analytics
- [ ] **v2.2.0**: Batch processing for multiple assignments
- [ ] **v2.3.0**: Integration with LMS platforms (Canvas, Moodle)
- [ ] **v3.0.0**: Multi-language support
- [ ] **v3.1.0**: Mobile application

### 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [OpenAI API Docs](https://platform.openai.com/docs/)
- [n8n Documentation](https://docs.n8n.io/)
- [Render Documentation](https://render.com/docs)

---

**Happy Coding!** 🎓✨

*For educational use only. Ensure compliance with your institution's academic integrity policies.*