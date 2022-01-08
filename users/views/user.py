from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from store.permissions import IsNonAuthenticated
from users.serializers import RegisterUserSerializer


class RegisterClientUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [IsNonAuthenticated]

