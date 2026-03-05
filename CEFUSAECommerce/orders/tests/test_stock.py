from django.test import TestCase
from products.models import Product

class StockTest(TestCase):

    def test_stock_validation(self):

        product = Product.objects.create(
            name="Mouse",
            price=50,
            stock=5
        )

        quantity_requested = 10

        self.assertTrue(quantity_requested > product.stock)