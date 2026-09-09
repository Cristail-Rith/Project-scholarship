from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

bp = Blueprint("orders", __name__)


@bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    total_price = 0
    items = []
    for item in data["items"]:
        product = Product.query.get(item["product_id"])
        if not product:
            return jsonify({"message": f"Product {item['product_id']} not found"}), 404
        total_price += product.price * item["quantity"]
        items.append(OrderItem(product_id=product.id, quantity=item["quantity"], price=product.price))

    order = Order(user_id=data["user_id"], total_price=total_price, items=items)
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order created"}), 201


@bp.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "user_id": o.user_id, "total_price": o.total_price, "status": o.status} for o in orders]), 200
