import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    # Use a unique username/email for each test run to avoid conflicts
    import uuid
    unique = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"testuser_{unique}",
        "email": f"test_{unique}@example.com",
        "password": "testpassword",
        "name": "Test User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == user_data["username"]

def test_login_user():
    # Register a new user first
    import uuid
    unique = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"loginuser_{unique}",
        "email": f"login_{unique}@example.com",
        "password": "testpassword",
        "name": "Login User"
    }
    client.post("/users/", json=user_data)
    # Attempt login
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
