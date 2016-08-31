from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.factories import utils
from texpenses.factories.serializers import factory as serializer_factory


FILTERING_BACKENDS = {
    'filter_fields': filters.DjangoFilterBackend,
    'search_fields': filters.SearchFilter,
    'ordering_fields': filters.OrderingFilter
}
VIEWSET_ATTRS = [('filter_fields', None), ('ordering_fields', None),
                 ('search_fields', None), ('ordering', None)]
CUSTOM_VIEWS_CODE = 'texpenses.views'


MIXINS = {
    'create': mixins.CreateModelMixin,
    'list': mixins.ListModelMixin,
    'retrieve': mixins.RetrieveModelMixin,
    'update': mixins.UpdateModelMixin,
    'delete': mixins.DestroyModelMixin
}


def factory(model_class, custom_permissions=(), api_name='APITravel',
            serializer_module_name=None):
    """TODO: Docstring for viewset_factory.

    :model_class: TODO
    :returns: A ModelViewSet viewset

    """
    if not model_class:
        raise Exception

    model_api_meta = getattr(model_class, api_name)
    assert model_api_meta is not None
    class_dict = {
        'authentication_classes': (SessionAuthentication, TokenAuthentication),
        'permission_classes': (IsAuthenticated,) + custom_permissions + (
            DjangoModelPermissions,),
        'queryset': model_class.objects.all(),
        'filter_backends': (),
        'model_api_meta': getattr(model_class, api_name),
        'serializer_class': serializer_factory(
            model_class, serializer_module_name),
    }
    cls = type(model_class.__name__, get_bases_classes(model_api_meta),
               class_dict)
    utils.set_attrs(cls, cls.model_api_meta, VIEWSET_ATTRS)
    init_filter_backends(cls)
    module_name = utils.camel2snake(model_class.__name__)
    module = utils.get_package_module(
        CUSTOM_VIEWS_CODE + '.' + module_name)
    utils.bound_methods(cls, module)
    return cls


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


def get_bases_classes(model_api_meta):
    """
    This function gets the corresponding base classes in order to construct
    the viewset class.

    A model can specify the allowed operations to it, e.g. update,
    list, delete, etc. Then, a viewset specify the allowed methods based on
    model's allowed operations by defining the corresponding bases classes.

    By default, all methods are allowed.

    :param model_api_meta: API class of model.
    :returns: A tuple of the corresponding base classes.
    """
    bases = (LoggingMixin,)
    operations = getattr(model_api_meta, 'allowed_operations', None)
    bases += (viewsets.ModelViewSet,) if not operations\
        else tuple([MIXINS[operation] for operation in operations]) + (
            viewsets.GenericViewSet,)
    return bases
