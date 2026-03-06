from django.urls import path
from products.views import (
    ProductListCreateView,
    ProductDetailView,
    ProductVariantListCreateView,
    ProductVariantDetailView,
    VariantStockView,
    CheckStockView,
)

urlpatterns = [
    
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/variants/', ProductVariantListCreateView.as_view(), name='product-variants'),
    path('variants/<int:vpk>/', ProductVariantDetailView.as_view(), name='variant-detail'),
    path('variants/<int:vpk>/stock/', VariantStockView.as_view(), name='variant-stock'),
    path('check-stock/', CheckStockView.as_view(), name='check-stock'),
]
