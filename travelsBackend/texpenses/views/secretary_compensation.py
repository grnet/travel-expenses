from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.reverse import reverse
from rest_framework.response import Response
from texpenses.views import utils

EXPOSED_METHODS = ['submit', 'save']


@detail_route(methods=['post'])
def save(self, request, pk=None):
    return utils.proceed(self, request, pk)


@detail_route(methods=['post'])
def submit(self, request, pk=None):
    instance = self.get_object()
    try:
        petition_id = instance.proceed()
        headers = {'location': reverse(
            'secretarycompensation-detail', args=[petition_id])}
        return Response(status=status.HTTP_303_SEE_OTHER, headers=headers)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)
