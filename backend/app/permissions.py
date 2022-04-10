from rest_framework.permissions import BasePermission, SAFE_METHODS


class isOwner(BasePermission):

    # object permission
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class isSelf(BasePermission):

    # object permission
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj == request.user
