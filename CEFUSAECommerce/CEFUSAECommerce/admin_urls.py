from django.urls import path

from orders.api.views import (
    AdminDashboardView,
    AdminOrderListView,
    AdminOrderDetailView,
    OrderDetailView,
    OrderStatusUpdateView,
)
from customers.api.views import AdminCustomerListView, AdminCustomerDetailView

urlpatterns = [
    path('dashboard/',                AdminDashboardView.as_view(),     name='admin-dashboard'),
    # Órdenes
    path('orders/',                   AdminOrderListView.as_view(),     name='admin-orders'),
    path('orders/<int:pk>/',          OrderDetailView.as_view(),        name='admin-order-detail'),
    path('orders/<int:pk>/status/',   OrderStatusUpdateView.as_view(),  name='admin-order-status'),
    path('orders/<int:pk>/delete/',   AdminOrderDetailView.as_view(),   name='admin-order-delete'),
    # Clientes
    path('customers/',                AdminCustomerListView.as_view(),  name='admin-customers'),
    path('customers/<int:pk>/',       AdminCustomerDetailView.as_view(),name='admin-customer-detail'),
]
