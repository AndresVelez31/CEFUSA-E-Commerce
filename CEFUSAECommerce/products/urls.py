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
    # ── Productos ─────────────────────────────────────
    # GET  /api/products/             → listar productos
    # POST /api/products/             → crear producto
    path('', ProductListCreateView.as_view(), name='product-list-create'),

    # GET    /api/products/<pk>/      → detalle
    # PATCH  /api/products/<pk>/      → actualizar
    # DELETE /api/products/<pk>/      → baja lógica
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # ── Variantes de un producto ───────────────────────
    # GET  /api/products/<pk>/variants/  → listar variantes
    # POST /api/products/<pk>/variants/  → añadir variante
    path('<int:pk>/variants/', ProductVariantListCreateView.as_view(), name='product-variants'),

    # ── Variante individual ────────────────────────────
    # GET    /api/products/variants/<vpk>/        → detalle variante
    # PATCH  /api/products/variants/<vpk>/        → actualizar variante
    # DELETE /api/products/variants/<vpk>/        → eliminar variante
    path('variants/<int:vpk>/', ProductVariantDetailView.as_view(), name='variant-detail'),

    # PATCH  /api/products/variants/<vpk>/stock/  → actualizar stock
    path('variants/<int:vpk>/stock/', VariantStockView.as_view(), name='variant-stock'),

    # ── Utilitarios ────────────────────────────────────
    # POST /api/products/check-stock/  → verificar disponibilidad
    path('check-stock/', CheckStockView.as_view(), name='check-stock'),
]
