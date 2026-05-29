from orders.models import Order, OrderItem
from orders.domain.builders import OrderBuilder
from orders.infra.factories import NotificationFactory
from orders.infra.microservice_clients import (
    CustomersClient,
    InventoryClient,
    MicroserviceError,
    PaymentClient,
)
from customers.services import CustomerService
from orders.tasks import send_order_notification
from django.utils.translation import gettext as _


class StockError(ValueError):
    """Excepción específica para errores de stock insuficiente."""
    pass


class OrderService:
    """
    Orquesta checkout: ms-customers, ms-inventory, ms-payment + persistencia en Django.
    """

    def __init__(self, notifier=None):
        self.notifier = notifier or NotificationFactory.create()
        self.customer_service = CustomerService()
        self.inventory = InventoryClient()
        self.payment = PaymentClient()
        self.customers_ms = CustomersClient()

    def create_order(
        self,
        customer_data: dict,
        items: list,
        shipping_address: str,
        discount_code: str = None,
    ) -> dict:
        try:
            if not customer_data:
                raise ValueError(_("Los datos del cliente son obligatorios"))
            if not items:
                raise ValueError(_("La orden debe tener al menos un item"))
            if not shipping_address:
                raise ValueError(_("La dirección de envío es obligatoria"))

            # 1. Cliente en ms-customers (Strangler)
            self.customers_ms.upsert_customer(customer_data)

            # 2. Cliente en Django (FK de órdenes en PostgreSQL)
            customer = self.customer_service.get_or_create_customer(
                email=customer_data["email"],
                data=customer_data,
            )

            builder = (
                OrderBuilder()
                .for_customer(customer)
                .with_shipping_address(shipping_address)
            )

            # 3. Validar variantes y stock en ms-inventory
            for item in items:
                variant_id = item.get("variant_id")
                if not variant_id:
                    raise ValueError(
                        _("Cada item debe incluir 'variant_id'.")
                    )

                variant = self.inventory.get_variant(variant_id)
                stock = self.inventory.check_stock(variant_id, item["quantity"])
                if not stock.get("available"):
                    raise StockError(
                        _(
                            "Stock insuficiente para '%(product)s'. "
                            "Disponible: %(available)s, solicitado: %(requested)s"
                        )
                        % {
                            "product": variant.get("product_name", variant_id),
                            "available": stock.get("current_stock", 0),
                            "requested": item["quantity"],
                        }
                    )

                try:
                    builder.add_item_snapshot(
                        variant_id=variant_id,
                        product_name=variant["product_name"],
                        quantity=item["quantity"],
                        price=variant["price"],
                        available_quantity=stock.get("current_stock", 0),
                    )
                except ValueError as stock_err:
                    raise StockError(str(stock_err)) from stock_err

            if discount_code:
                builder.with_discount(discount_code)

            order = builder.build()

            # 4. Reservar stock en ms-inventory
            for item in items:
                result = self.inventory.reserve_stock(
                    item["variant_id"], item["quantity"]
                )
                if not result.get("success", True) and "error" in result:
                    raise StockError(result["error"])

            # 5. Pago en microservicio flask_payment (monto ya con descuento del builder)
            payment_result = self.payment.process_payment(
                amount=float(order.total),
                discount_code=None,
                order_reference=f"ORD-{order.pk}",
            )
            if not payment_result.get("success", True):
                print(
                    f"[Warning] Pago fallido para orden #{order.pk}: {payment_result}"
                )

            try:
                send_order_notification.delay(
                    customer.email, order.pk, float(order.total)
                )
            except Exception as notify_err:
                print(f"[Warning] Notificación async no enviada: {notify_err}")

            return {
                "success": True,
                "order_id": order.pk,
                "total": float(order.total),
                "transaction_id": payment_result.get("transaction_id"),
                "message": _("Orden creada exitosamente"),
            }

        except MicroserviceError as e:
            if e.status_code == 409:
                return {
                    "success": False,
                    "order_id": None,
                    "total": None,
                    "message": str(e),
                    "error_type": "stock",
                }
            return {
                "success": False,
                "order_id": None,
                "total": None,
                "message": str(e),
            }
        except StockError as e:
            return {
                "success": False,
                "order_id": None,
                "total": None,
                "message": str(e),
                "error_type": "stock",
            }
        except ValueError as e:
            return {"success": False, "order_id": None, "total": None, "message": str(e)}
        except Exception as e:
            return {
                "success": False,
                "order_id": None,
                "total": None,
                "message": _("Error al crear la orden: %(error)s") % {"error": str(e)},
            }

    def get_order(self, order_id: int) -> Order | None:
        try:
            return Order.objects.select_related("customer").prefetch_related("items").get(
                pk=order_id
            )
        except Order.DoesNotExist:
            return None

    def update_status(self, order_id: int, new_status: str) -> dict:
        valid = [c[0] for c in Order.STATUS_CHOICES]
        if new_status not in valid:
            return {
                "success": False,
                "message": _("Estado inválido. Opciones: %(valid)s") % {"valid": valid},
            }
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save(update_fields=["status"])
            return {
                "success": True,
                "message": _("Estado actualizado a %(status)s") % {"status": new_status},
            }
        except Order.DoesNotExist:
            return {"success": False, "message": _("Orden no encontrada")}

    def get_dashboard_stats(self) -> dict:
        from django.db.models import Sum

        orders = Order.objects.all()
        try:
            total_customers = self.customers_ms.count_customers()
        except MicroserviceError:
            from customers.models import Customer

            total_customers = Customer.objects.count()

        return {
            "total_orders": orders.count(),
            "total_revenue": float(orders.aggregate(t=Sum("total"))["t"] or 0),
            "total_customers": total_customers,
            "pending_orders": orders.filter(status="pending").count(),
            "orders_by_status": {
                s: orders.filter(status=s).count() for s, _ in Order.STATUS_CHOICES
            },
        }

    def list_orders(self, status_filter: str = None):
        qs = Order.objects.select_related("customer").prefetch_related("items").all()
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def delete_order(self, order_id: int) -> dict:
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return {"success": True, "message": _("Orden eliminada")}
        except Order.DoesNotExist:
            return {"success": False, "message": _("Orden no encontrada")}
