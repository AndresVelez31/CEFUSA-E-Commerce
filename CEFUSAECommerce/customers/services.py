from django.utils.translation import gettext as _
from customers.models import Customer


class CustomerService:
    """
    Servicio para gestión de clientes.
    Cumple SRP: solo maneja lógica de negocio relativa a clientes.
    """

    def get_or_create_customer(self, email: str, data: dict) -> Customer:
        """
        Obtiene un cliente existente por email o crea uno nuevo.

        Args:
            email: Email del cliente
            data: {'nombre', 'apellido', 'telefono', 'direccion'}

        Returns:
            Customer object
        """
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                'nombre':    data.get('nombre', ''),
                'apellido':  data.get('apellido', ''),
                'telefono':  data.get('telefono', ''),
                'direccion': data.get('direccion', ''),
            }
        )

        # Si ya existía, actualizar datos que pudieron cambiar
        if not created:
            updated = False
            for field in ('nombre', 'apellido', 'telefono', 'direccion'):
                if data.get(field) and getattr(customer, field) != data[field]:
                    setattr(customer, field, data[field])
                    updated = True
            if updated:
                customer.save()

        return customer

    def get_customer_by_email(self, email: str):
        """
        Busca un cliente por email.

        Returns:
            Customer object o None
        """
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def get_customer_by_id(self, customer_id: int):
        """
        Busca un cliente por ID.

        Returns:
            Customer object o None
        """
        try:
            return Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return None

    def create_customer(self, data: dict) -> dict:
        """
        Crea un nuevo cliente.

        Returns:
            {'success': bool, 'customer': Customer, 'message': str}
        """
        if Customer.objects.filter(email=data.get('email')).exists():
            return {
                'success': False,
                'customer': None,
                'message': _("Ya existe un cliente con el email %(email)s") % {'email': data.get('email')}
            }

        customer = Customer.objects.create(
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            email=data.get('email'),
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', ''),
        )

        return {
            'success': True,
            'customer': customer,
            'message': _('Cliente creado exitosamente')
        }

    def get_customer_orders(self, customer_id: int) -> dict:
        """
        Retorna el historial de órdenes de un cliente.

        Returns:
            {'success': bool, 'orders': QuerySet, 'message': str}
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return {'success': False, 'orders': [], 'message': _('Cliente no encontrado')}

        return {
            'success': True,
            'customer': customer,
            'orders': customer.orders.all().order_by('-fecha_creacion'),
            'message': 'OK'
        }

    def list_customers(self):
        """Retorna todos los clientes ordenados por fecha de registro."""
        return Customer.objects.all().order_by('-created_at')

    def update_customer(self, customer_id: int, data: dict) -> dict:
        """
        Actualiza los campos de un cliente existente.
        Returns: {'success': bool, 'customer': Customer|None, 'message': str}
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return {'success': False, 'customer': None,
                    'message': _('Cliente no encontrado')}

        new_email = data.get('email')
        if new_email and new_email != customer.email:
            if Customer.objects.filter(email=new_email).exclude(pk=customer_id).exists():
                return {'success': False, 'customer': None,
                        'message': _('El email %(email)s ya está en uso por otro cliente') % {'email': new_email}}

        for field in ('nombre', 'apellido', 'email', 'telefono', 'direccion'):
            if field in data:
                setattr(customer, field, data[field])
        customer.save()
        return {'success': True, 'customer': customer, 'message': _('Cliente actualizado')}

    def delete_customer(self, customer_id: int) -> dict:
        """
        Elimina un cliente.
        Returns: {'success': bool, 'message': str}
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return {'success': False, 'message': _('Cliente no encontrado')}
        customer.delete()
        return {'success': True, 'message': _('Cliente eliminado')}
