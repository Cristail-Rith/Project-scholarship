from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.product import Product

bp = Blueprint("products", __name__)


@bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([serialize_product(product) for product in products]), 200


@bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True) or {}
    required = ("name", "price", "category_id")
    if any(field not in data for field in required):
        return jsonify({
            "message": "name, price, and category_id are required"
        }), 400
    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        rating=str(data.get("rating", "0.0")),
        image=data.get("image", ""),
        category_id=data["category_id"],
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({
        "message": "Product created",
        "product": serialize_product(product),
    }), 201


def serialize_product(product):
    return {
        "id": product.id,
        "title": product.name,
        "name": product.name,
        "category": product.category.name if product.category else "",
        "category_id": product.category_id,
        "price": product.price,
        "rating": product.rating,
        "description": product.description or "",
        "image": product.image or "",
    }
