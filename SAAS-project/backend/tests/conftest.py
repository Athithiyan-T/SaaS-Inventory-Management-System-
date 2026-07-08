"""
Shared pytest fixtures.

Every test gets a fresh Flask app connected to a brand new
in-memory SQLite database, so tests never interfere with each
other or with your real database.db file.
"""

import pytest

from app import create_app
from models import db


@pytest.fixture
def app():
    """Create a Flask app configured for testing."""
    test_app = create_app(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
        }
    )

    yield test_app

    # Clean up all tables after each test
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client we can use to make fake requests to our app."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """
    Signs up a brand new test user and returns headers with a valid
    JWT token, ready to use on any protected route.
    """
    response = client.post(
        "/api/signup",
        json={
            "email": "tester@example.com",
            "password": "password123",
            "organization_name": "Test Organization",
        },
    )
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
