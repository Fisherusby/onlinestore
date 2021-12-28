from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import VendorViewSet, BasketViewSet, CategoryViewSet, GoodsViewSet, BrandViewSet, OrderViewSet, \
    ReviewGoodsViewSet

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename="VendorViewSet")
router.register('category', CategoryViewSet, basename="CategoryViewSet")
router.register('goods', GoodsViewSet, basename="GoodsViewSet")
router.register('brand', BrandViewSet, basename='BrandViewSet')
router.register('basket', BasketViewSet, basename='BasketViewSet')
router.register('order', OrderViewSet, basename='OrderViewSet')
router.register('review_goods', ReviewGoodsViewSet, basename='ReviewGoodsViewSet')


urlpatterns = [
    path('', include(router.urls))
]