from rest_framework import serializers
from rest_framework.fields import Field
from collections import OrderedDict
from texpenses.serializers.utils import get_package_modules, camel2snake,\
    CUSTOM_SERIALIZER_CODE


READ_ONLY_FIELDS = ('id', 'url')


def modelserializer_factory(mdl, api_name='APITravel',
                            **kwargss):
    """ Generalized serializer factory to increase DRYness of code.

    :param mdl: The model for the HyperLinkedModelSerializer
    :param fields: The fields that should be exclusively present on the\
        serializer
    :param read_only_fields: The fields that should be read only on the\
        serialzer
    :param kwargss: Optional additional field specifications
    :return: A HyperLinkedModelSerializer
    """

    def _get_declared_fields(attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]
        fields.sort(key=lambda x: x[1]._creation_counter)
        return OrderedDict(fields)

    # Create an object that will look like a base serializer
    class Base(object):
        pass

    Base._declared_fields = _get_declared_fields(kwargss)
    model_meta = getattr(mdl, api_name)

    if model_meta is None:
        fields = '__all__'
    else:
        if model_meta.fields is None:
            fields = '__all__'
        else:
            fields = model_meta.fields

    read_only_fields = READ_ONLY_FIELDS + getattr(model_meta,
                                                  'read_only_fields', ())

    class TESerializer(Base, serializers.HyperlinkedModelSerializer):

        modules = get_package_modules()
        model_name = camel2snake(mdl.__name__)

        if model_name in modules:

            module = __import__(CUSTOM_SERIALIZER_CODE + "." + model_name,
                                fromlist="dummy")

            if hasattr(module, 'create'):
                create_method = getattr(module, 'create')
                create = create_method

            if hasattr(module, 'update'):
                update_method = getattr(module, 'update')
                update = update_method

            if hasattr(module, 'delete'):
                delete_method = getattr(module, 'delete')
                delete = delete_method

        class Meta:
            model = mdl

        setattr(Meta, "read_only_fields", read_only_fields)

        if fields:
            setattr(Meta, "fields", fields)

        def validate(self, attrs):
            super(TESerializer, self).validate(attrs)
            if self.instance is not None:
                attrs['id'] = self.instance.id
            model_inst = mdl(**attrs)
            model_inst.clean()
            return attrs

    return TESerializer
