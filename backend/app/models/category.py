from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, default="")
    description = db.Column(db.Text, nullable=False, default="")
    image = db.Column(db.String(500), nullable=False, default="")
    icon = db.Column(db.String(40), nullable=False, default="utensils")
    station = db.Column(db.String(80), nullable=False, default="Main Line")
    status = db.Column(db.String(20), nullable=False, default="Active")
    display_order = db.Column(db.Integer, nullable=False, default=1)

    products = db.relationship("Product", backref="category", lazy=True)
