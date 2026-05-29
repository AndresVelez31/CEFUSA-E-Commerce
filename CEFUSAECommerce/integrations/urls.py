from django.urls import path
from integrations.api.views import QuickBiteInfoView
from .views import PublicStatsView, ExchangeRateView, AllyInfoView

urlpatterns = [
    path('public/stats/', PublicStatsView.as_view(), name='public-stats'),
    path('integrations/exchange-rate/', ExchangeRateView.as_view(), name='exchange-rate'),
    path('integrations/ally/', AllyInfoView.as_view(), name='ally-info'),
    path('quickbite/info/', QuickBiteInfoView.as_view(), name='quickbite-info'),
]
