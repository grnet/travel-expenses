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


def get_module(model_class, api_class, package_lookup, module_lookup):
    """
    This functions gets the module object which contains custom implementation
    which should be bounded to a dynamically generated class (Serializer or
    ViewSet).

    API meta classes should specify the package where custom code is located.
    Moreover, it looks a module whose name is equal to the snake_case name
    of the model class in order to retrieve code specific to the corresponding
    model class. However, it is possible to override its name.

    :param model_class: Model class.
    :param api_class: API class which corresponds to the model.
    :param package_lookup: Field name of API class which stores the location
    of custom code.
    :param module_lookup: Field name of API class which stores the name of
    module inside the aforementioned package.
    """
    package = getattr(api_class, package_lookup, None)
    if not package:
        return
    default_module_name = camel2snake(model_class.__name__)
    module_name = getattr(api_class, module_lookup, None)
    return get_package_module(package + '.' + (
        module_name or default_module_name))


def camel2snake(name_camel_case):
    """ Converts a CamelCase string to snake_case. """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name_camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def bound_methods(cls, module):
    """
    This function looks up for specific methods in a specified module and if
    methods exist, then it bounds them to the given class.

    :param cls: Class to override its methods.
    :param module: Module object to look for implementations of the functions.
    """
    exposed_methods = getattr(module, 'EXPOSED_METHODS', [])
    if module is None:
        return

    for method_name in exposed_methods:
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
