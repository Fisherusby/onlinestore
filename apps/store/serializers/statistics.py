from rest_framework import serializers

from apps.store.models import Product
from apps.store.serializers import BrandSerializer, ProductCategorySerializer
from apps.store.serializers.product import OfferVendorSerializer, ProductImageSerializer


class PopularProductSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer()
    category = ProductCategorySerializer()
    images = ProductImageSerializer(many=True)
    offers = OfferVendorSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='AllProductViewSet-detail', lookup_field='slug')

    orders__count = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            'slug',
            'url',
            'full_name',
            'category',
            'model',
            'brand',
            'weight',
            'height',
            'width',
            'deep',
            'color',
            'images',
            'offers',
            'rating',
            'min_price',
            'max_price',
            'orders__count',
        )
