"""
Tests for the /settings routes.
"""


def test_get_settings_returns_default_threshold(client, auth_headers):
    response = client.get("/api/settings", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["default_low_stock_threshold"] == 10


def test_update_settings_changes_threshold(client, auth_headers):
    response = client.put(
        "/api/settings",
        json={"default_low_stock_threshold": 25},
        headers=auth_headers,
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["default_low_stock_threshold"] == 25

    # Confirm it actually persisted
    get_response = client.get("/api/settings", headers=auth_headers)
    assert get_response.get_json()["data"]["default_low_stock_threshold"] == 25


def test_update_settings_rejects_negative_threshold(client, auth_headers):
    response = client.put(
        "/api/settings",
        json={"default_low_stock_threshold": -5},
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_settings_require_authentication(client):
    response = client.get("/api/settings")
    assert response.status_code == 401
