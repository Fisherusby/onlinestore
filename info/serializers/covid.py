from rest_framework import serializers

from info.models import Covid


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
