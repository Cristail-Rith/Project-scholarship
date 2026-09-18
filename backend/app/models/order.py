from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending")
    order_type = db.Column(db.String(20), nullable=False, default="dine-in")
    payment_method = db.Column(db.String(20), nullable=False, default="cash")
    delivery_fee = db.Column(db.Float, nullable=False, default=0)
    notes = db.Column(db.Text, nullable=True)
    customer_name = db.Column(db.String(160), nullable=True)
    customer_email = db.Column(db.String(120), nullable=True)
    customer_phone = db.Column(db.String(40), nullable=True)
    table_number = db.Column(db.String(20), nullable=True)
    delivery_address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", lazy=True)

