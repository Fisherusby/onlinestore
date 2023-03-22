from rest_framework import viewsets, permissions, mixins
from apps.store.models import Order, ReceiptOfPayment
from apps.store.serializers import RetrieveOrderSerializer, ListOrderSerializer, CreateOrderSerializer, \
    PayOrderByWalletSerializer, PayOrderByCardSerializer

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()

    serializers = {
        'list': ListOrderSerializer,
        'create': CreateOrderSerializer,
        'retrieve': RetrieveOrderSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers[self.action]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user, pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404


class PayOrderByWalletViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ReceiptOfPayment.objects.all()
    serializer_class = PayOrderByWalletSerializer
    permission_classes = [permissions.IsAuthenticated]


class PayOrderByCardViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ReceiptOfPayment.objects.all()
    serializer_class = PayOrderByCardSerializer
    permission_classes = [permissions.IsAuthenticated]






