from datetime import datetime
import json
from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models.reservation import Reservation
from app.models.restaurant_table import RestaurantTable
from app.models.user import User

bp = Blueprint("reservations", __name__)


def admin_required(view):
    @wraps(view)
    @jwt_required()
    def wrapped(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return view(*args, **kwargs)
    return wrapped


@bp.post("/reservations")
@jwt_required(optional=True)
def create_reservation():
    data = request.get_json(silent=True) or {}
    required = ("date", "time", "guests", "first_name", "last_name")
    if any(not data.get(field) for field in required):
        return jsonify({"message": "Reservation details are required"}), 400

    try:
        guests = int(data["guests"])
        reserved_for = datetime.strptime(
            f"{data['date']} {data['time']}", "%Y-%m-%d %I:%M %p"
        )
    except (TypeError, ValueError):
        return jsonify({
            "message": "Invalid reservation date or guest count"
        }), 400

    if guests < 1:
        return jsonify({"message": "Guest count must be at least 1"}), 400

    area_name = str(data.get("area_name", "Main Dining Room"))[:100]
    area_zones = {
        "Main Dining Room": "Main Dining",
        "Garden Terrace": "Terrace",
        "Chef's Counter": "Bar",
        "Private Dining": "VIP Lounge",
        "VIP Suite": "VIP Lounge",
    }
    preferred_zone = area_zones.get(area_name)
    requested_table_id = data.get("table_id")
    if requested_table_id:
        table = db.session.get(RestaurantTable, int(requested_table_id))
        if not table:
            return jsonify({"message": "Selected table not found"}), 404
        if table.status != "available" or table.seats < guests or (preferred_zone and table.zone != preferred_zone):
            return jsonify({"message": "Selected table is not available for this party size"}), 409
    else:
        query = RestaurantTable.query.filter(
            RestaurantTable.seats >= guests,
            RestaurantTable.status == "available",
        )
        if preferred_zone:
            query = query.filter(RestaurantTable.zone == preferred_zone)
        table = query.order_by(RestaurantTable.seats, RestaurantTable.table_number).first()

    identity = get_jwt_identity()
    user = db.session.get(User, int(identity)) if identity else None
    booking_type = data.get("booking_type", "dining")
    valid_types = ("dining", "private", "room")
    if booking_type not in valid_types:
        booking_type = "dining"

    reservation = Reservation(
        user_id=user.id if user else None,
        table_id=table.id if table else None,
        reserved_for=reserved_for,
        guests=guests,
        booking_type=booking_type,
        status="pending",
        notes=data.get("notes", ""),
        area_name=area_name,
        occasion=str(data.get("occasion", "Casual Fine Dining"))[:100],
        dietary_preferences=json.dumps(data.get("dietary", [])),
        guest_name=f"{data['first_name']} {data['last_name']}".strip(),
        guest_email=data.get("email") or (user.email if user else ""),
        guest_phone=data.get("phone", ""),
    )
    if table:
        table.status = "reserved"
    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": "Reservation request received",
        "reservation": serialize_reservation(reservation),
    }), 201


@bp.get("/reservations")
@admin_required
def get_reservations():
    reservations = Reservation.query.order_by(Reservation.reserved_for).all()
    return jsonify([serialize_reservation(item) for item in reservations]), 200


def serialize_reservation(reservation):
    return {
        "id": reservation.id,
        "userId": reservation.user_id,
        "tableId": reservation.table_id,
        "tableNumber": (
            reservation.table.table_number if reservation.table else None
        ),
        "zone": (
            reservation.table.zone if reservation.table else "Main Dining"
        ),
        "reservedFor": reservation.reserved_for.isoformat(),
        "guests": reservation.guests,
        "status": reservation.status,
        "bookingType": reservation.booking_type,
        "areaName": reservation.area_name,
        "occasion": reservation.occasion,
        "dietary": json.loads(reservation.dietary_preferences or "[]"),
        "guestName": reservation.guest_name or "Guest",
        "guestEmail": reservation.guest_email or "",
        "guestPhone": reservation.guest_phone or "",
        "notes": reservation.notes or "",
    }


@bp.patch("/reservations/<int:reservation_id>")
@admin_required
def update_reservation(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    status = str((request.get_json(silent=True) or {}).get("status", "")).lower()
    if status not in {"pending", "confirmed", "cancelled", "completed"}:
        return jsonify({"message": "Unsupported reservation status"}), 400
    reservation.status = status
    if status == "cancelled" and reservation.table:
        reservation.table.status = "available"
    elif status in {"pending", "confirmed"} and reservation.table:
        reservation.table.status = "reserved"
    db.session.commit()
    return jsonify({"reservation": serialize_reservation(reservation)}), 200
