from decimal import Decimal
from django.utils.translation import gettext as _
from orders.models import Order, OrderItem


class OrderBuilder:
    """
    Builder para construcción de órdenes.
    Acepta objetos ProductVariant reales: valida stock y genera snapshots
    automáticamente del nombre y precio en el momento de la compra.
    """

    DISCOUNT_RATE = Decimal("0.10")  # 10 % de descuento plano

    def __init__(self):
        self._customer = None
        self._items = []   # {'variant': obj, 'quantity': int, 'product_name': str, 'price': Decimal}
        self._direccion_envio = None
        self._discount_code = None

    # ─── Métodos de configuración (fluent interface) ───────────────────────────

    def for_customer(self, customer):
        self._customer = customer
        return self

    def add_item(self, variant, quantity: int):
        """
        Agrega un item a la orden a partir de un ProductVariant real.
        Valida stock y captura snapshots de nombre y precio.

        Args:
            variant: ProductVariant (con .inventory, .price, .product.name)
            quantity: cantidad a ordenar (> 0)

        Raises:
            ValueError: si la cantidad es inválida o no hay stock suficiente
        """
        if quantity <= 0:
            raise ValueError(_("La cantidad debe ser mayor a 0"))

        # Validar inventario asignado
        try:
            inventory = variant.inventory
        except Exception:
            raise ValueError(
                _("La variante '%(variant)s' no tiene inventario asignado")
                % {"variant": variant}
            )

        # Validar stock disponible
        if not inventory.has_stock(quantity):
            raise ValueError(
                _(
                    "Stock insuficiente para '%(product)s' (%(sku)s). "
                    "Disponible: %(available)s, solicitado: %(requested)s"
                )
                % {
                    "product": variant.product.name,
                    "sku": variant.sku,
                    "available": inventory.available_quantity,
                    "requested": quantity,
                }
            )

        self._items.append({
            "variant":      variant,
            "product_name": variant.product.name,       # snapshot del nombre
            "quantity":     quantity,
            "price":        Decimal(str(variant.price)), # snapshot del precio
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
            raise ValueError(_("Se requiere un Customer para crear la orden"))
        if not self._items:
            raise ValueError(_("La orden debe tener al menos un item"))
        if not self._direccion_envio:
            raise ValueError(_("Se requiere una dirección de envío"))

        # Cálculos monetarios con los snapshots ya capturados
        subtotal = sum(
            item["quantity"] * item["price"]
            for item in self._items
        )

        if self._discount_code:
            discount_amount = subtotal * self.DISCOUNT_RATE
        else:
            discount_amount = Decimal("0.00")

        total = subtotal - discount_amount

        # Persistir la orden cabecera
        order = Order.objects.create(
            customer=self._customer,
            direccion_envio=self._direccion_envio,
            discount_code=self._discount_code,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total=total,
        )

        # Persistir cada item con su FK real a la variante
        for item in self._items:
            OrderItem.objects.create(
                order=order,
                variant=item["variant"],
                product_name=item["product_name"],
                quantity=item["quantity"],
                price=item["price"],
            )

        return order
