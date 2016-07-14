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


def override_fields(cls, meta_class, fields_to_override):
    """
    This function looks up for specific fields in a specified meta class which
    define how fields will be treated by the REST API classes (serializers,
    viewsets).

    :param cls: Class to override its fields.
    :param module: Class to get its fields.
    :param fields_to_override: List of tuple with the fields to override and
    their default values.
    """
    if meta_class is None:
        return

    for field_name, default in fields_to_override:
        field_value = getattr(meta_class, field_name, None)
        if field_value is None and default is None:
            continue
        setattr(cls, field_name, (
            default if field_value is None else field_value))
