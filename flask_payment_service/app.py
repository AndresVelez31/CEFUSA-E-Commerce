"""
Microservicio de pagos — extrae PaymentProcessorFactory del monolito Django.

Strangler Pattern: este servicio reemplaza gradualmente POST /api/v1/checkout/
en el monolito Django, exponiéndose en la nueva ruta /api/v2/checkout/.
"""
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)
ENV_TYPE = os.getenv("ENV_TYPE", "development")


def _process_payment(amount: float, discount_code: str = None) -> dict:
    """
    Lógica de negocio extraída de OrderService.create_order() del monolito.
    Calcula descuentos y genera un transaction_id simulado (mock) o real.
    """
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0")

    DISCOUNT_RATE = 0.10
    discount = round(amount * DISCOUNT_RATE, 2) if discount_code else 0.0
    total = round(amount - discount, 2)

    prefix = "MOCK" if ENV_TYPE == "development" else "REAL"
    return {
        "success": True,
        "transaction_id": f"{prefix}-{random.randint(100000, 999999)}",
        "subtotal": amount,
        "discount_code": discount_code,
        "discount_amount": discount,
        "total": total,
        "processor": "mock" if ENV_TYPE == "development" else "stripe",
    }


@app.route("/health", methods=["GET"])
def health():
    """Health check para Docker y Nginx."""
    return jsonify({"status": "ok", "service": "flask-payment-service"}), 200


@app.route("/api/v2/checkout/", methods=["POST"])
def checkout():
    """
    Endpoint principal del microservicio.

    Reemplaza POST /api/v1/checkout/ del monolito Django.

    Body JSON esperado:
        {
            "amount": 150.0,
            "discount_code": "SAVE10",   (opcional)
            "order_reference": "ORD-1"   (opcional)
        }

    Respuestas:
        200 OK  — Pago procesado exitosamente.
        400 Bad Request — Datos de entrada inválidos.
        500 Internal Server Error — Error inesperado del servidor.
    """
    data = request.get_json(silent=True)

    # Validar que se recibió un body JSON
    if not data:
        return jsonify({"success": False, "error": "Body JSON requerido"}), 400

    # Validar campo obligatorio 'amount'
    if "amount" not in data:
        return jsonify({"success": False, "error": "'amount' es obligatorio"}), 400

    # Validar que 'amount' sea numérico
    try:
        amount = float(data["amount"])
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "'amount' debe ser número"}), 400

    # Procesar pago con manejo de excepciones de negocio
    try:
        result = _process_payment(amount, data.get("discount_code"))
        result["order_reference"] = data.get("order_reference", "N/A")
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Error interno: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=(ENV_TYPE == "development"))
