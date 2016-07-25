import importlib
import re


def get_package_module(module_name):
    """
    This function loads programtically the desired module which is located in
    the default package. In case, it can't find such a module, it returns
    `None`.

    :param module_name: Name of module inside the package.

    :returns: The module object if it exists; `None` otherwise.
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def camel2snake(name_camel_case):
    """ Converts a CamelCase string to snake_case. """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name_camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def override_methods(cls, module, methods_to_override):
    """
    This function looks up for specific methods in a specified module and if
    methods exist, then it overrides the corresponding methods of the given
    class.

    :param cls: Class to override its methods.
    :param module: Module object to look for implementations of the functions.
    :param methods_to_override: List with the names of methods to override.
    """
    if module is None:
        return

    for method_name in methods_to_override:
        custom_method = getattr(module, method_name, None)
        if custom_method is not None:
            setattr(cls, method_name, custom_method)


def set_attrs(cls, api_class, attrs):
    """
    This function looks up for specific fields in a specified meta class which
    define how fields will be treated by the REST API classes (serializers,
    viewsets).

    :param cls: Serializer or Viewset class.
    :param api_class: API class of model.
    :param attrs: List of tuple with the attr names and
    their default values.
    """
    if api_class is None:
        return

    for attr_name, default in attrs:
        field_value = getattr(api_class, attr_name, None)
        if field_value is None and default is None:
            continue
        setattr(cls, attr_name, (
            default if field_value is None else field_value))
