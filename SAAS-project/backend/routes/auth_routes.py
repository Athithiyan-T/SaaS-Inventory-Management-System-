"""
Auth Routes

Handles user signup, login, and logout.
Signup creates a new Organization + User + default Settings.
"""

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required

from models import db
from models.user import User
from models.organization import Organization
from models.settings import Settings
from utils.validators import validate_signup_data, validate_login_data
from utils.helpers import success_response, error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Create a new organization and user account, then log them in."""
    data = request.get_json()

    # Step 1: Validate the incoming data
    error = validate_signup_data(data)
    if error:
        return error_response(error, 400)

    email = data.get("email").strip().lower()
    password = data.get("password")
    organization_name = data.get("organization_name").strip()

    # Step 2: Make sure this email isn't already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return error_response("An account with this email already exists.", 409)

    # Step 3: Create the organization first
    new_organization = Organization(organization_name=organization_name)
    db.session.add(new_organization)
    db.session.flush()  # lets us access new_organization.id before committing

    # Step 4: Create default settings for this new organization
    new_settings = Settings(
        organization_id=new_organization.id,
        default_low_stock_threshold=10,
    )
    db.session.add(new_settings)

    # Step 5: Create the user, linked to the new organization
    new_user = User(email=email, organization_id=new_organization.id)
    new_user.set_password(password)
    db.session.add(new_user)

    # Step 6: Save everything to the database
    db.session.commit()

    # Step 7: Log the user in immediately by issuing a JWT token
    access_token = create_access_token(identity=str(new_user.id))

    return success_response(
        data={
            "access_token": access_token,
            "user": new_user.to_dict(),
            "organization": new_organization.to_dict(),
        },
        message="Account created successfully.",
        status_code=201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log an existing user in and return a JWT token."""
    data = request.get_json()

    # Step 1: Validate the incoming data
    error = validate_login_data(data)
    if error:
        return error_response(error, 400)

    email = data.get("email").strip().lower()
    password = data.get("password")

    # Step 2: Find the user by email
    user = User.query.filter_by(email=email).first()

    # Step 3: Check the user exists and the password is correct
    if not user or not user.check_password(password):
        return error_response("Invalid email or password.", 401)

    # Step 4: Issue a JWT token
    access_token = create_access_token(identity=str(user.id))

    return success_response(
        data={
            "access_token": access_token,
            "user": user.to_dict(),
        },
        message="Logged in successfully.",
    )


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Log the user out.

    Since we use stateless JWT tokens, there's nothing to delete on
    the server. The frontend simply removes the token from storage.
    This endpoint mainly confirms the token was valid.
    """
    return success_response(message="Logged out successfully.")
