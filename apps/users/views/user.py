from rest_framework import viewsets, mixins
from apps.users.models import CustomUser

from apps.store.permissions import IsNonAuthenticated
from apps.users.serializers import RegisterUserSerializer


class RegisterClientUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsNonAuthenticated]

