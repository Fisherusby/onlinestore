from rest_framework import viewsets, mixins
from store.serializers import CategorySerializer
from store.models import Category


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(parent=None)

