import os
import uuid

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.reservation import Reservation
from app.models.restaurant_table import RestaurantTable

bp = Blueprint("tables", __name__)

ALLOWED_STATUSES = {"available", "occupied", "reserved", "cleaning"}
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


@bp.get("/uploads/tables/<path:filename>")
def table_image(filename):
    upload_folder = os.path.join(os.path.dirname(current_app.config["UPLOAD_FOLDER"]), "tables")
    return send_from_directory(upload_folder, filename)


def save_table_image(image_file):
    if not image_file or not image_file.filename:
        return ""
    safe_name = secure_filename(image_file.filename)
    extension = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None
    upload_folder = os.path.join(os.path.dirname(current_app.config["UPLOAD_FOLDER"]), "tables")
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    image_file.save(os.path.join(upload_folder, filename))
    return f"/uploads/tables/{filename}"


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
    data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
    table_number = data.get("number", data.get("table_number"))
    seats = data.get("capacity", data.get("seats", 2))
    status = normalize_status(data.get("status", "available"))

    try:
        table_number = int(table_number)
        seats = int(seats)
    except (TypeError, ValueError):
        return jsonify({"message": "number and capacity must be positive integers"}), 400
    if table_number < 1:
        return jsonify({"message": "number must be a positive integer"}), 400
    if seats < 1:
        return jsonify({"message": "capacity must be a positive integer"}), 400
    if status not in ALLOWED_STATUSES:
        return jsonify({"message": "status is not supported"}), 400

    image_file = request.files.get("image")
    bg_image = save_table_image(image_file) if image_file else str(data.get("bgImage", "")).strip()
    if bg_image is None:
        return jsonify({"message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"}), 400

    table = RestaurantTable(
        table_number=table_number, seats=seats, status=status
        , zone=data.get("zone", "Main Dining"),
        shape=data.get("shape", "square"),
        bg_image=bg_image,
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

    data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
    if "number" in data or "table_number" in data:
        try:
            table_number = int(data.get("number", data.get("table_number")))
        except (TypeError, ValueError):
            return jsonify({"message": "number must be a positive integer"}), 400
        if table_number < 1:
            return jsonify(
                {"message": "number must be a positive integer"}
            ), 400
        table.table_number = table_number

    if "capacity" in data or "seats" in data:
        try:
            seats = int(data.get("capacity", data.get("seats")))
        except (TypeError, ValueError):
            return jsonify({"message": "capacity must be a positive integer"}), 400
        if seats < 1:
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
    image_file = request.files.get("image")
    if image_file:
        bg_image = save_table_image(image_file)
        if bg_image is None:
            return jsonify({"message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"}), 400
        table.bg_image = bg_image
    elif "bgImage" in data:
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

    if Reservation.query.filter_by(table_id=table.id).first():
        return jsonify({
            "message": "This table has reservation history and cannot be deleted. Change its status or details instead."
        }), 409

    db.session.delete(table)
    db.session.commit()
    return jsonify({"message": "table deleted"}), 200







