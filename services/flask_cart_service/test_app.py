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

def test_get_empty_cart(client):
    r = client.get("/api/v2/cart/test-123/")
    assert r.status_code == 200
    assert r.get_json()["items"] == []

def test_add_item(client):
    r = client.post("/api/v2/cart/test-123/items/", json={
        "variant_id": 1, "product_name": "Camiseta", "price": 45000, "quantity": 2
    })
    assert r.status_code == 201
    assert r.get_json()["success"] is True

def test_add_item_increases_quantity(client):
    client.post("/api/v2/cart/test-dup/items/", json={"variant_id": 1, "price": 100, "quantity": 1})
    client.post("/api/v2/cart/test-dup/items/", json={"variant_id": 1, "price": 100, "quantity": 3})
    r = client.get("/api/v2/cart/test-dup/")
    items = r.get_json()["items"]
    assert items[0]["quantity"] == 4

def test_remove_item(client):
    client.post("/api/v2/cart/test-rm/items/", json={"variant_id": 5, "price": 50, "quantity": 1})
    r = client.delete("/api/v2/cart/test-rm/items/5/")
    assert r.status_code == 200

def test_clear_cart(client):
    client.post("/api/v2/cart/test-clear/items/", json={"variant_id": 1, "price": 10, "quantity": 1})
    r = client.delete("/api/v2/cart/test-clear/")
    assert r.status_code == 200
    r2 = client.get("/api/v2/cart/test-clear/")
    assert r2.get_json()["items"] == []

def test_add_item_missing_variant(client):
    r = client.post("/api/v2/cart/test-err/items/", json={})
    assert r.status_code == 400