from texpenses.models import UserPetition

EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    non_atomic_requests = ('GET', 'HEAD', 'OPTIONS', 'POST',)
    if self.request.method in non_atomic_requests:
        return UserPetition.objects.select_related('tax_office', 'user',
                                                   'project').\
            filter(user=self.request.user)
    else:
        return UserPetition.objects.select_for_update(nowait=True).\
            select_related('tax_office', 'user', 'project').\
            filter(user=self.request.user)
