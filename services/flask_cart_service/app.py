"""
Microservicio de Carrito — Strangler Pattern
Reemplaza CartContext.jsx (localStorage) del frontend.
Storage: In-memory (en prod sería Redis)
Puerto: 5002
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

# Storage en memoria — en producción se usaría Redis
carts = {}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ms-cart"}), 200


@app.route("/api/v2/cart/<cart_id>/", methods=["GET"])
def get_cart(cart_id):
    """Obtener el contenido del carrito."""
    cart = carts.get(cart_id, {"items": []})
    items = cart["items"]
    subtotal = sum(i["price"] * i["quantity"] for i in items)
    item_count = sum(i["quantity"] for i in items)
    return jsonify({
        "cart_id": cart_id,
        "items": items,
        "item_count": item_count,
        "subtotal": round(subtotal, 2)
    }), 200


@app.route("/api/v2/cart/<cart_id>/items/", methods=["POST"])
def add_item(cart_id):
    """Agregar un item al carrito (o sumar cantidad si ya existe)."""
    data = request.get_json()
    if not data or "variant_id" not in data:
        return jsonify({"success": False, "error": "variant_id es requerido"}), 400

    if cart_id not in carts:
        carts[cart_id] = {"items": []}

    items = carts[cart_id]["items"]
    existing = next((i for i in items if i["variant_id"] == data["variant_id"]), None)

    if existing:
        existing["quantity"] += data.get("quantity", 1)
    else:
        items.append({
            "variant_id": data["variant_id"],
            "product_name": data.get("product_name", ""),
            "price": float(data.get("price", 0)),
            "quantity": data.get("quantity", 1),
        })

    return jsonify({"success": True, "cart": carts[cart_id]}), 201


@app.route("/api/v2/cart/<cart_id>/items/<int:variant_id>/", methods=["PUT"])
def update_item(cart_id, variant_id):
    """Actualizar la cantidad de un item."""
    data = request.get_json()
    if cart_id not in carts:
        return jsonify({"success": False, "error": "Carrito no encontrado"}), 404

    item = next((i for i in carts[cart_id]["items"] if i["variant_id"] == variant_id), None)
    if not item:
        return jsonify({"success": False, "error": "Item no encontrado en el carrito"}), 404

    new_qty = data.get("quantity", item["quantity"])
    if new_qty <= 0:
        carts[cart_id]["items"] = [i for i in carts[cart_id]["items"] if i["variant_id"] != variant_id]
    else:
        item["quantity"] = new_qty

    return jsonify({"success": True, "cart": carts[cart_id]}), 200


@app.route("/api/v2/cart/<cart_id>/items/<int:variant_id>/", methods=["DELETE"])
def remove_item(cart_id, variant_id):
    """Quitar un item del carrito."""
    if cart_id not in carts:
        return jsonify({"success": False, "error": "Carrito no encontrado"}), 404
    carts[cart_id]["items"] = [i for i in carts[cart_id]["items"] if i["variant_id"] != variant_id]
    return jsonify({"success": True}), 200


@app.route("/api/v2/cart/<cart_id>/", methods=["DELETE"])
def clear_cart(cart_id):
    """Vaciar el carrito completo."""
    carts[cart_id] = {"items": []}
    return jsonify({"success": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

