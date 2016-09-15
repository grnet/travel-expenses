from texpenses.models import SecretaryCompensation


EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return SecretaryCompensation.objects.all()
