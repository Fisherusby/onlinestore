from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from apps.store.models import Basket, ProductInBasket
from apps.store.serializers import (
    BasketSerializer,
    CreateBasketSerializer,
    ProductToBasket,
)


class BasketViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Basket.objects.all()
    serializers = {
        "list": BasketSerializer,
        "create": CreateBasketSerializer,
        "update": CreateBasketSerializer,
        "retrieve": BasketSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers[self.action]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProductToBasketViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = ProductInBasket.objects.all()
    serializer_class = ProductToBasket
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        prodict_in_basket = get_object_or_404(
            ProductInBasket,
            basket__user=request.user,
            pk=self.kwargs["pk"],
        )
        if prodict_in_basket.count <= 1:
            prodict_in_basket.delete()
        else:
            prodict_in_basket.count -= 1
            prodict_in_basket.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
