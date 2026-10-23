from datetime import datetime, timedelta, timezone
from functools import wraps
import re

from flask import Blueprint, current_app, jsonify, request
import jwt
from sqlalchemy.exc import IntegrityError

from ..extensions import bcrypt, db
from ..models.user import User

auth = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,50}$")

def generate_token(user):
    secret = current_app.config.get("SECRET_KEY", "dev")
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return jsonify({"error": "Authentication token is missing"}), 401

        secret = current_app.config.get("SECRET_KEY", "dev")
        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            user_id = int(payload["sub"])
            current_user = db.session.get(User, user_id)
            if not current_user:
                return jsonify({"error": "User not found"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Authentication token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authentication token"}), 401
        except Exception:
            return jsonify({"error": "Token validation failed"}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@auth.post("/signup")
def signup():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if not isinstance(username, str) or not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "Username, email, and password must be strings"}), 400

    username = username.strip()
    email = email.strip().lower()

    if not USERNAME_REGEX.match(username):
        return jsonify({"error": "Username must be between 3 and 50 characters and contain only letters, numbers, and underscores"}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"error": "Invalid email address format"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email address already exists"}), 409

    new_user = User(
        username=username,
        email=email,
        role="member"
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this username or email already exists"}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the account"}), 500

    token = generate_token(new_user)
    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict(),
        "token": token
    }), 201

@auth.post("/login")
def login():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    identifier = data.get("email") or data.get("username")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required"}), 400

    identifier = str(identifier).strip()
    user = User.query.filter(
        (User.email == identifier.lower()) | (User.username == identifier)
    ).first()

    if not user or not user.check_password(str(password)):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user)
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "token": token
    }), 200

@auth.post("/logout")
def logout():
    # Client removes token from storage; endpoint provides clean confirmation
    return jsonify({"message": "Logout successful"}), 200

@auth.get("/me")
@token_required
def me(current_user):
    return jsonify({
        "user": current_user.to_dict()
    }), 200
