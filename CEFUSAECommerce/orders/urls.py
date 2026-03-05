from django.urls import path
from orders.views import CreateOrderView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CreateOrderView.as_view(), name='checkout'),
]