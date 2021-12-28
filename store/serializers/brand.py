from rest_framework import serializers

from store.models import Brand, Goods


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'name',
            'logo',
            'slug',
        )
        lookup_field = 'slug'


class BrandGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = (
            'full_name',
            'model',
            'slug',
            'images',
            'rating',
            'min_price',
            'max_price',
        )


class RetrieveBrandSerializer(serializers.ModelSerializer):
   # goods = BrandGoodsSerializer(many=True)

    class Meta:
        model = Brand
        fields = (
            'name',
            'logo',
            'slug',
     #       'goods'
        )