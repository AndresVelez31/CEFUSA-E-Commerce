from django.urls import path
from customers.api.views import CustomerListCreateView, CustomerDetailView, CustomerOrdersView

app_name = 'customers'

urlpatterns = [
    path('', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('<int:pk>/orders/', CustomerOrdersView.as_view(), name='customer-orders'),
]
