from rest_framework import serializers
from apps.store.models import Vendor


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='VendorViewSet',
        lookup_field='slug'
    )

    class Meta:
        model = Vendor
        fields = (
            'url',
            'name',
            'email',
            'address',
            'slug',
        )