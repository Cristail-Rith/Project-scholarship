from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_name = db.Column(db.String(120), nullable=False, default="")
    product_image = db.Column(db.String(500), nullable=False, default="")

    product = db.relationship("Product", backref="order_items", lazy=True)

