"""
Settings Model

Stores organization-wide settings. Right now this is just the
default low stock threshold, used when a product doesn't have
its own threshold set.
"""

from models import db


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False, unique=True)

    default_low_stock_threshold = db.Column(db.Integer, nullable=False, default=10)

    def to_dict(self):
        """Convert this settings row into a plain dictionary (for JSON responses)."""
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "default_low_stock_threshold": self.default_low_stock_threshold,
        }
