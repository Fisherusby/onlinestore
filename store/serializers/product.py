from rest_framework import serializers
from store.models import Product, OfferVendor, ReviewProduct, PhotoReviewProduct, FavoriteProduct
from .vendor import VendorSerializer
from .brand import BrandSerializer
from .product_category import ProductCategorySerializer
from django.shortcuts import get_object_or_404


class OfferVendorSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = OfferVendor
        fields = (
            'vendor',
            'price',
            'price_currency',
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = ProductCategorySerializer()
    offers = OfferVendorSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'full_name',
            'category',
            'model',
            'brand',
            'slug',
            'images',
            'offers',
            'rating',
            'min_price',
            'max_price',
        )
        lookup_field = 'slug'


class PhotoReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoReviewProduct
        fields = (
            'photo',
        )


class ReviewProductSerializer(serializers.ModelSerializer):
    photos = PhotoReviewProductSerializer(many=True)

    class Meta:
        model = ReviewProduct
        fields = (
            'user',
            'rating',
            'review_text',
            'title',
            'plus',
            'minus',
            'created_date',
            'photos',
        )


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewProductSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'reviews',
        )


# class FavoriteProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = (
#             'user',
#             'product',
#         )
#
#
# class ChangeFavoriteProductSerializer(serializers.Serializer):
#     slug = serializers.SlugField(max_length=255, min_length=None, allow_blank=False)


class ProductToFavoriteSerializer(serializers.Serializer):
    slug = serializers.SlugField(max_length=255, min_length=None, allow_blank=False)

    def create(self, validated_data):
        product = get_object_or_404(Product, slug=validated_data['slug'])
        FavoriteProduct.objects.get_or_create(user=self.context['request'].user, product=product)

        return validated_data





