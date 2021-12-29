from rest_framework import viewsets, mixins

from store.models import Goods, ReviewGoods
from store.serializers import GoodsSerializer, ReviewGoodsSerializer, GoodsReviewsSerializer


class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    lookup_field = 'slug'


class ReviewGoodsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsReviewsSerializer
