import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "phone_number": "+1234567890",
        "role": "elderly",
        "password": "testpassword"
    }
    
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_user():
    # First create a user
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "full_name": "Test User 2",
        "phone_number": "+1234567891",
        "role": "caregiver",
        "password": "testpassword2"
    }
    
    create_response = client.post("/api/users/", json=user_data)
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]
    
    # Then read the user
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser2"
    assert data["id"] == user_id

def test_fall_detection_endpoint():
    # Test the fall detection endpoint structure
    response = client.post("/api/fall-detection/detect-video", data={
        "user_id": 1
    })
    # This will fail because we're not providing a video file,
    # but we're testing that the endpoint exists
    assert response.status_code == 422  # Validation error expected