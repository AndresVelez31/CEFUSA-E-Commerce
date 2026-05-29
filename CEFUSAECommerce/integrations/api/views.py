from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from orders.services import OrderService
from products.models import Product


class PublicStatsView(APIView):
    """Endpoint público que expone las estadísticas de CEFUSA al equipo aliado."""

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
    """Consume la API de tasas de cambio vía Adapter Pattern (DIP)."""

    def get(self, request):
        from orders.infra.adapters.exchange_rate_adapter import ExchangeRateAdapter
        from_cur = request.query_params.get("from", "USD")
        to_cur = request.query_params.get("to", "COP")
        try:
            adapter = ExchangeRateAdapter()
            rate = adapter.get_exchange_rate(from_cur, to_cur)
            return Response({"from": from_cur, "to": to_cur, "rate": rate})
        except requests.Timeout:
            return Response({"error": "La API de tasas no respondió a tiempo"}, status=504)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=503)


class AllyInfoView(APIView):
    """
    Consume el servicio del equipo aliado (QuickBite) vía Adapter Pattern.
    GET /api/integrations/ally/
    """

    def get(self, request):
        from orders.infra.adapters.quickbite_adapter import QuickBiteAdapter
        try:
            result = QuickBiteAdapter().get_info()
            return Response(result, status=status.HTTP_200_OK)
        except requests.Timeout:
            return Response(
                {'success': False, 'message': 'QuickBite no respondió a tiempo'},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except requests.HTTPError as exc:
            return Response(
                {
                    'success': False,
                    'message': f'QuickBite respondió con error HTTP {exc.response.status_code}',
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except requests.RequestException:
            return Response(
                {'success': False, 'message': 'No se pudo conectar con QuickBite'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
