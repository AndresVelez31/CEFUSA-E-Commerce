from orders.models import Order, OrderItem
from orders.domain.builders import OrderBuilder
from orders.infra.factories import NotificationFactory, PaymentProcessorFactory
from customers.services import CustomerService


class OrderService:
    """
    Capa de aplicación para órdenes.
    Orquesta CustomerService + OrderBuilder + notificaciones + pagos.
    """

    def __init__(self, notifier=None, payment_processor=None):
        self.notifier = notifier or NotificationFactory.create()
        self.payment_processor = payment_processor or PaymentProcessorFactory.create()
        self.customer_service = CustomerService()

    # ─── Acción principal ──────────────────────────────────────────────────────

    def create_order(self, customer_data: dict, items: list,
                     shipping_address: str, discount_code: str = None) -> dict:
        """
        Crea una orden completa.

        Args:
            customer_data: {'nombre': str, 'apellido': str, 'email': str,
                            'telefono': str (opt), 'direccion': str (opt)}
            items:         [{'product_name': str, 'quantity': int, 'price': float,
                             'variant_id': int (opt)}, ...]
            shipping_address: dirección de envío
            discount_code:    código de descuento opcional

        Returns:
            {'success': bool, 'order_id': int|None, 'total': float|None, 'message': str}
        """
        try:
            # 1. Validaciones básicas
            if not customer_data:
                raise ValueError("Los datos del cliente son obligatorios")
            if not items:
                raise ValueError("La orden debe tener al menos un item")
            if not shipping_address:
                raise ValueError("La dirección de envío es obligatoria")

            # 2. Obtener o crear el cliente
            customer = self.customer_service.get_or_create_customer(
                email=customer_data['email'],
                data=customer_data,
            )

            # 3. Construir la orden con el Builder
            builder = (
                OrderBuilder()
                .for_customer(customer)
                .with_shipping_address(shipping_address)
            )

            for item in items:
                builder.add_item(
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    price=item['price'],
                    variant_id=item.get('variant_id'),
                )

            if discount_code:
                builder.with_discount(discount_code)

            order = builder.build()

            # 4. Notificar al cliente (no-crítico)
            try:
                message = (
                    f"Tu orden #{order.pk} fue creada exitosamente. "
                    f"Total: ${order.total}"
                )
                self.notifier.notify(
                    user_email=customer.email,
                    message=message,
                )
            except Exception as notify_err:
                print(f"[Warning] Notificación fallida: {notify_err}")

            return {
                'success':  True,
                'order_id': order.pk,
                'total':    float(order.total),
                'message':  'Orden creada exitosamente',
            }

        except ValueError as e:
            return {'success': False, 'order_id': None, 'total': None, 'message': str(e)}
        except Exception as e:
            return {'success': False, 'order_id': None, 'total': None,
                    'message': f'Error al crear la orden: {str(e)}'}

    # ─── Consultas ─────────────────────────────────────────────────────────────

    def get_order(self, order_id: int) -> Order | None:
        try:
            return Order.objects.select_related('customer').prefetch_related('items').get(pk=order_id)
        except Order.DoesNotExist:
            return None

    def update_status(self, order_id: int, new_status: str) -> dict:
        valid = [c[0] for c in Order.STATUS_CHOICES]
        if new_status not in valid:
            return {'success': False, 'message': f'Estado inválido. Opciones: {valid}'}
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save(update_fields=['status'])
            return {'success': True, 'message': f'Estado actualizado a {new_status}'}
        except Order.DoesNotExist:
            return {'success': False, 'message': 'Orden no encontrada'}
