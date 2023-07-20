from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.orders.views import (
    BasketViewSet,
    OrderViewSet,
    PayOrderByCardViewSet,
    PayOrderByWalletViewSet,
    ProductToBasketViewSet,
)

router = DefaultRouter()

router.register("basket", BasketViewSet, basename="BasketViewSet")
router.register("to_basket", ProductToBasketViewSet, basename="ProductToBasketViewSet")
router.register("order", OrderViewSet, basename="OrderViewSet")
router.register(
    "payment/wallet",
    PayOrderByWalletViewSet,
    basename="PayOrderByWalletViewSet",
)
router.register("payment/card", PayOrderByCardViewSet, basename="PayOrderByCardViewSet")

urlpatterns = [
    path("", include(router.urls)),
]
