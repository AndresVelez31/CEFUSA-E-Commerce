from django.test import TestCase
from products.models import Product
from orders.models import Order, OrderItem

class CheckoutTest(TestCase):

    def test_checkout_flow(self):

        # creación de producto
        product = Product.objects.create(
            name="Laptop",
            price=1000,
            stock=10
        )

        # creación de orden
        order = Order.objects.create()

        # creación de item
        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2
        )

        # calcular subtotal
        subtotal = item.quantity * product.price

        self.assertEqual(subtotal, 2000)