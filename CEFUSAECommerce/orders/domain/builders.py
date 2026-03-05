from decimal import Decimal
from orders.models import Order, OrderItem


class OrderBuilder:

    DISCOUNT_RATE = Decimal("0.10")  # 10 % de descuento

    def __init__(self):
        self._customer = None
        self._items = []
        self._direccion_envio = None
        self._discount_code = None

    # ─── Métodos de configuración (fluent interface) ───────────────────────────

    def for_customer(self, customer):
        self._customer = customer
        return self

    def add_item(self, product_name: str, quantity: int, price: float,
                 variant_id: int = None):
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if price < 0:
            raise ValueError("El precio no puede ser negativo")

        self._items.append({
            "product_name": product_name,
            "quantity":     quantity,
            "price":        Decimal(str(price)),
            "variant_id":   variant_id,
        })
        return self

    def with_shipping_address(self, address: str):
        self._direccion_envio = address
        return self

    def with_discount(self, discount_code: str = None):
        self._discount_code = discount_code
        return self

    # ─── Build ─────────────────────────────────────────────────────────────────

    def build(self) -> Order:
        if not self._customer:
            raise ValueError("Se requiere un Customer para crear la orden")
        if not self._items:
            raise ValueError("La orden debe tener al menos un item")
        if not self._direccion_envio:
            raise ValueError("Se requiere una dirección de envío")

        subtotal = sum(
            item["quantity"] * item["price"]
            for item in self._items
        )

        if self._discount_code:
            discount_amount = subtotal * self.DISCOUNT_RATE
        else:
            discount_amount = Decimal("0.00")

        total = subtotal - discount_amount

        order = Order.objects.create(
            customer=self._customer,
            direccion_envio=self._direccion_envio,
            discount_code=self._discount_code,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total=total,
        )

        for item in self._items:
            OrderItem.objects.create(
                order=order,
                variant_id=item["variant_id"],
                product_name=item["product_name"],
                quantity=item["quantity"],
                price=item["price"],
            )

        return order
