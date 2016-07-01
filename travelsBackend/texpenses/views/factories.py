from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework_tracking.mixins import LoggingMixin

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import isAdminOrRead
from texpenses.serializers.factories import modelserializer_factory


def viewset_factory(mdl, **kwargs):
    """TODO: Docstring for viewset_factory.

    :model: TODO
    :returns: A ModelViewSet viewset

    """

    class AbstractViewSet(LoggingMixin, viewsets.ModelViewSet):

        """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user) """
        if mdl is None:
            raise Exception

        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (
            IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
        queryset = mdl.objects.all()
        serializer_class = modelserializer_factory(mdl)

    return AbstractViewSet
