from texpenses.models import UserPetition

EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return UserPetition.objects.select_related('tax_office', 'user',
                                               'project').\
        prefetch_related('travel_info').filter(user=self.request.user)
