from django.urls import path, include
from rest_framework.routers import DefaultRouter

from info.views import ExchangeCurrencyViewSet, TodayExchangeCurrencyViewSet, CovidViewSet
from store.views import VendorViewSet, BasketViewSet, CategoryViewSet, ProductViewSet, BrandViewSet, OrderViewSet, \
    ProductReviewsViewSet, ListVendorViewSet, ProductToFavoriteViewSet, FavoriteProductsViewSet, ProductToBasketViewSet, \
    PayOrderByWalletViewSet, ReviewProductViewSet, MostPopularProductsViewSet, AllProductViewSet, PayOrderByCardViewSet
from users.views.user import RegisterClientUserViewSet



router = DefaultRouter()


router.register('store/products', AllProductViewSet, basename='AllProductViewSet')

# router.register('vendor', VendorViewSet, basename="VendorViewSet")
router.register('store/category', CategoryViewSet, basename="CategoryViewSet")
router.register('store/brand', BrandViewSet, basename='BrandViewSet')
router.register('store/user/basket', BasketViewSet, basename='BasketViewSet')
router.register('store/user/to_basket', ProductToBasketViewSet, basename='ProductToBasketViewSet')
router.register('store/user/order', OrderViewSet, basename='OrderViewSet')
router.register('store/product/reviews', ProductReviewsViewSet, basename='ProductReviewsViewSet')
router.register('store/product/review', ReviewProductViewSet, basename='ReviewProductViewSet')
router.register('store/user/favorite/product', ProductToFavoriteViewSet, basename='ProductToFavoriteViewSet')
router.register('store/user/favorite/products', FavoriteProductsViewSet, basename='FavoriteProductsViewSet')

router.register('store/user/payment/wallet', PayOrderByWalletViewSet, basename='PayOrderByWalletViewSet')
router.register('store/user/payment/card', PayOrderByCardViewSet, basename='PayOrderByCardViewSet')



router.register('info/currency', TodayExchangeCurrencyViewSet, basename='ExchangeCurrencyViewSet')
router.register('info/covid', CovidViewSet, basename='CovidViewSet')
router.register('info/popular_products', MostPopularProductsViewSet, basename='MostPopularProductsViewSet')
# router.register('currency/today', TodayExchangeCurrencyViewSet, basename='TodayExchangeCurrencyViewSet')

router.register('user/register', RegisterClientUserViewSet, basename='RegisterClientUserViewSet')


urlpatterns = [
    path('', include(router.urls)),
    path(r'user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('store/vendor/<slug:slug>',
         VendorViewSet.as_view({'get': 'retrieve', }), name='VendorViewSet'),
    path('store/vendor',
         ListVendorViewSet.as_view(), name='ListVendorViewSet'),
    # path('store/products/category/<slug:cat_slug>/',
    #      ProductViewSet.as_view({'get': 'list', }), name='ProductViewSet'),
    path('store/product/detail/<slug:slug>/',
         ProductViewSet.as_view({'get': 'retrieve', }), name='ProductViewSet'),
]


