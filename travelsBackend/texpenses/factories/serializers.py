from rest_framework import serializers
from texpenses.factories import utils


READ_ONLY_FIELDS = ('id', 'url')
FIELDS_TO_OVERRIDE = [('fields', '__all__'),
                      ('read_only_fields', READ_ONLY_FIELDS),
                      ('write_only_fields', None)]
METHODS_TO_OVERRIDE = ['create', 'update', 'delete', 'validate']
CUSTOM_SERIALIZERS_CODE = 'texpenses.serializers'


def factory(mdl, nested_model=None, serializer_module=None,
            api_name='APITravel'):
    """ Generalized serializer factory to increase DRYness of code.

    :param mdl: The model for the HyperLinkedModelSerializer
    :param fields: The fields that should be exclusively present on the\
        serializer
    :param read_only_fields: The fields that should be read only on the\
        serialzer
    :param kwargss: Optional additional field specifications
    :return: A HyperLinkedModelSerializer
    """
    if nested_model:
        snake_case_nested = utils.camel2snake(nested_model.__name__)

    class AbstractSerializer(serializers.HyperlinkedModelSerializer):
        if nested_model:
            additional_data = factory(nested_model)(
                write_only=True, many=True, source=snake_case_nested)

        class Meta:
            model = mdl

        def validate(self, attrs):
            attrs = super(AbstractSerializer, self).validate(attrs)
            model_inst = mdl(**attrs)
            model_inst.clean()
            return attrs

    model_meta = getattr(mdl, api_name)
    utils.override_fields(
        AbstractSerializer.Meta, model_meta, FIELDS_TO_OVERRIDE)
    module_name = utils.camel2snake(mdl.__name__) if not serializer_module\
        else serializer_module
    module = utils.get_package_module(
        CUSTOM_SERIALIZERS_CODE + '.' + module_name)
    utils.override_methods(AbstractSerializer, module, METHODS_TO_OVERRIDE)
    AbstractSerializer.__name__ = mdl.__name__
    return AbstractSerializer
