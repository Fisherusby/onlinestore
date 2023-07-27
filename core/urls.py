from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

schema_view = get_schema_view(
    openapi.Info(
        title="OnlineStore API",
        default_version="v0.1",
        description="Pet project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("", include("apps.frontend.urls")),
    path("api/store/", include("apps.store.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/vendors/", include("apps.vendors.urls")),
    path("api/info/", include("apps.info.urls")),
    path("api/users/", include("apps.users.urls")),
    # path("admin/", admin.site.urls),
    path('api/auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += (
        path(
            "docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
