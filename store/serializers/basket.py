from rest_framework import serializers
from store.models import Basket, GoodsInBasket, Goods
from store.serializers import VendorSerializer

from store.serializers.product import OfferVendorSerializer


class TitleGoodsInBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = (
            'full_name',
            'slug',
        )


class GoodsInBasketSerializer(serializers.ModelSerializer):
    # offer = OfferVendorSerializer()
    goods = TitleGoodsInBasketSerializer()
    vendor = VendorSerializer()

    class Meta:
        model = GoodsInBasket
        fields = (
          #  'offer',
            'goods',
            'vendor',
            'count',
            'price_sum',
        )


class BasketSerializer(serializers.ModelSerializer):
    goods_in_basket = GoodsInBasketSerializer(many=True)

    class Meta:
        model = Basket
        fields = (
            'goods_in_basket',
            'last_update',
            'total_price',
        )