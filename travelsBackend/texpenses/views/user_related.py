import logging
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
import urllib
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from djoser import views as djoser_views
from djoser import utils as djoser_utils
from djoser import settings as djoser_settings
from texpenses.serializers import CustomUserRegistrationSerializer,\
    PasswordResetConfirmRetypeSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
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

    @method_decorator(csrf_protect)
    def post(self, request):
        return super(CustomPasswordResetView, self).post(request)

    # Overwrite get_users to implement further filtering for rate limiting
    # and set last reset password email
    def get_users(self, email):
        users = super(CustomPasswordResetView, self).get_users(email)
        users_to_receive_email = [u for u in users
                                  if u.can_receive_reset_password_email()]
        for u in users_to_receive_email:
            u.set_last_reset_password_email()
        return users_to_receive_email


class PasswordResetView(djoser_views.PasswordResetConfirmView):

    """Use this endpoint to finish reset password process"""

    # Overwrite action method to reset rate limiting after
    # a successful password reset.
    def action(self, serializer):
        serializer.user.last_reset_password_email = None
        serializer.user.save()
        return super(PasswordResetView, self).action(serializer)


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

        if not user.can_receive_verification_email():
            raise PermissionDenied("email.sent.already")
        user.set_last_resend_verification_email()

        if djoser_settings.get('SEND_ACTIVATION_EMAIL'):
            self.send_email(**self.get_send_email_kwargs(user))
        return HttpResponse(status=202)

    @method_decorator(csrf_protect)
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
        IsAuthenticated,
    )
    queryset = User.objects.select_related('tax_office').all()
