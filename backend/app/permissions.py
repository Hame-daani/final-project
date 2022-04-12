from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
)


class isOwner(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return obj.user == request.user


class isSelf(BasePermission):

    # object permission
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and obj == request.user
