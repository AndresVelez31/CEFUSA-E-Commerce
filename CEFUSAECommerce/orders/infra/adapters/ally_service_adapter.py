import requests
from django.conf import settings


class AllyServiceAdapter:
    """
    Adapter para consumir el servicio del equipo aliado.
    Cuando les asignen un aliado, cambien la URL en settings.ALLY_SERVICE_URL.
    """
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.ALLY_SERVICE_URL

    def get_info(self) -> dict:
        response = requests.get(f"{self.base_url}/api/public/stats/", timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "ally_name": data.get("service", "Desconocido"),
            "ally_version": data.get("version", "N/A"),
            "ally_stats": data.get("stats", {}),
        }