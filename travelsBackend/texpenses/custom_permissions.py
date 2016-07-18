from rest_framework import permissions


class SubmissionPermissions(permissions.BasePermission):

    """Docstring for SubmissionPermissions. """
    SUBMISSION_SAFE_METHODS = permissions.SAFE_METHODS + tuple('POST')

    def has_permission(self, request, view):
        return request.user or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        request_user = request.user
        user_groups = request_user.groups.all()
        if user_groups:
            groups = [group.name for group in user_groups]

        return obj.user == request.user or request.user.is_staff or\
            'SECRETARY' in groups \
            and request.method in self.SUBMISSION_SAFE_METHODS


class IsOwnerOrAdmin(permissions.BasePermission):

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return request.user or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        request_user = request.user
        user_groups = request_user.groups.all()
        if user_groups:
            groups = [group.name for group in user_groups]

        if request.method == 'DELETE' and not request.user.is_staff:
            return False

        return obj.user == request.user or request.user.is_staff or\
            'SECRETARY' in groups


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
        return False
