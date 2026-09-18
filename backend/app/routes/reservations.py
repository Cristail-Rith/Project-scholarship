from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.reservation import Reservation
from app.models.restaurant_table import RestaurantTable
from app.models.user import User

bp = Blueprint("reservations", __name__)


@bp.post("/reservations")
@jwt_required()
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

    requested_table_id = data.get("table_id")
    if requested_table_id:
        table = db.session.get(RestaurantTable, int(requested_table_id))
        if not table:
            return jsonify({"message": "Selected table not found"}), 404
        if table.status != "available" or table.seats < guests:
            return jsonify({"message": "Selected table is not available for this party size"}), 409
    else:
        table = (
            RestaurantTable.query
            .filter(
                RestaurantTable.seats >= guests,
                RestaurantTable.status == "available",
            )
            .order_by(RestaurantTable.seats, RestaurantTable.table_number)
            .first()
        )
    if not table:
        return jsonify({
            "message": "No available table fits this party size"
        }), 409

    user = db.session.get(User, int(get_jwt_identity()))
    reservation = Reservation(
        user_id=user.id,
        table_id=table.id,
        reserved_for=reserved_for,
        guests=guests,
        status="confirmed",
        notes=data.get("notes", ""),
        guest_name=f"{data['first_name']} {data['last_name']}".strip(),
        guest_email=data.get("email", user.email),
        guest_phone=data.get("phone", ""),
    )
    table.status = "reserved"
    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": "Reservation confirmed",
        "reservation": serialize_reservation(reservation),
    }), 201


@bp.get("/reservations")
@jwt_required()
def get_reservations():
    reservations = Reservation.query.order_by(Reservation.reserved_for).all()
    return jsonify([serialize_reservation(item) for item in reservations]), 200


def serialize_reservation(reservation):
    return {
        "id": reservation.id,
        "tableId": reservation.table_id,
        "tableNumber": (
            reservation.table.table_number if reservation.table else None
        ),
        "reservedFor": reservation.reserved_for.isoformat(),
        "guests": reservation.guests,
        "status": reservation.status,
        "guestName": reservation.guest_name or "Guest",
        "guestEmail": reservation.guest_email or "",
        "guestPhone": reservation.guest_phone or "",
        "notes": reservation.notes or "",
    }
