"""
seed_data.py — Script de poblado de datos para CEFUSA E-Commerce

Crea datos realistas e interconectados:
  - 10 Customers (en Django)
  - Usa los productos de seed_products.py (tienda oficial CEFUSA)
  - 20 Orders relacionadas con customers y products reales

Uso:
    docker exec cefusa_django python /app/CEFUSAECommerce/seed_data.py
"""

import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSAECommerce.settings')
django.setup()

from customers.models import Customer
from products.models import Product, ProductVariant, Inventory
from orders.models import Order, OrderItem

print("🌱 Iniciando seed de datos CEFUSA...")

if Customer.objects.exists():
    print("✅ La base de datos ya contiene información. Omitiendo el seed automático.")
    import sys
    sys.exit(0)

# ──────────────────────────────────────────────────────────────────
# 1. PRODUCTOS CEFUSA (idénticos a seed_products.py)
# ──────────────────────────────────────────────────────────────────

# Limpiar datos existentes en el orden correcto (respetar FK)
OrderItem.objects.all().delete()
Order.objects.all().delete()
Customer.objects.all().delete()
Inventory.objects.all().delete()
ProductVariant.objects.all().delete()
Product.objects.all().delete()

print("  🗑️  Datos anteriores eliminados")

products_data = [
    {
        "name": "Camiseta Oficial CEFUSA",
        "description": "Camiseta oficial del equipo CEFUSA. Tecnología Dri-FIT para máxima transpirabilidad. Incluye escudo bordado y patrocinadores oficiales.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-CAM-S-ROJ",  "size": "S",  "color": "Rojo", "price": "120000.00", "stock": 20},
            {"sku": "CEFU-CAM-M-ROJ",  "size": "M",  "color": "Rojo", "price": "120000.00", "stock": 25},
            {"sku": "CEFU-CAM-L-ROJ",  "size": "L",  "color": "Rojo", "price": "120000.00", "stock": 18},
            {"sku": "CEFU-CAM-XL-ROJ", "size": "XL", "color": "Rojo", "price": "120000.00", "stock": 15},
        ]
    },
    {
        "name": "Camiseta Alternativa CEFUSA",
        "description": "Camiseta alternativa oficial con diseño exclusivo. Tela de alta calidad con tratamiento antibacterial.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-ALT-S-BLA",  "size": "S",  "color": "Blanco", "price": "115000.00", "stock": 15},
            {"sku": "CEFU-ALT-M-BLA",  "size": "M",  "color": "Blanco", "price": "115000.00", "stock": 22},
            {"sku": "CEFU-ALT-L-BLA",  "size": "L",  "color": "Blanco", "price": "115000.00", "stock": 16},
            {"sku": "CEFU-ALT-XL-BLA", "size": "XL", "color": "Blanco", "price": "115000.00", "stock": 12},
        ]
    },
    {
        "name": "Short Deportivo CEFUSA",
        "description": "Short oficial de entrenamiento CEFUSA. Cintura elástica con cordón ajustable. Bolsillos laterales con cierre.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-SHO-S-ROJ", "size": "S", "color": "Rojo",  "price": "75000.00", "stock": 18},
            {"sku": "CEFU-SHO-M-ROJ", "size": "M", "color": "Rojo",  "price": "75000.00", "stock": 20},
            {"sku": "CEFU-SHO-L-ROJ", "size": "L", "color": "Rojo",  "price": "75000.00", "stock": 14},
            {"sku": "CEFU-SHO-M-NEG", "size": "M", "color": "Negro", "price": "75000.00", "stock": 16},
        ]
    },
    {
        "name": "Gorra Oficial CEFUSA",
        "description": "Gorra con escudo bordado de CEFUSA. Visera curva y cierre ajustable. Tela transpirable con protección UV.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-GOR-UNI-ROJ", "size": "Único", "color": "Rojo",   "price": "45000.00", "stock": 30},
            {"sku": "CEFU-GOR-UNI-NEG", "size": "Único", "color": "Negro",  "price": "45000.00", "stock": 25},
            {"sku": "CEFU-GOR-UNI-BLA", "size": "Único", "color": "Blanco", "price": "45000.00", "stock": 20},
        ]
    },
    {
        "name": "Termo CEFUSA Premium",
        "description": "Termo térmico de acero inoxidable con logo CEFUSA. Mantiene bebidas frías por 24h y calientes por 12h. Capacidad 750ml.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-TER-750-ROJ", "size": "750ml", "color": "Rojo",   "price": "65000.00", "stock": 15},
            {"sku": "CEFU-TER-750-NEG", "size": "750ml", "color": "Negro",  "price": "65000.00", "stock": 12},
            {"sku": "CEFU-TER-750-BLA", "size": "750ml", "color": "Blanco", "price": "65000.00", "stock": 10},
        ]
    },
    {
        "name": "Medias Deportivas CEFUSA",
        "description": "Medias oficiales largas con logo CEFUSA. Tecnología anti-deslizante y soporte de arco. Pack de 2 pares.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-MED-UNI-ROJ", "size": "Único", "color": "Rojo",   "price": "28000.00", "stock": 35},
            {"sku": "CEFU-MED-UNI-BLA", "size": "Único", "color": "Blanco", "price": "28000.00", "stock": 30},
        ]
    },
    {
        "name": "Bufanda Oficial CEFUSA",
        "description": "Bufanda de hincha oficial con diseño de barra. 100% acrílico con flecos en los extremos. Medida 150cm x 20cm.",
        "category": "accesories",
        "variants": [
            {"sku": "CEFU-BUF-UNI-ROJ", "size": "Único", "color": "Rojo/Blanco", "price": "38000.00", "stock": 22},
        ]
    },
    {
        "name": "Chaqueta de Entrenamiento CEFUSA",
        "description": "Chaqueta deportiva oficial de entrenamiento con capucha. Tela de microfibra impermeable y transpirable.",
        "category": "clothes",
        "variants": [
            {"sku": "CEFU-CHA-S-NEG",  "size": "S",  "color": "Negro", "price": "185000.00", "stock": 8},
            {"sku": "CEFU-CHA-M-NEG",  "size": "M",  "color": "Negro", "price": "185000.00", "stock": 12},
            {"sku": "CEFU-CHA-L-NEG",  "size": "L",  "color": "Negro", "price": "185000.00", "stock": 10},
            {"sku": "CEFU-CHA-XL-NEG", "size": "XL", "color": "Negro", "price": "185000.00", "stock": 6},
        ]
    },
    {
        "name": "Balón de Fútbol CEFUSA Edición Especial",
        "description": "Balón oficial con diseño exclusivo CEFUSA. Tamaño 5, construcción cosida a máquina.",
        "category": "other",
        "variants": [
            {"sku": "CEFU-BAL-5-ROJO", "size": "5", "color": "Rojo/Blanco", "price": "95000.00", "stock": 15},
        ]
    },
    {
        "name": "Llavero Escudo CEFUSA",
        "description": "Llavero metálico con escudo 3D de CEFUSA. Acabado cromado de alta calidad.",
        "category": "other",
        "variants": [
            {"sku": "CEFU-LLA-UNI-MET", "size": "Único", "color": "Plateado", "price": "18000.00", "stock": 50},
        ]
    },
]

all_variants = []
for p_data in products_data:
    product = Product.objects.create(
        name=p_data["name"],
        description=p_data["description"],
        category=p_data["category"],
        is_active=True
    )
    for v_data in p_data["variants"]:
        variant = ProductVariant.objects.create(
            product=product,
            sku=v_data["sku"],
            size=v_data["size"],
            color=v_data["color"],
            price=Decimal(v_data["price"]),
            is_available=True
        )
        Inventory.objects.create(
            product_variant=variant,
            available_quantity=v_data["stock"],
            minimum_stock=5
        )
        all_variants.append(variant)

print(f"  🛍️  {Product.objects.count()} productos CEFUSA con {ProductVariant.objects.count()} variantes creados")

# ──────────────────────────────────────────────────────────────────
# 2. CLIENTES
# ──────────────────────────────────────────────────────────────────
customers_data = [
    {"nombre": "Andres",    "apellido": "Velez",      "email": "andres.velez@email.com",    "telefono": "3001234567", "direccion": "Calle 10 #5-20, Medellin"},
    {"nombre": "Nathalia",  "apellido": "Gomez",      "email": "nathalia.gomez@email.com",  "telefono": "3109876543", "direccion": "Carrera 7 #80-15, Bogota"},
    {"nombre": "Santiago",  "apellido": "Martinez",   "email": "santiago.m@email.com",      "telefono": "3204567890", "direccion": "Av. El Poblado #12-34, Medellin"},
    {"nombre": "Valentina", "apellido": "Lopez",      "email": "valentina.lopez@email.com", "telefono": "3156789012", "direccion": "Calle 72 #11-30, Bogota"},
    {"nombre": "Camila",    "apellido": "Rodriguez",  "email": "camila.rod@email.com",      "telefono": "3012345678", "direccion": "Carrera 43A #5-113, Medellin"},
    {"nombre": "Sebastian", "apellido": "Torres",     "email": "sebas.torres@email.com",    "telefono": "3187654321", "direccion": "Calle 19 #3-16, Cali"},
    {"nombre": "Isabella",  "apellido": "Ramirez",    "email": "isabella.r@email.com",      "telefono": "3223456789", "direccion": "Av. 6N #23-15, Cali"},
    {"nombre": "Daniel",    "apellido": "Hernandez",  "email": "daniel.hdz@email.com",      "telefono": "3048765432", "direccion": "Calle 93 #14-20, Bogota"},
    {"nombre": "Mariana",   "apellido": "Castro",     "email": "mariana.castro@email.com",  "telefono": "3169876543", "direccion": "Carrera 15 #88-30, Bogota"},
    {"nombre": "Julian",    "apellido": "Morales",    "email": "julian.morales@email.com",  "telefono": "3051234567", "direccion": "Calle 5 #20-40, Bucaramanga"},
]

customers = []
for data in customers_data:
    c = Customer.objects.create(**data)
    customers.append(c)

print(f"  👥 {len(customers)} clientes creados")

# ──────────────────────────────────────────────────────────────────
# 3. ÓRDENES con productos CEFUSA reales
# ──────────────────────────────────────────────────────────────────
# Índices de variantes (ver all_variants):
# 0-3:  Camiseta Oficial (S,M,L,XL Rojo)
# 4-7:  Camiseta Alternativa (S,M,L,XL Blanco)
# 8-11: Short Deportivo (S,M,L Rojo + M Negro)
# 12-14: Gorra (Rojo, Negro, Blanco)
# 15-17: Termo (Rojo, Negro, Blanco)
# 18-19: Medias (Rojo, Blanco)
# 20:   Bufanda
# 21-24: Chaqueta (S,M,L,XL Negro)
# 25:   Balón
# 26:   Llavero

orders_config = [
    # (customer_idx, [(variant_idx, qty)], status)
    (0, [(1, 2), (18, 1)],       'delivered'),   # Camiseta M Rojo x2 + Medias
    (0, [(12, 1), (20, 1)],      'confirmed'),   # Gorra Rojo + Bufanda
    (1, [(5, 1), (8, 1)],        'shipped'),     # Camiseta Alt M + Short S
    (1, [(21, 1), (18, 1)],      'pending'),     # Chaqueta S + Medias
    (2, [(2, 1), (11, 1)],       'delivered'),   # Camiseta L Rojo + Short M Negro
    (2, [(25, 1), (12, 1)],      'confirmed'),   # Balón + Gorra Rojo
    (3, [(13, 2)],               'pending'),     # Gorra Negro x2
    (3, [(0, 1), (4, 1)],        'cancelled'),   # Camiseta S Rojo + Camiseta Alt S
    (4, [(9, 2), (15, 1)],       'shipped'),     # Short M Rojo x2 + Termo Rojo
    (4, [(22, 1), (19, 1)],      'delivered'),   # Chaqueta M + Medias Blanco
    (5, [(24, 1), (16, 1)],      'confirmed'),   # Chaqueta XL + Termo Negro
    (5, [(20, 1), (26, 2)],      'pending'),     # Bufanda + Llavero x2
    (6, [(5, 2)],                'delivered'),   # Camiseta Alt M x2
    (6, [(18, 3), (19, 2)],      'shipped'),     # Medias Rojo x3 + Medias Blanco x2
    (7, [(1, 1), (9, 1), (12, 1)], 'confirmed'), # Camiseta M + Short M + Gorra
    (7, [(25, 1), (26, 1)],      'pending'),     # Balón + Llavero
    (8, [(20, 2), (14, 1)],      'delivered'),   # Bufanda x2 + Gorra Blanco
    (8, [(3, 1), (17, 1)],       'shipped'),     # Camiseta XL + Termo Blanco
    (9, [(22, 1), (2, 1)],       'confirmed'),   # Chaqueta M + Camiseta L
    (9, [(1, 2), (18, 1)],       'pending'),     # Camiseta M x2 + Medias
]

created_orders = 0
for customer_idx, items_cfg, status in orders_config:
    customer = customers[customer_idx]
    subtotal = Decimal('0')
    order_items_data = []

    for variant_idx, qty in items_cfg:
        variant = all_variants[variant_idx]
        subtotal += variant.price * qty
        order_items_data.append((variant, qty))

    discount = Decimal('0')
    if status == 'delivered' and subtotal > Decimal('200000'):
        discount = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))

    total = subtotal - discount
    tracking = f"CEFU-{random.randint(10000000, 99999999)}" if status in ['shipped', 'delivered'] else None

    order = Order.objects.create(
        customer=customer,
        status=status,
        direccion_envio=customer.direccion,
        subtotal=subtotal,
        discount_amount=discount,
        total=total,
        tracking_number=tracking,
        shipping_status='delivered' if status == 'delivered' else
                        'shipped' if status == 'shipped' else 'pending',
    )

    for variant, qty in order_items_data:
        OrderItem.objects.create(
            order=order,
            variant=variant,
            product_name=variant.product.name,
            quantity=qty,
            price=variant.price,
        )
    created_orders += 1

print(f"  📦 {created_orders} órdenes con items de productos CEFUSA")

# ──────────────────────────────────────────────────────────────────
# RESUMEN
# ──────────────────────────────────────────────────────────────────
print()
print("=" * 50)
print("✅ SEED COMPLETADO — CEFUSA E-Commerce")
print("=" * 50)
print(f"  🛍️  Productos:  {Product.objects.count()}")
print(f"  🎨 Variantes:  {ProductVariant.objects.count()}")
print(f"  👥 Clientes:   {Customer.objects.count()}")
print(f"  📦 Órdenes:    {Order.objects.count()}")
print(f"  🧾 Items:      {OrderItem.objects.count()}")
print()
print("  Estado de órdenes:")
for status, label in Order.STATUS_CHOICES:
    count = Order.objects.filter(status=status).count()
    print(f"    {label:12}: {count}")
print("=" * 50)
