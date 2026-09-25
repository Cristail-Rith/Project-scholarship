from datetime import date
from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models.event_inquiry import EventInquiry

bp = Blueprint("event_inquiries", __name__)
VALID_STATUSES = {"new", "contacted", "confirmed", "declined"}


def admin_required(view):
    @wraps(view)
    @jwt_required()
    def wrapped(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return view(*args, **kwargs)
    return wrapped


def serialize_inquiry(item):
    return {
        "id": item.id,
        "name": item.name,
        "email": item.email,
        "phone": item.phone,
        "eventDate": item.event_date.isoformat(),
        "guests": item.guests,
        "preferredSpace": item.preferred_space,
        "eventType": item.event_type,
        "notes": item.notes or "",
        "status": item.status,
        "createdAt": item.created_at.isoformat() if item.created_at else None,
    }


@bp.post("/event-inquiries")
def create_event_inquiry():
    data = request.get_json(silent=True) or {}
    required = ("name", "email", "phone", "date", "guests", "preferred_space", "event_type")
    if any(not str(data.get(key, "")).strip() for key in required):
        return jsonify({"message": "Please complete all required event details."}), 400

    try:
        event_date = date.fromisoformat(str(data["date"]))
        guests = int(data["guests"])
    except (TypeError, ValueError):
        return jsonify({"message": "Enter a valid event date and guest count."}), 400
    if guests < 5 or guests > 150:
        return jsonify({"message": "Event guest count must be between 5 and 150."}), 400

    inquiry = EventInquiry(
        name=str(data["name"]).strip(),
        email=str(data["email"]).strip().lower(),
        phone=str(data["phone"]).strip(),
        event_date=event_date,
        guests=guests,
        preferred_space=str(data["preferred_space"]).strip(),
        event_type=str(data["event_type"]).strip(),
        notes=str(data.get("notes", "")).strip(),
        status="new",
    )
    db.session.add(inquiry)
    db.session.commit()
    return jsonify({
        "message": "Event inquiry received",
        "inquiry": serialize_inquiry(inquiry),
    }), 201


@bp.get("/event-inquiries")
@admin_required
def get_event_inquiries():
    inquiries = EventInquiry.query.order_by(EventInquiry.created_at.desc()).all()
    return jsonify([serialize_inquiry(item) for item in inquiries]), 200


@bp.patch("/event-inquiries/<int:inquiry_id>")
@admin_required
def update_event_inquiry(inquiry_id):
    inquiry = db.session.get(EventInquiry, inquiry_id)
    if not inquiry:
        return jsonify({"message": "Event inquiry not found."}), 404
    status = str((request.get_json(silent=True) or {}).get("status", "")).lower()
    if status not in VALID_STATUSES:
        return jsonify({"message": "Unsupported inquiry status."}), 400
    inquiry.status = status
    db.session.commit()
    return jsonify({"inquiry": serialize_inquiry(inquiry)}), 200
