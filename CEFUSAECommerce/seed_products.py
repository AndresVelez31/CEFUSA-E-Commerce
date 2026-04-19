import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSAECommerce.settings')
django.setup()

from products.models import Product, ProductVariant, Inventory

# Limpiar datos existentes (opcional)
Inventory.objects.all().delete()
ProductVariant.objects.all().delete()
Product.objects.all().delete()

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
            {"sku": "CEFU-SHO-S-ROJ",  "size": "S", "color": "Rojo",  "price": "75000.00", "stock": 18},
            {"sku": "CEFU-SHO-M-ROJ",  "size": "M", "color": "Rojo",  "price": "75000.00", "stock": 20},
            {"sku": "CEFU-SHO-L-ROJ",  "size": "L", "color": "Rojo",  "price": "75000.00", "stock": 14},
            {"sku": "CEFU-SHO-M-NEG",  "size": "M", "color": "Negro", "price": "75000.00", "stock": 16},
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
        "description": "Chaqueta deportiva oficial de entrenamiento con capucha. Tela de microfibra impermeable y transpirable. Cierre completo con bolsillos laterales.",
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
        "description": "Balón oficial con diseño exclusivo CEFUSA. Tamaño 5, construcción cosida a máquina. Ideal para entrenamiento y partidos recreativos.",
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

created_products = 0
created_variants = 0

for p_data in products_data:
    product = Product.objects.create(
        name=p_data["name"],
        description=p_data["description"],
        category=p_data["category"],
        is_active=True
    )
    created_products += 1
    for v_data in p_data["variants"]:
        variant = ProductVariant.objects.create(
            product=product,
            sku=v_data["sku"],
            size=v_data["size"],
            color=v_data["color"],
            price=v_data["price"],
            is_available=True
        )
        Inventory.objects.create(
            product_variant=variant,
            available_quantity=v_data["stock"],
            minimum_stock=5
        )
        created_variants += 1

print(f"✓ {created_products} productos creados")
print(f"✓ {created_variants} variantes con inventario creadas")
