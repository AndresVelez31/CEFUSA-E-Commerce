from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
# orders/models.py



class Order(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.pk:
            return f"Order #{self.pk} - {self.customer_name}"
        return f"New Order - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    product_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
