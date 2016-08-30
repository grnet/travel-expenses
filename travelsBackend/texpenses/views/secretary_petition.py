from texpenses.models import SecretaryPetition


EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return SecretaryPetition.objects.all()
