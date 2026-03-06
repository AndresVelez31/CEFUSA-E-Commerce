from rest_framework import serializers
from products.models import Product, ProductVariant, Inventory


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ['available_quantity', 'minimum_stock', 'updated_at']


class ProductVariantSerializer(serializers.ModelSerializer):

    inventory = InventorySerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'size', 'color', 'price', 'is_available', 'inventory']


class CreateVariantSerializer(serializers.Serializer):

    sku           = serializers.CharField(max_length=100)
    size          = serializers.CharField(max_length=20,  required=False, allow_blank=True, default=None)
    color         = serializers.CharField(max_length=30,  required=False, allow_blank=True, default=None)
    price         = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    initial_stock = serializers.IntegerField(min_value=0, default=0)


class UpdateVariantSerializer(serializers.Serializer):
    """Todos los campos son opcionales para PATCH."""
    sku          = serializers.CharField(max_length=100,  required=False)
    size         = serializers.CharField(max_length=20,   required=False, allow_blank=True, allow_null=True)
    color        = serializers.CharField(max_length=30,   required=False, allow_blank=True, allow_null=True)
    price        = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    is_available = serializers.BooleanField(required=False)


class ProductSerializer(serializers.ModelSerializer):

    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'is_active', 'created_at', 'variants']


class CreateProductSerializer(serializers.Serializer):

    name        = serializers.CharField(max_length=150)
    description = serializers.CharField(required=False, allow_blank=True, default='')
    category    = serializers.ChoiceField(choices=Product.CATEGORY_CHOICES, default='other')
    is_active   = serializers.BooleanField(required=False, default=True)
    variants    = CreateVariantSerializer(many=True, required=False, default=list)


class UpdateProductSerializer(serializers.Serializer):
    """Todos los campos son opcionales para PATCH."""
    name        = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    category    = serializers.ChoiceField(choices=Product.CATEGORY_CHOICES, required=False)
    is_active   = serializers.BooleanField(required=False)


class UpdateStockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
