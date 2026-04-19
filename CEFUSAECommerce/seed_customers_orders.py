import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSAECommerce.settings')
django.setup()

from customers.models import Customer
from orders.models import Order, OrderItem
from products.models import ProductVariant

# ── Limpiar datos existentes ───────────────────────────────────────────────
OrderItem.objects.all().delete()
Order.objects.all().delete()
Customer.objects.all().delete()

# ── Clientes (Área Metropolitana de Medellín) ──────────────────────────────
customers_data = [
    {
        "nombre": "Carlos Andrés", "apellido": "Montoya",
        "email": "carlos.montoya@gmail.com", "telefono": "3104521890",
        "direccion": "Cra. 48 #77 Sur-15, Sabaneta, Antioquia"
    },
    {
        "nombre": "Valentina", "apellido": "Restrepo",
        "email": "valentina.restrepo@hotmail.com", "telefono": "3157834562",
        "direccion": "Cll. 36 Sur #43A-12, Envigado, Antioquia"
    },
    {
        "nombre": "Juan Diego", "apellido": "Ospina",
        "email": "juandiego.ospina@gmail.com", "telefono": "3003214789",
        "direccion": "Cra. 52 #49-08, Itagüí, Antioquia"
    },
    {
        "nombre": "Daniela", "apellido": "González",
        "email": "daniela.gonzalez@outlook.com", "telefono": "3216789034",
        "direccion": "Cll. 10 #32-45, El Poblado, Medellín, Antioquia"
    },
    {
        "nombre": "Andrés Felipe", "apellido": "Bedoya",
        "email": "andres.bedoya@gmail.com", "telefono": "3118902345",
        "direccion": "Cra. 65 #107-22, Bello, Antioquia"
    },
    {
        "nombre": "Natalia", "apellido": "Cárdenas",
        "email": "natalia.cardenas@yahoo.com", "telefono": "3042378901",
        "direccion": "Cll. 50 #52-38, Copacabana, Antioquia"
    },
    {
        "nombre": "Felipe", "apellido": "Arango",
        "email": "felipe.arango@gmail.com", "telefono": "3165670123",
        "direccion": "Cra. 55 #15 Sur-80, La Estrella, Antioquia"
    },
    {
        "nombre": "Luisa Fernanda", "apellido": "Ríos",
        "email": "luisa.rios@hotmail.com", "telefono": "3009823456",
        "direccion": "Cll. 73 #80-15, Laureles, Medellín, Antioquia"
    },
]

customers = []
for data in customers_data:
    c = Customer.objects.create(**data)
    customers.append(c)

print(f"✓ {len(customers)} clientes creados")

# ── Órdenes ────────────────────────────────────────────────────────────────
variants = list(ProductVariant.objects.select_related('product').all())

if not variants:
    print("✗ No hay variantes de productos. Ejecuta seed_products.py primero.")
    exit(1)

statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
shipping_statuses = {
    'pending':   'pending',
    'confirmed': 'preparing',
    'shipped':   'shipped',
    'delivered': 'delivered',
    'cancelled': 'pending',
}

orders_data = [
    # Carlos Andrés — entregada
    {
        "customer": customers[0],
        "status": "delivered",
        "direccion_envio": "Cra. 48 #77 Sur-15, Sabaneta, Antioquia",
        "items": [
            {"variant_idx": 0, "qty": 2},   # Camiseta Oficial S Rojo
            {"variant_idx": 10, "qty": 1},  # Gorra Rojo
        ]
    },
    # Valentina — enviada
    {
        "customer": customers[1],
        "status": "shipped",
        "direccion_envio": "Cll. 36 Sur #43A-12, Envigado, Antioquia",
        "items": [
            {"variant_idx": 4, "qty": 1},   # Camiseta Alternativa S Blanco
            {"variant_idx": 16, "qty": 1},  # Medias Rojo
        ]
    },
    # Juan Diego — confirmada
    {
        "customer": customers[2],
        "status": "confirmed",
        "direccion_envio": "Cra. 52 #49-08, Itagüí, Antioquia",
        "items": [
            {"variant_idx": 20, "qty": 1},  # Chaqueta M Negro
            {"variant_idx": 10, "qty": 1},  # Gorra Rojo
        ]
    },
    # Daniela — pendiente
    {
        "customer": customers[3],
        "status": "pending",
        "direccion_envio": "Cll. 10 #32-45, El Poblado, Medellín, Antioquia",
        "items": [
            {"variant_idx": 1, "qty": 1},   # Camiseta M Rojo
            {"variant_idx": 8, "qty": 1},   # Short S Rojo
        ]
    },
    # Andrés Felipe — segunda orden entregada
    {
        "customer": customers[4],
        "status": "delivered",
        "direccion_envio": "Cra. 65 #107-22, Bello, Antioquia",
        "items": [
            {"variant_idx": 13, "qty": 2},  # Termo Rojo
            {"variant_idx": 17, "qty": 1},  # Medias Blanco
        ]
    },
    # Natalia — cancelada
    {
        "customer": customers[5],
        "status": "cancelled",
        "direccion_envio": "Cll. 50 #52-38, Copacabana, Antioquia",
        "items": [
            {"variant_idx": 22, "qty": 1},  # Balón
        ]
    },
    # Felipe — confirmada
    {
        "customer": customers[6],
        "status": "confirmed",
        "direccion_envio": "Cra. 55 #15 Sur-80, La Estrella, Antioquia",
        "items": [
            {"variant_idx": 0, "qty": 1},
            {"variant_idx": 5, "qty": 1},
            {"variant_idx": 16, "qty": 2},
        ]
    },
    # Luisa Fernanda — pendiente
    {
        "customer": customers[7],
        "status": "pending",
        "direccion_envio": "Cll. 73 #80-15, Laureles, Medellín, Antioquia",
        "items": [
            {"variant_idx": 19, "qty": 1},  # Chaqueta S Negro
            {"variant_idx": 11, "qty": 1},  # Gorra Negro
        ]
    },
    # Carlos Andrés — segunda orden (confirmada)
    {
        "customer": customers[0],
        "status": "confirmed",
        "direccion_envio": "Cra. 48 #77 Sur-15, Sabaneta, Antioquia",
        "items": [
            {"variant_idx": 18, "qty": 1},  # Bufanda
            {"variant_idx": 15, "qty": 1},  # Termo Negro
        ]
    },
    # Valentina — segunda orden (entregada)
    {
        "customer": customers[1],
        "status": "delivered",
        "direccion_envio": "Cll. 36 Sur #43A-12, Envigado, Antioquia",
        "items": [
            {"variant_idx": 2, "qty": 1},   # Camiseta L Rojo
            {"variant_idx": 9, "qty": 1},   # Short M Rojo
        ]
    },
]

orders_created = 0
items_created = 0

for od in orders_data:
    subtotal = Decimal('0.00')
    line_items = []

    for item_data in od["items"]:
        idx = item_data["variant_idx"]
        # Si el índice supera los disponibles, usar módulo
        v = variants[idx % len(variants)]
        qty = item_data["qty"]
        price = v.price
        subtotal += price * qty
        line_items.append({"variant": v, "qty": qty, "price": price})

    total = subtotal  # sin descuento

    order = Order.objects.create(
        customer=od["customer"],
        status=od["status"],
        shipping_status=shipping_statuses[od["status"]],
        direccion_envio=od["direccion_envio"],
        subtotal=subtotal,
        discount_amount=Decimal('0.00'),
        total=total,
    )

    for li in line_items:
        OrderItem.objects.create(
            order=order,
            variant=li["variant"],
            product_name=li["variant"].product.name,
            quantity=li["qty"],
            price=li["price"],
        )
        items_created += 1

    orders_created += 1

print(f"✓ {orders_created} órdenes creadas")
print(f"✓ {items_created} items de orden creados")
