from rest_framework import permissions
from texpenses.models import SecretaryPetition


EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    non_atomic_requests = permissions.SAFE_METHODS
    query = SecretaryPetition.objects.select_related('tax_office', 'user',
                                                     'project').all()
    if self.request.method in non_atomic_requests:
        return query
    else:
        return query.select_for_update(nowait=True)
