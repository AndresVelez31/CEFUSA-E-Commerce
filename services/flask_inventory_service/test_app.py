import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["service"] == "ms-inventory"

def test_list_products(client):
    r = client.get("/api/v2/products/")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_create_product(client):
    r = client.post("/api/v2/products/", json={
        "name": "Camiseta Test",
        "description": "Una camiseta",
        "category": "clothes",
        "variants": [{"sku": "CAM-001", "price": 45000, "initial_stock": 10}]
    })
    assert r.status_code == 201
    assert r.get_json()["success"] is True

def test_check_stock(client):
    # Primero crear un producto
    client.post("/api/v2/products/", json={
        "name": "Test Stock", "variants": [{"sku": "STK-001", "price": 100, "initial_stock": 5}]
    })
    r = client.post("/api/v2/inventory/check-stock/", json={"variant_id": 1, "quantity": 3})
    assert r.status_code == 200

def test_reserve_stock_insufficient(client):
    r = client.post("/api/v2/inventory/reserve/", json={"variant_id": 1, "quantity": 9999})
    # Puede ser 404 o 409 dependiendo de si existe
    assert r.status_code in [404, 409]

def test_check_stock_missing_fields(client):
    r = client.post("/api/v2/inventory/check-stock/", json={})
    assert r.status_code == 400

