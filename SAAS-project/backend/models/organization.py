"""
Organization Model

Every user belongs to one organization. When a user signs up,
we automatically create a new organization for them.
"""

from models import db


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(150), nullable=False)

    # One organization can have many users and many products.
    # These let us do organization.users and organization.products
    users = db.relationship("User", backref="organization", lazy=True)
    products = db.relationship("Product", backref="organization", lazy=True)

    def to_dict(self):
        """Convert this organization into a plain dictionary (for JSON responses)."""
        return {
            "id": self.id,
            "organization_name": self.organization_name,
        }
