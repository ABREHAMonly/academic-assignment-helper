-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create tables
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    student_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    filename TEXT,
    original_text TEXT,
    topic TEXT,
    academic_level TEXT,
    word_count INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id),
    suggested_sources JSONB,
    plagiarism_score FLOAT,
    flagged_sections JSONB,
    research_suggestions TEXT,
    citation_recommendations TEXT,
    confidence_score FLOAT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT,
    authors TEXT,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT,
    embedding_data JSONB
);

-- Create indexes for text search
CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_assignments_student_id ON assignments(student_id);
CREATE INDEX IF NOT EXISTS idx_academic_sources_search 
ON academic_sources USING gin(to_tsvector('english', title || ' ' || abstract || ' ' || authors));