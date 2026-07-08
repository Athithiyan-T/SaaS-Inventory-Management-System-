"""
User Model

Stores login details for each user. Passwords are never stored
as plain text - we always hash them first using werkzeug.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from models import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Links this user to the organization they belong to
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    def set_password(self, plain_password):
        """Hash the given password and store it."""
        self.password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        """Check if the given password matches the stored hash."""
        return check_password_hash(self.password, plain_password)

    def to_dict(self):
        """Convert this user into a plain dictionary (for JSON responses)."""
        return {
            "id": self.id,
            "email": self.email,
            "organization_id": self.organization_id,
        }
