#test_api.py
# test_api.py (updated)
import requests
import json
import time
import sys

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
    
    # Generate unique email for testing
    import random
    unique_id = random.randint(1000, 9999)
    test_email = f"test{unique_id}@student.edu"
    
    # Register new user
    register_data = {
        "email": test_email,
        "password": "testpassword123",
        "full_name": f"Test Student {unique_id}",
        "student_id": f"S{unique_id}"
    }
    
    try:
        # Test registration
        print(f"📝 Registering new user: {test_email}")
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=10)
        print(f"📝 Registration response: {response.status_code}")
        if response.status_code != 200:
            print(f"📝 Registration response body: {response.text}")
        
        # Now test login with the newly created user
        login_data = {
            "email": test_email,
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
        import traceback
        traceback.print_exc()
        return None

def test_existing_user_login():
    """Test login with existing test user from setup_db.py"""
    print("\n🔐 Testing login with existing test user...")
    
    # Use the test user created by setup_db.py
    login_data = {
        "email": "test@student.edu",
        "password": "testpassword123"  # Password from setup_db.py
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        print(f"🔑 Existing user login: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ Got JWT token for existing user")
            return token
        else:
            print(f"❌ Existing user login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login test failed: {e}")
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
    time.sleep(3)
    
    try:
        # Test health endpoint
        if not test_health():
            print("❌ Health check failed. Is the server running?")
            sys.exit(1)
        
        # First try to test with new user
        print("\n--- Testing with new user ---")
        token = test_authentication()
        
        # If new user registration fails, try existing user
        if not token:
            print("\n--- Testing with existing user ---")
            token = test_existing_user_login()
        
        if token:
            # Test source search
            test_source_search(token)
        else:
            print("❌ All authentication tests failed")
            
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure the backend server is running: python backend/main.py")