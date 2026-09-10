import os
import uuid
from functools import wraps

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.product import Product
from app.models.category import Category

bp = Blueprint("products", __name__)
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


def admin_required(view):
    @wraps(view)
    @jwt_required()
    def wrapped(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return view(*args, **kwargs)

    return wrapped


@bp.get("/uploads/products/<path:filename>")
def product_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([serialize_product(product) for product in products]), 200


@bp.route("/products", methods=["POST"])
@admin_required
def create_product():
    data = (
        request.form.to_dict()
        if request.form
        else (request.get_json(silent=True) or {})
    )
    required = ("name", "price", "category_id", "sku")
    if any(field not in data for field in required):
        return jsonify({
            "message": "name, price, and category_id are required"
        }), 400
    image_file = request.files.get("image")
    image = (
        save_uploaded_image(image_file)
        if image_file
        else str(data.get("image", "")).strip()
    )
    if image is None:
        return jsonify({
            "message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"
        }), 400
    category = db.session.get(Category, data["category_id"])
    if not category:
        return jsonify({"message": "Category not found"}), 400

    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        rating=str(data.get("rating", "0.0")),
        image=image,
        category_id=data["category_id"],
        sku=data["sku"],
        cost_price=data.get("cost_price", 0),
        stock_quantity=data.get("stock_quantity", 0),
        reorder_level=data.get("reorder_level", 5),
        status=data.get(
            "status",
            determine_status(
                data.get("stock_quantity", 0), data.get("reorder_level", 5)
            ),
        ),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({
        "message": "Product created",
        "product": serialize_product(product),
    }), 201


@bp.route("/products/<int:product_id>", methods=["PUT"])
@admin_required
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = (
        request.form.to_dict()
        if request.form
        else (request.get_json(silent=True) or {})
    )
    uploaded_image = request.files.get("image")
    image = (
        save_uploaded_image(uploaded_image)
        if uploaded_image
        else str(data.get("image", product.image or "")).strip()
    )
    if uploaded_image and image is None:
        return jsonify({
            "message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"
        }), 400
    if (
        "category_id" in data
        and not db.session.get(Category, data["category_id"])
    ):
        return jsonify({"message": "Category not found"}), 400

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description or "")
    product.price = data.get("price", product.price)
    product.rating = str(data.get("rating", product.rating))
    product.image = image
    product.sku = data.get("sku", product.sku)
    product.cost_price = data.get("cost_price", product.cost_price)
    product.stock_quantity = data.get("stock_quantity", product.stock_quantity)
    product.reorder_level = data.get("reorder_level", product.reorder_level)
    product.status = data.get(
        "status",
        determine_status(product.stock_quantity, product.reorder_level),
    )
    if "category_id" in data:
        product.category_id = data["category_id"]
    db.session.commit()
    return jsonify({
        "message": "Product updated",
        "product": serialize_product(product),
    })


@bp.route("/products/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


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
        "sku": product.sku or f"PRD-{product.id}",
        "costPrice": product.cost_price,
        "stockQuantity": product.stock_quantity,
        "reorderLevel": product.reorder_level,
        "status": product.status,
    }


def determine_status(stock_quantity, reorder_level):
    stock = int(stock_quantity or 0)
    reorder = int(reorder_level or 0)
    if stock <= 0:
        return "Out of Stock"
    if stock <= reorder:
        return "Low Stock"
    return "In Stock"


def save_uploaded_image(image_file):
    if not image_file or not image_file.filename:
        return ""
    original_name = secure_filename(image_file.filename)
    extension = (
        original_name.rsplit(".", 1)[-1].lower()
        if "." in original_name
        else ""
    )
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    image_file.save(os.path.join(upload_folder, filename))
    return f"/uploads/products/{filename}"
