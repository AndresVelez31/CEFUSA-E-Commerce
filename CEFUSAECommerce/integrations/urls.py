from django.urls import path

from integrations.api.views import QuickBiteInfoView

urlpatterns = [
    path('quickbite/info/', QuickBiteInfoView.as_view(), name='quickbite-info'),
]
