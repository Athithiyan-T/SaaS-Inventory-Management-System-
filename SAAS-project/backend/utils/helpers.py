"""
Helpers

Small reusable functions used across different route files.
"""

from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    """Build a consistent success JSON response."""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(message="Something went wrong", status_code=400):
    """Build a consistent error JSON response."""
    return jsonify({"success": False, "message": message}), status_code
