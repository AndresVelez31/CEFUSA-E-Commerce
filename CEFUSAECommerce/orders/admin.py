from django.contrib import admin
from .models import Order, OrderItem
from django.utils.translation import gettext as _


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'customer', 'status', 'total', 'fecha_creacion')
    list_filter   = ('status',)
    search_fields = ('customer__email', 'customer__nombre', 'tracking_number')
    readonly_fields = ('fecha_creacion', 'subtotal', 'discount_amount', 'total')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'price', 'order')
