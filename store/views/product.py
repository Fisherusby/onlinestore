from rest_framework import viewsets, mixins

from store.models import Goods, ReviewGoods
from store.serializers import GoodsSerializer, ReviewGoodsSerializer


class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    lookup_field = 'slug'

    # def get_queryset(self):
    #     # import pdb
    #     # pdb.set_trace()
    #     return self.queryset.filter(slug=self.kwargs['slug'])


class ReviewGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ReviewGoods.objects.all()
    serializer_class = ReviewGoodsSerializer
    # lookup_field = 'goods__pk'