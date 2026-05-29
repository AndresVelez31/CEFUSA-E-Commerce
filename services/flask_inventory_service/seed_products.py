"""Carga productos de demostración en la BD SQLite de ms-inventory."""

PRODUCTS_DATA = [
    {
        "name": "Camiseta Oficial CEFUSA",
        "description": "Camiseta oficial del equipo CEFUSA. Tecnología Dri-FIT para máxima transpirabilidad.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-CAM-S-ROJ", "size": "S", "color": "Rojo", "price": 120000, "initial_stock": 20},
            {"sku": "CEFU-CAM-M-ROJ", "size": "M", "color": "Rojo", "price": 120000, "initial_stock": 25},
            {"sku": "CEFU-CAM-L-ROJ", "size": "L", "color": "Rojo", "price": 120000, "initial_stock": 18},
            {"sku": "CEFU-CAM-XL-ROJ", "size": "XL", "color": "Rojo", "price": 120000, "initial_stock": 15},
        ],
    },
    {
        "name": "Camiseta Alternativa CEFUSA",
        "description": "Camiseta alternativa oficial con diseño exclusivo.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-ALT-S-BLA", "size": "S", "color": "Blanco", "price": 115000, "initial_stock": 15},
            {"sku": "CEFU-ALT-M-BLA", "size": "M", "color": "Blanco", "price": 115000, "initial_stock": 22},
            {"sku": "CEFU-ALT-L-BLA", "size": "L", "color": "Blanco", "price": 115000, "initial_stock": 16},
        ],
    },
    {
        "name": "Short Deportivo CEFUSA",
        "description": "Short oficial de entrenamiento CEFUSA.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-SHO-S-ROJ", "size": "S", "color": "Rojo", "price": 75000, "initial_stock": 18},
            {"sku": "CEFU-SHO-M-ROJ", "size": "M", "color": "Rojo", "price": 75000, "initial_stock": 20},
            {"sku": "CEFU-SHO-L-ROJ", "size": "L", "color": "Rojo", "price": 75000, "initial_stock": 14},
        ],
    },
    {
        "name": "Gorra Oficial CEFUSA",
        "description": "Gorra con escudo bordado de CEFUSA.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-GOR-UNI-ROJ", "size": "Único", "color": "Rojo", "price": 45000, "initial_stock": 30},
            {"sku": "CEFU-GOR-UNI-NEG", "size": "Único", "color": "Negro", "price": 45000, "initial_stock": 25},
        ],
    },
    {
        "name": "Termo CEFUSA Premium",
        "description": "Termo térmico de acero inoxidable con logo CEFUSA. Capacidad 750ml.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-TER-750-ROJ", "size": "750ml", "color": "Rojo", "price": 65000, "initial_stock": 15},
            {"sku": "CEFU-TER-750-NEG", "size": "750ml", "color": "Negro", "price": 65000, "initial_stock": 12},
        ],
    },
    {
        "name": "Bufanda Oficial CEFUSA",
        "description": "Bufanda de hincha oficial con diseño de barra.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-BUF-UNI-ROJ", "size": "Único", "color": "Rojo/Blanco", "price": 38000, "initial_stock": 22},
        ],
    },
    {
        "name": "Chaqueta de Entrenamiento CEFUSA",
        "description": "Chaqueta deportiva oficial con capucha.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-CHA-M-NEG", "size": "M", "color": "Negro", "price": 185000, "initial_stock": 12},
            {"sku": "CEFU-CHA-L-NEG", "size": "L", "color": "Negro", "price": 185000, "initial_stock": 10},
        ],
    },
    {
        "name": "Balón de Fútbol CEFUSA Edición Especial",
        "description": "Balón oficial tamaño 5 con diseño exclusivo CEFUSA.",
        "category": "other",
        "variants": [
            {"sku": "CEFU-BAL-5-ROJO", "size": "5", "color": "Rojo/Blanco", "price": 95000, "initial_stock": 15},
        ],
    },
]


def seed_products(db, force=False):
    """Inserta productos de demo si la tabla está vacía (o si force=True)."""
    count = db.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]
    if count > 0 and not force:
        return 0, 0

    if force:
        db.execute("DELETE FROM inventory")
        db.execute("DELETE FROM variants")
        db.execute("DELETE FROM products")

    products_created = 0
    variants_created = 0

    for p_data in PRODUCTS_DATA:
        cursor = db.execute(
            "INSERT INTO products (name, description, category) VALUES (?, ?, ?)",
            (p_data["name"], p_data["description"], p_data["category"]),
        )
        product_id = cursor.lastrowid
        products_created += 1

        for v in p_data["variants"]:
            cur = db.execute(
                "INSERT INTO variants (product_id, sku, size, color, price) VALUES (?, ?, ?, ?, ?)",
                (product_id, v["sku"], v.get("size"), v.get("color"), v["price"]),
            )
            variant_id = cur.lastrowid
            db.execute(
                "INSERT INTO inventory (variant_id, available_quantity) VALUES (?, ?)",
                (variant_id, v.get("initial_stock", 0)),
            )
            variants_created += 1

    db.commit()
    return products_created, variants_created


if __name__ == "__main__":
    import sys
    from app import get_db, init_db

    init_db()
    db = get_db()
    n_products, n_variants = seed_products(db, force="--force" in sys.argv)
    db.close()
    print(f"✓ {n_products} productos y {n_variants} variantes en ms-inventory")
