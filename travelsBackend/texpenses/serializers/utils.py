import importlib
import pkgutil
import re


CUSTOM_SERIALIZER_CODE = 'texpenses.serializers'


def get_package_module(module_name):
    """
    This function loads programtically the desired module which is located in
    the default package. In case, it can't find such a module, it returns
    `None`.

    :param module_name: Name of module inside the package.

    :returns: The module object is it exists; `None` otherwise.
    """
    try:
        return importlib.import_module(
            CUSTOM_SERIALIZER_CODE + '.' + module_name)
    except ImportError:
        return None


def camel2snake(name_camel_case):
    """ Converts a CamelCase string to snake_case. """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name_camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
