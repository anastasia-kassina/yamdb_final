from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """Разрешения для пользователей с правами администатора"""

    def has_permission(self, request, view):
        return (
            request.user.is_staff or (
                request.user.is_authenticated and request.user.is_admin
            )
        )


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """Разрешения для пользователей с правами администатора и нет"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin
            )
        )


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """Разрешение для пользователей с правами администратора, модератора
    или автора.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
