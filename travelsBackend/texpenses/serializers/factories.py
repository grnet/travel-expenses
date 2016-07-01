from rest_framework import serializers
from rest_framework.fields import Field
from collections import OrderedDict


def modelserializer_factory(mdl, fields=None, read_only_fields=None, **kwargss):
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

    class TESerializer(Base, serializers.HyperlinkedModelSerializer):

        class Meta:
            model = mdl

        if read_only_fields is None:
            setattr(Meta, "read_only_fields", ('id', 'url'))
        else:
            setattr(Meta, "read_only_fields", read_only_fields)

        if fields:
            setattr(Meta, "fields", fields)

    return TESerializer
