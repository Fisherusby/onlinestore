from rest_framework import serializers
from store.models import Basket, ProductInBasket, Product
from store.serializers import VendorSerializer

from store.serializers.product import OfferVendorSerializer


class TitleProductInBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'full_name',
            'slug',
        )


class ProductInBasketSerializer(serializers.ModelSerializer):
    product = TitleProductInBasketSerializer()
    vendor = VendorSerializer()

    class Meta:
        model = ProductInBasket
        fields = (
            'product',
            'vendor',
            'count',
            'price_sum',
        )


class BasketSerializer(serializers.ModelSerializer):
    products_in_basket = ProductInBasketSerializer(many=True)

    class Meta:
        model = Basket
        fields = (
            'products_in_basket',
            'last_update',
            'total_price',
        )

