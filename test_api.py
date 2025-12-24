#test_api.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"💚 Health: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_authentication():
    """Test registration and login"""
    print("\n🔐 Testing authentication...")
    
    # Register new user
    register_data = {
        "email": "test@student.edu",
        "password": "testpassword123",
        "full_name": "Test Student",
        "student_id": "S001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=10)
        print(f"📝 Registration: {response.status_code}")
        
        # Login
        login_data = {
            "email": "test@student.edu",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        print(f"🔑 Login: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ Got JWT token")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return None

def test_source_search(token):
    """Test RAG source search"""
    print("\n🔍 Testing source search...")
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(
            f"{BASE_URL}/sources?query=machine+learning",
            headers=headers,
            timeout=10
        )
        
        print(f"📚 Source search: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['sources'])} sources")
            if data['sources']:
                for source in data['sources'][:2]:
                    print(f"   - {source['title']} ({source.get('year', 'N/A')})")
        else:
            print(f"❌ Source search failed: {response.text}")
    except Exception as e:
        print(f"❌ Source search test failed: {e}")

if __name__ == "__main__":
    print("🧪 Starting API tests...")
    
    # Wait for services to start
    time.sleep(5)
    
    try:
        # Test health endpoint
        if test_health():
            # Test authentication
            token = test_authentication()
            
            if token:
                # Test source search
                test_source_search(token)
            
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure the backend server is running: python backend/main.py")