import os
import uuid

from flask import Blueprint, jsonify, request, send_from_directory, current_app
from app.extensions import db
from app.models.user import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

AVATAR_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


def parse_request_data():
    if request.content_type and 'application/json' in request.content_type:
        return request.get_json(silent=True) or {}
    form = request.form.to_dict()
    files = request.files
    data = {k: v for k, v in form.items() if v}
    if files.get('avatar'):
        data['_avatar_file'] = files['avatar']
    return data


@bp.get("/users")
@jwt_required()
def get_users():
    current_user = User.query.get(int(get_jwt_identity()))
    if not current_user or current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403
    users = User.query.order_by(User.id.desc()).all()
    return jsonify({"users": [serialize_user(u) for u in users]}), 200


@bp.post("/users")
@jwt_required()
def create_user():
    current_user = User.query.get(int(get_jwt_identity()))
    if not current_user or current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403
    data = parse_request_data()
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    if not username or not email or not password:
        return jsonify({"message": "username, email, and password are required"}), 400
    if User.query.filter(
        (User.username == username) | (User.email == email)
    ).first():
        return jsonify({"message": "Username or email already exists"}), 409
    role = str(data.get("role", "customer")).strip()
    if role not in ("admin", "customer", "online_customer"):
        role = "customer"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(
        username=username, email=email,
        phone=str(data.get("phone", "")).strip() or None,
        password_hash=hashed_password, role=role,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "user": serialize_user(user)}), 201


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    phone = str(data.get("phone", "")).strip()
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
        phone=phone if phone else None,
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
    identifier = str(data.get("email", data.get("username", ""))).strip().lower()
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()
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
        "phone": user.phone,
        "avatar": user.avatar,
        "role": user.role,
    }


@bp.put("/users/<int:user_id>")
@jwt_required()
def update_user(user_id):
    current_user = User.query.get(int(get_jwt_identity()))
    if not current_user or current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = parse_request_data()

    avatar_file = data.pop('_avatar_file', None)

    if "username" in data:
        new_username = str(data["username"]).strip()
        if new_username and new_username != user.username:
            existing = User.query.filter(User.username == new_username).first()
            if existing and existing.id != user.id:
                return jsonify({"message": "Username already taken"}), 409
            user.username = new_username

    if "email" in data:
        new_email = str(data["email"]).strip().lower()
        if new_email and new_email != user.email:
            existing = User.query.filter(User.email == new_email).first()
            if existing and existing.id != user.id:
                return jsonify({"message": "Email already taken"}), 409
            user.email = new_email

    if "phone" in data:
        user.phone = str(data["phone"]).strip() if data["phone"] else None

    if "role" in data:
        role = str(data["role"]).strip()
        if role not in ("admin", "customer", "online_customer"):
            return jsonify({"message": "Invalid user role"}), 400
        user.role = role

    if avatar_file:
        AVATAR_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
        original_name = avatar_file.filename
        extension = (
            original_name.rsplit(".", 1)[-1].lower()
            if "." in original_name
            else ""
        )
        if extension not in AVATAR_EXTENSIONS:
            return jsonify({"message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"}), 400
        upload_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "uploads", "avatars"
        )
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"{user.id}_{uuid.uuid4().hex}.{extension}"
        avatar_file.save(os.path.join(upload_folder, filename))
        user.avatar = f"/uploads/avatars/{filename}"

    db.session.commit()
    return jsonify({"message": "User updated", "user": serialize_user(user)}), 200


@bp.delete("/users/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    current_user = User.query.get(int(get_jwt_identity()))
    if not current_user or current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


@bp.get("/me")
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"user": serialize_user(user)})


@bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json(silent=True) or {}

    if "username" in data:
        new_username = str(data["username"]).strip()
        if new_username and new_username != user.username:
            existing = User.query.filter(User.username == new_username).first()
            if existing and existing.id != user.id:
                return jsonify({"message": "Username already taken"}), 409
            user.username = new_username

    if "email" in data:
        new_email = str(data["email"]).strip().lower()
        if new_email and new_email != user.email:
            existing = User.query.filter(User.email == new_email).first()
            if existing and existing.id != user.id:
                return jsonify({"message": "Email already taken"}), 409
            user.email = new_email

    if "phone" in data:
        user.phone = str(data["phone"]).strip() if data["phone"] else None

    if "currentPassword" in data or "newPassword" in data:
        current_password = data.get("currentPassword", "")
        new_password = data.get("newPassword", "")
        if not current_password or not new_password:
            return jsonify({"message": "Current password and new password are required"}), 400
        if not bcrypt.check_password_hash(user.password_hash, current_password):
            return jsonify({"message": "Current password is incorrect"}), 401
        if len(new_password) < 6:
            return jsonify({"message": "New password must be at least 6 characters"}), 400
        user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": serialize_user(user)}), 200


@bp.route("/me/avatar", methods=["PATCH"])
@jwt_required()
def update_avatar():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404

    avatar_file = request.files.get("avatar")
    if not avatar_file or not avatar_file.filename:
        return jsonify({"message": "Avatar image is required"}), 400

    original_name = avatar_file.filename
    extension = (
        original_name.rsplit(".", 1)[-1].lower()
        if "." in original_name
        else ""
    )
    if extension not in AVATAR_EXTENSIONS:
        return jsonify({
            "message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"
        }), 400

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads",
        "avatars",
    )
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"{user.id}_{uuid.uuid4().hex}.{extension}"
    avatar_file.save(os.path.join(upload_folder, filename))

    avatar_path = f"/uploads/avatars/{filename}"
    user.avatar = avatar_path
    db.session.commit()

    return jsonify({"message": "Avatar updated", "user": serialize_user(user)}), 200


@bp.get("/uploads/avatars/<path:filename>")
def get_avatar(filename):
    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads",
        "avatars",
    )
    return send_from_directory(upload_folder, filename)
