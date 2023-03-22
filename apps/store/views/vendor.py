from rest_framework import mixins, viewsets
from rest_framework import generics, permissions
from apps.store.serializers import VendorSerializer
from apps.store.models import Vendor
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class VendorViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'slug'

    def get_object(self):
        try:
            return self.queryset.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404


class ListVendorViewSet(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permissions = [permissions.IsAdminUser]

