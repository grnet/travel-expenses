import json
import urlparse
from user_related import *
from collections import defaultdict
from texpenses.permissions.permission_rules import PERMISSION_RULES
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


def rule_to_dict(data, args):
    if len(args) == 1:
        return args[0]

    key = args.pop(0)
    for k in key.split(","):
        k = k.strip()
        data[k] = data[k] if k in data else {}
        partial = {
            k: rule_to_dict(data[k], args)
        }
        data.update(partial)
    return data


def load_permissions():
    PERMISSIONS = defaultdict(lambda: dict)
    for rule in PERMISSION_RULES:
        rule_to_dict(PERMISSIONS, list(rule))
    return PERMISSIONS


def load_resources():
    with open(getattr(settings, 'RESOURCES_FILE', 'common.json')) \
            as json_file:
        return json.load(json_file)


@ensure_csrf_cookie
def config(request):
    host_url = getattr(settings, 'HOST_URL', None)
    prefix = getattr(settings, 'API_PREFIX', '')
    default_city = getattr(settings, 'DEFAULT_CITY_DB_ID', 1)
    default_currency = getattr(settings, 'DEFAULT_CURRENCY', 'EUR')

    if host_url is None:
        host_url = request.build_absolute_uri('/')

    api_endpoint = urlparse.urljoin(host_url, prefix)

    permissions = load_permissions()
    resources = load_resources()

    config_data = {
        'backend_host': api_endpoint,
        'default_city': default_city,
        'default_currency': default_currency,
        'permissions': permissions,
        'resources': resources,
        'prefix': prefix,
        'host_url': host_url,
    }
    return HttpResponse(json.dumps(config_data),
                        content_type='application/json')
