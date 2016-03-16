# from django.test import TestCase
from validators import iban_validation

# Create your tests here.

iban = "GR1601101250000000012300695"

print iban_validation(iban)
