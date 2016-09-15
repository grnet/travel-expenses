from rest_framework.decorators import detail_route
from rest_framework.response import Response
from texpenses.models import UserCompensation, UserCompensationSubmission
from texpenses.generators.serializers import generate
from texpenses.views import utils

EXPOSED_METHODS = ['get_queryset', 'save', 'submit', 'get_serializer_class',
                   'proceed']


SUBMISSION_SERIALIZER = generate(UserCompensationSubmission)


@detail_route(methods=['post'])
def save(self, request, pk=None):
    return utils.proceed(self, request, pk)


@detail_route(methods=['post'])
def submit(self, request, pk=None):
    return utils.proceed(self, request, pk)


def get_serializer_class(self):
    return SUBMISSION_SERIALIZER if self.action == 'submit'\
        else self.serializer_class


def get_queryset(self):
    return UserCompensation.objects.filter(user=self.request.user)
