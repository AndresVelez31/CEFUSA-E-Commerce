"""
Microservicio de Inventario — Strangler Pattern
Reemplaza ProductService del monolito Django.
BD propia: SQLite (inventory.db)
Puerto: 5001
"""
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH", "inventory.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        category TEXT DEFAULT 'other',
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS variants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        sku TEXT UNIQUE NOT NULL,
        size TEXT,
        color TEXT,
        price REAL NOT NULL,
        is_available BOOLEAN DEFAULT 1,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variant_id INTEGER UNIQUE NOT NULL,
        available_quantity INTEGER DEFAULT 0,
        minimum_stock INTEGER DEFAULT 5,
        FOREIGN KEY(variant_id) REFERENCES variants(id)
    )''')
    db.commit()
    db.close()


# ─── Health ────────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ms-inventory"}), 200


# ─── Productos ─────────────────────────────────────────────────────────────────

@app.route("/api/v2/products/", methods=["GET"])
def list_products():
    """Listar todos los productos activos con sus variantes e inventario."""
    db = get_db()
    products = db.execute("SELECT * FROM products WHERE is_active=1").fetchall()
    result = []
    for p in products:
        variants = db.execute(
            "SELECT v.*, i.available_quantity "
            "FROM variants v LEFT JOIN inventory i ON i.variant_id = v.id "
            "WHERE v.product_id = ?", (p["id"],)
        ).fetchall()
        result.append({
            **dict(p),
            "variants": [dict(v) for v in variants]
        })
    db.close()
    return jsonify(result), 200


@app.route("/api/v2/products/<int:product_id>/", methods=["GET"])
def get_product(product_id):
    """Detalle de un producto con sus variantes."""
    db = get_db()
    p = db.execute(
        "SELECT * FROM products WHERE id = ? AND is_active = 1", (product_id,)
    ).fetchone()
    if not p:
        db.close()
        return jsonify({"success": False, "error": "Producto no encontrado"}), 404
    variants = db.execute(
        "SELECT v.*, i.available_quantity "
        "FROM variants v LEFT JOIN inventory i ON i.variant_id = v.id "
        "WHERE v.product_id = ?", (product_id,)
    ).fetchall()
    db.close()
    return jsonify({**dict(p), "variants": [dict(v) for v in variants]}), 200


@app.route("/api/v2/products/", methods=["POST"])
def create_product():
    """Crear un producto con variantes e inventario."""
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"success": False, "error": "name es obligatorio"}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO products (name, description, category) VALUES (?, ?, ?)",
        (data["name"], data.get("description", ""), data.get("category", "other"))
    )
    product_id = cursor.lastrowid

    for v in data.get("variants", []):
        cur = db.execute(
            "INSERT INTO variants (product_id, sku, size, color, price) VALUES (?, ?, ?, ?, ?)",
            (product_id, v["sku"], v.get("size"), v.get("color"), v["price"])
        )
        variant_id = cur.lastrowid
        db.execute(
            "INSERT INTO inventory (variant_id, available_quantity) VALUES (?, ?)",
            (variant_id, v.get("initial_stock", 0))
        )

    db.commit()
    product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    db.close()
    return jsonify({"success": True, "product": dict(product)}), 201


# ─── Inventario / Stock ────────────────────────────────────────────────────────

@app.route("/api/v2/inventory/check-stock/", methods=["POST"])
def check_stock():
    """Verificar disponibilidad de una variante."""
    data = request.get_json()
    if not data or "variant_id" not in data or "quantity" not in data:
        return jsonify({"error": "variant_id y quantity son requeridos"}), 400

    db = get_db()
    inv = db.execute(
        "SELECT * FROM inventory WHERE variant_id = ?", (data["variant_id"],)
    ).fetchone()
    db.close()

    if not inv:
        return jsonify({"error": "Variante no encontrada"}), 404

    return jsonify({
        "available": inv["available_quantity"] >= data["quantity"],
        "current_stock": inv["available_quantity"],
        "variant_id": data["variant_id"]
    }), 200


@app.route("/api/v2/inventory/reserve/", methods=["POST"])
def reserve_stock():
    """Reservar stock de una variante (descuenta la cantidad)."""
    data = request.get_json()
    if not data or "variant_id" not in data or "quantity" not in data:
        return jsonify({"error": "variant_id y quantity son requeridos"}), 400

    db = get_db()
    inv = db.execute(
        "SELECT * FROM inventory WHERE variant_id = ?", (data["variant_id"],)
    ).fetchone()

    if not inv:
        db.close()
        return jsonify({"success": False, "error": "Variante no encontrada"}), 404

    if inv["available_quantity"] < data["quantity"]:
        db.close()
        return jsonify({
            "success": False,
            "error": f"Stock insuficiente. Disponible: {inv['available_quantity']}, solicitado: {data['quantity']}"
        }), 409

    new_qty = inv["available_quantity"] - data["quantity"]
    db.execute(
        "UPDATE inventory SET available_quantity = ? WHERE variant_id = ?",
        (new_qty, data["variant_id"])
    )
    db.commit()
    db.close()
    return jsonify({"success": True, "remaining_stock": new_qty}), 200


@app.route("/api/v2/inventory/update/", methods=["PUT"])
def update_stock():
    """Actualizar manualmente el stock de una variante."""
    data = request.get_json()
    if not data or "variant_id" not in data or "quantity" not in data:
        return jsonify({"error": "variant_id y quantity son requeridos"}), 400
    if data["quantity"] < 0:
        return jsonify({"error": "La cantidad no puede ser negativa"}), 400

    db = get_db()
    inv = db.execute(
        "SELECT * FROM inventory WHERE variant_id = ?", (data["variant_id"],)
    ).fetchone()
    if not inv:
        db.close()
        return jsonify({"error": "Variante no encontrada"}), 404

    db.execute(
        "UPDATE inventory SET available_quantity = ? WHERE variant_id = ?",
        (data["quantity"], data["variant_id"])
    )
    db.commit()
    db.close()
    return jsonify({"success": True, "new_stock": data["quantity"]}), 200


# ─── Inicialización ───────────────────────────────────────────────────────────

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)


