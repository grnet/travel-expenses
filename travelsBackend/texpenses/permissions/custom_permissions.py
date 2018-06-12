from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    """
    Object-level permission to only allow owners of an object to edit/retrieve
    delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
