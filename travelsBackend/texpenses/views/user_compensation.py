from texpenses.models import UserCompensation


EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return UserCompensation.objects.filter(user=self.request.user)
