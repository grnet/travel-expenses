import requests
import urllib
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from djoser import views as djoser_views
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated,\
    DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from models import Specialty
from models import TaxOffice
from serializers import UserProfileSerializer
from serializers import SpecialtySerializer
from serializers import TaxOfficeSerializer
from serializers import CustomUserRegistrationSerializer
# from custom_permissions import IsOwnerOrAdmin
User = get_user_model()


@require_http_methods(["GET", ])
def custom_activation_view(request, uid=None, token=None):
    if uid and token:
        payload = {
            'uid': uid,
            'token': token
        }
        enc = urllib.urlencode(payload)
        url = 'http://localhost:8000/auth/activate/'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=enc, headers=headers)
        if response.status_code == 200:
            return HttpResponse("ACTIVATED")
        elif response.status_code == 403:
            return HttpResponse("ALREADY ACTIVATED")
        else:
            return HttpResponse("Could not activate account with uid:" +
                                uid + " and token:" + token)


class CustomUserView(djoser_views.UserView):

    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions,
    )
    queryset = User.objects.all()


class SpecialtyViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser, DjangoModelPermissions,)
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class TaxOfficeViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser, DjangoModelPermissions,)
    queryset = TaxOffice.objects.all()
    serializer_class = TaxOfficeSerializer


class CustomUserRegistrationView(djoser_views.RegistrationView):
    serializer_class = CustomUserRegistrationSerializer
