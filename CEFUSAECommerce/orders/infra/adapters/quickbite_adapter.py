import requests
from django.conf import settings
from .base import BaseCurrencyAdapter


class QuickBiteAdapter(BaseCurrencyAdapter):
    """
    Adapter concreto para consumir el servicio del equipo aliado QuickBite.
    Implementa BaseCurrencyAdapter siguiendo el principio DIP.

    Si el aliado cambia, solo se crea una nueva clase concreta.
    El resto del código no cambia.

    Ejemplo:
        adapter = QuickBiteAdapter()
        info = adapter.get_info()  # → {'success': True, 'data': {...}}
    """
    def __init__(self, base_url: str = None, timeout: int = 10):
        self.base_url = (base_url or settings.QUICKBITE_API_URL).rstrip('/')
        self.timeout = timeout

    def get_info(self) -> dict:
        url = f"{self.base_url}/api/info/"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return {
            'success': True,
            'source_url': url,
            'data': data,
        }
