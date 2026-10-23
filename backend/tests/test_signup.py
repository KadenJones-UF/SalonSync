import pytest
from app.models.user import User

def test_signup_success(client):
    """TC-REG-01: Register a new stylist account with valid information."""
    payload = {
        "username": "jsmith_color",
        "email": "jsmith@example.com",
        "password": "Balayage2026"
    }
    res = client.post("/api/auth/signup", json=payload)
    assert res.status_code == 201

    data = res.get_json()
    assert data["message"] == "User registered successfully"
    assert "user" in data
    user_data = data["user"]
    assert user_data["username"] == "jsmith_color"
    assert user_data["email"] == "jsmith@example.com"
    assert user_data["role"] == "member"
    assert "password" not in user_data
    assert "password_hash" not in user_data

    # Verify user exists in database with hashed password
    user = User.query.filter_by(username="jsmith_color").first()
    assert user is not None
    assert user.email == "jsmith@example.com"
    assert user.password_hash != "Balayage2026"
    assert user.password_hash.startswith("$2")

def test_signup_duplicate_username(client):
    """TC-REG-02: Registration rejects duplicate username."""
    client.post("/api/auth/signup", json={
        "username": "stylist1",
        "email": "stylist1@example.com",
        "password": "ValidPassword123"
    })

    res = client.post("/api/auth/signup", json={
        "username": "stylist1",
        "email": "different@example.com",
        "password": "AnotherPassword123"
    })
    assert res.status_code == 409
    data = res.get_json()
    assert "already exists" in data["error"].lower()

def test_signup_duplicate_email(client):
    """TC-REG-02: Registration rejects duplicate email."""
    client.post("/api/auth/signup", json={
        "username": "unique_user",
        "email": "duplicate@example.com",
        "password": "ValidPassword123"
    })

    res = client.post("/api/auth/signup", json={
        "username": "another_user",
        "email": "duplicate@example.com",
        "password": "AnotherPassword123"
    })
    assert res.status_code == 409
    data = res.get_json()
    assert "already exists" in data["error"].lower()

def test_signup_short_password(client):
    """TC-REG-02: Registration rejects password shorter than 8 characters."""
    res = client.post("/api/auth/signup", json={
        "username": "shortpass_user",
        "email": "short@example.com",
        "password": "short"
    })
    assert res.status_code == 400
    data = res.get_json()
    assert "at least 8 characters" in data["error"].lower()

def test_signup_invalid_email_format(client):
    """TC-REG-02: Registration rejects invalid email format."""
    res = client.post("/api/auth/signup", json={
        "username": "invalid_email_user",
        "email": "not-an-email",
        "password": "ValidPassword123"
    })
    assert res.status_code == 400
    data = res.get_json()
    assert "invalid email" in data["error"].lower()

def test_signup_missing_fields(client):
    """TC-REG-02: Registration rejects missing required fields."""
    # Missing username
    res = client.post("/api/auth/signup", json={
        "email": "missing_user@example.com",
        "password": "ValidPassword123"
    })
    assert res.status_code == 400

    # Missing email
    res = client.post("/api/auth/signup", json={
        "username": "no_email_user",
        "password": "ValidPassword123"
    })
    assert res.status_code == 400

    # Missing password
    res = client.post("/api/auth/signup", json={
        "username": "no_password_user",
        "email": "nopass@example.com"
    })
    assert res.status_code == 400

def test_signup_invalid_username_format(client):
    """TC-REG-02: Registration rejects invalid username format."""
    # Too short (< 3 chars)
    res = client.post("/api/auth/signup", json={
        "username": "ab",
        "email": "ab@example.com",
        "password": "ValidPassword123"
    })
    assert res.status_code == 400

    # Contains illegal characters
    res = client.post("/api/auth/signup", json={
        "username": "bad user!",
        "email": "bad@example.com",
        "password": "ValidPassword123"
    })
    assert res.status_code == 400

def test_signup_non_json_payload(client):
    """Registration rejects non-JSON requests."""
    res = client.post("/api/auth/signup", data="not json", content_type="text/plain")
    assert res.status_code == 400
