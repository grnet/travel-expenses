from django.core.validators import ValidationError
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

EXPOSED_METHODS = ['cancel']


@detail_route(methods=['post'])
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        petition_id = submitted.status_rollback()
        headers = {'location': reverse(
            'userpetition-detail', args=[petition_id])}
        return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
    except ValidationError as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)
