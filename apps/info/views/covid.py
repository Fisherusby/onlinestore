from rest_framework import viewsets, mixins

from apps.info.models import Covid
from apps.info.serializers import CovidSerializers


class CovidViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Covid.objects.all()
    serializer_class = CovidSerializers
    lookup_field = 'date'


