from rest_framework.decorators import detail_route
from rest_framework.response import Response
from texpenses.generators.serializers import generate
from texpenses.views import utils

EXPOSED_METHODS = ['get_queryset', 'save', 'submit', 'proceed']


@detail_route(methods=['post'])
def save(self, request, pk=None):
    return utils.proceed(self, request, pk)


@detail_route(methods=['post'])
def submit(self, request, pk=None):
    return utils.proceed(self, request, pk)
