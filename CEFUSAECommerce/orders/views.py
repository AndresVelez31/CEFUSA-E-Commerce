from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from orders.services import OrderService
from orders.serializers import CheckoutSerializer, OrderSerializer
from orders.models import Order


class CreateOrderView(APIView):
    """
    POST /api/orders/checkout/
    Crea una orden nueva a partir de los datos del cliente + items.
    """

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        service = OrderService()
        result = service.create_order(
            customer_data=data['customer'],
            items=data['items'],
            shipping_address=data['shipping_address'],
            discount_code=data.get('discount_code'),
        )

        if result['success']:
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """
    GET /api/orders/<pk>/
    Devuelve el detalle de una orden.
    """

    def get(self, request, pk):
        service = OrderService()
        order = service.get_order(pk)
        if not order:
            return Response(
                {'error': 'Orden no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(OrderSerializer(order).data)


class OrderStatusUpdateView(APIView):
    """
    PATCH /api/orders/<pk>/status/
    Actualiza el estado de una orden.
    Body: { "status": "confirmed" }
    """

    def patch(self, request, pk):
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {'error': 'El campo "status" es obligatorio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        service = OrderService()
        result = service.update_status(pk, new_status)
        if result['success']:
            return Response(result)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


# ─── Vistas de administración ──────────────────────────────────────────────────

class AdminDashboardView(APIView):
    """
    GET /api/admin/dashboard/
    Estadísticas generales para el panel admin.
    """

    def get(self, request):
        from customers.models import Customer
        orders = Order.objects.all()
        total_orders    = orders.count()
        total_revenue   = float(orders.aggregate(t=Sum('total'))['t'] or 0)
        total_customers = Customer.objects.count()
        pending_orders  = orders.filter(status='pending').count()
        orders_by_status = {
            s: orders.filter(status=s).count()
            for s, _ in Order.STATUS_CHOICES
        }
        return Response({
            'total_orders':      total_orders,
            'total_revenue':     total_revenue,
            'total_customers':   total_customers,
            'pending_orders':    pending_orders,
            'orders_by_status':  orders_by_status,
        })


class AdminOrderListView(APIView):
    """
    GET  /api/admin/orders/?status=<status>  → lista órdenes
    POST /api/admin/orders/                  → crea una orden manual
    """

    def get(self, request):
        status_filter = request.query_params.get('status')
        qs = Order.objects.select_related('customer').prefetch_related('items').all()
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response(OrderSerializer(qs, many=True).data)

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        service = OrderService()
        result = service.create_order(
            customer_data=data['customer'],
            items=data['items'],
            shipping_address=data['shipping_address'],
            discount_code=data.get('discount_code'),
        )
        if result['success']:
            order = Order.objects.select_related('customer').prefetch_related('items').get(
                pk=result['order_id']
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class AdminOrderDetailView(APIView):
    """
    DELETE /api/admin/orders/<pk>/  → elimina una orden
    (GET y PATCH de estado ya están en OrderDetailView y OrderStatusUpdateView)
    """

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Orden no encontrada'},
                            status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
