from app.extensions import db


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    preferred_date = db.Column(db.Date, nullable=True)
    guests = db.Column(db.Integer, nullable=False, default=2)
    message = db.Column(db.Text, nullable=False, default="")
    status = db.Column(db.String(20), nullable=False, default="new")
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
