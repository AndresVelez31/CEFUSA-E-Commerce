import requests
from .base import BaseCurrencyAdapter


class ExchangeRateAdapter(BaseCurrencyAdapter):
    """
    Adapter concreto — consume ExchangeRate-API.com (gratuita, sin API key).

    Ejemplo:
        adapter = ExchangeRateAdapter()
        rate = adapter.get_exchange_rate("USD", "COP")  # → 4150.50
    """
    BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

    def get_exchange_rate(self, from_currency: str = "USD", to_currency: str = "COP") -> float:
        response = requests.get(f"{self.BASE_URL}{from_currency}", timeout=5)
        response.raise_for_status()
        rates = response.json().get("rates", {})
        return rates.get(to_currency, 1.0)