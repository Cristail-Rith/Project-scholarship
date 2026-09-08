from flask import Blueprint, jsonify

from app.models.contact_detail import ContactDetail

bp = Blueprint("contact", __name__)


@bp.get("/contact-info")
def get_contact_info():
    details = ContactDetail.query.order_by(ContactDetail.sort_order).all()
    return jsonify([
        {
            "id": item.id,
            "label": item.label,
            "details": item.details,
            "contact": item.contact,
            "contact_url": item.contact_url,
        }
        for item in details
    ])
