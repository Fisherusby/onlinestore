from apps.orders.views.basket import BasketViewSet, ProductToBasketViewSet
from apps.orders.views.order import (
    OrderViewSet,
    PayOrderByCardViewSet,
    PayOrderByWalletViewSet,
)

__all__ = (
    'BasketViewSet',
    'ProductToBasketViewSet',
    'OrderViewSet',
    'PayOrderByWalletViewSet',
    'PayOrderByCardViewSet',
)
