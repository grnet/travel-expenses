from texpenses.models import UserPetitionCompensation


EXPOSED_METHODS = ['get_queryset']


def get_queryset(self):
    return UserPetitionCompensation.objects.filter(user=self.request.user)
