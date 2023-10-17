from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_superuser)


class IsCurrentUserOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.pk == request.user.pk
                    or request.user.is_superuser)


class IsCurrentUserOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.pk == request.user.pk
                or request.user.is_superuser)
