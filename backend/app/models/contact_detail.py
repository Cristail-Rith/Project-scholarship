from app.extensions import db


class ContactDetail(db.Model):
    __tablename__ = "contact_details"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    contact_url = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, nullable=False, default=0)
