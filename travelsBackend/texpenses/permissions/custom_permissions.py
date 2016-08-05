from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return request.user or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
