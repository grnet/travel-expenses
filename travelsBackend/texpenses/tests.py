from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile


class UserExtensionTests(TestCase):

    def test_user_exists(TestCase):
        password = 'kostas'
        username = 'kostas'
        email = 'kostas@gmail.com'
        user = User.objects.create_user(
            username=username, password=password, email=email)
        user_profile = UserProfile(user=user)

        print user_profile.user.username

        user = authenticate(username=username, password=password)

        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print(
                    "The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and
            # password
            print("The username and password were incorrect.")

    def test_see_urls(self):
        """TODO: Docstring for test_see_urls.
        :returns: TODO

        """
        from rest_framework import routers
        router = routers.DefaultRouter()
        router.urls.append(r'^auth/login/$')
        print router.urls
