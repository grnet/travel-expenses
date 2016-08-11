from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from texpenses.validators import date_validator, start_end_date_validator


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
