def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_product(client):
    product_data = {
        "name": "Integration Test Product",
        "description": "Testing product creation",
        "price": 499.99,
        "quantity": 10,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    response = client.post("/api/v1/products", json=product_data)

    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["quantity"] == 10
    assert "id" in response.json()


def test_get_product(client):
    product_data = {
        "name": "Get Test Product",
        "description": "Testing get product",
        "price": 299.99,
        "quantity": 5,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    create_response = client.post("/api/v1/products", json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_update_product(client):
    product_data = {
        "name": "Update Test Product",
        "description": "Before update",
        "price": 500,
        "quantity": 10,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    create_response = client.post("/api/v1/products", json=product_data)
    product_id = create_response.json()["id"]

    updated_data = {
        "name": "Updated Test Product",
        "description": "After update",
        "price": 750,
        "quantity": 20,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    response = client.put(
        f"/api/v1/products/{product_id}",
        json=updated_data
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Product"
    assert response.json()["price"] == "750.00"


def test_patch_product(client):
    product_data = {
        "name": "Patch Test Product",
        "description": "Original description",
        "price": 300,
        "quantity": 5,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    create_response = client.post("/api/v1/products", json=product_data)
    product_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/products/{product_id}",
        json={"price": 450}
    )

    assert response.status_code == 200
    assert response.json()["price"] == "450.00"
    assert response.json()["name"] == "Patch Test Product"


def test_list_products(client):
    product_data = {
        "name": "List Test Product",
        "description": "Testing product listing",
        "price": 200,
        "quantity": 15,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    client.post("/api/v1/products", json=product_data)

    response = client.get("/api/v1/products")

    assert response.status_code == 200
    assert "items" in response.json()
    assert "totalItems" in response.json()


def test_delete_product(client):
    product_data = {
        "name": "Delete Test Product",
        "description": "Testing product deletion",
        "price": 100,
        "quantity": 5,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    create_response = client.post("/api/v1/products", json=product_data)
    product_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/products/{product_id}")

    assert response.status_code == 204


def test_get_deleted_product(client):
    product_data = {
        "name": "Deleted Product Test",
        "description": "Testing deleted product",
        "price": 150,
        "quantity": 5,
        "category": "Electronics",
        "status": "ACTIVE"
    }

    create_response = client.post("/api/v1/products", json=product_data)
    product_id = create_response.json()["id"]

    client.delete(f"/api/v1/products/{product_id}")

    response = client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 404
    assert response.json()["success"] is False