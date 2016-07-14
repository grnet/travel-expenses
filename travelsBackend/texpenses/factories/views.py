from rest_framework import viewsets
from rest_framework import filters

from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.factories import utils
from texpenses.factories.serializers import factory as serializer_factory

DEFAULT_QUERYSET = lambda model: model.objects.all()
FILTERING_BACKENDS = {
    'filter_fields': filters.DjangoFilterBackend,
    'search_fields': filters.SearchFilter,
    'ordering_fields': filters.OrderingFilter
}
FIELDS_TO_OVERRIDE = [('filter_fields', None), ('ordering_fields', None),
                      ('search_fields', None), ('ordering', None)]
METHODS_TO_OVERRIDE = ['create', 'update', 'delete']
CUSTOM_VIEWS_CODE = 'texpenses.views'


def factory(model_class, custom_permission, api_name='APITravel', nested=None,
            serializer_module=None):
    """TODO: Docstring for viewset_factory.

    :model_class: TODO
    :returns: A ModelViewSet viewset

    """
    class AbstractViewSet(LoggingMixin, viewsets.ModelViewSet):

        if model_class is None:
            raise Exception

        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (IsAuthenticated,) + (custom_permission,) + (
            DjangoModelPermissions,)

        queryset = model_class.objects.all()
        filter_backends = ()
        model_meta = getattr(model_class, api_name)
        serializer_class = serializer_factory(model_class, nested,
                                              serializer_module)

        def get_queryset(self):
            queryset = getattr(self.model_meta, 'get_queryset', None)
            return queryset(self.request.user) if queryset else\
                DEFAULT_QUERYSET(model_class)

    utils.override_fields(AbstractViewSet, AbstractViewSet.model_meta,
                          FIELDS_TO_OVERRIDE)
    init_filter_backends(AbstractViewSet)
    module_name = utils.camel2snake(model_class.__name__)
    module = utils.get_package_module(
        CUSTOM_VIEWS_CODE + '.' + module_name)
    utils.override_methods(AbstractViewSet, module, METHODS_TO_OVERRIDE)
    AbstractViewSet.__name__ = model_class.__name__
    return AbstractViewSet


def init_filter_backends(cls):
    """
    Initialize the corresponding Django filter backends if the corresponding
    fields of the viewset class have been assigned.

    :param cls: Viewset class.
    """
    assert cls.filter_backends == ()
    for filter_option, filter_backend in FILTERING_BACKENDS.iteritems():
        value = getattr(cls, filter_option, None)
        if value:
            cls.filter_backends += (filter_backend,)
