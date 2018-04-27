import logging
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
import urllib
from django.conf import settings
import requests
from django.http import HttpResponse, HttpResponseRedirect
from djoser import views as djoser_views
from djoser import utils as djoser_utils
from texpenses.serializers import CustomUserRegistrationSerializer,\
    PasswordResetConfirmRetypeSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import response, status

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
        if response.status_code == 200 or response.status_code == 204:
            return HttpResponseRedirect("/")
        elif response.status_code == 403:
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Could not activate account with uid:" +
                                uid + " and token:" + token)


class CustomUserView(djoser_views.UserView):

    """API endpoint that lets a user view and edit some basic\
        user related info"""
    pass


class CustomActivationView(djoser_views.ActivationView):

    """API endpoint that activates a new user account"""
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

    def post(self, request, **kwargs):

        uid = djoser_utils.decode_uid(kwargs['uid'])
        self.user = User.objects.get(pk=uid)

        return super(PasswordResetView, self).post(request)

    def action(self, serializer):
        self.user.set_password(serializer.data['new_password'])
        self.user.save()
        return response.Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return PasswordResetConfirmRetypeSerializer


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


class CustomUserDetailedView(djoser_views.UserView):

    """API endpoint that allows a user to view and edit his personal info"""

    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions,
    )
    queryset = User.objects.select_related('tax_office').all()