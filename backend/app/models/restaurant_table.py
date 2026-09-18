from app.extensions import db


class RestaurantTable(db.Model):
    __tablename__ = "restaurant_tables"

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False, default=2)
    status = db.Column(db.String(20), nullable=False, default="available")
    zone = db.Column(db.String(40), nullable=False, default="Main Dining")
    shape = db.Column(db.String(20), nullable=False, default="square")
    bg_image = db.Column(db.String(500), nullable=False, default="")

    reservations = db.relationship("Reservation", backref="table", lazy=True)
