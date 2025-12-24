# backend/local_setup.py
import os
import sys
import subprocess

def setup_local_environment():
    print("🔧 Setting up local development environment...")
    
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(script_dir, "requirements.txt")])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Create .env file if it doesn't exist
    env_path = os.path.join(root_dir, ".env")
    if not os.path.exists(env_path):
        print("📝 Creating .env file...")
        with open(env_path, "w") as f:
            f.write("""# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/academic_helper

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# OpenAI API (optional - for RAG and AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Vector Database
USE_VECTOR=false

# n8n Configuration
N8N_WEBHOOK_URL=http://localhost:5678/webhook/assignment
N8N_ACCESS_TOKEN=your-n8n-access-token-here

# Application Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
UPLOAD_DIR=./uploads
""")
        print("✅ .env file created. Please update with your actual credentials.")
    else:
        print("✅ .env file already exists")
    
    # Create uploads directory
    uploads_dir = os.path.join(root_dir, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"✅ Created uploads directory: {uploads_dir}")
    
    # Create data directory
    data_dir = os.path.join(root_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create workflows directory
    workflows_dir = os.path.join(root_dir, "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    
    return True

if __name__ == "__main__":
    success = setup_local_environment()
    if success:
        print("\n🎉 Setup complete!")
        print("📋 Next steps:")
        print("  1. Update .env file with your configuration")
        print("  2. Run: python backend/setup_db.py to initialize database")
        print("  3. Run: python backend/main.py to start the server")
        print("  4. Access: http://localhost:8000/docs")
    else:
        print("\n❌ Setup failed. Please check errors above.")