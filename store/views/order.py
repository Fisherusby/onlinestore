from rest_framework import viewsets
from store.models import Order, GoodsInOrder
from store.serializers import OrderSerializer, GoodsInOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
     #   import pdb
      #  pdb.set_trace()
        return self.queryset.filter(user=self.request.user)


