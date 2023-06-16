from rest_framework import mixins, viewsets

from apps.store.permissions import IsNonAuthenticated
from apps.users.models import CustomUser
from apps.users.serializers import RegisterUserSerializer


class RegisterClientUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsNonAuthenticated]
