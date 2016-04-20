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


class isAdminOrRead(permissions.BasePermission):

    """Docstring for . """

    def has_permission(self, request, view):
        """TODO: Docstring for .

        :request: TODO
        :view: TODO
        :returns: TODO

        """
        isAdmin = request.user and request.user.is_staff

        if request.method in permissions.SAFE_METHODS:
            return True
        if isAdmin:
            return True
