from rest_framework import serializers
from apps.info.models import ExchangeCurrency

# currency = models.CharField(max_length=3)
# rate = models.DecimalField(max_digits=7, decimal_places=4)
# scale = models.PositiveIntegerField(default=1)
# created_date = models.DateTimeField(auto_now_add=True)
# date = models.DateField(default='1900-01-01')


class ExchangeCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeCurrency
        fields = (
            'currency',
            'rate',
            'scale',
            'date',
            'created_date',
        )
