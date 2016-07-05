from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import isAdminOrRead
from texpenses.serializers.factories import modelserializer_factory


def viewset_factory(model_class, api_name='APITravel', **kwargs):
    """TODO: Docstring for viewset_factory.

    :model_class: TODO
    :returns: A ModelViewSet viewset

    """
    class AbstractFilter(filters.FilterSet):

        class Meta:
            model = model_class

        model_meta = getattr(model_class, api_name)
        filter_fields = getattr(model_meta, 'filter_fields', ())

        setattr(Meta, 'fields', filter_fields)

    class AbstractViewSet(LoggingMixin, viewsets.ModelViewSet):

        """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user) """
        if model_class is None:
            raise Exception

        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (
            IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
        queryset = model_class.objects.all()

        if AbstractFilter.Meta.fields:
            filter_backends = (filters.DjangoFilterBackend,)
            filter_class = AbstractFilter
        serializer_class = modelserializer_factory(model_class)

    return AbstractViewSet
