from rest_framework.views import APIView
from rest_framework.response import Response
from orders.services import OrderService
from products.models import Product


class PublicStatsView(APIView):
    """Endpoint público para el equipo aliado — expone info del sistema."""

    def get(self, request):
        stats = OrderService().get_dashboard_stats()
        return Response({
            "service": "CEFUSA E-Commerce",
            "version": "2.0",
            "stats": {
                "total_products": Product.objects.filter(is_active=True).count(),
                "total_orders": stats["total_orders"],
                "total_customers": stats["total_customers"],
                "total_revenue": stats["total_revenue"],
            },
            "endpoints": {
                "products_v2": "/api/v2/products/",
                "checkout_v2": "/api/v2/checkout/",
                "customers_v2": "/api/v2/customers/",
            }
        })


class ExchangeRateView(APIView):
    """Consume API de terceros vía Adapter Pattern (DIP)."""

    def get(self, request):
        from orders.infra.adapters.exchange_rate_adapter import ExchangeRateAdapter
        from_cur = request.query_params.get("from", "USD")
        to_cur = request.query_params.get("to", "COP")
        try:
            adapter = ExchangeRateAdapter()
            rate = adapter.get_exchange_rate(from_cur, to_cur)
            return Response({"from": from_cur, "to": to_cur, "rate": rate})
        except Exception as e:
            return Response({"error": str(e)}, status=503)


class AllyInfoView(APIView):
    """Consume el servicio del equipo aliado vía Adapter."""

    def get(self, request):
        from orders.infra.adapters.ally_service_adapter import AllyServiceAdapter
        try:
            data = AllyServiceAdapter().get_info()
            return Response(data)
        except Exception as e:
            return Response({"error": f"No se pudo contactar al aliado: {e}"}, status=503)