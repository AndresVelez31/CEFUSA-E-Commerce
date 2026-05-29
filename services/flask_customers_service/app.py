"""
Microservicio de Clientes — Strangler Pattern
Reemplaza CustomerService del monolito Django.
BD propia: SQLite (customers.db)
Puerto: 5003
"""
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH", "customers.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefono TEXT DEFAULT '',
        direccion TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    db.commit()
    db.close()


# ─── Health ────────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ms-customers"}), 200


# ─── Clientes ──────────────────────────────────────────────────────────────────

@app.route("/api/v2/customers/", methods=["GET"])
def list_customers():
    """Listar todos los clientes ordenados por fecha de registro."""
    db = get_db()
    customers = db.execute(
        "SELECT * FROM customers ORDER BY created_at DESC"
    ).fetchall()
    db.close()
    return jsonify([dict(c) for c in customers]), 200


@app.route("/api/v2/customers/", methods=["POST"])
def create_customer():
    """Crear un nuevo cliente."""
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"success": False, "error": "Email es requerido"}), 400
    if not data.get("nombre") or not data.get("apellido"):
        return jsonify({"success": False, "error": "Nombre y apellido son requeridos"}), 400

    db = get_db()
    existing = db.execute(
        "SELECT id FROM customers WHERE email = ?", (data["email"],)
    ).fetchone()
    if existing:
        db.close()
        return jsonify({
            "success": False,
            "error": f"Ya existe un cliente con el email {data['email']}"
        }), 409

    db.execute(
        "INSERT INTO customers (nombre, apellido, email, telefono, direccion) VALUES (?, ?, ?, ?, ?)",
        (data["nombre"], data["apellido"], data["email"],
         data.get("telefono", ""), data.get("direccion", ""))
    )
    db.commit()
    customer = db.execute(
        "SELECT * FROM customers WHERE email = ?", (data["email"],)
    ).fetchone()
    db.close()
    return jsonify({"success": True, "customer": dict(customer)}), 201


@app.route("/api/v2/customers/<int:customer_id>/", methods=["GET"])
def get_customer(customer_id):
    """Obtener detalle de un cliente por ID."""
    db = get_db()
    c = db.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    db.close()
    if not c:
        return jsonify({"success": False, "error": "Cliente no encontrado"}), 404
    return jsonify(dict(c)), 200


@app.route("/api/v2/customers/upsert/", methods=["POST"])
def upsert_customer():
    """Crear o actualizar cliente por email (checkout / Django)."""
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"success": False, "error": "Email es requerido"}), 400
    if not data.get("nombre") or not data.get("apellido"):
        return jsonify({"success": False, "error": "Nombre y apellido son requeridos"}), 400

    db = get_db()
    existing = db.execute(
        "SELECT * FROM customers WHERE email = ?", (email,)
    ).fetchone()

    if existing:
        db.execute(
            "UPDATE customers SET nombre=?, apellido=?, telefono=?, direccion=? WHERE id=?",
            (
                data.get("nombre", existing["nombre"]),
                data.get("apellido", existing["apellido"]),
                data.get("telefono", existing["telefono"]),
                data.get("direccion", existing["direccion"]),
                existing["id"],
            ),
        )
        db.commit()
        customer = db.execute(
            "SELECT * FROM customers WHERE id = ?", (existing["id"],)
        ).fetchone()
        db.close()
        return jsonify({"success": True, "customer": dict(customer), "created": False}), 200

    db.execute(
        "INSERT INTO customers (nombre, apellido, email, telefono, direccion) VALUES (?, ?, ?, ?, ?)",
        (
            data["nombre"],
            data["apellido"],
            email,
            data.get("telefono", ""),
            data.get("direccion", ""),
        ),
    )
    db.commit()
    customer = db.execute(
        "SELECT * FROM customers WHERE email = ?", (email,)
    ).fetchone()
    db.close()
    return jsonify({"success": True, "customer": dict(customer), "created": True}), 201


@app.route("/api/v2/customers/by-email/", methods=["GET"])
def get_customer_by_email():
    """Buscar un cliente por email. Útil para el checkout.
    Uso: GET /api/v2/customers/by-email/?email=juan@example.com
    """
    email = request.args.get("email")
    if not email:
        return jsonify({"success": False, "error": "Parámetro 'email' es requerido"}), 400

    db = get_db()
    c = db.execute("SELECT * FROM customers WHERE email = ?", (email,)).fetchone()
    db.close()
    if not c:
        return jsonify({"success": False, "error": "Cliente no encontrado"}), 404
    return jsonify({"success": True, "customer": dict(c)}), 200


@app.route("/api/v2/customers/<int:customer_id>/", methods=["PUT"])
def update_customer(customer_id):
    """Actualizar datos de un cliente."""
    data = request.get_json()
    db = get_db()
    c = db.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not c:
        db.close()
        return jsonify({"success": False, "error": "Cliente no encontrado"}), 404

    # Verificar unicidad de email si cambia
    new_email = data.get("email", c["email"])
    if new_email != c["email"]:
        dup = db.execute(
            "SELECT id FROM customers WHERE email = ? AND id != ?",
            (new_email, customer_id)
        ).fetchone()
        if dup:
            db.close()
            return jsonify({
                "success": False,
                "error": f"El email {new_email} ya está en uso"
            }), 409

    db.execute(
        "UPDATE customers SET nombre=?, apellido=?, email=?, telefono=?, direccion=? WHERE id=?",
        (data.get("nombre", c["nombre"]),
         data.get("apellido", c["apellido"]),
         new_email,
         data.get("telefono", c["telefono"]),
         data.get("direccion", c["direccion"]),
         customer_id)
    )
    db.commit()
    updated = db.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    db.close()
    return jsonify({"success": True, "customer": dict(updated)}), 200


@app.route("/api/v2/customers/<int:customer_id>/", methods=["DELETE"])
def delete_customer(customer_id):
    """Eliminar un cliente."""
    db = get_db()
    c = db.execute("SELECT id FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not c:
        db.close()
        return jsonify({"success": False, "error": "Cliente no encontrado"}), 404
    db.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    db.commit()
    db.close()
    return jsonify({"success": True, "message": "Cliente eliminado"}), 200


# ─── Inicialización ────────────────────────────────────────────────────────────

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
