from django.contrib import admin
from products.models import Product, ProductVariant, Inventory

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Inventory)
