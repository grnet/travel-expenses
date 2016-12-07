import inflection
from django.apps import apps
from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from texpenses.generators.views import generate


API = getattr(settings, 'API_PREFIX', 'api')
API_ROUTER = routers.DefaultRouter()


def generate_api_urls():
    """
    This function generates endpoints for all models which are exposed to
    API.

    Models are exposed to API if contain an inner class named with the
    capitalized api prefix (default is `Api`).

    Then, it generates the corresponding views and registers them to
    rest framework router.
    """
    models = apps.get_models()
    for model in models:
        api_meta = getattr(model, API.capitalize(), None)
        if not api_meta or not getattr(api_meta, 'expose', True):
            continue
        default_resource_name = inflection.pluralize(
            model._meta.verbose_name.replace(' ', '-'))
        resource_name = getattr(api_meta, 'resource_name',
                                default_resource_name)
        API_ROUTER.register(resource_name, generate(model),
                            base_name=model._meta.model_name)
    return url(r'^' + API + '/', include(API_ROUTER.urls))
