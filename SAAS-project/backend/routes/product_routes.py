"""
Product Routes

Handles creating, reading, updating, deleting, and searching
inventory products. Every route here is scoped to the logged-in
user's organization, so users never see another organization's data.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from models import db
from models.product import Product
from middleware.auth import get_current_user
from utils.validators import validate_product_data
from utils.helpers import success_response, error_response

product_bp = Blueprint("products", __name__)


@product_bp.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    """
    Get all products for the current organization.
    Supports optional search via ?search=<text>, matching name or SKU.
    """
    current_user = get_current_user()
    search_term = request.args.get("search", "").strip()

    query = Product.query.filter_by(organization_id=current_user.organization_id)

    if search_term:
        like_pattern = f"%{search_term}%"
        query = query.filter(
            db.or_(
                Product.name.ilike(like_pattern),
                Product.sku.ilike(like_pattern),
            )
        )

    products = query.order_by(Product.created_at.desc()).all()

    return success_response(data=[p.to_dict() for p in products])


@product_bp.route("/products/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    """Get a single product by id, only if it belongs to the current organization."""
    current_user = get_current_user()

    product = Product.query.filter_by(
        id=product_id, organization_id=current_user.organization_id
    ).first()

    if not product:
        return error_response("Product not found.", 404)

    return success_response(data=product.to_dict())


@product_bp.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    """Create a new product under the current organization."""
    current_user = get_current_user()
    data = request.get_json()

    # Step 1: Validate basic fields
    error = validate_product_data(data)
    if error:
        return error_response(error, 400)

    name = data.get("name").strip()
    sku = data.get("sku").strip()

    # Step 2: Make sure the SKU is unique within this organization
    existing_product = Product.query.filter_by(
        organization_id=current_user.organization_id, sku=sku
    ).first()
    if existing_product:
        return error_response("A product with this SKU already exists.", 409)

    # Step 3: Create the product
    new_product = Product(
        organization_id=current_user.organization_id,
        name=name,
        sku=sku,
        description=data.get("description", ""),
        quantity=data.get("quantity", 0) or 0,
        cost_price=data.get("cost_price", 0) or 0,
        selling_price=data.get("selling_price", 0) or 0,
        low_stock_threshold=data.get("low_stock_threshold"),  # can be None, that's fine
    )

    db.session.add(new_product)
    db.session.commit()

    return success_response(
        data=new_product.to_dict(),
        message="Product created successfully.",
        status_code=201,
    )


@product_bp.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    """Update an existing product, only if it belongs to the current organization."""
    current_user = get_current_user()
    data = request.get_json()

    product = Product.query.filter_by(
        id=product_id, organization_id=current_user.organization_id
    ).first()

    if not product:
        return error_response("Product not found.", 404)

    # Step 1: Validate fields that were provided
    error = validate_product_data(data, is_update=True)
    if error:
        return error_response(error, 400)

    # Step 2: If SKU is being changed, make sure the new SKU is still unique
    new_sku = data.get("sku")
    if new_sku and new_sku.strip() != product.sku:
        duplicate = Product.query.filter_by(
            organization_id=current_user.organization_id, sku=new_sku.strip()
        ).first()
        if duplicate:
            return error_response("A product with this SKU already exists.", 409)
        product.sku = new_sku.strip()

    # Step 3: Update only the fields that were provided
    if "name" in data:
        product.name = data.get("name").strip()
    if "description" in data:
        product.description = data.get("description")
    if "quantity" in data:
        product.quantity = data.get("quantity") or 0
    if "cost_price" in data:
        product.cost_price = data.get("cost_price") or 0
    if "selling_price" in data:
        product.selling_price = data.get("selling_price") or 0
    if "low_stock_threshold" in data:
        product.low_stock_threshold = data.get("low_stock_threshold")

    db.session.commit()

    return success_response(data=product.to_dict(), message="Product updated successfully.")


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    """Delete a product, only if it belongs to the current organization."""
    current_user = get_current_user()

    product = Product.query.filter_by(
        id=product_id, organization_id=current_user.organization_id
    ).first()

    if not product:
        return error_response("Product not found.", 404)

    db.session.delete(product)
    db.session.commit()

    return success_response(message="Product deleted successfully.")
