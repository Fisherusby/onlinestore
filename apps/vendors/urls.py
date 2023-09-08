from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.vendors.views import ListVendorViewSet, VendorViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        '<slug:slug>',
        VendorViewSet.as_view(
            {
                'get': 'retrieve',
            }
        ),
        name='VendorViewSet',
    ),
    path('', ListVendorViewSet.as_view(), name='ListVendorViewSet'),
]
