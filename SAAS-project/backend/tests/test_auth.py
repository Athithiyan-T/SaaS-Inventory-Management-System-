"""
Tests for the authentication routes: /signup, /login, /logout
"""


def test_signup_creates_organization_and_user(client):
    response = client.post(
        "/api/signup",
        json={
            "email": "new@example.com",
            "password": "password123",
            "organization_name": "New Org",
        },
    )

    body = response.get_json()
    assert response.status_code == 201
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert body["data"]["user"]["email"] == "new@example.com"
    assert body["data"]["organization"]["organization_name"] == "New Org"


def test_signup_with_duplicate_email_fails(client):
    # First signup should succeed
    client.post(
        "/api/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "organization_name": "Org One",
        },
    )

    # Second signup with the same email should fail
    response = client.post(
        "/api/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "organization_name": "Org Two",
        },
    )

    assert response.status_code == 409
    assert response.get_json()["success"] is False


def test_signup_missing_password_fails(client):
    response = client.post(
        "/api/signup",
        json={"email": "missing@example.com", "organization_name": "Org"},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_login_with_correct_credentials_succeeds(client):
    client.post(
        "/api/signup",
        json={
            "email": "login@example.com",
            "password": "password123",
            "organization_name": "Login Org",
        },
    )

    response = client.post(
        "/api/login",
        json={"email": "login@example.com", "password": "password123"},
    )

    body = response.get_json()
    assert response.status_code == 200
    assert "access_token" in body["data"]


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/signup",
        json={
            "email": "wrongpass@example.com",
            "password": "password123",
            "organization_name": "Org",
        },
    )

    response = client.post(
        "/api/login",
        json={"email": "wrongpass@example.com", "password": "notmypassword"},
    )

    assert response.status_code == 401


def test_logout_requires_valid_token(client):
    # No Authorization header at all -> should be rejected
    response = client.post("/api/logout")
    assert response.status_code == 401


def test_logout_with_valid_token_succeeds(client, auth_headers):
    response = client.post("/api/logout", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()["success"] is True
