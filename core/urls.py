from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", include("apps.frontend.urls")),
    path("api/store/", include("apps.store.urls")),
    # path('api/forum/', include('apps.forum.urls')),
    path("api/info/", include("apps.info.urls")),
    path("api/users/", include("apps.users.urls")),
    # path('api/wallet/', include('apps.wallet.urls')),
    path("admin/", admin.site.urls),
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
