import re
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..extensions import bcrypt, db
from ..models.user import User

auth = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,50}$")

@auth.post("/signup")
def signup():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Missing fields
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Type checks and string stripping
    if not isinstance(username, str) or not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "Username, email, and password must be strings"}), 400

    username = username.strip()
    email = email.strip().lower()

    # Username validation (3-50 chars, alphanumeric + underscore)
    if not USERNAME_REGEX.match(username):
        return jsonify({"error": "Username must be between 3 and 50 characters and contain only letters, numbers, and underscores"}), 400

    # Email format validation
    if not EMAIL_REGEX.match(email):
        return jsonify({"error": "Invalid email address format"}), 400

    # Password length validation (minimum 8 characters)
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    # Check for existing user or email
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email address already exists"}), 409

    # Hash password with bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create user
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="member"
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this username or email already exists"}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the account"}), 500

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict()
    }), 201
