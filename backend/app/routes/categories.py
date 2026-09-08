from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.category import Category

bp = Blueprint("categories", __name__)


@bp.get("/categories")
def get_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify([{"id": item.id, "name": item.name} for item in categories])


@bp.post("/categories")
def create_category():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"message": "name is required"}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({"message": "Category already exists"}), 409
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({"id": category.id, "name": category.name}), 201
