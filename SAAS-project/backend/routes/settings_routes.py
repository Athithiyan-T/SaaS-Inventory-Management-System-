"""
Settings Routes

Lets a user view and update their organization's default
low stock threshold.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from models import db
from models.settings import Settings
from middleware.auth import get_current_user
from utils.helpers import success_response, error_response

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET"])
@jwt_required()
def get_settings():
    """Get the current organization's settings."""
    current_user = get_current_user()

    settings = Settings.query.filter_by(organization_id=current_user.organization_id).first()

    # Safety net: if a settings row is somehow missing, create a default one now.
    if not settings:
        settings = Settings(
            organization_id=current_user.organization_id,
            default_low_stock_threshold=10,
        )
        db.session.add(settings)
        db.session.commit()

    return success_response(data=settings.to_dict())


@settings_bp.route("/settings", methods=["PUT"])
@jwt_required()
def update_settings():
    """Update the current organization's default low stock threshold."""
    current_user = get_current_user()
    data = request.get_json()

    if not data or "default_low_stock_threshold" not in data:
        return error_response("default_low_stock_threshold is required.", 400)

    new_threshold = data.get("default_low_stock_threshold")

    # Basic validation: must be a whole number, zero or more
    if not isinstance(new_threshold, int) or new_threshold < 0:
        return error_response("default_low_stock_threshold must be a whole number of 0 or more.", 400)

    settings = Settings.query.filter_by(organization_id=current_user.organization_id).first()

    if not settings:
        settings = Settings(organization_id=current_user.organization_id)
        db.session.add(settings)

    settings.default_low_stock_threshold = new_threshold
    db.session.commit()

    return success_response(data=settings.to_dict(), message="Settings updated successfully.")
