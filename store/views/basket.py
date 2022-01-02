from rest_framework import viewsets, mixins, permissions
from store.models import ProductInBasket, Basket
from store.serializers import BasketSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


