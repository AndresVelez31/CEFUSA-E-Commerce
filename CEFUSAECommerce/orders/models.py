from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('shipped',   'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        related_name='orders'
    )

    fecha_creacion  = models.DateTimeField(auto_now_add=True)

    status          = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )

    direccion_envio = models.TextField()

    discount_code   = models.CharField(max_length=50, null=True, blank=True)

    subtotal        = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)]
    )

    total           = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    
    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    SHIPPING_STATUS_CHOICES = [
        ('pending',   'Pendiente'),
        ('preparing', 'Preparando'),
        ('shipped',   'Enviado'),
        ('delivered', 'Entregado'),
    ]
    shipping_status = models.CharField(
        max_length=20, choices=SHIPPING_STATUS_CHOICES, default='pending'
    )

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Orden #{self.pk} — {self.customer} [{self.status}]"

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_cancelled(self):
        return self.status == 'cancelled'


class OrderItem(models.Model):
    order        = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE
    )
    variant      = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='order_items'
    )
    product_name = models.CharField(max_length=150)   # snapshot del nombre
    quantity     = models.PositiveIntegerField()
    price        = models.DecimalField(                # snapshot del precio
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Item de orden'
        verbose_name_plural = 'Items de orden'

    @property
    def subtotal(self):
        """Precio unitario × cantidad al momento de la compra."""
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
