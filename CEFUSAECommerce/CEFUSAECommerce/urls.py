from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django-admin/',   admin.site.urls),
    path('api/orders/',     include('orders.urls')),
    path('api/customers/',  include('customers.urls')),
    path('api/admin/',      include('CEFUSAECommerce.admin_urls')),
    path('api/products/',   include('products.urls')),
    path('api/integrations/', include('integrations.urls')),
]