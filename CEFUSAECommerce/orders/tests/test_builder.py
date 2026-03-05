from django.test import TestCase
from ..domain.builders import OrderBuilder

class BuilderTest(TestCase):

    def test_builder_discount(self):

        builder = OrderBuilder()

        order = (
            builder
            .with_discount(10)
            .build()
        )

        self.assertEqual(order.discount_code, 10)