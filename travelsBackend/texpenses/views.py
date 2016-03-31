import requests
import urllib
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from djoser import views
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated,\
    DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from models import UserProfile
from models import Specialty
from models import TaxOffice
from serializers import UserProfileSerializer
from serializers import SpecialtySerializer
from serializers import TaxOfficeSerializer
from serializers import CustomUserRegistrationSerializer
# from serializers import UserCredentialsSerializer
from custom_permissions import IsOwnerOrAdmin


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


class CustomUserViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    """API endpoint that allows users model to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):

    """API endpoint that allows users model to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


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


class CustomUserRegistrationView(views.RegistrationView):
    serializer_class = CustomUserRegistrationSerializer
