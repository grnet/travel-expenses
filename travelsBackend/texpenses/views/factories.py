from rest_framework import viewsets
from rest_framework import filters

from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import isAdminOrRead, IsOwnerOrAdmin
from texpenses.serializers.factories import modelserializer_factory

DEFAULT_QUERYSET = lambda model: model.objects.all()


def viewset_factory(model_class, custom_permission, api_name='APITravel',
                    **kwargs):
    """TODO: Docstring for viewset_factory.

    :model_class: TODO
    :returns: A ModelViewSet viewset

    """
    class AbstractViewSet(LoggingMixin, viewsets.ModelViewSet):

        """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user) """
        if model_class is None:
            raise Exception

        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (IsAuthenticated,) + (custom_permission,) + (
            DjangoModelPermissions,)
        queryset = model_class.objects.all()
        model_meta = getattr(model_class, api_name)
        filter_fields = getattr(model_meta, 'filter_fields', None)
        search_fields = getattr(model_meta, 'search_fields', None)
        ordering_fields = getattr(model_meta, 'ordering_fields', None)
        ordering = getattr(model_meta, 'ordering', None)
        filter_backends = ()

        if filter_fields:
            filter_backends += (filters.DjangoFilterBackend,)
        if search_fields:
            filter_backends += (filters.SearchFilter,)
        if ordering_fields:
            filter_backends += (filters.OrderingFilter,)
        serializer_class = modelserializer_factory(model_class)

        def get_queryset(self):
            queryset = getattr(self.model_meta, 'get_queryset', None)
            return queryset(self.request.user) if queryset else\
                DEFAULT_QUERYSET(model_class)

    return AbstractViewSet
