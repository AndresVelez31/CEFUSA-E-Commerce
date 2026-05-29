from django.test import TestCase
from django.urls import reverse


class PublicStatsViewTest(TestCase):
    def test_public_stats_returns_200(self):
        response = self.client.get('/api/public/stats/')
        self.assertEqual(response.status_code, 200)

    def test_public_stats_has_service_field(self):
        response = self.client.get('/api/public/stats/')
        self.assertIn('service', response.json())

    def test_exchange_rate_returns_200(self):
        response = self.client.get('/api/integrations/exchange-rate/?from=USD&to=COP')
        # Puede ser 200 o 503 si no hay conexión — ambos son válidos en test
        self.assertIn(response.status_code, [200, 503])