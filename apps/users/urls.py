from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views.user import RegisterClientUserViewSet

router = DefaultRouter()
router.register("register", RegisterClientUserViewSet, basename="RegisterClientUserViewSet")

urlpatterns = [
    path("", include(router.urls)),
    path(
        r"password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
