from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect, text
from app.config import Config
from app.extensions import db, migrate, jwt
from app.routes import auth, categories, contact, products, orders, tables
from app.routes import reservations
from app.models.contact_detail import ContactDetail
from app.models.category import Category
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant_table import RestaurantTable


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
    app.register_blueprint(reservations.bp)
    app.register_blueprint(tables.bp)

    @app.get("/")
    def health_check():
        return {"message": "Restaurant API is running"}

    with app.app_context():
        db.create_all()
        ensure_category_columns()
        ensure_product_columns()
        ensure_order_columns()
        ensure_order_item_columns()
        ensure_order_item_product_id_nullable()
        ensure_reservation_columns()
        ensure_table_columns()
        ensure_user_columns()
        seed_categories()
        seed_tables()
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
        "Starters", "Main Course", "Desserts", "Beverages", "Pizza",
        "Chef Specials"
    )
    existing_names = {category.name for category in Category.query.all()}
    missing_categories = [
        Category(
            name=name,
            slug=name.lower().replace(" ", "-").replace("&", "and"),
            station="Main Line",
            status="Active",
            display_order=idx + 1,
        )
        for idx, name in enumerate(category_names)
        if name not in existing_names
    ]
    if missing_categories:
        db.session.add_all(missing_categories)
        db.session.commit()

    # Backfill slugs for legacy categories
    for category in Category.query.all():
        if not category.slug:
            category.slug = (
                category.name.lower().replace(" ", "-").replace("&", "and")
            )
    db.session.commit()


def seed_tables():
    if RestaurantTable.query.first():
        return

    tables = [
        RestaurantTable(table_number=1, seats=2, status="available", zone="Main Dining", shape="round", bg_image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=2, seats=4, status="occupied", zone="Main Dining", shape="square", bg_image="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=3, seats=4, status="occupied", zone="Main Dining", shape="square", bg_image="https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=4, seats=6, status="reserved", zone="Main Dining", shape="long", bg_image="https://images.unsplash.com/photo-1544161515-4ab6ce6db874?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=5, seats=2, status="cleaning", zone="Main Dining", shape="round", bg_image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=101, seats=8, status="reserved", zone="VIP Lounge", shape="long", bg_image="https://images.unsplash.com/photo-1578474846511-04ba529f0b88?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=102, seats=12, status="occupied", zone="VIP Lounge", shape="long", bg_image="https://images.unsplash.com/photo-1578474846511-04ba529f0b88?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=201, seats=4, status="available", zone="Terrace", shape="square", bg_image="https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=202, seats=4, status="available", zone="Terrace", shape="square", bg_image="https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=301, seats=2, status="available", zone="Bar", shape="round", bg_image="https://images.unsplash.com/photo-1514933651103-005eec06c4b?q=80&w=800&auto=format&fit=crop"),
    ]
    db.session.add_all(tables)
    db.session.commit()


def ensure_category_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("categories")
    }
    columns = {
        "slug": "VARCHAR(120) NOT NULL DEFAULT ''",
        "description": "TEXT NOT NULL DEFAULT ''",
        "image": "VARCHAR(500) NOT NULL DEFAULT ''",
        "icon": "VARCHAR(40) NOT NULL DEFAULT 'utensils'",
        "station": "VARCHAR(80) NOT NULL DEFAULT 'Main Line'",
        "status": "VARCHAR(20) NOT NULL DEFAULT 'Active'",
        "display_order": "INTEGER NOT NULL DEFAULT 1",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE categories ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_product_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("products")
    }
    columns = {
        "sku": "VARCHAR(80) NOT NULL DEFAULT ''",
        "previous_price": "FLOAT NULL",
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


def ensure_order_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("orders")
    }
    columns = {
        "order_type": "VARCHAR(20) NOT NULL DEFAULT 'dine-in'",
        "payment_method": "VARCHAR(20) NOT NULL DEFAULT 'cash'",
        "delivery_fee": "FLOAT NOT NULL DEFAULT 0",
        "notes": "TEXT NULL",
        "customer_name": "VARCHAR(160) NULL",
        "customer_email": "VARCHAR(120) NULL",
        "customer_phone": "VARCHAR(40) NULL",
        "table_number": "VARCHAR(20) NULL",
        "delivery_address": "VARCHAR(255) NULL",
        "created_at": "DATETIME NULL",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE orders ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.execute(
            text("UPDATE orders SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
        )
        db.session.commit()


def ensure_order_item_product_id_nullable():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("order_items")
    }
    if "product_id" not in existing_columns:
        return
    cols = inspect(db.engine).get_columns("order_items")
    for col in cols:
        if col["name"] == "product_id" and col.get("nullable", False):
            return
    dialect = db.engine.dialect.name
    if dialect == "postgresql":
        db.session.execute(text("ALTER TABLE order_items ALTER COLUMN product_id DROP NOT NULL"))
        db.session.commit()
    elif dialect == "mysql":
        db.session.execute(text("ALTER TABLE order_items MODIFY COLUMN product_id INT NULL"))
        db.session.commit()
    elif dialect == "sqlite":
        db.session.execute(text(
            "CREATE TABLE _order_items_new ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "order_id INTEGER NOT NULL REFERENCES orders(id), "
            "product_id INTEGER REFERENCES products(id), "
            "quantity INTEGER NOT NULL, "
            "price FLOAT NOT NULL, "
            "product_name VARCHAR(120) NOT NULL DEFAULT '', "
            "product_image VARCHAR(500) NOT NULL DEFAULT ''"
            ")"
        ))
        db.session.execute(text(
            "INSERT INTO _order_items_new (id, order_id, product_id, quantity, price, product_name, product_image) "
            "SELECT id, order_id, product_id, quantity, price, product_name, product_image FROM order_items"
        ))
        db.session.execute(text("DROP TABLE order_items"))
        db.session.execute(text("ALTER TABLE _order_items_new RENAME TO order_items"))
        db.session.commit()


def ensure_order_item_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("order_items")
    }
    columns = {
        "product_name": "VARCHAR(120) NOT NULL DEFAULT ''",
        "product_image": "VARCHAR(500) NOT NULL DEFAULT ''",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE order_items ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_reservation_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("reservations")
    }
    columns = {
        "guest_name": "VARCHAR(160) NULL",
        "guest_email": "VARCHAR(120) NULL",
        "guest_phone": "VARCHAR(40) NULL",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE reservations ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_table_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("restaurant_tables")
    }
    columns = {
        "zone": "VARCHAR(40) NOT NULL DEFAULT 'Main Dining'",
        "shape": "VARCHAR(20) NOT NULL DEFAULT 'square'",
        "bg_image": "VARCHAR(500) NOT NULL DEFAULT ''",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE restaurant_tables ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_user_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("users")
    }
    columns = {
        "phone": "VARCHAR(20) NULL",
        "avatar": "VARCHAR(500) NULL",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE users ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()
