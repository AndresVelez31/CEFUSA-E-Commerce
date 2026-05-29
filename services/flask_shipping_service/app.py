"""
Microservicio de Envíos — Strangler Pattern
Gestiona tracking y estado de envíos.
Storage: In-memory
Puerto: 5004
"""
from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

shipments = {}


def _generate_tracking():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"SHIP-{code}"


VALID_STATUSES = ["preparing", "shipped", "in_transit", "delivered"]


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ms-shipping"}), 200


@app.route("/api/v2/shipping/", methods=["POST"])
def create_shipment():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "Body JSON es requerido"}), 400

    order_id = data.get("order_id")
    if order_id is None:
        return jsonify({"success": False, "error": "order_id es requerido"}), 400
    if isinstance(order_id, bool) or not isinstance(order_id, int) or order_id <= 0:
        return jsonify({"success": False, "error": "order_id debe ser entero positivo"}), 400

    if order_id in shipments:
        return jsonify({"success": False, "error": "Ya existe un envío para esta orden"}), 409

    tracking = _generate_tracking()
    shipments[order_id] = {
        "order_id": order_id,
        "tracking_number": tracking,
        "status": "preparing",
        "address": data.get("address", ""),
        "recipient": data.get("recipient", ""),
    }
    return jsonify({"success": True, "shipment": shipments[order_id]}), 201


@app.route("/api/v2/shipping/<int:order_id>/", methods=["GET"])
def get_shipment(order_id):
    ship = shipments.get(order_id)
    if not ship:
        return jsonify({"success": False, "error": "Envío no encontrado"}), 404
    return jsonify(ship), 200


@app.route("/api/v2/shipping/<int:order_id>/status/", methods=["PUT"])
def update_status(order_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "Body JSON es requerido"}), 400

    ship = shipments.get(order_id)
    if not ship:
        return jsonify({"success": False, "error": "Envío no encontrado"}), 404

    new_status = data.get("status")
    if not new_status:
        return jsonify({"success": False, "error": "status es requerido"}), 400
    if new_status not in VALID_STATUSES:
        return jsonify({
            "success": False,
            "error": f"Status inválido. Opciones: {VALID_STATUSES}"
        }), 400

    ship["status"] = new_status
    return jsonify({"success": True, "shipment": ship}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)