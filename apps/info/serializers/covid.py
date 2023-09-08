from rest_framework import serializers

from apps.info.models import Covid


class CovidSerializers(serializers.ModelSerializer):
    class Meta:
        model = Covid
        fields = (
            'date',
            'infected',
            'deaths',
            'recovered',
            'sick',
        )
