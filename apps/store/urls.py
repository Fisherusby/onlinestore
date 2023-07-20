from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.store.views import (
    AllProductViewSet,
    BrandViewSet,
    CategoryViewSet,
    FavoriteProductsViewSet,
    MostPopularProductsViewSet,
    ProductReviewsViewSet,
    ProductToFavoriteViewSet,
    ProductViewSet,
    ReviewProductViewSet,
)

router = DefaultRouter()


router.register("products", AllProductViewSet, basename="AllProductViewSet")
router.register("category", CategoryViewSet, basename="CategoryViewSet")
router.register("brand", BrandViewSet, basename="BrandViewSet")

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
    "popular_products",
    MostPopularProductsViewSet,
    basename="MostPopularProductsViewSet",
)


urlpatterns = [
    path("", include(router.urls)),
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
