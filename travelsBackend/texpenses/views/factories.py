from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import isAdminOrRead
from texpenses.serializers.factories import modelserializer_factory


class AbstractViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user) """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    model=None
    queryset =
    fields = ('name', 'id', 'url', )
    serializer_class = modelserializer_factory(Specialty, fields)
