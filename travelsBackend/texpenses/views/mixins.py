from texpenses.models import UserPetition
from rest_framework import permissions, status
from django.db import transaction
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from texpenses.models import UserPetitionSubmission
from texpenses.actions import inform_on_action


class UserPetitionMixin(object):

    @transaction.atomic
    def update(self, request, pk=None):
        return super(UserPetitionMixin, self).update(request, pk)

    def get_queryset(self):
        non_atomic_requests = permissions.SAFE_METHODS
        query = UserPetition.objects.select_related('tax_office', 'user',
                                                    'project').\
            filter(user=self.request.user)
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)


class UserPetitionSubmissionMixin(object):

    @detail_route(methods=['post'])
    @transaction.atomic
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
        non_atomic_requests = permissions.SAFE_METHODS
        query = UserPetitionSubmission.objects.select_related('tax_office',
                                                              'user',
                                                              'project').\
            filter(user=self.request.user)
        if self.request.method in non_atomic_requests:
            return query
        else:
            return query.select_for_update(nowait=True)
