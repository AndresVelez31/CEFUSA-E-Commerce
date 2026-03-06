from products.models import Product, ProductVariant, Inventory

class ProductBuilder:
    
    def __init__(self):
        self._name = None
        self._description = ''
        self._category = 'other'
        self._variants = []
        
    def with_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        self._name = name.strip()
        return self
    
    def with_description(self, description: str):
        self._description = description
        return self
    
    def with_category(self, category: str):
        self._category = category
        return self
    
    def add_variant(self, sku: str, price: float, initial_stock: int = 0, size: str = None, color: str = None):
        if not sku or not sku.strip():
            raise ValueError("El SKU no puede estar vacío")
        if price < 0:
            raise ValueError("El precio no puede ser negativo")
        if initial_stock < 0:
            raise ValueError("El stock inicial no puede ser negativo")
        
        existing_skus = [v['sku'] for v in self._variants]
        
        if sku in existing_skus:
            raise ValueError(f"El SKU '{sku}' ya existe para este producto")
        
        self._variants.append({
            "sku": sku.strip(),
            "price": price,
            "initial_stock": initial_stock,
            "size": size,
            "color": color
        })
        return self
    
    def build(self):
        if not self._name:
            raise ValueError("El nombre del producto es obligatorio")

        product = Product.objects.create(
            name=self._name,
            description=self._description,
            category=self._category
        )
        
        for variant_data in self._variants:
            variant = ProductVariant.objects.create(
                product=product,
                sku=variant_data["sku"],
                price=variant_data["price"],
                size=variant_data.get("size"),
                color=variant_data.get("color")
            )
            Inventory.objects.create(
                product_variant=variant,
                available_quantity=variant_data["initial_stock"]
            )
        
        return product