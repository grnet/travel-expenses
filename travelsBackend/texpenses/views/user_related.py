import logging
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
import urllib
from django.conf import settings
import requests
from django.http import HttpResponse
from rest_framework_tracking.mixins import LoggingMixin
from djoser import views as djoser_views
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from texpenses.custom_permissions import isAdminOrRead
from texpenses.serializers import UserProfileSerializer, SpecialtySerializer,\
    KindSerializer, TaxOfficeSerializer, UserCategorySerializer,\
    CustomUserRegistrationSerializer
from texpenses.models import Specialty, Kind, TaxOffice, UserCategory


logger = logging.getLogger(__name__)

User = get_user_model()


@require_http_methods(["GET", ])
def custom_activation_view(request, uid=None, token=None):
    if uid and token:
        payload = {
            'uid': uid,
            'token': token
        }
        enc = urllib.urlencode(payload)
        url = settings.HOST_URL + settings.API_PREFIX + '/auth/activate/'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=enc, headers=headers)
        if response.status_code == 200:
            return HttpResponse("ACTIVATED")
        elif response.status_code == 403:
            return HttpResponse("ALREADY ACTIVATED")
        else:
            return HttpResponse("Could not activate account with uid:" +
                                uid + " and token:" + token)


class CustomUserView(LoggingMixin, djoser_views.UserView):

    """API endpoint that lets a user view and edit some basic\
        user related info"""
    pass


class CustomActivationView(LoggingMixin, djoser_views.ActivationView):

    """API endpoint that activates a new user account"""
    pass


class CustomSetUsernameView(LoggingMixin, djoser_views.SetUsernameView):

    """API endpoint that lets a user change his/her username"""
    pass


class CustomSetPasswordView(LoggingMixin, djoser_views.SetPasswordView):

    """API endpoint that lets a user change his/her password"""
    pass


class CustomPasswordResetView(LoggingMixin, djoser_views.PasswordResetView):

    """API endpoint that sends email to user with password reset link"""
    pass


class CustomPasswordResetConfirmView(LoggingMixin,
                                     djoser_views.PasswordResetConfirmView):

    """Use this endpoint to finish reset password process"""
    pass


class CustomLoginView(LoggingMixin, djoser_views.LoginView):

    """Use this endpoint to obtain user authentication toke"""
    pass


class CustomLogoutView(LoggingMixin, djoser_views.LogoutView):

    """API endpoint for logging out a user"""
    pass


class CustomRootView(LoggingMixin, djoser_views.RootView):

    """API endpoint that lists all user related API endpoints"""
    pass


class CustomUserDetailedView(LoggingMixin, djoser_views.UserView):

    """API endpoint that allows a user to view and edit his personal info"""

    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions,
    )
    queryset = User.objects.all()


class SpecialtyViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user) """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class KindViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user)"""

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class TaxOfficeViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = TaxOffice.objects.all()
    serializer_class = TaxOfficeSerializer


class UserCategoryViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer


class CustomUserRegistrationView(LoggingMixin, djoser_views.RegistrationView):

    """API endpoint for registering a new user"""
    serializer_class = CustomUserRegistrationSerializer
