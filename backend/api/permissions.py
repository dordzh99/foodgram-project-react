from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_superuser)


class IsCurrentUserOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj == request.user
                    or request.user.is_superuser)
        return False


class IsUserOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj == request.user
                or request.user.is_superuser)
