from rest_framework.decorators import detail_route
from rest_framework.response import Response
from texpenses.models import UserCompensation, UserCompensationSubmission
from texpenses.generators.serializers import generate


EXPOSED_METHODS = ['get_queryset', 'save', 'submit', 'get_serializer_class',
                   'procceed']


SUBMISSION_SERIALIZER = generate(UserCompensationSubmission)


@detail_route(methods=['post', 'get'])
def save(self, request, pk=None):
    return self.procceed(request, pk)


@detail_route(methods=['post', 'get'])
def submit(self, request, pk=None):
    return self.procceed(request, pk)


def procceed(self, request, pk=None):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    if request.data.keys():
        serializer.proceed(instance)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, headers=headers)


def get_serializer_class(self):
    return SUBMISSION_SERIALIZER if self.action == 'submit'\
        else self.serializer_class


def get_queryset(self):
    return UserCompensation.objects.filter(user=self.request.user)
