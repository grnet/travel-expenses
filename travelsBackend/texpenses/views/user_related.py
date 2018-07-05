import logging
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
import urllib
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from djoser import views as djoser_views
from djoser import utils as djoser_utils
from djoser import settings as djoser_settings
from texpenses.serializers import CustomUserRegistrationSerializer,\
    PasswordResetConfirmRetypeSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import response, status
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

User = get_user_model()

class CustomEmailActivationView(djoser_views.ActivationView):
    pass


class CustomUserView(djoser_views.UserView):

    """API endpoint that lets a user view and edit some basic\
        user related info"""
    pass


class CustomSetUsernameView(djoser_views.SetUsernameView):

    """API endpoint that lets a user change his/her username"""
    pass


class CustomSetPasswordView(djoser_views.SetPasswordView):

    """API endpoint that lets a user change his/her password"""
    pass


class CustomPasswordResetView(djoser_views.PasswordResetView):

    """API endpoint that sends email to user with password reset link"""
    pass


class PasswordResetView(djoser_views.PasswordResetConfirmView):

    """Use this endpoint to finish reset password process"""
    pass

class CustomLoginView(djoser_views.LoginView):

    """Use this endpoint to obtain user authentication toke"""
    pass


class CustomLogoutView(djoser_views.LogoutView):

    """API endpoint for logging out a user"""
    pass


class CustomRootView(djoser_views.RootView):

    """API endpoint that lists all user related API endpoints"""
    pass


class CustomUserRegistrationView(djoser_views.RegistrationView):

    """API endpoint for registering a new user"""
    serializer_class = CustomUserRegistrationSerializer

    def resend_verification(self, request, email):
        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            raise PermissionDenied("user.invalid.or.activated")

        if djoser_settings.get('SEND_ACTIVATION_EMAIL'):
            self.send_email(**self.get_send_email_kwargs(user))
        return HttpResponse(status=202)

    def create(self, request, *args, **kwargs):
        resend_email = request.data.get('resend_verification', None)
        if resend_email:
            return self.resend_verification(request, resend_email)
        return super(CustomUserRegistrationView, self).create(
            request, *args, **kwargs)

class CustomUserDetailedView(djoser_views.UserView):

    """API endpoint that allows a user to view and edit his personal info"""

    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions,
    )
    queryset = User.objects.select_related('tax_office').all()
