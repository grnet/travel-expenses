from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from texpenses.models import UserCompensationSubmission


EXPOSED_METHODS = ['cancel', 'get_queryset']


@detail_route(methods=['post'])
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        petition_id = submitted.status_rollback()
        headers = {'location':
                   reverse('usercompensation-detail',
                           args=[petition_id])}
        return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


def get_queryset(self):
    return UserCompensationSubmission.objects.\
        filter(user=self.request.user)
