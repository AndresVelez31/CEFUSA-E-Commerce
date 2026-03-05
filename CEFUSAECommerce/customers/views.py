from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from customers.services import CustomerService
from customers.serializers import CustomerSerializer, CreateCustomerSerializer


class CustomerListCreateView(APIView):
    """
    GET  /api/customers/       → lista todos los clientes
    POST /api/customers/       → crea un nuevo cliente
    """

    def get(self, request):
        service = CustomerService()
        from customers.models import Customer
        customers = Customer.objects.all().order_by('-created_at')
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        from customers.models import Customer
        customers = Customer.objects.all().order_by('-created_at')
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

    def _get_customer(self, pk):
        from customers.models import Customer
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self._get_customer(pk)
        if not customer:
            return Response({'message': 'Cliente no encontrado'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(CustomerSerializer(customer).data)

    def put(self, request, pk):
        customer = self._get_customer(pk)
        if not customer:
            return Response({'message': 'Cliente no encontrado'},
                            status=status.HTTP_404_NOT_FOUND)
        # Permitir edición de todos los campos excepto email si ya existe en otro cliente
        serializer = CreateCustomerSerializer(data=request.data)
        if not serializer.is_valid():
            # Si el único error es email duplicado pero es el mismo cliente, filtrarlo
            errors = serializer.errors.copy()
            if 'email' in errors:
                from customers.models import Customer
                same = Customer.objects.filter(
                    email=request.data.get('email')
                ).exclude(pk=pk)
                if not same.exists():
                    errors.pop('email')
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        customer.nombre   = data.get('nombre',   customer.nombre)
        customer.apellido = data.get('apellido', customer.apellido)
        customer.email    = data.get('email',    customer.email)
        customer.telefono = data.get('telefono', customer.telefono)
        customer.direccion= data.get('direccion',customer.direccion)
        customer.save()
        return Response(CustomerSerializer(customer).data)

    def delete(self, request, pk):
        customer = self._get_customer(pk)
        if not customer:
            return Response({'message': 'Cliente no encontrado'},
                            status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
