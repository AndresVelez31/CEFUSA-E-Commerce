"""
Clientes HTTP para microservicios Flask (Strangler Pattern).
Usados por OrderService y el panel admin.
"""
from __future__ import annotations

import requests
from django.conf import settings
from django.utils.translation import gettext as _


class MicroserviceError(Exception):
    """Error al comunicarse con un microservicio."""

    def __init__(self, service: str, message: str, status_code: int | None = None):
        self.service = service
        self.status_code = status_code
        super().__init__(message)


def _request(method: str, base_url: str, path: str, service: str, **kwargs) -> dict | list:
    url = f"{base_url.rstrip('/')}{path}"
    try:
        response = requests.request(method, url, timeout=kwargs.pop("timeout", 15), **kwargs)
    except requests.RequestException as exc:
        raise MicroserviceError(service, _("Servicio %(service)s no disponible") % {"service": service}) from exc

    if response.status_code >= 400:
        try:
            body = response.json()
            message = body.get("error") or body.get("message") or response.text
        except ValueError:
            message = response.text or _("Error HTTP %(code)s") % {"code": response.status_code}
        raise MicroserviceError(service, str(message), response.status_code)

    if response.status_code == 204 or not response.content:
        return {}
    return response.json()


class InventoryClient:
    def __init__(self):
        self.base_url = settings.MS_INVENTORY_URL

    def get_variant(self, variant_id: int) -> dict:
        return _request("GET", self.base_url, f"/api/v2/inventory/variants/{variant_id}/", "ms-inventory")

    def check_stock(self, variant_id: int, quantity: int) -> dict:
        return _request(
            "POST",
            self.base_url,
            "/api/v2/inventory/check-stock/",
            "ms-inventory",
            json={"variant_id": variant_id, "quantity": quantity},
        )

    def reserve_stock(self, variant_id: int, quantity: int) -> dict:
        return _request(
            "POST",
            self.base_url,
            "/api/v2/inventory/reserve/",
            "ms-inventory",
            json={"variant_id": variant_id, "quantity": quantity},
        )

    def count_products(self) -> int:
        products = _request("GET", self.base_url, "/api/v2/products/?all=1", "ms-inventory")
        return len(products) if isinstance(products, list) else 0


class PaymentClient:
    def __init__(self):
        self.base_url = settings.MS_PAYMENT_URL

    def process_payment(
        self,
        amount: float,
        discount_code: str | None = None,
        order_reference: str | None = None,
    ) -> dict:
        payload = {"amount": amount}
        if discount_code:
            payload["discount_code"] = discount_code
        if order_reference:
            payload["order_reference"] = order_reference
        return _request(
            "POST",
            self.base_url,
            "/api/v2/checkout/",
            "flask-payment",
            json=payload,
        )


class CustomersClient:
    def __init__(self):
        self.base_url = settings.MS_CUSTOMERS_URL

    def upsert_customer(self, data: dict) -> dict:
        return _request(
            "POST",
            self.base_url,
            "/api/v2/customers/upsert/",
            "ms-customers",
            json=data,
        )

    def count_customers(self) -> int:
        customers = _request("GET", self.base_url, "/api/v2/customers/", "ms-customers")
        return len(customers) if isinstance(customers, list) else 0
