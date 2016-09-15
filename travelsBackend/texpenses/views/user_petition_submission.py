from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from texpenses.models import UserPetitionSubmission
from texpenses.actions import inform


EXPOSED_METHODS = ['create', 'cancel', 'get_queryset']


@detail_route(methods=['post'])
def cancel(self, request, pk=None):
    submitted = self.get_object()
    try:
        petition_id = submitted.status_rollback()
        headers = {'location': reverse('userpetition-detail',
                                       args=[petition_id])}
        inform(submitted, 'CANCELLATION')
        return Response(headers=headers, status=status.HTTP_303_SEE_OTHER)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


def create(self, request, *args, **kwargs):
    response = super(self.__class__, self).create(request, *args, **kwargs)
    self.lookup_field = 'pk'
    petition_id = response.data['url'].rsplit('/', 2)[1]
    self.kwargs = {self.lookup_field: petition_id}
    instance = self.get_object()
    inform(instance, 'SUBMISSION')
    return response


def get_queryset(self):
    return UserPetitionSubmission.objects.filter(user=self.request.user)
