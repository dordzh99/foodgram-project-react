from rest_framework.permissions import BasePermission


class IsAuthorOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or obj.author == request.user
                or request.user.is_superuser)
