import json
import urlparse
import logging
logger = logging.getLogger(__name__)

from texpenses.models.common import load_resources, load_permissions
from django.conf import settings


from django.http import HttpResponse


def config(request):
    base = getattr(settings, 'BASE_URL', None)
    prefix = getattr(settings, 'API_PREFIX', '')
    api_endpoint = urlparse.urljoin(prefix, 'api')

    if base is None:
        base = request.build_absolute_uri('/')

    backend_host = urlparse.urljoin(base, api_endpoint)

    resources = load_resources()
    permissions = load_permissions()

    config_data = {
        'resources': resources,
        'permissions': permissions,
        'host': base,
        'prefix': prefix,
        'api_endpoint': api_endpoint,
        'backend_host': backend_host
    }
    return HttpResponse(json.dumps(config_data),
                        content_type='application/json')
