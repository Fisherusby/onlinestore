from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.store.models import (
    FavoriteProduct,
    OfferVendor,
    PhotoReviewProduct,
    Product,
    ProductImage,
    ReviewProduct,
)
from apps.vendors.serializers.vendor import VendorSerializer

from .brand import BrandSerializer
from .product_category import ProductCategorySerializer


class OfferVendorSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = OfferVendor
        fields = (
            "id",
            "vendor",
            "price",
            "price_in_currency",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer()
    category = ProductCategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    offers = OfferVendorSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="ProductViewSet", lookup_field="slug")

    class Meta:
        model = Product
        fields = (
            "slug",
            "url",
            "full_name",
            "category",
            "model",
            "brand",
            "weight",
            "height",
            "width",
            "deep",
            "color",
            "production",
            "images",
            "offers",
            "rating",
            "min_price",
            "max_price",
        )
        lookup_field = "slug"


class PhotoReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoReviewProduct
        fields = ("photo",)


class ReviewProductSerializer(serializers.ModelSerializer):
    photos = PhotoReviewProductSerializer(many=True)

    class Meta:
        model = ReviewProduct
        fields = (
            "id",
            "user",
            "rating",
            "review_text",
            "title",
            "plus",
            "minus",
            "created_at",
            "photos",
        )


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewProductSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "slug",
            "reviews",
        )


class UpdateReviewProductSerializer(serializers.ModelSerializer):
    photos = PhotoReviewProductSerializer(many=True, read_only=True)

    class Meta:
        model = ReviewProduct
        fields = (
            "id",
            "user",
            "rating",
            "review_text",
            "title",
            "plus",
            "minus",
            "created_at",
            "photos",
        )


class CreateReviewProductSerializer(serializers.ModelSerializer):
    photos = PhotoReviewProductSerializer(many=True, read_only=True)
    slug = serializers.SlugField(max_length=255, min_length=1)

    class Meta:
        model = ReviewProduct
        fields = (
            "slug",
            "rating",
            "review_text",
            "title",
            "plus",
            "minus",
            "created_at",
            "photos",
        )

    def validate_slug(self, v):
        try:
            self._product = Product.objects.get(slug=v)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Product_not_found")
        return v

    def create(self, validated_data):
        try:
            review = ReviewProduct.objects.get(product=self._product, user=self.context["request"].user)
            raise serializers.ValidationError("Forbidden_more_than_once")
        except ObjectDoesNotExist:
            review = ReviewProduct.objects.create(
                product=self._product,
                user=self.context["request"].user,
                rating=validated_data["rating"],
                review_text=validated_data["review_text"],
                title=validated_data["title"],
                plus=validated_data["plus"],
                minus=validated_data["minus"],
            )
            review.slug = validated_data["slug"]

        return review


class ProductToFavoriteSerializer(serializers.Serializer):
    slug = serializers.SlugField(max_length=255, min_length=None, allow_blank=False)

    def create(self, validated_data):
        product = get_object_or_404(Product, slug=validated_data["slug"])
        FavoriteProduct.objects.get_or_create(user=self.context["request"].user, product=product)

        return validated_data
