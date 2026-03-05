from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('clothes', 'Ropa'),
        ('accesories', 'Accesorios'),
        ('other', 'Otros')
    ]
    
    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES, default = 'other')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class ProductVariant(models.Model):
    
    product = models.ForeignKey(
        Product, 
        related_name= 'variants',
        on_delete=models.CASCADE
    )
    
    sku = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=20, null = True, blank = True)
    color = models.CharField(max_length=30, null = True, blank = True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
        )
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.sku}"
    
    
class Inventory(models.Model):
    
    product_variant = models.OneToOneField(
        ProductVariant, 
        related_name='inventory', 
        on_delete=models.CASCADE
    )
    
    available_quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)
    
    def has_stock(self, quantity: int) -> bool:
        return self.available_quantity >= quantity
    
    def is_below_minimum(self) -> bool:
        return self.available_quantity <= self.minimum_stock
        
    
    def __str__(self):
        return f"Inventario de {self.product_variant.sku}: {self.available_quantity} unidades"