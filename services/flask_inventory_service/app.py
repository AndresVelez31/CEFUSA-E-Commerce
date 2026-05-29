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
    from seed_products import seed_products
    seed_products(db)
    db.close()


# ─── Health ────────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ms-inventory"}), 200


# ─── Productos ─────────────────────────────────────────────────────────────────

def _product_with_variants(db, product_row):
    variants = db.execute(
        "SELECT v.*, i.available_quantity "
        "FROM variants v LEFT JOIN inventory i ON i.variant_id = v.id "
        "WHERE v.product_id = ?", (product_row["id"],)
    ).fetchall()
    return {**dict(product_row), "variants": [dict(v) for v in variants]}


@app.route("/api/v2/products/", methods=["GET"])
def list_products():
    """Listar productos con variantes. ?all=1 incluye inactivos (admin)."""
    db = get_db()
    show_all = request.args.get("all") == "1"
    query = "SELECT * FROM products" if show_all else "SELECT * FROM products WHERE is_active=1"
    products = db.execute(query).fetchall()
    result = [_product_with_variants(db, p) for p in products]
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
    result = _product_with_variants(db, p)
    db.close()
    return jsonify(result), 200


@app.route("/api/v2/products/<int:product_id>/", methods=["PATCH"])
def update_product(product_id):
    """Actualizar producto (admin)."""
    data = request.get_json() or {}
    db = get_db()
    p = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if not p:
        db.close()
        return jsonify({"success": False, "error": "Producto no encontrado"}), 404

    db.execute(
        "UPDATE products SET name=?, description=?, category=?, is_active=? WHERE id=?",
        (
            data.get("name", p["name"]),
            data.get("description", p["description"]),
            data.get("category", p["category"]),
            data.get("is_active", p["is_active"]),
            product_id,
        ),
    )
    db.commit()
    updated = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    result = _product_with_variants(db, updated)
    db.close()
    return jsonify(result), 200


@app.route("/api/v2/products/<int:product_id>/", methods=["DELETE"])
def delete_product(product_id):
    """Eliminar producto (soft delete)."""
    db = get_db()
    p = db.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
    if not p:
        db.close()
        return jsonify({"success": False, "error": "Producto no encontrado"}), 404
    db.execute("UPDATE products SET is_active=0 WHERE id = ?", (product_id,))
    db.commit()
    db.close()
    return jsonify({"success": True}), 200


@app.route("/api/v2/products/<int:product_id>/variants/", methods=["POST"])
def add_variant(product_id):
    """Agregar variante a un producto existente."""
    data = request.get_json() or {}
    if not data.get("sku") or data.get("price") is None:
        return jsonify({"success": False, "error": "sku y price son obligatorios"}), 400

    db = get_db()
    p = db.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
    if not p:
        db.close()
        return jsonify({"success": False, "error": "Producto no encontrado"}), 404

    try:
        cur = db.execute(
            "INSERT INTO variants (product_id, sku, size, color, price, is_available) VALUES (?, ?, ?, ?, ?, ?)",
            (
                product_id,
                data["sku"],
                data.get("size"),
                data.get("color"),
                data["price"],
                data.get("is_available", 1),
            ),
        )
        variant_id = cur.lastrowid
        db.execute(
            "INSERT INTO inventory (variant_id, available_quantity) VALUES (?, ?)",
            (variant_id, data.get("initial_stock", 0)),
        )
        db.commit()
        variant = db.execute(
            "SELECT v.*, i.available_quantity FROM variants v "
            "LEFT JOIN inventory i ON i.variant_id = v.id WHERE v.id = ?",
            (variant_id,),
        ).fetchone()
        db.close()
        return jsonify(dict(variant)), 201
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({"success": False, "error": "SKU ya existe"}), 409


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

@app.route("/api/v2/inventory/variants/<int:variant_id>/", methods=["GET"])
def get_variant(variant_id):
    """Detalle de variante con nombre de producto (checkout / órdenes)."""
    db = get_db()
    row = db.execute(
        "SELECT v.*, i.available_quantity, p.name AS product_name, p.id AS product_id "
        "FROM variants v "
        "JOIN products p ON p.id = v.product_id "
        "LEFT JOIN inventory i ON i.variant_id = v.id "
        "WHERE v.id = ? AND p.is_active = 1",
        (variant_id,),
    ).fetchone()
    db.close()
    if not row:
        return jsonify({"success": False, "error": "Variante no encontrada"}), 404
    return jsonify(dict(row)), 200


@app.route("/api/v2/inventory/variants/<int:variant_id>/", methods=["PATCH"])
def update_variant(variant_id):
    """Actualizar variante (admin)."""
    data = request.get_json() or {}
    db = get_db()
    v = db.execute("SELECT * FROM variants WHERE id = ?", (variant_id,)).fetchone()
    if not v:
        db.close()
        return jsonify({"success": False, "error": "Variante no encontrada"}), 404

    db.execute(
        "UPDATE variants SET sku=?, size=?, color=?, price=?, is_available=? WHERE id=?",
        (
            data.get("sku", v["sku"]),
            data.get("size", v["size"]),
            data.get("color", v["color"]),
            data.get("price", v["price"]),
            data.get("is_available", v["is_available"]),
            variant_id,
        ),
    )
    db.commit()
    updated = db.execute(
        "SELECT v.*, i.available_quantity FROM variants v "
        "LEFT JOIN inventory i ON i.variant_id = v.id WHERE v.id = ?",
        (variant_id,),
    ).fetchone()
    db.close()
    return jsonify(dict(updated)), 200


@app.route("/api/v2/inventory/variants/<int:variant_id>/", methods=["DELETE"])
def delete_variant(variant_id):
    """Eliminar variante."""
    db = get_db()
    v = db.execute("SELECT id FROM variants WHERE id = ?", (variant_id,)).fetchone()
    if not v:
        db.close()
        return jsonify({"success": False, "error": "Variante no encontrada"}), 404
    db.execute("DELETE FROM inventory WHERE variant_id = ?", (variant_id,))
    db.execute("DELETE FROM variants WHERE id = ?", (variant_id,))
    db.commit()
    db.close()
    return jsonify({"success": True}), 200


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


