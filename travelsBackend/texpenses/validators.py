import logging
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

logger = logging.getLogger(__name__)


iban_validation = RegexValidator(
    r'^^GR\d{9}[0-9A-Z]{16}$', 'IBAN number is not valid.')


def required_validator(obj, required_fields):
    for field in required_fields:
        if not getattr(obj, field, None):
            raise ValidationError('Field %s is required' % repr(field))


def afm_validator(value):
    NUM_DIGITS = 9
    if not value.isdigit():
        raise ValidationError(
            'AFM is not valid; it should include only digits')

    if all(int(v) == 0 for v in value):
        raise ValidationError(
            'AFM is not valid; it should not contain zero digits')

    if len(value) != NUM_DIGITS:
        raise ValidationError('AFM is not valid; it should contain 9 digits')

    last_digit = value[-1]
    total = sum(int(digit) * 2 ** ((NUM_DIGITS - 1) - i)
                for i, digit in enumerate(value[:-1]))
    if int(last_digit) != total % 11:
        raise ValidationError(
            'AFM is not valid; It does not conform to the general rules')


def date_validator(start_date, end_date, labels):
    """
    This validator checks if two given dates (starting date and ending date)
    are valid.

    Valid dates are dates which are after today and starting date is before
    ending date.

    :param start_date: Starting date.
    :param end_date: Ending date.
    :labels: tuple which contains labels for the start_date and end_date
    fields respectively.

    :raises: VallidationError if two given dates are not valid.
    """
    now = datetime.now()
    start_label, end_label = labels
    if start_date < now:
        raise ValidationError('%s date should be after today' % (start_label))

    if end_date < now:
        raise ValidationError('%s date should be after today' % (end_label))

    if end_date < start_date:
        raise ValidationError(
            '%s date should be after %s date' % (
                end_label, start_label))
