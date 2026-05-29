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

def test_create_shipment(client):
    r = client.post("/api/v2/shipping/", json={"order_id": 1, "address": "Calle 123"})
    assert r.status_code == 201
    assert "SHIP-" in r.get_json()["shipment"]["tracking_number"]

def test_create_duplicate_shipment(client):
    client.post("/api/v2/shipping/", json={"order_id": 99})
    r = client.post("/api/v2/shipping/", json={"order_id": 99})
    assert r.status_code == 409

def test_get_shipment(client):
    client.post("/api/v2/shipping/", json={"order_id": 2})
    r = client.get("/api/v2/shipping/2/")
    assert r.status_code == 200
    assert r.get_json()["status"] == "preparing"

def test_get_shipment_not_found(client):
    r = client.get("/api/v2/shipping/9999/")
    assert r.status_code == 404

def test_update_status(client):
    client.post("/api/v2/shipping/", json={"order_id": 3})
    r = client.put("/api/v2/shipping/3/status/", json={"status": "shipped"})
    assert r.status_code == 200
    assert r.get_json()["shipment"]["status"] == "shipped"

def test_update_invalid_status(client):
    client.post("/api/v2/shipping/", json={"order_id": 4})
    r = client.put("/api/v2/shipping/4/status/", json={"status": "volando"})
    assert r.status_code == 400

def test_create_missing_order_id(client):
    r = client.post("/api/v2/shipping/", json={})
    assert r.status_code == 400

def test_create_invalid_order_id(client):
    r = client.post("/api/v2/shipping/", json={"order_id": -1})
    assert r.status_code == 400

def test_update_status_missing_status(client):
    client.post("/api/v2/shipping/", json={"order_id": 5})
    r = client.put("/api/v2/shipping/5/status/", json={})
    assert r.status_code == 400