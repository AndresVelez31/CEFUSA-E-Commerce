from celery import shared_task
from django.utils.translation import gettext as _

@shared_task(ignore_result=True)
def send_order_notification(email: str, order_id: int, total: float):
    """Envía notificación de orden de forma asíncrona (no bloquea el checkout)."""
    from orders.infra.factories import NotificationFactory
    notifier = NotificationFactory.create()
    notifier.notify(
        user_email=email,
        message=f"Tu orden #{order_id} fue creada exitosamente. Total: ${total}"
    )
    return {"status": "sent", "email": email, "order_id": order_id}

@shared_task(ignore_result=True)
def generate_sales_report():
    """Genera reporte de ventas en background."""
    from orders.services import OrderService
    return OrderService().get_dashboard_stats()
