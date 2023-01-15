from rest_framework import viewsets, mixins
from users.models import CustomUser

from store.permissions import IsNonAuthenticated
from users.serializers import RegisterUserSerializer


class RegisterClientUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsNonAuthenticated]

