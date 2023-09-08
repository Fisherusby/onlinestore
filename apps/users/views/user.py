from rest_framework import mixins, viewsets

from apps.users.models import CustomUser
from apps.users.permissions import IsNonAuthenticated
from apps.users.serializers import RegisterUserSerializer


class RegisterClientUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # TODO Response without password hash
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsNonAuthenticated]
