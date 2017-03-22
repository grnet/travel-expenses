import logging
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

logger = logging.getLogger(__name__)


iban_validation = RegexValidator(
    r'^^GR\d{9}[0-9A-Z]{16}$', 'IBAN number is not valid.')


def required_validator(obj, fields=()):
    for field in fields:
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
    if int(last_digit) != (total % 11) % 10:
        raise ValidationError(
            'AFM is not valid; It does not conform to the general rules')


def start_end_date_validator(dates, labels):
    """
    Validates that end dates are after from start dates.

    :param dates: An iterable of pairs (a start date and end date) to be
    compared.
    :param labels: An iterable of labels which correspond to the objects.
    """
    for i, (start, end) in enumerate(dates):
        start_label, end_label = labels[i]
        if end < start:
            raise ValidationError('%s date should be after %s date.' % (
                repr(end_label), repr(start_label)))


def date_validator(field, value):
    """
    This validator checks if a given object (date or datetime) is after from
    current date.

    :param value: Date of Datetime object.

    :raises: VallidationError if given date or datetime object is not after
    from current day.
    """
    now = datetime.now().date() if type(value) is date else datetime.now()
    if value and value <= now:
        raise ValidationError('The {} date field should be after today.'.
                              format(field))
