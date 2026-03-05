from django.urls import path
from products.views import ProductListCreateView, ProductDetailView, CheckStockView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('check-stock/', CheckStockView.as_view(), name='check-stock'),
]