from products.models import Product, ProductVariant, Inventory
from products.domain.builders import ProductBuilder

class ProductService:
    def __init__(self):
        self.builder = ProductBuilder()
        
    def create_product(self, data: dict) -> Product:
        builder = ProductBuilder()
        builder.with_name(data['name'])
        builder.with_description(data.get('description', ''))
        builder.with_category(data.get('category', 'other'))
        
        variants = data.get('variants', [])
        for variant in variants:
            builder.add_variant(
                sku=variant['sku'],
                price=variant['price'],
                initial_stock=variant.get('initial_stock', 0),
                size=variant.get('size'),
                color=variant.get('color')
            )
        
        return builder.build()
    
    def list_products(self, filters: dict = None) -> list:
        queryset = Product.objects.filter(is_active=True).prefetch_related('variants')
        
        if filters: 
            category = filters.get('category')
            if category:
                queryset = queryset.filter(category=category)
                
        return queryset
    
    def get_product_details(self, product_id: int) -> Product:
        try:
            return Product.objects.prefetch_related(
                'variants',
                'variants__inventory'
                ).get(id=product_id, is_active=True)
            
        except Product.DoesNotExist:
            raise ValueError(f"Producto con id {product_id} no existe")
        
    def check_availability(self, variant_id: int, quantity: int) -> dict:
        try:
            variant = ProductVariant.objects.select_related('inventory').get(id=variant_id)
        
        except ProductVariant.DoesNotExist:
            raise ValueError(f"Variante con id {variant_id} no existe")
        
        inventory = variant.inventory
        
        return {
            'available': inventory.has_stock(quantity),
            'current_stock': inventory.available_quantity,
            'variant_name': str(variant),
        }
        
    def reserve_stock(self, variant_id: int, quantity: int) -> dict:
        try:
            variant = ProductVariant.objects.select_related('inventory').get(id=variant_id)
        
        except ProductVariant.DoesNotExist:
            raise ValueError(f"Variante con id {variant_id} no existe")
        
        inventory = variant.inventory
        
        if not inventory.has_stock(quantity):
            return {
                'success': False,
                'message': f"Stock insuficiente. Disponible: {inventory.available_quantity}, solicitado: {quantity}"
            }
            
        inventory.available_quantity -= quantity
        inventory.save()
        
        return {
            'success': True,
            'message': f"Stock reservado exitosamente. Restante: {inventory.available_quantity}"
        }
        
        
    def update_stock(self, variant_id: int, quantity: int) -> dict:
        try:
            inventory = Inventory.objects.select_related('variant').get(variant__id=variant_id)
            
        except Inventory.DoesNotExist:
            raise ValueError(f"Variante con id {variant_id} no existe")
        
        if quantity < 0:
            raise ValueError("La cantidad no puede ser negativa")
        
        inventory.available_quantity = quantity
        inventory.save()
        
        return {
            'success': True,
            'new_stock': inventory.available_quantity,
            'is_below_minimum': inventory.is_below_minimum()
        }