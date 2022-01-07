from rest_framework import viewsets, permissions, mixins
from store.models import Order, ProductInOrder, ReceiptOfPayment
from store.serializers import OrderSerializer, ProductInOrderSerializer, CreateOrderSerializer, \
    PayOrderByWalletSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()

    serializers = {
        'list': OrderSerializer,
        'create': CreateOrderSerializer,
        'retrieve': OrderSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers[self.action]

    def get_object(self):
        return self.queryset.filter(user=self.request.user)


class PayOrderByWalletViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ReceiptOfPayment.objects.all()
    serializer_class = PayOrderByWalletSerializer
    permission_classes = [permissions.IsAuthenticated]




