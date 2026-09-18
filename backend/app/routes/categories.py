import os
import uuid

from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.category import Category

bp = Blueprint("categories", __name__)
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "uploads",
    "categories",
)
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


@bp.get("/uploads/categories/<path:filename>")
def category_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@bp.get("/categories")
def get_categories():
    station = request.args.get("station", "All")
    query = Category.query.order_by(Category.display_order, Category.name)
    if station and station != "All":
        query = query.filter_by(station=station)
    categories = query.all()
    return jsonify([serialize_category(c) for c in categories]), 200


@bp.get("/categories/<int:category_id>")
def get_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    return jsonify(serialize_category(category)), 200


@bp.post("/categories", strict_slashes=False)
def create_category():
    data = (
        request.form.to_dict()
        if request.files
        else (request.get_json(silent=True) or {})
    )
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({"message": "Category already exists"}), 409

    image_file = request.files.get("image")
    image = save_uploaded_image(image_file) if image_file else ""
    if image is None:
        return jsonify({
            "message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"
        }), 400
    if image == "" and data.get("image"):
        image = str(data.get("image", "")).strip()

    category = Category(
        name=name,
        slug=data.get("slug") or slugify(name),
        description=str(data.get("description", "")).strip(),
        image=image,
        icon=str(data.get("icon", "utensils")).strip() or "utensils",
        station=data.get("station") or "Main Line",
        status=data.get("status") or "Active",
        display_order=max(get_next_display_order(), 1),
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(serialize_category(category)), 201


@bp.put("/categories/<int:category_id>", strict_slashes=False)
def update_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404

    data = (
        request.form.to_dict()
        if request.files
        else (request.get_json(silent=True) or {})
    )
    name = str(data.get("name", category.name)).strip()
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if name != category.name and Category.query.filter_by(name=name).first():
        return jsonify({"message": "Category already exists"}), 409

    if "name" in data:
        category.name = name
    if "slug" in data:
        category.slug = str(data["slug"]).strip() or slugify(category.name)
    if "description" in data:
        category.description = str(data.get("description", "")).strip()
    if "icon" in data:
        category.icon = str(data.get("icon", "utensils")).strip() or "utensils"
    if "station" in data:
        category.station = str(data["station"])
    if "status" in data:
        category.status = str(data["status"])
    if "display_order" in data:
        category.display_order = int(data["display_order"])

    image_file = request.files.get("image")
    if image_file:
        saved = save_uploaded_image(image_file)
        if saved is None:
            return jsonify({
                "message": "Use a JPG, PNG, WEBP, or GIF image under 5 MB"
            }), 400
        category.image = saved
    elif "image" in data:
        category.image = str(data.get("image", "")).strip()

    db.session.commit()
    return jsonify(serialize_category(category)), 200


@bp.delete("/categories/<int:category_id>")
def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


def serialize_category(cat):
    return {
        "id": cat.id,
        "name": cat.name,
        "slug": cat.slug,
        "description": cat.description or "",
        "image": cat.image or "",
        "icon": cat.icon or "utensils",
        "station": cat.station,
        "status": cat.status,
        "displayOrder": cat.display_order,
        "itemCount": len(cat.products),
    }


def slugify(text):
    return text.lower().replace(" ", "-").replace("&", "and").replace("/", "-")


def get_next_display_order():
    last = Category.query.order_by(db.desc(Category.display_order)).first()
    return (last.display_order + 1) if last else 1


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
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    return f"/uploads/categories/{filename}"
