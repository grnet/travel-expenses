from rest_framework.response import Response


def proceed(view, request, status, pk=None):
    instance = view.get_object()
    serializer = view.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.proceed(instance, status)
    headers = view.get_success_headers(serializer.data)
    return Response(serializer.data, headers=headers)
