import requests
from django.conf import settings


class QuickBiteService:
    """Cliente para la API externa QuickBite."""

    def __init__(self, base_url: str | None = None, timeout: int = 10):
        self.base_url = (base_url or settings.QUICKBITE_API_URL).rstrip('/')
        self.timeout = timeout

    def get_info(self) -> dict:
        url = f'{self.base_url}/api/info/'
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return {
            'success': True,
            'source_url': url,
            'data': data,
        }
