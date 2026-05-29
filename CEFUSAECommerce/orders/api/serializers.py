from django.utils.translation import gettext as _
from rest_framework import serializers
from orders.models import Order, OrderItem


# ─── Serializers de lectura ────────────────────────────────────────────────────

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model  = OrderItem
        fields = ['id', 'variant_id', 'product_name', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items              = OrderItemSerializer(many=True, read_only=True)
    customer_nombre    = serializers.CharField(source='customer.nombre_completo', read_only=True)
    customer_email     = serializers.EmailField(source='customer.email', read_only=True)
    status_display     = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Order
        fields = [
            'id', 'customer_nombre', 'customer_email',
            'fecha_creacion', 'status', 'status_display',
            'direccion_envio', 'discount_code',
            'subtotal', 'discount_amount', 'total',
            'shipping_status', 'tracking_number',
            'items',
        ]
        read_only_fields = fields


# ─── Serializers de escritura (checkout) ──────────────────────────────────────

class CheckoutItemSerializer(serializers.Serializer):
    variant_id   = serializers.IntegerField()                   # requerido: ID real de ProductVariant
    quantity     = serializers.IntegerField(min_value=1)
    # product_name y price son opcionales: el backend los genera como snapshot desde la variante
    product_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    price        = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)


class CheckoutCustomerSerializer(serializers.Serializer):
    nombre    = serializers.CharField(max_length=100)
    apellido  = serializers.CharField(max_length=100)
    email     = serializers.EmailField()
    telefono  = serializers.CharField(max_length=20,  required=False, allow_blank=True)
    direccion = serializers.CharField(max_length=255, required=False, allow_blank=True)


class CheckoutSerializer(serializers.Serializer):
    """
    Serializer de entrada para POST /api/orders/checkout/

    Ejemplo de body:
    {
        "customer": {"nombre": "Ana", "apellido": "García", "email": "ana@mail.com"},
        "items": [{"product_name": "Laptop X", "quantity": 1, "price": "1299.99"}],
        "shipping_address": "Calle 123, Ciudad",
        "discount_code": "SAVE10"
    }
    """
    customer         = CheckoutCustomerSerializer()
    items            = CheckoutItemSerializer(many=True)
    shipping_address = serializers.CharField()
    discount_code    = serializers.CharField(required=False, allow_blank=True,
                                             allow_null=True, default=None)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(_("La orden debe tener al menos un item."))
        return items
