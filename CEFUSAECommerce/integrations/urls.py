from django.urls import path
from integrations.api.views import PublicStatsView, ExchangeRateView, AllyInfoView

urlpatterns = [
    path('public/stats/', PublicStatsView.as_view(), name='public-stats'),
    path('exchange-rate/', ExchangeRateView.as_view(), name='exchange-rate'),
    path('ally/', AllyInfoView.as_view(), name='ally-info'),
]
