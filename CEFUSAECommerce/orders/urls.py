from django.urls import path
from orders.views import CreateOrderView, CheckoutView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CreateOrderView.as_view(), name='checkout'),
    path('checkout/', CheckoutView.as_view()),

]