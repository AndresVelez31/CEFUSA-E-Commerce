from django.contrib import admin
from django.urls import include, path

from integrations.api.views import QuickBiteInfoView

urlpatterns = [
    path('admin/',          admin.site.urls),
    path('api/orders/',     include('orders.urls')),
    path('api/customers/',  include('customers.urls')),
    path('api/admin/',      include('CEFUSAECommerce.admin_urls')),
    path('api/products/',   include('products.urls')),
    # QuickBite — API externa (proxy)
    path('api/integrations/quickbite/info/', QuickBiteInfoView.as_view(), name='quickbite-info'),
    path('api/integrations/', include('integrations.urls')),
]