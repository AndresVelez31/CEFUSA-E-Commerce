from decimal import Decimal
from orders.models import Order, OrderItem


class OrderBuilder:

    def __init__(self):
        self._customer_data = None
        self._items = []
        self._shipping_address = None
        self._discount_code = None

    #guarda la info del cliente
    def for_customer(self, customer_data: dict):
        self._customer_data = customer_data
        return self

    # agrega productos a la orden y guarda el item, verificando cantidades y precios
    def add_item(self, product_name: str, quantity: int, price: float):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if price < 0:
            raise ValueError("Price cannot be negative")

        self._items.append({
            "product_name": product_name,
            "quantity": quantity,
            "price": Decimal(price)
        })

        return self

    #guarda 
    def with_shipping_address(self, address: str):
        self._shipping_address = address
        return self

    def with_discount(self, discount_code=None):
        self._discount_code = discount_code
        return self

    def build(self):
        if not self._customer_data:
            raise ValueError("Customer data is required")

        if not self._items:
            raise ValueError("At least one item is required")

        if not self._shipping_address:
            raise ValueError("Shipping address is required")

        total = sum(
            item["quantity"] * item["price"]
            for item in self._items
        )

        if self._discount_code:
            total *= Decimal("0.90")

        order = Order.objects.create(
            customer_name=self._customer_data.get("name"),
            customer_email=self._customer_data.get("email"),
            shipping_address=self._shipping_address,
            discount_code=self._discount_code,
            total_amount=total
        )

        for item in self._items:
            OrderItem.objects.create(
                order=order,
                product_name=item["product_name"],
                quantity=item["quantity"],
                price=item["price"]
            )

        return order
