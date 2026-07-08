"""
Validators

Small helper functions to check if user input is valid,
before we try to save anything to the database.
"""

import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    """Return True if the email looks like a real email address."""
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email))


def validate_signup_data(data):
    """
    Check that signup data has everything we need.
    Returns an error message string, or None if everything is valid.
    """
    if not data:
        return "Request body is missing."

    email = data.get("email")
    password = data.get("password")
    organization_name = data.get("organization_name")

    if not organization_name or not organization_name.strip():
        return "Organization name is required."

    if not email or not email.strip():
        return "Email is required."

    if not is_valid_email(email):
        return "Please enter a valid email address."

    if not password or len(password) < 6:
        return "Password must be at least 6 characters long."

    return None


def validate_login_data(data):
    """
    Check that login data has everything we need.
    Returns an error message string, or None if everything is valid.
    """
    if not data:
        return "Request body is missing."

    email = data.get("email")
    password = data.get("password")

    if not email or not email.strip():
        return "Email is required."

    if not password:
        return "Password is required."

    return None


def validate_product_data(data, is_update=False):
    """
    Check that product data has everything we need.
    Returns an error message string, or None if everything is valid.
    """
    if not data:
        return "Request body is missing."

    name = data.get("name")
    sku = data.get("sku")

    # On create, name and sku are required.
    # On update, they are only checked if provided.
    if not is_update:
        if not name or not name.strip():
            return "Product name is required."
        if not sku or not sku.strip():
            return "SKU is required."
    else:
        if "name" in data and not str(data.get("name")).strip():
            return "Product name cannot be empty."
        if "sku" in data and not str(data.get("sku")).strip():
            return "SKU cannot be empty."

    return None
