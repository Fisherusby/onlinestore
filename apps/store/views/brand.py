from rest_framework import mixins, viewsets

from apps.store.models import Brand
from apps.store.serializers import BrandSerializer, RetrieveBrandSerializer


class BrandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all().order_by("name")
    serializers = {
        "list": BrandSerializer,
        "retrieve": RetrieveBrandSerializer,
    }
    lookup_field = "slug"

    def get_serializer_class(self):
        return self.serializers[self.action]
