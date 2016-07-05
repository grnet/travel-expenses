import pkgutil
import re

CUSTOM_SERIALIZER_CODE = 'texpenses.serializers'
exec("import " + CUSTOM_SERIALIZER_CODE + " as custom_serializer_code")


def get_package_modules():
    """TODO: Docstring for get_package_files.
    :returns: TODO

    """
    package = custom_serializer_code
    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if not ispkg:
            modules += [modname, ]
    return modules


def camel2snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
