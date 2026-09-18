from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User

bp = Blueprint("orders", __name__)

ALLOWED_ORDER_TYPES = {"dine-in", "takeout", "delivery"}
ALLOWED_PAYMENT_METHODS = {"cash", "qr", "card"}
ALLOWED_STATUSES = {
    "pending",
    "preparing",
    "ready",
    "delivered",
    "cancelled",
}


@bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json(silent=True) or {}
    raw_items = data.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        return jsonify({"message": "At least one order item is required"}), 400

    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "Customer account not found"}), 404

    order_type = str(data.get("order_type", "dine-in")).strip().lower()
    payment_method = str(data.get("payment_method", "cash")).strip().lower()
    if order_type not in ALLOWED_ORDER_TYPES:
        return jsonify({"message": "Invalid order type"}), 400
    if payment_method not in ALLOWED_PAYMENT_METHODS:
        return jsonify({"message": "Invalid payment method"}), 400

    order_items = []
    total_price = 0.0
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            return jsonify({"message": "Invalid order item"}), 400
        try:
            quantity = int(raw_item.get("quantity"))
        except (TypeError, ValueError):
            return jsonify({"message": "Invalid order item"}), 400
        if quantity < 1:
            return jsonify({"message": "Order item quantity must be at least 1"}), 400

        product_id = raw_item.get("product_id")
        if product_id is not None:
            try:
                product_id = int(product_id)
            except (TypeError, ValueError):
                return jsonify({"message": "Invalid order item"}), 400
            product = db.session.get(Product, product_id)
            if not product:
                return jsonify({"message": f"Product {product_id} not found"}), 404
            item_name = product.name
            item_image = product.image or ""
            item_price = product.price
        else:
            item_name = str(raw_item.get("name", ""))
            item_image = str(raw_item.get("image", "") or "")
            item_price = float(raw_item.get("price", 0))

        total_price += item_price * quantity
        order_items.append(
            OrderItem(
                product_id=product_id if product_id else None,
                quantity=quantity,
                price=item_price,
                product_name=item_name,
                product_image=item_image,
            )
        )

    delivery_fee = 5.0 if order_type == "delivery" else 0.0
    total_price += delivery_fee
    order = Order(
        user_id=user.id,
        total_price=total_price,
        order_type=order_type,
        payment_method=payment_method,
        delivery_fee=delivery_fee,
        notes=str(data.get("notes", "")).strip() or None,
        customer_name=str(data.get("customer_name", user.username)).strip(),
        customer_email=str(data.get("customer_email", user.email)).strip(),
        customer_phone=str(data.get("customer_phone", user.phone or "")).strip() or None,
        table_number=str(data.get("table_number", "")).strip() or None,
        delivery_address=str(data.get("delivery_address", "")).strip() or None,
        items=order_items,
    )
    db.session.add(order)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Unable to save order"}), 500

    return jsonify({"message": "Order created", "order": serialize_order(order)}), 201


@bp.route("/orders", methods=["GET"])
@jwt_required()
def get_orders():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "Customer account not found"}), 404

    if user.role == "admin":
        orders = Order.query.order_by(Order.created_at.desc(), Order.id.desc()).all()
    else:
        orders = (
            Order.query
            .filter_by(user_id=user.id)
            .order_by(Order.created_at.desc(), Order.id.desc())
            .all()
        )
    return jsonify([serialize_order(order) for order in orders]), 200


@bp.route("/orders/<int:order_id>", methods=["PATCH"])
@jwt_required()
def update_order(order_id):
    current_user = db.session.get(User, int(get_jwt_identity()))
    if not current_user:
        return jsonify({"message": "Customer account not found"}), 404

    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    if current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json(silent=True) or {}
    status = str(data.get("status", "")).strip().lower()
    if status not in ALLOWED_STATUSES:
        return jsonify({"message": "Invalid order status"}), 400

    order.status = status
    db.session.commit()
    return jsonify({"message": "Order updated", "order": serialize_order(order)}), 200


@bp.route("/orders/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):
    current_user = db.session.get(User, int(get_jwt_identity()))
    if not current_user or current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200


def serialize_order(order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_price": order.total_price,
        "status": order.status,
        "order_type": order.order_type,
        "payment_method": order.payment_method,
        "delivery_fee": order.delivery_fee,
        "notes": order.notes or "",
        "customer_name": order.customer_name or "",
        "customer_email": order.customer_email or "",
        "customer_phone": order.customer_phone or "",
        "table_number": order.table_number or "",
        "delivery_address": order.delivery_address or "",
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product_name or (item.product.name if item.product else ""),
                "product_image": item.product_image or (item.product.image if item.product else ""),
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in order.items
        ],
    }
