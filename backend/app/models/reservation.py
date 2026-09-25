from app.extensions import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    table_id = db.Column(
        db.Integer, db.ForeignKey("restaurant_tables.id"), nullable=True
    )
    reserved_for = db.Column(db.DateTime, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    booking_type = db.Column(db.String(20), nullable=False, default="dining")
    area_name = db.Column(db.String(100), nullable=False, default="Main Dining Room")
    occasion = db.Column(db.String(100), nullable=False, default="Casual Fine Dining")
    dietary_preferences = db.Column(db.String(500), nullable=False, default="[]")
    notes = db.Column(db.Text)
    guest_name = db.Column(db.String(160), nullable=True)
    guest_email = db.Column(db.String(120), nullable=True)
    guest_phone = db.Column(db.String(40), nullable=True)
