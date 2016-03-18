from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()


class UserExtensionTests(TestCase):

    def test_user_extension(self):
        """TODO: Docstring for test_user_extension.

        :arg1: TODO
        :returns: TODO

        """
        print User.objects.all()
