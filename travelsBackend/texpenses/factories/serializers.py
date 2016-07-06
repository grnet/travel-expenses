from rest_framework import serializers
from texpenses.factories import utils


READ_ONLY_FIELDS = ('id', 'url')
FIELDS_TO_OVERRIDE = [('fields', '__all__'),
                      ('read_only_fields', READ_ONLY_FIELDS),
                      ('write_only_fields', None)]
METHODS_TO_OVERRIDE = ['create', 'update', 'delete', 'validate']
CUSTOM_SERIALIZERS_CODE = 'texpenses.serializers'


def factory(mdl, api_name='APITravel'):
    """ Generalized serializer factory to increase DRYness of code.

    :param mdl: The model for the HyperLinkedModelSerializer
    :param fields: The fields that should be exclusively present on the\
        serializer
    :param read_only_fields: The fields that should be read only on the\
        serialzer
    :param kwargss: Optional additional field specifications
    :return: A HyperLinkedModelSerializer
    """
    class TESerializer(serializers.HyperlinkedModelSerializer):

        class Meta:
            model = mdl

        def validate(self, attrs):
            # TODO We have to make this method works without any need of the
            # id of object.
            super(TESerializer, self).validate(attrs)
            if self.instance is not None:
                attrs['id'] = self.instance.id
            model_inst = mdl(**attrs)
            model_inst.clean()
            return attrs

    model_meta = getattr(mdl, api_name)
    utils.override_fields(TESerializer.Meta, model_meta, FIELDS_TO_OVERRIDE)
    module_name = utils.camel2snake(mdl.__name__)
    module = utils.get_package_module(
        CUSTOM_SERIALIZERS_CODE + '.' + module_name)
    utils.override_methods(TESerializer, module, METHODS_TO_OVERRIDE)
    return TESerializer
