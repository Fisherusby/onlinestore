import datetime

from django.http import Http404
from rest_framework import mixins, viewsets

from apps.info.models import ExchangeCurrency
from apps.info.serializers import ExchangeCurrencySerializer
from apps.info.services import update_currency
from apps.users.permissions import IsAdminUserOrReadOnly


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
