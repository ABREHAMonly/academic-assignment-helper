# backend/railway_setup.py
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def setup_railway_database():
    print("🚂 Setting up Railway database...")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Connected to Railway database!")
            
            # Create tables
            from models import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created/verified!")
            
            # Check for existing data
            result = conn.execute(text("SELECT COUNT(*) FROM academic_sources"))
            count = result.scalar()
            
            if count == 0:
                print("📚 Inserting sample data...")
                
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
                print(f"📊 Database already has {count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Railway setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_railway_database()
    sys.exit(0 if success else 1)