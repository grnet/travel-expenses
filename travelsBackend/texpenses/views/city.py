from texpenses.models import City

EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return City.objects.select_related('country').all()
