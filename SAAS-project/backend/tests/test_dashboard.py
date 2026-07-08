"""
Tests for the /dashboard summary endpoint.
"""


def test_dashboard_totals_with_no_products(client, auth_headers):
    response = client.get("/api/dashboard", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["total_products"] == 0
    assert body["data"]["total_quantity"] == 0
    assert body["data"]["low_stock_count"] == 0


def test_dashboard_calculates_totals_and_low_stock(client, auth_headers):
    # Product with its own threshold, currently low on stock (2 <= 5)
    client.post(
        "/api/products",
        json={"name": "Low Stock Item", "sku": "LOW-1", "quantity": 2, "low_stock_threshold": 5},
        headers=auth_headers,
    )

    # Product with plenty of stock, above its threshold
    client.post(
        "/api/products",
        json={"name": "Healthy Item", "sku": "HEALTHY-1", "quantity": 100, "low_stock_threshold": 5},
        headers=auth_headers,
    )

    response = client.get("/api/dashboard", headers=auth_headers)
    body = response.get_json()["data"]

    assert body["total_products"] == 2
    assert body["total_quantity"] == 102
    assert body["low_stock_count"] == 1
    assert body["low_stock_products"][0]["sku"] == "LOW-1"


def test_dashboard_uses_default_threshold_when_product_has_none(client, auth_headers):
    # Lower the organization's default threshold to 3
    client.put("/api/settings", json={"default_low_stock_threshold": 3}, headers=auth_headers)

    # Product has no threshold of its own, quantity 3 should count as low stock
    client.post(
        "/api/products",
        json={"name": "No Threshold Item", "sku": "NOTHRESH-1", "quantity": 3},
        headers=auth_headers,
    )

    response = client.get("/api/dashboard", headers=auth_headers)
    body = response.get_json()["data"]

    assert body["low_stock_count"] == 1
