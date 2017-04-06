import logging
from datetime import datetime, date
from django.core.exceptions import ValidationError
from stdnum import iban
from stdnum.gr import vat
logger = logging.getLogger(__name__)


def required_validator(obj, fields=()):
    for field in fields:
        if not getattr(obj, field, None):
            raise ValidationError('Field %s is required' % repr(field))


def iban_validation(value):
    try:
        iban.validate(value)
    except Exception as ex:
        raise ValidationError(ex.message)


def afm_validator(value):
    try:
        vat.validate(value)
    except Exception as ex:
        raise ValidationError(ex.message)


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
