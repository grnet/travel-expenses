from django.test import TestCase
from validators import iban_validation
from validators import afm_validator


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
        afm = 1234566789
        afm_validator(afm)
        print "============================"
