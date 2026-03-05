from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre_completo', 'email', 'telefono', 'created_at']
    search_fields = ['nombre', 'apellido', 'email']
    list_filter   = ['created_at']
    readonly_fields = ['created_at']
