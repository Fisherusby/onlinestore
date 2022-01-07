from django.urls import path, include
from rest_framework.routers import DefaultRouter

from info.views import ExchangeCurrencyViewSet, TodayExchangeCurrencyViewSet
from store.views import VendorViewSet, BasketViewSet, CategoryViewSet, ProductViewSet, BrandViewSet, OrderViewSet, \
    ProductReviewsViewSet, ListVendorViewSet, ProductToFavoriteViewSet, FavoriteProductsViewSet, ProductToBasket

router = DefaultRouter()
# router.register('vendor', VendorViewSet, basename="VendorViewSet")
router.register('category', CategoryViewSet, basename="CategoryViewSet")
router.register('products/brand', BrandViewSet, basename='BrandViewSet')
router.register('basket', BasketViewSet, basename='BasketViewSet')
router.register('to_basket', ProductToBasket, basename='ProductToBasket')
router.register('order', OrderViewSet, basename='OrderViewSet')
router.register('product/reviews', ProductReviewsViewSet, basename='ProductReviewsViewSet')
router.register('favorite/product', ProductToFavoriteViewSet, basename='ProductToFavoriteViewSet')
router.register('favorite/products', FavoriteProductsViewSet, basename='FavoriteProductsViewSet')

router.register('currency', TodayExchangeCurrencyViewSet, basename = 'ExchangeCurrencyViewSet')
# router.register('currency/today', TodayExchangeCurrencyViewSet, basename='TodayExchangeCurrencyViewSet')


urlpatterns = [
    path('', include(router.urls)),
    path('vendor/<slug:slug>',
         VendorViewSet.as_view({'get': 'retrieve', }), name='VendorViewSet'),
    path('vendor',
         ListVendorViewSet.as_view(), name='ListVendorViewSet'),
    path('products/category/<slug:cat_slug>/',
         ProductViewSet.as_view({'get': 'list', }), name='ProductViewSet'),
    path('product/detail/<slug:slug>/',
         ProductViewSet.as_view({'get': 'retrieve', }), name='ProductViewSet'),
]


