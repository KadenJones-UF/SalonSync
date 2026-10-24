import pytest
from app.models.user import User

@pytest.fixture
def registered_user(client):
    payload = {
        "username": "stylist_jane",
        "email": "jane@example.com",
        "password": "CorrectPassword123"
    }
    res = client.post("/api/auth/signup", json=payload)
    assert res.status_code == 201
    return payload

def test_login_success_with_email(client, registered_user):
    """TC-AUTH-01: Log in with valid email and password."""
    res = client.post("/api/auth/login", json={
        "email": "jane@example.com",
        "password": "CorrectPassword123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["message"] == "Login successful"
    assert "token" in data
    assert data["user"]["username"] == "stylist_jane"
    assert data["user"]["email"] == "jane@example.com"

def test_login_success_with_username(client, registered_user):
    """TC-AUTH-01: Log in with valid username and password."""
    res = client.post("/api/auth/login", json={
        "username": "stylist_jane",
        "password": "CorrectPassword123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["message"] == "Login successful"
    assert "token" in data

def test_login_wrong_password(client, registered_user):
    """TC-AUTH-01: Block access with incorrect password."""
    res = client.post("/api/auth/login", json={
        "email": "jane@example.com",
        "password": "WrongPassword999"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert "invalid email or password" in data["error"].lower()

def test_login_nonexistent_user(client):
    """TC-AUTH-01: Block access for user that does not exist."""
    res = client.post("/api/auth/login", json={
        "email": "doesnotexist@example.com",
        "password": "SomePassword123"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert "invalid email or password" in data["error"].lower()

def test_login_missing_fields(client):
    """Block login when credentials are missing."""
    res = client.post("/api/auth/login", json={"email": "jane@example.com"})
    assert res.status_code == 400

    res2 = client.post("/api/auth/login", json={"password": "password123"})
    assert res2.status_code == 400

def test_logout(client):
    """TC-AUTH-01: Verify logout endpoint response."""
    res = client.post("/api/auth/logout")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Logout successful"

def test_protected_route_with_valid_token(client, registered_user):
    """Access protected /api/auth/me with valid Bearer token."""
    login_res = client.post("/api/auth/login", json={
        "email": "jane@example.com",
        "password": "CorrectPassword123"
    })
    token = login_res.get_json()["token"]

    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["user"]["username"] == "stylist_jane"

def test_me_returns_profile_fields(client, registered_user):
    """TC-PROF-02: /api/auth/me returns username, email, and role for the profile header."""
    login_res = client.post("/api/auth/login", json={
        "email": "jane@example.com",
        "password": "CorrectPassword123"
    })
    token = login_res.get_json()["token"]

    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    user = res.get_json()["user"]
    assert user["username"] == "stylist_jane"
    assert user["email"] == "jane@example.com"
    assert user["role"] == "member"

def test_protected_route_missing_or_invalid_token(client):
    """Block protected route when token is missing or corrupted."""
    # Missing token
    res1 = client.get("/api/auth/me")
    assert res1.status_code == 401

    # Invalid token string
    res2 = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.fake.token"})
    assert res2.status_code == 401
