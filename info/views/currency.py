import datetime

from info.models import ExchangeCurrency
from info.serializers import ExchangeCurrencySerializer
from rest_framework import viewsets, mixins
from store.permissions import IsAdminUserOrReadOnly


class ExchangeCurrencyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeCurrency.objects.all()
    serializer_class = ExchangeCurrencySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TodayExchangeCurrencyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeCurrency.objects.all()
    serializer_class = ExchangeCurrencySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        date_today = datetime.date.today()
        return self.queryset.filter(date=date_today)

