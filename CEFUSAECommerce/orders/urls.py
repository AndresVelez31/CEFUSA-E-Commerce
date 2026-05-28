from django.urls import path
from orders.api.views import CreateOrderView, OrderDetailView, OrderStatusUpdateView
from django.utils.translation import gettext as _

app_name = 'orders'

urlpatterns = [
    path('checkout/',                  CreateOrderView.as_view(),      name='checkout'),
    path('<int:pk>/',                  OrderDetailView.as_view(),      name='detail'),
    path('<int:pk>/status/',           OrderStatusUpdateView.as_view(),name='status-update'),
]