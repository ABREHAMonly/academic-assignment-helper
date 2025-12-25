# backend/render_setup.py
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def setup_render_database():
    print("🚀 Setting up Render database...")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Connected to Render database!")
            
            # Import models
            from models import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created/verified!")
            
            # Check for existing data
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
                    },
                    {
                        "title": "Deep Learning",
                        "authors": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
                        "publication_year": 2016,
                        "abstract": "Comprehensive textbook on deep learning.",
                        "full_text": "Full text content here...",
                        "source_type": "textbook"
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
            
            # Create test user if not exists
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM students WHERE email = 'test@student.edu'"))
                if result.scalar() == 0:
                    from auth import get_password_hash
                    hashed_pw = get_password_hash("testpassword123")
                    conn.execute(text("""
                        INSERT INTO students (email, password_hash, full_name, student_id) 
                        VALUES ('test@student.edu', :password, 'Test Student', 'S12345')
                    """), {"password": hashed_pw})
                    conn.commit()
                    print("✅ Test user created (email: test@student.edu, password: testpassword123)")
            except Exception as e:
                print(f"⚠️ Could not create test user: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Render database setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_render_database()
    sys.exit(0 if success else 1)