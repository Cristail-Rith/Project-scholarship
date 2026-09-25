from datetime import date
from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models.contact_message import ContactMessage

bp = Blueprint("contact_messages", __name__)
VALID_STATUSES = {"new", "contacted", "resolved"}


def admin_required(view):
    @wraps(view)
    @jwt_required()
    def wrapped(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return view(*args, **kwargs)
    return wrapped


def serialize_message(item):
    return {
        "id": item.id,
        "name": item.name,
        "email": item.email,
        "phone": item.phone,
        "preferredDate": item.preferred_date.isoformat() if item.preferred_date else "",
        "guests": item.guests,
        "message": item.message or "",
        "status": item.status,
        "createdAt": item.created_at.isoformat() if item.created_at else None,
    }


@bp.post("/contact-messages")
def create_contact_message():
    data = request.get_json(silent=True) or {}
    required = ("name", "email", "phone")
    if any(not str(data.get(key, "")).strip() for key in required):
        return jsonify({"message": "Name, email, and phone are required."}), 400
    try:
        guests = int(data.get("guests", 2))
        preferred_date = date.fromisoformat(data["date"]) if data.get("date") else None
    except (TypeError, ValueError):
        return jsonify({"message": "Enter a valid date and guest count."}), 400
    if guests not in {1, 2, 4, 6}:
        return jsonify({"message": "Choose a supported guest count."}), 400

    item = ContactMessage(
        name=str(data["name"]).strip(),
        email=str(data["email"]).strip().lower(),
        phone=str(data["phone"]).strip(),
        preferred_date=preferred_date,
        guests=guests,
        message=str(data.get("message", "")).strip(),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Your request has been received.", "contactMessage": serialize_message(item)}), 201


@bp.get("/contact-messages")
@admin_required
def get_contact_messages():
    items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([serialize_message(item) for item in items]), 200


@bp.patch("/contact-messages/<int:message_id>")
@admin_required
def update_contact_message(message_id):
    item = db.session.get(ContactMessage, message_id)
    if not item:
        return jsonify({"message": "Contact message not found."}), 404
    status = str((request.get_json(silent=True) or {}).get("status", "")).lower()
    if status not in VALID_STATUSES:
        return jsonify({"message": "Unsupported message status."}), 400
    item.status = status
    db.session.commit()
    return jsonify({"contactMessage": serialize_message(item)}), 200
