from orders.models import Order, OrderItem
from orders.domain.builders import OrderBuilder
from orders.infra.factories import NotificationFactory, PaymentProcessorFactory
from customers.services import CustomerService
from products.services import ProductService
from orders.tasks import send_order_notification
from django.utils.translation import gettext as _

class StockError(ValueError):
    """Excepción específica para errores de stock insuficiente.
    El view la captura y devuelve HTTP 409."""
    pass


class OrderService:
    """
    Capa de aplicación para órdenes.
    Orquesta CustomerService + OrderBuilder + notificaciones + pagos.
    """

    def __init__(self, notifier=None, payment_processor=None):
        self.notifier = notifier or NotificationFactory.create()
        self.payment_processor = payment_processor or PaymentProcessorFactory.create()
        self.customer_service = CustomerService()
        self.product_service  = ProductService()

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
                raise ValueError(_("Los datos del cliente son obligatorios"))
            if not items:
                raise ValueError(_("La orden debe tener al menos un item"))
            if not shipping_address:
                raise ValueError(_("La dirección de envío es obligatoria"))

            # 2. Obtener o crear el cliente
            customer = self.customer_service.get_or_create_customer(
                email=customer_data['email'],
                data=customer_data,
            )

            # 3. Resolver variantes y construir la orden con el Builder
            builder = (
                OrderBuilder()
                .for_customer(customer)
                .with_shipping_address(shipping_address)
            )

            for item in items:
                variant_id = item.get('variant_id')
                if not variant_id:
                    raise ValueError(
                        _("Cada item debe incluir 'variant_id' con el ID de la variante del producto.")
                    )

                # Obtener la variante real (con inventory prefetcheado)
                from products.models import ProductVariant
                try:
                    variant = ProductVariant.objects.select_related(
                        'product', 'inventory'
                    ).get(pk=variant_id)
                except ProductVariant.DoesNotExist:
                    raise ValueError(
                        _("Variante con id %(variant_id)s no existe.")
                        % {"variant_id": variant_id}
                    )

                # add_item valida stock internamente y lanza ValueError si no hay
                try:
                    builder.add_item(
                        variant=variant,
                        quantity=item['quantity'],
                    )
                except ValueError as stock_err:
                    raise StockError(str(stock_err))

            if discount_code:
                builder.with_discount(discount_code)

            order = builder.build()

            # 4. Descontar stock de cada variante
            for item in items:
                self.product_service.reserve_stock(
                    variant_id=item['variant_id'],
                    quantity=item['quantity'],
                )

            # 5. Procesar pago (Factory decide Mock vs Real según ENV_TYPE)
            payment_result = self.payment_processor.process_payment(float(order.total))
            if not payment_result['success']:
                # Si el pago falla lo registramos, pero no revertimos el stock
                # (en producción aquí iría lógica de compensación)
                print(f"[Warning] Pago fallido para orden #{order.pk}: {payment_result}")

            # 6. Notificar al cliente (no-crítico)

            send_order_notification.delay(customer.email, order.pk, float(order.total))


            return {
                'success':  True,
                'order_id': order.pk,
                'total':    float(order.total),
                'message':  _("Orden creada exitosamente"),
            }

        except StockError as e:
            return {'success': False, 'order_id': None, 'total': None,
                    'message': str(e), 'error_type': 'stock'}
        except ValueError as e:
            return {'success': False, 'order_id': None, 'total': None, 'message': str(e)}
        except Exception as e:
            return {'success': False, 'order_id': None, 'total': None,
                    'message': _("Error al crear la orden: %(error)s") % {"error": str(e)}}

    # ─── Consultas ─────────────────────────────────────────────────────────────

    def get_order(self, order_id: int) -> Order | None:
        try:
            return Order.objects.select_related('customer').prefetch_related('items').get(pk=order_id)
        except Order.DoesNotExist:
            return None

    def update_status(self, order_id: int, new_status: str) -> dict:
        valid = [c[0] for c in Order.STATUS_CHOICES]
        if new_status not in valid:
            return {
                'success': False,
                'message': _("Estado inválido. Opciones: %(valid)s") % {"valid": valid},
            }
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save(update_fields=['status'])
            return {
                'success': True,
                'message': _("Estado actualizado a %(status)s") % {"status": new_status},
            }
        except Order.DoesNotExist:
            return {'success': False, 'message': _("Orden no encontrada")}

    def get_dashboard_stats(self) -> dict:
        """Estadísticas generales para el panel de administración."""
        from django.db.models import Sum
        from customers.models import Customer
        orders = Order.objects.all()
        return {
            'total_orders':     orders.count(),
            'total_revenue':    float(orders.aggregate(t=Sum('total'))['t'] or 0),
            'total_customers':  Customer.objects.count(),
            'pending_orders':   orders.filter(status='pending').count(),
            'orders_by_status': {
                s: orders.filter(status=s).count()
                for s, _ in Order.STATUS_CHOICES
            },
        }

    def list_orders(self, status_filter: str = None):
        """Retorna todas las órdenes con filtro opcional por status."""
        qs = Order.objects.select_related('customer').prefetch_related('items').all()
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def delete_order(self, order_id: int) -> dict:
        """Elimina una orden por ID."""
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return {'success': True, 'message': _("Orden eliminada")}
        except Order.DoesNotExist:
            return {'success': False, 'message': _("Orden no encontrada")}
