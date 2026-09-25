from app.extensions import db


class EventInquiry(db.Model):
    __tablename__ = "event_inquiries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    preferred_space = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=False, default="")
    status = db.Column(db.String(20), nullable=False, default="new")
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
