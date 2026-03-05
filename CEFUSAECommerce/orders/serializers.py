from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "product_name",
            "quantity",
            "price"
        ]

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "shipping_address",
            "discount_code",
            "total_amount",
            "items",
            "created_at"
        ]

class CheckoutSerializer(serializers.Serializer):

    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    shipping_address = serializers.CharField()

    items = OrderItemSerializer(many=True)

    discount_code = serializers.CharField(
        required=False,
        allow_null=True
    )