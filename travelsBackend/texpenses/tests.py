from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from validators import iban_validation
from validators import afm_validator


class UserRESTApiTests(TestCase):
    password = 'kostas'
    username = 'kostas'
    email = 'kostas@gmail.com'

    def create_user(self):
        print "Creating new user:"
        return User.objects.create_user(
            username=self.username, password=self.password, email=self.email)

    def test_user_exists(self):
        user = self.create_user()
        print "Done."
        user_profile = UserProfile(user=user)

        print user_profile.user.username

        user = authenticate(username=self.username, password=self.password)

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

    def test_login(self):
        self.create_user()
        print "Done"
        client = APIClient()

        result = client.login(username=self.username, password=self.password)
        print "Result is:" + str(result)
        self.assertTrue(
            result, msg="User:" + self.username + ", does not exist")

    def test_user_credentials(self):
        self.create_user()
        print "Done"
        token = Token.objects.get(user__username=self.username)
        client = APIClient()
        result = client.credentials(HTTP_AUTHORIZATION='Token' + token.key)
        print result


class UserProfileTests(APITestCase):

    password = 'kostas'
    username = 'kostas'
    email = 'kostas@gmail.com'

    def create_user(self):
        return User.objects.create_user(
            username=self.username, password=self.password, email=self.email)

    def test_create_user_profile(self):
        url = reverse('users/userprofiles')
        user = self.create_user()
        data = {'name': 'kostas', 'surname':
                'vogias', 'user': user}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().name, 'kostas')

    def test_user_is_superuser(self):
        user = self.create_user()
        print "User: " + self.username + " is superuser:"\
            + str(user.is_superuser)


class UserFormValidation(TestCase):

    def test_iban_validator(self):
        """TODO: Docstring for test_iban_validator.
        :returns: TODO

        """
        print "\nRunning iban validator test"
        iban = "GR160110125000000001230069a"
        iban_validation(iban)
        print "============================="

    def test_afm_validator(self):
        """TODO: Docstring for test_afm_validator.
        :returns: TODO

        """
        print "\nRunning afm validator test"
        afm = "002345612"
        # afm = 000000000
        afm_validator(afm)
        print "============================"
