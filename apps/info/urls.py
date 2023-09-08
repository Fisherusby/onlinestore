from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import CovidViewSet, TodayExchangeCurrencyViewSet

router = DefaultRouter()

router.register('currency', TodayExchangeCurrencyViewSet, basename='ExchangeCurrencyViewSet')
router.register('covid', CovidViewSet, basename='CovidViewSet')

urlpatterns = [
    path('', include(router.urls)),
]
