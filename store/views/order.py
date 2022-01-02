from rest_framework import viewsets, permissions, mixins
from store.models import Order, ProductInOrder
from store.serializers import OrderSerializer, ProductInOrderSerializer, CreateOrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()

    serializers = {
        'list': OrderSerializer,
        'create': CreateOrderSerializer,
        'retrieve': OrderSerializer,
    }
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers[self.action]

    def get_object(self):
     #   import pdb
      #  pdb.set_trace()
        return self.queryset.filter(user=self.request.user)


