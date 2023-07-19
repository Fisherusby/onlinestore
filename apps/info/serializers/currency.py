from rest_framework import serializers

from apps.info.models import ExchangeCurrency


class ExchangeCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeCurrency
        fields = (
            "currency",
            "rate",
            "scale",
            "date",
            "created_at",
        )
