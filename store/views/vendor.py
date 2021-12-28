from rest_framework import mixins, viewsets

from store.serializers import VendorSerializer
from store.models import Vendor


class VendorViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


    def get_queryset(self):
        # import pdb
        # pdb.set_trace()
        return self.queryset.filter(pk=self.kwargs['pk'])

