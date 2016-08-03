from rest_framework import serializers
from texpenses.factories import utils


READ_ONLY_FIELDS = ('id', 'url')
SERIALIZER_ATTRS = [('fields', '__all__'),
                    ('read_only_fields', READ_ONLY_FIELDS),
                    ('write_only_fields', None), ('extra_kwargs', None)]
CUSTOM_SERIALIZERS_CODE = 'texpenses.serializers'


class ModelFieldNotRelated(Exception):
    pass


class InvalidProxyModel(Exception):
    pass


def factory(model_class, serializer_module_name=None, api_name='APITravel'):
    """ Generalized serializer factory to increase DRYness of code.

    :param model_class: The model for the HyperLinkedModelSerializer
    :param fields: The fields that should be exclusively present on the\
        serializer
    :param read_only_fields: The fields that should be read only on the\
        serialzer
    :param kwargss: Optional additional field specifications
    :return: A HyperLinkedModelSerializer
    """

    class Meta:
        model = model_class

    # Standard serializer class content.
    class_dict = {
        'Meta': Meta,
    }
    model_api_class = getattr(model_class, api_name)
    assert model_api_class is not None

    nested_serializers = get_nested_serializer(model_class, model_api_class)
    class_dict.update(nested_serializers)
    cls = type(
        model_class.__name__, (serializers.HyperlinkedModelSerializer,),
        class_dict)
    utils.set_attrs(cls.Meta, model_api_class, SERIALIZER_ATTRS)
    module_name = utils.camel2snake(model_class.__name__)\
        if not serializer_module_name else serializer_module_name
    module = utils.get_package_module(
        CUSTOM_SERIALIZERS_CODE + '.' + module_name)
    utils.bound_methods(cls, module)
    return cls


MANY_TO_MANY_REL = 'ManyToManyField'


def get_related_model(model, model_field_name):
    """
    This function get the related model class.

    Based on the given model class and the model field name which corresponds
    to a relation with another model, this function extracts the underlying
    related model class.

    :param model: Model class.
    :param model_field_name: Model field name which corresponds to relation
    with another model.
    :returns: Related model class.

    :raises: ModelFieldNotRelated If the given field is not related to another
    model.
    """
    model_field = model._meta.get_field(model_field_name)
    if model_field.rel is None:
        raise ModelFieldNotRelated(
            'Field %s is not related with another model' % (
                repr(model_field_name)))
    return model_field.rel.to


def get_base_or_proxy(base_model_class, proxy_model_class):
    """
    Get model class to construct model serializer.

    If a proxy model has not been specified, then it gets the base model class.
    If a proxy model has been specified, then it checks that it is actual a
    proxy model of the given base model class.

    :param base_model_class: Base model class of relation.
    :param proxy_model_class: Specified proxy model class.
    :returns: Either the base model class or proxy model class.

    :raises: InvalidProxyModel if the given proxy model is not an actual
    proxy model of the defined base model.
    """
    if not proxy_model_class:
        return base_model_class
    if not (proxy_model_class._meta.proxy and
            proxy_model_class._meta.concrete_model is base_model_class):
        raise InvalidProxyModel('Given proxy model %s is invalid' % (
            proxy_model_class.__class__.__name__))
    return proxy_model_class


def get_nested_serializer(model, model_api_class):
    """
    This function constructs nested serializers based on the nested relations
    defined on the API class of a given model.

    :param model: Model class which supports nested serialization.
    :param model_api_class: API class of specified model.

    :returns: A dictionary keyed by the api field name which corresponds to
    the nested serializer and it maps to the corresponding serializer class.
    """
    nested_relations = getattr(model_api_class, 'nested_relations', None)
    if not nested_relations:
        return {}
    nested_serializers = {}
    for api_field_name, model_field_name, model_proxy_class in map((
            lambda x: x + (None,) if len(x) == 2 else x), nested_relations):
        rel_model_class = get_related_model(model, model_field_name)
        serializer_class = factory(get_base_or_proxy(
            rel_model_class, model_proxy_class))
        many = model._meta.get_field(
            model_field_name).get_internal_type() == MANY_TO_MANY_REL
        source = None if api_field_name == model_field_name\
            else model_field_name
        nested_serializers[api_field_name] = serializer_class(
            many=many, source=source)
    return nested_serializers
