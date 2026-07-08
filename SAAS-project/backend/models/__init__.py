"""
This file creates a single shared SQLAlchemy database object (db).

Every model file (user.py, organization.py, etc.) will import "db"
from here, so all models use the same database connection.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here so that db.create_all() knows about all of them.
# This must come after "db" is defined above, to avoid circular imports.
from models.organization import Organization
from models.user import User
from models.product import Product
from models.settings import Settings
