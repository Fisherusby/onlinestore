from rest_framework import serializers

from apps.store.models import Brand, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'name',
            'logo',
            'slug',
        )
        lookup_field = 'slug'


class BrandProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
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
    products = BrandProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = (
            'name',
            'logo',
            'slug',
            'products',
        )

