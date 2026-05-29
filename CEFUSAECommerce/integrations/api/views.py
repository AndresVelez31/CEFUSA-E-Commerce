from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from integrations.services import QuickBiteService


class QuickBiteInfoView(APIView):
    """
    GET /api/integrations/quickbite/info/
    Proxy hacia QuickBite GET /api/info/
    """

    def get(self, request):
        service = QuickBiteService()
        try:
            result = service.get_info()
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
