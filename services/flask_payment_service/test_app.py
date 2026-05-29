"""
test_app.py — Tests de integración del microservicio Flask (Persona 3)
Ejecutar con: python -m pytest test_app.py -v
"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Health check ──────────────────────────────────────────────
class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_health_body(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "ok"
        assert data["service"] == "flask-payment-service"


# ── Checkout exitoso ──────────────────────────────────────────
class TestCheckoutSuccess:
    def test_checkout_sin_descuento(self, client):
        res = client.post("/api/v2/checkout/",
                          json={"amount": 100.0, "order_reference": "ORD-1"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["total"] == 100.0
        assert data["discount_amount"] == 0.0

    def test_checkout_con_descuento_10_pct(self, client):
        res = client.post("/api/v2/checkout/",
                          json={"amount": 100.0, "discount_code": "SAVE10"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["discount_amount"] == 10.0
        assert data["total"] == 90.0

    def test_transaction_id_presente(self, client):
        res = client.post("/api/v2/checkout/", json={"amount": 50.0})
        assert "transaction_id" in res.get_json()

    def test_transaction_id_prefijo_mock(self, client):
        # En development ENV_TYPE=development → prefijo MOCK-
        data = client.post("/api/v2/checkout/", json={"amount": 50.0}).get_json()
        assert data["transaction_id"].startswith("MOCK-")

    def test_order_reference_se_refleja(self, client):
        res = client.post("/api/v2/checkout/",
                          json={"amount": 50.0, "order_reference": "REF-99"})
        assert res.get_json()["order_reference"] == "REF-99"

    def test_order_reference_default_na(self, client):
        res = client.post("/api/v2/checkout/", json={"amount": 50.0})
        assert res.get_json()["order_reference"] == "N/A"

    def test_subtotal_correcto(self, client):
        res = client.post("/api/v2/checkout/", json={"amount": 200.0})
        assert res.get_json()["subtotal"] == 200.0

    def test_campos_respuesta_completos(self, client):
        data = client.post("/api/v2/checkout/", json={"amount": 50.0}).get_json()
        campos = ["success", "transaction_id", "subtotal",
                  "discount_code", "discount_amount", "total", "processor"]
        for campo in campos:
            assert campo in data, f"Falta campo: {campo}"


# ── Errores de entrada (400) ──────────────────────────────────
class TestCheckoutErrors:
    def test_sin_body(self, client):
        res = client.post("/api/v2/checkout/")
        assert res.status_code == 400
        assert res.get_json()["success"] is False

    def test_sin_amount(self, client):
        res = client.post("/api/v2/checkout/",
                          json={"discount_code": "SAVE10"})
        assert res.status_code == 400
        assert "'amount'" in res.get_json()["error"]

    def test_amount_no_numerico(self, client):
        res = client.post("/api/v2/checkout/",
                          json={"amount": "cien pesos"})
        assert res.status_code == 400

    def test_amount_negativo(self, client):
        res = client.post("/api/v2/checkout/", json={"amount": -50.0})
        assert res.status_code == 400
        assert res.get_json()["success"] is False

    def test_amount_cero(self, client):
        res = client.post("/api/v2/checkout/", json={"amount": 0})
        assert res.status_code == 400

    def test_body_vacio(self, client):
        res = client.post("/api/v2/checkout/",
                          content_type="application/json",
                          data="{}")
        assert res.status_code == 400
