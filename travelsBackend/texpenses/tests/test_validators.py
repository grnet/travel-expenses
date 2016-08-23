from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from texpenses.validators import date_validator, start_end_date_validator,\
    iban_validation


class ValidatorTest(TestCase):

    def test_date_validaror(self):
        date = datetime.now()
        self.assertRaises(ValidationError, date_validator, date)
        self.assertRaises(ValidationError, date_validator, date.date())

        date += timedelta(days=1)
        date_validator(date)
        date_validator(None)

    def test_start_end_date_validator(self):
        start = datetime.now()
        end = datetime.now()
        start_end_date_validator(((start, end),), (('', ''),))

        end -= timedelta(days=1)
        self.assertRaises(ValidationError, start_end_date_validator,
                          ((start, end),), (('', ''),))

    def test_iban_validator(self):
        iban = 'GR4902603280000910200635494'

        try:
            iban_validation(iban)
        except ValidationError:
            self.fail("iban_validation raised ValidationError!")

        iban = 'GR4902603280000910200'
        self.assertRaises(ValidationError, iban_validation, iban)

        iban = 'G4902603280000910200635494'
        self.assertRaises(ValidationError, iban_validation, iban)

        iban = ''
        self.assertRaises(ValidationError, iban_validation, iban)
