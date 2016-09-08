from texpenses.models import UserPetition

EXPOSED_METHODS = ['get_queryset']



def get_queryset(self):
    return UserPetition.objects.filter(user=self.request.user)
