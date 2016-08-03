from django.core.validators import ValidationError
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

EXPOSED_METHODS = ['cancel']


@detail_route(methods=['post'])
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        submitted.cancel()
        return Response({'detail': 'Petition was cancelled.'})
    except ValidationError as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)
