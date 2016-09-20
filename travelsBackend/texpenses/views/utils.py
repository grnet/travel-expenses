from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response


def proceed(view, request, pk=None):
    instance = view.get_object()
    serializer = view.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.proceed(instance)
        headers = view.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)
    except PermissionDenied as e:
        return Response({'detail': e.message},
                        status=status.HTTP_403_FORBIDDEN)
