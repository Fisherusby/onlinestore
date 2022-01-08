from rest_framework import viewsets, mixins

from store.models import Product
from store.serializers import ProductSerializer, PopularProductSerializer
from django.db.models import Count


class MostPopularProductsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all(). \
        annotate(Count('orders')).filter(orders__count__gt=0).order_by('-orders__count')[:5]
    serializer_class = PopularProductSerializer

