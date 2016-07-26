from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from texpenses.validators import dates_list_validator


class ValidatorTest(TestCase):

    def test_dates_list_validator(self):

        # test method when all dates are none

        date1 = None
        date2 = None
        date3 = None

        secretary_dates = (date1, date2, date3, )
        secretary_dates_labels = ('date1', 'date2', 'date3')

        dates_list_validator(secretary_dates, secretary_dates_labels)

        # test method with empty date tuples
        secretary_dates = ()
        secretary_dates_labels = ()
        dates_list_validator(secretary_dates, secretary_dates_labels)

        # test method with arbitrary data tuples
        now = datetime.now().date()
        date1 = now + timedelta(1)
        date2 = None
        date3 = now - timedelta(days=2)

        secretary_dates = (date1, date2, date3, )
        secretary_dates_labels = ('date1', 'date2', 'date3')

        self.assertRaises(ValidationError, dates_list_validator,
                          secretary_dates, secretary_dates_labels)
