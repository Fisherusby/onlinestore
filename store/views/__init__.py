from .vendor import VendorViewSet, ListVendorViewSet
from .product_category import CategoryViewSet
from .product import ProductViewSet, ProductReviewsViewSet, ProductToFavoriteViewSet, FavoriteProductsViewSet,\
    ReviewProductViewSet, AllProductViewSet
from .brand import BrandViewSet
from .basket import BasketViewSet, ProductToBasketViewSet
from .order import OrderViewSet, PayOrderByWalletViewSet
from .statistics import MostPopularProductsViewSet


