from rest_framework import viewsets, mixins

from info.models import Covid
from info.serializers import CovidSerializers


class CovidViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Covid.objects.all()
    serializer_class = CovidSerializers
    lookup_field = 'date'


