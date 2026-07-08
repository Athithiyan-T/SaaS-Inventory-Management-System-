"""
Auth Middleware

A small helper used by protected routes to fetch the currently
logged-in user based on their JWT token.
"""

from flask_jwt_extended import get_jwt_identity
from models import db
from models.user import User


def get_current_user():
    """
    Reads the user id stored inside the JWT token and fetches
    that user from the database. Must be called from inside a
    route that is decorated with @jwt_required().
    """
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return db.session.get(User, int(user_id))
