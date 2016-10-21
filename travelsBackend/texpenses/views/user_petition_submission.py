from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from texpenses.models import UserPetitionSubmission
from texpenses.actions import inform_on_action


EXPOSED_METHODS = ['create', 'cancel', 'get_queryset']


@detail_route(methods=['post'])
@inform_on_action('CANCELLATION')
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        petition_id = submitted.status_rollback()
        headers = {'location': reverse('userpetition-detail',
                                       args=[petition_id])}
        return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


@inform_on_action('SUBMISSION')
def create(self, request, *args, **kwargs):
    return super(self.__class__, self).create(request, *args, **kwargs)


def get_queryset(self):
    return UserPetitionSubmission.objects.select_for_update(nowait=True).\
        select_related('tax_office', 'user', 'project').\
        filter(user=self.request.user)
