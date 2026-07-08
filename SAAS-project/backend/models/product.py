"""
Product Model

Stores each inventory item that belongs to an organization.
"""

from datetime import datetime, timezone
from models import db


def _utcnow():
    """Small helper so every timestamp in this model uses the same clock."""
    return datetime.now(timezone.utc)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    sku = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    quantity = db.Column(db.Integer, nullable=False, default=0)
    cost_price = db.Column(db.Float, nullable=False, default=0.0)
    selling_price = db.Column(db.Float, nullable=False, default=0.0)

    # If this is empty (None), the organization's default threshold is used instead
    low_stock_threshold = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        """Convert this product into a plain dictionary (for JSON responses)."""
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description,
            "quantity": self.quantity,
            "cost_price": self.cost_price,
            "selling_price": self.selling_price,
            "low_stock_threshold": self.low_stock_threshold,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
