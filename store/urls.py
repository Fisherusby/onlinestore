from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import VendorViewSet, BasketViewSet, CategoryViewSet, ProductViewSet, BrandViewSet, OrderViewSet, \
    ReviewProductViewSet, ListVendorViewSet, ProductToFavoriteViewSet, FavoriteProductsViewSet

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename="VendorViewSet")
router.register('category', CategoryViewSet, basename="CategoryViewSet")
router.register('products/brand', BrandViewSet, basename='BrandViewSet')
router.register('basket', BasketViewSet, basename='BasketViewSet')
router.register('order', OrderViewSet, basename='OrderViewSet')
router.register('review_product', ReviewProductViewSet, basename='ReviewProductViewSet')
router.register('favorite/product', ProductToFavoriteViewSet, basename='ProductToFavoriteViewSet')
router.register('favorite/products', FavoriteProductsViewSet, basename='FavoriteProductsViewSet')


urlpatterns = [
    path('', include(router.urls)),
    path('vendor/list', ListVendorViewSet.as_view(), name='ListVendorViewSet'),
    path('products/category/<cat_slug>',
         ProductViewSet.as_view({'get': 'list', }), name='ProductViewSet'),
    path('product/detail/<slug>',
         ProductViewSet.as_view({'get': 'retrieve', }), name='ProductViewSet'),
]


