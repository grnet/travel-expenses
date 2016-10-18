from texpenses.models import SecretaryPetition


EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return SecretaryPetition.objects.select_related('tax_office', 'user',
                                                    'project').\
        prefetch_related('travel_info').all()
