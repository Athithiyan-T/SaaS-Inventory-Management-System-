"""
Tests for the product routes: create, read, update, delete, search.
"""


def test_create_product_succeeds(client, auth_headers):
    response = client.post(
        "/api/products",
        json={"name": "Widget", "sku": "WID-1", "quantity": 5},
        headers=auth_headers,
    )

    body = response.get_json()
    assert response.status_code == 201
    assert body["data"]["name"] == "Widget"
    assert body["data"]["sku"] == "WID-1"


def test_create_product_without_name_fails(client, auth_headers):
    response = client.post(
        "/api/products",
        json={"sku": "NO-NAME-1"},
        headers=auth_headers,
    )

    assert response.status_code == 400


def test_duplicate_sku_within_same_org_fails(client, auth_headers):
    client.post(
        "/api/products",
        json={"name": "Widget", "sku": "DUPLICATE-SKU"},
        headers=auth_headers,
    )

    response = client.post(
        "/api/products",
        json={"name": "Another Widget", "sku": "DUPLICATE-SKU"},
        headers=auth_headers,
    )

    assert response.status_code == 409


def test_get_products_returns_only_current_org_products(client, auth_headers):
    client.post(
        "/api/products",
        json={"name": "Gadget", "sku": "GAD-1"},
        headers=auth_headers,
    )

    response = client.get("/api/products", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["data"]) == 1
    assert body["data"][0]["sku"] == "GAD-1"


def test_search_products_by_name(client, auth_headers):
    client.post("/api/products", json={"name": "Blue Pen", "sku": "PEN-1"}, headers=auth_headers)
    client.post("/api/products", json={"name": "Red Marker", "sku": "MARK-1"}, headers=auth_headers)

    response = client.get("/api/products?search=pen", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Blue Pen"


def test_update_product_changes_fields(client, auth_headers):
    create_response = client.post(
        "/api/products",
        json={"name": "Old Name", "sku": "UPD-1", "quantity": 2},
        headers=auth_headers,
    )
    product_id = create_response.get_json()["data"]["id"]

    response = client.put(
        f"/api/products/{product_id}",
        json={"name": "New Name", "quantity": 20},
        headers=auth_headers,
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["name"] == "New Name"
    assert body["data"]["quantity"] == 20


def test_delete_product_removes_it(client, auth_headers):
    create_response = client.post(
        "/api/products",
        json={"name": "To Delete", "sku": "DEL-1"},
        headers=auth_headers,
    )
    product_id = create_response.get_json()["data"]["id"]

    delete_response = client.delete(f"/api/products/{product_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_products_require_authentication(client):
    response = client.get("/api/products")
    assert response.status_code == 401
