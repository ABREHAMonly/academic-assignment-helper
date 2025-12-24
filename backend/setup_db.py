#backend\setup_db.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import sys

# Add the parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def setup_database():
    print("🗄️  Setting up database...")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("💡 Set DATABASE_URL in Railway environment variables")
        return False
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Connected to database successfully!")
            
            # Import here to avoid circular imports
            from backend.models import Base
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created/verified successfully!")
            
            # Check if we have sample data
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM academic_sources"))
                count = result.scalar()
                
                if count == 0:
                    print("📚 Inserting sample academic sources...")
                    
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
                        conn.execute(text("""
                            INSERT INTO academic_sources 
                            (title, authors, publication_year, abstract, full_text, source_type)
                            VALUES (:title, :authors, :publication_year, :abstract, :full_text, :source_type)
                        """), source)
                    conn.commit()
                    print("✅ Sample data inserted!")
                else:
                    print(f"📊 Database already has {count} academic source records")
                    
            except Exception as e:
                print(f"⚠️  Could not insert sample data: {e}")
                # Continue anyway - tables are created
            
            # Check for test user
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM students WHERE email = 'test@student.edu'"))
                if result.scalar() == 0:
                    conn.execute(text("""
                        INSERT INTO students (email, password_hash, full_name, student_id) 
                        VALUES ('test@student.edu', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Test Student', 'S12345')
                    """))
                    conn.commit()
                    print("✅ Test user created (email: test@student.edu, password: testpassword123)")
            except:
                print("⚠️  Could not create test user (might already exist)")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)