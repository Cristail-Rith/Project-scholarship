from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.String(10), nullable=False, default="0.0")
    image = db.Column(db.String(500), nullable=False, default="")
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )
    sku = db.Column(db.String(80), nullable=False, default="")
    cost_price = db.Column(db.Float, nullable=False, default=0)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=5)
    status = db.Column(db.String(20), nullable=False, default="Out of Stock")
