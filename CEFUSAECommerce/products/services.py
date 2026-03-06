from products.models import Product, ProductVariant, Inventory
from products.domain.builders import ProductBuilder

class ProductService:
    def __init__(self):
        pass  # El builder se instancia localmente en create_product

    def create_product(self, data: dict) -> 'Product':
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
            inventory = Inventory.objects.select_related('product_variant').get(product_variant__id=variant_id)
            
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

    # ─── Actualizar producto ──────────────────────────────────────────────────

    def update_product(self, product_id: int, data: dict) -> dict:
        """
        Actualiza los campos básicos de un producto (PATCH parcial).
        Returns: {'success': bool, 'product': Product|None, 'message': str}
        """
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return {'success': False, 'product': None,
                    'message': f'Producto con id {product_id} no existe'}

        updatable = ('name', 'description', 'category', 'is_active')
        for field in updatable:
            if field in data:
                setattr(product, field, data[field])
        product.save()
        return {'success': True, 'product': product, 'message': 'Producto actualizado'}

    def deactivate_product(self, product_id: int) -> dict:
        """
        Baja lógica: marca el producto como is_active=False.
        La lógica de negocio vive aquí, no en la vista.
        """
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            return {'success': False, 'message': f'Producto con id {product_id} no existe'}
        product.is_active = False
        product.save()
        return {'success': True, 'message': 'Producto desactivado'}

    # ─── CRUD de variantes ────────────────────────────────────────────────────

    def get_variant(self, variant_id: int) -> ProductVariant:
        """
        Devuelve la variante o lanza ValueError si no existe.
        """
        try:
            return ProductVariant.objects.select_related(
                'product', 'inventory'
            ).get(pk=variant_id)
        except ProductVariant.DoesNotExist:
            raise ValueError(f'Variante con id {variant_id} no existe')

    def add_variant_to_product(self, product_id: int, variant_data: dict) -> dict:
        """
        Añade una nueva variante a un producto existente.
        Returns: {'success': bool, 'variant': ProductVariant|None, 'message': str}
        """
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return {'success': False, 'variant': None,
                    'message': f'Producto con id {product_id} no existe'}

        if ProductVariant.objects.filter(sku=variant_data['sku']).exists():
            return {'success': False, 'variant': None,
                    'message': f"El SKU '{variant_data['sku']}' ya está en uso"}

        variant = ProductVariant.objects.create(
            product=product,
            sku=variant_data['sku'],
            price=variant_data['price'],
            size=variant_data.get('size'),
            color=variant_data.get('color'),
        )
        Inventory.objects.create(
            product_variant=variant,
            available_quantity=variant_data.get('initial_stock', 0),
        )
        return {'success': True, 'variant': variant,
                'message': 'Variante añadida exitosamente'}

    def update_variant(self, variant_id: int, data: dict) -> dict:
        """
        Actualiza los campos de una variante (PATCH parcial).
        Returns: {'success': bool, 'variant': ProductVariant|None, 'message': str}
        """
        try:
            variant = ProductVariant.objects.get(pk=variant_id)
        except ProductVariant.DoesNotExist:
            return {'success': False, 'variant': None,
                    'message': f'Variante con id {variant_id} no existe'}

        # Verificar unicidad del SKU si se cambia
        new_sku = data.get('sku')
        if new_sku and new_sku != variant.sku:
            if ProductVariant.objects.filter(sku=new_sku).exists():
                return {'success': False, 'variant': None,
                        'message': f"El SKU '{new_sku}' ya está en uso"}

        updatable = ('sku', 'size', 'color', 'price', 'is_available')
        for field in updatable:
            if field in data:
                setattr(variant, field, data[field])
        variant.save()
        return {'success': True, 'variant': variant,
                'message': 'Variante actualizada exitosamente'}

    def delete_variant(self, variant_id: int) -> dict:
        """
        Elimina una variante y su inventario.
        No permite borrar si la variante tiene órdenes asociadas.
        Returns: {'success': bool, 'message': str}
        """
        try:
            variant = ProductVariant.objects.prefetch_related('order_items').get(pk=variant_id)
        except ProductVariant.DoesNotExist:
            return {'success': False,
                    'message': f'Variante con id {variant_id} no existe'}

        if variant.order_items.exists():
            return {'success': False,
                    'message': 'No se puede eliminar una variante que tiene órdenes asociadas'}

        variant.delete()  # CASCADE elimina el Inventory automáticamente
        return {'success': True, 'message': 'Variante eliminada exitosamente'}
