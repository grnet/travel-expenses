from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from texpenses.validators import dates_list_validator


class ValidatorTest(TestCase):

    def test_dates_list_validator(self):

        date1 = datetime.now() + timedelta(1)
        date2 = None

        date3 = datetime.now() - timedelta(days=2)

        secretary_dates = (date1, date2, date3, )

        secretary_dates_labels = ('date1', 'date2', 'date3')

        self.assertRaises(ValidationError, dates_list_validator,
                          secretary_dates, secretary_dates_labels)
