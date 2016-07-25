from rest_framework import serializers
from texpenses.factories import utils


READ_ONLY_FIELDS = ('id', 'url')
FIELDS_TO_EXPOSE = [('fields', '__all__'),
                    ('read_only_fields', READ_ONLY_FIELDS),
                    ('write_only_fields', None), ('extra_kwargs', None)]
METHODS_TO_OVERRIDE = ['create', 'update', 'delete', 'validate']
CUSTOM_SERIALIZERS_CODE = 'texpenses.serializers'


class ModelFieldNotFound(Exception):
    pass


class ModelFieldNotRelated(Exception):
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

    def validate(self, attrs):
        attrs = super(cls, self).validate(attrs)
        model_inst = model_class(**attrs)
        model_inst.clean()
        return attrs

    # Standard serializer class content.
    class_dict = {
        'validate': validate,
        'Meta': Meta,
    }
    model_api_class = getattr(model_class, api_name)
    assert model_api_class is not None
    nested_serializers = get_nested_serializer(model_class, model_api_class)
    class_dict.update(nested_serializers)
    cls = type(
        model_class.__name__, (serializers.HyperlinkedModelSerializer,),
        class_dict)
    utils.override_fields(
        cls.Meta, model_api_class, FIELDS_TO_EXPOSE)
    module_name = utils.camel2snake(model_class.__name__)\
        if not serializer_module_name else serializer_module_name
    module = utils.get_package_module(
        CUSTOM_SERIALIZERS_CODE + '.' + module_name)
    utils.override_methods(cls, module, METHODS_TO_OVERRIDE)
    cls.__name__ = model_class.__name__
    return cls


RELATED_DESCRIPTORS = {
    'ForwardOneToOneDescriptor': lambda x: x.field.rel.to,
    'ForwardManyToOneDescriptor': lambda x: x.field.rel.to,
    'ManyToManyDescriptor': lambda x: x.rel.to,
}

MANY_TO_MANY_REL = 'ManyToManyDescriptor'


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
    for api_field_name, model_field_name in nested_relations:
        model_field = getattr(model, model_field_name, None)

        if model_field is None:
            raise ModelFieldNotFound('Field %s not found on model %s' % (
                repr(model_field_name), model.__name__))
        field_rel_name = model_field.__class__.__name__
        if field_rel_name not in RELATED_DESCRIPTORS:
            raise ModelFieldNotRelated(
                'Field %s is not related with another model' % (
                    repr(model_field_name)))
        serializer_class = factory(RELATED_DESCRIPTORS[field_rel_name](
            model_field))
        many = field_rel_name == MANY_TO_MANY_REL
        source = None if api_field_name == model_field_name\
            else model_field_name
        nested_serializers[api_field_name] = serializer_class(
            many=many, source=source)
    return nested_serializers
