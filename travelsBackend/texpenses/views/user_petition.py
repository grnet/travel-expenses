from texpenses.models import UserPetition
from rest_framework import permissions

EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    non_atomic_requests = permissions.SAFE_METHODS
    query = UserPetition.objects.select_related('tax_office', 'user',
                                                'project').\
        filter(user=self.request.user)
    if self.request.method in non_atomic_requests:
        return query
    else:
        return query.select_for_update(nowait=True)
