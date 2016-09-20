from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.reverse import reverse
from rest_framework.response import Response
from texpenses.models import Petition

EXPOSED_METHODS = ['submit', 'save']


VIEW_NAMES = {
    Petition.USER_COMPENSATION: 'usercompensation-detail',
    Petition.USER_COMPENSATION_SUBMISSION: 'usercompensation-detail',
    Petition.SECRETARY_COMPENSATION: 'secretarycompensation-detail',
    Petition.SECRETARY_COMPENSATION_SUBMISSION: 'secretarycompensation-detail',
}


@detail_route(methods=['post'])
def save(self, request, pk=None):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.proceed(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)


@detail_route(methods=['post'])
def submit(self, request, pk=None):
    instance = self.get_object()
    try:
        petition_id = instance.proceed()
        headers = {'location': reverse(
            VIEW_NAMES[instance.status], args=[petition_id])}
        return Response(status=status.HTTP_303_SEE_OTHER, headers=headers)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)
