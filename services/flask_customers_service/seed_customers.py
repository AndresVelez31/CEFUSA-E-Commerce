def seed_customers(db):
    """Inserta clientes por defecto si la tabla está vacía."""
    count = db.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    if count > 0:
        return

    print("🌱 Poblando base de datos de ms_customers...")
    customers_data = [
        ("Andres", "Velez", "andres.velez@email.com", "3001234567", "Calle 10 #5-20, Medellin"),
        ("Nathalia", "Gomez", "nathalia.gomez@email.com", "3109876543", "Carrera 7 #80-15, Bogota"),
        ("Santiago", "Martinez", "santiago.m@email.com", "3204567890", "Av. El Poblado #12-34, Medellin"),
        ("Valentina", "Lopez", "valentina.lopez@email.com", "3156789012", "Calle 72 #11-30, Bogota"),
        ("Camila", "Rodriguez", "camila.rod@email.com", "3012345678", "Carrera 43A #5-113, Medellin"),
        ("Sebastian", "Torres", "sebas.torres@email.com", "3187654321", "Calle 19 #3-16, Cali"),
        ("Isabella", "Ramirez", "isabella.r@email.com", "3223456789", "Av. 6N #23-15, Cali"),
        ("Daniel", "Hernandez", "daniel.hdz@email.com", "3048765432", "Calle 93 #14-20, Bogota"),
        ("Mariana", "Castro", "mariana.castro@email.com", "3169876543", "Carrera 15 #88-30, Bogota"),
        ("Julian", "Morales", "julian.morales@email.com", "3051234567", "Calle 5 #20-40, Bucaramanga"),
    ]

    db.executemany(
        "INSERT INTO customers (nombre, apellido, email, telefono, direccion) VALUES (?, ?, ?, ?, ?)",
        customers_data
    )
    db.commit()
    print("✅ ms_customers poblado con éxito.")
