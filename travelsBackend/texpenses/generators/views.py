from django.conf import settings
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from texpenses.generators import utils
from texpenses.generators.serializers import generate as generate_serializer


FILTERING_BACKENDS = {
    'filter_fields': filters.DjangoFilterBackend,
    'search_fields': filters.SearchFilter,
    'ordering_fields': filters.OrderingFilter
}
VIEWSET_ATTRS = [('filter_fields', None), ('ordering_fields', None),
                 ('search_fields', None), ('ordering', None)]


MIXINS = {
    'create': mixins.CreateModelMixin,
    'list': mixins.ListModelMixin,
    'retrieve': mixins.RetrieveModelMixin,
    'update': mixins.UpdateModelMixin,
    'delete': mixins.DestroyModelMixin,
}
CACHING_MIXIN = CacheResponseMixin


PACKAGE_LOOKUP_FIELD = 'viewset_code'
MODULE_LOOKUP_FIELD = 'viewset_module_name'
API_CLS_NAME = getattr(settings, 'API_PREFIX', 'api').capitalize()


def generate(model_class):
    """
    A function to generate a viewset according to the model given as
    parameter.

    It constructs a serializer class according to this model and configuration
    of viewset (which methods are allowable, queryset, possible
    filtering/ordering/search fields) is defined inside `API`
    inner class of the specified model.

    `API` class may also define package or module where custom implementation
    is located and should be bound to the generated class.

    :param model_class: The model class required to generate a
    `ViewSet` based on it.
    :return: A `ViewSet` class.
    """
    if not model_class:
        raise Exception

    model_api_meta = getattr(model_class, API_CLS_NAME)
    assert model_api_meta is not None

    def get_queryset(self):
        return model_class.objects.all()

    class_dict = {
        'authentication_classes': (SessionAuthentication, TokenAuthentication),
        'permission_classes': (IsAuthenticated, DjangoModelPermissions),
        'get_queryset': get_queryset,
        'filter_backends': (),
        'serializer_class': generate_serializer(model_class),
    }
    cls = type(model_class.__name__, get_bases_classes(model_api_meta),
               class_dict)
    utils.set_attrs(cls, model_api_meta, VIEWSET_ATTRS)
    init_filter_backends(cls)
    module = utils.get_module(
        model_class, model_api_meta, PACKAGE_LOOKUP_FIELD,
        MODULE_LOOKUP_FIELD)
    if module:
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
    bases = ()

    operations = getattr(model_api_meta, 'allowable_operations', None)

    caching = getattr(model_api_meta, 'caching', False)
    if caching:
        bases += (CACHING_MIXIN,)

    bases += (viewsets.ModelViewSet,) if not operations\
        else tuple([MIXINS[operation] for operation in operations]) + (
            viewsets.GenericViewSet,)
    return bases
