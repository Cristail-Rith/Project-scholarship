from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.user import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

bcrypt = Bcrypt()

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    if not username or not email or not password:
        return jsonify({
            "message": "username, email, and password are required"
        }), 400
    if User.query.filter(
        (User.username == username) | (User.email == email)
    ).first():
        return jsonify({"message": "Username or email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    first_user = User.query.count() == 0
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="admin" if first_user else "customer",
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User created",
        "user": serialize_user(user),
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(
        user.password_hash, data.get("password", "")
    ):
        token = create_access_token(
            identity=str(user.id), additional_claims={"role": user.role}
        )
        return jsonify({
            "message": "Login successful",
            "access_token": token,
            "user": serialize_user(user),
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401


def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


@bp.get("/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"user": serialize_user(user)})
