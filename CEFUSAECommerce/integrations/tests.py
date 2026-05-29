from django.test import TestCase


class IntegrationsViewTest(TestCase):
    def test_public_stats_returns_200(self):
        response = self.client.get('/api/integrations/public/stats/')
        self.assertEqual(response.status_code, 200)

    def test_public_stats_has_service_field(self):
        response = self.client.get('/api/integrations/public/stats/')
        self.assertIn('service', response.json())

    def test_exchange_rate_returns_200_or_503(self):
        response = self.client.get('/api/integrations/exchange-rate/?from=USD&to=COP')
        # Puede ser 200 o 503/504 si no hay conexión — ambos son válidos en test
        self.assertIn(response.status_code, [200, 503, 504])

    def test_ally_quickbite_returns_200_or_error(self):
        response = self.client.get('/api/integrations/ally/')
        # Puede ser 200 si QuickBite está disponible, o 502/503/504 si no
        self.assertIn(response.status_code, [200, 502, 503, 504])