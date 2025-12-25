import requests
import os

# Test your Render URL after deployment
BASE_URL = "https://your-app.onrender.com"  # Your Render URL

def test_render():
    print(f"Testing {BASE_URL}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"✅ Health: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test authentication
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@student.edu", "password": "testpassword123"},
            timeout=10
        )
        print(f"🔑 Login: {response.status_code}")
        if response.status_code == 200:
            print("✅ Authentication works!")
    except Exception as e:
        print(f"❌ Login failed: {e}")

if __name__ == "__main__":
    test_render()