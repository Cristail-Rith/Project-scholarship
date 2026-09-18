from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.restaurant_table import RestaurantTable

bp = Blueprint("tables", __name__)

ALLOWED_STATUSES = {"available", "occupied", "reserved", "cleaning"}


def serialize_table(table):
    reservation = next(
        (
            item for item in table.reservations
            if item.status in {"pending", "confirmed"}
        ),
        None,
    )
    return {
        "id": table.id,
        "number": table.table_number,
        "capacity": table.seats,
        "status": table.status.capitalize(),
        "zone": table.zone,
        "shape": table.shape,
        "bgImage": table.bg_image,
        "reservation": {
            "guestName": reservation.guest_name or "Guest",
            "guestEmail": reservation.guest_email or "",
            "guestPhone": reservation.guest_phone or "",
            "guests": reservation.guests,
            "reservedFor": reservation.reserved_for.isoformat(),
            "status": reservation.status,
        } if reservation else None,
    }


def normalize_status(value):
    if value is None:
        return None
    return str(value).strip().lower()


@bp.get("/tables")
def get_tables():
    tables = RestaurantTable.query.order_by(RestaurantTable.table_number).all()
    return jsonify([serialize_table(table) for table in tables]), 200


@bp.post("/tables")
def create_table():
    data = request.get_json(silent=True) or {}
    table_number = data.get("number", data.get("table_number"))
    seats = data.get("capacity", data.get("seats", 2))
    status = normalize_status(data.get("status", "available"))

    if not isinstance(table_number, int) or table_number < 1:
        return jsonify({"message": "number must be a positive integer"}), 400
    if not isinstance(seats, int) or seats < 1:
        return jsonify({"message": "capacity must be a positive integer"}), 400
    if status not in ALLOWED_STATUSES:
        return jsonify({"message": "status is not supported"}), 400

    table = RestaurantTable(
        table_number=table_number, seats=seats, status=status
        , zone=data.get("zone", "Main Dining"),
        shape=data.get("shape", "square"),
        bg_image=data.get("bgImage", ""),
    )
    db.session.add(table)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "that table number already exists"}), 409

    return jsonify(serialize_table(table)), 201


@bp.patch("/tables/<int:table_id>")
def update_table(table_id):
    table = db.session.get(RestaurantTable, table_id)
    if not table:
        return jsonify({"message": "table not found"}), 404

    data = request.get_json(silent=True) or {}
    if "number" in data or "table_number" in data:
        table_number = data.get("number", data.get("table_number"))
        if not isinstance(table_number, int) or table_number < 1:
            return jsonify(
                {"message": "number must be a positive integer"}
            ), 400
        table.table_number = table_number

    if "capacity" in data or "seats" in data:
        seats = data.get("capacity", data.get("seats"))
        if not isinstance(seats, int) or seats < 1:
            return jsonify(
                {"message": "capacity must be a positive integer"}
            ), 400
        table.seats = seats

    if "status" in data:
        status = normalize_status(data["status"])
        if status not in ALLOWED_STATUSES:
            return jsonify({"message": "status is not supported"}), 400
        table.status = status
    if "zone" in data:
        table.zone = str(data["zone"])
    if "shape" in data:
        table.shape = str(data["shape"])
    if "bgImage" in data:
        table.bg_image = str(data["bgImage"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "that table number already exists"}), 409

    return jsonify(serialize_table(table)), 200


@bp.delete("/tables/<int:table_id>")
def delete_table(table_id):
    table = db.session.get(RestaurantTable, table_id)
    if not table:
        return jsonify({"message": "table not found"}), 404

    db.session.delete(table)
    db.session.commit()
    return jsonify({"message": "table deleted"}), 200
