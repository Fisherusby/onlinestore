from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsNonAuthenticated(BasePermission):
    """Allows access only to authenticated users."""

    def has_permission(self, request, view):
        return bool(not (request.user and request.user.is_authenticated))


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.user == request.user)


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_profile.is_client)


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_profile.is_vendor)


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_authenticated and request.user.is_staff
        )
