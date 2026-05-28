"""
Tests para el microservicio ms-customers.
Cubre los 7 endpoints: health, list, create, get, get_by_email, update, delete.
"""
import pytest
import app as app_module
from app import app


@pytest.fixture(autouse=True)
def reset_db(tmp_path):
    """Cada test usa una BD SQLite temporal fresca e independiente."""
    db_file = str(tmp_path / "test_customers.db")
    app_module.DB_PATH = db_file
    app_module.init_db()
    yield
    app_module.DB_PATH = "customers.db"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ─── Health ────────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "ms-customers"


# ─── List ──────────────────────────────────────────────────────────────────────

def test_list_customers_empty(client):
    r = client.get("/api/v2/customers/")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)
    assert len(r.get_json()) == 0


# ─── Create ────────────────────────────────────────────────────────────────────

def test_create_customer(client):
    r = client.post("/api/v2/customers/", json={
        "nombre": "Andrés", "apellido": "Vélez", "email": "andres@test.com"
    })
    assert r.status_code == 201
    data = r.get_json()
    assert data["success"] is True
    assert data["customer"]["email"] == "andres@test.com"


def test_create_duplicate_email(client):
    client.post("/api/v2/customers/", json={
        "nombre": "A", "apellido": "B", "email": "dup@test.com"
    })
    r = client.post("/api/v2/customers/", json={
        "nombre": "C", "apellido": "D", "email": "dup@test.com"
    })
    assert r.status_code == 409


def test_create_missing_email(client):
    r = client.post("/api/v2/customers/", json={"nombre": "Sin Email", "apellido": "Test"})
    assert r.status_code == 400


def test_create_missing_nombre(client):
    r = client.post("/api/v2/customers/", json={"email": "x@test.com"})
    assert r.status_code == 400


# ─── Get by ID ─────────────────────────────────────────────────────────────────

def test_get_customer_not_found(client):
    r = client.get("/api/v2/customers/9999/")
    assert r.status_code == 404


def test_get_customer_exists(client):
    client.post("/api/v2/customers/", json={
        "nombre": "Juan", "apellido": "Perez", "email": "juan@test.com"
    })
    r = client.get("/api/v2/customers/1/")
    assert r.status_code == 200
    assert r.get_json()["email"] == "juan@test.com"


# ─── Get by Email ──────────────────────────────────────────────────────────────

def test_get_by_email(client):
    client.post("/api/v2/customers/", json={
        "nombre": "Maria", "apellido": "Lopez", "email": "maria@test.com"
    })
    r = client.get("/api/v2/customers/by-email/?email=maria@test.com")
    assert r.status_code == 200
    assert r.get_json()["customer"]["nombre"] == "Maria"


def test_get_by_email_not_found(client):
    r = client.get("/api/v2/customers/by-email/?email=noexiste@test.com")
    assert r.status_code == 404


def test_get_by_email_missing_param(client):
    r = client.get("/api/v2/customers/by-email/")
    assert r.status_code == 400


# ─── Update ────────────────────────────────────────────────────────────────────

def test_update_customer(client):
    client.post("/api/v2/customers/", json={
        "nombre": "Luis", "apellido": "García", "email": "luis@test.com"
    })
    r = client.put("/api/v2/customers/1/", json={"telefono": "3001234567"})
    assert r.status_code == 200
    assert r.get_json()["customer"]["telefono"] == "3001234567"


def test_update_customer_not_found(client):
    r = client.put("/api/v2/customers/9999/", json={"nombre": "Ghost"})
    assert r.status_code == 404


# ─── Delete ────────────────────────────────────────────────────────────────────

def test_delete_customer(client):
    client.post("/api/v2/customers/", json={
        "nombre": "To", "apellido": "Delete", "email": "delete@test.com"
    })
    r = client.delete("/api/v2/customers/1/")
    assert r.status_code == 200
    assert r.get_json()["success"] is True


def test_delete_customer_not_found(client):
    r = client.delete("/api/v2/customers/9999/")
    assert r.status_code == 404
