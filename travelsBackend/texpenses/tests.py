# from django.test import TestCase
from validators import iban_validation
from validators import afm_validator
# Create your tests here.

# iban = "GR1601101250000000012300695"

# print iban_validation(iban)

afm = "123456789"

print afm_validator(afm)
