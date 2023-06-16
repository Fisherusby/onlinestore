from .basket import BasketViewSet, ProductToBasketViewSet
from .brand import BrandViewSet
from .order import OrderViewSet, PayOrderByCardViewSet, PayOrderByWalletViewSet
from .product import (
    AllProductViewSet,
    FavoriteProductsViewSet,
    ProductReviewsViewSet,
    ProductToFavoriteViewSet,
    ProductViewSet,
    ReviewProductViewSet,
)
from .product_category import CategoryViewSet
from .statistics import MostPopularProductsViewSet
from .vendor import ListVendorViewSet, VendorViewSet
