from rest_framework import serializers
from texpenses.serializers.utils import get_package_module, camel2snake


READ_ONLY_FIELDS = ('id', 'url')
FIELDS_TO_OVERRIDE = [('fields', '__all__'),
                      ('read_only_fields', READ_ONLY_FIELDS),
                      ('write_only_fields', None)]
METHODS_TO_OVERRIDE = ['create', 'update', 'delete']


def modelserializer_factory(mdl, api_name='APITravel'):
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
    override_fields(TESerializer.Meta, model_meta)
    module_name = camel2snake(mdl.__name__)
    module = get_package_module(module_name)
    override_methods(TESerializer, module)
    return TESerializer


def override_methods(cls, module):
    """
    This function looks up for specific methods in a specified module and if
    methods exist, then it overrides the corresponding methods of the given
    class.

    :param cls: Class to override its methods.
    :param module: Module object to look for implementations of the functions.
    """
    if module is None:
        return

    for method_name in METHODS_TO_OVERRIDE:
        custom_method = getattr(module, method_name, None)
        if custom_method is not None:
            setattr(cls, method_name, custom_method)


def override_fields(cls, meta_class):
    """
    This function looks up for specific fields in a specified meta class which
    define how fields will be treated by the serializer.

    :param cls: Class to override its fields.
    :param module: Class to get its fields.
    """
    if meta_class is None:
        return

    for field_name, default in FIELDS_TO_OVERRIDE:
        field_value = getattr(meta_class, field_name, None)
        if field_value is None and default is None:
            continue
        setattr(cls, field_name, (
            default if field_value is None else field_value))
