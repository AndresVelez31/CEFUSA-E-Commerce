from django.test import TestCase
from products.models import Inventory, Product

class StockTest(TestCase):

    def test_stock_validation(self):

        product = Product.objects.create(
            name="Mouse",
            price=50,
            stock=5
        )

        quantity_requested = 10

        inventory = Inventory.objects.get(product=product)
        self.assertTrue(quantity_requested > inventory.available_quantity)