from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from customers.services import CustomerService
from customers.api.serializers import CustomerSerializer, CreateCustomerSerializer


class CustomerListCreateView(APIView):
    """
    GET  /api/customers/       → lista todos los clientes
    POST /api/customers/       → crea un nuevo cliente
    """

    def get(self, request):
        customers = CustomerService().list_customers()
        return Response(CustomerSerializer(customers, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateCustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = CustomerService()
        result = service.create_customer(serializer.validated_data)

        if result['success']:
            out = CustomerSerializer(result['customer'])
            return Response(out.data, status=status.HTTP_201_CREATED)

        return Response({'message': result['message']}, status=status.HTTP_409_CONFLICT)


class CustomerDetailView(APIView):
    """
    GET /api/customers/<id>/   → detalle de un cliente
    """

    def get(self, request, pk):
        service = CustomerService()
        customer = service.get_customer_by_id(pk)
        if not customer:
            return Response(
                {'message': 'Cliente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerOrdersView(APIView):
    """
    GET /api/customers/<id>/orders/   → historial de órdenes del cliente
    """

    def get(self, request, pk):
        service = CustomerService()
        result = service.get_customer_orders(pk)

        if not result['success']:
            return Response(
                {'message': result['message']},
                status=status.HTTP_404_NOT_FOUND
            )

        # Importación local para evitar ciclo circular
        from orders.serializers import OrderSerializer
        serializer = OrderSerializer(result['orders'], many=True)
        return Response({
            'customer': CustomerSerializer(result['customer']).data,
            'orders': serializer.data,
        }, status=status.HTTP_200_OK)


# ─── Vistas de administración ──────────────────────────────────────────────────

class AdminCustomerListView(APIView):
    """
    GET  /api/admin/customers/  → lista todos los clientes
    POST /api/admin/customers/  → crea un cliente nuevo
    """

    def get(self, request):
        customers = CustomerService().list_customers()
        return Response(CustomerSerializer(customers, many=True).data)

    def post(self, request):
        serializer = CreateCustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = CustomerService()
        result = service.create_customer(serializer.validated_data)
        if result['success']:
            return Response(CustomerSerializer(result['customer']).data,
                            status=status.HTTP_201_CREATED)
        return Response({'message': result['message']}, status=status.HTTP_409_CONFLICT)


class AdminCustomerDetailView(APIView):
    """
    GET    /api/admin/customers/<pk>/  → detalle
    PUT    /api/admin/customers/<pk>/  → editar
    DELETE /api/admin/customers/<pk>/  → eliminar
    """

    def get(self, request, pk):
        customer = CustomerService().get_customer_by_id(pk)
        if not customer:
            return Response({'message': 'Cliente no encontrado'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(CustomerSerializer(customer).data)

    def put(self, request, pk):
        result = CustomerService().update_customer(pk, request.data)
        if not result['success']:
            err_status = (
                status.HTTP_409_CONFLICT
                if 'uso' in result['message']
                else status.HTTP_404_NOT_FOUND
            )
            return Response({'message': result['message']}, status=err_status)
        return Response(CustomerSerializer(result['customer']).data)

    def delete(self, request, pk):
        result = CustomerService().delete_customer(pk)
        if not result['success']:
            return Response({'message': result['message']}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
