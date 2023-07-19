from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.store.views import (
    AllProductViewSet,
    BasketViewSet,
    BrandViewSet,
    CategoryViewSet,
    FavoriteProductsViewSet,
    ListVendorViewSet,
    MostPopularProductsViewSet,
    OrderViewSet,
    PayOrderByCardViewSet,
    PayOrderByWalletViewSet,
    ProductReviewsViewSet,
    ProductToBasketViewSet,
    ProductToFavoriteViewSet,
    ProductViewSet,
    ReviewProductViewSet,
    VendorViewSet,
)

router = DefaultRouter()


router.register("products", AllProductViewSet, basename="AllProductViewSet")
router.register("category", CategoryViewSet, basename="CategoryViewSet")
router.register("brand", BrandViewSet, basename="BrandViewSet")
router.register("user/basket", BasketViewSet, basename="BasketViewSet")
router.register("user/to_basket", ProductToBasketViewSet, basename="ProductToBasketViewSet")
router.register("user/order", OrderViewSet, basename="OrderViewSet")
router.register("product/reviews", ProductReviewsViewSet, basename="ProductReviewsViewSet")
router.register("product/review", ReviewProductViewSet, basename="ReviewProductViewSet")
router.register(
    "user/favorite/product",
    ProductToFavoriteViewSet,
    basename="ProductToFavoriteViewSet",
)
router.register(
    "user/favorite/products",
    FavoriteProductsViewSet,
    basename="FavoriteProductsViewSet",
)

router.register(
    "user/payment/wallet",
    PayOrderByWalletViewSet,
    basename="PayOrderByWalletViewSet",
)
router.register("user/payment/card", PayOrderByCardViewSet, basename="PayOrderByCardViewSet")

router.register(
    "popular_products",
    MostPopularProductsViewSet,
    basename="MostPopularProductsViewSet",
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "vendor/<slug:slug>",
        VendorViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="VendorViewSet",
    ),
    path("vendor", ListVendorViewSet.as_view(), name="ListVendorViewSet"),
    path(
        "product/detail/<slug:slug>/",
        ProductViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="ProductViewSet",
    ),
]
