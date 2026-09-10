from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect, text
from app.config import Config
from app.extensions import db, migrate, jwt
from app.routes import auth, categories, contact, products, orders, tables
from app.models.contact_detail import ContactDetail
from app.models.category import Category


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(tables.bp)

    @app.get("/")
    def health_check():
        return {"message": "Restaurant API is running"}

    with app.app_context():
        db.create_all()
        ensure_product_columns()
        seed_categories()
        seed_contact_details()

    return app


def seed_contact_details():
    if ContactDetail.query.first():
        return

    details = [
        {
            "label": "Reservations",
            "details": "Recommended for dinner and weekend visits",
            "contact": "+1 234 567 8900",
            "contact_url": "tel:+12345678900",
            "sort_order": 1,
        },
        {
            "label": "General inquiries",
            "details": "Menu questions, dietary needs, and feedback",
            "contact": "hello@flavoria.com",
            "contact_url": "mailto:hello@flavoria.com",
            "sort_order": 2,
        },
        {
            "label": "Private events",
            "details": (
                "Intimate dinners, weddings, and corporate celebrations"
            ),
            "contact": "events@flavoria.com",
            "contact_url": "mailto:events@flavoria.com",
            "sort_order": 3,
        },
        {
            "label": "Location",
            "details": "123 Culinary Avenue, Gourmet District",
            "contact": "New York, NY 10001, USA",
            "sort_order": 4,
        },
        {
            "label": "Parking",
            "details": "Valet service available after 5:00 PM",
            "contact": "Street parking nearby",
            "sort_order": 5,
        },
        {
            "label": "Dress code",
            "details": "Smart casual",
            "contact": "Jackets welcome, never required",
            "sort_order": 6,
        },
    ]
    db.session.add_all(ContactDetail(**item) for item in details)
    db.session.commit()


def seed_categories():
    category_names = (
        "Starters", "Main Course", "Desserts", "Beverages", "Pizza"
    )
    existing_names = {category.name for category in Category.query.all()}
    missing_categories = [
        Category(name=name)
        for name in category_names
        if name not in existing_names
    ]
    if missing_categories:
        db.session.add_all(missing_categories)
        db.session.commit()


def ensure_product_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("products")
    }
    columns = {
        "sku": "VARCHAR(80) NOT NULL DEFAULT ''",
        "cost_price": "FLOAT NOT NULL DEFAULT 0",
        "stock_quantity": "INTEGER NOT NULL DEFAULT 0",
        "reorder_level": "INTEGER NOT NULL DEFAULT 5",
        "status": "VARCHAR(20) NOT NULL DEFAULT 'Out of Stock'",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE products ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()
