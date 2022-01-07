from rest_framework import serializers
from store.models import Product, OfferVendor, ReviewProduct, PhotoReviewProduct, FavoriteProduct, ProductImage
from .vendor import VendorSerializer
from .brand import BrandSerializer
from .product_category import ProductCategorySerializer
from django.shortcuts import get_object_or_404


class OfferVendorSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = OfferVendor
        fields = (
            'id',
            'vendor',
            'price',
            'price_in_currency',
        )

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'image',
        )


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer()
    category = ProductCategorySerializer()
    images = ProductImageSerializer(many=True)
    offers = OfferVendorSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='ProductViewSet',
        lookup_field='slug'
    )


    class Meta:
        model = Product
        fields = (
            'url',
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


class ProductToFavoriteSerializer(serializers.Serializer):
    slug = serializers.SlugField(max_length=255, min_length=None, allow_blank=False)

    def create(self, validated_data):
        product = get_object_or_404(Product, slug=validated_data['slug'])
        FavoriteProduct.objects.get_or_create(user=self.context['request'].user, product=product)

        return validated_data





