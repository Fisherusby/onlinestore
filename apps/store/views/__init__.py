from .brand import BrandViewSet
from .product import (
    AllProductViewSet,
    FavoriteProductsViewSet,
    ProductReviewsViewSet,
    ProductToFavoriteViewSet,
    ReviewProductViewSet,
)
from .product_category import CategoryViewSet
from .statistics import MostPopularProductsViewSet

__all__ = (
    BrandViewSet,
    AllProductViewSet,
    FavoriteProductsViewSet,
    ProductReviewsViewSet,
    ProductToFavoriteViewSet,
    ReviewProductViewSet,
    MostPopularProductsViewSet,
    CategoryViewSet,
)
