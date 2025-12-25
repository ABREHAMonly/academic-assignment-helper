# backend/main.py (updated imports)
# backend/main.py (fixed imports)
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import os
import sys
from datetime import timedelta
import uuid
import PyPDF2
import docx
import json
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Import modules
from auth import *
from models import Base, Student, Assignment, AnalysisResult, AcademicSource
from rag_service import RAGService

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
        
        # Add test data if needed
        with SessionLocal() as db:
            count = db.execute(text("SELECT COUNT(*) FROM academic_sources")).scalar()
            if count == 0:
                print("📚 Adding sample data...")
                # Insert sample sources
                sample_sources = [
                    {
                        "title": "Machine Learning: A Probabilistic Perspective",
                        "authors": "Kevin P. Murphy",
                        "publication_year": 2012,
                        "abstract": "This textbook offers a comprehensive introduction to machine learning from a probabilistic perspective.",
                        "full_text": "Full text content here...",
                        "source_type": "textbook"
                    },
                    {
                        "title": "Attention Is All You Need",
                        "authors": "Vaswani et al.",
                        "publication_year": 2017,
                        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.",
                        "full_text": "Full text content here...",
                        "source_type": "paper"
                    }
                ]
                
                for source in sample_sources:
                    db.execute(text("""
                        INSERT INTO academic_sources 
                        (title, authors, publication_year, abstract, full_text, source_type)
                        VALUES (:title, :authors, :year, :abstract, :full_text, :source_type)
                    """), {
                        "title": source["title"],
                        "authors": source["authors"],
                        "year": source["publication_year"],
                        "abstract": source["abstract"],
                        "full_text": source["full_text"],
                        "source_type": source["source_type"]
                    })
                db.commit()
                print("✅ Sample data inserted!")
    except Exception as e:
        print(f"⚠️ Database setup warning: {e}")
    yield
    # Shutdown logic would go here

# ✅ ONLY ONE FastAPI app instance
app = FastAPI(
    title="Academic Assignment Helper API",
    version="2.0.0",
    description="RAG-powered academic assignment analysis with plagiarism detection",
    lifespan=lifespan
)

# Security
security = HTTPBearer()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        token_data = verify_token(credentials.credentials)
        user = db.query(Student).filter(Student.email == token_data["email"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Helper functions (keep as is)
def extract_text_from_pdf(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text])
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ""

def save_upload_file(file: UploadFile, upload_dir: str = "./uploads") -> str:
    """Save uploaded file to disk and return path"""
    os.makedirs(upload_dir, exist_ok=True)
    file_extension = file.filename.split('.')[-1].lower()
    file_path = f"{upload_dir}/{uuid.uuid4()}.{file_extension}"
    
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return file_path

# Routes (update health endpoint)
@app.post("/auth/register")
def register(
    email: str = Body(...),
    password: str = Body(...),
    full_name: str = Body(...),
    student_id: str = Body(...),
    db: Session = Depends(get_db)
):
    # Check if user exists
    existing = db.query(Student).filter(Student.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with password length check
    if len(password) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 characters)")
    
    hashed_password = get_password_hash(password)
    student = Student(
        email=email,
        password_hash=hashed_password,
        full_name=full_name,
        student_id=student_id
    )
    
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return {"message": "User registered successfully", "user_id": student.id}

@app.post("/auth/login")
def login(
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    user = db.query(Student).filter(Student.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check password length
    if len(password) > 72:
        password = password[:72]
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user.email, "role": "student", "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload")
async def upload_assignment(
    file: UploadFile = File(...),
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in ['pdf', 'docx', 'txt']:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # Save file
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    file_path = save_upload_file(file, upload_dir)
    
    # Extract text
    try:
        if file_extension == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            text = extract_text_from_docx(file_path)
        else:  # txt
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    # Create assignment record
    assignment = Assignment(
        student_id=current_user.id,
        filename=file.filename,
        original_text=text,
        word_count=len(text.split())
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    
    # Analyze with RAG
    rag_service = RAGService(db)
    sources = rag_service.search_sources(text[:500])
    analysis = rag_service.analyze_assignment(text, sources)
    plagiarism = rag_service.detect_plagiarism(text, sources)
    
    # Create analysis result
    analysis_result = AnalysisResult(
        assignment_id=assignment.id,
        suggested_sources=sources,
        plagiarism_score=plagiarism.get("plagiarism_score", 0.0),
        flagged_sections=plagiarism.get("flagged_sections", []),
        research_suggestions=analysis.get("suggestions", "Analysis complete."),
        citation_recommendations=analysis.get("citation_recommendation", "APA"),
        confidence_score=0.8 if plagiarism.get("confidence") == "high" else 0.5
    )
    
    db.add(analysis_result)
    db.commit()
    db.refresh(analysis_result)
    
    # Clean up file
    try:
        os.remove(file_path)
    except:
        pass
    
    return {
        "job_id": str(analysis_result.id),
        "message": "Assignment uploaded and analyzed successfully",
        "status": "completed",
        "assignment_id": assignment.id
    }

@app.get("/analysis/{analysis_id}")
def get_analysis(
    analysis_id: int,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check assignment belongs to user
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.id == analysis_id
    ).join(Assignment).filter(Assignment.student_id == current_user.id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": analysis.id,
        "assignment_id": analysis.assignment_id,
        "suggested_sources": analysis.suggested_sources or [],
        "plagiarism_score": analysis.plagiarism_score or 0.0,
        "research_suggestions": analysis.research_suggestions or "",
        "citation_recommendations": analysis.citation_recommendations or "",
        "confidence_score": analysis.confidence_score or 0.0,
        "analyzed_at": analysis.analyzed_at.isoformat() if analysis.analyzed_at else ""
    }

@app.get("/sources")
def search_sources(
    query: str,
    top_k: int = 5,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rag_service = RAGService(db)
    sources = rag_service.search_sources(query, top_k)
    
    return {
        "query": query,
        "sources": sources
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        print(f"Database connection error: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "service": "academic-assignment-helper",
        "database": db_status,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "version": "2.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "Academic Assignment Helper API",
        "docs": "/docs",
        "health": "/health",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("BACKEND_PORT", 8000)))
    print(f"🚀 Starting Academic Assignment Helper on {host}:{port}...")
    uvicorn.run(app, host=host, port=port, log_level="info")