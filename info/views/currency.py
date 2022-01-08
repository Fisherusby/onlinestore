import datetime

from info.models import ExchangeCurrency
from info.serializers import ExchangeCurrencySerializer
from rest_framework import viewsets, mixins

from info.tools.currency import update_currency
from store.permissions import IsAdminUserOrReadOnly
from django.http import Http404


class ExchangeCurrencyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeCurrency.objects.all()
    serializer_class = ExchangeCurrencySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TodayExchangeCurrencyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeCurrency.objects.all()
    serializer_class = ExchangeCurrencySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'currency'

    def get_queryset(self):
        last = self.queryset.last()
        if last:
            date_today = datetime.date.today()
            if date_today != last.date:
                update_currency()
            return self.queryset.filter(date=date_today)
        else:
            raise Http404

