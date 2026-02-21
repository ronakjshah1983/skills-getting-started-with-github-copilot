import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test listing activities
def test_list_activities():
    # Arrange
    # (No setup needed, just use client)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Arrange-Act-Assert: Test registering a participant
def test_register_participant():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

# Arrange-Act-Assert: Test duplicate registration
def test_duplicate_registration():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Arrange-Act-Assert: Test unregistering a participant
def test_unregister_participant():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

# Arrange-Act-Assert: Test unregistering a non-existent participant
def test_unregister_nonexistent():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

# Arrange-Act-Assert: Test invalid activity
def test_invalid_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
