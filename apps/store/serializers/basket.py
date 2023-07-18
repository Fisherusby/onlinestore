from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.store.models import Basket, OfferVendor, Product, ProductInBasket, Vendor


class ShortProductInBasketSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="ProductViewSet",
        lookup_field="slug",
    )

    class Meta:
        model = Product
        fields = (
            "url",
            "full_name",
            "slug",
        )


class ShortVendorProductInBasketSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="VendorViewSet", lookup_field="slug")

    class Meta:
        model = Vendor
        fields = (
            "url",
            "name",
            "slug",
        )


class ProductInBasketSerializer(serializers.ModelSerializer):
    product = ShortProductInBasketSerializer()
    vendor = ShortVendorProductInBasketSerializer()

    class Meta:
        model = ProductInBasket
        fields = (
            "id",
            "product",
            "vendor",
            "count",
            "price_in_currency",
        )


class BasketSerializer(serializers.ModelSerializer):
    products_in_basket = ProductInBasketSerializer(many=True)

    class Meta:
        model = Basket
        fields = (
            "products_in_basket",
            "last_update",
            "total_price",
        )


class ProductCreateProductInBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("slug",)


class VendorCreateProductInBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("slug",)


class CreateProductInBasketSerializer(serializers.ModelSerializer):
    # product = ProductCreateProductInBasketSerializer(read_only=True)
    # vendor = VendorCreateProductInBasketSerializer(read_only=True)

    class Meta:
        model = ProductInBasket
        fields = (
            "offer",
            "count",
            "price_in_currency",
        )


class CreateBasketSerializer(serializers.ModelSerializer):
    products_in_basket = CreateProductInBasketSerializer(many=True)

    class Meta:
        model = Basket
        fields = (
            "products_in_basket",
            "total_price",
        )

    def create(self, validated_data):
        try:
            basket = Basket.objects.filter(user=self.context["request"].user).last()
        except ObjectDoesNotExist:
            basket = Basket.objects.create(user=self.context["request"].user)

        for pib in validated_data["products_in_basket"]:
            import pdb

            pdb.set_trace()
            ProductInBasket.objects.create(basket=basket, offer=pib["offer"], count=pib["count"])

        return basket


class ProductToBasket(serializers.Serializer):
    vendor = serializers.SlugField(max_length=255, min_length=None, allow_blank=False)
    product = serializers.SlugField(max_length=255, min_length=None, allow_blank=False)

    def create(self, validated_data):
        try:
            offer = OfferVendor.objects.get(
                vendor__slug=validated_data["vendor"],
                product__slug=validated_data["product"],
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError("offer_not_found")

        try:
            basket = Basket.objects.get(user=self.context["request"].user)
        except ObjectDoesNotExist:
            basket = Basket.objects.create(user=self.context["request"].user)

        try:
            product_in_basket = ProductInBasket.objects.get(
                basket=basket,
                offer=offer,
            )
            product_in_basket.count += 1
            product_in_basket.save()
        except ObjectDoesNotExist:
            product_in_basket = ProductInBasket.objects.create(
                basket=basket,
                offer=offer,
                count=1,
            )

        return product_in_basket
