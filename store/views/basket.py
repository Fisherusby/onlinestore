from rest_framework import viewsets, mixins
from store.models import ProductInBasket, Basket
from store.serializers import BasketSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


