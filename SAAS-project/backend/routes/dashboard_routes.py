"""
Dashboard Routes

Provides a summary of the organization's inventory:
total products, total quantity, and low stock products.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required

from models.product import Product
from models.settings import Settings
from middleware.auth import get_current_user
from utils.helpers import success_response

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():
    """Return summary stats for the current organization."""
    current_user = get_current_user()
    organization_id = current_user.organization_id

    # Get this organization's default low stock threshold.
    # Fall back to 10 if a settings row somehow doesn't exist yet.
    settings = Settings.query.filter_by(organization_id=organization_id).first()
    default_threshold = settings.default_low_stock_threshold if settings else 10

    products = Product.query.filter_by(organization_id=organization_id).all()

    total_products = len(products)
    total_quantity = sum(p.quantity for p in products)

    # A product is "low stock" if its quantity is at or below its own
    # threshold, or the organization's default threshold if it has none set.
    low_stock_products = []
    for product in products:
        threshold = product.low_stock_threshold if product.low_stock_threshold is not None else default_threshold
        if product.quantity <= threshold:
            low_stock_products.append(product.to_dict())

    return success_response(
        data={
            "total_products": total_products,
            "total_quantity": total_quantity,
            "low_stock_count": len(low_stock_products),
            "low_stock_products": low_stock_products,
        }
    )
